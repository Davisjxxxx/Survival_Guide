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
ZONES = {'Z01':'Survival fundamentals','Z02':'Shelter and housing',
         'Z03':'Fire and ignition','Z04':'Water','Z11':'Navigation reconstruction',
         'Z13':'Home preparedness reconstruction','Z14':'Food preservation reconstruction',
         'Z15':'Outage reconstruction'}
PACKS = {'water','fire','exposure','food','triage'}
FIELDS = {'objective','applies','equipment','verify','stop','diagram','visual','reviewer'}
STATUS = 'Editorial review draft · Specialist review pending · Publication hold'
ID = re.compile(r'Z\d{2}-[PR]\d{2}')


def require(condition, message):
    if not condition:
        raise ValueError(message)


def table(path, key):
    with path.open(encoding='utf-8', newline='') as file:
        records = list(csv.DictReader(file, delimiter='\t'))
    keyed = {r[key]: r for r in records}
    require(len(keyed) == len(records), f'Duplicate {key} in {path.name}')
    require(all(all(isinstance(v, str) and v.strip() for v in r.values()) for r in records),
            f'Empty or invalid column in {path.name}')
    return keyed


def load_evidence():
    sources = table(FOUND/'evidence/sources.tsv','id')
    claims = table(FOUND/'evidence/claims.tsv','id')
    targets = set()
    for source in sources.values():
        target = urlsplit(source['url'])
        canonical = (target.netloc.lower().removeprefix('www.'),target.path.rstrip('/'))
        require(target.scheme == 'https' and target.netloc and not target.query and not target.fragment,
                f'Invalid source URL {source["id"]}')
        require(canonical not in targets, f'Duplicate source destination {source["id"]}')
        targets.add(canonical)
        date.fromisoformat(source['checked'])
    require({r['pack'] for r in claims.values()} == PACKS, 'Evidence pack missing')
    for claim in claims.values():
        require(claim['source'] in sources, f'Missing source for {claim["id"]}')
    return sources, claims


def load_cards(paths, claims):
    cards = {}
    for path in paths:
        for block in path.read_text().strip().split('\n\n'):
            head, *lines = block.splitlines()
            card_id, title, origin = [part.strip() for part in head.split('|')]
            require(ID.fullmatch(card_id) and card_id[:3] in ZONES and card_id not in cards,
                    f'Invalid or duplicate page ID {card_id}')
            require(title and origin, f'Title or lineage missing for {card_id}')
            card = {'id':card_id, 'zone':card_id[:3], 'title':title, 'origin':origin,
                    'action':[], 'batch':path.stem, 'publication':'HOLD',
                    'technical_review':'AI editorial check; qualified reviewer pending'}
            for line in lines:
                key, sep, value = line.partition(': ')
                require(sep and value and '<' not in value and not re.search(r'\b(TBD|TODO|PLACEHOLDER)\b',value),
                        f'Malformed text in {card_id}')
                if key in {'action','verify','stop'}:
                    text, marker, refs = value.rpartition(' @')
                    claim_ids = refs.split(',')
                    require(marker and text and len(claim_ids) == len(set(claim_ids))
                            and all(ref in claims or ref == 'ED' for ref in claim_ids),
                            f'Broken claim links in {card_id}: {line}')
                    require(key == 'action' or key not in card, f'Duplicate {key} in {card_id}')
                    item = {'text':text,'claims':claim_ids}
                    if key == 'action':
                        card[key].append(item)
                    else:
                        card[key] = item
                else:
                    require(key in FIELDS and key not in card, f'Unexpected field {key} in {card_id}')
                    card[key] = value
            require(FIELDS <= card.keys() and 3 <= len(card['action']) <= 4, f'Incomplete page {card_id}')
            require(card['diagram'].count(' | ') == 2, f'Exactly three visual stages required: {card_id}')
            require(any(ref != 'ED' for item in [*card['action'],card['verify'],card['stop']]
                        for ref in item['claims']), f'Missing factual source linkage: {card_id}')
            cards[card_id] = card
    require(cards, 'No pages supplied')
    return cards


def crosswalk():
    with (FOUND/'evidence/track-b-crosswalk.tsv').open(newline='') as file:
        rows = list(csv.DictReader(file, delimiter='\t'))
    covered = set()
    for row in rows:
        artifact = row['artifact']
        if artifact in ('B012','B013','B014'):
            first, last = map(int,row['pages'].split('–'))
            covered.update(f'{artifact}-P{n:02}.html' for n in range(first,last+1))
        else:
            covered.add(artifact)
    expected = {p.name for p in (ROOT/'reader').glob('B0*') if p.suffix in ('.html','.pdf')}
    require(expected <= covered, 'Track B crosswalk omits an artifact')
    return rows


def doc(title, body):
    return ('<!doctype html><html lang="en"><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width, initial-scale=1">'
            f'<title>{escape(title)}</title><link rel="stylesheet" href="library.css">'
            '<link rel="stylesheet" href="edition.css"><body class="library foundation">'
            '<a class="skip-link" href="#content">Skip to content</a>'
            f'<aside class="edition">{STATUS}</aside>{body}</body></html>')


def statement(item):
    refs = ', '.join(item['claims'])
    return (f'<span data-claims="{escape(refs)}">{escape(item["text"]) }'
            f'<sup><a href="#evidence" aria-label="Evidence {escape(refs)}">[{escape(refs)}]</a></sup></span>')


def navigation(previous, next_):
    links = ['<a href="index.html">Contents &amp; search</a>']
    for label, dest in [('Previous', previous),('Next',next_)]:
        if dest:
            links.append(f'<a rel="{label.lower()}" href="{dest}.html">{label}</a>')
    return '<nav class="folio" aria-label="Page navigation">' + ''.join(links) + '</nav>'


def write_card(card, previous, next_, claims, sources, output):
    card_id = card['id']
    items = [*card['action'],card['verify'],card['stop']]
    refs = sorted({ref for row in items for ref in row['claims']} - {'ED'})
    entries = []
    for ref in refs:
        claim = claims[ref]
        source = sources[claim['source']]
        entries.append(f'<dt>{ref} · {escape(source["agency"])} · {escape(source["title"])}</dt>'
                       f'<dd>{escape(claim["locator"])} · {escape(claim["conditions"])}<br>'
                       f'{escape(claim["support"])}<br><a href="{escape(source["url"])}">Primary source</a>'
                       f' · checked {escape(source["checked"])}</dd>')
    actions = ''.join(f'<li>{statement(row)}</li>' for row in card['action'])
    origin = escape(card["origin"])
    lineage = f'<p>Lineage · {origin}</p>' if card['id'][4] == 'R' else ''
    body = (
        navigation(previous,next_) +
        f'<main id="content"><article class="card"><p class="kicker">{card_id} · {escape(ZONES[card["zone"]])}</p>'
        f'<h1>{escape(card["title"])}</h1><p class="objective">{escape(card["objective"])}</p>{lineage}'
        f'<p><strong>When it applies</strong> · {escape(card["applies"])}</p>'
        f'<p><strong>Equipment</strong> · {escape(card["equipment"])}</p>'
        f'<figure><img src="visuals/{card_id}.svg" alt="{escape(card["diagram"])}">'
        f'<figcaption>{escape(card["visual"])}</figcaption></figure>'
        f'<h2>Actions</h2><ol class="actions">{actions}</ol>'
        f'<p><strong>Verify</strong> · {statement(card["verify"])}</p>'
        f'<p class="stop"><strong>Stop or change course</strong> · {statement(card["stop"])}</p>'
        f'<footer class="card-footer">Qualified review pending · {escape(card["reviewer"])}'
        f'<br>Evidence IDs · {escape(", ".join(refs))} · ED identifies an editorial check or adaptation.</footer>'
        '<details id="evidence" open><summary>Evidence and editorial notes</summary><dl>'
        + ''.join(entries) + f'</dl><p>Source lineage · {origin}.</p></details></article></main>')
    (output/f'{card_id}.html').write_text(doc(card['title'],body),encoding='utf-8')


def write_index(cards, output):
    groups = []
    for zone, title in ZONES.items():
        links = []
        for card in cards.values():
            if card['zone'] != zone:
                continue
            search = ' '.join([card['id'],card['title'],card['objective'],card['applies'],
                               *[item['text'] for item in card['action']]]).lower()
            links.append(f'<li data-index="{escape(search)}"><a href="{card["id"]}.html">'
                         f'<small>{card["id"]}</small> · {escape(card["title"])}</a></li>')
        if links:
            groups.append(f'<section><h2>{title}</h2><ul>{"".join(links)}</ul></section>')
    body = (
        '<header class="cover-panel"><div><p>Survival Field Encyclopedia</p><h1>Foundational field cards</h1></div></header>'
        '<main id="content"><div class="lookup"><label for="lookup">Search field cards</label>'
        '<input type="search" id="lookup"><p id="matches" role="status"></p></div>'
        f'<div class="catalog">{"".join(groups)}</div></main><script src="search.js"></script>')
    (output/'index.html').write_text(doc('Foundational field cards',body),encoding='utf-8')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=FOUND/'reader')
    args = parser.parse_args()
    from foundation_diagrams import render_diagram

    sources, claims = load_evidence()
    cards = load_cards(sorted((FOUND/'manuscripts').glob('*.cards')),claims)
    crosswalk()
    output = args.output
    output.mkdir(parents=True,exist_ok=True)
    (output/'visuals').mkdir(exist_ok=True)
    for path in ('library.css','search.js'):
        shutil.copyfile(ROOT/'production/templates'/path,output/path)
    shutil.copyfile(FOUND/'edition.css',output/'edition.css')
    keys = list(cards)
    visuals = []
    for i, (card_id, card) in enumerate(cards.items()):
        write_card(card,keys[i-1] if i else None,keys[i+1] if i+1<len(keys) else None,claims,sources,output)
        filename = f'visuals/{card_id}.svg'
        data = render_diagram(card).encode()
        (output/filename).write_bytes(data)
        visuals.append(dict(id=card_id+'-FIG01',page=card_id,file=filename,sha256=sha256(data).hexdigest(),
                            rights='Project original',classification='Editable conceptual diagram',
                            provenance=card['batch']+'.cards and scripts/foundation_diagrams.py',
                            diagnostic_photo=False,review='Independent subject review pending'))
    write_index(cards,output)
    (output/'asset-manifest.json').write_text(json.dumps(visuals,indent=2,ensure_ascii=False)+'\n')
    (output/'page-manifest.json').write_text(json.dumps(list(cards.values()),indent=2,ensure_ascii=False)+'\n')
    print(f'{len(cards)} draft cards, {len(visuals)} original SVGs, {len(sources)} sources, {len(claims)} evidence rows')


if __name__ == '__main__':
    main()
