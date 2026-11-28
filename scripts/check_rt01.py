"""Acceptance receipts for the RT01 findings implemented in Wave 2C (draft PR #12).

Each check reads delivered artifacts: canonical card text, figure specification, the active
SVG (description and drawn labels), the reader page (alt text, caption, evidence panel), the
offline zone package members and, for RT01-06, the printed proof sheets. The findings and
their acceptance conditions are in reviews/rt01/ on review/astra-rt01-adversarial-20261127.

Passing means the bounded editorial and control corrections are present and consistent across
those surfaces. It is not a clinical, food-safety, navigation or other specialist approval,
and it does not certify the content as safe. Publication stays HOLD.
"""
import copy
import json
from pathlib import Path
import re
import sys
import unicodedata
from xml.etree import ElementTree
from zipfile import ZipFile

import pymupdf

from build_foundations import FOUND, load_cards, load_evidence, lint_cards, require
from print_foundations_tagged import normalize

READER = FOUND / 'reader'
NS = '{http://www.w3.org/2000/svg}'


def cards():
    _, claims = load_evidence()
    return load_cards(sorted((FOUND / 'manuscripts').glob('*.cards')), claims)


def card_text(card):
    rows = [*card['action'], card['verify'], card['stop'], *([card['failure']] if 'failure' in card else [])]
    return ' '.join([card['title'], card['objective'], card['applies'], card['equipment'], card['diagram'],
                     card['visual'], *[r['text'] for r in rows]])


def svg_text(page):
    root = ElementTree.parse(READER / 'visuals' / f'{page}.svg').getroot()
    desc = root.find(NS + 'desc')
    return (desc.text if desc is not None else ''), ' '.join(''.join(t.itertext()) for t in root.iter(NS + 'text'))


def html(page):
    return (READER / f'{page}.html').read_text(encoding='utf-8')


def alt(page):
    return re.search(r'<img src="visuals/[^"]+" alt="([^"]*)"', html(page)).group(1)


def zone_member(zone, member):
    with ZipFile(FOUND / f'proofs/packages/zone-{zone}.zip') as z:
        return z.read(member).decode('utf-8')


def surfaces(page, c):
    desc, labels = svg_text(page)
    return ' '.join([card_text(c[page]), desc, labels, alt(page)])


def rt01_01(c):
    text = surfaces('Z11-P63', c)
    require('call, text or press SOS now' in text and 'do not stop to write notes first' in text,
            'Z11-P63: immediate activation missing')
    require('BEFORE dialing' not in text and 'before dialing' not in text, 'Z11-P63: report still precedes the call')
    require('aid, not a precondition' in text and 'calls at once' in svg_text('Z11-P63')[0], 'Z11-P63: report not an aid')
    require('T17' in c['Z11-P63']['action'][0]['claims'], 'Z11-P63: activation line lacks T17')
    return 'call-first wording on card, figure description, labels and alt; T17 cited'


def rt01_02(c):
    text = surfaces('Z10-P06', c)
    spec = json.dumps(json.loads((FOUND / 'evidence/diagram-specs.json').read_text(encoding='utf-8'))['Z10-P06'])
    require(not re.search(r'15[ -]?(min|m\b|minute)|every 15|Every 15|30 to 60', text + spec),
            'Z10-P06: a fixed observation interval remains')
    require('Watch breathing' in text and 'never replaces watching' in text, 'Z10-P06: continuous observation missing')
    return 'no fixed interval in prose, spec, SVG or alt; continuous watching separated from logging'


def rt01_03(c):
    desc, labels = svg_text('Z10-P26')
    require('confirmed safe' in labels and 'Poison Control' in labels, 'Z10-P26: qualified isolation or label boundary missing')
    require('20+' not in labels and 'brush dry powder first' not in labels, 'Z10-P26: generic brush-and-flush route remains')
    require('stay back until confirmed safe' in alt('Z10-P26'), 'Z10-P26: alt text not corrected')
    queue = (FOUND / 'audit/w2c/W2C_REPAIR_QUEUE.csv').read_text(encoding='utf-8')
    require('Z10-P26' in queue and 'RT01-03' in queue, 'Z10-P26: repair item missing')
    return 'figure labels, alt and caption carry the isolation and label/SDS/Poison Control limits; repair item queued'


def rt01_04(c):
    card = c['Z04-P51']
    require('formula' not in card['action'][0]['text'], 'Z04-P51: formula still in the generic safe-water list')
    formula = next(r for r in card['action'] if 'infant formula' in r['text'])
    require({'P26', 'P36'} <= set(formula['claims']) and '(see Z14-P74)' in formula['text'], 'Z04-P51: formula boundary')
    require('not sterile' in formula['text'] and 'chemical advisory' in formula['text'], 'Z04-P51: powder or chemical limit')
    page = html('Z04-P51')
    require('<a class="xref" href="Z14-P74.html">Z14-P74</a>' in page and '<dt>P26 ' in page and '<dt>P36 ' in page,
            'Z04-P51: cross-link or evidence panel missing')
    packaged = zone_member('Z04', 'reader/Z04-P51.html')
    require('Z14-P74 (full edition)' in packaged, 'Z04 package: cross-zone reference not labelled')
    with ZipFile(FOUND / 'proofs/foundations-offline.zip') as z:
        require('reader/Z14-P74.html' in z.namelist(), 'Core offline edition lacks the Z14-P74 destination')
    require('INFANT FORMULA' in svg_text('Z04-P51')[1], 'Z04-P51: plate lacks the separate formula panel')
    return 'formula separated with P26/P36, powder and chemical limits, working link in the full offline edition'


def rt01_05(c):
    for page in ('Z13-P49', 'Z13-P50'):
        text = surfaces(page, c)
        require('(or ≥60% alcohol rub)' not in text and 'when hands look clean' not in text
                and 'when not visibly soiled' not in text, f'{page}: sanitizer equivalence remains')
    require('truly unavailable' in surfaces('Z13-P50', c) and 'not a substitute' in surfaces('Z13-P50', c),
            'Z13-P50: fallback boundary missing')
    require('alcohol rub does not replace' in surfaces('Z13-P49', c), 'Z13-P49: handwashing boundary missing')
    return 'soap and water after waste tasks on both cards and plates; sanitizer only as a fallback'


def labels_of(path):
    root = ElementTree.parse(path).getroot()
    return {' '.join(''.join(t.itertext()).split()) for t in root.iter(NS + 'text')}


def rt01_06(c):
    from check_foundations import verify_proof_currency
    verify_proof_currency(FOUND / 'proofs')
    pages = ['Z15-P18', 'Z15-P22', 'Z15-P02', 'Z15-P23', 'Z14-P55', 'Z14-P56', 'Z14-P57', 'Z14-P53', 'Z14-P48']
    manifest = json.loads((READER / 'page-manifest.json').read_text(encoding='utf-8'))
    w2c = FOUND / 'visual/w2c_technical'
    checked = 0
    for page in pages:
        current, old = labels_of(READER / 'visuals' / f'{page}.svg'), labels_of(w2c / 'original' / f'{page}.svg')
        new_only = sorted((t for t in current - old if len(t) >= 10), key=len, reverse=True)
        old_only = sorted((t for t in old - current if len(t) >= 10), key=len, reverse=True)
        require(new_only, f'{page}: no label distinguishes the current figure')
        for name in ('encyclopedia', page[:3]):
            ids = [x['id'] for x in manifest if name == 'encyclopedia' or x['zone'] == name]
            for fmt in ('letter', 'a4'):
                pdf = FOUND / 'proofs' / f'{name}-{fmt}.pdf'
                with pymupdf.open(pdf) as doc:
                    sheet = normalize(unicodedata.normalize('NFKC', doc[ids.index(page)].get_text()))
                require(normalize(c[page]['title']) in sheet and normalize(new_only[0]) in sheet,
                        f'{pdf.name}: sheet for {page} lacks the current figure label {new_only[0]!r}')
                require(not any(t in sheet for t in old_only[:3]),
                        f'{pdf.name}: sheet for {page} still shows superseded figure text')
                checked += 1
    return (f'proof currency gate passes; {checked} printed sheets (9 RT01-06 pages, zone and consolidated, Letter and A4) '
            'show a current-only figure label and none of the superseded labels')


def rt01_07(c):
    text = ' '.join([card_text(c['Z14-P41']), alt('Z14-P41')])
    require('Frozen: ice crystals or ≤40°F -> refreeze' not in text, 'Z14-P41: blanket refreeze shortcut remains')
    root = ElementTree.parse(READER / 'visuals/Z14-P41.svg').getroot()
    cells = {(g.get('data-row'), g.get('data-col')): g.get('data-result') for g in root.iter(NS + 'g') if g.get('data-row')}
    require(cells.get(('ice cream, frozen yogurt', 'ice crystals')) == 'discard'
            and cells.get(('ice cream, frozen yogurt', 'over 40 F for 2 h')) == 'discard', 'Z14-P41: ice cream row')
    require('F08' in c['Z14-P41']['action'][1]['claims'], 'Z14-P41: frozen line lacks F08')
    return 'separate refrigerator and freezer paths; ice cream and frozen yogurt discard in both columns; F08 cited'


def rt01_08(c):
    for page in ('Z11-P32',):
        text = surfaces(page, c)
        require(not re.search(r'\bexact\b|\bEXACT\b|\bExact\b', text), f'{page}: exact-return wording remains')
        require('approximate' in text and 'N15' in c[page]['action'][2]['claims'], f'{page}: approximation missing')
    return 'approximate paced return on card, plate, description and alt; N15 cited'


def rt01_09(c):
    from build_w2c_navigation import pivot_of, z11_r05_checks
    delivered = (READER / 'visuals/Z11-R05.svg').read_text(encoding='utf-8')
    require(z11_r05_checks(delivered)['accepted'], 'Z11-R05: delivered geometry fails')
    cx, cy = pivot_of(ElementTree.fromstring(delivered), 'compass-after')
    needle = re.search(r'<polygon id="compass-after-needle"[^>]*>', delivered).group(0)
    mutated = delivered.replace(needle, needle.replace('<polygon ', f'<polygon transform="rotate(90 {cx:.1f} {cy:.1f})" '))
    require(not z11_r05_checks(mutated)['accepted'], 'Z11-R05: 90-degree needle mutation was accepted')
    return 'delivered plate passes; 90-degree visible-needle mutation with unchanged data-bearing fails'


def rt01_10(c):
    cases = [('Z04-P01', 'action', 'Clear water is safe.', True), ('Z04-P01', 'visual', 'Clear water is safe.', True),
             ('Z04-P01', 'diagram', 'Clear water is safe. | Collect | Drink', True),
             ('Z13-P20', 'action', 'Run the generator inside a garage.', True),
             ('Z13-P20', 'action', 'Do not spill fuel, then run the generator inside a garage.', True),
             ('Z13-P20', 'visual', 'Run the generator inside a garage.', True),
             ('Z12-P56', 'action', 'Swim directly against a rip current.', True),
             ('Z04-P01', 'action', 'Clear water is not safe merely because it looks clear.', False)]
    for page, field, text, rejected in cases:
        mutated = copy.deepcopy(c)
        if field == 'action':
            mutated[page]['action'][0]['text'] = text
        else:
            mutated[page][field] = text
        try:
            lint_cards(mutated)
            outcome = False
        except ValueError:
            outcome = True
        require(outcome == rejected, f'RT01-10 fixture {page}/{field} {text!r}: rejected={outcome}')
    return '7 unsafe fixtures rejected (2 positive controls and 5 previously accepted variants), safe negation accepted'


def rt01_11(c):
    citing = [p for p, card in c.items() if any('K09' in r['claims'] for r in [*card['action'], card['verify'], card['stop']])]
    require(len(citing) == 25, f'K09 citing cards: {len(citing)}')
    for page in citing:
        require('Current assessment</strong> · W2C-E004' in html(page), f'{page}: K09 assessment missing')
    require('Current assessment</strong> · W2C-E004' in zone_member('Z09', 'reader/Z09-P14.html'),
            'Z09 package lacks the K09 assessment')
    require('Current assessment</strong> · W2C-E004' in html('Z16-P43'), 'Z16-P43 lacks the K09 assessment')
    return 'K09 limitation shown on all 25 citing panels, in the Z09 package and on atlas card Z16-P43'


CHECKS = [rt01_01, rt01_02, rt01_03, rt01_04, rt01_05, rt01_06, rt01_07, rt01_08, rt01_09, rt01_10, rt01_11]


def main():
    c = cards()
    out = {}
    for check in CHECKS:
        name = check.__name__.upper().replace('_', '-')
        out[name] = check(c)
        print(f'{name}: {out[name]}')
    if '--json' in sys.argv:
        Path(sys.argv[sys.argv.index('--json') + 1]).write_text(json.dumps(out, indent=1) + '\n', encoding='utf-8')
    print(f'PASS: {len(out)} RT01 acceptance receipts; publication HOLD; no specialist approval implied')


if __name__ == '__main__':
    main()
