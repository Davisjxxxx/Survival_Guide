"""Topology-checked rope drawings for Wave 2C technical plates.

A rope is a smooth centerline through control points ``(x, y, z)`` in plate
units (x right, y down, as in SVG) with ``z`` as depth toward the viewer. The
control points are joined with a uniform Catmull-Rom spline written as cubic
Bezier segments. The projected centerline is sampled to locate every
self-crossing, and each crossing is resolved by the interpolated depth of the
two strands. A crossing is accepted only when the depth gap is clear and the
strands meet at a legible angle.

The SVG draws the whole rope once and then redraws a short window of each
over-strand with a background halo and outline, so the printed over/under
structure is exactly the structure of the depth model.

Verification helpers:

* ``Rope.crossings`` - ordered crossing table with over/under strands;
* ``Rope.gauss()`` - sequence of over (O) and under (U) passages along the rope;
* ``Rope.determinant()`` - knot determinant of the diagram closed through the
  outer face (meaningful when both rope ends run out to the exterior);
* ``Rope.inside(point, s0, s1)`` - point-in-loop test for a closed rope segment.

These checks establish that a drawing is internally consistent and matches a
stated tying sequence. They do not replace a qualified rigging review.
"""
from fractions import Fraction
from math import asin, atan2, degrees, hypot, pi, sin

MIN_DEPTH_GAP = 0.5
MIN_CROSSING_ANGLE = 28.0


def _lerp(a, b, t):
    return tuple(x + (y - x) * t for x, y in zip(a, b))


def catmull_rom(points):
    """Return cubic Bezier segments ``(p0, c1, c2, p1)`` through ``points``."""
    pts = [tuple(float(v) for v in p) for p in points]
    if len(pts) < 2:
        raise ValueError('A rope needs at least two control points')
    first = tuple(2 * a - b for a, b in zip(pts[0], pts[1]))
    last = tuple(2 * a - b for a, b in zip(pts[-1], pts[-2]))
    ext = [first, *pts, last]
    segments = []
    for i in range(1, len(pts)):
        p0, p1, p2, p3 = ext[i - 1], ext[i], ext[i + 1], ext[i + 2]
        c1 = tuple(b + (c - a) / 6 for a, b, c in zip(p0, p1, p2))
        c2 = tuple(c - (d - b) / 6 for b, c, d in zip(p1, p2, p3))
        segments.append((p1, c1, c2, p2))
    return segments


def bezier(seg, t):
    p0, c1, c2, p1 = seg
    u = 1 - t
    return tuple(u * u * u * a + 3 * u * u * t * b + 3 * u * t * t * c + t * t * t * d
                 for a, b, c, d in zip(p0, c1, c2, p1))


def _segment_hit(a, b, c, d):
    """Intersection parameters of 2D segments ab and cd, or None."""
    rx, ry = b[0] - a[0], b[1] - a[1]
    sx, sy = d[0] - c[0], d[1] - c[1]
    den = rx * sy - ry * sx
    if abs(den) < 1e-12:
        return None
    qx, qy = c[0] - a[0], c[1] - a[1]
    t = (qx * sy - qy * sx) / den
    u = (qx * ry - qy * rx) / den
    if 0 <= t < 1 and 0 <= u < 1:
        return t, u
    return None


def _det(matrix):
    """Exact determinant by fraction-based elimination."""
    m = [[Fraction(v) for v in row] for row in matrix]
    n = len(m)
    sign, result = 1, Fraction(1)
    for col in range(n):
        pivot = next((r for r in range(col, n) if m[r][col] != 0), None)
        if pivot is None:
            return 0
        if pivot != col:
            m[col], m[pivot] = m[pivot], m[col]
            sign = -sign
        result *= m[col][col]
        for r in range(col + 1, n):
            factor = m[r][col] / m[col][col]
            if factor:
                for k in range(col, n):
                    m[r][k] -= factor * m[col][k]
    return int(sign * result)


def _fmt(v):
    text = f'{v:.1f}'
    return text[:-2] if text.endswith('.0') else text


class Rope:
    def __init__(self, points, samples_per_segment=60, name='rope'):
        self.name = name
        self.points = points
        self.segments = catmull_rom(points)
        self.samples = []
        s = 0.0
        prev = None
        for index, seg in enumerate(self.segments):
            for k in range(samples_per_segment + (1 if index == len(self.segments) - 1 else 0)):
                t = k / samples_per_segment
                p = bezier(seg, t)
                if prev is not None:
                    s += hypot(p[0] - prev[0], p[1] - prev[1])
                self.samples.append((p[0], p[1], p[2], s))
                prev = p
        self.length = s
        self.crossings = self._find_crossings()

    # ----------------------------------------------------------------- geometry
    def at(self, s):
        """Point (x, y, z) at arc length ``s``."""
        s = max(0.0, min(self.length, s))
        lo, hi = 0, len(self.samples) - 1
        while hi - lo > 1:
            mid = (lo + hi) // 2
            if self.samples[mid][3] <= s:
                lo = mid
            else:
                hi = mid
        a, b = self.samples[lo], self.samples[hi]
        span = b[3] - a[3]
        t = 0 if span == 0 else (s - a[3]) / span
        return _lerp(a[:3], b[:3], t)

    def tangent(self, s, h=1.5):
        a, b = self.at(s - h), self.at(s + h)
        n = hypot(b[0] - a[0], b[1] - a[1]) or 1
        return ((b[0] - a[0]) / n, (b[1] - a[1]) / n)

    def nearest_s(self, x, y):
        best = min(self.samples, key=lambda p: (p[0] - x) ** 2 + (p[1] - y) ** 2)
        return best[3]

    def _find_crossings(self):
        pts = self.samples
        found = []
        for i in range(len(pts) - 1):
            a, b = pts[i], pts[i + 1]
            for j in range(i + 2, len(pts) - 1):
                c, d = pts[j], pts[j + 1]
                if c[3] - b[3] < 6:
                    continue
                hit = _segment_hit(a, b, c, d)
                if not hit:
                    continue
                t, u = hit
                s1 = a[3] + (b[3] - a[3]) * t
                s2 = c[3] + (d[3] - c[3]) * u
                if any(abs(s1 - f['s1']) < 2 and abs(s2 - f['s2']) < 2 for f in found):
                    continue
                p1, p2 = self.at(s1), self.at(s2)
                t1, t2 = self.tangent(s1), self.tangent(s2)
                cross = t1[0] * t2[1] - t1[1] * t2[0]
                angle = degrees(asin(min(1.0, abs(cross))))
                over_first = p1[2] > p2[2]
                found.append(dict(
                    s1=s1, s2=s2, x=p1[0], y=p1[1], z1=p1[2], z2=p2[2],
                    gap=abs(p1[2] - p2[2]), angle=angle,
                    over=s1 if over_first else s2, under=s2 if over_first else s1,
                ))
        found.sort(key=lambda f: f['s1'])
        for number, f in enumerate(found, 1):
            f['id'] = number
        return found

    # ------------------------------------------------------------ verification
    def gauss(self):
        events = []
        for f in self.crossings:
            events.append((f['over'], 'O', f['id']))
            events.append((f['under'], 'U', f['id']))
        events.sort()
        return [(kind, ident) for _, kind, ident in events]

    def gauss_string(self):
        return ' '.join(f'{kind}{ident}' for kind, ident in self.gauss())

    def determinant(self):
        """Knot determinant of the diagram closed through the outer face."""
        n = len(self.crossings)
        if n == 0:
            return 1
        unders = sorted((f['under'], f['id']) for f in self.crossings)
        index = {ident: k for k, (_, ident) in enumerate(unders)}

        def arc_of(s):
            # arc k runs from under-event k to under-event k+1 (cyclic)
            k = -1
            for pos, (us, _) in enumerate(unders):
                if us < s:
                    k = pos
            return k % n

        matrix = [[0] * n for _ in range(n)]
        for row, f in enumerate(self.crossings):
            k = index[f['id']]
            incoming, outgoing = (k - 1) % n, k
            over = arc_of(f['over'])
            matrix[row][over] += 2
            matrix[row][incoming] -= 1
            matrix[row][outgoing] -= 1
        minor = [r[1:] for r in matrix[1:]]
        return abs(_det(minor)) if minor else 1

    def check_crossings(self, min_gap=MIN_DEPTH_GAP, min_angle=MIN_CROSSING_ANGLE):
        problems = []
        for f in self.crossings:
            if f['gap'] < min_gap:
                problems.append(f"crossing {f['id']} depth gap {f['gap']:.2f}")
            if f['angle'] < min_angle:
                problems.append(f"crossing {f['id']} angle {f['angle']:.1f}")
        return problems

    def inside(self, point, s0, s1):
        """True when ``point`` lies inside the polygon traced from s0 to s1 and closed."""
        poly = [(p[0], p[1]) for p in self.samples if s0 <= p[3] <= s1]
        x, y = point
        inside = False
        for (x1, y1), (x2, y2) in zip(poly, poly[1:] + poly[:1]):
            if (y1 > y) != (y2 > y):
                xin = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
                if xin > x:
                    inside = not inside
        return inside

    def report(self):
        return dict(
            name=self.name,
            crossings=len(self.crossings),
            gauss=self.gauss_string(),
            determinant=self.determinant(),
            min_depth_gap=round(min((f['gap'] for f in self.crossings), default=0), 2),
            min_angle=round(min((f['angle'] for f in self.crossings), default=90), 1),
            length=round(self.length, 1),
        )

    # ---------------------------------------------------------------- drawing
    def path_d(self):
        p0 = self.segments[0][0]
        parts = [f'M{_fmt(p0[0])} {_fmt(p0[1])}']
        for _, c1, c2, p1 in self.segments:
            parts.append(f'C{_fmt(c1[0])} {_fmt(c1[1])} {_fmt(c2[0])} {_fmt(c2[1])} {_fmt(p1[0])} {_fmt(p1[1])}')
        return ''.join(parts)

    def window_d(self, s0, s1, step=1.5):
        s0, s1 = max(0.0, s0), min(self.length, s1)
        count = max(2, int((s1 - s0) / step) + 1)
        pts = [self.at(s0 + (s1 - s0) * k / (count - 1)) for k in range(count)]
        return 'M' + 'L'.join(f'{_fmt(p[0])} {_fmt(p[1])}' for p in pts)

    def svg(self, width=10.0, rope='#c9933f', edge='#4a3215', shine='#f0d49a',
            halo='#f2f3e9', halo_width=3.0, outline=1.6, whip=None, ident=None):
        """Return SVG markup for the rope with crossings drawn by depth."""
        total = width + 2 * outline
        ident = ident or self.name
        d = self.path_d()
        layers = [
            f'<path d="{d}" fill="none" stroke="{edge}" stroke-width="{_fmt(total)}" stroke-linecap="round" stroke-linejoin="round"/>',
            f'<path d="{d}" fill="none" stroke="{rope}" stroke-width="{_fmt(width)}" stroke-linecap="round" stroke-linejoin="round"/>',
            f'<path d="{d}" fill="none" stroke="{shine}" stroke-width="{_fmt(width * 0.26)}" stroke-linecap="round" stroke-linejoin="round" opacity=".85"/>',
        ]
        unders = [f['under'] for f in self.crossings]
        halos, strands = [], []
        for f in sorted(self.crossings, key=lambda c: max(c['z1'], c['z2'])):
            reach = (total / 2 + halo_width) / max(sin(f['angle'] * pi / 180), 0.4) + width * 0.9
            s0, s1 = f['over'] - reach, f['over'] + reach
            for u in unders:
                if s0 < u < f['over']:
                    s0 = (u + f['over']) / 2
                if f['over'] < u < s1:
                    s1 = (u + f['over']) / 2
            wd = self.window_d(s0, s1)
            # Two passes: every halo first, then every over-strand, so parallel
            # over-strands at one crossing never erase each other's outline.
            halos.append(f'<path d="{wd}" fill="none" stroke="{halo}" stroke-width="{_fmt(total + 2 * halo_width)}" stroke-linecap="butt"/>')
            strands.append(
                f'<path d="{wd}" fill="none" stroke="{edge}" stroke-width="{_fmt(total)}" stroke-linecap="butt"/>'
                f'<path d="{wd}" fill="none" stroke="{rope}" stroke-width="{_fmt(width)}" stroke-linecap="butt"/>'
                f'<path d="{wd}" fill="none" stroke="{shine}" stroke-width="{_fmt(width * 0.26)}" stroke-linecap="butt" opacity=".85"/>'
            )
        windows = halos + strands
        ends = []
        if whip:
            for s in (0.0, self.length):
                a = self.at(min(s, self.length - 7) if s else 0)
                b = self.at(max(s - 7, 0) if s else 7)
                ends.append(f'<path d="M{_fmt(a[0])} {_fmt(a[1])}L{_fmt(b[0])} {_fmt(b[1])}" stroke="{whip}" '
                            f'stroke-width="{_fmt(total)}" stroke-linecap="butt"/>')
        return f'<g id="{ident}">' + ''.join(layers + windows + ends) + '</g>'


def describe(rope):
    rep = rope.report()
    return (f"{rep['name']}: {rep['crossings']} crossings, determinant {rep['determinant']}, "
            f"min depth gap {rep['min_depth_gap']}, min angle {rep['min_angle']} deg; {rep['gauss']}")
