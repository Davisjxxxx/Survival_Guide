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

    def test_co_alarm_must_not_delay_evacuation_for_equipment(self):
        text = self.sample.replace('Z01-P01', 'Z13-P01')
        start = text.index('stop: ')
        finish = text.index('\n', start)
        unsafe = 'stop: A CO alarm requires shutting off the generator and evacuating everyone. @C07'
        with self.assertRaisesRegex(ValueError, 'CO evacuation delayed'):
            self.load(text[:start] + unsafe + text[finish:])

    def test_conflicting_tourniquet_placement_is_rejected(self):
        text = self.sample.replace('Z01-P01', 'Z10-P01')
        original = next(line for line in text.splitlines() if line.startswith('action: '))
        mixed = 'action: Place the tourniquet high and tight 2 to 3 inches above the wound. @M02'
        with self.assertRaisesRegex(ValueError, 'mixed tourniquet placement'):
            self.load(text.replace(original, mixed))

    def test_fixed_lay_cpr_delay_is_rejected(self):
        text = self.sample.replace('Z01-P01', 'Z10-P01')
        original = next(line for line in text.splitlines() if line.startswith('action: '))
        delay = 'action: Monitor breathing for a full minute before deciding on CPR. @M03'
        with self.assertRaisesRegex(ValueError, 'fixed lay breathing-check delay'):
            self.load(text.replace(original, delay))

    def test_expanded_batch_operational_editorial_only_action_is_rejected(self):
        text = self.sample.replace(' @T01', ' @ED', 1)
        text += '\nfailure: Exposure remains possible on an unverified route. @E01'
        with self.assertRaisesRegex(ValueError, 'needs a direct claim'):
            self.load(text, filename='17-test.cards')

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

    def test_z08_materials_guard_rejects_visual_safety_and_unprotected_dust(self):
        vis = self.sample.replace('Z01-P01', 'Z08-P01').replace(
            'Pause on stable ground', 'Visual appearance guarantees safe non-toxic stone for boiling'
        )
        with self.assertRaisesRegex(ValueError, 'unsafe visual material safety'):
            self.load(vis)
        dust = self.sample.replace('Z01-P01', 'Z08-P01').replace(
            'Pause on stable ground', 'Dry-grind quartz flakes without eye or dust protection'
        )
        with self.assertRaisesRegex(ValueError, 'unprotected mineral dust'):
            self.load(dust)

    def test_z06_harvest_guard_rejects_emergency_legal_exemption(self):
        harv = self.sample.replace('Z01-P01', 'Z06-P01').replace(
            'Pause on stable ground', 'An emergency automatically grants a legal exemption from fishing rules'
        )
        with self.assertRaisesRegex(ValueError, 'emergency legal harvest exemption'):
            self.load(harv)

    def test_z07_traps_guard_rejects_actionable_injurious_trap_construction(self):
        trap = self.sample.replace('Z01-P01', 'Z07-P01').replace(
            'Pause on stable ground', 'Set a wire snare along the narrow trail to catch small mammals'
        )
        with self.assertRaisesRegex(ValueError, 'actionable injurious trap'):
            self.load(trap)

    def test_z05_wild_foods_guard_rejects_edibility_folklore_and_photo_clearance(self):
        folk = self.sample.replace('Z01-P01', 'Z05-P01').replace(
            'Pause on stable ground', 'Rub sap on your lip to test edibility of an unknown plant'
        )
        with self.assertRaisesRegex(ValueError, 'universal edibility test'):
            self.load(folk)
        myth = self.sample.replace('Z01-P01', 'Z05-P01').replace(
            'Pause on stable ground', 'Boiling removes all mushroom toxins before eating'
        )
        with self.assertRaisesRegex(ValueError, 'folk toxicity test'):
            self.load(myth)
        pic = self.sample.replace('Z01-P01', 'Z05-P01').replace(
            'Pause on stable ground', 'A single photo authorizes consumption of a wild berry'
        )
        with self.assertRaisesRegex(ValueError, 'visual-only consumption clearance'):
            self.load(pic)

    def test_z16_atlas_guard_requires_upstream_zone_cross_reference(self):
        atlas = self.sample.replace('Z01-P01', 'Z16-P01').replace('B012-P01', 'Atlas standalone')
        with self.assertRaisesRegex(ValueError, 'upstream zone cross-reference'):
            self.load(atlas)

    def test_a02_handoff_matches_canonical_remaining_five_zones(self):
        handoff = (FOUND / 'audit/a02/NEON_FINAL_PRODUCTION_HANDOFF.md').read_text(encoding='utf-8')
        rows = re.findall(r'^\|\s*P\d{2}\s*\|\s*(Z\d{2})\s+([^|]+?)\s*\|\s*(\d+)\s*\|', handoff, flags=re.M)
        self.assertEqual(len(rows), 5)
        expected = {z: (_norm_domain(d), p) for z, d, p, _ in ALL_16_ZONES if z in {'Z05', 'Z06', 'Z07', 'Z08', 'Z16'}}
        found = {z: (_norm_domain(d), int(p)) for z, d, p in rows}
        self.assertEqual(found, expected)

    def test_p16_p20_domain_diagram_contracts_validate_strictly(self):
        validate_spec('Z05-P01', {
            'type': 'lookalike_diagnostic',
            'target_name': 'Target specimen', 'target_traits': ['Trait A', 'Trait B'],
            'toxic_name': 'Toxic lookalike', 'toxic_traits': ['Hazard A', 'Hazard B'],
            'exclusion': 'Stop if any key feature is absent', 'variant': 'plant_pair',
        })
        validate_spec('Z05-P90', {
            'type': 'fungal_anatomy',
            'features': ['Cap & cuticle', 'Free white gills', 'Annulus ring', 'Basal volva cup'],
            'scale': 'Scale: cm bar (conceptual)', 'hold': 'HOLD: No consumption clearance', 'variant': 'agaric_volva',
        })
        validate_spec('Z08-P01', {
            'type': 'geological_strata',
            'strata': ['Glacial till', 'Sedimentary bed', 'Crystalline bedrock'],
            'note': 'Regional survey context', 'hazard': 'Dust/collect rules apply', 'variant': 'strata',
        })
        with self.assertRaisesRegex(ValueError, 'Invalid figure label list'):
            validate_spec('Z05-P02', {
                'type': 'fungal_anatomy',
                'features': ['Only two', 'features'],
                'scale': 'cm', 'hold': 'HOLD', 'variant': 'agaric_volva',
            })

    def test_taxonomic_register_schema_when_present(self):
        reg = FOUND / 'evidence/z05-taxonomic-register.tsv'
        if not reg.exists():
            return
        with reg.open(encoding='utf-8', newline='') as f:
            rows = list(csv.DictReader(f, delimiter='\t'))
        self.assertGreaterEqual(len(rows), 6)
        required_cols = {
            'page_id', 'kingdom', 'accepted_binomial', 'authority', 'synonyms',
            'regional_scope', 'voucher_source', 'season', 'life_stage',
            'diagnostic_features', 'poisonous_lookalike', 'observable_exclusions',
            'image_provenance', 'image_rights', 'consumption_status', 'expert_review',
        }
        self.assertTrue(required_cols <= set(rows[0].keys()))
        for r in rows:
            self.assertEqual(r['consumption_status'], 'WITHHELD_HOLD')
            self.assertIn('PENDING', r['expert_review'])


    def test_a03_atlas_requires_real_page_targets(self):
        from build_foundations import validate_atlas_targets
        atlas = {'Z16-P01': {'id': 'Z16-P01', 'zone': 'Z16',
                             'action': [{'text': 'Open Z10-P50 for the full conditions.'}]}}
        with self.assertRaisesRegex(ValueError, 'invalid upstream atlas targets'):
            validate_atlas_targets(atlas)
        atlas['Z10-P50'] = {'id': 'Z10-P50', 'zone': 'Z10'}
        validate_atlas_targets(atlas)

    def test_a03_atlas_links_exact_source_pages_only(self):
        from build_foundations import statement
        rendered = statement({'text': 'Z10-P50 and Z10 are different references.', 'claims': ['T09']},
                             link_atlas=True)
        self.assertIn('href="Z10-P50.html"', rendered)
        self.assertNotIn('href="Z10.html"', rendered)

    def test_a03_zone_package_reference_rewrite(self):
        from check_foundations import LocalAssetCheck, scope_zone_links
        page = 'reader/Z16-P01.html'
        available = {page, 'reader/index.html'}
        original = '<a href="index.html">Index</a><a class="atlas-link" href="Z01-P01.html">Z01-P01</a>'
        scoped = scope_zone_links(page, original, available)
        self.assertIn('href="index.html"', scoped)
        self.assertIn('Z01-P01 (full edition)', scoped)
        self.assertNotIn('href="Z01-P01.html"', scoped)
        LocalAssetCheck(page, available).feed(scoped)
        with self.assertRaisesRegex(ValueError, 'Broken packaged reference'):
            LocalAssetCheck(page, available).feed('<img src="missing.svg">')

    def test_a03_v01_sources_preserve_illustration_boundary(self):
        from xml.etree import ElementTree
        from foundation_diagrams import v01_source_path
        ns = '{http://www.w3.org/2000/svg}'
        pilot = v01_source_path('Z14-P54')
        root = ElementTree.parse(pilot).getroot()
        self.assertIsNotNone(root.find(ns + 'desc'))
        self.assertIn('NOT TO SCALE', pilot.read_text())
        self.assertFalse(list(root.iter(ns + 'image')))

    def test_v02_reconstructed_svgs_preserve_originals_and_boundaries(self):
        import json
        from xml.etree import ElementTree
        from build_foundations import FOUND
        from foundation_diagrams import v02_source_path
        ns = '{http://www.w3.org/2000/svg}'
        specs = json.loads((FOUND / 'evidence/diagram-specs.json').read_text(encoding='utf-8'))
        v02_ids = sorted(cid for cid, spec in specs.items() if spec.get('type') == 'v02_artwork')
        self.assertGreaterEqual(len(v02_ids), 64)
        for cid in v02_ids:
            rev = v02_source_path(cid)
            orig = FOUND / 'visual/v02_technical/original' / f'{cid}.svg'
            self.assertTrue(rev.is_file(), f'Missing V02 revised SVG: {cid}')
            self.assertTrue(orig.is_file(), f'Missing preserved V02 original SVG: {cid}')
            root = ElementTree.parse(rev).getroot()
            desc = root.find(ns + 'desc')
            self.assertIsNotNone(desc, f'Missing <desc> in {cid}')
            self.assertTrue(bool(desc.text and desc.text.strip()))
            self.assertIn('NOT TO SCALE', rev.read_text(encoding='utf-8'))
            self.assertFalse(list(root.iter(ns + 'image')), f'Unexpected raster image in vector SVG {cid}')

    def test_v03_authentic_photo_provenance_and_hold(self):
        import hashlib, json
        from build_foundations import FOUND
        v03 = FOUND / 'visual/v03_authentic_photos'
        records = json.loads((v03 / 'MANIFEST.json').read_text(encoding='utf-8'))
        self.assertGreaterEqual(len(records), 30)
        for rec in records:
            orig = (v03 / rec['original_file']).read_bytes()
            disp = (v03 / rec['delivery_derivative']).read_bytes()
            self.assertTrue(orig.startswith(b'\xff\xd8'), f'Invalid JPEG: {rec["original_file"]}')
            self.assertEqual(hashlib.sha256(orig).hexdigest(), rec['original_sha256'])
            self.assertEqual(hashlib.sha256(disp).hexdigest(), rec['derivative_sha256'])
            self.assertEqual(rec['expert_validation_status'], 'PENDING')
            self.assertEqual(rec['diagnostic_qualification'], 'WITHHELD')

    def test_v02_v03_governance_registers_and_atlas_preservation(self):
        import csv
        from build_foundations import FOUND
        visual = FOUND / 'visual'
        with (visual / 'V02_BACKLOG_RECONCILIATION.csv').open(encoding='utf-8') as f:
            self.assertEqual(len(list(csv.DictReader(f))), 854)
        with (visual / 'V03_TAXONOMIC_DIAGNOSTIC_EVIDENCE.csv').open(encoding='utf-8') as f:
            trows = list(csv.DictReader(f))
            self.assertEqual(len(trows), 113)
            self.assertTrue(all(r['consumption_status'] == 'WITHHELD_HOLD' for r in trows))
        with (visual / 'V02_V03_EVIDENCE_RESOLUTION_REGISTER.csv').open(encoding='utf-8') as f:
            self.assertEqual(len(list(csv.DictReader(f))), 172)
        for idx in range(1, 76):
            self.assertTrue((FOUND / 'reader/visuals' / f'Z16-P{idx:02d}.svg').is_file())


if __name__ == '__main__':
    unittest.main()
