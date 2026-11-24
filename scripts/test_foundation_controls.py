"""Regression checks for unpublished page, evidence integrity, and contradiction guards."""
import tempfile
import unittest
from pathlib import Path

from build_foundations import FOUND, load_cards, load_evidence


class ControlTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sources, cls.claims = load_evidence()
        cls.sample = (FOUND / 'manuscripts/01-pilot.cards').read_text(encoding='utf-8').strip().split('\n\n')[0]

    def load(self, text, filename='test.cards'):
        with tempfile.TemporaryDirectory() as tmp:
            manuscript = Path(tmp) / filename
            manuscript.write_text(text + '\n', encoding='utf-8')
            return load_cards([manuscript], self.claims)

    def test_review_only_status(self):
        card = self.load(self.sample)['Z01-P01']
        self.assertEqual(card['publication'], 'HOLD')
        self.assertIn('pending', card['technical_review'])

    def test_duplicate_page_ids_rejected(self):
        with self.assertRaisesRegex(ValueError, 'duplicate page ID'):
            self.load(self.sample + '\n\n' + self.sample)

    def test_unknown_claim_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'Broken claim links'):
            self.load(self.sample.replace('@T01', '@NO-SOURCE'))

    def test_missing_reviewer_is_rejected(self):
        content = self.sample.split('\nreviewer:')[0]
        with self.assertRaisesRegex(ValueError, 'Incomplete page'):
            self.load(content)

    def test_no_explicit_publication_override(self):
        with self.assertRaisesRegex(ValueError, 'Unexpected field'):
            self.load(self.sample + '\npublication: PUBLISH')

    def test_expanded_batch_requires_failure_field(self):
        with self.assertRaisesRegex(ValueError, 'Missing failure recognition'):
            self.load(self.sample, filename='06-test.cards')

    def test_duplicate_title_rejected(self):
        second = self.sample.replace('Z01-P01', 'Z01-P99')
        with self.assertRaisesRegex(ValueError, 'Duplicate card title'):
            self.load(self.sample + '\n\n' + second)

    def test_clarity_potability_contradiction_rejected(self):
        bad = self.sample.replace('Pause on stable ground', 'Clear water is safe to drink')
        with self.assertRaisesRegex(ValueError, 'visual clarity potability'):
            self.load(bad)

    def test_unvalidated_structural_load_rejected(self):
        shelter = self.sample.replace('Z01-P01', 'Z02-P99').replace(
            'Pause on stable ground', 'This roof supports 400 pounds of snow load'
        )
        with self.assertRaisesRegex(ValueError, 'unvalidated structural load'):
            self.load(shelter)


if __name__ == '__main__':
    unittest.main()
