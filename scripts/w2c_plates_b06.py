"""Wave 2C batch W2C-B06: food temperature and the cold chain.

Plates show food temperature against refrigeration and cooking thresholds and
where thermometers measure it: cooking endpoints on a scaled thermometer, appliance
thermometers, outage hold times on a shared time axis, the keep/refreeze/discard
cues, and safe thawing. Numbers come from the FoodSafety.gov temperature and outage
charts, FDA and CDC outage pages, USDA FSIS thawing guidance and the New York State
Department of Health dry-ice page, read on 2026-11-28 (claims F08-F12, P37). Z14-P41
draws the refrigerator and freezer paths separately and leaves refreezing to the food
row (RT01-07). Run with --out DIR, --write or --check (includes geometry checks).
"""
import argparse
from pathlib import Path

from w2c_svg import FLOW, INK, REVERSE, WATER, WATER_EDGE, Plate, check, cross

OUT = Path(__file__).resolve().parents[1] / 'foundations/visual/w2c_technical/revised'
SCALE = dict(x=430, top=78, bottom=318, tmin=130.0, tmax=175.0)   # thermometer scale in degrees F
HOLD = dict(x0=150, px_per_h=11.0)                                 # outage time axis


def ty(temp):
    s = SCALE
    return s['bottom'] - (temp - s['tmin']) * (s['bottom'] - s['top']) / (s['tmax'] - s['tmin'])


def z14_p37():
    p = Plate('Z14-P37', 'Safe minimum internal temperatures checked with a food thermometer',
              'Left: a roast cut in section with a thermometer probe in its thickest part. Centre: a scaled '
              'thermometer column from 130 to 175 degrees F with marks at 145 F for whole cuts of beef, pork, veal and '
              'lamb (with a 3-minute rest) and fish, 160 F for ground meats and egg dishes, and 165 F for poultry, '
              'casseroles and leftovers. Meat colour and juices are not a test. Conceptual, not to scale apart from the '
              'temperature column.', scale_note='NOT TO SCALE EXCEPT TEMPERATURE COLUMN')
    p.add('<ellipse cx="190" cy="214" rx="140" ry="76" fill="#b5654a" stroke="#183a30" stroke-width="2.6"/>'
          '<ellipse cx="190" cy="214" rx="96" ry="48" fill="#cf8c73"/><ellipse cx="190" cy="214" rx="46" ry="22" fill="#e1a98f"/>')
    p.add('<path d="M190 214L300 104" stroke="#9aa1a5" stroke-width="5"/><circle cx="300" cy="104" r="20" fill="#ffffff" stroke="#183a30" stroke-width="2.4"/>'
          '<path d="M300 104l9-7" stroke="#183a30" stroke-width="2.4"/>')
    p.add('<circle cx="190" cy="214" r="6" fill="#183a30"/>')
    p.lines(46, 316, ['probe tip in the thickest part'], 'tiny')
    p.lines(46, 72, ['meat colour and juices are not a test'], 'tiny warn')
    s = SCALE
    p.add(f'<rect x="{s["x"] - 10}" y="{s["top"] - 10}" width="20" height="{s["bottom"] - s["top"] + 20}" rx="10" fill="#ffffff" stroke="{INK}" stroke-width="2.4"/>'
          f'<rect x="{s["x"] - 4}" y="{ty(165)}" width="8" height="{s["bottom"] - ty(165) + 6}" fill="#c0392b"/>')
    p.add('<g id="temp-scale">')
    for t in range(130, 176, 5):
        p.add(f'<line data-temp="{t}" x1="{s["x"] + 10}" y1="{ty(t):.2f}" x2="{s["x"] + (22 if t % 10 == 0 else 16)}" y2="{ty(t):.2f}" stroke="{INK}" stroke-width="1.6"/>')
        if t % 10 == 0:
            p.add(f'<text x="{s["x"] - 18}" y="{ty(t) + 5:.1f}" class="tiny" text-anchor="end">{t}</text>')
    p.add('</g>')
    p.lines(s['x'] - 30, s['top'] - 18 + 4, ['°F'], 'tiny')
    for t, rows in ((165, ['165 F: poultry, casseroles, leftovers']), (160, ['160 F: ground meats, egg dishes']),
                    (145, ['145 F + 3 min rest: whole cuts of', 'beef, pork, veal, lamb; fish 145 F'])):
        y = ty(t)
        p.add(f'<path data-mark="{t}" d="M{s["x"] + 24} {y:.2f}H{s["x"] + 60}" stroke="{FLOW}" stroke-width="3"/>')
        p.lines(s['x'] + 68, y + 5, rows, 'tiny')
    p.band('Not at temperature: return it to the heat; wash plates that held raw meat before reuse.')
    return p.svg()


def appliance_thermometer(x, y, reading, label):
    return (f'<rect x="{x}" y="{y}" width="40" height="22" rx="4" fill="#ffffff" stroke="{INK}" stroke-width="1.8"/>'
            f'<text x="{x + 20}" y="{y + 16}" class="tiny" text-anchor="middle" font-size="12">{reading}</text>'
            f'<text x="{x + 48}" y="{y + 16}" class="tiny">{label}</text>')


def z14_p39():
    p = Plate('Z14-P39', 'Appliance thermometers in the refrigerator and freezer',
              'Cutaway of a refrigerator with the freezer above. An appliance thermometer hangs in each compartment: '
              'the freezer reads 0 degrees F or below and the refrigerator 40 degrees F or below. The control knob is '
              'a setting, not a measurement. Frozen water containers help keep food cold. Above 40 F the food enters '
              'the danger zone; check the reading when power returns and sort food against the official charts. '
              'Conceptual, not to scale.')
    p.add('<rect x="80" y="70" width="230" height="262" rx="14" fill="#f6f7f2" stroke="#183a30" stroke-width="2.8"/>'
          '<line x1="80" y1="150" x2="310" y2="150" stroke="#183a30" stroke-width="2.4"/>')
    for k in range(3):
        p.add(f'<path d="M{100 + k * 40} 136v-36q0-8 8-8h16q8 0 8 8v36z" fill="#dcecf3" stroke="#183a30" stroke-width="1.6"/>')
    p.add(appliance_thermometer(226, 104, '0 °F', ''))
    p.add('<path d="M96 206h198M96 262h198" stroke="#9aa59c" stroke-width="2"/>')
    p.add(appliance_thermometer(180, 220, '38 °F', ''))
    p.add('<circle cx="284" cy="170" r="11" fill="#e6e8e9" stroke="#183a30" stroke-width="1.8"/><path d="M284 170v-8" stroke="#183a30" stroke-width="2.2"/>')
    p.lines(330, 96, ['freezer: 0 °F or below'], 'small')
    p.lead((326, 92), (268, 112))
    p.lines(330, 128, ['frozen water containers', 'help keep food cold'], 'tiny')
    p.lead((326, 124), (290, 140), (208, 134))
    p.lines(330, 230, ['refrigerator: 40 °F or below'], 'small')
    p.lead((326, 226), (222, 230))
    p.lines(330, 176, ['control knob: a setting,', 'not a measured temperature'], 'tiny')
    p.lead((326, 172), (296, 170))
    p.panel(620, 46, 256, 290, 'bad', 'ABOVE 40 °F')
    p.add(f'<rect x="650" y="96" width="22" height="200" rx="11" fill="#ffffff" stroke="{INK}" stroke-width="2"/>'
          f'<rect x="654" y="96" width="14" height="110" fill="{REVERSE}" fill-opacity=".45"/>'
          f'<path d="M640 206h42" stroke="{INK}" stroke-width="2.4"/>')
    p.lines(690, 212, ['40 °F'], 'small')
    p.lines(690, 130, ['check the', 'reading when', 'power returns'], 'tiny')
    p.band('Readings staying above 40 °F (refrigerator) or 0 °F (freezer): evaluate the food and repair the unit.')
    return p.svg()


def z14_p40():
    x0, k = HOLD['x0'], HOLD['px_per_h']
    p = Plate('Z14-P40', 'Cold-holding times during a power outage',
              'Bars on one time axis show how long food stays safe with the doors kept closed: a refrigerator about 4 '
              'hours, a half-full freezer about 24 hours and a full freezer about 48 hours. Below, a cooler packed with '
              'ice keeps food at 40 degrees F or below when the outage runs longer, with its temperature checked; dry '
              'ice is handled only with insulated gloves and never used in a small, poorly ventilated space. '
              'Conceptual, not to scale apart from the time bars.', scale_note='NOT TO SCALE EXCEPT TIME BARS')
    p.add(f'<path d="M{x0} 196H{x0 + 50 * k}" stroke="{INK}" stroke-width="2"/>')
    for h in (0, 12, 24, 36, 48):
        p.add(f'<path d="M{x0 + h * k} 192v8" stroke="{INK}" stroke-width="1.6"/>'
              f'<text x="{x0 + h * k}" y="216" class="tiny" text-anchor="middle">{h} h</text>')
    for i, (hours, label, ident) in enumerate(((4, 'refrigerator, door closed', 'bar-fridge'),
                                               (24, 'half-full freezer', 'bar-half'),
                                               (48, 'full freezer', 'bar-full'))):
        y = 80 + i * 36
        p.add(f'<rect id="{ident}" data-hours="{hours}" x="{x0}" y="{y}" width="{hours * k}" height="22" fill="{FLOW}" fill-opacity="{0.45 + i * 0.2}"/>')
        p.lines(x0 - 10, y + 16, [f'{hours} h'], 'tiny', anchor='end')
        p.lines(x0 + hours * k + 10 if hours < 40 else x0 + 12, y + 16, [label], 'tiny inv' if hours >= 40 else 'tiny')
    p.lines(40, 246, ['keep doors shut;', 'open only to read', 'the thermometer'], 'tiny')
    # cooler, dry ice, snow
    p.add('<rect x="250" y="246" width="110" height="62" rx="8" fill="#5f8fa3" stroke="#183a30" stroke-width="2.2"/>'
          '<rect x="258" y="254" width="94" height="14" fill="#dcecf3"/>')
    p.lines(372, 266, ['cooler with ice: keep', '40 °F or below, check it'], 'tiny')
    p.add('<rect x="560" y="252" width="56" height="34" fill="#eef2f3" stroke="#183a30" stroke-width="2"/>'
          '<path d="M568 252l8-12M592 252l8-12" stroke="#9aa1a5" stroke-width="2"/>')
    p.lines(626, 262, ['dry ice: insulated gloves;', 'never a small closed space'], 'tiny')
    p.band('After the hold time: read the thermometer, then sort each item with the official chart.')
    return p.svg()


def chart_cell(x, y, ok, word, row, col):
    mark = check(x, y - 5, 9) if ok else cross(x, y - 5, 9)
    return (f'<g data-row="{row}" data-col="{col}" data-result="{word}">{mark}'
            f'<text x="{x + 14}" y="{y}" class="tiny">{word}</text></g>')


def z14_p41():
    p = Plate('Z14-P41', 'Keep, refreeze or discard: each food goes to its own chart row',
              'Two separate paths. Left, refrigerator food: a thermometer reading and the hours above 40 degrees F decide '
              'which column applies; after 40 F or above for more than 2 hours, or 4 hours without power, the chart '
              'row for each food decides: meat, poultry, seafood, milk, eggs and soft cheese are discarded, while hard '
              'cheese, butter and uncut fresh fruit are kept. Right, freezer food: the chart has a column for food that '
              'still has ice crystals and one for food at 40 F or above for more than 2 hours; meat, poultry and '
              'seafood may be refrozen while ice crystals remain, ice cream and frozen yogurt are discarded in both '
              'columns, and hard cheeses may be refrozen in both. Sample rows only; the full printed chart governs. '
              'Food is never tasted. Conceptual, not to scale.')
    p.panel(24, 46, 404, 290, 'neutral', 'REFRIGERATOR FOOD')
    p.panel(442, 46, 434, 290, 'neutral', 'FREEZER FOOD')
    # refrigerator path
    p.add('<rect x="44" y="86" width="48" height="24" rx="4" fill="#ffffff" stroke="#183a30" stroke-width="1.8"/>'
          '<text x="68" y="103" class="tiny" text-anchor="middle" font-size="12">46 °F</text>')
    p.lines(104, 98, ['40 °F or above for more than 2 h,', 'or 4 h without power: then'], 'tiny')
    p.lines(44, 152, ['chart row'], 'tiny mute')
    p.lines(286, 152, ['result'], 'tiny mute')
    rows_l = [('meat, poultry, seafood', False, 'discard'), ('milk, eggs, soft cheese', False, 'discard'),
              ('hard cheese, butter', True, 'keep'), ('uncut fresh fruit', True, 'keep')]
    for i, (label, ok, word) in enumerate(rows_l):
        y = 186 + i * 32
        p.add(f'<path d="M40 {y - 22}H412" stroke="#c9d1c8" stroke-width="1.2"/>')
        p.text(44, y, label, 'tiny')
        p.add(chart_cell(292, y, ok, word, label, 'over 40 F for 2 h'))
    p.lines(44, 322, ['history unknown: discard'], 'tiny warn')
    # freezer path
    p.add('<rect x="462" y="84" width="56" height="40" rx="5" fill="#dcecf3" stroke="#183a30" stroke-width="2"/>')
    for (cx, cy) in ((474, 96), (490, 110), (506, 94), (500, 116)):
        p.add(f'<path d="M{cx - 4} {cy}h8M{cx} {cy - 4}v8M{cx - 3} {cy - 3}l6 6M{cx + 3} {cy - 3}l-6 6" stroke="#3d7186" stroke-width="1.3"/>')
    p.lines(530, 92, ['the food row decides; quality', 'may suffer after refreezing'], 'tiny')
    p.lines(462, 152, ['chart row'], 'tiny mute')
    p.lines(684, 138, ['ice crystals', 'remain'], 'tiny mute')
    p.lines(782, 138, ['40 °F+ for', 'over 2 h'], 'tiny mute')
    rows_r = [('meat, poultry, seafood', (True, 'refreeze'), (False, 'discard')),
              ('ice cream, frozen yogurt', (False, 'discard'), (False, 'discard')),
              ('hard cheeses', (True, 'refreeze'), (True, 'refreeze'))]
    for i, (label, a, b) in enumerate(rows_r):
        y = 196 + i * 40
        if label.startswith('ice cream'):
            p.add(f'<rect x="456" y="{y - 26}" width="414" height="38" rx="4" fill="#fbeee7"/>')
        p.add(f'<path d="M456 {y - 26}H870" stroke="#c9d1c8" stroke-width="1.2"/>')
        p.text(462, y, label, 'tiny')
        p.add(chart_cell(692, y, a[0], a[1], label, 'ice crystals'))
        p.add(chart_cell(790, y, b[0], b[1], label, 'over 40 F for 2 h'))
    p.lines(462, 322, ['sample rows: use the full printed chart'], 'tiny')
    p.band('Never taste food to decide. If the chart row or temperature history is unclear, discard it.')
    return p.svg()


def z14_p65():
    p = Plate('Z14-P65', 'Safe thawing and why the counter fails',
              'Three safe methods: in the refrigerator on a tray at 40 degrees F or below (food may be refrozen); in '
              'cold tap water in a leak-proof bag with the water changed every 30 minutes, then cooked immediately; and '
              'in a microwave, then cooked immediately. Food thawed in cold water or a microwave is cooked before '
              'refreezing. On the counter the outer layer enters the 40 to 140 degree F danger zone while the centre is '
              'still frozen. Conceptual, not to scale.')
    labels = [('REFRIGERATOR', ['40 °F or below, on a tray;', 'may refreeze']),
              ('COLD WATER', ['leak-proof bag;', 'change water every', '30 min; cook it']),
              ('MICROWAVE', ['cook immediately', 'after thawing'])]
    for i, (title, rows) in enumerate(labels):
        x = 24 + i * 214
        p.panel(x, 46, 200, 290, 'ok', title)
        p.lines(x + 14, 276, rows, 'tiny')
    p.add('<rect x="54" y="96" width="140" height="150" rx="8" fill="#f6f7f2" stroke="#183a30" stroke-width="2"/>'
          '<path d="M60 206h128" stroke="#9aa59c" stroke-width="2"/><rect x="72" y="218" width="104" height="10" fill="#c9cdd0"/>'
          '<rect x="86" y="196" width="76" height="22" rx="6" fill="#d4a089" stroke="#183a30" stroke-width="1.6"/>')
    p.add(f'<rect x="262" y="140" width="148" height="100" rx="6" fill="#c9cdd0" stroke="#183a30" stroke-width="2"/>'
          f'<rect x="268" y="156" width="136" height="78" fill="{WATER}"/>'
          '<rect x="300" y="182" width="72" height="34" rx="8" fill="#d4a089" stroke="#183a30" stroke-width="1.6"/>')
    p.add('<rect x="470" y="116" width="150" height="104" rx="8" fill="#e2e4e4" stroke="#183a30" stroke-width="2"/>'
          '<rect x="480" y="128" width="98" height="80" fill="#4a4f52"/><rect x="502" y="168" width="56" height="22" rx="6" fill="#d4a089"/>')
    p.panel(666, 46, 210, 290, 'bad', '✕ COUNTER')
    p.add('<ellipse cx="770" cy="176" rx="76" ry="48" fill="#c0392b" fill-opacity=".28" stroke="#8b3825" stroke-width="2"/>'
          '<ellipse cx="770" cy="176" rx="40" ry="24" fill="#dcecf3" stroke="#3d7186" stroke-width="2"/>')
    p.lines(690, 252, ['outer layer: 40 to 140 °F', 'centre still frozen'], 'tiny')
    p.band('Perishable food left at room temperature more than 2 hours (1 hour above 90 °F): discard it.')
    return p.svg()


def geometry_checks():
    from xml.etree import ElementTree
    ns = '{http://www.w3.org/2000/svg}'
    out = {}
    root = ElementTree.fromstring(z14_p37())
    ticks = [(float(e.get('data-temp')), float(e.get('y1'))) for e in root.iter(ns + 'line') if e.get('data-temp')]
    (t0, y0), (t1, y1) = ticks[0], ticks[-1]
    linear = all(abs(y - (y0 + (t - t0) * (y1 - y0) / (t1 - t0))) < 0.02 for t, y in ticks)
    marks = {float(e.get('data-mark')): float(e.get('d').split()[1].split('H')[0]) for e in root.iter(ns + 'path') if e.get('data-mark')}
    marks_ok = all(abs(y - ty(t)) < 0.02 for t, y in marks.items()) and set(marks) == {145.0, 160.0, 165.0}
    out['Z14-P37'] = dict(scale_linear=linear, marks_at_stated_temperatures=marks_ok, accepted=linear and marks_ok)
    root = ElementTree.fromstring(z14_p40())
    bars = {e.get('id'): (float(e.get('data-hours')), float(e.get('width'))) for e in root.iter(ns + 'rect') if e.get('data-hours')}
    proportional = all(abs(w - h * HOLD['px_per_h']) < 0.01 for h, w in bars.values())
    out['Z14-P40'] = dict(bars={k: v[0] for k, v in bars.items()}, proportional=proportional, accepted=proportional and len(bars) == 3)
    root = ElementTree.fromstring(z14_p41())
    cells = {(g.get('data-row'), g.get('data-col')): g.get('data-result') for g in root.iter(ns + 'g') if g.get('data-row')}
    ice_cream_discarded = (cells.get(('ice cream, frozen yogurt', 'ice crystals')) == 'discard'
                           and cells.get(('ice cream, frozen yogurt', 'over 40 F for 2 h')) == 'discard')
    meat_refreeze_only_with_crystals = (cells.get(('meat, poultry, seafood', 'ice crystals')) == 'refreeze'
                                        and cells.get(('meat, poultry, seafood', 'over 40 F for 2 h')) == 'discard')
    # separate paths: no drawn path spans the gutter between the refrigerator and freezer panels (x 428-442)
    spans = [e for e in root.iter(ns + 'path') if e.get('d', '').startswith('M') and 'H' in e.get('d', '')
             and float(e.get('d')[1:].split()[0]) < 428 and float(e.get('d').split('H')[1].split()[0].rstrip('"')) > 442]
    out['Z14-P41'] = dict(ice_cream_discarded_in_both_columns=ice_cream_discarded,
                          meat_refreezes_only_with_ice_crystals=meat_refreeze_only_with_crystals,
                          no_connector_between_paths=not spans,
                          accepted=ice_cream_discarded and meat_refreeze_only_with_crystals and not spans)
    return out


PLATES = {'Z14-P37': z14_p37, 'Z14-P39': z14_p39, 'Z14-P40': z14_p40, 'Z14-P41': z14_p41, 'Z14-P65': z14_p65}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path)
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--only')
    args = parser.parse_args()
    for page, make in PLATES.items():
        if args.only and page != args.only:
            continue
        svg = make()
        if args.out:
            args.out.mkdir(parents=True, exist_ok=True)
            (args.out / f'{page}.svg').write_text(svg, encoding='utf-8')
        if args.write:
            (OUT / f'{page}.svg').write_text(svg, encoding='utf-8')
        if args.check and (OUT / f'{page}.svg').read_text(encoding='utf-8') != svg:
            raise SystemExit(f'{page} differs from a fresh build')
    geometry = geometry_checks()
    if not all(v['accepted'] for v in geometry.values()):
        raise SystemExit(f'Plate geometry check failed: {geometry}')
    print(f'{len(PLATES)} batch W2C-B06 plate(s) built; geometry {geometry}')


if __name__ == '__main__':
    main()
