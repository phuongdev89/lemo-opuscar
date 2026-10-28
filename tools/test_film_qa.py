"""General QA configuration and real preparation-path regression tests."""
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import math_qa as qa


class FilmQATests(unittest.TestCase):
    def test_config_math_overlay_only_for_math(self):
        with tempfile.TemporaryDirectory() as folder, patch.dict(os.environ, {}, clear=True):
            root = Path(folder)
            (root / '.env').write_text('AI_QA_REQUIRED=true\nAI_QA_MODEL=shared\n')
            (root / '.env.math').write_text('AI_QA_REQUIRED=false\nAI_QA_MODEL=math\n')
            self.assertTrue(qa.enabled(qa.load_config(root, film_type='general')))
            self.assertFalse(qa.enabled(qa.load_config(root, film_type='math')))
            self.assertEqual(qa.load_config(root)['AI_QA_MODEL'], 'math')

    def test_overlay_preserves_unspecified_keys(self):
        with tempfile.TemporaryDirectory() as folder, patch.dict(os.environ, {'AI_QA_MODEL': 'env'}, clear=True):
            root = Path(folder)
            (root / '.env').write_text('AI_QA_REQUIRED=false\n')
            (root / '.env.math').write_text('AI_QA_REQUIRED=TRUE\n')
            self.assertTrue(qa.enabled(qa.load_config(root)))
            self.assertEqual(qa.load_config(root)['AI_QA_MODEL'], 'env')
            self.assertFalse(qa.enabled(qa.load_config(root, film_type='general')))

    def test_general_style_and_assets_without_math_fields(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            for name in ('brief', 'style', 'proposal', 'narration'):
                (root / (name + '.md')).write_text(name)
            manifest = {name: name + '.md' for name in ('brief', 'style', 'proposal', 'narration')}
            path = root / 'input.json'
            path.write_text(json.dumps(manifest))
            content, _ = qa.prepare(path, 'style', film_type='general')
            context = json.loads(content[0]['text'])
            self.assertEqual(context['film_type'], 'general')
            self.assertEqual(context['brief'], 'brief')
            self.assertNotIn('grade', context)
            (root / 'frame.png').write_bytes(b'fixture')
            manifest['images'] = [{'path': 'frame.png'}]
            path.write_text(json.dumps(manifest))
            content, _ = qa.prepare(path, 'assets', film_type='general')
            self.assertEqual(json.loads(content[0]['text'])['narration'], 'narration')
            with self.assertRaises(ValueError):
                qa.prepare(path, 'assets')

    def test_prompts_route_by_film_type(self):
        self.assertEqual(qa.system_prompt('assets', 'math'), qa.SYSTEM)
        self.assertEqual(qa.system_prompt('style', 'general'), qa.GENERAL_STYLE_SYSTEM)
        self.assertIn('logo_required', qa.system_prompt('final', 'general'))
        self.assertIn('assessment', qa.system_prompt('assets', 'general'))

    def test_general_report_contract(self):
        report = {
            'verdict': 'pass', 'assessment': 'Brief and facts reviewed',
            'coverage': 'Submitted frame', 'issues': [],
            'image_checks': [{'image_id': 'frame.png', **{
                field: {'status': 'pass', 'evidence': 'Observed evidence'}
                for field in qa.ASSET_VISUAL_CHECKS}}],
        }
        qa.validate_report(report, ['frame.png'], film_type='general')
        with self.assertRaises(ValueError):
            qa.validate_report(report, ['frame.png'], film_type='math')
        report['image_checks'][0]['readability']['status'] = 'fail'
        with self.assertRaises(ValueError):
            qa.validate_report(report, ['frame.png'], film_type='general')

    def test_disabled_makes_no_request(self):
        with patch.object(qa, 'load_config', return_value={}), patch.object(qa, 'request_review') as request:
            self.assertEqual(qa.main([], default_film_type='general'), 0)
            request.assert_not_called()

    def test_enabled_missing_config_blocks(self):
        with patch.object(qa, 'load_config', return_value={'AI_QA_REQUIRED': 'true'}), patch.object(qa, 'request_review') as request:
            self.assertEqual(qa.main([], default_film_type='general'), 2)
            request.assert_not_called()

if __name__ == '__main__':
    unittest.main()
