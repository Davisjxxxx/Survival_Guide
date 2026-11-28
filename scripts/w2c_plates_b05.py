"""Wave 2C batch W2C-B05: home canning heat and pressure.

Plates show the physical controls behind tested canning processes: what each gauge
type reports, what a pressure or boil interruption does to the process time, why
altitude changes the setting, the limits of atmospheric steam canners, and the
methods USDA does not recommend. Numbers appear only where the cited USDA or NCHFP
section states them. Run with --out DIR, --write or --check (includes geometry).
"""
import argparse
from math import cos, radians, sin
from pathlib import Path

from w2c_svg import FLOW, INK, REVERSE, STEEL, WATER, WATER_EDGE, Plate, check, cross, flame

OUT = Path(__file__).resolve().parents[1] / 'foundations/visual/w2c_technical/revised'
DIAL = dict(cx=200, cy=196, r=96, vmax=20.0, start=-135.0, sweep=270.0)   # value v at bearing start + v*sweep/vmax
GAUGE_READS, TRUE_PRESSURE = 11.0, 9.0


def dial_point(v, r):
    a = radians(DIAL['start'] + v * DIAL['sweep'] / DIAL['vmax'])
    return DIAL['cx'] + r * sin(a), DIAL['cy'] - r * cos(a)


def jar(x, y, w=26, h=40, fill='#d9a441'):
    return (f'<rect x="{x}" y="{y + 6}" width="{w}" height="{h - 6}" rx="5" fill="{fill}" stroke="{INK}" stroke-width="1.6"/>'
            f'<rect x="{x + 3}" y="{y}" width="{w - 6}" height="7" rx="2" fill="#9aa1a5" stroke="{INK}" stroke-width="1.4"/>')


def z14_p55():
    p = Plate('Z14-P55', 'Dial gauge accuracy and weighted gauge settings on a pressure canner',
              'Left: a dial gauge with a 0 to 20 pound scale. An untested gauge reads 11 pounds while the true canner '
              'pressure is 9 pounds; a gauge that reads high causes under-processing. Dial gauges are checked for '
              'accuracy each year before use, adjusted when off by up to 2 pounds and replaced when off by more. '
              'Right: a weighted gauge on the vent pipe rocks or jiggles as the maker describes and needs no accuracy '
              'check; above 1,000 feet the tested table calls for the next heavier weight. Conceptual, not to scale.')
    p.panel(24, 46, 420, 290, 'neutral', 'DIAL GAUGE')
    p.panel(462, 46, 414, 290, 'neutral', 'WEIGHTED GAUGE')
    cx, cy, r = DIAL['cx'], DIAL['cy'], DIAL['r']
    p.add(f'<circle cx="{cx}" cy="{cy}" r="{r + 12}" fill="#e6e8e9" stroke="{INK}" stroke-width="3"/>'
          f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#ffffff" stroke="{INK}" stroke-width="1.6"/>')
    for v in range(0, 21):
        x1, y1 = dial_point(v, r - (14 if v % 5 == 0 else 8))
        x2, y2 = dial_point(v, r - 2)
        p.add(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{INK}" stroke-width="{2.4 if v % 5 == 0 else 1.2}"/>')
        if v % 5 == 0:
            tx, ty = dial_point(v, r - 30)
            p.add(f'<text x="{tx:.1f}" y="{ty + 6:.1f}" class="tiny" text-anchor="middle">{v}</text>')
    tx, ty = dial_point(TRUE_PRESSURE, r - 4)
    bx, by = dial_point(TRUE_PRESSURE, 18)
    p.add(f'<line id="true-pressure" data-value="{TRUE_PRESSURE}" x1="{bx:.2f}" y1="{by:.2f}" x2="{tx:.2f}" y2="{ty:.2f}" '
          f'stroke="{REVERSE}" stroke-width="2.4" stroke-dasharray="6 4"/>')
    nx, ny = dial_point(GAUGE_READS, r - 10)
    p.add(f'<line id="gauge-needle" data-value="{GAUGE_READS}" x1="{cx}" y1="{cy}" x2="{nx:.2f}" y2="{ny:.2f}" stroke="{INK}" stroke-width="4"/>'
          f'<circle cx="{cx}" cy="{cy}" r="7" fill="{INK}"/>')
    p.add(f'<text x="{cx}" y="{cy + 46}" class="tiny" text-anchor="middle">lb</text>')
    p.lines(318, 104, ['reads 11 lb', 'true 9 lb:', 'reads high', '= under-', 'processing'], 'tiny')
    p.lead((314, 120), (226, 140))
    p.lines(44, 318, ['test yearly; adjust if off up to 2 lb; replace if more'], 'tiny')
    # weighted gauge on the vent pipe of a canner lid
    p.add('<path d="M500 280h340" stroke="#9aa1a5" stroke-width="10"/><path d="M500 280q170-46 340 0" fill="#c9cdd0" stroke="#183a30" stroke-width="2.4"/>')
    p.add('<rect x="662" y="222" width="10" height="36" fill="#7c8c95" stroke="#183a30" stroke-width="1.6"/>')
    for k, (lab, w) in enumerate((('15', 62), ('10', 52), ('5', 42))):
        y = 160 + k * 22
        p.add(f'<rect x="{667 - w / 2}" y="{y}" width="{w}" height="14" rx="4" fill="{["#5f6b70", "#77858b", "#9aa8ad"][k]}" stroke="#183a30" stroke-width="1.6"/>'
              f'<text x="{667 + w / 2 + 8}" y="{y + 12}" class="tiny">{lab} lb</text>')
    p.add('<path d="M650 230q-10 7 0 14M684 230q10 7 0 14" fill="none" stroke="#205b68" stroke-width="2.2"/>')
    p.lines(486, 98, ['rocks or jiggles as the maker', 'describes; no accuracy check'], 'tiny')
    p.lines(486, 318, ['above 1,000 ft: next heavier weight'], 'tiny')
    p.lines(748, 236, ['e.g. 5 to 10', 'or 10 to 15 lb'], 'tiny')
    p.band('Cracked face, sticking needle or a gauge more than 2 lb off: replace it before canning.')
    return p.svg()


TIMER = dict(x0=120, full=300, dip=(240, 288))


def z14_p56():
    x0, full = TIMER['x0'], TIMER['full']
    d0, d1 = TIMER['dip']
    p = Plate('Z14-P56', 'A pressure or boil interruption restarts the full process time',
              'Pressure-versus-time trace for a pressure canner. Pressure rises to the target, holds, then dips below '
              'the target for a short time before it is restored. Below the trace, adding the lost minutes at the end '
              'is crossed out; the full process time restarts from the moment target pressure returns. A note applies '
              'the same rule to a boiling-water canner when the boil stops. Conceptual, not to scale.')
    p.add(f'<path d="M{x0 - 30} 80V226H{x0 + 560}" fill="none" stroke="{INK}" stroke-width="2.2"/>')
    p.lines(x0 - 26, 74, ['pressure'], 'tiny')
    p.lines(x0 + 520, 248, ['time'], 'tiny')
    p.add(f'<path d="M{x0 - 30} 120H{x0 + 560}" stroke="{FLOW}" stroke-width="1.8" stroke-dasharray="7 5"/>')
    p.lines(x0 + 470, 112, ['target'], 'tiny')
    p.add(f'<rect x="{d0}" y="120" width="{d1 - d0}" height="106" fill="{REVERSE}" fill-opacity=".14"/>')
    p.add(f'<path d="M{x0 - 30} 222C{x0 - 10} 222 {x0 - 6} 118 {x0} 116L{d0} 116C{d0 + 10} 116 {d0 + 12} 162 {d0 + 24} 162'
          f'C{d1 - 18} 162 {d1 - 10} 116 {d1} 116L{x0 + 560} 116" fill="none" stroke="{INK}" stroke-width="3.4"/>')
    p.lines(d0 - 10, 196, ['below target'], 'tiny warn')
    # timer bars
    p.add(f'<rect id="planned" x="{x0}" y="262" width="{full}" height="14" fill="#9aa8ad"/>')
    p.lines(x0 - 104, 274, ['planned'], 'tiny')
    p.add(f'<rect x="{x0}" y="286" width="{d0 - x0}" height="14" fill="#9aa8ad"/>'
          f'<rect x="{d1}" y="286" width="{full - (d0 - x0)}" height="14" fill="#c9a49a"/>')
    p.add(cross(x0 + full + (d1 - d0) + 24, 293, 10))
    p.lines(x0 - 104, 298, ['add minutes'], 'tiny warn')
    p.add(f'<rect id="restarted" x="{d1}" y="310" width="{full}" height="14" fill="{FLOW}"/>')
    p.add(check(d1 + full + 24, 317, 10))
    p.lines(x0 - 104, 322, ['restart full'], 'tiny ok')
    p.panel(712, 46, 164, 290, 'neutral', 'WATER BATH')
    p.lines(724, 104, ['boil stops?', 'back to a full', 'boil, then time', 'from the start'], 'tiny')
    p.add('<rect x="740" y="210" width="110" height="80" rx="8" fill="#c9cdd0" stroke="#183a30" stroke-width="2"/>'
          f'<rect x="746" y="226" width="98" height="58" fill="{WATER}"/>')
    p.add(flame(778, 304, 0.55), flame(812, 304, 0.55))
    p.band('Uncertain about a batch after an interruption: consult Extension before using it.')
    return p.svg()


def z14_p57():
    p = Plate('Z14-P57', 'Why canning settings change with altitude',
              'Left: the same pot of water boiling at sea level and at a higher elevation; water boils at a lower '
              'temperature as altitude increases, and lower boiling temperatures are less effective at killing '
              'bacteria, so sea-level settings can under-process at 1,000 feet or more. Right: the tested recipe has '
              'separate tables for boiling-water, dial-gauge and weighted-gauge canners; at higher elevation the '
              'boiling-water time increases, the dial-gauge pressure increases, and the weighted gauge moves to the '
              'next heavier weight. Values are never moved between tables. Conceptual, not to scale.')
    p.add('<path d="M40 300L180 300L300 200L470 150" fill="none" stroke="#8a7350" stroke-width="4"/>'
          '<path d="M40 300L180 300L300 200L470 150L470 330H40Z" fill="#d9caa4" fill-opacity=".55"/>')
    for (x, y, h, lab) in ((110, 300, 70, 'sea level'), (400, 170, 50, 'higher elevation')):
        p.add(f'<rect x="{x - 26}" y="{y - 34}" width="52" height="30" rx="5" fill="#c9cdd0" stroke="{INK}" stroke-width="2"/>'
              f'<rect x="{x - 22}" y="{y - 28}" width="44" height="22" fill="{WATER}"/>')
        p.add(f'<rect x="{x + 34}" y="{y - 34 - h}" width="10" height="{h + 26}" rx="5" fill="#ffffff" stroke="{INK}" stroke-width="1.8"/>'
              f'<rect x="{x + 37}" y="{y - 34 - h * (0.92 if x == 110 else 0.62)}" width="4" height="{h * (0.92 if x == 110 else 0.62) + 22}" fill="#c0392b"/>')
        p.lines(x - 34, y + 22 if x == 110 else y + 30, [lab], 'tiny')
    p.lines(56, 104, ['water boils at a lower temperature', 'as altitude increases: sea-level', 'settings can under-process'], 'tiny')
    p.panel(498, 46, 378, 290, 'neutral', 'USE YOUR CANNER\'S TABLE')
    p.add('<circle cx="530" cy="112" r="16" fill="#ffffff" stroke="#183a30" stroke-width="2"/><path d="M530 112V100M530 112h9" stroke="#183a30" stroke-width="2"/>')
    p.lines(556, 108, ['boiling water: longer time'], 'tiny')
    p.add('<circle cx="530" cy="168" r="16" fill="#ffffff" stroke="#183a30" stroke-width="2"/><path d="M530 168l9-8" stroke="#183a30" stroke-width="2.4"/>')
    p.lines(556, 164, ['dial gauge: higher pressure'], 'tiny')
    p.add('<rect x="516" y="214" width="28" height="10" rx="3" fill="#77858b" stroke="#183a30" stroke-width="1.4"/>'
          '<rect x="512" y="224" width="36" height="10" rx="3" fill="#5f6b70" stroke="#183a30" stroke-width="1.4"/>')
    p.lines(556, 222, ['weighted gauge: next', 'heavier weight'], 'tiny')
    p.add(cross(530, 292, 11))
    p.lines(556, 290, ['never move a value between', 'dial and weighted tables'], 'tiny')
    p.band('Unknown elevation or no altitude table: look both up before lighting the burner.')
    return p.svg()


def z14_p53():
    p = Plate('Z14-P53', 'Atmospheric steam canner limits',
              'Cross-section of an atmospheric steam canner: a shallow base holds water under a rack of jars, steam '
              'fills the dome and air is vented out before timing begins. Limits: acid or properly acidified foods '
              'with pH 4.6 or below, a total process of 45 minutes or less including altitude adjustment, and no '
              'opening to add water during processing. It is not a pressure canner and is not used for low-acid '
              'foods. Conceptual, not to scale.')
    p.add('<rect x="120" y="246" width="260" height="44" rx="10" fill="#c9cdd0" stroke="#183a30" stroke-width="2.6"/>'
          f'<rect x="128" y="262" width="244" height="22" fill="{WATER}"/>'
          '<path d="M134 246h232" stroke="#6b6b6b" stroke-width="4"/>')
    for k in range(4):
        p.add(jar(150 + k * 52, 202, 30, 44, '#c4562f'))
    p.add('<path d="M128 246V150q122-96 244 0v96" fill="#ffffff" fill-opacity=".35" stroke="#183a30" stroke-width="2.6"/>'
          '<rect x="236" y="74" width="28" height="14" rx="4" fill="#9aa1a5" stroke="#183a30" stroke-width="1.8"/>')
    for x in (180, 250, 320):
        p.arrow(f'M{x} 240C{x - 10} 210 {x + 12} 180 {x} 150', 'air', 2.4, dash='4 4')
    p.add('<circle cx="340" cy="126" r="5" fill="#183a30"/><circle cx="160" cy="126" r="5" fill="#183a30"/>')
    p.arrow('M154 122L110 112', 'air', 2.4)
    p.lines(40, 84, ['air vented out', 'before timing'], 'tiny')
    p.lines(40, 320, ['shallow base: do not open to add water'], 'tiny')
    p.panel(478, 46, 398, 290, 'neutral', 'ONLY WITHIN THE TESTED LIMITS')
    p.add(check(500, 106, 11))
    p.lines(520, 110, ['acid or acidified foods,', 'pH 4.6 or below, tested recipe'], 'tiny')
    p.add(check(500, 176, 11))
    p.lines(520, 180, ['45 minutes or less in total,', 'including altitude adjustment'], 'tiny')
    p.add(cross(500, 246, 11))
    p.lines(520, 250, ['not a pressure canner:', 'no low-acid foods'], 'tiny')
    p.band('Recipe, adjusted time or equipment outside these limits: use the correct tested method.')
    return p.svg()


def z14_p48():
    p = Plate('Z14-P48', 'Canning methods USDA does not recommend, and the tested equipment',
              'Left: jars processed in a conventional oven, open-kettle filling with jars turned upside down, a '
              'microwave oven, a dishwasher and a paraffin wax seal are each crossed out; USDA does not recommend them '
              'because they do not prevent all risks of spoilage. Right: a boiling-water canner with water over the '
              'jar tops and a pressure canner holding at least four quart jars, used with a tested recipe. '
              'Conceptual, not to scale.')
    p.panel(24, 46, 470, 290, 'bad', '✕ NOT RECOMMENDED')
    p.panel(512, 46, 364, 290, 'ok', '✓ TESTED EQUIPMENT')
    # oven
    p.add('<rect x="44" y="90" width="96" height="76" rx="5" fill="#d9dcdc" stroke="#183a30" stroke-width="2"/>'
          '<rect x="54" y="102" width="76" height="52" fill="#3b3b3b"/>')
    p.add(jar(66, 112, 18, 30), jar(96, 112, 18, 30))
    p.lines(50, 186, ['oven'], 'tiny')
    # open kettle and inverted jar
    p.add('<path d="M172 120h70l-6 44h-58z" fill="#9aa1a5" stroke="#183a30" stroke-width="2"/>'
          '<g transform="rotate(180 270 142)">' + jar(258, 122, 24, 40) + '</g>')
    p.lines(170, 186, ['open kettle, jar', 'turned upside down'], 'tiny')
    # microwave
    p.add('<rect x="328" y="94" width="104" height="66" rx="6" fill="#e2e4e4" stroke="#183a30" stroke-width="2"/>'
          '<rect x="338" y="104" width="62" height="46" fill="#4a4f52"/><circle cx="416" cy="114" r="4" fill="#183a30"/>')
    p.lines(330, 186, ['microwave'], 'tiny')
    # dishwasher
    p.add('<rect x="70" y="216" width="92" height="94" rx="6" fill="#d9dcdc" stroke="#183a30" stroke-width="2"/>'
          '<path d="M70 236h92" stroke="#183a30" stroke-width="2"/>')
    p.lines(176, 266, ['dishwasher'], 'tiny')
    # paraffin seal
    p.add('<rect x="300" y="236" width="40" height="56" rx="6" fill="#b84a6b" stroke="#183a30" stroke-width="2"/>'
          '<rect x="300" y="236" width="40" height="10" fill="#f2efe1" stroke="#183a30" stroke-width="1.6"/>')
    p.lines(354, 266, ['paraffin seal'], 'tiny')
    for x, y in ((126, 92), (226, 116), (418, 96), (146, 222), (334, 232)):
        p.add(cross(x, y, 11))
    p.lines(44, 326, ['do not prevent all risks of spoilage'], 'tiny warn')
    # tested equipment
    p.add('<rect x="540" y="150" width="140" height="96" rx="10" fill="#c9cdd0" stroke="#183a30" stroke-width="2.4"/>'
          f'<rect x="546" y="162" width="128" height="78" fill="{WATER}"/>')
    for k in range(3):
        p.add(jar(556 + k * 40, 188, 28, 44))
    p.add('<path d="M546 172h128" stroke="#3d7186" stroke-width="2" stroke-dasharray="5 4"/>')
    p.lines(536, 100, ['boiling-water canner,', 'water over jar tops'], 'tiny')
    p.add('<path d="M712 156q72-40 144 0v92h-144z" fill="#c9cdd0" stroke="#183a30" stroke-width="2.4"/>'
          '<rect x="778" y="128" width="10" height="20" fill="#7c8c95"/>')
    for k in range(4):
        p.add(jar(720 + k * 34, 196, 28, 48))
    p.lines(708, 100, ['pressure canner that', 'holds 4 quart jars'], 'tiny')
    p.lines(536, 290, ['with a tested recipe for the', 'food, jar size and altitude'], 'tiny')
    p.band('Any recipe that calls for these methods: reject it and use a tested method.')
    return p.svg()


def geometry_checks():
    from math import atan2, degrees, hypot
    from xml.etree import ElementTree
    out = {}
    root = ElementTree.fromstring(z14_p55())
    get = {e.get('id'): e for e in root.iter() if e.get('id')}

    def value_of(el, fx, fy):
        x1, y1, x2, y2 = (float(el.get(k)) for k in ('x1', 'y1', 'x2', 'y2'))
        bearing = degrees(atan2(x2 - fx, -(y2 - fy)))
        return (bearing - DIAL['start']) * DIAL['vmax'] / DIAL['sweep']
    needle = value_of(get['gauge-needle'], DIAL['cx'], DIAL['cy'])
    true = value_of(get['true-pressure'], DIAL['cx'], DIAL['cy'])
    out['Z14-P55'] = dict(needle_reads=round(needle, 2), true_marker=round(true, 2),
                          accepted=abs(needle - GAUGE_READS) < 0.05 and abs(true - TRUE_PRESSURE) < 0.05)
    root = ElementTree.fromstring(z14_p56())
    get = {e.get('id'): e for e in root.iter() if e.get('id')}
    planned, restarted = float(get['planned'].get('width')), float(get['restarted'].get('width'))
    starts_at_restore = float(get['restarted'].get('x')) == TIMER['dip'][1]
    out['Z14-P56'] = dict(planned=planned, restarted=restarted, restarts_when_pressure_returns=starts_at_restore,
                          accepted=planned == restarted and starts_at_restore)
    return out


PLATES = {'Z14-P55': z14_p55, 'Z14-P56': z14_p56, 'Z14-P57': z14_p57, 'Z14-P53': z14_p53, 'Z14-P48': z14_p48}


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
    print(f'{len(PLATES)} batch W2C-B05 plate(s) built; geometry {geometry}')


if __name__ == '__main__':
    main()
