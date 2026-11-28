"""Wave 2C batch W2C-B03: combustion products and fuel vapours in occupied spaces.

Each plate shows where carbon monoxide or fuel vapour comes from, where it goes in
a building, where warning devices sit, and the exit. Sources are in the ledger.
Run with --out DIR to preview, --write to refresh the revised SVGs, or --check.
"""
import argparse
from pathlib import Path

from w2c_svg import (FLOW, INK, REVERSE, STEEL, Plate, alarm, check, cross, flame, gas, jug, person, pipe)

OUT = Path(__file__).resolve().parents[1] / 'foundations/visual/w2c_technical/revised'


def room(x, y, w, h, floor='#cbbf9f'):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#f5f2e8" stroke="#183a30" stroke-width="2.4"/>'
            f'<rect x="{x}" y="{y + h - 8}" width="{w}" height="8" fill="{floor}"/>')


def z13_p20():
    p = Plate('Z13-P20', 'Carbon monoxide from improvised indoor heat',
              'Left: a closed room heated with an open gas oven, a charcoal grill and a camp stove. Carbon monoxide '
              'spreads through the room and reaches a person asleep on a couch; it is colourless and odourless and a '
              'cracked window does not clear it. Right: when home heat fails, people stay in warm layers in one '
              'interior room and go early to a warming centre or another place with power. Conceptual, not to scale.')
    p.panel(24, 46, 470, 290, 'bad', '✕ IMPROVISED INDOOR HEAT')
    p.panel(512, 46, 364, 290, 'ok', '✓ WHEN HOME HEAT FAILS')
    p.add(room(40, 84, 438, 238))
    p.add(gas(52, 92, 414, 190))
    p.add('<rect x="420" y="112" width="40" height="70" fill="#d8ecf4" stroke="#183a30" stroke-width="2"/>'
          '<rect x="420" y="138" width="40" height="6" fill="#f5f2e8"/>'
          '<path d="M420 138h40M420 144h40" stroke="#183a30" stroke-width="1.6"/>')
    # oven with door open
    p.add('<rect x="60" y="216" width="76" height="96" rx="4" fill="#d9dcdc" stroke="#183a30" stroke-width="2.2"/>'
          '<path d="M64 262l-26 30h76l-14-30z" fill="#bfc4c4" stroke="#183a30" stroke-width="2"/>'
          '<rect x="72" y="226" width="52" height="30" fill="#3b3b3b"/>')
    p.add(flame(98, 252, 0.55))
    # charcoal grill and camp stove
    p.add('<path d="M168 262h56l-8 22h-40z" fill="#3e3e3e" stroke="#183a30" stroke-width="2"/>'
          '<path d="M180 284l-8 28M212 284l8 28" stroke="#183a30" stroke-width="2.4"/>')
    for k in range(4):
        p.add(f'<circle cx="{180 + k * 11}" cy="260" r="4" fill="#e0703a"/>')
    p.add('<rect x="252" y="290" width="52" height="22" rx="3" fill="#5f8f6a" stroke="#183a30" stroke-width="2"/>')
    p.add(flame(278, 290, 0.5))
    p.add(cross(98, 206, 11), cross(196, 246, 11), cross(278, 268, 11))
    # sleeper on couch inside the CO
    p.add('<rect x="336" y="272" width="118" height="30" rx="8" fill="#9aa69c" stroke="#183a30" stroke-width="2"/>')
    p.add(person(352, 272, 92, 'lie'))
    p.add(alarm(300, 104, 'co', 12))
    for x0, y0 in ((110, 200), (200, 236), (280, 252)):
        p.arrow(f'M{x0} {y0}C{x0 + 20} {y0 - 70} {x0 + 120} {y0 - 120} {x0 + 170} {y0 - 110}', 'air', 2.6, dash='5 4')
    p.lines(70, 116, ['carbon monoxide: no colour,', 'no smell; fills a closed room'], 'tiny')
    p.lines(290, 196, ['a cracked window', 'does not clear it'], 'tiny')
    p.lead((410, 192), (420, 144))
    # right: layers, one interior room, warming centre
    p.add(room(532, 120, 150, 180))
    p.add(person(580, 292, 86, fill='#7a5a43'), person(624, 292, 70, fill='#8b6a52'))
    p.lines(530, 104, ['warm layers in one', 'interior room'], 'tiny')
    p.add('<rect x="744" y="176" width="112" height="86" rx="4" fill="#e6efe9" stroke="#183a30" stroke-width="2.4"/>'
          '<path d="M736 178l64-40 64 40" fill="none" stroke="#183a30" stroke-width="2.4"/>'
          '<rect x="786" y="222" width="28" height="40" fill="#cfe0e6" stroke="#183a30" stroke-width="1.6"/>')
    p.arrow('M690 236H738', 'flow', 4)
    p.lines(718, 284, ['go early to a', 'warming centre or', 'a place with power'], 'tiny')
    p.band('Headache, dizziness, nausea or a CO alarm: get everyone outside now, then call 911.')
    return p.svg()


def z13_p56():
    p = Plate('Z13-P56', 'Smoke and carbon monoxide alarm placement and replacement',
              'Cutaway of a three-level home. A smoke alarm and a carbon monoxide alarm are on every level, including '
              'the basement, and a carbon monoxide alarm sits in the hallway outside the bedrooms. No carbon monoxide '
              'alarm is placed in the kitchen or directly above the furnace. A side panel notes that the test button '
              'checks circuitry rather than sensor accuracy, smoke alarms are replaced every ten years or as the maker '
              'directs, and carbon monoxide alarms at the replacement age the maker gives. Conceptual, not to scale.')
    # house section
    p.add('<path d="M40 128L250 56L460 128" fill="#e9e2cf" stroke="#183a30" stroke-width="2.4"/>')
    for y0, label in ((128, 'bedroom level'), (204, 'main level')):
        p.add(f'<rect x="56" y="{y0}" width="388" height="64" fill="#f6f3ea" stroke="#183a30" stroke-width="2.2"/>')
    p.add('<rect x="56" y="268" width="388" height="62" fill="#e7e2d4" stroke="#183a30" stroke-width="2.2"/>')
    p.lines(64, 146, ['upper'], 'tiny')
    p.lines(64, 222, ['main'], 'tiny')
    p.lines(64, 286, ['basement'], 'tiny')
    p.add('<path d="M200 128v64M318 128v64M318 204v64" stroke="#183a30" stroke-width="2"/>')
    p.lines(214, 184, ['hall'], 'tiny')
    p.lines(76, 184, ['bedroom'], 'tiny')
    p.lines(330, 184, ['bedroom'], 'tiny')
    # alarms per level
    p.add(alarm(250, 142, 'smoke'), alarm(280, 170, 'co'))
    p.add(alarm(150, 218, 'smoke'), alarm(240, 246, 'co'))
    p.add('<rect x="350" y="230" width="72" height="30" fill="#d9dcdc" stroke="#183a30" stroke-width="2"/>')
    p.lines(326, 224, ['kitchen'], 'tiny')
    p.add(alarm(420, 214, 'co', 9), cross(420, 214, 13))
    p.add(alarm(220, 284, 'smoke'), alarm(160, 304, 'co'))
    p.add('<rect x="330" y="290" width="40" height="36" fill="#9aa1a5" stroke="#183a30" stroke-width="2"/>')
    p.lines(380, 316, ['furnace'], 'tiny')
    p.add(alarm(350, 280, 'co', 9), cross(350, 278, 13))
    # rules panel
    p.panel(476, 46, 400, 290, 'neutral', 'PLACEMENT AND REPLACEMENT')
    p.add(alarm(500, 96, 'smoke'), alarm(500, 132, 'co'))
    p.lines(522, 102, ['smoke alarm on every level,', 'including the basement'], 'tiny')
    p.lines(522, 138 + 12, ['CO alarm on every level and', 'outside sleeping areas'], 'tiny')
    p.add(cross(500, 202, 11))
    p.lines(522, 200, ['no CO alarm in the kitchen or', 'right above fuel-burning gear'], 'tiny')
    p.lines(492, 262, ['test button checks circuitry,', 'not CO sensor accuracy', 'replace: smoke 10 yr or per', 'maker; CO at maker\'s age'], 'tiny')
    p.band('Steady CO alarm: get everyone outside to fresh air, then call 911 from outside.')
    return p.svg()


def z15_p43():
    ft = 6.0  # plan scale: 6 px per foot, drawn as a scale bar
    p = Plate('Z15-P43', 'Outage household layout with no indoor combustion',
              'Plan view drawn to an indicated scale. A generator runs outside with its exhaust pointed away, at least '
              '20 feet from the nearest window and door and from the attached garage. Inside, LED lanterns replace '
              'flame, the refrigerator and freezer stay closed, electronics are unplugged against surges, and a carbon '
              'monoxide alarm is on the level. A side panel gives the cold-holding times, the rule that generators, '
              'camp stoves and charcoal grills stay outdoors, and the exit triggers. Clearances are drawn to the '
              'indicated scale; symbols are not to scale.',
              scale_note='CLEARANCES TO SCALE · SYMBOLS NOT TO SCALE')
    hx, hy, hw, hh = 40, 74, 36 * ft, 30 * ft
    p.add(f'<rect id="house" x="{hx}" y="{hy}" width="{hw}" height="{hh}" fill="#f6f3ea" stroke="#183a30" stroke-width="2.6"/>')
    p.add(f'<rect id="garage" x="{hx}" y="{hy + hh}" width="{18 * ft}" height="{8 * ft}" fill="#ebe6d7" stroke="#183a30" stroke-width="2.2"/>')
    p.lines(hx + 8, hy + hh + 30, ['attached garage'], 'tiny')
    wx = hx + hw
    p.add(f'<rect id="window" x="{wx - 4}" y="{hy + 30}" width="8" height="40" fill="#cfe0e6" stroke="#183a30" stroke-width="1.6"/>')
    gx = wx + 20 * ft
    p.add(f'<rect id="generator" x="{gx}" y="{hy + 31}" width="34" height="38" rx="4" fill="#d6a542" stroke="#183a30" stroke-width="2"/>')
    p.arrow(f'M{gx + 36} {hy + 50}H{gx + 72}', 'air', 3)
    p.add(f'<path id="clearance" d="M{wx} {hy + 90}H{gx}" stroke="{INK}" stroke-width="1.8"/>'
          f'<path d="M{wx} {hy + 82}v16M{gx} {hy + 82}v16" stroke="{INK}" stroke-width="1.8"/>')
    p.lines(wx + 12, hy + 116, ['at least 20 ft from', 'windows, doors and', 'attached garage'], 'tiny')
    p.lines(gx - 12, hy + 18, ['generator,', 'exhaust away'], 'tiny')
    p.lines(wx - 60, hy + 22, ['window'], 'tiny')
    # inside
    p.add(f'<rect x="{hx + 14}" y="{hy + 14}" width="38" height="62" fill="#e9eef0" stroke="#183a30" stroke-width="2"/>'
          f'<path d="M{hx + 14} {hy + 38}h38" stroke="#183a30" stroke-width="1.6"/>')
    p.lines(hx + 60, hy + 34, ['fridge and', 'freezer closed'], 'tiny')
    p.add(f'<path d="M{hx + 22} {hy + 100}h16v24h-16zM{hx + 50} {hy + 100}h16v24h-16z" fill="#f6e7a8" stroke="#183a30" stroke-width="1.8"/>')
    p.lines(hx + 74, hy + 118, ['LED lanterns'], 'tiny')
    p.add(alarm(hx + 186, hy + 108, 'co', 11))
    p.lines(hx + 150, hy + 140, ['CO alarm'], 'tiny')
    p.add(f'<rect x="{hx + 22}" y="{hy + 148}" width="30" height="11" rx="2" fill="#c9cdd0" stroke="#183a30" stroke-width="1.4"/>'
          f'<path d="M{hx + 52} {hy + 153}h12" stroke="#183a30" stroke-width="1.6" stroke-dasharray="3 3"/>')
    p.lines(hx + 74, hy + 160, ['unplugged'], 'tiny')
    # scale comparator
    p.add(f'<g id="scale-bar"><rect x="{wx + 30}" y="300" width="{10 * ft}" height="7" fill="#183a30"/>'
          f'<rect x="{wx + 30 + 10 * ft}" y="300" width="{10 * ft}" height="7" fill="#ffffff" stroke="#183a30" stroke-width="1.4"/></g>')
    p.lines(wx + 30, 326, ['0 to 20 ft at plan scale'], 'tiny')
    # side panel
    p.panel(560, 46, 316, 290, 'neutral', 'KEEP COLD, KEEP CLEAR AIR')
    p.lines(578, 98, ['closed refrigerator: about 4 h', 'full closed freezer: about 48 h'], 'tiny')
    p.add(cross(588, 158, 11))
    p.lines(606, 162, ['no gas stove or oven for heat'], 'tiny')
    p.add(cross(588, 194, 11))
    p.lines(606, 198, ['generators, camp stoves and', 'charcoal grills stay outdoors,', '20 ft from windows'], 'tiny')
    p.lines(578, 290, ['leave for a place with power if', 'heat or cold becomes extreme'], 'tiny')
    p.band('CO alarm, unsafe indoor cold or heat, or medical power running out: relocate or call 911.')
    return p.svg()


def z13_p60():
    p = Plate('Z13-P60', 'Fuel vapour inside a home versus outdoor storage',
              'Left: gasoline cans stored in a basement. Their vapour is heavier than air, collects low and travels '
              'across the floor to the pilot flame of a water heater or furnace, where it can ignite. Right: sealed, '
              'approved fuel containers and a propane cylinder stored upright outdoors in a ventilated shed away from '
              'living quarters and ignition sources. Conceptual, not to scale.')
    p.panel(24, 46, 430, 290, 'bad', '✕ FUEL STORED INDOORS')
    p.panel(472, 46, 404, 290, 'ok', '✓ OUTDOORS, VENTILATED, AWAY')
    p.add('<rect x="40" y="90" width="398" height="232" fill="#ece7d9" stroke="#183a30" stroke-width="2.4"/>'
          '<rect x="40" y="314" width="398" height="8" fill="#b8ad92"/>')
    for k in range(2):
        cx = 66 + k * 46
        p.add(f'<path d="M{cx} 314v-46l8-10h24v56z" fill="#c44a35" stroke="#183a30" stroke-width="2"/>'
              f'<rect x="{cx + 20}" y="250" width="8" height="10" fill="#183a30"/>')
    p.add('<path d="M70 312C140 300 220 312 300 304C330 300 350 306 366 300" fill="none" stroke="#8a8f86" stroke-width="16" '
          'stroke-opacity=".35" stroke-linecap="round"/>')
    p.arrow('M150 302C220 296 300 304 352 298', 'air', 2.8, dash='6 5')
    p.add('<rect x="352" y="196" width="56" height="118" rx="10" fill="#c8ccc9" stroke="#183a30" stroke-width="2.2"/>'
          '<rect x="364" y="286" width="32" height="18" fill="#3b3b3b"/>')
    p.add(flame(380, 302, 0.45))
    p.lines(56, 118, ['gasoline vapour is heavier', 'than air and stays low'], 'tiny')
    p.lines(214, 256, ['travels to pilot', 'lights and sparks'], 'tiny')
    p.lead((270, 262), (300, 296))
    p.lines(240, 214, ['water heater', 'or furnace'], 'tiny')
    p.lead((330, 214), (352, 226))
    # right: outdoor ventilated shed away from the house
    p.add('<path d="M488 196V120l40-28 40 28v76" fill="#e9e2cf" stroke="#183a30" stroke-width="2.4"/>')
    p.lines(500, 216, ['home'], 'tiny')
    p.add('<rect x="724" y="150" width="140" height="150" fill="#d7d0bd" stroke="#183a30" stroke-width="2.4"/>'
          '<path d="M716 152l78-38 78 38" fill="none" stroke="#183a30" stroke-width="2.4"/>')
    for k in range(4):
        p.add(f'<path d="M{736 + k * 8} 160h4M{736 + k * 8} 166h4" stroke="#183a30" stroke-width="2"/>')
    p.add('<path d="M744 298v-46l8-10h24v56z" fill="#c44a35" stroke="#183a30" stroke-width="2"/>'
          '<rect x="806" y="232" width="30" height="66" rx="13" fill="#e7e7e2" stroke="#183a30" stroke-width="2"/>'
          '<rect x="814" y="222" width="14" height="12" fill="#9aa1a5" stroke="#183a30" stroke-width="1.6"/>')
    p.arrow('M580 236H714', 'flow', 3)
    p.lines(582, 196, ['away from living', 'quarters and sparks'], 'tiny')
    p.lines(734, 190, ['vented; sealed,', 'approved cans'], 'tiny')
    p.lines(724, 324, ['cylinder upright'], 'tiny')
    p.band('Strong fuel odour or a hissing cylinder: leave, avoid switches and flames, call from outside.')
    return p.svg()


def z13_p57():
    p = Plate('Z13-P57', 'When a portable extinguisher is an option, and when to leave',
              'Left: a small fire confined to one pan or wastebasket. The user has alerted others, the fire department '
              'has been called, the user stands with a clear escape route behind them and sprays at the base of the '
              'fire. Below, the four PASS steps: pull the pin, aim low at the base, squeeze slowly and evenly, sweep '
              'side to side. Right: smoke filling the room, fire spreading beyond one object, or no clear escape route '
              'means leaving and calling 911. Conceptual, not to scale.')
    p.panel(24, 46, 470, 290, 'ok', '✓ ONLY IF ALL ARE TRUE')
    p.panel(512, 46, 364, 290, 'bad', '✕ LEAVE, THEN CALL 911')
    p.add('<rect x="40" y="88" width="438" height="148" fill="#f5f2e8" stroke="#183a30" stroke-width="2.2"/>'
          '<rect x="40" y="228" width="438" height="8" fill="#cbbf9f"/>')
    p.add('<rect x="46" y="128" width="30" height="100" fill="#b6c9b9" stroke="#183a30" stroke-width="2"/>'
          '<circle cx="70" cy="180" r="2.6" fill="#183a30"/>')
    p.lines(84, 110, ['clear escape route', 'behind you'], 'tiny')
    p.lead((90, 118), (64, 128))
    p.add(person(150, 228, 100, fill='#4d6a78'))
    p.add('<rect x="166" y="162" width="18" height="40" rx="6" fill="#c0392b" stroke="#183a30" stroke-width="2"/>'
          '<path d="M184 170q22-4 40 16" fill="none" stroke="#183a30" stroke-width="3"/>')
    p.add('<path d="M226 188L330 216" stroke="#e8e8e8" stroke-width="16" stroke-linecap="round" opacity=".9"/>')
    p.arrow('M226 188L326 214', 'ink', 2.4, dash='5 4')
    p.add('<path d="M326 228h56l-6-16h-44z" fill="#6b6b6b" stroke="#183a30" stroke-width="2"/>')
    p.add(flame(354, 212, 0.85))
    p.lines(318, 110, ['small fire in one', 'pan or wastebasket'], 'tiny')
    p.lead((350, 120), (354, 180))
    steps = [('P', 'pull the pin'), ('A', 'aim at the base'), ('S', 'squeeze slowly'), ('S', 'sweep side to side')]
    for i, (letter, label) in enumerate(steps):
        x = 44 + (i % 2) * 226
        y = 262 + (i // 2) * 28
        p.add(f'<circle cx="{x + 13}" cy="{y - 6}" r="12" fill="#183a30"/>'
              f'<text x="{x + 13}" y="{y}" class="small inv" text-anchor="middle">{letter}</text>')
        p.lines(x + 32, y, [label], 'tiny')
    p.lines(44, 324, ['also: others alerted, 911 called, able, safe from smoke'], 'tiny')
    # right: conditions to leave
    p.add('<rect x="530" y="88" width="330" height="150" fill="#f5f2e8" stroke="#183a30" stroke-width="2.2"/>')
    p.add('<path d="M530 88h330v54H530z" fill="#6f6f6f" fill-opacity=".55"/>')
    p.add(flame(600, 236, 1.1), flame(650, 236, 1.3), flame(704, 236, 1.0))
    p.lines(560, 120, ['smoke filling the room'], 'tiny inv')
    p.lines(744, 176, ['fire beyond', 'one object'], 'tiny')
    p.lines(532, 264, ['no clear way out', 'extinguisher empty or fire', 'not out at once'], 'tiny')
    p.band('If unsure, or the fire is not small and contained: alert others, get out, call 911.')
    return p.svg()


def geometry_checks():
    """Measured relationships that the plates state numerically."""
    from math import hypot
    from xml.etree import ElementTree
    ns = '{http://www.w3.org/2000/svg}'
    root = ElementTree.fromstring(z15_p43())
    get = {e.get('id'): e for e in root.iter() if e.get('id')}
    bar = [r for r in get['scale-bar'].iter(ns + 'rect')]
    px_per_ft = sum(float(r.get('width')) for r in bar) / 20.0
    house, gen, garage = get['house'], get['generator'], get['garage']
    wall = float(house.get('x')) + float(house.get('width'))
    gx, gy0 = float(gen.get('x')), float(gen.get('y'))
    gy1 = gy0 + float(gen.get('height'))
    clear_wall_ft = (gx - wall) / px_per_ft
    gar_x = float(garage.get('x')) + float(garage.get('width'))
    gar_y = float(garage.get('y'))
    dy = max(gar_y - gy1, 0)
    clear_garage_ft = hypot(gx - gar_x, dy) / px_per_ft
    return {'Z15-P43': dict(px_per_ft=px_per_ft, generator_to_wall_ft=round(clear_wall_ft, 2),
                            generator_to_garage_ft=round(clear_garage_ft, 2),
                            accepted=clear_wall_ft >= 20 and clear_garage_ft >= 20)}


PLATES = {'Z13-P20': z13_p20, 'Z13-P56': z13_p56, 'Z15-P43': z15_p43, 'Z13-P60': z13_p60, 'Z13-P57': z13_p57}


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
    print(f'{len(PLATES)} batch W2C-B03 plate(s) built; geometry {geometry}')


if __name__ == '__main__':
    main()
