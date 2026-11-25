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
    'canner_vent': 'PRESSURE CANNER VENT PATH',
    'branch': 'CONDITIONAL DECISION',
    'mechanism': 'MECHANISM DIAGRAM',
    'comparison': 'COMPARATIVE CONFIGURATION',
    'environment': 'ENVIRONMENTAL RELATIONSHIP',
    'decision_tree': 'DECISION TREE',
    'failure_mode': 'FAILURE-MODE ANALYSIS',
    'correct_vs_wrong': 'CORRECT VS INCORRECT CONFIGURATION',
    'sequence_plate': 'SEQUENTIAL INSTRUCTIONAL PLATE',
    'system_boundary': 'SYSTEM SEPARATION & BOUNDARY',
    'escalation_ladder': 'CARE / ESCALATION LADDER',
    'anatomy_zone': 'CONCEPTUAL ORIENTATION & ZONE GUIDE',
    'seasonal_timeline': 'TIME / SEASONAL PROGRESSION',
    'geological_strata': 'GEOLOGICAL STRATA & MATERIAL PROFILE',
    'mineral_test_plate': 'NON-DESTRUCTIVE MINERAL OBSERVATION PLATE',
    'wildlife_track_plate': 'WILDLIFE SIGN, TRACK & HABITAT PLATE',
    'regulation_boundary': 'JURISDICTION, SEASON & LEGAL BOUNDARY',
    'hazard_exclusion_map': 'SPATIAL HAZARD & EXCLUSION ZONE MAP',
    'botanical_morphology': 'BOTANICAL DIAGNOSTIC MORPHOLOGY',
    'fungal_anatomy': 'FUNGAL ANATOMICAL CUTAWAY',
    'lookalike_diagnostic': 'DIAGNOSTIC LOOKALIKE CONTRAST PLATE',
    'atlas_crossref_plate': 'CROSS-ZONE REFERENCE & THRESHOLD MATRIX',
    'specimen_doc_plate': 'SPECIMEN VOUCHER & MULTI-VIEW PROTOCOL',
}

_SPECS_CACHE = None


SPEC_KEYS = {
    'v01_artwork': set(),
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
    'canner_vent': set(),
    'correct_vs_wrong': {'correct_title','correct_items','wrong_title','wrong_items','reason','variant'},
    'sequence_plate': {'steps','cue','variant'},
    'system_boundary': {'zone_a','zone_b','barrier','hazard','variant'},
    'escalation_ladder': {'tiers','trigger'},
    'anatomy_zone': {'regions','priority','stop','variant'},
    'seasonal_timeline': {'phases','threshold','variant'},
    'geological_strata': {'strata','note','hazard','variant'},
    'mineral_test_plate': {'tests','scale','hazard','variant'},
    'wildlife_track_plate': {'features','scale','limit','variant'},
    'regulation_boundary': {'authority','checks','prohibition','variant'},
    'hazard_exclusion_map': {'zones','buffer','report','variant'},
    'botanical_morphology': {'features','scale','hold','variant'},
    'fungal_anatomy': {'features','scale','hold','variant'},
    'lookalike_diagnostic': {'target_name','target_traits','toxic_name','toxic_traits','exclusion','variant'},
    'atlas_crossref_plate': {'rows','preserve','variant'},
    'specimen_doc_plate': {'views','voucher','hold','variant'},
}
SPEC_OPTIONAL = {
    'cutaway': {'hazard'},
    'mechanism': {'accent'},
    'correct_vs_wrong': {'reuse_note'},
    'sequence_plate': {'reuse_note'},
    'system_boundary': {'reuse_note'},
    'escalation_ladder': {'reuse_note'},
    'anatomy_zone': {'reuse_note'},
    'seasonal_timeline': {'reuse_note'},
    'geological_strata': {'reuse_note'},
    'mineral_test_plate': {'reuse_note'},
    'wildlife_track_plate': {'reuse_note'},
    'regulation_boundary': {'reuse_note'},
    'hazard_exclusion_map': {'reuse_note'},
    'botanical_morphology': {'reuse_note'},
    'fungal_anatomy': {'reuse_note'},
    'lookalike_diagnostic': {'reuse_note'},
    'atlas_crossref_plate': {'reuse_note'},
    'specimen_doc_plate': {'reuse_note'},
}
SPEC_LIST_LENGTHS = {
    'layers':3,'components':4,'nodes':3,'options':3,'zones':3,'gates':3,
    'correct_items':2,'wrong_items':2,'steps':4,'tiers':3,'regions':3,'phases':4,
    'strata':3,'tests':4,'features':4,'checks':3,'target_traits':2,'toxic_traits':2,
    'rows':3,'views':4,
}


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
            elif key == 'steps':
                for step in value:
                    if not isinstance(step,dict) or set(step) != {'label','detail'} or any(
                        not isinstance(part,str) or not part.strip() for part in step.values()
                    ):
                        raise ValueError(f'Invalid sequence step on {page}')
            elif key == 'tiers':
                for tier in value:
                    if not isinstance(tier,dict) or set(tier) != {'role','scope','action'} or any(
                        not isinstance(part,str) or not part.strip() for part in tier.values()
                    ):
                        raise ValueError(f'Invalid escalation tier on {page}')
            elif key == 'phases':
                for phase in value:
                    if not isinstance(phase,dict) or set(phase) != {'window','focus'} or any(
                        not isinstance(part,str) or not part.strip() for part in phase.values()
                    ):
                        raise ValueError(f'Invalid timeline phase on {page}')
            elif key == 'rows':
                for row in value:
                    if not isinstance(row,dict) or set(row) != {'zones','topic','stop'} or any(
                        not isinstance(part,str) or not part.strip() for part in row.values()
                    ):
                        raise ValueError(f'Invalid atlas matrix row on {page}')
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


def _render_correct_vs_wrong(spec):
    """Side-by-side correct vs incorrect configuration with distinct physical/hazard geometry & grayscale patterns."""
    variant = spec['variant']
    parts = [f'<g id="correct-vs-wrong-{variant}-artwork">']
    # Left panel: CORRECT (solid border, checkmark badge, crisp dark teal header)
    parts.append('<rect x="28" y="38" width="322" height="100" rx="8" fill="#e1ece3" stroke="#184438" stroke-width="2.8"/>')
    parts.append('<rect x="28" y="38" width="322" height="24" rx="6" fill="#184438"/>')
    parts.append('<path d="M40 50l5 5 10-10" fill="none" stroke="#fffdf7" stroke-width="2.5" stroke-linecap="round"/>')
    parts.append(_lbl(spec['correct_title'], 198, 54, 11.5, '#fffdf7'))
    # Variant-specific physical cue on left panel (compact x=38..102)
    if variant == 'electrical':
        parts.append('<rect x="38" y="74" width="32" height="24" rx="4" fill="#c7d8ce" stroke="#184438" stroke-width="2"/>')
        parts.append('<path d="M70 86h12" stroke="#184438" stroke-width="2" marker-end="url(#arrow)"/>')
        parts.append('<rect x="84" y="74" width="18" height="24" rx="3" fill="#fffdf7" stroke="#184438" stroke-width="2"/>')
    elif variant == 'thermal':
        parts.append('<path d="M40 100V78l18-9 18 9v22Z" fill="#cde0d4" stroke="#184438" stroke-width="2"/>')
        parts.append('<path d="M80 86h20" stroke="#2f6b7d" stroke-width="2.5" marker-end="url(#arrow)"/>')
    elif variant == 'canning':
        parts.append('<rect x="44" y="74" width="28" height="32" rx="4" fill="#d3e3ea" stroke="#184438" stroke-width="2"/>')
        parts.append('<path d="M42 74h32M50 69h16" stroke="#184438" stroke-width="3"/>')
        parts.append('<circle cx="88" cy="86" r="9" fill="#fffdf7" stroke="#184438" stroke-width="2"/>')
    elif variant == 'medical':
        parts.append('<circle cx="66" cy="88" r="16" fill="#fffdf7" stroke="#184438" stroke-width="2.2"/>')
        parts.append('<path d="M66 78v20M56 88h20" stroke="#184438" stroke-width="3"/>')
    else:
        parts.append('<polygon points="40,104 62,70 84,104" fill="#cde0d4" stroke="#184438" stroke-width="2.2"/>')
        parts.append('<path d="M84 92h18" stroke="#184438" stroke-width="2.5" marker-end="url(#arrow)"/>')
    parts.append(text(wrap(spec['correct_items'][0], 35)[:2], 112, 79, 13.5, 10.8, 650, '#183c31', 'start'))
    parts.append(text(wrap(spec['correct_items'][1], 35)[:2], 112, 111, 13.5, 10.8, 650, '#183c31', 'start'))

    # Right panel: INCORRECT (dashed double-contrast border, X badge, terracotta header)
    parts.append('<rect x="370" y="38" width="322" height="100" rx="8" fill="#f8ebe3" stroke="#8f381c" stroke-width="2.8" stroke-dasharray="7 4"/>')
    parts.append('<rect x="370" y="38" width="322" height="24" rx="6" fill="#8f381c"/>')
    parts.append('<path d="M382 44l10 10m0-10l-10 10" fill="none" stroke="#fffdf7" stroke-width="2.5" stroke-linecap="round"/>')
    parts.append(_lbl(spec['wrong_title'], 540, 54, 11.5, '#fffdf7'))
    if variant == 'electrical':
        parts.append('<rect x="380" y="74" width="32" height="24" rx="4" fill="#ecd2c5" stroke="#8f381c" stroke-width="2"/>')
        parts.append('<path d="M414 86l12-7-5 12 12-5" fill="none" stroke="#8f381c" stroke-width="2.5"/>')
    elif variant == 'thermal':
        parts.append('<rect x="384" y="74" width="36" height="28" rx="4" fill="#ecd2c5" stroke="#8f381c" stroke-width="2"/>')
        parts.append('<path d="M392 94q10-14 20 0" fill="none" stroke="#8f381c" stroke-width="2.5"/>')
    elif variant == 'canning':
        parts.append('<rect x="386" y="74" width="30" height="32" rx="4" fill="#ecd2c5" stroke="#8f381c" stroke-width="2" stroke-dasharray="4 3"/>')
        parts.append('<path d="M384 74l34 32M418 74l-34 32" stroke="#8f381c" stroke-width="2"/>')
    elif variant == 'medical':
        parts.append('<polygon points="406,70 424,104 388,104" fill="#ecd2c5" stroke="#8f381c" stroke-width="2.2"/>')
        parts.append(_lbl('!', 406, 98, 15, '#8f381c'))
    else:
        parts.append('<path d="M380 96q13-12 26 0t26 0" fill="none" stroke="#8f381c" stroke-width="2.8"/>')
        parts.append('<circle cx="406" cy="80" r="9" fill="#ecd2c5" stroke="#8f381c" stroke-width="2"/>')
    parts.append(text(wrap(spec['wrong_items'][0], 35)[:2], 446, 79, 13.5, 10.8, 650, '#5a2310', 'start'))
    parts.append(text(wrap(spec['wrong_items'][1], 35)[:2], 446, 111, 13.5, 10.8, 650, '#5a2310', 'start'))

    # Bottom causal reason bar
    parts.append('<rect x="28" y="141" width="664" height="17" rx="4" fill="#f5f1e2" stroke="#7c6928"/>')
    parts.append(_lbl(spec['reason'], 360, 153, 10.5, '#3d3312'))
    parts.append('</g>')
    return ''.join(parts)


def _render_sequence_plate(spec):
    """Four-step sequential instructional plate with numbered badges and directional progression."""
    variant = spec['variant']
    steps = spec['steps']
    fills = ['#dce8df', '#e3ece5', '#eef2e4', '#d5e4da']
    parts = [f'<g id="sequence-plate-{variant}-artwork">']
    for i, st in enumerate(steps):
        x = 26 + i * 170
        w = 152
        parts.append(f'<rect x="{x}" y="44" width="{w}" height="90" rx="8" fill="{fills[i]}" stroke="#285345" stroke-width="2.3"/>')
        parts.append(f'<circle cx="{x+18}" cy="58" r="11" fill="#184438"/>')
        parts.append(_lbl(str(i + 1), x + 18, 62, 11.5, '#fffdf7'))
        parts.append(text(wrap(st['label'], 15), x + 35, 58, 13, 11, 700, '#183c31', 'start'))
        parts.append(f'<path d="M{x+10} 78h{w-20}" stroke="#9bb1a3" stroke-width="1.5"/>')
        parts.append(text(wrap(st['detail'], 20), x + w / 2, 95, 13.5, 10.8, 600, '#183c31', 'middle'))
        if i < 3:
            parts.append(f'<path d="M{x+w+2} 89h12" stroke="#184438" stroke-width="3" marker-end="url(#arrow)"/>')
    parts.append('<rect x="26" y="139" width="668" height="18" rx="4" fill="#faeee5" stroke="#a05332"/>')
    parts.append(_lbl(spec['cue'], 360, 152, 10.8, '#642e1e'))
    parts.append('</g>')
    return ''.join(parts)


def _render_system_boundary(spec):
    """Physical system isolation/boundary cutaway with domain-specific architectural geometry."""
    variant = spec['variant']
    parts = [f'<g id="system-boundary-{variant}-artwork">']
    if variant == 'panel_gen':
        # House panel left, transfer-switch isolation gap center, outdoor generator right
        parts.append('<rect x="34" y="46" width="196" height="84" rx="7" fill="#dce8df" stroke="#184438" stroke-width="2.8"/>')
        parts.append('<rect x="50" y="64" width="28" height="46" rx="3" fill="#fffdf7" stroke="#184438" stroke-width="2"/>')
        parts.append('<path d="M234 88h92" stroke="#184438" stroke-width="3" stroke-dasharray="6 4"/>')
        parts.append('<rect x="330" y="54" width="60" height="68" rx="6" fill="#f5f1e2" stroke="#7c6928" stroke-width="2.5"/>')
        parts.append('<path d="M394 88h92" stroke="#8f381c" stroke-width="3" stroke-dasharray="6 4"/>')
        parts.append('<rect x="490" y="46" width="196" height="84" rx="7" fill="#f7e6dc" stroke="#8f381c" stroke-width="2.8"/>')
    elif variant == 'well_septic':
        # Ground slope with upland cased well left, separation barrier center, flood/septic zone right
        parts.append('<path d="M30 84L260 88L460 112L690 116V134H30Z" fill="#c9d5b8" stroke="#4f6549" stroke-width="2.2"/>')
        parts.append('<rect x="92" y="46" width="22" height="82" fill="#d3e3ea" stroke="#184438" stroke-width="2.5"/>')
        parts.append('<path d="M360 44v90" stroke="#8f381c" stroke-width="3.5" stroke-dasharray="7 5"/>')
        parts.append('<rect x="492" y="92" width="170" height="32" rx="5" fill="#d9c6b0" stroke="#8f381c" stroke-width="2.2"/>')
    elif variant == 'canning_pressure':
        # Pressure vessel cutaway with lid lock, dial/weighted gauge, jar rack & headspace
        parts.append('<rect x="44" y="50" width="206" height="82" rx="8" fill="#dbe6ea" stroke="#184438" stroke-width="3"/>')
        parts.append('<path d="M40 50h214" stroke="#184438" stroke-width="6"/>')
        parts.append('<circle cx="147" cy="44" r="9" fill="#fffdf7" stroke="#184438" stroke-width="2"/>')
        parts.append('<rect x="280" y="54" width="160" height="74" rx="6" fill="#f5f1e2" stroke="#7c6928" stroke-width="2.5"/>')
        parts.append('<rect x="470" y="50" width="206" height="82" rx="8" fill="#faeee5" stroke="#8f381c" stroke-width="2.8"/>')
    elif variant == 'cold_chain':
        # Cold insulated zone left, thermal boundary door seal center, danger zone right
        parts.append('<rect x="34" y="46" width="210" height="84" rx="8" fill="#d4e5ec" stroke="#245368" stroke-width="3"/>')
        parts.append('<rect x="276" y="46" width="168" height="84" rx="6" fill="#f5f1e2" stroke="#7c6928" stroke-width="2.5"/>')
        parts.append('<rect x="476" y="46" width="210" height="84" rx="8" fill="#f7e6dc" stroke="#8f381c" stroke-width="3"/>')
    else:
        # Interior shelter safe zone vs exterior hazard wall
        parts.append('<rect x="34" y="46" width="210" height="84" rx="8" fill="#dce8df" stroke="#184438" stroke-width="3"/>')
        parts.append('<rect x="276" y="46" width="168" height="84" rx="6" fill="#eef1e6" stroke="#4f6c5d" stroke-width="2.5"/>')
        parts.append('<rect x="476" y="46" width="210" height="84" rx="8" fill="#f7e6dc" stroke="#8f381c" stroke-width="3"/>')

    # Crisp legible zone callout pills placed cleanly with zero overlap
    parts.append('<rect x="42" y="58" width="194" height="58" rx="5" fill="#fffdf7" fill-opacity="0.88" stroke="#184438"/>')
    parts.append(text(wrap(spec['zone_a'], 22), 139, 82, 14, 11.2, 700, '#183c31', 'middle'))
    parts.append('<rect x="264" y="60" width="192" height="54" rx="5" fill="#fffdf7" fill-opacity="0.92" stroke="#7c6928"/>')
    parts.append(text(wrap(spec['barrier'], 22), 360, 82, 14, 11.2, 700, '#3d3312', 'middle'))
    parts.append('<rect x="484" y="58" width="194" height="58" rx="5" fill="#fffdf7" fill-opacity="0.88" stroke="#8f381c"/>')
    parts.append(text(wrap(spec['zone_b'], 22), 581, 82, 14, 11.2, 700, '#642e1e', 'middle'))
    parts.append('<rect x="34" y="138" width="652" height="19" rx="4" fill="#faeee5" stroke="#a05332"/>')
    parts.append(_lbl(spec['hazard'], 360, 151, 10.8, '#642e1e'))
    parts.append('</g>')
    return ''.join(parts)


def _render_escalation_ladder(spec):
    """Three-tier stepped scope-of-practice or emergency warning escalation ladder."""
    tiers = spec['tiers']
    fills = ['#e1ece3', '#f4efd8', '#f6e1d7']
    strokes = ['#184438', '#7c6928', '#8f381c']
    text_fills = ['#183c31', '#3d3312', '#642e1e']
    parts = ['<g id="escalation-ladder-artwork">']
    for i, tier in enumerate(tiers):
        x = 30 + i * 224
        y = 58 - i * 9
        h = 76 + i * 9
        parts.append(f'<rect x="{x}" y="{y}" width="206" height="{h}" rx="7" fill="{fills[i]}" stroke="{strokes[i]}" stroke-width="2.6"/>')
        parts.append(f'<rect x="{x}" y="{y}" width="206" height="22" rx="5" fill="{strokes[i]}"/>')
        parts.append(_lbl(tier['role'], x + 103, y + 15, 11, '#fffdf7'))
        parts.append(_lbl(tier['scope'], x + 103, y + 36, 10.6, text_fills[i]))
        parts.append(text(wrap(tier['action'], 27)[:2], x + 103, y + 52, 13, 10.5, 650, text_fills[i], 'middle'))
        if i < 2:
            parts.append(f'<path d="M{x+208} {y+28}l12-8" stroke="{strokes[i+1]}" stroke-width="3" marker-end="url(#arrow)"/>')
    parts.append('<rect x="30" y="139" width="660" height="18" rx="4" fill="#faeee5" stroke="#a05332"/>')
    parts.append(_lbl(spec['trigger'], 360, 152, 10.8, '#642e1e'))
    parts.append('</g>')
    return ''.join(parts)


def _render_anatomy_zone(spec):
    """Conceptual orientation and care-zone schematic (explicitly non-diagnostic)."""
    variant = spec['variant']
    regions = spec['regions']
    parts = [f'<g id="anatomy-zone-{variant}-artwork">']
    # Left conceptual silhouette/zone schematic box
    parts.append('<rect x="28" y="42" width="176" height="94" rx="8" fill="#e6eee8" stroke="#285345" stroke-width="2.4"/>')
    if variant == 'airway_bleed':
        parts.append('<circle cx="116" cy="60" r="11" fill="#fffdf7" stroke="#184438" stroke-width="2.2"/>')
        parts.append('<rect x="96" y="75" width="40" height="36" rx="8" fill="#cde0d4" stroke="#184438" stroke-width="2.2"/>')
        parts.append('<path d="M96 84L72 104M136 84l24 20M106 111v20M126 111v20" stroke="#184438" stroke-width="3" stroke-linecap="round"/>')
        parts.append('<circle cx="136" cy="92" r="5" fill="#8f381c"/>')
    elif variant == 'thermal_core':
        parts.append('<ellipse cx="116" cy="89" rx="44" ry="34" fill="#d4e5ec" stroke="#245368" stroke-width="2.2" stroke-dasharray="5 3"/>')
        parts.append('<ellipse cx="116" cy="89" rx="22" ry="18" fill="#e9c89f" stroke="#8f381c" stroke-width="2.5"/>')
        parts.append(_lbl('CORE', 116, 93, 10.5, '#642e1e'))
    elif variant == 'limb_splint':
        parts.append('<path d="M52 89h128" stroke="#184438" stroke-width="10" stroke-linecap="round"/>')
        parts.append('<rect x="64" y="74" width="104" height="30" rx="5" fill="none" stroke="#8f381c" stroke-width="2.5" stroke-dasharray="6 3"/>')
        parts.append('<circle cx="80" cy="89" r="6" fill="#fffdf7" stroke="#184438" stroke-width="2"/>')
        parts.append('<circle cx="152" cy="89" r="6" fill="#fffdf7" stroke="#184438" stroke-width="2"/>')
    else:
        parts.append('<circle cx="116" cy="89" r="32" fill="#f7e6dc" stroke="#8f381c" stroke-width="2.4"/>')
        parts.append('<circle cx="116" cy="89" r="14" fill="#fffdf7" stroke="#184438" stroke-width="2"/>')
        parts.append('<path d="M116 57v64M84 89h64" stroke="#73877b" stroke-width="1.5" stroke-dasharray="4 3"/>')

    # Right three structured priority/orientation zones
    for i, reg in enumerate(regions):
        y = 42 + i * 32
        parts.append(f'<rect x="218" y="{y}" width="474" height="27" rx="5" fill="#f9faef" stroke="#4f6c5d" stroke-width="1.8"/>')
        parts.append(f'<rect x="218" y="{y}" width="26" height="27" rx="4" fill="#184438"/>')
        parts.append(_lbl(str(i + 1), 231, y + 18, 11, '#fffdf7'))
        parts.append(_lbl(reg, 254, y + 18, 11.2, '#183c31', 'start'))
    parts.append('<rect x="28" y="139" width="324" height="18" rx="4" fill="#dceadf" stroke="#184438"/>')
    parts.append(_lbl(spec['priority'], 190, 152, 10.5, '#183c31'))
    parts.append('<rect x="364" y="139" width="328" height="18" rx="4" fill="#faeee5" stroke="#a05332"/>')
    parts.append(_lbl(spec['stop'], 528, 152, 10.5, '#642e1e'))
    parts.append('</g>')
    return ''.join(parts)


def _render_seasonal_timeline(spec):
    """Physically meaningful time, temperature, or seasonal progression bar."""
    variant = spec['variant']
    phases = spec['phases']
    fills = ['#d5e5dc', '#e4ebd4', '#f4ebd2', '#f5dfd5']
    parts = [f'<g id="seasonal-timeline-{variant}-artwork">']
    # Horizontal timeline spine
    parts.append('<path d="M36 62h644" stroke="#184438" stroke-width="4" marker-end="url(#arrow)"/>')
    for i, ph in enumerate(phases):
        x = 28 + i * 168
        w = 156
        cx = x + w / 2
        parts.append(f'<circle cx="{cx}" cy="62" r="8" fill="#184438" stroke="#fffdf7" stroke-width="2"/>')
        parts.append(_lbl(ph['window'], cx, 48, 11, '#183c31'))
        parts.append(f'<rect x="{x}" y="76" width="{w}" height="58" rx="6" fill="{fills[i]}" stroke="#315245" stroke-width="2"/>')
        parts.append(text(wrap(ph['focus'], 20), cx, 98, 14, 11, 650, '#183c31', 'middle'))
    parts.append('<rect x="28" y="139" width="664" height="18" rx="4" fill="#faeee5" stroke="#a05332"/>')
    parts.append(_lbl(spec['threshold'], 360, 152, 10.8, '#642e1e'))
    parts.append('</g>')
    return ''.join(parts)


def _render_canner_vent(_spec):
    """Show steam leaving an open vent before the canner is pressurized."""
    return ''.join([
        '<g id="canner-vent-artwork">',
        '<path d="M45 72H350V116Q350 142 325 142H70Q45 142 45 116Z" '
        'fill="#f5f5ea" stroke="#315245" stroke-width="3"/>',
        '<path d="M49 126Q103 121 158 126T268 126T346 126V131L335 140H58L49 132Z" '
        'fill="#bddce3"/>',
        '<path d="M64 128H331" stroke="#315245" stroke-width="2"/>',
        '<path d="M95 126V101Q95 96 101 96H128Q134 96 134 101V126 '
        'M167 126V101Q167 96 173 96H200Q206 96 206 101V126 '
        'M239 126V101Q239 96 245 96H272Q278 96 278 101V126" '
        'fill="#e1eee3" stroke="#315245" stroke-width="2"/>',
        '<path d="M86 72Q103 57 167 57H214Q280 57 307 72M189 57V48H202V57" '
        'fill="none" stroke="#315245" stroke-width="3"/>',
        '<path d="M195 94V77M195 63V32" stroke="#24829b" stroke-width="3" '
        'stroke-dasharray="4 3" marker-end="url(#arrow)"/>',
        '<path d="M204 49h136l25-5M280 100h80M346 133h14" fill="none" '
        'stroke="#697f73" stroke-width="1.5"/>',
        _lbl('Open vent: steam exits before pressurizing', 374, 48, 12, anchor='start'),
        _lbl('Jars stand on rack above the base', 374, 104, 12, anchor='start'),
        _lbl('Use specified water depth and loading', 374, 137, 12, anchor='start'),
        '</g>',
    ])


def _render_geological_strata(spec):
    """Geological cross-section, fracture geometry, soil horizon, or wood-grain plate."""
    variant = spec['variant']
    strata = spec['strata']
    parts = [f'<g id="geological-strata-{variant}-artwork">']
    parts.append('<rect x="28" y="38" width="236" height="96" rx="6" fill="#f7f4ea" stroke="#2c4b3f" stroke-width="2.2"/>')
    if variant == 'fracture':
        # Conchoidal fracture ripples vs planar cleavage
        parts.append('<path d="M48 118L84 52L152 48L188 94L138 122Z" fill="#bfc8bf" stroke="#183c31" stroke-width="2.2"/>')
        parts.append('<path d="M90 64q24 14 48 2M82 80q32 16 64 2M76 96q36 16 70 0" fill="none" stroke="#315245" stroke-width="1.8"/>')
        parts.append('<path d="M196 54h52v62h-52Z" fill="#dcd6c4" stroke="#6d5c42" stroke-width="2" stroke-dasharray="5 3"/>')
        parts.append('<path d="M196 74h52M196 94h52" stroke="#6d5c42" stroke-width="1.8"/>')
    elif variant == 'clay_soil':
        # Soil horizons O/A/B/C with drainage arrows
        parts.append('<rect x="32" y="42" width="228" height="20" fill="#8b7a5e"/>')
        parts.append('<rect x="32" y="62" width="228" height="28" fill="#b79c73"/>')
        parts.append('<rect x="32" y="90" width="228" height="22" fill="#9a8d82"/>')
        parts.append('<rect x="32" y="112" width="228" height="18" fill="#c7c4ba" stroke-dasharray="4 3"/>')
        parts.append('<path d="M62 46v78M142 46v78M222 46v78" stroke="#245368" stroke-width="2" stroke-dasharray="4 3" marker-end="url(#arrow)"/>')
    elif variant == 'wood_grain':
        # Wood cross-section rings, radial checks, and bast fiber bark layers
        parts.append('<circle cx="94" cy="86" r="38" fill="#d9c094" stroke="#4f3c24" stroke-width="2.6"/>')
        parts.append('<circle cx="94" cy="86" r="27" fill="none" stroke="#7c5e3a" stroke-width="1.6"/>')
        parts.append('<circle cx="94" cy="86" r="16" fill="none" stroke="#7c5e3a" stroke-width="1.6"/>')
        parts.append('<path d="M94 86l36-14M154 50h96v72h-96Z" fill="#e9dec7" stroke="#4f3c24" stroke-width="2"/>')
        parts.append('<path d="M162 54v64M178 54v64M194 54v64M210 54v64M226 54v64" stroke="#7c5e3a" stroke-width="1.6"/>')
    elif variant == 'dust_hazard':
        # Airborne silica / fiber plume + eye & respiratory exclusion boundary
        parts.append('<path d="M46 118l44-24 26 24Z" fill="#9ea39b" stroke="#263d35" stroke-width="2"/>')
        parts.append('<circle cx="118" cy="76" r="22" fill="#f2d6cc" stroke="#8f381c" stroke-width="2.2" stroke-dasharray="4 3"/>')
        parts.append('<circle cx="152" cy="64" r="16" fill="#f7e4dc" stroke="#8f381c" stroke-width="1.8" stroke-dasharray="3 3"/>')
        parts.append('<path d="M194 48v76" stroke="#8f381c" stroke-width="3" stroke-dasharray="6 4"/>')
        parts.append(_lbl('PPE', 228, 90, 11, '#183c31'))
    else:
        # Upper Midwest stratified glacial drift over Paleozoic sedimentary over Precambrian shield
        parts.append('<path d="M32 64q56-10 114 0t114-4v22H32Z" fill="#c7d1b6" stroke="#315245" stroke-width="1.5"/>')
        parts.append('<path d="M32 86h228v22H32Z" fill="#d9cba8" stroke="#6d5c42" stroke-width="1.5"/>')
        parts.append('<path d="M32 108h228v22H32Z" fill="#9ea5a0" stroke="#263d35" stroke-width="1.8"/>')
        parts.append('<path d="M52 108l14 22M106 108l14 22M160 108l14 22M214 108l14 22" stroke="#263d35" stroke-width="1.4"/>')
    # Scale bar inside graphic
    parts.append('<path d="M38 128h46M38 124v8M84 124v8" stroke="#183c31" stroke-width="1.8"/>')
    for i, layer in enumerate(strata):
        y = 38 + i * 33
        parts.append(f'<rect x="278" y="{y}" width="414" height="28" rx="5" fill="#f9faef" stroke="#4f6c5d" stroke-width="1.8"/>')
        parts.append(f'<rect x="278" y="{y}" width="26" height="28" rx="4" fill="#184438"/>')
        parts.append(_lbl(str(i + 1), 291, y + 18, 11, '#fffdf7'))
        parts.append(_lbl(layer, 314, y + 18, 11, '#183c31', 'start'))
    parts.append('<rect x="28" y="139" width="320" height="18" rx="4" fill="#dceadf" stroke="#184438"/>')
    parts.append(_lbl(spec['note'], 188, 152, 10.4, '#183c31'))
    parts.append('<rect x="358" y="139" width="334" height="18" rx="4" fill="#faeee5" stroke="#a05332"/>')
    parts.append(_lbl(spec['hazard'], 525, 152, 10.4, '#642e1e'))
    parts.append('</g>')
    return ''.join(parts)


def _render_mineral_test_plate(spec):
    """Non-destructive field mineral observation grid with Mohs reference bar."""
    variant = spec['variant']
    tests = spec['tests']
    parts = [f'<g id="mineral-test-{variant}-artwork">']
    # Left Mohs hardness / property ladder
    parts.append('<rect x="28" y="38" width="164" height="96" rx="6" fill="#eef3ee" stroke="#285345" stroke-width="2.2"/>')
    parts.append('<path d="M46 56h128M46 76h128M46 96h128M46 116h128" stroke="#6f8c7a" stroke-width="2"/>')
    for idx, tag in enumerate(('1-2 Soft', '3-5 Mid', '6-7 Quartz', '8-10 Hard')):
        parts.append(f'<rect x="36" y="{44 + idx * 20}" width="{22 + idx * 18}" height="10" rx="2" fill="#315245" opacity="{0.45 + idx * 0.16:.2f}"/>')
        parts.append(_lbl(tag, 186, 53 + idx * 20, 9.4, '#183c31', 'end'))
    # Right 2x2 non-destructive observation grid
    for i, item in enumerate(tests):
        col, row = i % 2, i // 2
        x = 206 + col * 246
        y = 38 + row * 50
        parts.append(f'<rect x="{x}" y="{y}" width="236" height="44" rx="6" fill="#f9faef" stroke="#4f6c5d" stroke-width="1.8"/>')
        parts.append(f'<rect x="{x}" y="{y}" width="24" height="44" rx="4" fill="#285345"/>')
        parts.append(_lbl(str(i + 1), x + 12, y + 26, 11, '#fffdf7'))
        parts.append(text(wrap(item, 27)[:2], x + 32, y + 18, 14, 10.6, 650, '#183c31', 'start'))
    parts.append('<rect x="28" y="139" width="290" height="18" rx="4" fill="#dceadf" stroke="#184438"/>')
    parts.append(_lbl(spec['scale'], 173, 152, 10.4, '#183c31'))
    parts.append('<rect x="328" y="139" width="364" height="18" rx="4" fill="#faeee5" stroke="#a05332"/>')
    parts.append(_lbl(spec['hazard'], 510, 152, 10.4, '#642e1e'))
    parts.append('</g>')
    return ''.join(parts)


def _render_wildlife_track_plate(spec):
    """Wildlife track/gait/fish anatomy/habitat observation plate with scale ruler."""
    variant = spec['variant']
    features = spec['features']
    parts = [f'<g id="wildlife-track-{variant}-artwork">']
    parts.append('<rect x="28" y="38" width="206" height="96" rx="6" fill="#f6f4eb" stroke="#2c4b3f" stroke-width="2.2"/>')
    if variant == 'tracks':
        # Conceptual paw pad + toe pads + cloven hoof comparison with ruler
        parts.append('<ellipse cx="82" cy="96" rx="16" ry="12" fill="#4f6c5d"/>')
        for tx, ty in ((62, 74), (75, 64), (91, 64), (102, 74)):
            parts.append(f'<ellipse cx="{tx}" cy="{ty}" rx="6" ry="9" fill="#315245"/>')
        parts.append('<path d="M148 112c-12-16-8-42 6-52c4 14 4 38-6 52ZM176 112c12-16 8-42-6-52c-4 14-4 38 6 52Z" fill="#5e4b35"/>')
    elif variant == 'fish_anatomy':
        # Conceptual freshwater fish silhouette with dorsal/adipose/caudal fins & lateral line
        parts.append('<path d="M52 86q56-34 114-4l30-18-10 22 10 22-30-18q-58 30-114-4Z" fill="#b7d2d9" stroke="#183c31" stroke-width="2.2"/>')
        parts.append('<path d="M88 64l28-14 14 14M74 86q42-4 82 0" fill="none" stroke="#315245" stroke-width="2" stroke-dasharray="4 3"/>')
        parts.append('<circle cx="72" cy="82" r="3.5" fill="#183c31"/>')
    elif variant == 'habitat_layers':
        # Upland forest -> riparian edge -> littoral shelf -> deep basin transect
        parts.append('<path d="M32 76L94 82L152 108L230 120V130H32Z" fill="#c7d4b6" stroke="#315245" stroke-width="1.8"/>')
        parts.append('<path d="M126 94H230V120L152 108Z" fill="#a8cad4" opacity="0.8"/>')
        parts.append('<path d="M54 76V52M46 64l8-14 8 14M74 78V56M66 68l8-14 8 14" stroke="#184438" stroke-width="2" fill="none"/>')
    elif variant == 'field_hygiene':
        # Clean knife/gloves -> cold chain <= 40 F -> safe internal cook temp
        parts.append('<rect x="42" y="54" width="52" height="58" rx="5" fill="#dceadf" stroke="#184438" stroke-width="2"/>')
        parts.append('<path d="M96 83h24" stroke="#184438" stroke-width="2.5" marker-end="url(#arrow)"/>')
        parts.append('<rect x="124" y="54" width="96" height="58" rx="5" fill="#d9e8ef" stroke="#245368" stroke-width="2"/>')
        parts.append(_lbl('COOL', 172, 78, 11, '#183c31'))
        parts.append(_lbl('CLEAN', 68, 86, 10.5, '#183c31'))
    else:
        # Gait trail straddle & stride diagram
        for gx, gy in ((52, 108), (86, 68), (124, 108), (160, 68), (196, 108)):
            parts.append(f'<circle cx="{gx}" cy="{gy}" r="8" fill="#315245"/>')
        parts.append('<path d="M52 108h144M52 68h144" stroke="#8f381c" stroke-width="1.5" stroke-dasharray="4 3"/>')
    # Metric/inch scale ticks along bottom of left plate
    parts.append('<path d="M38 126h100M38 121v8M63 123v6M88 121v8M113 123v6M138 121v8" stroke="#183c31" stroke-width="1.6"/>')
    for i, feat in enumerate(features):
        col, row = i % 2, i // 2
        x = 248 + col * 224
        y = 38 + row * 50
        parts.append(f'<rect x="{x}" y="{y}" width="216" height="44" rx="5" fill="#f9faef" stroke="#4f6c5d" stroke-width="1.8"/>')
        parts.append(f'<rect x="{x}" y="{y}" width="22" height="44" rx="4" fill="#184438"/>')
        parts.append(_lbl(str(i + 1), x + 11, y + 26, 10.6, '#fffdf7'))
        parts.append(text(wrap(feat, 25)[:2], x + 28, y + 18, 14, 10.4, 650, '#183c31', 'start'))
    parts.append('<rect x="28" y="139" width="290" height="18" rx="4" fill="#dceadf" stroke="#184438"/>')
    parts.append(_lbl(spec['scale'], 173, 152, 10.4, '#183c31'))
    parts.append('<rect x="328" y="139" width="364" height="18" rx="4" fill="#faeee5" stroke="#a05332"/>')
    parts.append(_lbl(spec['limit'], 510, 152, 10.4, '#642e1e'))
    parts.append('</g>')
    return ''.join(parts)


def _render_regulation_boundary(spec):
    """Jurisdiction, authority, season, and no-emergency-exemption verification schematic."""
    variant = spec['variant']
    checks = spec['checks']
    parts = [f'<g id="regulation-boundary-{variant}-artwork">']
    parts.append('<rect x="28" y="38" width="200" height="96" rx="7" fill="#184438" stroke="#183c31" stroke-width="2"/>')
    parts.append(_lbl('AUTHORITY GATE', 128, 60, 11, '#dceadf'))
    parts.append(text(wrap(spec['authority'], 21)[:3], 128, 82, 16, 11.5, 700, '#fffdf7', 'middle'))
    parts.append('<path d="M230 86h20" stroke="#184438" stroke-width="3" marker-end="url(#arrow)"/>')
    for i, chk in enumerate(checks):
        y = 38 + i * 33
        parts.append(f'<rect x="256" y="{y}" width="436" height="28" rx="5" fill="#f9faef" stroke="#315245" stroke-width="1.8"/>')
        parts.append(f'<rect x="256" y="{y}" width="26" height="28" rx="4" fill="#2b5d4e"/>')
        parts.append(_lbl(str(i + 1), 269, y + 18, 10.8, '#fffdf7'))
        parts.append(_lbl(chk, 292, y + 18, 10.8, '#183c31', 'start'))
    parts.append('<rect x="28" y="139" width="664" height="18" rx="4" fill="#f7dfd6" stroke="#8f381c" stroke-width="1.6"/>')
    parts.append(_lbl(spec['prohibition'], 360, 152, 10.6, '#642e1e'))
    parts.append('</g>')
    return ''.join(parts)


def _render_hazard_exclusion_map(spec):
    """Overhead spatial hazard/exclusion-zone map with compass cue and reporting bar."""
    variant = spec['variant']
    zones = spec['zones']
    parts = [f'<g id="hazard-exclusion-{variant}-artwork">']
    # Left overhead concentric / corridor hazard map
    parts.append('<rect x="28" y="38" width="224" height="96" rx="6" fill="#eef3ec" stroke="#285345" stroke-width="2.2"/>')
    if variant == 'trapping_corridor':
        parts.append('<path d="M36 96q68-22 140 6t68-14" fill="none" stroke="#5b8fa1" stroke-width="10"/>')
        parts.append('<path d="M36 62h208" stroke="#6f8c7a" stroke-width="4" stroke-dasharray="6 4"/>')
        parts.append('<circle cx="136" cy="88" r="18" fill="#f5d9cf" stroke="#8f381c" stroke-width="2.2" stroke-dasharray="4 3"/>')
        parts.append(_lbl('HAZARD', 136, 92, 9.6, '#642e1e'))
    elif variant == 'pet_leash':
        parts.append('<path d="M36 86h208" stroke="#285345" stroke-width="6"/>')
        parts.append('<rect x="36" y="42" width="208" height="24" fill="#f5dfd5" stroke="#8f381c" stroke-dasharray="5 3"/>')
        parts.append('<rect x="36" y="106" width="208" height="24" fill="#f5dfd5" stroke="#8f381c" stroke-dasharray="5 3"/>')
        parts.append(_lbl('ON-LEASH TRAIL', 140, 90, 9.8, '#fffdf7'))
    else:
        parts.append('<circle cx="140" cy="86" r="40" fill="#dceadf" stroke="#285345" stroke-width="2"/>')
        parts.append('<circle cx="140" cy="86" r="24" fill="#f5e6c8" stroke="#7c6928" stroke-width="2" stroke-dasharray="5 3"/>')
        parts.append('<circle cx="140" cy="86" r="10" fill="#d97254" stroke="#8f381c" stroke-width="2"/>')
    # North arrow cue
    parts.append('<path d="M44 62V44" stroke="#183c31" stroke-width="2" marker-end="url(#arrow)"/>')
    parts.append(_lbl('N', 54, 52, 10, '#183c31'))
    for i, z in enumerate(zones):
        y = 38 + i * 33
        parts.append(f'<rect x="266" y="{y}" width="426" height="28" rx="5" fill="#f9faef" stroke="#4f6c5d" stroke-width="1.8"/>')
        parts.append(f'<rect x="266" y="{y}" width="26" height="28" rx="4" fill="{"#8f381c" if i == 0 else "#285345"}"/>')
        parts.append(_lbl(str(i + 1), 279, y + 18, 10.8, '#fffdf7'))
        parts.append(_lbl(z, 302, y + 18, 10.8, '#183c31', 'start'))
    parts.append('<rect x="28" y="139" width="318" height="18" rx="4" fill="#dceadf" stroke="#184438"/>')
    parts.append(_lbl(spec['buffer'], 187, 152, 10.4, '#183c31'))
    parts.append('<rect x="356" y="139" width="336" height="18" rx="4" fill="#faeee5" stroke="#a05332"/>')
    parts.append(_lbl(spec['report'], 524, 152, 10.4, '#642e1e'))
    parts.append('</g>')
    return ''.join(parts)


def _render_botanical_morphology(spec):
    """Conceptual botanical anatomy cutaway (leaves, umbel/roots, berries, trees) with HOLD bar."""
    variant = spec['variant']
    features = spec['features']
    parts = [f'<g id="botanical-morphology-{variant}-artwork">']
    parts.append('<rect x="28" y="38" width="206" height="96" rx="6" fill="#f6f7ef" stroke="#2c4b3f" stroke-width="2.2"/>')
    if variant == 'umbel_root':
        # Compound umbel + hollow/chambered root cutaway
        parts.append('<path d="M90 122V66M90 66l-28-14M90 66l-10-18M90 66l10-18M90 66l28-14" stroke="#285345" stroke-width="2.2"/>')
        for cx in (62, 80, 100, 118):
            parts.append(f'<circle cx="{cx}" cy="49" r="5" fill="#dceadf" stroke="#285345" stroke-width="1.5"/>')
        parts.append('<path d="M168 54c-16 14-14 48 0 68c14-20 16-54 0-68Z" fill="#e6d9be" stroke="#5e4b35" stroke-width="2.2"/>')
        parts.append('<path d="M158 72h20M156 86h24M158 100h20" stroke="#8f381c" stroke-width="2"/>')
    elif variant == 'berry_shrub':
        # Branch + alternate leaves + multi-seeded drupe/berry cluster + calyx
        parts.append('<path d="M44 114L176 54" stroke="#5e4b35" stroke-width="3.2"/>')
        parts.append('<ellipse cx="86" cy="70" rx="20" ry="9" transform="rotate(-35 86 70)" fill="#94b698" stroke="#184438" stroke-width="1.8"/>')
        parts.append('<ellipse cx="134" cy="96" rx="20" ry="9" transform="rotate(28 134 96)" fill="#94b698" stroke="#184438" stroke-width="1.8"/>')
        for bx, by in ((164, 68), (182, 74), (172, 88), (192, 86)):
            parts.append(f'<circle cx="{bx}" cy="{by}" r="7.5" fill="#4f3d59" stroke="#183c31" stroke-width="1.6"/>')
    elif variant == 'tree_nut':
        # Needle fascicle / lobed leaf + armored nut/acorn cap
        parts.append('<path d="M74 116V56M74 86l-24-18M74 86l24-18M74 70l-18-16M74 70l18-16" stroke="#184438" stroke-width="2.4"/>')
        parts.append('<path d="M150 74h48q0-18-24-20q-24 2-24 20Z" fill="#7c6345" stroke="#3d2e1e" stroke-width="2"/>')
        parts.append('<path d="M154 74h40v20q0 20-20 26q-20-6-20-26Z" fill="#d9be92" stroke="#3d2e1e" stroke-width="2"/>')
    elif variant == 'phenology':
        # 4 seasonal life stages: shoot -> flower -> fruit -> dormant twig
        for idx, (x, h) in enumerate(((56, 22), (102, 42), (148, 48), (194, 34))):
            parts.append(f'<path d="M{x} 118v-{h}" stroke="#285345" stroke-width="2.6"/>')
            parts.append(f'<circle cx="{x}" cy="{118 - h}" r="{5 + (idx % 2) * 3}" fill="{"#94b698" if idx < 2 else "#8f381c"}" stroke="#183c31"/>')
    else:
        # Opposite vs alternate leaf arrangement on stems
        parts.append('<path d="M78 120V48" stroke="#285345" stroke-width="3"/>')
        parts.append('<ellipse cx="56" cy="70" rx="16" ry="7" fill="#94b698" stroke="#184438"/>')
        parts.append('<ellipse cx="100" cy="70" rx="16" ry="7" fill="#94b698" stroke="#184438"/>')
        parts.append('<ellipse cx="56" cy="98" rx="16" ry="7" fill="#94b698" stroke="#184438"/>')
        parts.append('<ellipse cx="100" cy="98" rx="16" ry="7" fill="#94b698" stroke="#184438"/>')
        parts.append('<path d="M168 120V48" stroke="#285345" stroke-width="3"/>')
        parts.append('<ellipse cx="146" cy="64" rx="16" ry="7" fill="#c7d4b6" stroke="#184438"/>')
        parts.append('<ellipse cx="190" cy="84" rx="16" ry="7" fill="#c7d4b6" stroke="#184438"/>')
        parts.append('<ellipse cx="146" cy="104" rx="16" ry="7" fill="#c7d4b6" stroke="#184438"/>')
    parts.append('<path d="M38 127h72M38 123v7M74 123v7M110 123v7" stroke="#183c31" stroke-width="1.6"/>')
    for i, feat in enumerate(features):
        col, row = i % 2, i // 2
        x = 248 + col * 224
        y = 38 + row * 50
        parts.append(f'<rect x="{x}" y="{y}" width="216" height="44" rx="5" fill="#f9faef" stroke="#4f6c5d" stroke-width="1.8"/>')
        parts.append(f'<rect x="{x}" y="{y}" width="22" height="44" rx="4" fill="#184438"/>')
        parts.append(_lbl(str(i + 1), x + 11, y + 26, 10.6, '#fffdf7'))
        parts.append(text(wrap(feat, 25)[:2], x + 28, y + 18, 14, 10.4, 650, '#183c31', 'start'))
    parts.append('<rect x="28" y="139" width="276" height="18" rx="4" fill="#dceadf" stroke="#184438"/>')
    parts.append(_lbl(spec['scale'], 166, 152, 10.3, '#183c31'))
    parts.append('<rect x="314" y="139" width="378" height="18" rx="4" fill="#f7dfd6" stroke="#8f381c" stroke-width="1.6"/>')
    parts.append(_lbl(spec['hold'], 503, 152, 10.3, '#642e1e'))
    parts.append('</g>')
    return ''.join(parts)


def _render_fungal_anatomy(spec):
    """Conceptual mushroom anatomical cross-section (cap, gills/pores, annulus, volva, substrate)."""
    variant = spec['variant']
    features = spec['features']
    parts = [f'<g id="fungal-anatomy-{variant}-artwork">']
    parts.append('<rect x="28" y="38" width="206" height="96" rx="6" fill="#f7f4ec" stroke="#2c4b3f" stroke-width="2.2"/>')
    if variant == 'morel_cutaway':
        # True hollow morel cutaway vs chambered/stuffed false morel
        parts.append('<path d="M78 46c-18 8-22 30-14 48h28c8-18 4-40-14-48Z" fill="#c9b896" stroke="#4f3c24" stroke-width="2"/>')
        parts.append('<path d="M78 54c-8 6-10 22-6 36h12c4-14 2-30-6-36Z" fill="#fffdf7" stroke="#4f3c24" stroke-width="1.6"/>')
        parts.append('<rect x="69" y="94" width="18" height="28" fill="#fffdf7" stroke="#4f3c24" stroke-width="2"/>')
        parts.append('<path d="M168 48c-22 6-24 28-14 40h28c10-12 8-34-14-40Z" fill="#a6684b" stroke="#642e1e" stroke-width="2"/>')
        parts.append('<path d="M158 64h20M156 76h24M162 88v32M174 88v32" stroke="#642e1e" stroke-width="2"/>')
    elif variant == 'polypore_tooth':
        # Shelf bracket polypore on deadwood substrate showing pore underside
        parts.append('<rect x="44" y="44" width="26" height="82" fill="#8b7152" stroke="#3d2e1e" stroke-width="2"/>')
        parts.append('<path d="M70 64q66-14 116 14q-24 18-116 14Z" fill="#d9a66c" stroke="#5e3d1e" stroke-width="2.2"/>')
        parts.append('<path d="M76 84h98" stroke="#5e3d1e" stroke-width="2" stroke-dasharray="2 3"/>')
        parts.append('<path d="M70 98q48-6 84 10q-16 12-84 8Z" fill="#c9935b" stroke="#5e3d1e" stroke-width="2"/>')
    elif variant == 'spore_substrate':
        # Spore print card (half dark/half light) + wood vs soil substrate check
        parts.append('<rect x="46" y="50" width="76" height="58" fill="#fffdf7" stroke="#263d35" stroke-width="2"/>')
        parts.append('<rect x="84" y="50" width="38" height="58" fill="#263d35"/>')
        parts.append('<circle cx="84" cy="79" r="20" fill="none" stroke="#8f381c" stroke-width="2.5" stroke-dasharray="4 3"/>')
        parts.append('<rect x="138" y="88" width="80" height="24" rx="4" fill="#9c8261" stroke="#4f3c24" stroke-width="2"/>')
        parts.append('<path d="M178 88V64m-18 0q18-14 36 0Z" fill="#d7ceb8" stroke="#4f3c24" stroke-width="2"/>')
    else:
        # Agaric cutaway: cap, gills, annulus ring, stipe, basal volva cup in soil
        parts.append('<path d="M68 74q58-42 116 0Z" fill="#d8ccb4" stroke="#3d2e1e" stroke-width="2.2"/>')
        parts.append('<path d="M78 74v6M92 74v6M106 74v6M146 74v6M160 74v6M174 74v6" stroke="#5e4b35" stroke-width="1.6"/>')
        parts.append('<rect x="116" y="74" width="20" height="44" fill="#f9f7ef" stroke="#3d2e1e" stroke-width="2"/>')
        parts.append('<path d="M110 88l16 8 16-8" fill="none" stroke="#8f381c" stroke-width="2.4"/>')
        parts.append('<path d="M104 108q22 24 44 0l-6 18h-32Z" fill="#e6c8ba" stroke="#8f381c" stroke-width="2.2"/>')
        parts.append('<path d="M40 120h180" stroke="#7c6345" stroke-width="2" stroke-dasharray="5 3"/>')
    parts.append('<path d="M38 128h64M38 124v7M102 124v7" stroke="#183c31" stroke-width="1.6"/>')
    for i, feat in enumerate(features):
        col, row = i % 2, i // 2
        x = 248 + col * 224
        y = 38 + row * 50
        parts.append(f'<rect x="{x}" y="{y}" width="216" height="44" rx="5" fill="#f9faef" stroke="#4f6c5d" stroke-width="1.8"/>')
        parts.append(f'<rect x="{x}" y="{y}" width="22" height="44" rx="4" fill="{"#8f381c" if i == 3 else "#184438"}"/>')
        parts.append(_lbl(str(i + 1), x + 11, y + 26, 10.6, '#fffdf7'))
        parts.append(text(wrap(feat, 25)[:2], x + 28, y + 18, 14, 10.4, 650, '#183c31', 'start'))
    parts.append('<rect x="28" y="139" width="276" height="18" rx="4" fill="#dceadf" stroke="#184438"/>')
    parts.append(_lbl(spec['scale'], 166, 152, 10.3, '#183c31'))
    parts.append('<rect x="314" y="139" width="378" height="18" rx="4" fill="#f7dfd6" stroke="#8f381c" stroke-width="1.6"/>')
    parts.append(_lbl(spec['hold'], 503, 152, 10.3, '#642e1e'))
    parts.append('</g>')
    return ''.join(parts)


def _render_lookalike_diagnostic(spec):
    """Side-by-side target vs toxic-lookalike contrast plate with explicit HOLD exclusion bar."""
    variant = spec['variant']
    parts = [f'<g id="lookalike-diagnostic-{variant}-artwork">']
    # Left panel: Target specimen traits (solid dark border)
    parts.append('<rect x="28" y="38" width="318" height="96" rx="7" fill="#e6efe8" stroke="#184438" stroke-width="2.6"/>')
    parts.append('<rect x="28" y="38" width="318" height="23" rx="5" fill="#184438"/>')
    parts.append(_lbl('SUBJECT · ' + spec['target_name'], 187, 54, 10.8, '#fffdf7'))
    for idx, line in enumerate(spec['target_traits']):
        parts.append(text(wrap(f'{idx + 1}. {line}', 36)[:2], 40, 77 + idx * 29, 13, 10.5, 650, '#183c31', 'start'))
    # Center contrast divider badge
    parts.append('<circle cx="360" cy="86" r="15" fill="#fffdf7" stroke="#642e1e" stroke-width="2.2"/>')
    parts.append(_lbl('VS', 360, 90, 10.5, '#642e1e'))
    # Right panel: Toxic lookalike warning (dashed rust border)
    parts.append('<rect x="374" y="38" width="318" height="96" rx="7" fill="#f9eae3" stroke="#8f381c" stroke-width="2.6" stroke-dasharray="7 4"/>')
    parts.append('<rect x="374" y="38" width="318" height="23" rx="5" fill="#8f381c"/>')
    parts.append(_lbl('TOXIC LOOKALIKE · ' + spec['toxic_name'], 533, 54, 10.8, '#fffdf7'))
    for idx, line in enumerate(spec['toxic_traits']):
        parts.append(text(wrap(f'! {line}', 36)[:2], 386, 77 + idx * 29, 13, 10.5, 650, '#642e1e', 'start'))
    parts.append('<rect x="28" y="139" width="664" height="18" rx="4" fill="#f7dfd6" stroke="#8f381c" stroke-width="1.6"/>')
    parts.append(_lbl(spec['exclusion'], 360, 152, 10.5, '#642e1e'))
    parts.append('</g>')
    return ''.join(parts)


def _render_atlas_crossref_plate(spec):
    """Cross-zone field reference index preserving upstream zone IDs, conditions, and stop rules."""
    variant = spec['variant']
    rows = spec['rows']
    parts = [f'<g id="atlas-crossref-{variant}-artwork">']
    parts.append('<rect x="28" y="38" width="664" height="22" rx="4" fill="#184438"/>')
    parts.append(_lbl('SOURCE ZONES', 96, 53, 10.5, '#fffdf7'))
    parts.append(_lbl('INDEXED TOPIC & CONDITION', 308, 53, 10.5, '#fffdf7'))
    parts.append(_lbl('PRESERVED STOP / ESCALATION', 566, 53, 10.5, '#fffdf7'))
    for i, row in enumerate(rows):
        y = 63 + i * 24
        bg = '#f9faef' if i % 2 == 0 else '#eef3ee'
        parts.append(f'<rect x="28" y="{y}" width="664" height="22" rx="3" fill="{bg}" stroke="#7e9485" stroke-width="1.3"/>')
        parts.append(f'<rect x="28" y="{y}" width="136" height="22" rx="3" fill="#dceadf" stroke="#4f6c5d" stroke-width="1.2"/>')
        parts.append(_lbl(row['zones'], 96, y + 15, 10.5, '#183c31'))
        parts.append(_lbl(row['topic'], 174, y + 15, 10.4, '#183c31', 'start'))
        parts.append(_lbl(row['stop'], 456, y + 15, 10.4, '#642e1e', 'start'))
    parts.append('<rect x="28" y="139" width="664" height="18" rx="4" fill="#faeee5" stroke="#a05332"/>')
    parts.append(_lbl(spec['preserve'], 360, 152, 10.5, '#642e1e'))
    parts.append('</g>')
    return ''.join(parts)


def _render_specimen_doc_plate(spec):
    """Multi-view voucher specimen documentation workflow for botany, mycology, geology, and tracks."""
    variant = spec['variant']
    views = spec['views']
    parts = [f'<g id="specimen-doc-{variant}-artwork">']
    for i, view in enumerate(views):
        x = 28 + i * 168
        parts.append(f'<rect x="{x}" y="38" width="156" height="96" rx="6" fill="#f9faef" stroke="#285345" stroke-width="2"/>')
        parts.append(f'<rect x="{x}" y="38" width="156" height="22" rx="4" fill="#285345"/>')
        parts.append(_lbl(f'VIEW {i + 1}', x + 78, 53, 10.6, '#fffdf7'))
        # Viewfinder corner brackets inside card
        parts.append(f'<path d="M{x+12} 72v-6h6M{x+144} 72v-6h-6M{x+12} 120v6h6M{x+144} 120v6h-6" fill="none" stroke="#6f8c7a" stroke-width="1.8"/>')
        parts.append(text(wrap(view, 18)[:3], x + 78, 84, 14, 10.6, 650, '#183c31', 'middle'))
        if i < 3:
            parts.append(f'<path d="M{x+157} 86h9" stroke="#285345" stroke-width="2.2" marker-end="url(#arrow)"/>')
    parts.append('<rect x="28" y="139" width="330" height="18" rx="4" fill="#dceadf" stroke="#184438"/>')
    parts.append(_lbl(spec['voucher'], 193, 152, 10.3, '#183c31'))
    parts.append('<rect x="366" y="139" width="326" height="18" rx="4" fill="#f7dfd6" stroke="#8f381c"/>')
    parts.append(_lbl(spec['hold'], 529, 152, 10.3, '#642e1e'))
    parts.append('</g>')
    return ''.join(parts)


RENDERERS = {
    'cutaway': _render_cutaway,
    'force_redirect': _render_force_redirect,
    'canner_vent': _render_canner_vent,
    'branch': _render_branch,
    'exploded': _render_exploded,
    'cross_section': _render_cross_section,
    'mechanism': _render_mechanism,
    'comparison': _render_comparison,
    'environment': _render_environment,
    'decision_tree': _render_decision_tree,
    'failure_mode': _render_failure_mode,
    'correct_vs_wrong': _render_correct_vs_wrong,
    'sequence_plate': _render_sequence_plate,
    'system_boundary': _render_system_boundary,
    'escalation_ladder': _render_escalation_ladder,
    'anatomy_zone': _render_anatomy_zone,
    'seasonal_timeline': _render_seasonal_timeline,
    'geological_strata': _render_geological_strata,
    'mineral_test_plate': _render_mineral_test_plate,
    'wildlife_track_plate': _render_wildlife_track_plate,
    'regulation_boundary': _render_regulation_boundary,
    'hazard_exclusion_map': _render_hazard_exclusion_map,
    'botanical_morphology': _render_botanical_morphology,
    'fungal_anatomy': _render_fungal_anatomy,
    'lookalike_diagnostic': _render_lookalike_diagnostic,
    'atlas_crossref_plate': _render_atlas_crossref_plate,
    'specimen_doc_plate': _render_specimen_doc_plate,
}


def v01_source_path(card_id):
    return ROOT / 'foundations/visual/VISUAL_PILOT_REVIEW_PACKAGE/revised' / f'{card_id}.svg'


def render_diagram(card):
    stages = card['diagram'].split(' | ')
    card_id = card['id']
    specs = load_specs()
    spec = specs.get(card_id)
    if spec and spec['type'] == 'v01_artwork':
        return v01_source_path(card_id).read_text(encoding='utf-8')
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
