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
            manifest = {'mode': 'guided', 'grade': '2', 'problem': 'problem.md',
                'solution': 'solution.md', 'narration': 'narration.md',
                'images': [{'path': 'frame.png', 'timestamp': 1}]}
            path = root / 'qa-input-final.json'
            path.write_text(json.dumps(manifest))
            content, fingerprints = qa.prepare(path, 'final')
            self.assertTrue(content[-1]['image_url']['url'].startswith('data:image/png;base64,'))
            self.assertIn('frame.png', fingerprints)
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


if __name__ == '__main__':
    unittest.main()
