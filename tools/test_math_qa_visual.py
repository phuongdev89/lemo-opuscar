"""Regression checks for typography evidence; no provider calls."""
import unittest

from math_qa import ASSET_VISUAL_CHECKS, validate_report


class VisualEvidenceTests(unittest.TestCase):
    def report(self):
        return {
            'verdict': 'pass', 'independent_solution': 'E',
            'coverage': 'Fixture image only', 'issues': [],
            'image_checks': [{
                'image_id': 'frame.png',
                **{name: {'status': 'pass', 'evidence': 'Observed fixture evidence'}
                   for name in ASSET_VISUAL_CHECKS},
            }],
        }

    def test_old_readability_only_contract_is_rejected(self):
        report = self.report()
        for name in ('glyph_integrity', 'font_consistency', 'text_overlap'):
            del report['image_checks'][0][name]
        with self.assertRaises(ValueError):
            validate_report(report, ['frame.png'])

    def test_missing_typography_evidence_is_rejected(self):
        for name in ('glyph_integrity', 'font_consistency', 'text_overlap'):
            with self.subTest(name=name):
                report = self.report()
                report['image_checks'][0][name]['evidence'] = ''
                with self.assertRaises(ValueError):
                    validate_report(report, ['frame.png'])

    def test_pass_cannot_hide_failure_or_uncertainty(self):
        for name in ASSET_VISUAL_CHECKS:
            for status in ('fail', 'insufficient_evidence'):
                with self.subTest(name=name, status=status):
                    report = self.report()
                    report['image_checks'][0][name]['status'] = status
                    with self.assertRaises(ValueError):
                        validate_report(report, ['frame.png'])

    def test_complete_evidence_passes(self):
        validate_report(self.report(), ['frame.png'])

    def test_final_remains_logo_only(self):
        report = self.report()
        report['image_checks'] = [{
            'image_id': 'frame.png',
            'logo_overlap': {'status': 'pass', 'evidence': 'Logo clear of content'},
        }]
        validate_report(report, ['frame.png'], stage='final')


if __name__ == '__main__':
    unittest.main()
