"""Derive the reader's current evidence-assessment layer (RT01-11).

Baseline claims (foundations/evidence/claims.tsv) and the historical audit ledgers stay as
recorded. This script reads the latest determinations about those claims and writes
foundations/evidence/assessments.tsv, which build_foundations.py shows inside every evidence
panel that cites the claim:

* A04 source decisions (foundations/audit/a04/EVIDENCE_RESOLUTION_VERIFICATION.csv): claim-wide;
* W2C evidence decisions (foundations/audit/w2c/W2C_EVIDENCE_DECISIONS.csv): claim-wide when the
  decision concerns the claim's source or scope, otherwise only on the pages the decision names.

A displayed assessment is a pointer to a recorded determination. It is not a scientific
clearance, closes no specialist hold and approves nothing. Use --write or --check.
"""
import argparse
import csv
from io import StringIO
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
FOUND = ROOT / 'foundations'
OUT = FOUND / 'evidence/assessments.tsv'
A04 = FOUND / 'audit/a04/EVIDENCE_RESOLUTION_VERIFICATION.csv'
W2C = FOUND / 'audit/w2c/W2C_EVIDENCE_DECISIONS.csv'
FIELDS = ['assessment_id', 'claim_id', 'pages', 'status', 'summary', 'limits', 'record', 'checked']
CLAIM = re.compile(r'^[A-Z]{1,2}\d{2,3}$')

A04_STATUS = {
    'OPEN_PARTIAL_OR_UNSUPPORTED': 'Open: support partial or missing (A04)',
    'REOPENED_SCOPE': 'Reopened: earlier closure narrowed (A04)',
    'CONFIRMED_BOUNDED': 'Bounded support confirmed (A04)',
    'CONFIRMED_BOUNDED_ALTERNATE': 'Bounded support confirmed from an alternate source (A04)',
    'NEWLY_CONFIRMED_BOUNDED': 'Bounded support newly confirmed (A04)',
}
# decision -> (reader status, claim-wide?)
W2C_STATUS = {
    'NEW_BOUNDED_PRIMARY_SUPPORT': ('Bounded primary support recorded', True),
    'LOCATOR_NOT_FOUND_ESCALATED': ('Open: cited section not found in the source; escalated', True),
    'MAJOR_SCOPE_MISMATCH_ESCALATED': ('Open: source scope does not match the claim; escalated', True),
    'SCOPE_NARROWED_BY_LATER_SOURCE': ('Narrowed: later guidance limits this claim', True),
    'CLAIM_PARTIALLY_SUPPORTED': ('Partial: part of this claim is not on the cited page', True),
    'CITATION_CORRECTED': ('Citation corrected on this card', False),
    'WEAK_SUPPORT_FLAGGED': ('Open: weak support for a statement on this card', False),
    'PARTIAL_SUPPORT_RECORDED': ('Partial support for a statement on this card', False),
    'UNSUPPORTED_CLAUSE_FLAGGED': ('Open: a statement on this card is not supported by this source', False),
    'UNSUPPORTED_SCOPE_FLAGGED': ('Open: this card applies the source beyond its scope', False),
    'NOT_REVERIFIED': ('Not re-verified for a statement on this card', False),
    'SOURCE_CONFLICT_RESOLVED_BY_LATER_GUIDANCE': ('Source conflict: the later guidance governs on this card', False),
    'REGIONAL_OCCURRENCE_GAP_ESCALATED': None,   # concerns a taxon profile, not a claim
}


def clean(value, fallback='None recorded'):
    value = ' '.join((value or '').split())
    return value if value else fallback


def rows(path):
    with path.open(newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def claim_ids():
    with (FOUND / 'evidence/claims.tsv').open(newline='', encoding='utf-8') as f:
        return {r['id'] for r in csv.DictReader(f, delimiter='\t')}


def build():
    known = claim_ids()
    out = []
    for r in rows(A04):
        claim = r['claim_id'].strip()
        if claim not in known:
            raise SystemExit(f'A04 decision for unknown claim {claim}')
        out.append(dict(assessment_id=f'A04-{claim}', claim_id=claim, pages='*',
                        status=A04_STATUS[r['disposition']], summary=clean(r['qualified_scope_and_limits']),
                        limits=clean(r['specialist_and_publication_limits']),
                        record='foundations/audit/a04/EVIDENCE_RESOLUTION_VERIFICATION.csv', checked=r['checked']))
    for r in rows(W2C):
        mapped = W2C_STATUS[r['decision']]
        if mapped is None:
            continue
        status, claim_wide = mapped
        claims = [c for c in r['claim_id'].split() if CLAIM.match(c)]
        for claim in claims:
            if claim not in known:
                raise SystemExit(f"{r['decision_id']} names unknown claim {claim}")
            out.append(dict(
                assessment_id=r['decision_id'] if len(claims) == 1 else f"{r['decision_id']}-{claim}",
                claim_id=claim, pages='*' if claim_wide else clean(r['pages_affected']),
                status=status, summary=clean(r['bounded_scope']), limits=clean(r['limitations']),
                record=f"foundations/audit/w2c/W2C_EVIDENCE_DECISIONS.csv#{r['decision_id']}",
                checked=r['checked']))
    ids = [r['assessment_id'] for r in out]
    if len(ids) != len(set(ids)):
        raise SystemExit('Duplicate assessment id')
    buf = StringIO()
    writer = csv.DictWriter(buf, fieldnames=FIELDS, delimiter='\t', lineterminator='\n', quoting=csv.QUOTE_NONE,
                            escapechar=None)
    writer.writeheader()
    for row in sorted(out, key=lambda r: (r['claim_id'], r['checked'], r['assessment_id'])):
        if any('\t' in v for v in row.values()):
            raise SystemExit(f"Tab in assessment {row['assessment_id']}")
        writer.writerow(row)
    return buf.getvalue(), out


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    text, records = build()
    if args.write:
        OUT.write_text(text, encoding='utf-8')
    if args.check and (not OUT.is_file() or OUT.read_text(encoding='utf-8') != text):
        raise SystemExit('foundations/evidence/assessments.tsv is stale; run scripts/w2c_assessments.py --write')
    open_items = sum(r['status'].startswith(('Open', 'Reopened', 'Partial', 'Not re-verified', 'Narrowed'))
                     for r in records)
    print(f'{len(records)} assessments over {len({r["claim_id"] for r in records})} claims; '
          f'{open_items} open, partial, narrowed or not re-verified')


if __name__ == '__main__':
    main()
