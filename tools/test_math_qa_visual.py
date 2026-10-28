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

    def test_final_rejects_logo_only_evidence(self):
        report = self.report()
        report['image_checks'] = [{
            'image_id': 'frame.png',
            'logo_overlap': {'status': 'pass', 'evidence': 'Logo clear of content'},
        }]
        with self.assertRaisesRegex(ValueError, 'delivery_cleanliness'):
            validate_report(report, ['frame.png'], stage='final')

    def test_delivery_cleanliness_is_required_in_assets(self):
        report = self.report()
        del report['image_checks'][0]['delivery_cleanliness']
        with self.assertRaisesRegex(ValueError, 'delivery_cleanliness'):
            validate_report(report, ['frame.png'])

    def test_production_artifacts_require_blocker_in_both_stages(self):
        for stage in ('assets', 'final'):
            with self.subTest(stage=stage):
                report = self.report()
                report['verdict'] = 'fail'
                report['image_checks'][0]['delivery_cleanliness'] = {
                    'status': 'fail', 'evidence': 'Visible VÙNG LOGO AN TOÀN at top right',
                }
                report['issues'] = [{
                    'severity': 'fix', 'location': 'frame.png',
                    'evidence': 'Production-only safe-zone label visible',
                    'message': 'Remove debug layer from export',
                }]
                with self.assertRaisesRegex(ValueError, 'blocker'):
                    validate_report(report, ['frame.png'], stage=stage)
                report['issues'][0]['severity'] = 'blocker'
                validate_report(report, ['frame.png'], stage=stage)
                report['verdict'] = 'pass'
                with self.assertRaises(ValueError):
                    validate_report(report, ['frame.png'], stage=stage)

    def test_final_accepts_logo_and_cleanliness_evidence(self):
        validate_report(self.report(), ['frame.png'], stage='final')


if __name__ == '__main__':
    unittest.main()
