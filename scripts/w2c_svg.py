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
    def __init__(self, page_id, title, desc):
        self.page_id = page_id
        self.title = title
        self.desc = desc
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
            f'<text x="24" y="32" class="small">{self.page_id} · TECHNICAL REVIEW · NOT TO SCALE</text>',
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
