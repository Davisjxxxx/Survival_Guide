"""Measure W2C plate labels in Chromium and fail on clipping, collisions or panel crossings.

Each SVG is laid out at 720 px, the width the production vector audit uses (font metrics in
user units grow slightly at smaller sizes). Every <text> bounding box must lie inside the
viewBox, must not overlap another label by more than 1.5 units in both directions, and a
label whose anchor sits inside a panel (rounded rect with a W2C panel fill) must stay inside
that panel. Labels outside panels must not intrude into the bottom stop band unless they are
the band text itself. This is a layout aid: it does not judge content, contrast or meaning.

Usage: python w2c_label_audit.py PLATE.svg [...] [--json OUT]
"""
import argparse
import json
from pathlib import Path
from shutil import which
import sys

from playwright.sync_api import sync_playwright

PANEL_FILLS = {'#e7f0ea', '#fbeee7', '#f7f7ef'}
BAND = (24, 345, 852, 32)
TOL = 1.5          # panel-edge and canvas tolerance
OVERLAP = 2.0      # label-on-label threshold, as in scripts/audit_foundation_vectors.py

MEASURE = """(markup) => {
  document.body.innerHTML = markup;
  const svg = document.querySelector('svg');
  const vb = svg.viewBox.baseVal;
  const texts = [...svg.querySelectorAll('text')].map(el => {
    const b = el.getBBox();
    return {t: el.textContent, x: b.x, y: b.y, w: b.width, h: b.height,
            ax: parseFloat(el.getAttribute('x')), ay: parseFloat(el.getAttribute('y')),
            transformed: !!el.getAttribute('transform') || !!el.closest('[transform]')};
  });
  const panels = [...svg.querySelectorAll('rect')].filter(r => r.getAttribute('rx') === '10')
    .map(r => ({fill: (r.getAttribute('fill') || '').toLowerCase(), x: +r.getAttribute('x'), y: +r.getAttribute('y'),
                w: +r.getAttribute('width'), h: +r.getAttribute('height')}));
  return {vb: {x: vb.x, y: vb.y, w: vb.width, h: vb.height}, texts, panels};
}"""


def inside(b, r, tol=TOL):
    return b['x'] >= r['x'] - tol and b['y'] >= r['y'] - tol and \
        b['x'] + b['w'] <= r['x'] + r['w'] + tol and b['y'] + b['h'] <= r['y'] + r['h'] + tol


def overlap(a, b):
    dx = min(a['x'] + a['w'], b['x'] + b['w']) - max(a['x'], b['x'])
    dy = min(a['y'] + a['h'], b['y'] + b['h']) - max(a['y'], b['y'])
    return dx > OVERLAP and dy > OVERLAP


def audit(page, path):
    m = page.evaluate(MEASURE, path.read_text(encoding='utf-8'))
    vb = m['vb']
    panels = [p for p in m['panels'] if p['fill'] in PANEL_FILLS]
    problems = []
    texts = [t for t in m['texts'] if t['t'].strip()]
    for t in texts:
        if not inside(t, vb, 0.1):
            problems.append(f"outside canvas: {t['t']!r}")
        if t['transformed']:
            continue
        home = [p for p in panels if p['x'] <= t['ax'] <= p['x'] + p['w'] and p['y'] <= t['ay'] <= p['y'] + p['h']]
        if home:
            panel = min(home, key=lambda p: p['w'] * p['h'])
            if not inside(t, panel):
                problems.append(f"crosses panel edge: {t['t']!r}")
        elif not (BAND[1] <= t['ay'] <= BAND[1] + BAND[3]) and t['y'] + t['h'] > BAND[1] + TOL and t['ay'] > 40:
            problems.append(f"intrudes into stop band: {t['t']!r}")
    for i, a in enumerate(texts):
        for b in texts[i + 1:]:
            if overlap(a, b):
                problems.append(f"labels overlap: {a['t']!r} / {b['t']!r}")
    return dict(labels=len(texts), panels=len(panels), problems=problems, clean=not problems)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('svgs', nargs='+', type=Path)
    parser.add_argument('--json', type=Path)
    args = parser.parse_args()
    results = {}
    with sync_playwright() as pw:
        browser = pw.chromium.launch(executable_path=which('google-chrome') or which('chromium'))
        page = browser.new_page(viewport={'width': 1000, 'height': 600})
        page.set_content('<!doctype html><meta charset="utf-8"><style>svg{display:block;width:720px}</style><body></body>')
        for path in args.svgs:
            results[path.stem] = audit(page, path)
        browser.close()
    if args.json:
        args.json.write_text(json.dumps(results, indent=1, sort_keys=True) + '\n', encoding='utf-8')
    for name, r in results.items():
        print(name, 'clean' if r['clean'] else 'PROBLEMS', f"({r['labels']} labels, {r['panels']} panels)")
        for problem in r['problems']:
            print('   ', problem)
    sys.exit(0 if all(r['clean'] for r in results.values()) else 1)


if __name__ == '__main__':
    main()
