"""Wave 2C batch W2C-B04: severe-weather warning geometry and shelter.

Plates show the spatial or temporal relationship each warning card depends on:
where to shelter inside a large building, who an outdoor siren is designed to
reach, how a watch area differs from a storm-based warning polygon, and how a
flash flood's rise differs from a river flood's. Sources are in the ledger.
Run with --out DIR to preview, --write to refresh the revised SVGs, or --check.
"""
import argparse
from pathlib import Path

from w2c_svg import FLOW, INK, REVERSE, WATER, WATER_EDGE, Plate, check, cross, person

OUT = Path(__file__).resolve().parents[1] / 'foundations/visual/w2c_technical/revised'


def z15_p18():
    p = Plate('Z15-P18', 'Tornado warning shelter inside a store, school or workplace',
              'Floor plan of a large public building. A large open room such as a cafeteria, gymnasium, auditorium '
              'or sales floor and the glass storefront are marked as places to leave. Arrows lead people to the '
              'designated shelter location or an interior room on the lowest floor away from windows. A side panel '
              'shows that vehicles are not safe, so people stay inside rather than go to the parking lot. '
              'Conceptual plan, not to scale.')
    p.add('<rect x="40" y="70" width="480" height="236" fill="#f6f3ea" stroke="#183a30" stroke-width="3"/>')
    p.add('<rect x="40" y="70" width="270" height="236" fill="#ece5d2" stroke="#183a30" stroke-width="2"/>')
    p.add('<path d="M60 306h230" stroke="#7fb4c9" stroke-width="8"/>')
    for x in range(64, 290, 40):
        p.add(f'<path d="M{x} 302v8" stroke="#183a30" stroke-width="1.4"/>')
    p.add(cross(175, 150, 15), cross(175, 288, 11))
    p.lines(64, 104, ['large open room: cafeteria,', 'gym, auditorium, sales floor'], 'tiny')
    p.lines(64, 334, ['glass storefront and windows'], 'tiny')
    # interior shelter core
    p.add('<rect x="350" y="120" width="140" height="136" fill="#dfeadf" stroke="#205b68" stroke-width="3"/>'
          '<path d="M350 188h140M420 120v68" stroke="#205b68" stroke-width="2"/>')
    p.lines(358, 142, ['restrooms'], 'tiny')
    p.lines(358, 214, ['interior hallway'], 'tiny')
    p.add(check(470, 236, 12))
    p.add(person(372, 252, 34, fill='#4d6a78'), person(396, 252, 30, fill='#4d6a78'), person(452, 252, 34, fill='#4d6a78'))
    for y0 in (170, 230):
        p.arrow(f'M230 {y0}C280 {y0} 300 {y0 - 6} 342 {y0 - 10}', 'flow', 3.4)
    p.lines(336, 278, ['designated shelter or', 'lowest interior room'], 'tiny')
    # side panel: stay inside, vehicles are not safe
    p.panel(540, 46, 336, 290, 'bad', '✕ DO NOT GO OUT TO THE CAR')
    p.add('<path d="M572 250h96l-12-30h-72z" fill="#9aa1a5" stroke="#183a30" stroke-width="2"/>'
          '<rect x="562" y="250" width="116" height="26" rx="6" fill="#b9c0c4" stroke="#183a30" stroke-width="2"/>'
          '<circle cx="586" cy="280" r="10" fill="#183a30"/><circle cx="654" cy="280" r="10" fill="#183a30"/>')
    p.add(cross(620, 200, 15))
    p.lines(700, 216, ['vehicles are', 'not safe in a', 'tornado'], 'tiny')
    p.lines(560, 104, ['follow the building drill to', 'the shelter location; stay', 'away from windows'], 'tiny')
    p.band('Stay in the shelter until staff or officials say the warning has passed.')
    return p.svg()


def z15_p22():
    p = Plate('Z15-P22', 'Outdoor sirens versus indoor warning receivers at night',
              'Left: an outdoor warning siren on a pole sends sound to a person outside; sirens are designed only to '
              'alert people who are outdoors. The sound reaching a closed house is not designed to wake people inside. '
              'Inside the bedroom, a battery-backed NOAA Weather Radio on the nightstand and a phone with emergency '
              'alerts turned on sound the warning beside the sleeper. Conceptual, not to scale.')
    p.add('<path d="M30 300H876" stroke="#8a7350" stroke-width="3"/>')
    p.add('<rect x="84" y="110" width="8" height="190" fill="#6b6b6b"/>'
          '<path d="M76 104h24l18-14v40l-18-14H76z" fill="#d6a542" stroke="#183a30" stroke-width="2"/>')
    for r in (40, 70, 100):
        p.add(f'<path d="M{118 + r * .2} {110 - r * .6}a{r} {r} 0 0 1 0 {r * 1.2}" fill="none" stroke="#205b68" stroke-width="2.4"/>')
    p.add(person(250, 300, 76, fill='#4d6a78'), check(250, 196, 12))
    p.lines(40, 326, ['siren: designed only to alert people outside'], 'tiny')
    # house with bedroom
    p.add('<path d="M360 300V170l120-70 120 70v130z" fill="#efe9d8" stroke="#183a30" stroke-width="3"/>'
          '<rect x="390" y="196" width="180" height="104" fill="#f7f4ea" stroke="#183a30" stroke-width="2"/>')
    for r in (40, 64):
        p.add(f'<path d="M{330 - r * .3} {190 - r * .4}a{r} {r} 0 0 1 0 {r * .9}" fill="none" stroke="#8a8f86" stroke-width="2" stroke-dasharray="5 4"/>')
    p.add(cross(346, 158, 12))
    p.lines(316, 98, ['not designed to', 'wake people inside'], 'tiny')
    p.add('<rect x="404" y="262" width="96" height="22" rx="6" fill="#b7c3c6" stroke="#183a30" stroke-width="2"/>')
    p.add(person(418, 262, 70, 'lie', fill='#7a5a43'))
    p.add('<rect x="516" y="252" width="40" height="32" fill="#9b8a6b" stroke="#183a30" stroke-width="1.6"/>'
          '<rect x="520" y="234" width="32" height="18" rx="3" fill="#ffffff" stroke="#183a30" stroke-width="1.8"/>'
          '<rect x="538" y="222" width="10" height="12" rx="2" fill="#183a30"/>')
    for r in (12, 20):
        p.add(f'<path d="M{536 - r} {226 - r * .2}a{r} {r} 0 0 1 0 {-r * .01}" fill="none"/>'
              f'<path d="M{552 + r * .4} {236 - r}a{r} {r} 0 0 1 0 {r * 1.4}" fill="none" stroke="#c0392b" stroke-width="2.4"/>')
    # side panel: indoor alerts
    p.panel(620, 46, 256, 290, 'ok', '✓ INDOOR ALERTS')
    p.add('<rect x="646" y="96" width="70" height="42" rx="6" fill="#ffffff" stroke="#183a30" stroke-width="2.2"/>'
          '<rect x="654" y="104" width="34" height="14" fill="#cfe0e6"/><circle cx="702" cy="124" r="6" fill="#c0392b"/>')
    p.lines(646, 166, ['NOAA Weather Radio', 'with battery backup', 'in the bedroom'], 'tiny')
    p.add('<rect x="650" y="232" width="30" height="52" rx="6" fill="#ffffff" stroke="#183a30" stroke-width="2.2"/>'
          '<rect x="654" y="240" width="22" height="30" fill="#f7e5d9"/>')
    p.lines(692, 252, ['phone emergency', 'alerts left on'], 'tiny')
    p.band('Never rely on a single power-dependent or outdoor-only warning method overnight.')
    return p.svg()


def z15_p02():
    p = Plate('Z15-P02', 'Watch area versus storm-based warning polygon',
              'Map of a block of counties. A watch covers a broad multi-county area where conditions are favorable '
              'for dangerous weather. A storm-based warning is a polygon drawn around the storm\'s threat path, not '
              'county lines, and includes a town ahead of the storm, where the hazard is imminent or occurring. A '
              'side panel pairs each tier with its household action. Conceptual map, not to scale.')
    x0, y0, cw, ch = 40, 70, 80, 64
    p.add(f'<rect x="{x0 + cw}" y="{y0}" width="{cw * 5}" height="{ch * 3}" fill="#f3d98b" fill-opacity=".55" stroke="#b08a2a" stroke-width="3"/>')
    for i in range(6):
        for j in range(4):
            p.add(f'<rect x="{x0 + i * cw}" y="{y0 + j * ch}" width="{cw}" height="{ch}" fill="none" stroke="#9aa59c" stroke-width="1.4"/>')
    p.lines(x0 + cw + 8, y0 + 20, ['WATCH: conditions favorable', 'across many counties'], 'tiny')
    p.add('<polygon points="236,262 286,214 402,152 432,182 318,250 262,290" fill="#c0392b" fill-opacity=".18" stroke="#8b3825" stroke-width="3"/>')
    p.add('<circle cx="250" cy="270" r="18" fill="#6f8f6a"/><circle cx="250" cy="270" r="10" fill="#e0a43a"/><circle cx="250" cy="270" r="4" fill="#c0392b"/>')
    p.arrow('M268 258L322 224', 'ink', 3)
    p.add('<rect x="356" y="182" width="14" height="14" fill="#183a30"/><rect x="374" y="176" width="10" height="20" fill="#183a30"/>')
    p.lines(388, 214, ['town in the', 'warned polygon'], 'tiny')
    p.lines(56, 330 - 8, ['WARNING: polygon around the threat area, not county lines'], 'tiny')
    p.lines(150, 300, ['storm'], 'tiny')
    p.panel(546, 46, 330, 290, 'neutral', 'TIER AND ACTION')
    p.add('<rect x="562" y="80" width="18" height="18" fill="#f3d98b" stroke="#b08a2a" stroke-width="2"/>')
    p.lines(590, 94, ['WATCH: favorable, possible', 'prepare, stage, monitor'], 'tiny')
    p.add('<rect x="562" y="150" width="18" height="18" fill="#c0392b" fill-opacity=".25" stroke="#8b3825" stroke-width="2"/>')
    p.lines(590, 164, ['WARNING: imminent or', 'occurring: act now'], 'tiny')
    p.lines(562, 234, ['ADVISORY: nuisance level,', 'use caution'], 'tiny')
    p.lines(562, 298, ['do not wait to see the funnel,', 'water or flames'], 'tiny')
    p.band('Warning in your area: take the protective action now, without waiting for visual confirmation.')
    return p.svg()


def z15_p23():
    p = Plate('Z15-P23', 'Flash flood versus river flood rise',
              'Two schematic water-level curves. Left: a flash flood rises rapidly over low-lying areas, generally '
              'within about six hours of the cause, and can strike where it is not raining. Right: a river flood '
              'comes as the river overtops its banks after upstream rain or snowmelt; the curve is schematic with no '
              'time scale, and river forecasts give the expected crest. A note covers ice jams and dam or levee '
              'failures, which can release a sudden flood with little warning. Conceptual, not to scale.')
    for x, title in ((24, 'FLASH FLOOD'), (452, 'RIVER OR SNOWMELT FLOOD')):
        p.panel(x, 46, 424 if x == 452 else 414, 290, 'neutral', title)
    def axes(x, y, w, h):
        p.add(f'<path d="M{x} {y}V{y + h}H{x + w}" fill="none" stroke="#183a30" stroke-width="2.2"/>')
        p.lines(x + 8, y + 6, ['water level'], 'tiny')
        p.lines(x + w - 34, y + h + 20, ['time'], 'tiny')
        p.add(f'<path d="M{x} {y + h * .45}H{x + w}" stroke="{REVERSE}" stroke-width="1.6" stroke-dasharray="6 5"/>')
        p.lines(x + 8, y + h * .45 - 8, ['flood level'], 'tiny')
    axes(70, 108, 340, 174)
    for k in range(5):
        p.add(f'<rect x="{84 + k * 10}" y="{280 - (k % 3 + 2) * 12}" width="7" height="{(k % 3 + 2) * 12}" fill="#5f8fa3"/>')
    p.add(f'<path d="M70 268C120 268 132 264 150 250C162 236 168 140 182 126C200 118 240 160 300 222C340 252 380 262 410 264" '
          f'fill="none" stroke="{WATER_EDGE}" stroke-width="4"/>')
    p.lines(194, 120, ['rapid rise, generally within', 'about 6 h of the cause'], 'tiny')
    p.lines(74, 316, ['rain bars: intense local rain'], 'tiny')
    axes(498, 108, 340, 174)
    p.add(f'<path d="M498 270C560 268 600 258 640 236C690 208 720 160 760 148C800 142 820 152 838 162" '
          f'fill="none" stroke="{WATER_EDGE}" stroke-width="4"/>')
    p.add(f'<circle cx="760" cy="148" r="5" fill="{INK}"/>')
    p.lines(654, 132, ['forecast crest'], 'tiny')
    p.lines(506, 316, ['schematic: river overtops banks'], 'tiny')
    p.band('Ice jams and dam or levee failures can release a sudden flood: go to high ground now.')
    return p.svg()


PLATES = {'Z15-P18': z15_p18, 'Z15-P22': z15_p22, 'Z15-P02': z15_p02, 'Z15-P23': z15_p23}


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
    print(f'{len(PLATES)} batch W2C-B04 plate(s) built')


if __name__ == '__main__':
    main()
