"""Derive the Wave 2C manifest and production register from the batch ledger.

Inputs: foundations/audit/w2c/W2C_BATCHES.json (decisions per plate) and the A04
queue foundations/audit/a04/WAVE_2C_TECHNICAL_QUEUE.csv (375 items).
Outputs: foundations/visual/w2c_technical/MANIFEST.json (file custody) and
foundations/audit/w2c/W2C_PRODUCTION_REGISTER.csv (status of every queue item).

Use --write to refresh both outputs and --check to confirm they match.
"""
import argparse
import csv
from hashlib import sha256
from io import StringIO
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FOUND = ROOT / 'foundations'
W2C = FOUND / 'visual/w2c_technical'
AUDIT = FOUND / 'audit/w2c'
LEDGER = AUDIT / 'W2C_BATCHES.json'
QUEUE = FOUND / 'audit/a04/WAVE_2C_TECHNICAL_QUEUE.csv'
QUAL = FOUND / 'audit/a04/V01_V02_VISUAL_QUALIFICATION.csv'
DISPOSITIONS = {'PROVISIONAL_EDITORIAL_CANDIDATE', 'HELD_SPECIALIST_INPUT', 'HELD_SOURCE_GAP',
                'HELD_AUTHENTIC_EVIDENCE', 'REJECTED_RETAIN_PREDECESSOR'}
BUILDERS = {'build_w2c_knots.py': ('Z09-P14', 'Z09-P15'), 'build_w2c_navigation.py': ('Z11-R05',),
            'w2c_plates_b02.py': ('Z13-P44', 'Z13-P37', 'Z13-P48', 'Z13-P41', 'Z13-P53'),
            'w2c_plates_b03.py': ('Z13-P20', 'Z13-P56', 'Z15-P43', 'Z13-P60', 'Z13-P57')}
REGISTER_FIELDS = ['page_id', 'asset_id', 'priority', 'origin', 'review_family', 'w2c_status', 'batch',
                   'predecessor_sha256', 'revised_sha256', 'physical_relationship', 'source_basis',
                   'geometry_validation', 'inspection', 'card_changes', 'remaining_dependencies',
                   'specialist', 'release']


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def rows(path):
    with path.open(newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def ledger_plates():
    data = json.loads(LEDGER.read_text(encoding='utf-8'))
    plates = {}
    for batch in data['batches']:
        for plate in batch['plates']:
            if plate['page_id'] in plates:
                raise ValueError(f"Plate listed twice in the ledger: {plate['page_id']}")
            if plate['disposition'] not in DISPOSITIONS:
                raise ValueError(f"Unknown disposition for {plate['page_id']}: {plate['disposition']}")
            plates[plate['page_id']] = dict(plate, batch=batch['batch'])
    return data, plates


def builder_for(page):
    return next((f'scripts/{name}' for name, pages in BUILDERS.items() if page in pages), '')


def manifest(plates):
    candidates = {r['page_id']: r for r in rows(QUAL)}
    records = []
    for page, plate in sorted(plates.items()):
        original, revised = W2C / 'original' / f'{page}.svg', W2C / 'revised' / f'{page}.svg'
        active = FOUND / 'reader/visuals' / f'{page}.svg'
        record = dict(
            page_id=page, batch=plate['batch'], disposition=plate['disposition'],
            predecessor=f'original/{page}.svg', predecessor_sha256=digest(original),
        )
        if plate['disposition'] == 'PROVISIONAL_EDITORIAL_CANDIDATE':
            record.update(revised=f'revised/{page}.svg', revised_sha256=digest(revised),
                          active_reader_sha256=digest(active))
        a04 = candidates.get(page)
        if a04 and a04['disposition'] == 'RECONSTRUCTION_REQUIRED':
            record['supersedes_a04_candidate_sha256'] = a04['candidate_sha256']
        record.update(builder=builder_for(page),
                      classification='Editable conceptual technical illustration; not an engineering, '
                                     'clinical or certified diagram',
                      publication='HOLD')
        records.append(record)
    return json.dumps(records, indent=2) + '\n'


def register(plates, manifest_text):
    custody = {r['page_id']: r for r in json.loads(manifest_text)}
    out = StringIO()
    writer = csv.DictWriter(out, fieldnames=REGISTER_FIELDS, lineterminator='\n')
    writer.writeheader()
    for item in rows(QUEUE):
        page = item['page_id']
        plate, record = plates.get(page), custody.get(page, {})
        writer.writerow(dict(
            page_id=page, asset_id=item['asset_id'], priority=item['priority'], origin=item['origin'],
            review_family=item['review_family'],
            w2c_status=plate['disposition'] if plate else 'QUEUED',
            batch=plate['batch'] if plate else '',
            predecessor_sha256=record.get('predecessor_sha256', ''),
            revised_sha256=record.get('revised_sha256', ''),
            physical_relationship=plate['physical_relationship'] if plate else '',
            source_basis=plate['source_basis'] if plate else item['sources'],
            geometry_validation=plate['geometry_validation'] if plate else '',
            inspection=plate['inspection'] if plate else '',
            card_changes=plate.get('card_changes', '') if plate else '',
            remaining_dependencies=plate['remaining_dependencies'] if plate else item['required_change'],
            specialist=item['specialist'], release='HOLD',
        ))
    return out.getvalue()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    _, plates = ledger_plates()
    queue_pages = {r['page_id'] for r in rows(QUEUE)}
    stray = sorted(set(plates) - queue_pages)
    if stray:
        raise SystemExit(f'Ledger plates outside the Wave 2C queue: {stray}')
    manifest_text = manifest(plates)
    register_text = register(plates, manifest_text)
    targets = {W2C / 'MANIFEST.json': manifest_text, AUDIT / 'W2C_PRODUCTION_REGISTER.csv': register_text}
    if args.write:
        for path, text in targets.items():
            path.write_text(text, encoding='utf-8')
    if args.check:
        for path, text in targets.items():
            if not path.is_file() or path.read_text(encoding='utf-8') != text:
                raise SystemExit(f'{path.relative_to(ROOT)} is stale; run scripts/w2c_register.py --write')
    done = sum(p['disposition'] == 'PROVISIONAL_EDITORIAL_CANDIDATE' for p in plates.values())
    print(f'{len(queue_pages)} queue items: {done} provisional candidates, '
          f'{len(plates) - done} held or rejected, {len(queue_pages) - len(plates)} queued')


if __name__ == '__main__':
    main()
