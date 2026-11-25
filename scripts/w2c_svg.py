"""Shared drawing primitives for Wave 2C technical plates (900 x 395, A04 style).

Plates keep the qualified A04 conventions: a header naming the page and NOT TO
SCALE, the physical subject as the drawing, short labels tied to parts with
leader lines, typed arrows (flow, reverse flow, load or reaction, air or heat,
motion), and a bottom band carrying the card's stop or exit condition.
"""
from html import escape

BG = '#f2f3e9'
INK = '#183a30'
FLOW = '#205b68'
REVERSE = '#8b3825'
LOAD = '#3b3b3b'
AIR = '#6b7f8c'
WATER = '#9cc3cf'
WATER_EDGE = '#3d7186'
SOIL = '#c9b48a'
SOIL_EDGE = '#8a7350'
STEEL = '#c9cdd0'
PANEL_OK = '#e7f0ea'
PANEL_BAD = '#fbeee7'
STYLE = ('<style>text{font:650 19px system-ui,sans-serif;fill:#183a30}.small{font-size:17px}.tiny{font-size:15px}'
         '.head{font-size:18px;letter-spacing:.4px}.warn{fill:#8b3825}.ok{fill:#205b68}.mute{fill:#4c5d55}.inv{fill:#ffffff}'
         '.lead{fill:none;stroke:#365c50;stroke-width:1.6}</style>')
MARKERS = {
    'flow': FLOW, 'reverse': REVERSE, 'load': LOAD, 'air': AIR, 'ink': INK,
}


def fmt(v):
    text = f'{v:.1f}'
    return text[:-2] if text.endswith('.0') else text


class Plate:
    def __init__(self, page_id, title, desc, scale_note='NOT TO SCALE'):
        self.page_id = page_id
        self.title = title
        self.desc = desc
        self.scale_note = scale_note
        self.items = []

    def add(self, *markup):
        self.items.extend(markup)
        return self

    def text(self, x, y, s, cls='small', anchor='start', extra=''):
        a = '' if anchor == 'start' else f' text-anchor="{anchor}"'
        self.items.append(f'<text x="{fmt(x)}" y="{fmt(y)}" class="{cls}"{a}{extra}>{escape(s)}</text>')
        return self

    def lines(self, x, y, rows, cls='small', pitch=None, anchor='start'):
        if pitch is None:
            pitch = 21 if 'tiny' in cls else 23 if 'small' in cls else 25
        for i, row in enumerate(rows):
            self.text(x, y + i * pitch, row, cls, anchor)
        return self

    def lead(self, *pts):
        d = 'M' + 'L'.join(f'{fmt(x)} {fmt(y)}' for x, y in pts)
        self.items.append(f'<path class="lead" d="{d}"/>')
        return self

    def arrow(self, d, kind='flow', width=4, dash=None, ident=None):
        color = MARKERS[kind]
        extra = f' stroke-dasharray="{dash}"' if dash else ''
        idattr = f' id="{ident}"' if ident else ''
        self.items.append(f'<path{idattr} d="{d}" fill="none" stroke="{color}" stroke-width="{width}"{extra} '
                          f'marker-end="url(#m-{kind})"/>')
        return self

    def panel(self, x, y, w, h, kind='ok', title=None):
        fill = PANEL_OK if kind == 'ok' else PANEL_BAD if kind == 'bad' else '#f7f7ef'
        stroke = '#7ea08d' if kind == 'ok' else '#c08a72' if kind == 'bad' else '#a9b6aa'
        self.items.append(f'<rect x="{fmt(x)}" y="{fmt(y)}" width="{fmt(w)}" height="{fmt(h)}" rx="10" '
                          f'fill="{fill}" stroke="{stroke}" stroke-width="1.6"/>')
        if title:
            cls = 'head ok' if kind == 'ok' else 'head warn' if kind == 'bad' else 'head'
            self.text(x + 16, y + 26, title, cls)
        return self

    def band(self, s):
        self.items.append('<rect x="24" y="345" width="852" height="32" rx="4" fill="#f7e5d9"/>')
        self.text(37, 367, s, 'small')
        return self

    def svg(self):
        defs = ''.join(
            f'<marker id="m-{k}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="4.2" markerHeight="4.2" '
            f'orient="auto"><path d="M0 0L10 5L0 10Z" fill="{c}"/></marker>' for k, c in MARKERS.items())
        head = [
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 395" role="img" aria-labelledby="title desc">',
            f'<title id="title">{escape(self.title)}</title>',
            f'<desc id="desc">{escape(self.desc)}</desc>',
            f'<defs>{defs}</defs>',
            STYLE,
            f'<rect x="1" y="1" width="898" height="393" rx="12" fill="{BG}" stroke="#789481" stroke-width="2"/>',
            f'<text x="24" y="32" class="small">{self.page_id} · TECHNICAL REVIEW · {self.scale_note}</text>',
            f'<g id="{self.page_id.lower()}-artwork">',
        ]
        return '\n'.join(head + self.items + ['</g>', '</svg>']) + '\n'


# ---------------------------------------------------------------- components
def pipe(points, width=10, color='#8fa3ad', edge='#4a5a62'):
    d = 'M' + 'L'.join(f'{fmt(x)} {fmt(y)}' for x, y in points)
    return (f'<path d="{d}" fill="none" stroke="{edge}" stroke-width="{width + 3}" stroke-linejoin="round"/>'
            f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linejoin="round"/>')


def hose(points, width=7):
    return pipe(points, width, '#4f8a4c', '#2d5a2b')


def bucket(x, y, w, h, liquid='#c9d9b8', level=0.6, label=None):
    """Open bucket with its rim at y (top) and base at y + h."""
    taper = w * 0.08
    body = f'M{fmt(x)} {fmt(y)}L{fmt(x + w)} {fmt(y)}L{fmt(x + w - taper)} {fmt(y + h)}L{fmt(x + taper)} {fmt(y + h)}Z'
    ly = y + h * (1 - level)
    lt = taper * (1 - level)
    fill = (f'M{fmt(x + lt)} {fmt(ly)}L{fmt(x + w - lt)} {fmt(ly)}L{fmt(x + w - taper)} {fmt(y + h)}'
            f'L{fmt(x + taper)} {fmt(y + h)}Z')
    out = [f'<path d="{fill}" fill="{liquid}"/>',
           f'<path d="{body}" fill="none" stroke="{INK}" stroke-width="2.6" stroke-linejoin="round"/>',
           f'<line x1="{fmt(x - 4)}" y1="{fmt(y)}" x2="{fmt(x + w + 4)}" y2="{fmt(y)}" stroke="{INK}" stroke-width="3.4"/>']
    if label:
        out.append(f'<text x="{fmt(x + w / 2)}" y="{fmt(y + h * 0.82)}" class="tiny" text-anchor="middle">{escape(label)}</text>')
    return ''.join(out)


def ground(x, y, w, h, water_top=None):
    """Soil block with optional saturated zone from water_top downward."""
    out = [f'<rect x="{fmt(x)}" y="{fmt(y)}" width="{fmt(w)}" height="{fmt(h)}" fill="{SOIL}" stroke="{SOIL_EDGE}" stroke-width="1.5"/>']
    if water_top is not None:
        out.append(f'<rect x="{fmt(x)}" y="{fmt(water_top)}" width="{fmt(w)}" height="{fmt(y + h - water_top)}" '
                   f'fill="{WATER}" fill-opacity=".38"/>')
        for k in range(int(x) + 10, int(x + w) - 10, 26):
            out.append(f'<path d="M{k} {fmt(water_top + 10)}h12" stroke="{WATER_EDGE}" stroke-width="1.4"/>')
    return ''.join(out)


def cross(x, y, r=13, color=REVERSE):
    return (f'<circle cx="{fmt(x)}" cy="{fmt(y)}" r="{r}" fill="#fff" stroke="{color}" stroke-width="2.6"/>'
            f'<path d="M{fmt(x - r * .45)} {fmt(y - r * .45)}L{fmt(x + r * .45)} {fmt(y + r * .45)}'
            f'M{fmt(x + r * .45)} {fmt(y - r * .45)}L{fmt(x - r * .45)} {fmt(y + r * .45)}" stroke="{color}" stroke-width="3"/>')


def check(x, y, r=13, color=FLOW):
    return (f'<circle cx="{fmt(x)}" cy="{fmt(y)}" r="{r}" fill="#fff" stroke="{color}" stroke-width="2.6"/>'
            f'<path d="M{fmt(x - r * .5)} {fmt(y)}L{fmt(x - r * .1)} {fmt(y + r * .42)}L{fmt(x + r * .52)} {fmt(y - r * .4)}" '
            f'fill="none" stroke="{color}" stroke-width="3"/>')


def jug(x, y, h=54, label='SAFE', fill='#dcecf3'):
    w = h * 0.62
    return (f'<path d="M{fmt(x)} {fmt(y + h)}V{fmt(y + h * .28)}Q{fmt(x)} {fmt(y + h * .16)} {fmt(x + w * .3)} {fmt(y + h * .12)}'
            f'V{fmt(y)}H{fmt(x + w * .62)}V{fmt(y + h * .12)}Q{fmt(x + w)} {fmt(y + h * .16)} {fmt(x + w)} {fmt(y + h * .28)}'
            f'V{fmt(y + h)}Z" fill="{fill}" stroke="{INK}" stroke-width="2.2"/>'
            + (f'<text x="{fmt(x + w / 2)}" y="{fmt(y + h * .72)}" class="tiny" text-anchor="middle" font-size="11">{escape(label)}</text>'
               if label else ''))


def person(x, y, h=70, pose='stand', fill='#5a6f78'):
    """Simple figure. stand: feet at (x, y); lie: lying on its side with head at x, body to the right."""
    r = h * 0.11
    if pose == 'lie':
        return (f'<circle cx="{fmt(x)}" cy="{fmt(y - r)}" r="{fmt(r)}" fill="{fill}"/>'
                f'<rect x="{fmt(x + r * 1.2)}" y="{fmt(y - r * 1.9)}" width="{fmt(h * 0.78)}" height="{fmt(r * 1.8)}" '
                f'rx="{fmt(r * 0.9)}" fill="{fill}"/>')
    return (f'<circle cx="{fmt(x)}" cy="{fmt(y - h + r)}" r="{fmt(r)}" fill="{fill}"/>'
            f'<path d="M{fmt(x - h * .13)} {fmt(y - h * .76)}h{fmt(h * .26)}l{fmt(h * .03)} {fmt(h * .4)}h-{fmt(h * .08)}'
            f'l-.0 {fmt(h * .36)}h-{fmt(h * .07)}l-{fmt(h * .02)}-{fmt(h * .3)}l-{fmt(h * .02)} {fmt(h * .3)}h-{fmt(h * .07)}'
            f'v-{fmt(h * .36)}h-{fmt(h * .08)}z" fill="{fill}"/>')


def flame(x, y, s=1.0):
    """Flame with its base at (x, y)."""
    return (f'<path d="M{fmt(x)} {fmt(y)}c{fmt(-14 * s)} 0 {fmt(-16 * s)} {fmt(-14 * s)} {fmt(-8 * s)} {fmt(-24 * s)}'
            f'c{fmt(2 * s)} {fmt(6 * s)} {fmt(6 * s)} {fmt(8 * s)} {fmt(6 * s)} {fmt(2 * s)}c0 {fmt(-8 * s)} {fmt(6 * s)} {fmt(-12 * s)} '
            f'{fmt(10 * s)} {fmt(-16 * s)}c{fmt(-2 * s)} {fmt(10 * s)} {fmt(8 * s)} {fmt(14 * s)} {fmt(6 * s)} {fmt(26 * s)}'
            f'c{fmt(-1 * s)} {fmt(8 * s)} {fmt(-8 * s)} {fmt(12 * s)} {fmt(-14 * s)} {fmt(12 * s)}z" fill="#e0703a" stroke="#8b3825" stroke-width="1.6"/>'
            f'<path d="M{fmt(x)} {fmt(y - 2 * s)}c{fmt(-5 * s)} 0 {fmt(-6 * s)} {fmt(-6 * s)} {fmt(-2 * s)} {fmt(-10 * s)}'
            f'c{fmt(1 * s)} {fmt(3 * s)} {fmt(4 * s)} {fmt(4 * s)} {fmt(5 * s)} {fmt(0)}c{fmt(1 * s)} {fmt(5 * s)} 0 {fmt(10 * s)} {fmt(-3 * s)} {fmt(10 * s)}z" fill="#f6c453"/>')


def alarm(x, y, kind='smoke', r=12):
    if kind == 'co':
        return (f'<rect x="{fmt(x - r)}" y="{fmt(y - r * .75)}" width="{fmt(2 * r)}" height="{fmt(1.5 * r)}" rx="3" '
                f'fill="#ffffff" stroke="#183a30" stroke-width="2"/><text x="{fmt(x)}" y="{fmt(y + 4)}" class="tiny" '
                f'text-anchor="middle" font-size="11">CO</text>')
    return (f'<circle cx="{fmt(x)}" cy="{fmt(y)}" r="{fmt(r)}" fill="#ffffff" stroke="#183a30" stroke-width="2"/>'
            f'<circle cx="{fmt(x)}" cy="{fmt(y)}" r="{fmt(r * .4)}" fill="none" stroke="#183a30" stroke-width="1.4"/>')


def gas(x, y, w, h, fill='#8a8f86', opacity=.32):
    return (f'<rect x="{fmt(x)}" y="{fmt(y)}" width="{fmt(w)}" height="{fmt(h)}" rx="18" fill="{fill}" '
            f'fill-opacity="{opacity}" stroke="#6b706a" stroke-width="1.6" stroke-dasharray="6 5"/>')
