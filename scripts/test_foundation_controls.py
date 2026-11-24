"""Regression checks for unpublished page and evidence integrity."""
import tempfile
import unittest
from pathlib import Path

from build_foundations import FOUND, load_cards, load_evidence


class ControlTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sources, cls.claims = load_evidence()
        cls.sample = (FOUND/'manuscripts/01-pilot.cards').read_text().strip().split('\n\n')[0]

    def load(self, text):
        with tempfile.TemporaryDirectory() as tmp:
            manuscript = Path(tmp)/'test.cards'
            manuscript.write_text(text+'\n')
            return load_cards([manuscript],self.claims)

    def test_review_only_status(self):
        card = self.load(self.sample)['Z01-P01']
        self.assertEqual(card['publication'],'HOLD')
        self.assertIn('pending',card['technical_review'])

    def test_duplicate_page_ids_rejected(self):
        with self.assertRaisesRegex(ValueError,'duplicate page ID'):
            self.load(self.sample+'\n\n'+self.sample)

    def test_unknown_claim_is_rejected(self):
        with self.assertRaisesRegex(ValueError,'Broken claim links'):
            self.load(self.sample.replace('@T01','@NO-SOURCE'))

    def test_missing_reviewer_is_rejected(self):
        content = self.sample.split('\nreviewer:')[0]
        with self.assertRaisesRegex(ValueError,'Incomplete page'):
            self.load(content)

    def test_no_explicit_publication_override(self):
        with self.assertRaisesRegex(ValueError,'Unexpected field'):
            self.load(self.sample+'\npublication: PUBLISH')


if __name__ == '__main__':
    unittest.main()
