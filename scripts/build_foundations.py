"""Validate evidence and authoring inputs, then compile a standalone offline edition."""
import argparse
import csv
from datetime import date
from hashlib import sha256
from html import escape
import json
from pathlib import Path
import re
import shutil
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
FOUND = ROOT / 'foundations'
FOUNDATIONAL_ZONES = ['Z01', 'Z02', 'Z03', 'Z04']
ZONES = {
    'Z01': 'Survival fundamentals',
    'Z02': 'Shelter and housing',
    'Z03': 'Fire and ignition',
    'Z04': 'Water',
    'Z11': 'Navigation reconstruction',
    'Z13': 'Home preparedness reconstruction',
    'Z14': 'Food preservation reconstruction',
    'Z15': 'Outage reconstruction',
}
ZONE_TARGETS = {'Z01': 22, 'Z02': 55, 'Z03': 45, 'Z04': 55}
PACKS = {'water', 'fire', 'exposure', 'food', 'triage'}
FIELDS = {'objective', 'applies', 'equipment', 'verify', 'stop', 'diagram', 'visual', 'reviewer'}
CLAIM_FIELDS = {'id', 'pack', 'source', 'locator', 'conditions', 'support',
                'limitations', 'conflicts', 'editorial_note', 'reviewer'}
STATUS = 'Editorial review draft · Specialist review pending · Publication hold'
ID = re.compile(r'Z\d{2}-[PR]\d{2}')

ALL_16_ZONES = [
    ('Z01', 'Survival fundamentals', 22, 'Critical'),
    ('Z02', 'Shelter and housing', 55, 'Critical'),
    ('Z03', 'Fire and ignition', 45, 'Critical'),
    ('Z04', 'Water', 55, 'Critical'),
    ('Z05', 'Wild foods and poisonous lookalikes', 135, 'Critical'),
    ('Z06', 'Hunting and fishing', 48, 'High'),
    ('Z07', 'Traps and snares', 30, 'High'),
    ('Z08', 'Rocks, minerals and materials', 60, 'High'),
    ('Z09', 'Tools and construction', 53, 'High'),
    ('Z10', 'Wilderness medicine', 80, 'Critical'),
    ('Z11', 'Navigation, weather and rescue', 68, 'Critical'),
    ('Z12', 'Extreme environments', 75, 'High'),
    ('Z13', 'Home survival and utilities', 70, 'Critical'),
    ('Z14', 'Food production and preservation', 80, 'Critical'),
    ('Z15', 'Disaster scenarios', 65, 'High'),
    ('Z16', 'Field reference atlas', 75, 'High'),
]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def table(path, key, required_columns=None):
    with path.open(encoding='utf-8', newline='') as file:
        reader = csv.DictReader(file, delimiter='\t')
        if required_columns:
            require(required_columns <= set(reader.fieldnames or []),
                    f'Missing required columns in {path.name}: {sorted(required_columns - set(reader.fieldnames or []))}')
        records = list(reader)
    keyed = {r[key]: r for r in records}
    require(len(keyed) == len(records), f'Duplicate {key} in {path.name}')
    require(all(all(isinstance(v, str) and v.strip() for v in r.values()) for r in records),
            f'Empty or invalid column in {path.name}')
    return keyed


def load_evidence():
    sources = table(FOUND / 'evidence/sources.tsv', 'id',
                    {'id', 'agency', 'title', 'url', 'revision', 'checked'})
    claims = table(FOUND / 'evidence/claims.tsv', 'id', CLAIM_FIELDS)
    targets = set()
    for source in sources.values():
        target = urlsplit(source['url'])
        canonical = (target.netloc.lower().removeprefix('www.'), target.path.rstrip('/'))
        require(target.scheme == 'https' and target.netloc and not target.query and not target.fragment,
                f'Invalid source URL {source["id"]}')
        require(canonical not in targets, f'Duplicate source destination {source["id"]}')
        targets.add(canonical)
        date.fromisoformat(source['checked'])
    require({r['pack'] for r in claims.values()} == PACKS, 'Evidence pack missing')
    for claim in claims.values():
        require(claim['source'] in sources, f'Missing source for {claim["id"]}')
    return sources, claims


def classify_card(card_id, origin):
    if card_id[4] == 'R':
        return 'Reconstruction draft'
    low = origin.lower()
    if 'new manuscript' in low and not re.search(r'\bb0(03|07|08|09|10|11|12|13|14)\b', low):
        return 'New manuscript'
    if re.search(r'\bb0(03|07|08|09|10|11|12|13|14)\b', low):
        return 'Adapted historical material'
    return 'New manuscript'


def _sort_key(card_id):
    zone_order = list(ZONES).index(card_id[:3])
    kind_order = 0 if card_id[4] == 'P' else 1
    return (zone_order, kind_order, int(card_id[5:]))


def lint_cards(cards):
    """Detect duplicate titles and safety-critical instruction contradictions."""
    titles = {}
    for cid, card in cards.items():
        norm_title = ' '.join(card['title'].lower().split())
        require(norm_title not in titles, f'Duplicate card title between {titles.get(norm_title)} and {cid}')
        titles[norm_title] = cid

        statements = [item['text'] for item in card['action']]
        if 'failure' in card:
            statements.append(card['failure']['text'])
        statements.extend([card['verify']['text'], card['stop']['text']])
        full = ' '.join([card['title'], card['objective'], card['applies'], *statements]).lower()

        # Rule 1: Never imply visual clarity proves potability.
        if re.search(r'\bclear water is (safe|potable)\b|\bclarity (proves|guarantees|establishes) (safety|potability)\b', full):
            raise ValueError(f'Contradiction: visual clarity potability claim in {cid}')

        # Rule 2: Never authorize fuel-burning appliances inside tents/vehicles/enclosures.
        if re.search(r'\b(run|operate|burn|light)\b[^.]{0,45}\b(stove|heater|charcoal|generator)\b[^.]{0,35}\b(inside|in) (a |the )?(tent|vehicle|snow cave|enclosure|garage)\b', full):
            if not re.search(r'\b(never|do not|keep|avoid|not)\b', full):
                raise ValueError(f'Contradiction: enclosed combustion authorization in {cid}')

        # Rule 3: Boiling duration must not omit altitude distinction when stating 1-minute rolling boil.
        if re.search(r'rolling boil.{0,25}(one|1)\s+minute', full):
            require('6,500' in full or 'altitude' in full or 'elevation' in full,
                    f'Contradiction: boiling duration omits altitude rule in {cid}')

        # Rule 4: Portable generator distance must never contradict >= 20 feet.
        if 'portable generator' in full and re.search(r'\b(\d+)\s*feet\b', full):
            nums = [int(m) for m in re.findall(r'\b(\d+)\s*feet\b', full)]
            require(all(n >= 20 for n in nums), f'Contradiction: generator distance < 20 ft in {cid}')

        # Rule 5: Do not state unvalidated structural load capacities as safe engineering specs.
        if card['zone'] == 'Z02' and re.search(r'\b(supports|holds|rated for|safe load of)\s+\d+\s*(lb|lbs|pounds|kg|psf)\b', full):
            raise ValueError(f'Contradiction: unvalidated structural load rating in {cid}')


def load_cards(paths, claims):
    cards = {}
    for path in paths:
        is_expanded_batch = bool(re.match(r'^(0[6-9]|[1-9]\d)-', path.stem))
        for block in path.read_text(encoding='utf-8').strip().split('\n\n'):
            if not block.strip():
                continue
            head, *lines = block.splitlines()
            parts = [part.strip() for part in head.split('|')]
            require(len(parts) == 3, f'Malformed card header in {path.name}: {head}')
            card_id, title, origin = parts
            require(ID.fullmatch(card_id) and card_id[:3] in ZONES and card_id not in cards,
                    f'Invalid or duplicate page ID {card_id}')
            require(title and origin, f'Title or lineage missing for {card_id}')
            card = {
                'id': card_id,
                'zone': card_id[:3],
                'title': title,
                'origin': origin,
                'category': classify_card(card_id, origin),
                'action': [],
                'batch': path.stem,
                'publication': 'HOLD',
                'technical_review': 'AI editorial check; qualified reviewer pending',
            }
            for line in lines:
                key, sep, value = line.partition(': ')
                require(sep and value and '<' not in value and not re.search(r'\b(TBD|TODO|PLACEHOLDER)\b', value),
                        f'Malformed text in {card_id}')
                if key in {'action', 'failure', 'verify', 'stop'}:
                    text_part, marker, refs = value.rpartition(' @')
                    claim_ids = refs.split(',')
                    require(marker and text_part and len(claim_ids) == len(set(claim_ids))
                            and all(ref in claims or ref == 'ED' for ref in claim_ids),
                            f'Broken claim links in {card_id}: {line}')
                    require(key == 'action' or key not in card, f'Duplicate {key} in {card_id}')
                    item = {'text': text_part, 'claims': claim_ids}
                    if key == 'action':
                        card[key].append(item)
                    else:
                        card[key] = item
                else:
                    require(key in FIELDS and key not in card, f'Unexpected field {key} in {card_id}')
                    card[key] = value
            require(FIELDS <= card.keys() and 3 <= len(card['action']) <= 4, f'Incomplete page {card_id}')
            if is_expanded_batch:
                require('failure' in card, f'Missing failure recognition field in {card_id}')
            require(card['diagram'].count(' | ') == 2, f'Exactly three visual stages required: {card_id}')
            all_items = [*card['action'], card['verify'], card['stop']]
            if 'failure' in card:
                all_items.append(card['failure'])
            require(any(ref != 'ED' for item in all_items for ref in item['claims']),
                    f'Missing factual source linkage: {card_id}')
            cards[card_id] = card
    require(cards, 'No pages supplied')
    ordered = {cid: cards[cid] for cid in sorted(cards, key=_sort_key)}
    lint_cards(ordered)
    return ordered


def crosswalk():
    with (FOUND / 'evidence/track-b-crosswalk.tsv').open(encoding='utf-8', newline='') as file:
        rows = list(csv.DictReader(file, delimiter='\t'))
    covered = set()
    for row in rows:
        artifact = row['artifact']
        if artifact in ('B012', 'B013', 'B014'):
            first, last = map(int, row['pages'].split('–'))
            covered.update(f'{artifact}-P{n:02}.html' for n in range(first, last + 1))
        else:
            covered.add(artifact)
    expected = {p.name for p in (ROOT / 'reader').glob('B0*') if p.suffix in ('.html', '.pdf')}
    require(expected <= covered, 'Track B crosswalk omits an artifact')
    return rows


def doc(title, body, css_prefix=''):
    return (
        '<!doctype html><html lang="en"><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        f'<title>{escape(title)}</title>'
        f'<link rel="stylesheet" href="{css_prefix}library.css">'
        f'<link rel="stylesheet" href="{css_prefix}edition.css">'
        '<body class="library foundation">'
        '<a class="skip-link" href="#content">Skip to content</a>'
        f'<aside class="edition">{STATUS}</aside>{body}</body></html>'
    )


def statement(item):
    refs = ', '.join(item['claims'])
    return (
        f'<span data-claims="{escape(refs)}">{escape(item["text"])}'
        f'<sup><a href="#evidence" aria-label="Evidence {escape(refs)}">[{escape(refs)}]</a></sup></span>'
    )


def badge_html(category):
    cls = 'badge'
    if category == 'Adapted historical material':
        cls += ' badge-adapted'
    elif category == 'Reconstruction draft':
        cls += ' badge-recon'
    return f'<span class="{cls}">{escape(category)}</span>'


def navigation(previous, next_, zone):
    links = ['<a href="index.html">Contents &amp; search</a>']
    if zone in FOUNDATIONAL_ZONES:
        links.append(f'<a href="zones/{zone}/index.html">{zone} Zone reader</a>')
    links.append('<a href="directory.html">Encyclopedia directory</a>')
    for label, dest in [('Previous', previous), ('Next', next_)]:
        if dest:
            links.append(f'<a rel="{label.lower()}" href="{dest}.html">{label}</a>')
    return '<nav class="folio" aria-label="Page navigation">' + ''.join(links) + '</nav>'


def write_card(card, previous, next_, claims, sources, output):
    card_id = card['id']
    items = [*card['action'], card['verify'], card['stop']]
    if 'failure' in card:
        items.append(card['failure'])
    refs = sorted({ref for row in items for ref in row['claims']} - {'ED'})
    entries = []
    for ref in refs:
        claim = claims[ref]
        source = sources[claim['source']]
        entries.append(
            f'<dt>{ref} · {escape(source["agency"])} · {escape(source["title"])} ({escape(source["revision"])})</dt>'
            f'<dd><strong>Section</strong>: {escape(claim["locator"])} · <strong>Conditions</strong>: {escape(claim["conditions"])}<br>'
            f'<strong>Support</strong>: {escape(claim["support"])}<br>'
            f'<strong>Limitations</strong>: {escape(claim["limitations"])} · '
            f'<strong>Conflicting evidence</strong>: {escape(claim["conflicts"])}<br>'
            f'<strong>Editorial note</strong>: {escape(claim["editorial_note"])} · '
            f'<strong>Specialist reviewer</strong>: {escape(claim["reviewer"])}<br>'
            f'<a href="{escape(source["url"])}">Primary source</a> · checked {escape(source["checked"])}</dd>'
        )
    actions = ''.join(f'<li>{statement(row)}</li>' for row in card['action'])
    stages = ''.join(f'<li>{escape(stage)}</li>' for stage in card['diagram'].split(' | '))
    origin = escape(card['origin'])
    lineage = f'<p>Lineage · {origin}</p>' if card['id'][4] == 'R' else ''
    failure_html = (
        f'<p class="failure"><strong>Failure recognition</strong> · {statement(card["failure"])}</p>'
        if 'failure' in card else ''
    )
    body = (
        navigation(previous, next_, card['zone'])
        + f'<main id="content"><article class="card">'
        f'<p class="kicker">{card_id} · {escape(ZONES[card["zone"]])} · {badge_html(card["category"])}</p>'
        f'<h1>{escape(card["title"])}</h1>'
        f'<p class="objective">{escape(card["objective"])}</p>{lineage}'
        f'<p><strong>When it applies</strong> · {escape(card["applies"])}</p>'
        f'<p><strong>Equipment</strong> · {escape(card["equipment"])}</p>'
        f'<figure><img src="visuals/{card_id}.svg" alt="{escape(card["diagram"])}">'
        f'<figcaption>{escape(card["visual"])}<ul class="diagram-labels" aria-hidden="true">{stages}</ul></figcaption></figure>'
        f'<h2>Actions</h2><ol class="actions">{actions}</ol>'
        f'{failure_html}'
        f'<p><strong>Verify</strong> · {statement(card["verify"])}</p>'
        f'<p class="stop"><strong>Stop or change course</strong> · {statement(card["stop"])}</p>'
        f'<footer class="card-footer">Qualified review pending · {escape(card["reviewer"])}'
        f'<br>Evidence IDs · {escape(", ".join(refs))} · ED identifies an editorial check or adaptation.</footer>'
        '<details id="evidence" open><summary>Evidence and editorial notes</summary><dl>'
        + ''.join(entries)
        + f'</dl><p>Source lineage · {origin} · Classification · {escape(card["category"])}.</p></details></article></main>'
    )
    (output / f'{card_id}.html').write_text(doc(card['title'], body), encoding='utf-8')


def _card_search_text(card):
    parts = [card['id'], card['title'], card['objective'], card['applies'], card['category'],
             *[item['text'] for item in card['action']]]
    if 'failure' in card:
        parts.append(card['failure']['text'])
    return ' '.join(parts).lower()


def write_index(cards, output):
    found_cards = [c for c in cards.values() if c['zone'] in FOUNDATIONAL_ZONES]
    recon_cards = [c for c in cards.values() if c['zone'] not in FOUNDATIONAL_ZONES]
    zone_links = []
    for z in FOUNDATIONAL_ZONES:
        cnt = sum(1 for c in found_cards if c['zone'] == z)
        zone_links.append(f'<a href="zones/{z}/index.html">{z} {escape(ZONES[z])} ({cnt}/{ZONE_TARGETS[z]})</a>')
    zone_links.append('<a href="directory.html">16-Zone Encyclopedia Directory</a>')

    groups = []
    for zone, title in ZONES.items():
        links = []
        for card in cards.values():
            if card['zone'] != zone:
                continue
            links.append(
                f'<li data-index="{escape(_card_search_text(card))}">'
                f'<a href="{card["id"]}.html"><small>{card["id"]}</small> · {escape(card["title"])} '
                f'{badge_html(card["category"])}</a></li>'
            )
        if links:
            heading = f'{zone} · {title} ({len(links)})'
            groups.append(f'<section id="{zone}"><h2>{escape(heading)}</h2><ul>{"".join(links)}</ul></section>')

    body = (
        '<header class="cover-panel"><div><p>Survival Field Encyclopedia</p>'
        '<h1>Foundational field cards</h1>'
        f'<p class="cover-sub">{len(found_cards)} foundational draft pages across Z01–Z04 plus '
        f'{len(recon_cards)} retained reconstruction drafts. Offline searchable edition.</p></div></header>'
        '<main id="content">'
        f'<nav class="zone-bar" aria-label="Zone readers and directory">{"".join(zone_links)}</nav>'
        '<div class="lookup"><label for="lookup">Search field cards</label>'
        '<input type="search" id="lookup" placeholder="e.g. hypothermia, boil, windbreak, ferro">'
        '<p id="matches" role="status"></p></div>'
        f'<div class="catalog">{"".join(groups)}</div></main><script src="search.js"></script>'
    )
    (output / 'index.html').write_text(doc('Foundational field cards', body), encoding='utf-8')


def write_zone_readers(cards, output):
    for zone in FOUNDATIONAL_ZONES:
        zone_dir = output / 'zones' / zone
        zone_dir.mkdir(parents=True, exist_ok=True)
        zcards = [c for c in cards.values() if c['zone'] == zone]
        adapted = sum(1 for c in zcards if c['category'] == 'Adapted historical material')
        new_ms = sum(1 for c in zcards if c['category'] == 'New manuscript')
        nav_links = ['<a href="../../index.html">Consolidated reader</a>']
        for z in FOUNDATIONAL_ZONES:
            if z != zone:
                nav_links.append(f'<a href="../{z}/index.html">{z} reader</a>')
        nav_links.append('<a href="../../directory.html">Encyclopedia directory</a>')
        items = []
        for card in zcards:
            items.append(
                f'<li data-index="{escape(_card_search_text(card))}">'
                f'<a href="../../{card["id"]}.html"><small>{card["id"]}</small> · {escape(card["title"])} '
                f'{badge_html(card["category"])}</a></li>'
            )
        body = (
            f'<nav class="folio" aria-label="Zone navigation">{"".join(nav_links)}</nav>'
            f'<header class="cover-panel"><div><p>Survival Field Encyclopedia · {zone}</p>'
            f'<h1>{escape(ZONES[zone])}</h1>'
            f'<p class="cover-sub">{len(zcards)} of {ZONE_TARGETS[zone]} draft pages '
            f'({adapted} adapted historical · {new_ms} new manuscripts). Offline standalone zone reader.</p></div></header>'
            '<main id="content"><div class="lookup"><label for="lookup">Search zone pages</label>'
            '<input type="search" id="lookup"><p id="matches" role="status"></p></div>'
            f'<div class="catalog"><section><h2>{zone} · {escape(ZONES[zone])}</h2><ul>{"".join(items)}</ul></section></div>'
            '</main><script src="../../search.js"></script>'
        )
        (zone_dir / 'index.html').write_text(
            doc(f'{zone} · {ZONES[zone]}', body, css_prefix='../../'),
            encoding='utf-8'
        )


def write_directory(cards, xwalk_rows, output):
    """Build the integrated 16-zone directory without modifying the frozen Track B reader."""
    counts = {}
    for c in cards.values():
        counts[c['zone']] = counts.get(c['zone'], 0) + 1

    zone_rows = []
    for zid, zname, target, prio in ALL_16_ZONES:
        draft_cnt = counts.get(zid, 0)
        if zid in FOUNDATIONAL_ZONES:
            link = f'<a href="zones/{zid}/index.html">Open {zid} reader ({draft_cnt}/{target})</a>'
            state = 'DRAFT_COMPLETE' if draft_cnt == target else f'IN_PROGRESS ({draft_cnt}/{target})'
        elif draft_cnt:
            link = f'<a href="index.html#{zid}">Reconstruction drafts ({draft_cnt})</a>'
            state = 'RECONSTRUCTION_DRAFT'
        else:
            link = 'Planned in 16-zone scope'
            state = 'RETAINED_SCOPE_OPEN'
        zone_rows.append(
            f'<tr><td><strong>{zid}</strong></td><td>{escape(zname)}</td><td>{target}</td>'
            f'<td>{draft_cnt}</td><td>{escape(prio)}</td><td>{escape(state)}</td><td>{link}</td></tr>'
        )

    proof_rows = []
    for row in xwalk_rows:
        art = row['artifact']
        if art.endswith('-original.pdf'):
            kind = 'Duplicate historical proof (original preserved)'
            badge = '<span class="badge badge-frozen">Duplicate historical proof</span>'
        elif art.endswith(('.pdf', '.html')):
            kind = 'Frozen historical proof'
            badge = '<span class="badge badge-frozen">Frozen historical proof</span>'
        elif art in ('B012', 'B013', 'B014'):
            kind = 'Frozen Track B chapter HTML'
            badge = '<span class="badge badge-frozen">Frozen Track B HTML</span>'
        else:
            kind = 'Historical archive / lacuna'
            badge = '<span class="badge badge-frozen">Archive record</span>'
        dest = '../../reader/index.html'
        if art.endswith(('.pdf', '.html')):
            dest = f'../../reader/{art}'
        proof_rows.append(
            f'<li data-index="{escape((art + " " + row["zones"] + " " + row["disposition"] + " " + kind).lower())}">'
            f'<a href="{dest}"><small>{escape(art)}</small> (pp. {escape(row["pages"])}) · '
            f'{escape(row["zones"])} · {escape(row["disposition"])} {badge}</a></li>'
        )

    found_links = []
    for c in cards.values():
        found_links.append(
            f'<li data-index="{escape(_card_search_text(c))}">'
            f'<a href="{c["id"]}.html"><small>{c["id"]}</small> · {escape(c["title"])} '
            f'{badge_html(c["category"])}</a></li>'
        )

    nav = (
        '<nav class="folio" aria-label="Directory navigation">'
        '<a href="index.html">Consolidated foundational reader</a>'
        '<a href="zones/Z01/index.html">Z01</a>'
        '<a href="zones/Z02/index.html">Z02</a>'
        '<a href="zones/Z03/index.html">Z03</a>'
        '<a href="zones/Z04/index.html">Z04</a>'
        '<a href="../../reader/index.html">Frozen Track B edition (unchanged)</a></nav>'
    )
    body = (
        nav
        + '<header class="cover-panel"><div><p>Survival Field Encyclopedia · Integrated Master Directory</p>'
        '<h1>Sixteen-zone encyclopedia directory</h1>'
        '<p class="cover-sub">Links the foundational Z01–Z04 edition, retained reconstructions, and frozen Track B '
        'historical proofs without altering any frozen edition files.</p></div></header>'
        '<main id="content">'
        '<h2>Master 16-zone status</h2>'
        '<table class="dir-table"><thead><tr><th>Zone</th><th>Domain</th><th>Planned</th><th>Drafts</th>'
        '<th>Priority</th><th>Status</th><th>Reader access</th></tr></thead>'
        f'<tbody>{"".join(zone_rows)}</tbody></table>'
        '<div class="lookup"><label for="lookup">Search across foundational pages, reconstructions, and frozen proofs</label>'
        '<input type="search" id="lookup"><p id="matches" role="status"></p></div>'
        '<div class="catalog">'
        f'<section><h2>Foundational &amp; reconstruction drafts ({len(cards)})</h2><ul>{"".join(found_links)}</ul></section>'
        f'<section><h2>Frozen Track B historical proofs &amp; duplicates ({len(xwalk_rows)})</h2><ul>{"".join(proof_rows)}</ul></section>'
        '</div></main><script src="search.js"></script>'
    )
    (output / 'directory.html').write_text(doc('Sixteen-zone encyclopedia directory', body), encoding='utf-8')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=FOUND / 'reader')
    args = parser.parse_args()
    from foundation_diagrams import CROSS_SECTIONS, load_specs, render_diagram, reset_specs_cache

    reset_specs_cache()
    sources, claims = load_evidence()
    cards = load_cards(sorted((FOUND / 'manuscripts').glob('*.cards')), claims)
    xwalk_rows = crosswalk()
    specs = load_specs()

    output = args.output
    output.mkdir(parents=True, exist_ok=True)
    (output / 'visuals').mkdir(exist_ok=True)
    for path in ('library.css', 'search.js'):
        shutil.copyfile(ROOT / 'production/templates' / path, output / path)
    shutil.copyfile(FOUND / 'edition.css', output / 'edition.css')

    keys = list(cards)
    visuals = []
    for i, (card_id, card) in enumerate(cards.items()):
        if re.match(r'^(0[6-9]|[1-9]\d)-', card['batch']):
            require(card_id in specs, f'Missing technical diagram specification for {card_id}')
        write_card(card, keys[i - 1] if i else None, keys[i + 1] if i + 1 < len(keys) else None, claims, sources, output)
        filename = f'visuals/{card_id}.svg'
        data = render_diagram(card).encode('utf-8')
        (output / filename).write_bytes(data)
        spec = specs.get(card_id)
        if card_id in CROSS_SECTIONS:
            diag_type = 'cross_section_hand'
            spec_src = 'scripts/foundation_diagrams.py#CROSS_SECTIONS'
        elif spec:
            diag_type = spec['type']
            spec_src = f'foundations/evidence/diagram-specs.json#{card_id}'
        else:
            diag_type = 'sequence_schematic'
            spec_src = f'foundations/manuscripts/{card["batch"]}.cards'
        visuals.append(dict(
            id=card_id + '-FIG01',
            page=card_id,
            file=filename,
            sha256=sha256(data).hexdigest(),
            rights='Project original',
            classification='Editable conceptual technical diagram',
            diagram_type=diag_type,
            provenance=f'{card["batch"]}.cards, {spec_src}, and scripts/foundation_diagrams.py',
            diagnostic_photo=False,
            review='Independent subject review pending',
        ))

    write_index(cards, output)
    write_zone_readers(cards, output)
    write_directory(cards, xwalk_rows, output)
    (output / 'asset-manifest.json').write_text(json.dumps(visuals, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    (output / 'page-manifest.json').write_text(json.dumps(list(cards.values()), indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    found_cnt = sum(1 for c in cards.values() if c['zone'] in FOUNDATIONAL_ZONES)
    print(f'{len(cards)} draft cards ({found_cnt} foundational Z01-Z04), {len(visuals)} original SVGs, '
          f'{len(sources)} sources, {len(claims)} evidence rows')


if __name__ == '__main__':
    main()
