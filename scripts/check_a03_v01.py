"""Verify A03/V01 receipt coverage, scope custody and media hashes."""
import csv
from hashlib import sha256
from html.parser import HTMLParser
import json

from build_foundations import ALL_16_ZONES, FOUND, require, validate_atlas_targets
from check_foundations import PILOT_DIR

AUDIT = FOUND / 'audit/a03'
VISUAL = FOUND / 'visual'


def table(path, key, delimiter=','):
    with path.open(encoding='utf-8', newline='') as source:
        rows = list(csv.DictReader(source, delimiter=delimiter))
    keyed = {row[key]: row for row in rows}
    require(len(keyed) == len(rows), f'Duplicate {key} in {path.name}')
    return keyed


class AtlasLinks(HTMLParser):
    """Read the actual rendered upstream routes."""
    def __init__(self):
        super().__init__()
        self.destinations = set()

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == 'a' and 'atlas-link' in attributes.get('class', '').split():
            self.destinations.add(attributes['href'])


def audit_atlas(cards, reader):
    atlas = table(AUDIT / 'ATLAS_FIDELITY_AUDIT.csv', 'page_id')
    require(atlas.keys() == {cid for cid in cards if cid.startswith('Z16-')}, 'Missing atlas coverage')
    validate_atlas_targets(cards)
    for id, record in atlas.items():
        parsed = AtlasLinks()
        parsed.feed((reader / f'{id}.html').read_text(encoding='utf-8'))
        targets = record['verified_current_targets'].split()
        require(parsed.destinations == {f'{cid}.html' for cid in targets}, f'Atlas route drift on {id}')
        for target in targets:
            card = cards[target]
            require(card['publication'] == 'HOLD'
                    and f'{target}: {card["applies"]}' in record['source_applicability']
                    and f'{target}: {card["stop"]["text"]}' in record['source_stop_conditions']
                    and f'{target}: {card["equipment"]}' in record['source_equipment'],
                    f'Atlas receipt differs from {target}')


def audit_taxonomy_and_evidence(cards):
    taxa = table(FOUND / 'evidence/z05-taxonomic-register.tsv', 'page_id', '\t')
    reviewed = table(AUDIT / 'TAXONOMIC_VERIFICATION_REGISTER.csv', 'page_id')
    require(len(taxa) == 113 and taxa.keys() == reviewed.keys(), 'Taxonomic review coverage changed')
    for id, record in reviewed.items():
        require(record['consumption_status'] == taxa[id]['consumption_status'] == 'WITHHELD_HOLD'
                and 'WITHHELD_HOLD' in cards[id]['stop']['text'], f'Taxon hold changed for {id}')
    evidence = table(AUDIT / 'CLAIM_SUPPORT_AUDIT.csv', 'claim_id')
    inherited = table(FOUND / 'audit/a02/UNRESOLVED_EVIDENCE_REGISTER.csv', 'claim_id')
    open_items = table(AUDIT / 'UNRESOLVED_EVIDENCE_REGISTER.csv', 'claim_id')
    require(len(inherited) == 116 and inherited.keys() <= open_items.keys(),
            'Inherited open evidence was lost')
    require(sum(r['origin'] == 'P16–P20_86' for r in evidence.values()) == 86, 'Missing new-claim audit')


def audit_visuals(cards, reader):
    dispositions = table(VISUAL / 'VISUAL_ASSET_DISPOSITION_REGISTER.csv', 'page_id')
    backlog = table(VISUAL / 'ILLUSTRATION_REPLACEMENT_BACKLOG.csv', 'page_id')
    baseline = table(FOUND / 'audit/p16_p20/VISUAL_REDESIGN_BACKLOG.csv', 'page_id')
    photos = table(VISUAL / 'DIAGNOSTIC_PHOTOGRAPHY_ACQUISITION_REGISTER.csv', 'page_id')
    previous_photos = table(FOUND / 'evidence/photo-requirements.tsv', 'page', '\t')
    require(dispositions.keys() == cards.keys(), 'Incomplete visual disposition coverage')
    require({id for id, r in baseline.items() if r['current_class'] == '3_GENERIC_REDESIGN_CANDIDATE'}
            <= backlog.keys(), 'A predecessor redesign candidate was dropped')
    require(previous_photos.keys() <= photos.keys() and all(
        row['status'].startswith('OPEN') for row in photos.values()), 'Photo requirements lost or cleared')
    for id, record in dispositions.items():
        proof = reader / 'visuals' / f'{id}.svg'
        require(sha256(proof.read_bytes()).hexdigest() == record['sha256'],
                f'Visual receipt differs from {proof.name}')
    specimens = PILOT_DIR / 'specimens'
    for record in json.loads((specimens / 'MANIFEST.json').read_text()):
        original = (specimens / record['file']).read_bytes()
        require(original.startswith(b'\xff\xd8') and sha256(original).hexdigest() == record['sha256']
                and record['rights'] == 'CC0' and record['diagnostic_qualification'] == 'WITHHELD',
                f'Specimen provenance or hold changed: {record["file"]}')


def main():
    reader = FOUND / 'reader'
    cards = {c['id']: c for c in json.loads((reader / 'page-manifest.json').read_text())}
    require(len(cards) == 1016 and all(r['publication'] == 'HOLD' for r in cards.values()),
            'Canonical edition size or publication hold changed')
    for zone, _, planned, _ in ALL_16_ZONES:
        require(sum(c['zone'] == zone for c in cards.values()) == planned, f'Allocation drift in {zone}')
    audit_atlas(cards, reader)
    audit_taxonomy_and_evidence(cards)
    audit_visuals(cards, reader)
    holds = table(AUDIT / 'SPECIALIST_REVIEW_REGISTER.csv', 'id')
    require(len(holds) == 25 and all(r['status'] == 'PENDING' and r['publication'] == 'HOLD'
                                    for r in holds.values()), 'Specialist hold drift')
    print('PASS: A03/V01 canonical scope, atlas routes and conditions, evidence, images and holds')


if __name__ == '__main__':
    main()
