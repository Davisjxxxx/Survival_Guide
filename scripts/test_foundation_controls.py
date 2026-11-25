"""Regression checks for unpublished page, evidence integrity, canonical scope, and domain contradiction guards."""
import csv
import re
import tempfile
import unittest
from pathlib import Path

from build_foundations import ALL_16_ZONES, FOUND, ROOT, valid_card_id, active_zones, inline_emphasis, load_cards, load_evidence
from foundation_diagrams import validate_spec


def _norm_domain(value):
    return ' '.join(value.lower().replace('&', 'and').split())


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
        second = self.sample.replace('Z01-P01', 'Z01-P02')
        with self.assertRaisesRegex(ValueError, 'Duplicate card title'):
            self.load(self.sample + '\n\n' + second)

    def test_clarity_potability_contradiction_rejected(self):
        bad = self.sample.replace('Pause on stable ground', 'Clear water is safe to drink')
        with self.assertRaisesRegex(ValueError, 'visual clarity potability'):
            self.load(bad)

    def test_unvalidated_structural_load_rejected(self):
        shelter = self.sample.replace('Z01-P01', 'Z02-P01').replace(
            'Pause on stable ground', 'This roof supports 400 pounds of snow load'
        )
        with self.assertRaisesRegex(ValueError, 'unvalidated structural load'):
            self.load(shelter)

    def test_z09_unvalidated_cordage_rating_rejected(self):
        tool = self.sample.replace('Z01-P01', 'Z09-P01').replace(
            'Pause on stable ground', 'This improvised rope has a safe working load 300 lb for lifting'
        )
        with self.assertRaisesRegex(ValueError, 'unvalidated cordage/rigging'):
            self.load(tool)

    def test_z11_moss_north_myth_rejected(self):
        nav = self.sample.replace('Z01-P01', 'Z11-P01').replace(
            'Pause on stable ground', 'Moss always grows on the north side of trees to guide travel'
        )
        with self.assertRaisesRegex(ValueError, 'moss-north folklore'):
            self.load(nav)

    def test_z12_safe_ice_claim_rejected(self):
        env = self.sample.replace('Z01-P01', 'Z12-P01').replace(
            'Pause on stable ground', 'Foot tracks prove safe ice across the lake'
        )
        with self.assertRaisesRegex(ValueError, 'unsafe universal ice'):
            self.load(env)

    def test_z12_swim_against_rip_rejected(self):
        env = self.sample.replace('Z01-P01', 'Z12-P01').replace(
            'Pause on stable ground', 'Swim directly against the rip current toward the beach'
        )
        with self.assertRaisesRegex(ValueError, 'unsafe rip-current'):
            self.load(env)


    def test_combustion_warning_on_other_line_does_not_exempt_action(self):
        text = self.sample.replace(
            'action: Pause on stable ground and check the scene before approaching an injured person.',
            'action: Operate the stove in a tent. Never ignore the weather.',
        )
        with self.assertRaisesRegex(ValueError,'enclosed combustion'):
            self.load(text)

    def test_figure_spec_rejects_misspelled_branch_and_cue_keys(self):
        with self.assertRaisesRegex(ValueError,'Invalid figure specification'):
            validate_spec('Z02-P42',{'type':'failure_mode','cause':'snow','symptom':'crack','correction':'leave'})

    def test_figure_spec_rejects_truncated_component_lists(self):
        with self.assertRaisesRegex(ValueError,'Invalid figure label list'):
            validate_spec('Z09-P01',{'type':'mechanism','nodes':['a','b','c','d'],'callout':'Check'})

    def test_editorial_emphasis_escapes_literal_markup(self):
        self.assertEqual(inline_emphasis('**Urgent** <a>'), '<strong>Urgent</strong> &lt;a&gt;')


    def test_zone_five_supports_full_allocation_without_changing_old_ids(self):
        self.assertTrue(valid_card_id('Z05-P135'))
        self.assertFalse(valid_card_id('Z05-P136'))
        self.assertFalse(valid_card_id('Z05-P001'))
        self.assertFalse(valid_card_id('Z05-P00'))
        self.assertTrue(valid_card_id('Z01-P01'))

    def test_active_zones_are_discovered_without_promoting_starter_reconstructions(self):
        self.assertEqual(active_zones([{'id':'Z05-P100','zone':'Z05'},
                                       {'id':'Z13-R03','zone':'Z13'}]), ['Z05'])

    def test_canonical_sixteen_zone_scope_matches_master_matrix(self):
        """Verify every zone ID, canonical domain, and planned page count matches frozen master scope."""
        frozen_path = ROOT / 'project/planning/ZONE_COMPLETION_MATRIX.csv'
        with frozen_path.open(encoding='utf-8', newline='') as f:
            frozen_rows = {r['zone']: (_norm_domain(r['domain']), int(r['draft_pages'])) for r in csv.DictReader(f)}
        self.assertEqual(len(frozen_rows), 16)
        self.assertEqual(sum(pages for _, pages in frozen_rows.values()), 1016)

        # Authoritative check against build_foundations.ALL_16_ZONES
        code_rows = {z: (_norm_domain(d), p) for z, d, p, _ in ALL_16_ZONES}
        self.assertEqual(code_rows, frozen_rows)
        self.assertEqual(code_rows['Z05'], ('wild foods and poisonous lookalikes', 135))
        self.assertEqual(code_rows['Z08'], ('rocks, minerals and materials', 60))
        self.assertEqual(code_rows['Z10'], ('wilderness medicine', 80))

        # Check foundations/ZONE_COMPLETION_MATRIX.csv matches per-zone canonical scope
        active_matrix = FOUND / 'ZONE_COMPLETION_MATRIX.csv'
        with active_matrix.open(encoding='utf-8', newline='') as f:
            active_rows = {r['zone']: (_norm_domain(r['domain']), int(r['planned_pages'])) for r in csv.DictReader(f)}
        self.assertEqual(active_rows, frozen_rows)

        # Check NEON_CONTINUATION_HANDOFF.md table rows match canonical zone-domain-allocation triplets
        handoff = (FOUND / 'audit/NEON_CONTINUATION_HANDOFF.md').read_text(encoding='utf-8')
        table_rows = re.findall(r'^\|\s*\d+\s*\|\s*(Z\d{2})\s+([^|]+?)\s*\|\s*(\d+)\s*\|', handoff, flags=re.M)
        self.assertGreaterEqual(len(table_rows), 9)
        for zid, domain, alloc in table_rows:
            self.assertIn(zid, frozen_rows)
            self.assertEqual(_norm_domain(domain), frozen_rows[zid][0], f'Domain mismatch for {zid}')
            self.assertEqual(int(alloc), frozen_rows[zid][1], f'Allocation mismatch for {zid}')

    def test_z10_medicine_guards_reject_dosage_surgery_and_snow_rubbing(self):
        med_dose = self.sample.replace('Z01-P01', 'Z10-P01').replace(
            'Pause on stable ground', 'Give 800 mg of ibuprofen every four hours'
        )
        with self.assertRaisesRegex(ValueError, 'unauthorized lay medication dosage'):
            self.load(med_dose)
        med_bite = self.sample.replace('Z01-P01', 'Z10-P01').replace(
            'Pause on stable ground', 'Cut the snakebite wound and suck venom out quickly'
        )
        with self.assertRaisesRegex(ValueError, 'unsafe invasive field medical procedure'):
            self.load(med_bite)
        med_frost = self.sample.replace('Z01-P01', 'Z10-P01').replace(
            'Pause on stable ground', 'Rub frostbitten toes vigorously with snow'
        )
        with self.assertRaisesRegex(ValueError, 'unsafe frostbite snow-rubbing'):
            self.load(med_frost)

    def test_z13_utilities_guard_rejects_generator_backfeeding(self):
        util = self.sample.replace('Z01-P01', 'Z13-P01').replace(
            'Pause on stable ground', 'Plug the portable generator directly into a dryer outlet'
        )
        with self.assertRaisesRegex(ValueError, 'unsafe generator backfeeding'):
            self.load(util)

    def test_z14_preservation_guard_rejects_oven_and_waterbath_low_acid(self):
        oven = self.sample.replace('Z01-P01', 'Z14-P02').replace(
            'Pause on stable ground', 'Use oven canning to seal vegetable jars quickly'
        )
        with self.assertRaisesRegex(ValueError, 'unsafe canning method'):
            self.load(oven)
        low_acid = self.sample.replace('Z01-P01', 'Z14-P02').replace(
            'Pause on stable ground', 'Water-bath can low-acid green beans for two hours'
        )
        with self.assertRaisesRegex(ValueError, 'unsafe water-bath canning'):
            self.load(low_acid)

    def test_z15_disaster_guard_rejects_flood_crossing_and_overpass_shelter(self):
        flood = self.sample.replace('Z01-P01', 'Z15-P01').replace(
            'Pause on stable ground', 'Drive through the flooded road slowly in low gear'
        )
        with self.assertRaisesRegex(ValueError, 'unsafe floodwater crossing'):
            self.load(flood)
        overpass = self.sample.replace('Z01-P01', 'Z15-P01').replace(
            'Pause on stable ground', 'Shelter under a highway overpass if a tornado approaches'
        )
        with self.assertRaisesRegex(ValueError, 'unsafe tornado overpass'):
            self.load(overpass)

    def test_new_p12_p15_diagram_contracts_validate_strictly(self):
        validate_spec('Z10-P01', {
            'type': 'escalation_ladder',
            'tiers': [
                {'role': 'Lay responder', 'scope': 'Scene & pressure', 'action': 'Stop bleeding'},
                {'role': '911 Dispatcher', 'scope': 'Guided actions', 'action': 'Follow instructions'},
                {'role': 'EMS / Clinician', 'scope': 'Definitive care', 'action': 'Transport & treat'},
            ],
            'trigger': 'Escalate early for red flags',
        })
        with self.assertRaisesRegex(ValueError, 'Invalid sequence step'):
            validate_spec('Z10-P02', {
                'type': 'sequence_plate',
                'steps': [{'label': '1', 'detail': 'a'}, {'label': '2', 'detail': 'b'},
                          {'label': '3', 'detail': 'c'}, {'wrong': '4'}],
                'cue': 'Check', 'variant': 'bleeding',
            })


if __name__ == '__main__':
    unittest.main()
