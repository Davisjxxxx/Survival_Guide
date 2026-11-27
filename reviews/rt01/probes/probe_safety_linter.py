"""Read-only adversarial probes of the manuscript linter.

NEGATIVE TEST FIXTURES ONLY. The intentionally unsafe strings below are not
survival guidance. Mutations exist only in memory; no manuscript is changed.
This probes a specific linter, not the full build or all release controls.
"""
import argparse
import copy
import json
from pathlib import Path
import subprocess
import sys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    sys.path.insert(0, str(args.repo / 'scripts'))
    from build_foundations import load_evidence, load_cards, lint_cards
    _, claims = load_evidence()
    cards = load_cards(sorted((args.repo / 'foundations/manuscripts').glob('*.cards')), claims)
    cases = [
        ('RT-MUT-01', 'Z04-P01', 'action', 'Clear water is safe.',
         'Exact water-clarity rule, operational text: positive detection control'),
        ('RT-MUT-02', 'Z04-P01', 'visual', 'Clear water is safe.',
         'Same unsafe assertion in the reader-visible figure caption'),
        ('RT-MUT-03', 'Z04-P01', 'diagram', 'Clear water is safe. | Collect | Drink',
         'Same unsafe assertion in visible stage labels and image alt text'),
        ('RT-MUT-04', 'Z13-P20', 'action', 'Run the generator inside a garage.',
         'Exact indoor-combustion rule: positive detection control'),
        ('RT-MUT-05', 'Z13-P20', 'action', 'Do not spill fuel, then run the generator inside a garage.',
         'An unrelated prohibition in the same clause masks the unsafe authorization'),
        ('RT-MUT-06', 'Z13-P20', 'visual', 'Run the generator inside a garage.',
         'Same unsafe combustion assertion in a reader-visible caption'),
        ('RT-MUT-07', 'Z12-P56', 'action', 'Swim directly against a rip current.',
         'A prohibition elsewhere in the existing card masks the unsafe action'),
        ('RT-MUT-08', 'Z04-P01', 'action', 'Clear water is not safe merely because it looks clear.',
         'Safe negated statement: false-positive control'),
    ]
    results = []
    for test_id, page, field, text, description in cases:
        mutated = copy.deepcopy(cards)
        if field == 'action':
            mutated[page]['action'][0]['text'] = text
        else:
            mutated[page][field] = text
        try:
            lint_cards(mutated)
        except ValueError as e:
            status, error = 'REJECTED', str(e)
        else:
            status, error = 'ACCEPTED', None
        results.append(dict(test_id=test_id, page_id=page, field=field,
                            fixture=text, description=description,
                            observed=status, error=error))
    payload = {
        'checkpoint': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=args.repo, text=True).strip(),
        'kind': 'synthetic in-memory negative fixtures, not production content',
        'scope': 'build_foundations.lint_cards only; no manuscript, SVG, package or release gate was mutated',
        'canonical_card_count': len(cards), 'results': results,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2) + '\n')
    for r in results:
        print(r['test_id'], r['observed'], r['description'])


if __name__ == '__main__':
    main()
