import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import math_qa as qa


class MathQATest(unittest.TestCase):
    def test_disabled_never_reads_inputs_or_calls_api(self):
        for flag in ('', 'false', '1', 'yes'):
            with patch.object(qa, 'load_config', return_value={'AI_QA_REQUIRED': flag}), \
                 patch.object(qa, 'prepare') as prepare, \
                 patch.object(qa, 'request_review') as request, contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(qa.main(['--manifest', 'missing.json']), 0)
                prepare.assert_not_called()
                request.assert_not_called()

    def test_missing_config_blocks_without_network(self):
        with patch.object(qa, 'load_config', return_value={'AI_QA_REQUIRED': 'true'}), \
             patch.object(qa, 'request_review') as request, contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(qa.main([]), 2)
            request.assert_not_called()

    def test_overlay_preserves_other_keys(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / '.env').write_text('AI_QA_MODEL=shared\nAI_QA_KEY=secret\n')
            (root / '.env.math').write_text('AI_QA_MODEL=math\nAI_QA_REQUIRED=false\n')
            with patch.dict(qa.os.environ, {'AI_QA_URL': 'https://example.test/v1'}):
                cfg = qa.load_config(root)
            self.assertEqual(cfg['AI_QA_MODEL'], 'math')
            self.assertEqual(cfg['AI_QA_KEY'], 'secret')
            self.assertEqual(cfg['AI_QA_URL'], 'https://example.test/v1')

    def test_contradictory_pass_rejected(self):
        with self.assertRaises(ValueError):
            qa.validate_report({'verdict': 'pass', 'independent_solution': '2',
                'coverage': 'frame', 'issues': [{'severity': 'fix', 'location': 'a',
                'evidence': 'b', 'message': 'c'}]})

    def test_actual_images_and_final_gate(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for name in ('problem.md', 'solution.md', 'narration.md'):
                (root / name).write_text('test', encoding='utf-8')
            (root / 'frame.png').write_bytes(b'image-bytes')
            (root / 'final.mp4').write_bytes(b'final-video')
            manifest = {'mode': 'guided', 'grade': '2', 'problem': 'problem.md',
                'solution': 'solution.md', 'narration': 'narration.md',
                'video': 'final.mp4', 'images': [{'path': 'frame.png', 'timestamp': 1}]}
            path = root / 'qa-input-final.json'
            path.write_text(json.dumps(manifest))
            def extract(command, **kwargs):
                Path(command[-1]).write_bytes(b'actual-extracted-frame')
                return type('Result', (), {'returncode': 0})()
            self.addCleanup(patch.stopall)
            patch.object(qa.subprocess, 'run', side_effect=extract).start()
            content, fingerprints = qa.prepare(path, 'final')
            self.assertTrue(content[-1]['image_url']['url'].startswith('data:image/png;base64,'))
            self.assertIn('qa-extracted-final/00.png', fingerprints)
            self.assertIn('final.mp4', fingerprints)
            self.assertNotIn('frame.png', fingerprints)
            self.assertNotIn('problem.md', fingerprints)
            self.assertEqual(set(json.loads(content[0]['text'])), {'stage', 'image_ids'})
            # Final QA needs no lesson documents, even on disk.
            for key in ('problem', 'solution', 'narration', 'grade', 'mode'):
                manifest.pop(key)
            path.write_text(json.dumps(manifest))
            qa.prepare(path, 'final')
            manifest['images'][0]['role'] = 'cover'
            path.write_text(json.dumps(manifest))
            with self.assertRaises(ValueError):
                qa.prepare(path, 'final')
            manifest['images'][0]['role'] = 'frame'
            manifest.pop('video')
            path.write_text(json.dumps(manifest))
            with self.assertRaisesRegex(ValueError, 'requires video'):
                qa.prepare(path, 'final')
            manifest['video'] = 'final.mp4'
            path.write_text(json.dumps(manifest))
            cfg = {'AI_QA_REQUIRED': 'true', 'AI_QA_MODEL': 'gpt-6-luna',
                   'AI_QA_KEY': 'test', 'AI_QA_URL': 'https://example.test/v1'}
            for verdict, code in (('pass', 0), ('fail', 1), ('insufficient_evidence', 1)):
                with patch.object(qa, 'load_config', return_value=cfg), \
                     patch.object(qa, 'request_review', return_value={'verdict': verdict}) as request, \
                     contextlib.redirect_stdout(io.StringIO()):
                    self.assertEqual(qa.main(['--manifest', str(path), '--stage', 'final']), code)
                    request.assert_called_once()
                self.assertEqual(json.loads((root / 'qa-final.json').read_text())['verdict'], verdict)
            with patch.object(qa, 'load_config', return_value=cfg), \
                 patch.object(qa, 'request_review', side_effect=RuntimeError('QA failed')), \
                 contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(qa.main(['--manifest', str(path), '--stage', 'final']), 2)
            self.assertEqual(json.loads((root / 'qa-final.json').read_text())['verdict'], 'error')
            manifest['images'][0].pop('timestamp')
            path.write_text(json.dumps(manifest))
            with self.assertRaises(ValueError):
                qa.prepare(path, 'final')

    def test_logo_checks_cannot_be_omitted_or_contradict_pass(self):
        report = {'verdict': 'pass', 'independent_solution': '5', 'coverage': 'frame', 'issues': []}
        with self.assertRaises(ValueError):
            qa.validate_report(report, ['frame.png'])
        check = {'image_id': 'frame.png', 'logo_overlap': {'status': 'pass', 'evidence': 'Logo clear of header'},
                 'readability': {'status': 'pass', 'evidence': 'All labels readable'}}
        report['image_checks'] = [check]
        qa.validate_report(report, ['frame.png'])

        with self.assertRaises(ValueError):
            qa.validate_report(report, ['frame.png', 'missing.png'])
        check['logo_overlap']['status'] = 'fail'
        with self.assertRaises(ValueError):
            qa.validate_report(report, ['frame.png'])
        report['verdict'] = 'fail'
        report['issues'] = [{'severity': 'fix', 'location': 'frame.png',
            'evidence': 'logo covers header', 'message': 'move logo'}]
        with self.assertRaisesRegex(ValueError, 'blocker'):
            qa.validate_report(report, ['frame.png'])
        report['issues'][0]['severity'] = 'blocker'
        qa.validate_report(report, ['frame.png'])

    def test_final_logo_report_does_not_require_solution_or_readability(self):
        report = {'verdict': 'pass', 'coverage': 'logo in supplied frame only', 'issues': [],
                  'image_checks': [{'image_id': 'frame.png', 'logo_overlap': {
                      'status': 'pass', 'evidence': 'Logo inside frame, clear of header and diagram'}}]}
        qa.validate_report(report, ['frame.png'], stage='final')
        with self.assertRaises(ValueError):
            qa.validate_report(report, ['frame.png'], stage='assets')
        report['image_checks'][0]['logo_overlap']['status'] = 'fail'
        with self.assertRaises(ValueError):
            qa.validate_report(report, ['frame.png'], stage='final')

    def test_final_request_uses_short_logo_prompt(self):
        report = {'verdict': 'pass', 'coverage': 'one frame', 'issues': [],
                  'image_checks': [{'image_id': 'scene-1', 'logo_overlap': {
                      'status': 'pass', 'evidence': 'Logo clear of header'}}]}
        data = {'choices': [{'finish_reason': 'stop', 'message': {'content': json.dumps(report)}}]}
        content = [{'type': 'text', 'text': json.dumps({'stage': 'final', 'image_ids': ['scene-1']})}]
        response = io.BytesIO(json.dumps(data).encode())
        with patch.object(qa.urllib.request, 'urlopen', return_value=response) as network:
            qa.request_review({'AI_QA_URL': 'https://example.test/v1',
                               'AI_QA_KEY': 'test', 'AI_QA_MODEL': 'test'}, content)
        payload = json.loads(network.call_args.args[0].data)
        self.assertEqual(payload['messages'][0]['content'], qa.LOGO_SYSTEM)
        self.assertNotIn('independent_solution', payload['messages'][0]['content'])
        self.assertEqual(payload['messages'][1]['content'], content)



if __name__ == '__main__':
    unittest.main()
