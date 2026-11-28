"""Wave 2C batch W2C-B08: the household water supply.

Plates draw how much water to store and for how long, the three advisory tiers, private
well testing and why boiling concentrates nitrate, and floodwater as a source to avoid.
Quantities are computed and checked: jug counts equal people x days x 1 gallon, refill
marks sit 6 months apart, and the boiled pot keeps the same nitrate in less water.
Sources: CDC storage (W14, W35), CDC advisories (W07, D12), EPA well testing (W37),
MDH nitrate (W36), CDC floodwater (W39), read 2026-11-28. Run with --out, --write or --check.
"""
import argparse
from pathlib import Path

from w2c_svg import FLOW, INK, REVERSE, WATER, WATER_EDGE, Plate, check, cross, flame, jug, person

OUT = Path(__file__).resolve().parents[1] / 'foundations/visual/w2c_technical/revised'
PEOPLE, MIN_DAYS, GOAL_DAYS = 4, 3, 14
TIMELINE = dict(x0=70, px_per_month=31.0, months=24, every=6)
POT = dict(before=0.80, after=0.40, dots=14)


def can5(x, y, gal=5, fill='#5f8fa3'):
    return (f'<g data-gal="{gal}"><rect x="{x}" y="{y + 6}" width="30" height="36" rx="4" fill="{fill}" stroke="{INK}" stroke-width="1.6"/>'
            f'<rect x="{x + 9}" y="{y}" width="12" height="7" rx="2" fill="#2f3b40"/></g>')


# ---------------------------------------------------------------- Z13-P33
def z13_p33():
    p = Plate('Z13-P33', 'How much drinking water to store for a household',
              'A household of four. Left: the minimum of 1 gallon per person per day for 3 days drawn as a grid of '
              '12 one-gallon jugs, one row per person and one column per day. Centre: the 2-week goal of 56 gallons '
              'drawn as eleven 5-gallon containers and one 1-gallon jug. Right: more water for pregnancy, illness, '
              'pets or a hot climate, and storage in a cool place (50 to 70 degrees F) out of direct sunlight and away '
              'from gasoline and pesticides. Conceptual, not to scale.')
    p.panel(24, 46, 304, 290, 'ok', '✓ 3-DAY MINIMUM')
    p.panel(342, 46, 270, 290, 'neutral', '2-WEEK GOAL')
    p.panel(626, 46, 250, 290, 'neutral', 'MORE, AND WHERE')
    for d in range(MIN_DAYS):
        p.text(122 + d * 56, 98, f'day {d + 1}', 'tiny', anchor='middle')
    for r in range(PEOPLE):
        y = 106 + r * 44
        p.add(person(62, y + 38, 36))
        for d in range(MIN_DAYS):
            p.add(f'<g data-gal="1" data-day="{d + 1}">{jug(110 + d * 56, y, 36, None)}</g>')
    p.lines(40, 304, ['4 people x 1 gal x 3 days', '= 12 gallons'], 'tiny ok')
    k = 0
    for row in range(3):
        for col in range(4):
            if k < 11:
                p.add(can5(364 + col * 52, 90 + row * 56))
                k += 1
    p.add(f'<g data-gal="1">{jug(530, 206, 36, None)}</g>')
    p.lines(358, 282, ['4 people x 14 days = 56 gal:', 'eleven 5-gal + one 1-gal'], 'tiny')
    p.lines(642, 96, ['store more for:', 'pregnancy, illness,', 'pets, a hot climate'], 'tiny')
    p.add(f'<rect x="648" y="168" width="14" height="60" rx="7" fill="#ffffff" stroke="{INK}" stroke-width="2"/>'
          f'<rect x="652" y="196" width="6" height="30" fill="{WATER_EDGE}"/>')
    p.lines(672, 196, ['cool: 50 to 70 °F,', 'out of sunlight'], 'tiny')
    p.add('<path d="M650 262h26v32h-26z" fill="#c4472f" stroke="#183a30" stroke-width="1.8"/><path d="M656 262v-8h12" fill="none" stroke="#183a30" stroke-width="2"/>')
    p.add(cross(690, 262, 9))
    p.lines(708, 278, ['away from gasoline', 'and pesticides'], 'tiny')
    p.band('Leaking, cracked, chemical-smelling or algae-fouled containers: discard or use as non-potable.')
    return p.svg()


# ---------------------------------------------------------------- Z04-P50
def z04_p50():
    t = TIMELINE
    p = Plate('Z04-P50', 'Rotate stored water every 6 months and inspect the containers',
              'Top: a two-year timeline with self-filled drinking water replaced every 6 months (refill marks at 0, 6, '
              '12, 18 and 24 months, drawn to scale); commercial bottled water follows its printed date. Lower left: '
              'containers are replaced when they leak, the cap swells, the plastic turns brittle or the water smells. '
              'Lower right: water is stored cool (50 to 70 degrees F), out of direct sunlight and away from fuel and '
              'pesticides, with a portable portion ready for evacuation. Conceptual, not to scale apart from the timeline.',
              scale_note='NOT TO SCALE EXCEPT TIMELINE')
    p.panel(24, 46, 852, 150, 'neutral', 'SELF-FILLED WATER: REPLACE EVERY 6 MONTHS')
    x1 = t['x0'] + t['months'] * t['px_per_month']
    p.add(f'<path d="M{t["x0"]} 160H{x1}" stroke="{INK}" stroke-width="2.4"/>')
    for m in range(0, t['months'] + 1, 3):
        x = t['x0'] + m * t['px_per_month']
        p.add(f'<path d="M{x} 155v10" stroke="{INK}" stroke-width="1.6"/>')
        if m % t['every'] == 0:
            p.text(x, 184, f'{m} mo', 'tiny', anchor='middle')
            p.add(f'<g data-refill-month="{m}" transform="translate({x - 11} 104)">{jug(0, 0, 40, None, "#cfe6ef")}</g>')
    p.lines(560, 92, ['commercial bottles: printed date'], 'tiny')
    p.panel(24, 206, 418, 130, 'bad', '✕ REPLACE THE CONTAINER IF')
    items = [('leaking', 48), ('cap swollen', 150), ('brittle plastic', 254), ('off odour', 362)]
    for label, x in items:
        p.add(jug(x + 6, 252, 40, None, '#eef2f3'))
        p.lines(x - 6, 320, [label], 'tiny')
    p.add('<path d="M64 296q-4 7 0 10q4-3 0-10z" fill="#3d7186"/>'
          '<path d="M160 250q14-10 28 0" fill="none" stroke="#8b3825" stroke-width="2.4"/>'
          '<path d="M268 262l8 10-6 8 8 10" fill="none" stroke="#8b3825" stroke-width="2"/>'
          '<path d="M394 248q6-8 0-16M402 248q6-8 0-16" fill="none" stroke="#6b7f8c" stroke-width="2"/>')
    p.panel(456, 206, 420, 130, 'ok', '✓ STORE AND STAGE')
    p.add(f'<rect x="478" y="244" width="12" height="56" rx="6" fill="#ffffff" stroke="{INK}" stroke-width="2"/>'
          f'<rect x="481" y="270" width="6" height="28" fill="{WATER_EDGE}"/>')
    p.lines(498, 262, ['50 to 70 °F, dark,', 'away from fuel'], 'tiny')
    p.add('<rect x="634" y="262" width="56" height="54" rx="10" fill="#7a8f6d" stroke="#183a30" stroke-width="2"/>'
          '<rect x="646" y="250" width="12" height="16" rx="2" fill="#cfe6ef" stroke="#183a30" stroke-width="1.4"/>'
          '<rect x="664" y="250" width="12" height="16" rx="2" fill="#cfe6ef" stroke="#183a30" stroke-width="1.4"/>')
    p.lines(700, 282, ['portable portion', 'for evacuation'], 'tiny')
    p.band('Leaking, sun-degraded or chemically exposed container: replace it; do not trust the water.')
    return p.svg()


# ---------------------------------------------------------------- Z13-P36
def tap(x, y):
    return (f'<path d="M{x} {y}h30v-10h12v26h-12v-6h-30z" fill="#c9cdd0" stroke="{INK}" stroke-width="1.8"/>'
            f'<path d="M{x + 36} {y + 18}v12" stroke="{WATER_EDGE}" stroke-width="3"/>')


def z13_p36():
    p = Plate('Z13-P36', 'Boil Water, Do Not Drink and Do Not Use advisories',
              'Three advisory tiers. Boil Water: germs; bring tap water to a full rolling boil for 1 minute (3 minutes '
              'above 6,500 feet), even if it was filtered, and use bottled or boiled water for drinking, food and '
              'brushing teeth; use ready-made infant formula when available. Do Not Drink: chemicals or toxins; use '
              'bottled water for drinking, cooking, brushing teeth, washing produce, formula, ice and pets; boiling does '
              'not make the water safe. Do Not Use: any contact may be dangerous; use bottled water for every purpose. '
              'During any advisory, no water or ice from refrigerator dispensers. Conceptual, not to scale.')
    p.panel(24, 46, 276, 246, 'neutral', 'BOIL WATER')
    p.panel(312, 46, 276, 246, 'bad', 'DO NOT DRINK')
    p.panel(600, 46, 276, 246, 'bad', 'DO NOT USE')
    p.add('<path d="M60 120h96v46q0 14-14 14h-68q-14 0-14-14z" fill="#c9cdd0" stroke="#183a30" stroke-width="2"/>'
          f'<path d="M64 128h88v6h-88z" fill="{WATER}"/>' + flame(108, 196, 0.8))
    p.lines(170, 120, ['1 min', '(3 min above', '6,500 ft)'], 'tiny')
    p.lines(40, 226, ['germs: boil even if filtered;', 'bottled or boiled for food', 'and teeth'], 'tiny')
    p.add('<path d="M348 120h96v46q0 14-14 14h-68q-14 0-14-14z" fill="#c9cdd0" stroke="#183a30" stroke-width="2"/>' + flame(396, 196, 0.8))
    p.add(cross(452, 118, 12))
    p.lines(474, 124, ['boiling', 'does not help'], 'tiny warn')
    p.lines(328, 226, ['chemicals or toxins: bottled', 'water to drink, cook, teeth,', 'formula, ice, pets'], 'tiny')
    p.add(tap(640, 130))
    p.add('<path d="M760 100v40M752 140h16" stroke="#183a30" stroke-width="2.4"/><path d="M748 146l-6 22M760 146v24M772 146l6 22" stroke="#3d7186" stroke-width="2" stroke-dasharray="4 3"/>')
    p.add(cross(700, 112, 12) + cross(800, 112, 12))
    p.lines(616, 226, ['any contact may harm:', 'bottled water for', 'every purpose'], 'tiny')
    p.panel(24, 300, 852, 38, 'neutral')
    p.lines(40, 325, ['Any advisory: no water or ice from refrigerator dispensers.'], 'tiny')
    p.band('Keep every precaution until the utility or health officials say the advisory has ended.')
    return p.svg()


# ---------------------------------------------------------------- Z13-P43
def pot_with_dots(x, y, level, ident):
    """Pot whose water fills `level` of its height; POT['dots'] nitrate dots spread in the water."""
    w, h = 120, 90
    top = y + h * (1 - level)
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="#e8eef0" stroke="{INK}" stroke-width="2"/>',
           f'<rect id="{ident}-water" x="{x + 3}" y="{top:.1f}" width="{w - 6}" height="{y + h - top - 3:.1f}" fill="{WATER}"/>']
    cols = 7
    rows = POT['dots'] // cols
    for i in range(POT['dots']):
        cx = x + 12 + (i % cols) * ((w - 24) / (cols - 1))
        cy = top + 8 + (i // cols) * ((y + h - top - 16) / max(rows - 1, 1))
        out.append(f'<circle class="{ident}-n" cx="{cx:.1f}" cy="{cy:.1f}" r="3.2" fill="#8b3825"/>')
    return ''.join(out)


def z13_p43():
    p = Plate('Z13-P43', 'Test a private well every year; boiling concentrates nitrate',
              'Left: every year a laboratory certified for drinking-water testing checks the well for total coliform '
              'bacteria, nitrate, total dissolved solids and pH. Centre: test again after flooding, well repair or a '
              'change in taste, odour or colour, and before bringing a new baby home; test more often where small '
              'children, elderly adults, or pregnant or nursing people live. Right: boiling evaporates water but leaves '
              'the nitrate, so the same nitrate ends up in less water; above 10 mg/L nitrate use bottled water, '
              'especially for formula for babies under six months. Conceptual, not to scale.')
    p.panel(24, 46, 260, 290, 'ok', '✓ EVERY YEAR')
    p.panel(296, 46, 270, 290, 'neutral', 'TEST AGAIN AFTER')
    p.panel(578, 46, 298, 290, 'bad', '✕ BOILING CONCENTRATES')
    p.add('<rect x="54" y="100" width="40" height="64" rx="6" fill="#ffffff" stroke="#183a30" stroke-width="2"/>'
          '<rect x="58" y="92" width="32" height="10" rx="2" fill="#5f8fa3"/><path d="M60 124h28M60 136h20" stroke="#9aa59c" stroke-width="2"/>')
    p.lines(106, 120, ['certified', 'drinking-water lab'], 'tiny')
    p.lines(40, 210, ['total coliform', 'nitrate', 'dissolved solids', 'pH'], 'tiny')
    triggers = ['flooding', 'well repair', 'taste, odour or colour', 'a new baby coming home']
    p.lines(312, 100, triggers, 'tiny')
    p.lines(312, 226, ['test more often with', 'small children, elderly,', 'pregnant or nursing'], 'tiny')
    p.add(pot_with_dots(596, 116, POT['before'], 'before') + pot_with_dots(740, 116, POT['after'], 'after'))
    p.arrow('M720 160H736', 'ink', 2.5)
    p.lines(596, 98, ['before'], 'tiny')
    p.lines(740, 98, ['after boiling'], 'tiny')
    p.lines(594, 238, ['same nitrate, less water;', 'above 10 mg/L use bottled', 'water, above all for formula', 'for babies under 6 months'], 'tiny')
    p.band('Coliform, or nitrate, arsenic or lead above the limit: switch to safe water; call health officials.')
    return p.svg()


# ---------------------------------------------------------------- Z04-P19
def z04_p19():
    p = Plate('Z04-P19', 'Floodwater is not a water source',
              'Left: a flooded street carries sewage from an overflowing pipe, a drum of hazardous waste, debris and '
              'a downed power line in the water; the person on dry ground stays out of the water and never walks or '
              'drives across a flooded road. Right: drinking water comes from stored or sealed supplies and official '
              'distribution until local officials say how the water can be used; food or drink touched by floodwater '
              'can cause diarrheal disease. Conceptual, not to scale.')
    p.panel(24, 46, 580, 290, 'bad', '✕ STAY OUT OF FLOODWATER')
    p.panel(618, 46, 258, 290, 'ok', '✓ STORED WATER')
    p.add('<path d="M70 256V176l56-38 56 38v80" fill="#e9e4d8" stroke="#183a30" stroke-width="2"/>')
    p.add(f'<path d="M40 214q30-10 60 0t60 0 60 0 60 0 60 0 60 0 60 0 60 0V326H40z" fill="{WATER}" fill-opacity=".8" stroke="{WATER_EDGE}" stroke-width="2"/>')
    p.add('<rect x="200" y="200" width="18" height="40" fill="#7c8c95"/><path d="M209 240q8 10 0 22" fill="none" stroke="#6b5a3a" stroke-width="4"/>')
    p.add('<rect x="268" y="222" width="30" height="38" rx="3" fill="#d9a441" stroke="#183a30" stroke-width="2"/><path d="M268 236h30" stroke="#183a30" stroke-width="1.4"/>')
    p.add('<path d="M330 252l60-8" stroke="#6b5a3a" stroke-width="9" stroke-linecap="round"/>')
    p.add('<path d="M430 100v130" stroke="#5b4630" stroke-width="7"/><path d="M430 106l60 14q-6 60-14 98" fill="none" stroke="#183a30" stroke-width="2.4"/>'
          '<path d="M470 222l6-10 6 10 6-10" fill="none" stroke="#f2c94c" stroke-width="2.6"/>')
    p.add(person(552, 210, 70))
    p.add('<path d="M520 200H612" stroke="#8a7350" stroke-width="5"/>')
    p.add(cross(500, 176, 11))
    p.lines(40, 92, ['sewage, hazardous waste, debris,', 'downed power lines'], 'tiny')
    p.add(jug(640, 100, 60, None) + jug(686, 100, 60, None))
    p.add('<rect x="740" y="96" width="112" height="70" rx="4" fill="#ffffff" stroke="#183a30" stroke-width="2"/>'
          '<path d="M752 116h88M752 132h88M752 148h56" stroke="#9aa59c" stroke-width="3"/>')
    p.lines(634, 196, ['drink stored or sealed', 'water until local officials', 'say how to use tap water'], 'tiny')
    p.lines(634, 274, ['floodwater on food or', 'drink: diarrheal disease'], 'tiny warn')
    p.band('Never wade into floodwater for water; never boil water suspected of fuel or chemicals.')
    return p.svg()


PLATES = {'Z13-P33': z13_p33, 'Z04-P50': z04_p50, 'Z13-P36': z13_p36, 'Z13-P43': z13_p43, 'Z04-P19': z04_p19}


def checks():
    from xml.etree import ElementTree
    ns = '{http://www.w3.org/2000/svg}'
    out = {}
    root = ElementTree.fromstring(z13_p33())
    gals = [int(g.get('data-gal')) for g in root.iter(ns + 'g') if g.get('data-gal')]
    minimum = sum(1 for g in root.iter(ns + 'g') if g.get('data-day'))
    out['Z13-P33'] = dict(minimum_jugs=minimum, goal_gallons=sum(gals) - minimum,
                          accepted=minimum == PEOPLE * MIN_DAYS and sum(gals) - minimum == PEOPLE * GOAL_DAYS)
    root = ElementTree.fromstring(z04_p50())
    months = sorted(int(g.get('data-refill-month')) for g in root.iter(ns + 'g') if g.get('data-refill-month'))
    xs = [float(g.get('transform').split('(')[1].split()[0]) + 11 for g in root.iter(ns + 'g') if g.get('data-refill-month')]
    spaced = all(abs((b - a) - TIMELINE['every'] * TIMELINE['px_per_month']) < 0.01 for a, b in zip(xs, xs[1:]))
    out['Z04-P50'] = dict(refill_months=months, spacing_is_6_months=spaced, accepted=months == [0, 6, 12, 18, 24] and spaced)
    root = ElementTree.fromstring(z13_p43())
    get = {e.get('id'): e for e in root.iter() if e.get('id')}
    before = sum(1 for e in root.iter(ns + 'circle') if e.get('class') == 'before-n')
    after = sum(1 for e in root.iter(ns + 'circle') if e.get('class') == 'after-n')
    vol_b, vol_a = float(get['before-water'].get('height')), float(get['after-water'].get('height'))
    out['Z13-P43'] = dict(nitrate_dots_before=before, after=after, water_height_before=vol_b, after_height=vol_a,
                          concentration_ratio=round((after / vol_a) / (before / vol_b), 2),
                          accepted=before == after and vol_a < vol_b)
    p36 = z13_p36()
    out['Z13-P36'] = dict(boiling_not_for_chemicals='does not help' in p36, three_tiers=all(t in p36 for t in ('BOIL WATER', 'DO NOT DRINK', 'DO NOT USE')),
                          accepted=True)
    out['Z13-P36']['accepted'] = all(v for k, v in out['Z13-P36'].items() if k != 'accepted')
    p19 = z04_p19()
    out['Z04-P19'] = dict(stay_out='STAY OUT' in p19, officials='local officials' in p19, accepted='STAY OUT' in p19 and 'local officials' in p19)
    return out


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
    result = checks()
    if not all(v['accepted'] for v in result.values()):
        raise SystemExit(f'Plate check failed: {result}')
    print(f'{len(PLATES)} batch W2C-B08 plate(s) built; checks {result}')


if __name__ == '__main__':
    main()
