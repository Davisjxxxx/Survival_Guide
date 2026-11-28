"""Fingerprint the inputs a tagged print proof is made from (RT01-06).

A proof sheet is printed from a card's reader body (its evidence panel removed and links
unwrapped), the figure that body embeds, and the print stylesheets. proof_section() builds
that body exactly as scripts/print_foundations_tagged.py prints it; page_inputs() hashes the
body with each embedded image's bytes; style_digest() covers the stylesheets and the proof
template. Print receipts record these per PDF, and scripts/check_foundations.py compares
them with the current inputs: a proof whose inputs changed must be rebuilt, or explicitly
withheld in foundations/proofs/PROOF-CURRENCY.json when it is not part of any package.

A matching fingerprint means the PDF was printed from the current inputs. It says nothing
about the content's correctness, safety or approval.
"""
from hashlib import sha256
import json
from pathlib import Path

from bs4 import BeautifulSoup

from build_foundations import FOUND, FOUNDATIONAL_ZONES

READER = FOUND / 'reader'
PROOF_TEMPLATE = '<style>.proof+.proof{break-before:page}</style><body class="library foundation"><main>'
STYLESHEETS = ('library.css', 'edition.css')
# Proofs that ship inside an offline package; these may never be withheld as stale.
PACKAGED_PROOF_NAMES = {'reconstructions'} | {f'Z{n:02d}' for n in range(1, 17)}


def proof_section(reader, card, absolute=True):
    """The card body a proof sheet prints, and the image paths it embeds (relative to reader)."""
    soup = BeautifulSoup((reader / f'{card["id"]}.html').read_text(encoding='utf-8'), 'html.parser')
    article = soup.find('article')
    article.find('details').decompose()
    for ref in article.select('sup a, a.atlas-link, a.xref'):
        ref.unwrap()
    images = []
    for image in article.find_all('img'):
        images.append(image['src'])
        if absolute:
            image['src'] = (reader / image['src']).as_uri()
    return f'<section class="proof">{soup.select_one("aside.edition")}{article}</section>', images


def page_inputs(reader, card):
    body, images = proof_section(reader, card, absolute=False)
    digest = sha256(body.encode('utf-8'))
    for src in images:
        digest.update(f'\n{src}:'.encode('utf-8') + sha256((reader / src).read_bytes()).hexdigest().encode('ascii'))
    return digest.hexdigest()[:16]


def style_digest(reader):
    digest = sha256(PROOF_TEMPLATE.encode('utf-8'))
    for name in STYLESHEETS:
        digest.update(name.encode('utf-8') + sha256((reader / name).read_bytes()).hexdigest().encode('ascii'))
    return digest.hexdigest()[:16]


def editions(cards):
    """Every proof edition the printer produces, by name, with its cards in print order."""
    zones = {zone: [c for c in cards if c['zone'] == zone] for zone in sorted({c['zone'] for c in cards})}
    out = {'foundations': [c for c in cards if c['zone'] in FOUNDATIONAL_ZONES], 'encyclopedia': list(cards),
           **{zone: cs for zone, cs in zones.items() if len(cs) > 1}}
    out['reconstructions'] = [c for c in cards if c['category'] == 'Reconstruction draft']
    return out


def edition_of(filename):
    """Edition name of a proof file: foundations.pdf, Z14-letter.pdf, encyclopedia-a4.pdf, ..."""
    stem = Path(filename).stem
    for suffix in ('-letter', '-a4'):
        if stem.endswith(suffix):
            return stem[:-len(suffix)]
    return stem


def fingerprint(reader, selection, cache=None):
    """Receipt fields for a proof printed from selection: per-page inputs and the style digest."""
    cache = {} if cache is None else cache
    pages = {}
    for card in selection:
        if card['id'] not in cache:
            cache[card['id']] = page_inputs(reader, card)
        pages[card['id']] = cache[card['id']]
    return dict(style_inputs=style_digest(reader), page_inputs=pages)


def stale_pages(record, current):
    """Pages whose print inputs differ between a receipt record and the current inputs."""
    if record.get('style_inputs') != current['style_inputs']:
        return sorted(current['page_inputs'])
    old, new = record.get('page_inputs', {}), current['page_inputs']
    return sorted(k for k in set(old) | set(new) if old.get(k) != new.get(k))


def load_cards(reader=READER):
    return json.loads((reader / 'page-manifest.json').read_text(encoding='utf-8'))
