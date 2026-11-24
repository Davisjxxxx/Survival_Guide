"""Editable technical diagrams for the field cards.

All drawings are conceptual and unscaled. Specifications for generated technical
illustrations are retained in foundations/evidence/diagram-specs.json.
"""
from html import escape
import json
from pathlib import Path
from textwrap import wrap

ROOT = Path(__file__).resolve().parents[1]
SPEC_PATH = ROOT / 'foundations/evidence/diagram-specs.json'

# Preserved original pilot/core schematics (11 hand-authored cross-sections).
CROSS_SECTIONS = {
    'Z03-P12': (
        '<path d="M300 139h317v13H300Z" fill="#a28c68"/>'
        '<path d="M405 65l-5 68 6 8 6-8-4-68Z" fill="#8b6d4f" stroke="#315245" stroke-width="3"/>'
        '<path d="M379 64h53" stroke="#647e72" stroke-width="15" stroke-linecap="round"/>'
        '<path d="M90 98q170-98 435 11" fill="none" stroke="#776649" stroke-width="7"/>'
        '<path d="M90 98l304 6q18 2 18-4t-11-4l124 13" fill="none" stroke="#315245" stroke-width="2.5"/>'
        '<path d="M395 139q22-16 47 0" fill="#b67544"/>'
        '<path d="M272 75h58" stroke="#285345" stroke-width="4" marker-end="url(#arrow)"/>'
    ),
    'Z02-P10': (
        '<path d="M64 133h618" stroke="#9da684" stroke-width="6"/>'
        '<path d="M163 118l180-66 166 66" fill="none" stroke="#315245" stroke-width="7"/>'
        '<path d="M239 124h226v9H239Z" fill="#d4ae5d"/>'
        '<path d="M149 109l-36 38m411-38 36 38" stroke="#5b8fa1" stroke-width="5" marker-end="url(#arrow)"/>'
        '<path d="M577 142h94" stroke="#5b8fa1" stroke-width="4" marker-end="url(#arrow)"/>'
    ),
    'Z03-P06': (
        '<path d="M26 146h663" stroke="#849477" stroke-width="5"/>'
        '<rect x="75" y="93" width="93" height="48" rx="7" fill="#7e927c" stroke="#2e5446" stroke-width="4"/>'
        '<path d="M74 108H34M74 122H34" stroke="#96745e" stroke-width="5" marker-end="url(#arrow)"/>'
        '<path d="M188 116h329M189 104v24M517 104v24" stroke="#315245" stroke-width="2"/>'
        '<text x="301" y="103">≥ 20 ft</text>'
        '<path d="M532 85l65-35 64 35v58H532Z" fill="#c4d4b4" stroke="#315245" stroke-width="4"/>'
        '<path d="M557 104h24v23h-24zM606 101h24v42h-24z" fill="#f8f4e9" stroke="#315245" stroke-width="2"/>'
    ),
    'Z03-P10': (
        '<path d="M62 57l50-9 88 45-96 28Z" fill="#9c9e85" stroke="#6e765d" stroke-width="3"/>'
        '<path d="M218 45l17 4-29 90-17-6Z" fill="#768986" stroke="#315245" stroke-width="4"/>'
        '<path d="M213 96q152 9 293 30" fill="none" stroke="#a55b26" stroke-width="3" stroke-dasharray="6 9" marker-end="url(#arrow)"/>'
        '<path d="M498 145l33-39 15 32 36-39 3 35 49-25 20 36Z" fill="#ad965e"/>'
    ),
    'Z04-P10': (
        '<path d="M59 65l12 79h147l12-79" fill="#a5c6cf" stroke="#386273" stroke-width="4"/>'
        '<path d="M72 125q76-14 145 0v17H74Z" fill="#988261"/>'
        '<path d="M229 96h68" stroke="#305966" stroke-width="4" marker-end="url(#arrow)"/>'
        '<path d="M317 83l8 60h96l8-60" fill="#a5c6cf" stroke="#386273" stroke-width="4"/>'
        '<path d="M434 109h71" stroke="#305966" stroke-width="4" marker-end="url(#arrow)"/>'
        '<rect x="524" y="79" width="146" height="63" rx="8" fill="#c1d3b5" stroke="#315245" stroke-width="4"/>'
        '<text x="554" y="116">TREATMENT</text>'
    ),
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

KIND_LABELS = {
    'cutaway': 'CUTAWAY VIEW',
    'exploded': 'EXPLODED COMPONENTS',
    'cross_section': 'MATERIAL CROSS-SECTION',
    'force_redirect': 'STATIC FORCE SCHEMATIC',
    'branch': 'CONDITIONAL DECISION',
    'mechanism': 'MECHANISM DIAGRAM',
    'comparison': 'COMPARATIVE CONFIGURATION',
    'environment': 'ENVIRONMENTAL RELATIONSHIP',
    'decision_tree': 'DECISION TREE',
    'failure_mode': 'FAILURE-MODE ANALYSIS',
}

_SPECS_CACHE = None


SPEC_KEYS = {
    'cutaway': {'layers','callout','accent','variant'},
    'exploded': {'components','callout'},
    'cross_section': {'layers','callout'},
    'mechanism': {'nodes','callout'},
    'comparison': {'options'},
    'environment': {'zones','callout','variant'},
    'decision_tree': {'gates','abort'},
    'failure_mode': {'cause','cue','correction'},
    'branch': {'question','yes','no','stop'},
    'force_redirect': set(),
}
SPEC_OPTIONAL = {'cutaway': {'hazard'}, 'mechanism': {'accent'}}
SPEC_LIST_LENGTHS = {'layers':3,'components':4,'nodes':3,'options':3,'zones':3,'gates':3}


def validate_spec(page, spec):
    kind = spec.get('type')
    keys = spec.keys() - {'type'}
    if kind not in SPEC_KEYS or not SPEC_KEYS[kind] <= keys <= SPEC_KEYS[kind] | SPEC_OPTIONAL.get(kind,set()):
        raise ValueError(f'Invalid figure specification on {page}: {kind}, {sorted(keys)}')
    for key, value in spec.items():
        if isinstance(value,str) and not value.strip():
            raise ValueError(f'Blank figure label on {page}: {key}')
        if key in SPEC_LIST_LENGTHS:
            length = 4 if key == 'layers' and kind == 'cross_section' else SPEC_LIST_LENGTHS[key]
            if not isinstance(value,list) or len(value) != length:
                raise ValueError(f'Invalid figure label list on {page}: {key}')
            if key == 'options':
                for option in value:
                    if not isinstance(option,dict) or set(option) != {'name','note','limit'} or any(
                        not isinstance(part,str) or not part.strip() for part in option.values()
                    ):
                        raise ValueError(f'Invalid comparison option on {page}')
            elif any(not isinstance(label,str) or not label.strip() for label in value):
                raise ValueError(f'Invalid figure label on {page}: {key}')


def load_specs():
    global _SPECS_CACHE
    if _SPECS_CACHE is None:
        if SPEC_PATH.exists():
            _SPECS_CACHE = json.loads(SPEC_PATH.read_text(encoding='utf-8'))
            for page, spec in _SPECS_CACHE.items():
                validate_spec(page,spec)
        else:
            _SPECS_CACHE = {}
    return _SPECS_CACHE


def reset_specs_cache():
    global _SPECS_CACHE
    _SPECS_CACHE = None


def text(lines, x, y, line_height=18, size=14, weight=650, fill='#183c31', anchor='start'):
    attrs = f'font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}"'
    return ''.join(
        f'<text x="{x}" y="{y + i * line_height}" {attrs}>{escape(line)}</text>'
        for i, line in enumerate(lines)
    )


def _lbl(label, x, y, size=12, fill='#183c31', anchor='middle'):
    return f'<text x="{x}" y="{y}" font-size="{size}" font-weight="650" fill="{fill}" text-anchor="{anchor}">{escape(label)}</text>'


def _render_cutaway(spec):
    """Technical cutaway showing outer shell, interior layers, barrier, and flow/hazard callouts."""
    layers = spec.get('layers', ['Outer barrier', 'Protected core', 'Ground / base'])
    callout = spec.get('callout', 'Separation barrier')
    accent = spec.get('accent', '#4e8397')
    hazard = spec.get('hazard', '')
    style = spec.get('variant', 'enclosure')
    parts = ['<g id="cutaway-artwork">']
    if style == 'vessel':
        # Cutaway vessel / catchment / cistern
        parts.append('<rect x="52" y="46" width="170" height="98" rx="8" fill="#dbe6ea" stroke="#315245" stroke-width="3"/>')
        parts.append(f'<rect x="56" y="76" width="162" height="64" rx="4" fill="{accent}" opacity="0.45"/>')
        parts.append('<path d="M56 118q40-10 81 0t81 0v22H56Z" fill="#9a8362"/>')
        parts.append('<path d="M222 86h78" stroke="#315245" stroke-width="3.5" marker-end="url(#arrow)"/>')
        parts.append('<rect x="308" y="46" width="146" height="98" rx="8" fill="#f7f4e9" stroke="#315245" stroke-width="3"/>')
        parts.append('<path d="M312 88h138M312 108h138" stroke="#6f8c7a" stroke-width="3" stroke-dasharray="6 4"/>')
        parts.append('<path d="M454 95h68" stroke="#315245" stroke-width="3.5" marker-end="url(#arrow)"/>')
        parts.append('<rect x="530" y="46" width="146" height="98" rx="8" fill="#d9e7dc" stroke="#184438" stroke-width="3.5"/>')
        parts.append('<path d="M528 46h150" stroke="#184438" stroke-width="7"/>')
        parts.append(_lbl(layers[0], 137, 68, 12))
        parts.append(_lbl(layers[1] if len(layers) > 1 else 'Barrier', 381, 74, 12))
        parts.append(_lbl(layers[2] if len(layers) > 2 else 'Protected', 603, 98, 12))
        parts.append(_lbl(callout, 381, 134, 11, '#5d3420'))
    elif style == 'ground_pit':
        # Cutaway soil / hearth / snow trench with explicit boundary
        parts.append('<path d="M30 82h205l25 54h200l25-54h205v68H30Z" fill="#bfb293" stroke="#5b5139" stroke-width="2.5"/>')
        parts.append('<path d="M262 126h196v10H262Z" fill="#7d6e54"/>')
        parts.append(f'<rect x="278" y="96" width="164" height="28" rx="5" fill="{accent}" opacity="0.55" stroke="#184438" stroke-width="2.5"/>')
        parts.append('<path d="M238 66h244" stroke="#a05332" stroke-width="3" stroke-dasharray="7 5"/>')
        parts.append('<path d="M105 56v22m510-22v22" stroke="#285345" stroke-width="3" marker-end="url(#arrow)"/>')
        parts.append(_lbl(layers[0], 130, 52, 12))
        parts.append(_lbl(layers[1] if len(layers) > 1 else 'Interior', 360, 114, 12))
        parts.append(_lbl(layers[2] if len(layers) > 2 else 'Boundary', 590, 52, 12))
        parts.append(_lbl(callout, 360, 60, 11, '#8b3e1f'))
    else:
        # Cutaway shelter / structure / layered wall
        parts.append('<path d="M40 142h640" stroke="#7d8a68" stroke-width="6"/>')
        parts.append('<path d="M135 140L360 44l225 96" fill="#d9e4d7" stroke="#285345" stroke-width="5"/>')
        parts.append('<path d="M185 140L360 64l175 76" fill="#f7f4ea" stroke="#5c7c6d" stroke-width="2.5" stroke-dasharray="6 4"/>')
        parts.append(f'<rect x="242" y="114" width="236" height="22" rx="6" fill="{accent}" stroke="#285345" stroke-width="2"/>')
        parts.append('<path d="M62 82h66m470 0h66" stroke="#507f92" stroke-width="4" marker-end="url(#arrow)"/>')
        parts.append(_lbl(layers[0], 360, 58, 11, '#183c31'))
        parts.append(_lbl(layers[1] if len(layers) > 1 else 'Air gap / vent', 360, 96, 12, '#183c31'))
        parts.append(_lbl(layers[2] if len(layers) > 2 else 'Insulated base', 360, 130, 11, '#183c31'))
        parts.append(_lbl(callout, 605, 68, 11, '#8b3e1f'))
    if hazard:
        parts.append(f'<rect x="492" y="130" width="204" height="20" rx="4" fill="#faeee5" stroke="#a05332"/>')
        parts.append(_lbl(hazard, 594, 144, 10.5, '#7a2f15'))
    parts.append('</g>')
    return ''.join(parts)


def _render_exploded(spec):
    """Exploded component view with 4-5 distinct aligned assembly modules and dashed alignment axis."""
    comps = spec.get('components', ['Component A', 'Component B', 'Component C', 'Component D'])[:4]
    axis_note = spec.get('callout', 'Assembly / inspection axis')
    fills = ['#d5e2d8', '#e8dfbe', '#cde0e8', '#dfd4c7']
    parts = ['<g id="exploded-artwork">']
    parts.append('<path d="M55 96h610" stroke="#7c8f83" stroke-width="2" stroke-dasharray="7 5"/>')
    n = len(comps)
    span = 620 // n
    for i, comp in enumerate(comps):
        x = 50 + i * span
        w = span - 26
        parts.append(f'<rect x="{x}" y="58" width="{w}" height="74" rx="8" fill="{fills[i % len(fills)]}" stroke="#285345" stroke-width="2.5"/>')
        # Subtle mechanical flange / tab visual cue
        parts.append(f'<rect x="{x+10}" y="48" width="{min(36, w-20)}" height="10" rx="3" fill="#6b8577"/>')
        parts.append(f'<circle cx="{x+w-14}" cy="72" r="5" fill="#285345"/>')
        lines = wrap(comp, 16)
        parts.append(text(lines, x + w / 2, 92 - (len(lines) - 1) * 7, 15, 12, 650, '#183c31', 'middle'))
        if i < n - 1:
            parts.append(f'<path d="M{x+w+3} 95h18" stroke="#285345" stroke-width="2.5" marker-end="url(#arrow)"/>')
    parts.append(_lbl(axis_note, 360, 149, 11, '#4c5f55'))
    parts.append('</g>')
    return ''.join(parts)


def _render_cross_section(spec):
    """Horizontal stratified material cross-section with thickness bands and heat/moisture vectors."""
    strata = spec.get('layers', ['Outer weather face', 'Intermediate layer', 'Inner core', 'Base substrate'])[:4]
    vector = spec.get('callout', 'Transfer / barrier path')
    fills = ['#c5d8de', '#e5d4a1', '#cadbc6', '#b7a98d']
    parts = ['<g id="cross-section-artwork">']
    y0 = 42
    h = 26
    for i, layer in enumerate(strata):
        y = y0 + i * h
        parts.append(f'<rect x="70" y="{y}" width="450" height="{h}" fill="{fills[i % len(fills)]}" stroke="#315245" stroke-width="1.8"/>')
        parts.append(_lbl(layer, 295, y + 17, 12, '#183c31'))
    # Vertical barrier / transfer vector arrows on right side
    parts.append('<path d="M555 48v88" stroke="#a05332" stroke-width="3.5" marker-end="url(#arrow)"/>')
    parts.append('<path d="M585 138V52" stroke="#366c7d" stroke-width="3.5" marker-end="url(#arrow)"/>')
    parts.append(text(wrap(vector, 16), 605, 80, 15, 11.5, 650, '#183c31', 'start'))
    parts.append('</g>')
    return ''.join(parts)


def _render_mechanism(spec):
    """Physical mechanism diagram showing input, conversion zone, output, and feedback/loss."""
    nodes = spec.get('nodes', ['Input force / energy', 'Active interface', 'Useful output'])[:3]
    loss = spec.get('callout', 'Loss / limiting factor')
    accent = spec.get('accent', '#c97b42')
    parts = ['<g id="mechanism-artwork">']
    # Left input block
    parts.append('<rect x="38" y="54" width="168" height="68" rx="10" fill="#d3e3dc" stroke="#285345" stroke-width="3"/>')
    parts.append(text(wrap(nodes[0], 18), 122, 84, 15, 12, 650, '#183c31', 'middle'))
    parts.append('<path d="M208 88h56" stroke="#285345" stroke-width="4" marker-end="url(#arrow)"/>')
    # Central active zone (circle / reactor / interface)
    parts.append(f'<ellipse cx="360" cy="88" rx="88" ry="42" fill="{accent}" fill-opacity="0.28" stroke="{accent}" stroke-width="3.5"/>')
    parts.append(text(wrap(nodes[1], 18), 360, 84, 15, 12, 700, '#183c31', 'middle'))
    parts.append('<path d="M450 88h56" stroke="#285345" stroke-width="4" marker-end="url(#arrow)"/>')
    # Right output block
    parts.append('<rect x="514" y="54" width="168" height="68" rx="10" fill="#e5ebd8" stroke="#285345" stroke-width="3"/>')
    parts.append(text(wrap(nodes[2], 18), 598, 84, 15, 12, 650, '#183c31', 'middle'))
    # Loss / limit vector downward
    parts.append('<path d="M360 130v14" stroke="#a05332" stroke-width="3"/>')
    parts.append('<rect x="215" y="136" width="290" height="20" rx="4" fill="#faeee5" stroke="#a05332"/>')
    parts.append(_lbl(loss, 360, 150, 10.5, '#7a2f15'))
    parts.append('</g>')
    return ''.join(parts)


def _render_comparison(spec):
    """Side-by-side comparative configuration matrix (2 or 3 distinct options with clear limits)."""
    opts = spec.get('options', [
        {'name': 'Option A', 'note': 'Primary method', 'limit': 'Limit A'},
        {'name': 'Option B', 'note': 'Alternative', 'limit': 'Limit B'},
        {'name': 'Option C', 'note': 'Fallback', 'limit': 'Limit C'},
    ])[:3]
    parts = ['<g id="comparison-artwork">']
    n = len(opts)
    w = (660 - (n - 1) * 18) // n
    fills = ['#dce8df', '#e5e9d5', '#e4e8ee']
    for i, opt in enumerate(opts):
        x = 30 + i * (w + 18)
        parts.append(f'<rect x="{x}" y="44" width="{w}" height="104" rx="8" fill="{fills[i % len(fills)]}" stroke="#315245" stroke-width="2.5"/>')
        parts.append(f'<rect x="{x}" y="44" width="{w}" height="24" rx="6" fill="#285345"/>')
        parts.append(_lbl(opt['name'], x + w / 2, 60, 11.5, '#fffdf7'))
        parts.append(text(wrap(opt['note'], 22 if n == 3 else 30), x + 10, 84, 14, 11.5, 600, '#183c31'))
        parts.append(f'<rect x="{x+8}" y="122" width="{w-16}" height="20" rx="4" fill="#faeee5" stroke="#a05332"/>')
        parts.append(_lbl(opt['limit'], x + w / 2, 136, 10, '#7a2f15'))
    parts.append('</g>')
    return ''.join(parts)


def _render_environment(spec):
    """Environmental relationship schematic (terrain profile, hazard source, safe zone, wind/water path)."""
    zones = spec.get('zones', ['Hazard zone', 'Transition / buffer', 'Safer refuge'])[:3]
    flow = spec.get('callout', 'Environmental force')
    variant = spec.get('variant', 'terrain')
    parts = ['<g id="environment-artwork">']
    if variant == 'watershed':
        parts.append('<path d="M28 58L220 112L375 138L520 105L692 64V150H28Z" fill="#cad7b8" stroke="#53684a" stroke-width="2.5"/>')
        parts.append('<path d="M280 124q95 24 190-6l-20 30H295Z" fill="#639db2"/>')
        parts.append('<path d="M90 54l95 26m445-22l-95 24" stroke="#477a90" stroke-width="3.5" marker-end="url(#arrow)"/>')
    elif variant == 'wind_tree':
        parts.append('<path d="M28 144h664" stroke="#7d8a68" stroke-width="5"/>')
        parts.append('<path d="M44 74h120M44 98h105" stroke="#4b7c90" stroke-width="4" marker-end="url(#arrow)"/>')
        parts.append('<path d="M220 144V58l-28 24h56Z" fill="#6e7c5a" stroke="#315245" stroke-width="2.5"/>')
        parts.append('<path d="M235 64l95 52" stroke="#a05332" stroke-width="3" stroke-dasharray="6 5" marker-end="url(#arrow)"/>')
        parts.append('<path d="M510 144l45-42 45 42Z" fill="#285345"/>')
    else:
        parts.append('<path d="M28 136Q185 150 325 110T692 68V150H28Z" fill="#cbd7bc" stroke="#566b4e" stroke-width="2.5"/>')
        parts.append('<path d="M72 64h142" stroke="#a05332" stroke-width="4" marker-end="url(#arrow)"/>')
        parts.append('<rect x="522" y="54" width="128" height="44" rx="7" fill="#dfeae0" stroke="#184438" stroke-width="3"/>')
    parts.append('<rect x="40" y="122" width="190" height="22" rx="4" fill="#faeee5" stroke="#a05332"/>')
    parts.append(_lbl(zones[0], 135, 137, 10.5, '#7a2f15'))
    parts.append('<rect x="265" y="122" width="190" height="22" rx="4" fill="#f7f4e9" stroke="#73877b"/>')
    parts.append(_lbl(zones[1], 360, 137, 10.5, '#183c31'))
    parts.append('<rect x="490" y="122" width="190" height="22" rx="4" fill="#dceadf" stroke="#184438"/>')
    parts.append(_lbl(zones[2], 585, 137, 10.5, '#183c31'))
    parts.append(_lbl(flow, 360, 56, 11.5, '#2b5566'))
    parts.append('</g>')
    return ''.join(parts)


def _render_decision_tree(spec):
    """Structured two-gate branching decision tree with explicit stop/abort branch."""
    gates = spec.get('gates', ['Gate 1?', 'Gate 2?', 'Proceed'])[:3]
    abort = spec.get('abort', 'STOP / Alternate plan')
    parts = ['<g id="decision-tree-artwork">']
    # Diamond 1
    parts.append('<polygon points="125,44 215,82 125,120 35,82" fill="#e6eee6" stroke="#184438" stroke-width="2.8"/>')
    parts.append(text(wrap(gates[0], 14), 125, 79, 14, 11, 700, '#183c31', 'middle'))
    parts.append('<path d="M215 82h60" stroke="#285345" stroke-width="3" marker-end="url(#arrow)"/>')
    parts.append(_lbl('YES', 244, 75, 10, '#184438'))
    # Diamond 2
    parts.append('<polygon points="365,44 455,82 365,120 275,82" fill="#e6eee6" stroke="#184438" stroke-width="2.8"/>')
    parts.append(text(wrap(gates[1], 14), 365, 79, 14, 11, 700, '#183c31', 'middle'))
    parts.append('<path d="M455 82h55" stroke="#285345" stroke-width="3" marker-end="url(#arrow)"/>')
    parts.append(_lbl('YES', 482, 75, 10, '#184438'))
    # Proceed box
    parts.append('<rect x="516" y="54" width="166" height="56" rx="8" fill="#d3e6d6" stroke="#184438" stroke-width="3"/>')
    parts.append(text(wrap(gates[2], 18), 599, 79, 14, 11.5, 700, '#183c31', 'middle'))
    # NO branches down to STOP bar
    parts.append('<path d="M125 120v14h240v-14" fill="none" stroke="#a05332" stroke-width="2.5"/>')
    parts.append(_lbl('NO', 142, 131, 9.5, '#8b3e1f'))
    parts.append(_lbl('NO', 382, 131, 9.5, '#8b3e1f'))
    parts.append('<rect x="115" y="132" width="490" height="22" rx="5" fill="#faeee5" stroke="#a05332" stroke-width="2"/>')
    parts.append(_lbl(abort, 360, 147, 11, '#7a2f15'))
    parts.append('</g>')
    return ''.join(parts)


def _render_failure_mode(spec):
    """Failure-mode cause -> observable cue -> immediate correction / abort illustration."""
    cause = spec.get('cause', 'Failure trigger')
    cue = spec.get('cue', 'Observable warning cue')
    action = spec.get('correction', 'Stop and correct')
    parts = ['<g id="failure-mode-artwork">']
    # Hazard trigger
    parts.append('<rect x="34" y="52" width="192" height="84" rx="8" fill="#f7e5dc" stroke="#a05332" stroke-width="3"/>')
    parts.append('<rect x="34" y="52" width="192" height="22" rx="6" fill="#a05332"/>')
    parts.append(_lbl('FAILURE CAUSE', 130, 67, 10.5, '#fffdf7'))
    parts.append(text(wrap(cause, 20), 130, 92, 15, 11.5, 650, '#5a2310', 'middle'))
    parts.append('<path d="M228 94h34" stroke="#a05332" stroke-width="3.5" marker-end="url(#arrow)"/>')
    # Observable cue
    parts.append('<rect x="266" y="52" width="192" height="84" rx="8" fill="#f6f1d9" stroke="#8a7228" stroke-width="3"/>')
    parts.append('<rect x="266" y="52" width="192" height="22" rx="6" fill="#8a7228"/>')
    parts.append(_lbl('RECOGNIZE CUE', 362, 67, 10.5, '#fffdf7'))
    parts.append(text(wrap(cue, 20), 362, 92, 15, 11.5, 650, '#443810', 'middle'))
    parts.append('<path d="M460 94h34" stroke="#285345" stroke-width="3.5" marker-end="url(#arrow)"/>')
    # Corrective stop
    parts.append('<rect x="498" y="52" width="192" height="84" rx="8" fill="#dceadf" stroke="#184438" stroke-width="3"/>')
    parts.append('<rect x="498" y="52" width="192" height="22" rx="6" fill="#184438"/>')
    parts.append(_lbl('CORRECT / ABORT', 594, 67, 10.5, '#fffdf7'))
    parts.append(text(wrap(action, 20), 594, 92, 15, 11.5, 650, '#183c31', 'middle'))
    parts.append('</g>')
    return ''.join(parts)


def _render_force_redirect(spec):
    # Equal, static pulls on the pulley, not on the anchor. The resultant is dashed.
    return (
        '<g id="force-redirect-artwork" stroke-linecap="round">'
        '<path d="M40 150h640" stroke="#92a595"/>'
        '<circle cx="185" cy="56" r="20" fill="#dce8df" stroke="#285345" stroke-width="2"/>'
        '<circle cx="520" cy="56" r="20" fill="#dce8df" stroke="#285345" stroke-width="2"/>'
        '<g stroke="#285345" stroke-width="3" marker-end="url(#arrow)">'
        '<path d="M169 62v56"/><path d="M201 62v56"/>'
        '<path d="M520 62v56"/><path d="M526 56h58"/></g>'
        '<g stroke="#963c24" stroke-width="3" stroke-dasharray="5 4" marker-end="url(#arrow)">'
        '<path d="M185 58v72"/><path d="M521 58l50 50"/></g>'
        + _lbl('T',156,99) + _lbl('T',215,99) + _lbl('2T',185,144)
        + _lbl('T',506,104) + _lbl('T',579,43) + _lbl('√2 T',591,115)
        + _lbl('Parallel pulls',100,145) + _lbl('Right-angle pulls',488,145)
        + '</g>'
    )


def _render_branch(spec):
    parts = ['<g id="conditional-artwork">']
    parts.append('<rect x="40" y="42" width="640" height="25" rx="5" fill="#dce8df" stroke="#285345"/>')
    parts.append(_lbl(spec['question'],360,59))
    for i, (label, field) in enumerate((('YES','yes'),('NO','no'))):
        x = 40 + 335*i
        parts.append(f'<rect x="{x}" y="82" width="305" height="46" rx="6" fill="#f9faef" stroke="#688476"/>')
        parts.append(_lbl(label,x+26,104,10))
        parts.append(text(wrap(spec[field],29),x+53,101,13,11))
    parts.append(_lbl(spec['stop'],360,149,11,'#672d18'))
    return ''.join(parts) + '</g>'


RENDERERS = {
    'cutaway': _render_cutaway,
    'force_redirect': _render_force_redirect,
    'branch': _render_branch,
    'exploded': _render_exploded,
    'cross_section': _render_cross_section,
    'mechanism': _render_mechanism,
    'comparison': _render_comparison,
    'environment': _render_environment,
    'decision_tree': _render_decision_tree,
    'failure_mode': _render_failure_mode,
}


def render_diagram(card):
    stages = card['diagram'].split(' | ')
    card_id = card['id']
    specs = load_specs()
    spec = specs.get(card_id)
    if card_id in CROSS_SECTIONS:
        artwork = CROSS_SECTIONS[card_id]
        header_tag = f'{card_id} · FIELD SCHEMATIC'
        start_y, total, panel_y = 182, 240, 162
    elif spec:
        kind = spec['type']
        if kind not in RENDERERS:
            raise ValueError(f'Unknown diagram type {kind} for {card_id}')
        artwork = RENDERERS[kind](spec)
        header_tag = f'{card_id} · {KIND_LABELS[kind]} (CONCEPTUAL, NOT TO SCALE)'
        start_y, total, panel_y = 182, 242, 162
    else:
        artwork = None
        header_tag = f'{card_id} · FIELD SCHEMATIC'
        start_y, total, panel_y = 63, 116, 38

    panels = []
    for i, stage in enumerate(stages):
        x = 20 + i * 233
        panels.append(
            f'<rect x="{x}" y="{panel_y}" width="212" height="62" rx="7" '
            'fill="#f9faef" stroke="#90a595"/>'
        )
        panels.append(text(wrap(stage, 24), x + 12, start_y, 18, 14.5, 650, '#183c31'))
        if i < 2 and not artwork:
            panels.append(
                f'<path d="M{x+216} {panel_y+31}h13" stroke="#285345" '
                'stroke-width="2" marker-end="url(#arrow)"/>'
            )
    desc_text = card['diagram']
    if spec:
        desc_text = f"{KIND_LABELS[spec['type']]}: {card['diagram']} — Conceptual illustration, not to scale."
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 {total}" role="img" '
        'aria-labelledby="title desc">\n'
        f'  <title id="title">{escape(card["title"])}</title>\n'
        f'  <desc id="desc">{escape(desc_text)}</desc>\n'
        '  <defs>\n'
        '    <marker id="arrow" viewBox="0 0 10 10" markerWidth="3" markerHeight="3" '
        'refX="8" refY="5" orient="auto"><path d="M0 0L10 5 0 10Z" fill="#285345"/></marker>\n'
        '  </defs>\n'
        f'  <rect width="720" height="{total}" rx="12" fill="#edf1e9"/>\n'
        '  <g font-family="system-ui,sans-serif" font-size="14.5" font-weight="650" fill="#183c31">\n'
        f'    {text([header_tag], 20, 23, 18, 14, 700, "#183c31")}\n'
        f'    {artwork or ""}\n'
        f'    <g id="stage-panels">{"".join(panels)}</g>\n'
        '  </g>\n'
        '</svg>\n'
    )
