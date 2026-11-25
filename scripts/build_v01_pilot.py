"""Build the standalone V01 reviewer gallery and its tagged sample proofs."""
import argparse
from hashlib import sha256
from html import escape
import json
import shutil

from PIL import Image
from build_foundations import FOUND

PILOT = FOUND / 'visual/VISUAL_PILOT_REVIEW_PACKAGE'


def build_gallery():
    cards = {c['id']: c for c in json.loads((FOUND / 'reader/page-manifest.json').read_text())}
    specimens = PILOT / 'specimens'
    records = json.loads((specimens / 'MANIFEST.json').read_text())
    proxies = PILOT / 'display'
    proxies.mkdir(exist_ok=True)
    plates = []
    for path in sorted((PILOT / 'revised').glob('*.svg')):
        card = cards[path.stem]
        title = escape(card['title'])
        plate = f'''<section class="sheet" id="{path.stem}"><header><p>{path.stem} · Review candidate</p><h2>{title}</h2></header>
<p>{escape(card['objective'])}</p><div class="compare">
<figure><img src="original/{path.name}" alt="Predecessor conceptual figure"><figcaption>Predecessor figure</figcaption></figure>
<figure><img src="revised/{path.name}" alt="V01 technical graphic for {title}"><figcaption>V01 editable source · conceptual, not to scale</figcaption></figure></div>
<h3>Decision boundary</h3><p>{escape(card['stop']['text'])}</p><p class="hold">Qualified review pending · Publication HOLD</p></section>'''
        plates.append(plate)

    views = []
    proxy_receipt = []
    for item in records:
        native = specimens / item['file']
        if sha256(native.read_bytes()).hexdigest() != item['sha256']:
            raise ValueError(f'Original specimen bytes differ: {native.name}')
        view = proxies / native.name
        with Image.open(native) as original:
            original.thumbnail((1150, 1150))
            original.convert('RGB').save(view, quality=89)
        proxy_receipt.append({'file': view.name, 'original_sha256': item['sha256'],
                              'proxy_sha256': sha256(view.read_bytes()).hexdigest()})
        caption = f"{item['taxon_as_displayed']} · MIN {item['catalog_number']}"
        views.append(f'''<figure><img src="display/{view.name}" alt="Archive voucher image labeled {escape(caption)}">
<figcaption><strong>{escape(caption)}</strong><br>{escape(item['credit'])} · {escape(item['rights'])}.
{escape(item['limits'])} <a href="specimens/{native.name}">Original JPEG</a> ·
<a href="{escape(item['catalogue_url'])}">Catalogue record</a></figcaption></figure>''')
    (proxies / 'MANIFEST.json').write_text(json.dumps(proxy_receipt, indent=2) + '\n')

    specimen_plates = []
    for offset in range(0, len(views), 2):
        number = offset // 2 + 1
        specimen_plates.append(f'''<section class="sheet" id="voucher-{number}"><h2>Authentic voucher study images · Plate {number}</h2>
<p>Archival exhibits for source and view review. Diagnostic qualification is pending, and consumption remains withheld.</p>
<div class="compare">{''.join(views[offset:offset+2])}</div></section>''')
    html = f'''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>V01 visual pilot review package</title><link rel="stylesheet" href="pilot.css">
<main id="content"><header class="cover"><p>Survival Field Encyclopedia</p><h1>V01 visual pilot</h1>
<p>Review the original and revised technical illustrations, then examine the documented voucher media and its limits.</p>
<p class="hold">Editorial and visual review draft · Publication HOLD</p></header>
{''.join(plates)}{''.join(specimen_plates)}</main></html>'''
    (PILOT / 'index.html').write_text(html, encoding='utf-8')
    return 1 + len(plates) + len(specimen_plates)


def print_gallery(sheets):
    import pymupdf
    from playwright.sync_api import sync_playwright

    with sync_playwright() as driver:
        browser = driver.chromium.launch(executable_path=shutil.which('google-chrome') or shutil.which('chromium'))
        page = browser.new_page(offline=True, viewport={'width': 1280, 'height': 900})
        page.goto((PILOT / 'index.html').as_uri())
        page.locator('img').evaluate_all('(images) => Promise.all(images.map(img => img.decode()))')
        for fmt in ('Letter', 'A4'):
            path = PILOT / f'V01-review-{fmt.lower()}.pdf'
            page.pdf(path=path, format=fmt, print_background=True, tagged=True)
            with pymupdf.open(path) as proof:
                assert len(proof) == sheets, (fmt, len(proof), sheets)
                assert proof.xref_get_key(proof.pdf_catalog(), 'StructTreeRoot')[0] == 'xref'
                assert 'Publication HOLD' in proof[0].get_text()
                print(f'{path.name}: {sheets} tagged sheets')
        for width in (390, 1280):
            page.set_viewport_size({'width': width, 'height': 900})
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth+1')
            page.locator('#Z14-P54').screenshot(path=PILOT / f'pilot-{width}.png')
        browser.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--print', action='store_true', dest='render_print')
    args = parser.parse_args()
    count = build_gallery()
    if args.render_print:
        print_gallery(count)
