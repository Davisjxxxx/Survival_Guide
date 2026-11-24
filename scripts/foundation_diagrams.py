"""Editable diagrams for the field cards. All drawings are conceptual and unscaled."""
from html import escape
from textwrap import wrap

# Each original drawing adds a spatial or material relationship to the three text labels.
CROSS_SECTIONS = {
    'Z02-P01': (
        '<path d="M25 80Q115 159 201 131T330 99L452 68H686V152H25Z" fill="#c9d6b6"/>'
        '<path d="M38 100Q103 146 191 136L209 143Q105 163 34 119Z" fill="#68a3b6"/>'
        '<path d="M410 88l38-31 34 31Z" fill="#274d42"/>'
        '<path d="M501 85h135" stroke="#285345" stroke-width="5" marker-end="url(#arrow)"/>'
    ),
    'Z02-P02': (
        '<path d="M30 147h664" stroke="#8a936e" stroke-width="6"/>'
        '<path d="M56 81h179M87 110h139" stroke="#5a8191" stroke-width="5" marker-end="url(#arrow)"/>'
        '<path d="M290 146V51l-35 12v83Z" fill="#7b835f"/>'
        '<path d="M399 147l31-42 35 42" fill="#b7caba" stroke="#315245" stroke-width="4"/>'
        '<path d="M463 120h165" stroke="#285345" stroke-width="5" marker-end="url(#arrow)"/>'
    ),
    'Z02-P03': (
        '<path d="M80 120h550v34H80Z" fill="#b2a98b"/>'
        '<rect x="108" y="102" width="482" height="18" rx="7" fill="#dbad50"/>'
        '<path d="M122 101q47-33 125-26h286q42 3 45 26Z" fill="#82a798"/>'
        '<circle cx="147" cy="81" r="17" fill="#527566"/><path d="M174 76l72-18h274l41 21" '
        'fill="none" stroke="#285345" stroke-width="8" stroke-linecap="round"/>'
    ),
    'Z03-P02': (
        '<path d="M59 131l32-26 32 25-6-32 48 34-18-42 32 42z" fill="#a68d56"/>'
        '<path d="M273 132l96-39m-82 45 108-28m-93 27 55-49" stroke="#92724b" '
        'stroke-width="7" stroke-linecap="round"/>'
        '<path d="M493 133l129-35m-94 40 97-13m-112-8 89-42" stroke="#715435" '
        'stroke-width="16" stroke-linecap="round"/>'
    ),
    'Z03-P03': (
        '<path d="M23 86h132m-94 28h94" stroke="#527e8b" stroke-width="5" marker-end="url(#arrow)"/>'
        '<path d="M184 148V58l-26 12v78Z" fill="#7b835f"/>'
        '<path d="M282 145h290" stroke="#b1a585" stroke-width="16"/>'
        '<path d="M289 132h277" stroke="#d3ab60" stroke-width="10"/>'
        '<path d="M362 124v-29q22-30 81 0l30 29Z" fill="#80a596"/>'
        '<circle cx="359" cy="110" r="14" fill="#365b4c"/>'
    ),
    'Z04-P01': (
        '<path d="M41 77l111 48 82-34" fill="none" stroke="#6f9b9d" stroke-width="6"/>'
        '<path d="M145 75v25m33-34v24m31-32v22" stroke="#6292a6" stroke-width="4"/>'
        '<path d="M232 113l35 22" stroke="#6292a6" stroke-width="5" marker-end="url(#arrow)"/>'
        '<path d="M271 99l17 50h73l17-50Z" fill="#8db3c4" stroke="#305a6e" stroke-width="4"/>'
        '<path d="M441 65v87" stroke="#aa603d" stroke-width="4" stroke-dasharray="6 5"/>'
        '<rect x="566" y="81" width="89" height="65" rx="11" fill="#b1c9b9" stroke="#315245" stroke-width="4"/>'
        '<path d="M564 80h93" stroke="#315245" stroke-width="9"/>'
    ),
}


def text(lines, x, y, line_height=20):
    return ''.join(f'<text x="{x}" y="{y+i*line_height}">{escape(line)}</text>'
                   for i,line in enumerate(lines))


def render_diagram(card):
    stages = card['diagram'].split(' | ')
    card_id = card['id']
    artwork = CROSS_SECTIONS.get(card_id)
    if artwork:
        start_y, total, panel_y = 182, 240, 162
    else:
        start_y, total, panel_y = 63, 116, 38
    panels = []
    for i, stage in enumerate(stages):
        x = 20+i*233
        panels.append(f'<rect x="{x}" y="{panel_y}" width="212" height="62" rx="7" '
                      f'fill="#f9faef" stroke="#90a595"/>')
        panels.append(text(wrap(stage,24),x+12,start_y,18))
        if i < 2 and not artwork:
            panels.append(f'<path d="M{x+216} {panel_y+31}h13" stroke="#285345" '
                          'stroke-width="2" marker-end="url(#arrow)"/>')
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 {total}" role="img" '
        'aria-labelledby="title desc">'
        f'<title id="title">{escape(card["title"])}</title><desc id="desc">{escape(card["diagram"])}</desc>'
        '<defs><marker id="arrow" viewBox="0 0 10 10" markerWidth="3" markerHeight="3" '
        'refX="8" refY="5" orient="auto"><path d="M0 0L10 5 0 10Z" fill="#285345"/></marker></defs>'
        f'<rect width="720" height="{total}" rx="12" fill="#edf1e9"/>'
        '<g font-family="system-ui,sans-serif" font-size="15" font-weight="650" fill="#183c31">'
        + text([card_id+' · FIELD SCHEMATIC'],20,23) + (artwork or '')
        + ''.join(panels) + '</g></svg>\n')
