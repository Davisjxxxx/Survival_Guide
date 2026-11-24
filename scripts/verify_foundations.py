"""Exercise the standalone offline edition and produce QA and single-card-per-sheet Letter/A4 proofs."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import shutil
import tempfile
from xml.etree import ElementTree

import pymupdf
from PIL import Image, ImageDraw
from playwright.sync_api import sync_playwright

from build_foundations import active_zones, FOUND, FOUNDATIONAL_ZONES, crosswalk, require

PAPER_SIZES = {
    'letter': ('Letter', 612.0, 792.0),
    'a4': ('A4', 595.28, 841.89),
}


def check_contents(page, output, cards):
    page.goto((output / 'index.html').as_uri())
    require(page.locator('.catalog li').count() == len(cards), 'Contents count drift')
    page.keyboard.press('Tab')
    require(page.locator(':focus').get_attribute('href') == '#content', 'Keyboard skip missing')
    search = page.get_by_role('searchbox')
    search.fill(cards[-1]['id'])
    require(page.locator('.catalog li:not([hidden])').count() == 1, 'Search filter failed')
    page.locator('.catalog li:not([hidden]) a').click()
    require(page.locator('h1').inner_text() == cards[-1]['title'], 'Search navigation failed')
    if len(cards) > 1:
        page.get_by_role('link', name='Previous').click()
        require(page.locator('h1').inner_text() == cards[-2]['title'], 'Previous failed')
        page.get_by_role('link', name='Next').click()
        require(page.locator('h1').inner_text() == cards[-1]['title'], 'Next failed')


def check_zone_and_directory(page, output, cards):
    page.goto((output / 'directory.html').as_uri())
    require(page.locator('table.dir-table tbody tr').count() == 16, 'Directory must cover all 16 zones')
    for link in page.locator('a[href^="history/"]').evaluate_all('a=>a.map(x=>x.getAttribute("href"))'):
        require((output/link).is_file(), f'Missing offline historical target {link}')
    for zone in active_zones(cards):
        zcards = [c for c in cards if c['zone'] == zone]
        if not zcards:
            continue
        zpath = output / 'zones' / zone / 'index.html'
        require(zpath.exists(), f'Missing zone reader {zone}')
        page.goto(zpath.as_uri())
        require(page.locator('.catalog li').count() == len(zcards), f'Zone {zone} count drift')
        page.get_by_role('searchbox').fill(zcards[0]['id'])
        require(page.locator('.catalog li:not([hidden])').count() == 1, f'Zone {zone} search failed')


def print_card(page, card, targets, fmt_key):
    fmt_name, exp_w, exp_h = PAPER_SIZES[fmt_key]
    raw = page.pdf(
        format=fmt_name,
        print_background=True,
        prefer_css_page_size=False,
        margin={'top': '11mm', 'bottom': '11mm', 'left': '12mm', 'right': '12mm'},
    )
    with pymupdf.open(stream=raw, filetype='pdf') as single:
        require(len(single) == 1, f'Print overflow ({fmt_name}) on {card["id"]}: {len(single)} pages')
        rect = single[0].rect
        require(abs(rect.width - exp_w) < 4 and abs(rect.height - exp_h) < 4,
                f'Unexpected {fmt_name} page size on {card["id"]}: {rect.width:.1f}x{rect.height:.1f}')
        sheet = single[0].get_text()
        required = [card['id'], 'When it applies', 'Equipment', 'Actions', 'Verify',
                    'Stop or change course', 'Publication hold', 'Qualified review pending']
        if 'failure' in card:
            required.append('Failure recognition')
        joined = re.sub(r'(?<=\S)\n([-–—/])(?=\S)', r'\1', sheet)
        normal = ' '.join(re.sub(r'(?<=\S)([-–—/])\n(?=\S)', r'\1', joined).split())
        required.extend(card[field] for field in ('title', 'objective', 'applies', 'equipment'))
        statements = [*card['action'], card['verify'], card['stop']]
        if 'failure' in card:
            statements.append(card['failure'])
        for text_item in [*required, *[item['text'] for item in statements]]:
            require(' '.join(text_item.replace('**','').split()) in normal,
                    f'Print ({fmt_name}) missing content on {card["id"]}: {text_item}')
        for target_pdf in targets:
            target_pdf.insert_pdf(single)


def contact_sheet(pdf, cards, path):
    columns = 5 if len(cards) > 60 else 4
    width, height = (220, 292) if len(cards) > 60 else (270, 358)
    rows = (len(cards) + columns - 1) // columns
    image = Image.new('RGB', (columns * width, rows * height), '#e8e8e0')
    draw = ImageDraw.Draw(image)
    scale = 0.34 if len(cards) > 60 else 0.41
    for i, card in enumerate(cards):
        pix = pdf[i].get_pixmap(matrix=pymupdf.Matrix(scale, scale), alpha=False)
        thumb = Image.frombytes('RGB', (pix.width, pix.height), pix.samples)
        thumb.thumbnail((width - 12, height - 24))
        x, y = i % columns * width, i // columns * height
        image.paste(thumb, (x + 6, y + 19))
        draw.text((x + 6, y + 3), card['id'], fill='#173c31')
    image.save(path, quality=84)


def run_axe(page, axe_path):
    page.add_script_tag(path=str(axe_path.resolve()))
    return page.evaluate(
        '''async()=>await axe.run({runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa']}})'''
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--reader', type=Path, default=FOUND / 'reader')
    parser.add_argument('--proofs', type=Path, default=FOUND / 'proofs')
    parser.add_argument('--axe', type=Path)
    parser.add_argument('--browser-only', action='store_true', help='Run browser QA without writing legacy print proofs')
    parser.add_argument('--batch')
    parser.add_argument('--zone')
    parser.add_argument('--foundations-only', action='store_true')
    parser.add_argument('--formats', default='letter', help='Comma-separated: letter,a4')
    parser.add_argument('--write-zone-pdfs', action='store_true')
    parser.add_argument('--name', default='foundations')
    args = parser.parse_args()

    formats = [f.strip().lower() for f in args.formats.split(',') if f.strip()]
    require(formats and all(f in PAPER_SIZES for f in formats), f'Invalid formats: {args.formats}')

    if args.browser_only:
        formats = []
        require(not args.write_zone_pdfs,'Use tagged print separately from browser-only QA')

    output, proofs = args.reader.resolve(), args.proofs.resolve()
    proofs.mkdir(parents=True, exist_ok=True)
    cards = json.loads((output / 'page-manifest.json').read_text(encoding='utf-8'))
    assets = json.loads((output / 'asset-manifest.json').read_text(encoding='utf-8'))

    for pdf_path in sorted((FOUND.parent / 'reader').glob('B0*.pdf')):
        page_numbers = []
        for row in crosswalk():
            if row['artifact'] == pdf_path.name:
                limits = list(map(int, row['pages'].split('–')))
                page_numbers.extend(range(limits[0], limits[-1] + 1))
        with pymupdf.open(pdf_path) as original:
            require(sorted(page_numbers) == list(range(1, len(original) + 1)),
                    f'Crosswalk does not uniquely cover {pdf_path.name}')

    require(len(cards) == len(assets) == len({c['id'] for c in cards}), 'Missing or duplicate card/asset')
    require({a['page'] for a in assets} == {c['id'] for c in cards}, 'Orphaned figure')
    for asset in assets:
        raw = (output / asset['file']).read_bytes()
        require(hashlib.sha256(raw).hexdigest() == asset['sha256'] and asset['diagnostic_photo'] is False,
                f'Figure authenticity metadata mismatch: {asset["id"]}')
        svg = ElementTree.fromstring(raw)
        require(svg.tag == '{http://www.w3.org/2000/svg}svg' and not any(
            tag.tag.rsplit('}', 1)[-1] in {'image', 'script', 'foreignObject'}
            or any(k.rsplit('}', 1)[-1] in {'href', 'src'} for k in tag.attrib)
            for tag in svg.iter()), f'Nonlocal or invalid visual {asset["id"]}')

    chosen = [
        card for card in cards
        if (not args.batch or card['batch'] == args.batch)
        and (not args.zone or card['zone'] == args.zone)
        and (not args.foundations_only or card['zone'] in FOUNDATIONAL_ZONES)
    ]
    require(chosen, 'No cards in selected scope')
    chosen_ids = {c['id'] for c in chosen}

    shots = []
    widths = (320, 390, 1280)
    reports = {
        'tested_cards': len(cards),
        'printed_cards': len(chosen) if formats else 0,
        'formats': formats,
        'widths': list(widths),
        'actual_browser_errors': [],
        'http_requests': [],
        'axe_incomplete': {},
        'axe_violations': {},
    }
    pdfs = {fmt: pymupdf.open() for fmt in formats}
    zone_pdfs = {
        (z, fmt): pymupdf.open()
        for z in FOUNDATIONAL_ZONES for fmt in formats
    } if args.write_zone_pdfs else {}
    recon_pdf = pymupdf.open() if args.write_zone_pdfs else None

    try:
        with sync_playwright() as pw, tempfile.TemporaryDirectory(dir=proofs) as tmp:
            browser = pw.chromium.launch(executable_path=shutil.which('google-chrome') or shutil.which('chromium'))
            reports['chromium'] = browser.version
            for width in widths:
                context = browser.new_context(viewport={'width': width, 'height': 920}, offline=True)
                page = context.new_page()
                page.on('pageerror', lambda e: reports['actual_browser_errors'].append(str(e)))
                page.on('request', lambda q: reports['http_requests'].append(q.url) if q.url.startswith(('http:', 'https:')) else None)
                check_contents(page, output, cards)
                check_zone_and_directory(page, output, cards)
                if args.axe and width == 1280:
                    for slug, target in [('index', output / 'index.html'), ('directory', output / 'directory.html')]:
                        page.goto(target.as_uri())
                        result = run_axe(page, args.axe)
                        reports['axe_version'] = page.evaluate('axe.version')
                        reports['axe_incomplete'][slug] = [i['id'] for i in result['incomplete']]
                        reports['axe_violations'][slug] = [i['id'] for i in result['violations']]
                    for zone in active_zones(cards):
                        if not any(c['zone'] == zone for c in cards):
                            continue
                        page.goto((output / 'zones' / zone / 'index.html').as_uri())
                        result = run_axe(page, args.axe)
                        reports['axe_incomplete'][f'zone-{zone}'] = [i['id'] for i in result['incomplete']]
                        reports['axe_violations'][f'zone-{zone}'] = [i['id'] for i in result['violations']]

                cards_to_visit = cards if (not args.batch and not args.zone) else chosen
                for card in cards_to_visit:
                    page.goto((output / f'{card["id"]}.html').as_uri())
                    require(
                        page.locator('h1').inner_text() == card['title']
                        and page.evaluate('document.documentElement.scrollWidth <= innerWidth+1')
                        and page.locator('figure img').evaluate_all('(imgs) => imgs.length > 0 && imgs.every((i) => i.complete && i.naturalWidth > 0)'),
                        f'Layout, content or figure failed at {width}: {card["id"]}',
                    )
                    expected_markers = len(card['action']) + 2 + (1 if 'failure' in card else 0)
                    require(page.locator('[data-claims]').count() == expected_markers,
                            f'Missing evidence markers on {card["id"]}')
                    if args.axe and width == 1280:
                        result = run_axe(page, args.axe)
                        reports['axe_incomplete'][card['id']] = [i['id'] for i in result['incomplete']]
                        reports['axe_violations'][card['id']] = [i['id'] for i in result['violations']]
                    if width in (390, 1280) and card == chosen[0]:
                        shot = Path(tmp) / f'{args.name}-{width}.png'
                        page.screenshot(path=shot, full_page=True)
                        shots.append(shot)
                    if width == 1280 and card['id'] in chosen_ids:
                        for fmt in formats:
                            targets = [pdfs[fmt]]
                            if args.write_zone_pdfs and card['zone'] in FOUNDATIONAL_ZONES:
                                targets.append(zone_pdfs[(card['zone'], fmt)])
                            print_card(page, card, targets, fmt)
                    if width == 1280 and args.write_zone_pdfs and card['zone'] not in FOUNDATIONAL_ZONES:
                        print_card(page, card, [recon_pdf], 'letter')
                context.close()
            browser.close()

            require(not reports['actual_browser_errors'] and not reports['http_requests']
                    and not any(reports['axe_violations'].values()), f'Browser checks failed: {reports}')

            toc = [[1, card['id'] + ' · ' + card['title'], i] for i, card in enumerate(chosen, 1)]
            for fmt in formats:
                pdf = pdfs[fmt]
                require(len(pdf) == len(chosen), f'Unexpected {fmt} PDF page count')
                pdf.set_toc(toc)
                pdf.set_metadata({'title': f'Survival Field Encyclopedia · {args.name} ({fmt.upper()})',
                                  'subject': 'Editorial review draft'})
                out_name = f'{args.name}-{fmt}.pdf' if args.zone else (f'{args.name}.pdf' if fmt == 'letter' else f'{args.name}-{fmt}.pdf')
                pdf.save(proofs / out_name, garbage=4, deflate=True)

            if args.write_zone_pdfs:
                for zone in FOUNDATIONAL_ZONES:
                    zcards = [c for c in chosen if c['zone'] == zone]
                    ztoc = [[1, card['id'] + ' · ' + card['title'], i] for i, card in enumerate(zcards, 1)]
                    for fmt in formats:
                        zpdf = zone_pdfs[(zone, fmt)]
                        require(len(zpdf) == len(zcards), f'Unexpected zone {zone} {fmt} page count')
                        zpdf.set_toc(ztoc)
                        zpdf.set_metadata({'title': f'Survival Field Encyclopedia · {zone} ({fmt.upper()})',
                                           'subject': 'Editorial review draft'})
                        zpdf.save(proofs / f'{zone}-{fmt}.pdf', garbage=4, deflate=True)
                rcards = [c for c in cards if c['zone'] not in FOUNDATIONAL_ZONES]
                if rcards and len(recon_pdf) == len(rcards):
                    recon_pdf.set_toc([[1, c['id'] + ' · ' + c['title'], i] for i, c in enumerate(rcards, 1)])
                    recon_pdf.set_metadata({'title': 'Survival Field Encyclopedia · Reconstructions (LETTER)',
                                            'subject': 'Editorial review draft'})
                    recon_pdf.save(proofs / 'reconstructions.pdf', garbage=4, deflate=True)

            if formats:
                contact_sheet(pdfs[formats[0]], chosen, proofs / f'{args.name}-contact.jpg')
            for shot in shots:
                shutil.copyfile(shot, proofs / shot.name)
    finally:
        for pdf in pdfs.values():
            pdf.close()
        for pdf in zone_pdfs.values():
            pdf.close()
        if recon_pdf is not None:
            recon_pdf.close()

    reports['zones'] = dict(Counter(c['zone'] for c in chosen))
    (proofs / f'{args.name}-qa.json').write_text(json.dumps(reports, indent=2) + '\n', encoding='utf-8')
    print(f'PASS: {len(cards)} cards checked at {len(widths)} widths, {len(chosen)} printed sheets x {formats}, '
          f'{len(reports["axe_violations"])} axe audits; no HTTP requests or JavaScript errors.')


if __name__ == '__main__':
    main()
