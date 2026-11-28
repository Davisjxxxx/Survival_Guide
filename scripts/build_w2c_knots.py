"""Build the Wave 2C knot plates from topology-checked rope models.

Z09-P14 (bowline) and Z09-P15 (figure-eight stopper and figure-eight loop) were
returned in A04 because the drawn crossings did not establish the knots. Each
rope here is a depth model whose projected crossings are verified against the
tying sequence in the card and in FM 3-97.61 (Aug 2002) sections 4-12, 4-14 and
4-20, and against an independent standard-bowline crossing diagram:

* bowline core: seven crossings in the reference passage order
  (O1 U2 U3 O4 O5 U6 O2 U7 U5 O6 U1 O7 O3 U4), tail end inside the fixed loop;
* overhand stopper on the bowline tail: three alternating crossings, determinant 3;
* figure-eight stopper: four alternating crossings, determinant 5 (the only knot
  with crossing number <= 4 and determinant 5 is the figure-eight knot);
* figure-eight loop: a doubled figure-eight core (determinant 5) whose two
  parallel strands never cross each other.

Run with --write to refresh the SVGs and the topology receipt, or with --check
to confirm the retained files match a fresh build.
"""
import argparse
import json
from math import atan2, cos, hypot, sin
from pathlib import Path

from w2c_rope import Rope

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'foundations/visual/w2c_technical'

BG = '#f2f3e9'
INK = '#183a30'
WARN = '#8b3825'
STYLE = ('<style>text{font:650 19px system-ui,sans-serif;fill:#183a30}.small{font-size:17px}'
         '.tiny{font-size:15px}.warn{fill:#8b3825}.ok{fill:#205b68}.num{font-size:15px;font-weight:750;fill:#fff}'
         '.lead{fill:none;stroke:#365c50;stroke-width:1.6}</style>')
BOWLINE_EXPECTED = 'O1 U2 U3 O4 O5 U6 O2 U7 U5 O6 U1 O7 O3 U4'
STOPPER_EXPECTED = 'U8 O9 U10 O8 U9 O10'


def place(points, unit, ox, oy):
    return [(ox + x * unit, oy - y * unit, z) for x, y, z in points]


# ------------------------------------------------------------------ bowline
BOWLINE_CORE = [
    (0, 5.3, 0), (0, 4.95, 0.3),
    (0, 4.45, 0.8),            # X1 standing part over the collar
    (0.02, 3.7, 0),
    (0.0, 2.95, -1),           # loop crossing: standing part under returning side
    (0.05, 2.2, -0.4),
    (0.12, 1.45, -1),          # standing part under the down pass
    (-0.12, 0.65, 0), (0.4, -0.45, 0.5), (1.2, -0.92, 0.8),
    (2.05, -0.9, 1.0),         # rim over the down pass (tail exit)
    (3.0, -0.45, 0.7),
    (3.62, 0.85, 1.0),         # rim over the up pass (entry)
    (3.4, 2.2, 0.4), (2.85, 2.85, -0.2),
    (2.15, 3.12, -1.0),        # rim under the up pass (exit)
    (1.1, 3.2, 0.2),
    (0.0, 2.95, 1.0),          # returning side over the standing part
    (-0.6, 2.62, 0.2),
    (-1.2, 2.15, -1.0),        # returning side under the down pass
    (-1.8, 1.35, -0.2), (-2.4, 0.1, 0), (-2.65, -1.25, 0), (-2.2, -2.65, 0), (-0.65, -3.65, 0),
    (1.6, -4.0, 0), (3.75, -3.75, 0), (5.15, -2.7, 0), (5.6, -1.2, 0), (5.35, -0.05, 0),
    (4.7, 0.5, -0.4),
    (3.62, 0.85, -1.0),        # up pass enters under the rim
    (2.85, 1.95, -0.1),
    (2.15, 3.12, 1.0),         # up pass leaves over the rim
    (1.5, 3.98, 0.4), (0.72, 4.48, -0.4),
    (0, 4.45, -1.0),           # collar behind the standing part
    (-0.9, 4.4, -0.4), (-1.62, 3.95, 0), (-1.85, 3.15, 0.4), (-1.62, 2.55, 0.8),
    (-1.2, 2.15, 1.0),         # down pass over the returning side
    (-0.55, 1.75, 0.6),
    (0.12, 1.45, 1.0),         # down pass over the standing part
    (1.1, 0.75, 0.3),
    (2.05, -0.9, -1.0),        # down pass leaves under the rim
    (2.2, -1.45, 0),
]
STOPPER_SHAPE = [
    (0.0, 0.2, 0),
    (0.0, -0.25, -1.0),        # descending tail under
    (0.08, -0.78, 0.2),
    (0.32, -0.97, 1.0),        # loop rim over (end enters beneath)
    (0.78, -1.0, 0.3), (1.02, -0.58, -0.3),
    (0.95, -0.2, -1.0),        # loop rim under (end leaves on top)
    (0.62, 0.18, 0), (0.25, 0.12, 0.6),
    (0.0, -0.25, 1.0),         # loop closes over the descending tail
    (-0.45, -0.68, 0.3), (-0.32, -1.3, -0.3),
    (0.32, -0.97, -1.0),       # end passes under the rim
    (0.62, -0.55, 0),
    (0.95, -0.2, 1.0),         # end passes over the rim
    (1.32, -0.06, 0.3), (1.5, -0.55, 0), (1.32, -1.2, 0),
]
SHORT_TAIL_CORE = BOWLINE_CORE[:-1] + [(2.12, -1.18, 0)]


def bowline_points(stopper=True, scale_stopper=1.3, origin=(2.3, -1.5)):
    if not stopper:
        return list(SHORT_TAIL_CORE)
    ox, oy = origin
    return BOWLINE_CORE + [(ox + x * scale_stopper, oy + y * scale_stopper, z) for x, y, z in STOPPER_SHAPE]


def bowline_ropes():
    main = Rope(place(bowline_points(), 30, 150, 204), name='bowline')
    alone = Rope(place([(2.3, -0.2, 0)] + [(2.3 + 1.3 * x, -1.5 + 1.3 * y, z) for x, y, z in STOPPER_SHAPE]
                       + [(4.6, -4.4, 0)], 30, 150, 204), name='overhand stopper (isolated)')
    short = Rope(place(bowline_points(stopper=False), 14.5, 712, 158), name='short-tail failure view')
    return main, alone, short


def marker(n, x, y, fill=INK):
    return (f'<circle cx="{x:.0f}" cy="{y:.0f}" r="12" fill="{fill}"/>'
            f'<text x="{x:.0f}" y="{y + 5:.0f}" class="num" text-anchor="middle">{n}</text>')


def arrow_along(rope, s, length=26, offset=14, side=1, color=INK, ident='a'):
    x, y, _ = rope.at(s)
    tx, ty = rope.tangent(s)
    nx, ny = -ty * side, tx * side
    x0, y0 = x + nx * offset - tx * length / 2, y + ny * offset - ty * length / 2
    x1, y1 = x + nx * offset + tx * length / 2, y + ny * offset + ty * length / 2
    return (f'<path d="M{x0:.1f} {y0:.1f}L{x1:.1f} {y1:.1f}" stroke="{color}" stroke-width="3" '
            f'fill="none" marker-end="url(#{ident})"/>')


def crossing(rope, ident):
    return next(c for c in rope.crossings if c['id'] == ident)


def label_point(rope, s, offset, side=1):
    x, y, _ = rope.at(s)
    tx, ty = rope.tangent(s)
    return x - ty * side * offset, y + tx * side * offset


def bowline_svg():
    main, alone, short = bowline_ropes()
    collar, loop_x, down_cross, rim_exit, up_entry, up_exit = (crossing(main, i) for i in (1, 2, 3, 4, 5, 6))
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 395" role="img" aria-labelledby="title desc">',
        '<title id="title">Bowline formed, backed with a stopper and checked</title>',
        '<desc id="desc">Loose bowline in utility cord. The standing part runs up to the load. A small overhand loop '
        'is formed in the standing part with the working side on top. The working end comes up through that loop, '
        'passes behind the standing part and goes back down through the loop beside its first pass, so the tail '
        'finishes inside the fixed loop, where an overhand stopper is tied with tail to spare. A smaller view shows '
        'the failure to avoid: a short tail with no stopper, which can work loose. Utility loads only; not for '
        'climbing or life-safety use. Conceptual drawing, not to scale.</desc>',
        '<defs><marker id="a" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="4.2" markerHeight="4.2" orient="auto">'
        '<path d="M0 0L10 5L0 10Z" fill="#183a30"/></marker></defs>',
        STYLE,
        f'<rect x="1" y="1" width="898" height="393" rx="12" fill="{BG}" stroke="#789481" stroke-width="2"/>',
        '<text x="24" y="32" class="small">Z09-P14 · TECHNICAL REVIEW · NOT TO SCALE</text>',
        '<g id="bowline-artwork">',
        main.svg(width=10, ident='bowline-rope', halo=BG, halo_width=3.4),
        # direction of travel for the working end: up pass, collar, down pass
        arrow_along(main, (up_entry['s2'] + up_exit['s2']) / 2, side=1, offset=17),
        arrow_along(main, collar['s2'] + 42, side=-1, offset=16),
        arrow_along(main, (down_cross['s2'] + rim_exit['s2']) / 2 + 10, side=1, offset=17),
    ]
    top_x, top_y, _ = main.at(0)
    parts.append(f'<path d="M{top_x:.0f} {top_y - 3:.0f}V46" stroke="{INK}" stroke-width="2.4" marker-end="url(#a)"/>')
    parts.append(f'<text x="{top_x + 14:.0f}" y="58" class="tiny">to load</text>')
    spots = [
        (1, (loop_x['x'] + 26, loop_x['y'] + 14)),
        (2, (up_entry['x'] + 31, up_entry['y'] - 38)),
        (3, label_point(main, collar['s2'] + 70, 24, side=1)),
        (4, (rim_exit['x'] - 42, rim_exit['y'] + 5)),
        (5, label_point(main, main.length - 95, 30, side=1)),
    ]
    for n, (x, y) in spots:
        parts.append(marker(n, x, y))
    parts.append('</g>')
    legend = [
        (1, 'Loop: working side on top'),
        (2, 'Up through the loop'),
        (3, 'Behind the standing part'),
        (4, 'Back down beside pass 2'),
        (5, 'Tail inside loop, stopper'),
        (None, 'tied with tail to spare'),
    ]
    parts.append('<g id="bowline-steps">')
    for i, (n, label) in enumerate(legend):
        y = 96 + i * 40 if n else 96 + (i - 1) * 40 + 22
        if n:
            parts.append(marker(n, 352, y - 6))
        parts.append(f'<text x="372" y="{y:.0f}" class="small">{label}</text>')
    parts.append('</g>')
    parts += [
        '<g id="bowline-failure">',
        '<rect x="612" y="52" width="266" height="282" rx="10" fill="#fbf3ee" stroke="#b9876f" stroke-width="1.6"/>',
        '<text x="630" y="80" class="small warn">✕ AVOID</text>',
        short.svg(width=5.4, outline=1.1, halo='#fbf3ee', halo_width=2.0, ident='bowline-short-tail'),
        '<text x="630" y="292" class="small warn">Short tail, no stopper:</text>',
        '<text x="630" y="316" class="small warn">can work loose</text>',
        '</g>',
        '<rect x="24" y="345" width="852" height="32" rx="4" fill="#f7e5d9"/>',
        '<text x="37" y="367" class="small">Utility loads only. Never use a camp-cord bowline for climbing, rescue or life support.</text>',
        '</svg>',
    ]
    return '\n'.join(parts) + '\n', [main, alone, short]


def bowline_checks(ropes):
    main, alone, short = ropes
    results = {}
    for rope in ropes:
        results[rope.name] = rope.report()
        results[rope.name]['problems'] = rope.check_crossings()
    codes = main.gauss_string().split()
    results['bowline']['core_matches_reference'] = ' '.join(codes[:14]) == BOWLINE_EXPECTED
    results['bowline']['stopper_sequence_alternates'] = ' '.join(codes[14:]) == STOPPER_EXPECTED
    loop_cross, entry = crossing(main, 2), crossing(main, 5)
    end = main.samples[-1]
    results['bowline']['tail_end_inside_fixed_loop'] = main.inside((end[0], end[1]), loop_cross['s2'], entry['s2'])
    results['short-tail failure view']['core_matches_reference'] = short.gauss_string() == BOWLINE_EXPECTED
    results['overhand stopper (isolated)']['is_trefoil'] = (
        len(alone.crossings) == 3 and alone.determinant() == 3)
    return results


# ----------------------------------------------------------- figure-eight
# Core figure-eight path (math axes, y up): standing part enters from the left, a
# loop is formed (working side over), the end wraps behind the standing part and
# is routed through the loop. Verified: four alternating crossings, determinant 5.
FIG8_CORE = [
    (-6, 0, 0), (-4, 0, 0), (-2.6, 0, 0), (-1.2, 0, 0), (0, 0.05, 0),
    (0.8, 0.45, 0.6), (0.95, 1.0, 1.0), (0.75, 1.75, 0.6), (0, 2.1, 0), (-0.75, 1.8, -0.6),
    (-0.95, 1.25, -1.0), (-0.75, 0.6, 0), (-0.5, 0, 1.0),
    (-0.6, -0.9, 0.6), (-1.25, -1.25, 0), (-1.9, -0.8, -0.6), (-1.95, 0, -1.0),
    (-1.75, 0.85, -0.3), (-1.35, 1.25, 0.4), (-0.95, 1.25, 1.0), (0, 1.05, 0),
    (0.95, 1.0, -1.0), (1.8, 0.85, -0.3), (3.0, 0.7, 0), (4.5, 0.7, 0)]
FIG8_EXPECTED = 'O1 U2 O3 U4 O2 U1 O4 U3'


def fig8_stopper_rope(unit=40, ox=228, oy=214):
    # mirrored so the standing part arrives from the right through the grommet
    pts = [(-x, y, z) for x, y, z in FIG8_CORE]
    pts = [(x, y, z) for x, y, z in pts if x > -3.6] + [(-4.6, 1.1, 0)]
    pts = [(4.55, 0, 0)] + pts[1:]
    return Rope(place(pts, unit, ox, oy), name='figure-eight stopper')


def offset_points(points, d):
    """Offset control points by +/-d along their local normals (plate units)."""
    left, right = [], []
    for i, (x, y, z) in enumerate(points):
        ax, ay, _ = points[max(i - 1, 0)]
        bx, by, _ = points[min(i + 1, len(points) - 1)]
        n = hypot(bx - ax, by - ay) or 1
        tx, ty = (bx - ax) / n, (by - ay) / n
        left.append((x - ty * d, y + tx * d, z))
        right.append((x + ty * d, y - tx * d, z))
    return left, right


def fig8_loop_ropes(unit=30, ox=640, oy=226, d=6.4):
    # rotate the core so the doubled standing part enters from below and the bight leaves at the top
    rot = [(-y, x, z) for x, y, z in FIG8_CORE]
    core_math = [(0, -2.75, 0)] + [(x, y, z) for x, y, z in rot if -2.5 < y < 2.2] + [(-0.72, 2.45, 0)]
    core_pts = place(core_math, unit, ox, oy)
    core = Rope(core_pts, name='figure-eight loop core')
    left, right = offset_points(core_pts, d)
    # the bight: leave the knot on one strand, turn, and come back on the other
    (lx, ly, _), (rx, ry, _) = left[-1], right[-1]
    mx, my = (lx + rx) / 2, (ly + ry) / 2
    w, h = 1.55 * unit, 2.05 * unit
    side = 1 if lx > mx else -1
    bight = [(mx + (lx - mx) * 1.6, my - 0.35 * unit, 0), (mx + side * w * 0.55, my - 0.95 * unit, 0),
             (mx + side * w * 0.62, my - 1.45 * unit, 0), (mx, my - h, 0), (mx - side * w * 0.62, my - 1.45 * unit, 0),
             (mx - side * w * 0.55, my - 0.95 * unit, 0), (mx + (rx - mx) * 1.6, my - 0.35 * unit, 0)]
    stand = (left[0][0], left[0][1] + 0.62 * unit, 0)
    tail = (right[0][0], right[0][1] + 0.66 * unit, 0)
    doubled = Rope([stand] + left + bight + right[::-1] + [tail], samples_per_segment=40,
                   name='figure-eight loop')
    return core, doubled


def strand_crossings_follow_core(core, doubled, radius):
    """Every doubled-strand crossing sits at a core crossing, four per core crossing."""
    counts = {c['id']: 0 for c in core.crossings}
    stray = 0
    for f in doubled.crossings:
        near = [c for c in core.crossings if hypot(c['x'] - f['x'], c['y'] - f['y']) <= radius]
        if len(near) != 1:
            stray += 1
            continue
        c = near[0]
        agrees = (abs(max(f['z1'], f['z2']) - max(c['z1'], c['z2'])) < 0.5
                  and abs(min(f['z1'], f['z2']) - min(c['z1'], c['z2'])) < 0.5)
        counts[c['id']] += 1 if agrees else 100
    return stray == 0 and all(v == 4 for v in counts.values()), counts, stray


def fig8_svg():
    stopper = fig8_stopper_rope()
    core, loop = fig8_loop_ropes()
    tail_x, tail_y, _ = stopper.at(stopper.length)
    pull_x, pull_y, _ = stopper.at(0)
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 395" role="img" aria-labelledby="title desc">',
        '<title id="title">Figure-eight stopper and figure-eight loop</title>',
        '<desc id="desc">Two separate knots in utility cord. Left: a figure-eight stopper tied in the end of a line '
        'that passes through a tarp grommet; when the line is pulled, the wide knot bears on the grommet, and a tail '
        'extends beyond the knot. Right: a figure-eight loop tied in a doubled line, with the two strands running '
        'side by side through the knot without crossing, a fixed loop above, and the standing part and a tail to '
        'spare below. Not certified life-safety anchors. Conceptual drawing, not to scale.</desc>',
        '<defs><marker id="a" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="4.2" markerHeight="4.2" orient="auto">'
        '<path d="M0 0L10 5L0 10Z" fill="#183a30"/></marker></defs>',
        STYLE,
        f'<rect x="1" y="1" width="898" height="393" rx="12" fill="{BG}" stroke="#789481" stroke-width="2"/>',
        '<text x="24" y="32" class="small">Z09-P15 · TECHNICAL REVIEW · NOT TO SCALE</text>',
        '<g id="stopper-artwork">',
        '<text x="40" y="76">STOPPER AT A LINE END</text>',
        # tarp edge in section with an edge-on grommet ring around the line
        '<rect x="319" y="118" width="11" height="186" rx="3" fill="#c9cdbd" stroke="#6b7b70" stroke-width="1.5"/>',
        '<rect x="314" y="190" width="21" height="11" rx="2" fill="#5d6a66"/>',
        '<rect x="314" y="227" width="21" height="11" rx="2" fill="#5d6a66"/>',
        stopper.svg(width=10, ident='fig8-stopper-rope', halo=BG, halo_width=3.4),
        f'<path d="M{pull_x + 6:.0f} {pull_y:.0f}h46" stroke="{INK}" stroke-width="3" marker-end="url(#a)"/>',
        f'<text x="{pull_x - 4:.0f}" y="{pull_y - 16:.0f}" class="small">pull</text>',
        '<path class="lead" d="M331 146L352 124"/><text x="300" y="114" class="tiny">tarp edge, grommet</text>',
        '<path class="lead" d="M286 266L300 292"/><text x="150" y="314" class="small">wide knot bears on grommet</text>',
        f'<path class="lead" d="M{tail_x + 4:.0f} {tail_y - 9:.0f}L{tail_x + 10:.0f} {tail_y - 34:.0f}"/>'
        f'<text x="{tail_x - 6:.0f}" y="{tail_y - 42:.0f}" class="small">tail beyond knot</text>',
        '</g>',
        '<path d="M470 64V330" stroke="#a7b9ab" stroke-width="1.5" stroke-dasharray="5 6"/>',
        '<g id="loop-artwork">',
        '<text x="500" y="76">FIXED LOOP: FIGURE-EIGHT ON A BIGHT</text>',
        loop.svg(width=9, outline=1.4, ident='fig8-loop-rope', halo=BG, halo_width=2.6),
        '</g>',
    ]
    top = min(loop.samples, key=lambda q: q[1])
    knot_right = max((q for q in loop.samples if 150 < q[1] < 260), key=lambda q: q[0])
    stand = loop.samples[0]
    tail = loop.samples[-1]
    parts += [
        f'<path class="lead" d="M{top[0] + 34:.0f} {top[1] + 22:.0f}L{top[0] + 70:.0f} {top[1] + 22:.0f}"/>'
        f'<text x="{top[0] + 76:.0f}" y="{top[1] + 28:.0f}" class="small">loop</text>',
        f'<path class="lead" d="M{knot_right[0] + 6:.0f} {knot_right[1]:.0f}L{knot_right[0] + 34:.0f} {knot_right[1] - 18:.0f}"/>'
        f'<text x="{knot_right[0] + 38:.0f}" y="{knot_right[1] - 30:.0f}" class="small">strands side by side,</text>'
        f'<text x="{knot_right[0] + 38:.0f}" y="{knot_right[1] - 8:.0f}" class="small">never crossed</text>',
        f'<path class="lead" d="M{stand[0] - 8:.0f} {stand[1] - 6:.0f}L{stand[0] - 40:.0f} {stand[1] - 6:.0f}"/>'
        f'<text x="{stand[0] - 46:.0f}" y="{stand[1] - 1:.0f}" class="small" text-anchor="end">standing part</text>',
        f'<path class="lead" d="M{tail[0] + 8:.0f} {tail[1] - 4:.0f}L{tail[0] + 40:.0f} {tail[1] - 4:.0f}"/>'
        f'<text x="{tail[0] + 46:.0f}" y="{tail[1] + 1:.0f}" class="small">tail to spare</text>',
        '<rect x="24" y="345" width="852" height="32" rx="4" fill="#f7e5d9"/>',
        '<text x="37" y="367" class="small">Camp-cord figure-eight loops are not certified anchors for climbing, rescue or life support.</text>',
        '</svg>',
    ]
    return '\n'.join(parts) + '\n', [stopper, core, loop]


def fig8_checks(ropes):
    stopper, core, loop = ropes
    results = {}
    for rope in ropes:
        results[rope.name] = rope.report()
        results[rope.name]['problems'] = rope.check_crossings()
    results['figure-eight stopper']['is_figure_eight'] = (
        len(stopper.crossings) == 4 and stopper.determinant() == 5 and stopper.gauss_string() == FIG8_EXPECTED)
    results['figure-eight loop core']['is_figure_eight'] = (
        len(core.crossings) == 4 and core.determinant() == 5 and core.gauss_string() == FIG8_EXPECTED)
    ok, counts, stray = strand_crossings_follow_core(core, loop, 22)
    results['figure-eight loop']['doubled_core_consistent'] = ok
    results['figure-eight loop']['strand_crossings_per_core_crossing'] = counts
    results['figure-eight loop']['stray_strand_crossings'] = stray
    return results


PLATES = {'Z09-P14': (bowline_svg, bowline_checks), 'Z09-P15': (fig8_svg, fig8_checks)}


def build():
    output = {}
    for page, (make, check) in PLATES.items():
        svg, ropes = make()
        output[page] = (svg, check(ropes))
    return output


def accepted(results):
    flat = []
    for page, checks in results.items():
        for name, rec in checks.items():
            flat.append(not rec['problems'])
            flat.extend(v for k, v in rec.items() if k.startswith(('is_', 'core_', 'tail_', 'stopper_', 'doubled_')))
    return all(flat)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true', help='Write revised SVGs and the topology receipt')
    parser.add_argument('--check', action='store_true', help='Fail unless retained files equal a fresh build')
    parser.add_argument('--out', type=Path, help='Write SVGs to a scratch directory instead')
    args = parser.parse_args()
    built = build()
    results = {page: checks for page, (_, checks) in built.items()}
    receipt = json.dumps(results, indent=1, sort_keys=True) + '\n'
    if not accepted(results):
        raise SystemExit('Knot topology check failed:\n' + receipt)
    if args.out:
        args.out.mkdir(parents=True, exist_ok=True)
        for page, (svg, _) in built.items():
            (args.out / f'{page}.svg').write_text(svg, encoding='utf-8')
    if args.write:
        for page, (svg, _) in built.items():
            (OUT / 'revised' / f'{page}.svg').write_text(svg, encoding='utf-8')
        (OUT / 'qa/KNOT_TOPOLOGY.json').write_text(receipt, encoding='utf-8')
    if args.check:
        for page, (svg, _) in built.items():
            if (OUT / 'revised' / f'{page}.svg').read_text(encoding='utf-8') != svg:
                raise SystemExit(f'{page} differs from a fresh topology-checked build')
        if (OUT / 'qa/KNOT_TOPOLOGY.json').read_text(encoding='utf-8') != receipt:
            raise SystemExit('Knot topology receipt differs from a fresh build')
    print(f'PASS: {len(built)} knot plates, topology accepted')


if __name__ == '__main__':
    main()
