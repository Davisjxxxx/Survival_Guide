"""Check A02 receipt coverage against the draft reader, evidence and figure hashes."""
import csv
from hashlib import sha256
from html import escape
import json

from build_foundations import ALL_16_ZONES, FOUND, load_evidence, require

AUDIT = FOUND / 'audit/a02'
REVIEW_ZONES = {'Z10', 'Z13', 'Z14', 'Z15'}
REQUIRED_ARTIFACTS = {
    'ASTRA_A02_EXECUTIVE_REPORT.md', 'TECHNICAL_FINDINGS.csv', 'CLAIM_SUPPORT_AUDIT.csv',
    'UNRESOLVED_EVIDENCE_REGISTER.csv', 'CROSS_ZONE_CONTRADICTIONS.csv',
    'VISUAL_QUALITY_CLASSIFICATION.csv', 'DIAGNOSTIC_PHOTOGRAPHY_ACQUISITION_PLAN.csv',
    'SPECIALIST_REVIEW_REGISTER.csv', 'PRODUCTION_CONTROL_IMPROVEMENTS.md',
    'NEON_FINAL_PRODUCTION_HANDOFF.md',
}


def rows(path, delimiter=','):
    with path.open(encoding='utf-8', newline='') as source:
        return list(csv.DictReader(source, delimiter=delimiter))


def keyed(records, key):
    result = {record[key]: record for record in records}
    require(len(result) == len(records), f'Duplicate {key} in audit receipt')
    return result


def assert_scope_and_evidence(reader, cards):
    directory = (reader / 'directory.html').read_text(encoding='utf-8')
    for zone, title, count, _ in ALL_16_ZONES:
        require(f'<strong>{zone}</strong></td><td>{escape(title)}</td><td>{count}</td>' in directory, f'Missing canonical directory label for {zone}')
        zone_cards = [card for card in cards.values() if card['zone'] == zone]
        require(len(zone_cards) <= count, f'Scope exceeds the allocation for {zone}')

    sources, claims = load_evidence()
    evidence = keyed(rows(AUDIT / 'CLAIM_SUPPORT_AUDIT.csv'), 'claim_id')
    unresolved = keyed(rows(AUDIT / 'UNRESOLVED_EVIDENCE_REGISTER.csv'), 'claim_id')
    inherited = {row['claim_id'] for row in rows(FOUND / 'audit/CLAIM_COVERAGE_AUDIT.csv')
                 if row['disposition'] == 'KEEP_OPEN_SOURCE_OR_APPLICABILITY'}
    covered_inherited = {i for i, row in evidence.items() if row['origin'] == 'INHERITED_A01'}
    require(inherited == covered_inherited and inherited <= unresolved.keys(),
            'Inherited unresolved A01 evidence coverage changed')
    require(sum(row['origin'] == 'NEON_80' for row in evidence.values()) == 80,
            'Missing original P12–P15 claim assessment')
    for claim_id, row in evidence.items():
        claim = claims[claim_id]
        require(row['current_support'] == claim['support'] and row['locator'] == claim['locator']
                and row['primary_url'] == sources[claim['source']]['url'],
                f'Claim receipt diverges from current evidence for {claim_id}')
    for row in unresolved.values():
        require(row['status'] == 'OPEN' and row['publication'] == 'HOLD',
                f'Unsupported evidence disposition for {row["claim_id"]}')


def assert_statement_coverage(cards):
    statements = {}
    for card in cards.values():
        fields = {f'action{i}': action for i, action in enumerate(card['action'], 1)}
        fields.update({field: card[field] for field in ('verify', 'stop', 'failure') if field in card})
        statements.update({(card['id'], field): item for field, item in fields.items()})
    report = rows(AUDIT / 'ASSERTION_SCREEN.csv')
    screened = {(row['page_id'], row['field']) for row in report}
    expected = {key for key in statements if key[0][:3] in REVIEW_ZONES}
    require(expected <= screened and len(report) == len(screened), 'Incomplete or duplicate assertion review')
    for row in report:
        key = row['page_id'], row['field']
        item = statements[key]
        require(row['a02_exact'] == item['text'] and row['links'].split() == item['claims'],
                f'Assertion text or source links differ for {key}')
    return len(expected)


def assert_visual_and_photo_coverage(reader, cards):
    figures = keyed(rows(AUDIT / 'VISUAL_QUALITY_CLASSIFICATION.csv'), 'page_id')
    planned = keyed(rows(FOUND / 'evidence/photo-requirements.tsv', '\t'), 'page')
    photo_plan = keyed(rows(AUDIT / 'DIAGNOSTIC_PHOTOGRAPHY_ACQUISITION_PLAN.csv'), 'page')
    require(figures.keys() == cards.keys(), 'Incomplete A02 figure coverage')
    require(photo_plan.keys() == planned.keys(), 'Diagnostic photograph scope is incomplete')
    for page, row in figures.items():
        digest = sha256((reader / f'visuals/{page}.svg').read_bytes()).hexdigest()
        require(row['sha256'] == digest and (row['requires_diagnostic_photo'] == '1') == (page in planned),
                f'Asset or photo requirement mismatch for {page}')
    require(all(row['acquisition_status'].startswith('OPEN') for row in photo_plan.values()),
            'A02 contains an unverified diagnostic disposition')


def main():
    require(REQUIRED_ARTIFACTS <= {file.name for file in AUDIT.iterdir()}, 'Missing A02 deliverables')
    reader = FOUND / 'reader'
    cards = keyed(json.loads((reader / 'page-manifest.json').read_text()), 'id')
    require(len(cards) == 668 and all(card['publication'] == 'HOLD' for card in cards.values()),
            'A02 draft card coverage or HOLD status changed')
    assert_scope_and_evidence(reader, cards)
    checked = assert_statement_coverage(cards)
    assert_visual_and_photo_coverage(reader, cards)
    holds = keyed(rows(AUDIT / 'SPECIALIST_REVIEW_REGISTER.csv'), 'id')
    require(len(holds) == 21 and all(r['status'] == 'PENDING' and r['publication'] == 'HOLD'
                                    for r in holds.values()), 'A02 specialist HOLD status changed')
    print(f'PASS: A02 scope, {checked} priority statements, figure hashes, open photo needs and specialist holds')


if __name__ == '__main__':
    main()
