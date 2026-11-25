"""Build Wave 2C navigation plates from one angular model.

Z11-R05 was returned in A04 because the compass and the map meridian were drawn
apart and no correction was shown. This plate is generated from a single model
in a fixed ground frame (true north up the page), following the USGS procedure
"How To Get Your Map and Compass To Face the Same Direction" and NOAA NCEI's
declination convention (east positive; true bearing = magnetic + declination):

1. the baseplate edge lies on the map's north-south neat line;
2. the dial is turned so ring north agrees with map north, then corrected for
   declination (subtract a positive declination);
3. map and compass are turned together until the red needle overlays the
   orienting arrow; the map is then oriented to true north;
4. visible landmarks are compared with their map symbols.

The declination angle is exaggerated for legibility and labelled as such. The
geometry is checked numerically from the emitted SVG elements: --check confirms
the retained file equals a fresh build and that the angular relationships hold.
"""
import argparse
import json
from math import atan2, cos, degrees, radians, sin
from pathlib import Path
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'foundations/visual/w2c_technical'
SVG_NS = '{http://www.w3.org/2000/svg}'
BG = '#f2f3e9'
INK = '#183a30'
DECLINATION = 12.0           # exaggerated example east declination, degrees
UNORIENTED = -28.0           # map north bearing before rotation, degrees
LINE_TOL = 0.15              # degrees; line endpoints are emitted at 0.1-0.01 px precision
STYLE = ('<style>text{font:650 19px system-ui,sans-serif;fill:#183a30}.small{font-size:17px}'
         '.tiny{font-size:15px}.map{font-size:13px;fill:#4b5a3b}.warn{fill:#8b3825}.ok{fill:#205b68}'
         '.num{font-size:15px;font-weight:750;fill:#fff}.lead{fill:none;stroke:#365c50;stroke-width:1.6}</style>')


def rot(x, y, deg):
    """Rotate a local point (y up) by a bearing (clockwise degrees) into page offsets (y down)."""
    a = radians(deg)
    return x * cos(a) + y * sin(a), x * sin(a) - y * cos(a)


def pt(cx, cy, x, y, deg):
    dx, dy = rot(x, y, deg)
    return cx + dx, cy + dy


def poly(points):
    return ' '.join(f'{x:.1f},{y:.1f}' for x, y in points)


def line_bearing(x1, y1, x2, y2):
    return degrees(atan2(x2 - x1, -(y2 - y1))) % 360


def compass(cx, cy, heading, dial, needle, ident, k=1.0):
    """Baseplate compass. heading: direction-of-travel bearing; dial: ring north offset
    from the direction of travel (clockwise degrees); needle: magnetic north bearing."""
    g = [f'<g id="{ident}">']

    def P(x, y, deg):
        return pt(cx, cy, x * k, y * k, deg)
    plate = [P(x, y, heading) for x, y in [(-27, -40), (27, -40), (27, 84), (-27, 84)]]
    g.append(f'<polygon points="{poly(plate)}" fill="#e9f1f2" fill-opacity=".9" stroke="{INK}" stroke-width="2.2"/>')
    # direction-of-travel arrow and index mark, fixed to the baseplate
    tail_x, tail_y = P(0, 36, heading)
    tip_x, tip_y = P(0, 78, heading)
    g.append(f'<line id="{ident}-travel" x1="{tail_x:.1f}" y1="{tail_y:.1f}" x2="{tip_x:.1f}" y2="{tip_y:.1f}" '
             f'stroke="{INK}" stroke-width="3" marker-end="url(#a)"/>')
    ix1, iy1 = P(0, 27, heading)
    ix2, iy2 = P(0, 33, heading)
    g.append(f'<line x1="{ix1:.1f}" y1="{iy1:.1f}" x2="{ix2:.1f}" y2="{iy2:.1f}" stroke="{INK}" stroke-width="3"/>')
    # rotating housing: ring ticks, orienting lines and orienting arrow follow the dial
    ring = heading + dial
    g.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{26 * k:.1f}" fill="#ffffff" stroke="{INK}" stroke-width="2.2"/>')
    for tick in range(0, 360, 30):
        a1x, a1y = P(0, 22, ring + tick)
        a2x, a2y = P(0, 26, ring + tick)
        g.append(f'<line x1="{a1x:.1f}" y1="{a1y:.1f}" x2="{a2x:.1f}" y2="{a2y:.1f}" stroke="{INK}" stroke-width="1.4"/>')
    for dx in (-11, 11):
        l1 = P(dx, -19, ring)
        l2 = P(dx, 19, ring)
        g.append(f'<line x1="{l1[0]:.1f}" y1="{l1[1]:.1f}" x2="{l2[0]:.1f}" y2="{l2[1]:.1f}" stroke="#c4472f" '
                 'stroke-width="1" stroke-dasharray="3 2"/>')
    arrow = [P(x, y, ring) for x, y in [(-6, -14), (6, -14), (6, 9), (10, 9), (0, 21), (-10, 9), (-6, 9)]]
    g.append(f'<polygon id="{ident}-orienting" data-bearing="{ring % 360:.3f}" points="{poly(arrow)}" '
             'fill="none" stroke="#c4472f" stroke-width="2"/>')
    nx, ny = P(0, 21, ring)
    g.append(f'<text x="{nx:.1f}" y="{ny + 4:.1f}" class="tiny" text-anchor="middle" font-size="{11 * k:.0f}" '
             f'transform="rotate({ring:.1f} {nx:.1f} {ny:.1f})" fill="#183a30">N</text>')
    # magnetic needle points to magnetic north whatever the baseplate does
    north = [P(x, y, needle) for x, y in [(-4.5, 0), (0, 22), (4.5, 0)]]
    south = [P(x, y, needle) for x, y in [(-4.5, 0), (0, -22), (4.5, 0)]]
    g.append(f'<polygon points="{poly(south)}" fill="#ffffff" stroke="{INK}" stroke-width="1.4"/>')
    g.append(f'<polygon id="{ident}-needle" data-bearing="{needle % 360:.3f}" points="{poly(north)}" '
             f'fill="#c4472f" stroke="{INK}" stroke-width="1.4"/>')
    g.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{2.6 * k:.1f}" fill="{INK}"/>')
    g.append('</g>')
    return ''.join(g)


def topo_map(cx, cy, heading, ident, w=236, h=176, features=True, you=(34, -62), hill=(-2, 40), lake=(74, 32)):
    """Map sheet rotated so map north lies on ``heading``; returns markup and named points."""
    corners = [pt(cx, cy, x, y, heading) for x, y in [(-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2)]]
    g = [f'<g id="{ident}">', f'<polygon points="{poly(corners)}" fill="#efe9d5" stroke="#5d653e" stroke-width="2.4"/>']
    a = pt(cx, cy, -w / 2, -h / 2, heading)
    b = pt(cx, cy, -w / 2, h / 2, heading)
    g.append(f'<line id="{ident}-neatline" x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" '
             'stroke="#5d653e" stroke-width="4.5"/>')
    sx, sy = pt(cx, cy, w / 2 - 22, h / 2 - 22, heading)
    g.append(f'<text x="{sx:.1f}" y="{sy + 5:.1f}" class="map" text-anchor="middle" '
             f'transform="rotate({heading:.1f} {sx:.1f} {sy:.1f})">N ★</text>')
    for k, (y0, amp) in enumerate([(-58, 9), (-20, 7), (62, 8)]):
        wav = [pt(cx, cy, x, y0 + amp * ((x / 37.0) % 2 - 1) ** 2 * (1 if k % 2 else -1), heading)
               for x in range(int(-w / 2) + 14, int(w / 2) - 10, 12)]
        g.append(f'<polyline points="{poly(wav)}" fill="none" stroke="#c8b98f" stroke-width="1.3"/>')
    points = {}
    if features:
        lake_shape = [(-30, 8), (-4, 20), (18, 10), (22, -10), (4, -20), (-18, -14)]
        lake_pts = [pt(cx, cy, lake[0] + x, lake[1] + y, heading) for x, y in lake_shape]
        g.append(f'<polygon points="{poly(lake_pts)}" fill="#9cc3cf" stroke="#3d7186" stroke-width="1.6"/>')
        for r in (18, 11, 5):
            hx, hy = pt(cx, cy, hill[0], hill[1], heading)
            g.append(f'<ellipse cx="{hx:.1f}" cy="{hy:.1f}" rx="{r * 1.35:.1f}" ry="{r:.1f}" fill="none" '
                     f'stroke="#9e8755" stroke-width="1.5" transform="rotate({heading:.1f} {hx:.1f} {hy:.1f})"/>')
        points['lake'] = pt(cx, cy, lake[0], lake[1], heading)
        points['hill'] = pt(cx, cy, hill[0], hill[1], heading)
        points['you'] = pt(cx, cy, you[0], you[1], heading)
        yx, yy = points['you']
        g.append(f'<circle cx="{yx:.1f}" cy="{yy:.1f}" r="6" fill="#ffffff" stroke="{INK}" stroke-width="2.4"/>')
    g.append('</g>')
    return ''.join(g), points


def north_key(x, y, ident):
    tx, ty = x, y - 54
    mx, my = pt(x, y, 0, 54, DECLINATION)
    ax, ay = pt(x, y, 0, 30, 0)
    bx, by = pt(x, y, 0, 30, DECLINATION)
    return (f'<g id="{ident}"><line id="{ident}-true" x1="{x}" y1="{y}" x2="{tx}" y2="{ty}" stroke="{INK}" stroke-width="2.6"/>'
            f'<text x="{tx - 6}" y="{ty - 6}" class="tiny" text-anchor="end">true N ★</text>'
            f'<line id="{ident}-magnetic" x1="{x}" y1="{y}" x2="{mx:.2f}" y2="{my:.2f}" stroke="#c4472f" stroke-width="2.6" '
            f'stroke-dasharray="6 3"/><text x="{mx + 6:.1f}" y="{my - 2:.1f}" class="tiny" fill="#a53a24">MN</text>'
            f'<path d="M{ax:.1f} {ay:.1f}A30 30 0 0 1 {bx:.1f} {by:.1f}" fill="none" stroke="{INK}" stroke-width="1.5"/></g>')


def z11_r05_svg():
    K = 1.62
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 395" role="img" aria-labelledby="title desc">',
        '<title id="title">Orient a map to true north with a baseplate compass</title>',
        '<desc id="desc">Plan view with true north up the page in both panels. Panel 1: the map is turned away from '
        'true north. The baseplate edge lies on the map north-south neat line, the dial is set from map north '
        'with the declination correction applied, and the red needle is not yet inside the orienting arrow. Panel 2: '
        'map and compass have been turned together until the red needle overlays the orienting arrow; map north now '
        'points to true north, and sight lines from your position through the hill and lake symbols reach the real '
        'hill and lake. Magnetic north is shown east of true north with the angle exaggerated; use the current local '
        'declination. Conceptual drawing, not to scale.</desc>',
        '<defs><marker id="a" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="4" markerHeight="4" orient="auto">'
        '<path d="M0 0L10 5L0 10Z" fill="#183a30"/></marker>'
        '<clipPath id="clip-setup"><rect x="26" y="80" width="420" height="258"/></clipPath>'
        '<clipPath id="clip-oriented"><rect x="458" y="80" width="418" height="258"/></clipPath></defs>',
        STYLE,
        f'<rect x="1" y="1" width="898" height="393" rx="12" fill="{BG}" stroke="#789481" stroke-width="2"/>',
        '<text x="24" y="32" class="small">Z11-R05 · TECHNICAL REVIEW · NOT TO SCALE</text>',
        '<path d="M452 70V336" stroke="#a7b9ab" stroke-width="1.5" stroke-dasharray="5 6"/>',
    ]
    # panel 1: set up on an unoriented map
    m1x, m1y = 268, 224
    map1, _ = topo_map(m1x, m1y, UNORIENTED, 'map-before', w=320, h=250, features=False)
    c1 = pt(m1x, m1y, -160 + 27 * K, 8, UNORIENTED)
    parts += [
        '<g id="panel-setup"><text x="36" y="66">1 · SET UP ON THE MAP</text>',
        f'<g clip-path="url(#clip-setup)">{map1}</g>',
        compass(c1[0], c1[1], UNORIENTED, DECLINATION, DECLINATION, 'compass-before', k=K),
        north_key(414, 152, 'key-before'),
        '<text x="36" y="98" class="small">Edge on a north-south</text>',
        '<text x="36" y="121" class="small">neat line</text>',
        f'<path class="lead" d="M{c1[0] - 36:.0f} {c1[1] - 70:.0f}L84 126"/>',
        f'<path class="lead" d="M{c1[0] + 46:.0f} {c1[1] - 2:.0f}L286 194"/>',
        '<text x="290" y="198" class="small">Dial: ring N to</text>',
        '<text x="290" y="221" class="small">map N, minus a</text>',
        '<text x="290" y="244" class="small">positive declination</text>',
        '<text x="290" y="289" class="small warn">Needle not yet</text>',
        '<text x="290" y="312" class="small warn">in the arrow</text>',
        '</g>',
    ]
    # panel 2: map and compass turned together until the needle overlays the arrow
    m2x, m2y = 590, 214
    map2, pts2 = topo_map(m2x, m2y, 0.0, 'map-after', w=240, h=210, you=(0, -86), hill=(70, -48), lake=(100, 4))
    c2 = pt(m2x, m2y, -120 + 27 * K, -30, 0.0)
    yx, yy = pts2['you']
    hx, hy = pts2['hill']
    lx, ly = pts2['lake']
    real_hill = (yx + (hx - yx) * 2.4, yy + (hy - yy) * 2.4)
    real_lake = (yx + (lx - yx) * 1.8, yy + (ly - yy) * 1.8)
    parts += [
        '<g id="panel-oriented"><text x="468" y="66">2 · TURN BOTH TOGETHER</text>',
        f'<g clip-path="url(#clip-oriented)">{map2}</g>',
        compass(c2[0], c2[1], 0.0, DECLINATION, DECLINATION, 'compass-after', k=K),
        f'<line id="sight-hill" x1="{yx:.1f}" y1="{yy:.1f}" x2="{real_hill[0]:.1f}" y2="{real_hill[1]:.1f}" '
        'stroke="#205b68" stroke-width="2.2" stroke-dasharray="7 5"/>',
        f'<line id="sight-lake" x1="{yx:.1f}" y1="{yy:.1f}" x2="{real_lake[0]:.1f}" y2="{real_lake[1]:.1f}" '
        'stroke="#205b68" stroke-width="2.2" stroke-dasharray="7 5"/>',
        f'<path d="M{real_hill[0] - 30:.1f} {real_hill[1] + 9:.1f}L{real_hill[0]:.1f} {real_hill[1] - 15:.1f}'
        f'L{real_hill[0] + 30:.1f} {real_hill[1] + 9:.1f}Z" fill="#cdbf98" stroke="#7d6b45" stroke-width="2"/>',
        f'<ellipse cx="{real_lake[0] + 6:.1f}" cy="{real_lake[1]:.1f}" rx="34" ry="13" fill="#9cc3cf" stroke="#3d7186" stroke-width="2"/>',
        f'<text x="{real_hill[0] + 36:.0f}" y="{real_hill[1] + 6:.0f}" class="tiny">hill</text>',
        f'<text x="{real_lake[0] + 44:.0f}" y="{real_lake[1] + 5:.0f}" class="tiny">lake</text>',
        north_key(852, 326, 'key-after'),
        f'<path class="lead" d="M{c2[0] + 34:.0f} {c2[1] - 28:.0f}L{c2[0] + 62:.0f} 98"/>',
        f'<text x="{c2[0] + 48:.0f}" y="92" class="small ok">Red needle over arrow</text>',
        '<text x="468" y="337" class="small">Map N on true N. Check two landmarks.</text>',
        '</g>',
        '<text x="446" y="176" class="tiny" text-anchor="end">MN angle exaggerated</text>',
        '<rect x="24" y="345" width="852" height="32" rx="4" fill="#f7e5d9"/>',
        '<text x="37" y="367" class="small">Stand clear of metal. If the needle disagrees with obvious terrain, stop and re-check.</text>',
        '</svg>',
    ]
    return '\n'.join(parts) + '\n'


def bearing_of(root, ident):
    node = root.find(f".//*[@id='{ident}']")
    return float(node.get('data-bearing'))


def line_dir(root, ident):
    node = root.find(f".//*[@id='{ident}']")
    return line_bearing(*(float(node.get(k)) for k in ('x1', 'y1', 'x2', 'y2')))


def angle_diff(a, b):
    return abs((a - b + 180) % 360 - 180)


def z11_r05_checks(svg):
    root = ElementTree.fromstring(svg)
    checks = {}
    for phase in ('before', 'after'):
        travel = line_dir(root, f'compass-{phase}-travel')
        neat = line_dir(root, f'map-{phase}-neatline')
        arrow = bearing_of(root, f'compass-{phase}-orienting')
        needle = bearing_of(root, f'compass-{phase}-needle')
        # the neat line is emitted south-west corner to north-west corner, i.e. toward map north
        checks[phase] = dict(
            travel_parallel_to_neat_line=angle_diff(travel, neat) < LINE_TOL,
            orienting_arrow_equals_travel_plus_declination=angle_diff(arrow, travel + DECLINATION) < LINE_TOL,
            needle_on_magnetic_north=angle_diff(needle, DECLINATION) < 0.05,
            needle_in_orienting_arrow=angle_diff(needle, arrow) < 0.05,
            map_north_on_true_north=angle_diff(travel, 0) < LINE_TOL,
        )
    key = {phase: angle_diff(line_dir(root, f'key-{phase}-magnetic'), line_dir(root, f'key-{phase}-true'))
           for phase in ('before', 'after')}
    accepted = (all(v for k, v in checks['after'].items())
                and not checks['before']['needle_in_orienting_arrow']
                and not checks['before']['map_north_on_true_north']
                and all(checks['before'][k] for k in ('travel_parallel_to_neat_line',
                                                      'orienting_arrow_equals_travel_plus_declination',
                                                      'needle_on_magnetic_north'))
                and all(abs(v - DECLINATION) < LINE_TOL for v in key.values()))
    return dict(phases=checks, north_key_declination=key, declination_drawn=DECLINATION,
                declination_labelled='exaggerated example; use current local value', accepted=accepted)


PLATES = {'Z11-R05': (z11_r05_svg, z11_r05_checks)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--out', type=Path)
    args = parser.parse_args()
    results = {}
    for page, (make, check) in PLATES.items():
        svg = make()
        results[page] = check(svg)
        if not results[page]['accepted']:
            raise SystemExit(f'{page} geometry check failed: {json.dumps(results[page], indent=1)}')
        if args.out:
            args.out.mkdir(parents=True, exist_ok=True)
            (args.out / f'{page}.svg').write_text(svg, encoding='utf-8')
        if args.write:
            (OUT / 'revised' / f'{page}.svg').write_text(svg, encoding='utf-8')
        if args.check and (OUT / 'revised' / f'{page}.svg').read_text(encoding='utf-8') != svg:
            raise SystemExit(f'{page} differs from a fresh geometry-checked build')
    receipt = json.dumps(results, indent=1, sort_keys=True) + '\n'
    if args.write:
        (OUT / 'qa/NAVIGATION_GEOMETRY.json').write_text(receipt, encoding='utf-8')
    if args.check and (OUT / 'qa/NAVIGATION_GEOMETRY.json').read_text(encoding='utf-8') != receipt:
        raise SystemExit('Navigation geometry receipt differs from a fresh build')
    print(f'PASS: {len(results)} navigation plate(s), geometry accepted')


if __name__ == '__main__':
    main()
