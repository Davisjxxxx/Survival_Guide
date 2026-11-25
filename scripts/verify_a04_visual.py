"""Verify A04 cards, galleries, and print comparison proofs in offline Chromium."""
import argparse
import csv
from hashlib import sha256
import json
from pathlib import Path
from shutil import which

from bs4 import BeautifulSoup
import pymupdf
from playwright.sync_api import sync_playwright

from build_foundations import FOUND, require
from verify_foundations import run_axe

AUDIT = FOUND / 'audit/a04'
VISUAL = FOUND / 'visual'
COMPARISON = VISUAL / 'a04_comparison'
PILOT = VISUAL / 'v03_realistic/pilot'


def browser_visit(page, path):
    page.goto(path.as_uri())
    require(page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1'),
            f'Horizontal overflow on {path.name} at {page.viewport_size["width"]}')
    require(page.locator('img').evaluate_all(
        'images => images.every(i => i.complete && i.naturalWidth)'), f'Broken images on {path.name}')


def make_print_sources():
    pilot_pages = sorted(PILOT.glob('Z??-P??.html'))
    articles = []
    for file in pilot_pages:
        page = BeautifulSoup(file.read_text(encoding='utf-8'), 'html.parser')
        articles.append(str(page.select_one('article.card')))
    head = ''.join(f'<link rel="stylesheet" href="{css}">'
                   for css in ('library.css', 'edition.css', 'pilot.css'))
    paper = PILOT / 'print.html'
    paper.write_text('<!doctype html><html lang="en"><meta charset="utf-8">'
                     '<title>A04 generated instructional illustrations · Publication HOLD</title>'
                     f'{head}<body class="library foundation"><main>{"".join(articles)}</main></body></html>\n',
                     encoding='utf-8')


def print_proofs(page, write):
    specs = [(PILOT / 'print.html', PILOT, 'A04-generated', 2),
             (COMPARISON / 'atlas/index.html', COMPARISON / 'atlas', 'A04-compact-atlas', 9)]
    records = {}
    for source, folder, prefix, expected_sheets in specs:
        for paper in ('letter', 'a4'):
            output = folder / f'{prefix}-{paper}.pdf'
            if write:
                page.goto(source.as_uri())
                page.pdf(path=output, format=paper, tagged=True, print_background=True)
            with pymupdf.open(output) as doc:
                require(len(doc) == expected_sheets, f'{output.name}: {len(doc)} sheets, expected {expected_sheets}')
                catalog = doc.pdf_catalog()
                require(doc.xref_get_key(catalog, 'StructTreeRoot')[0] == 'xref',
                        f'Missing tagged structure in {output.name}')
                require(all(sheet.get_text().strip() for sheet in doc), f'Blank sheet in {output.name}')
                records[output.relative_to(FOUND).as_posix()] = dict(
                    sheets=len(doc), tagged=True, sha256=sha256(output.read_bytes()).hexdigest())
    return records


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--axe', type=Path, required=True)
    parser.add_argument('--write-proof', action='store_true')
    args = parser.parse_args()
    if args.write_proof:
        make_print_sources()
    with (AUDIT / 'V01_V02_VISUAL_QUALIFICATION.csv').open(newline='', encoding='utf-8') as file:
        plates = list(csv.DictReader(file))
    paths = {row['page_id']: FOUND / 'reader' / f"{row['page_id']}.html" for row in plates}
    galleries = {
        'technical-gallery': VISUAL / 'v02_technical/index.html',
        'photo-gallery': VISUAL / 'v03_authentic_photos/index.html',
        'v01-gallery': VISUAL / 'VISUAL_PILOT_REVIEW_PACKAGE/index.html',
        'atlas-comparison': COMPARISON / 'atlas/index.html',
        'pilot-shelter': PILOT / 'Z02-P14.html',
        'pilot-garden': PILOT / 'Z14-P03.html',
    }
    report = {'javascript_errors': [], 'network_requests': [], 'widths': [320, 390, 1280],
              'cards': len(paths), 'galleries_and_pilot_pages': len(galleries), 'axe_violations': {}, 'axe_manual': {}}
    with sync_playwright() as pw:
        browser = pw.chromium.launch(executable_path=which('google-chrome') or which('chromium'))
        report['chromium'] = browser.version
        for width in report['widths']:
            context = browser.new_context(offline=True, viewport={'width': width, 'height': 1050})
            page = context.new_page()
            page.on('pageerror', lambda error: report['javascript_errors'].append(str(error)))
            page.on('request', lambda request: report['network_requests'].append(request.url)
                    if request.url.startswith(('http:', 'https:')) else None)
            for name, path in {**paths, **galleries}.items():
                browser_visit(page, path)
                if width == 1280:
                    result = run_axe(page, args.axe)
                    report['axe_version'] = page.evaluate('axe.version')
                    report['axe_violations'][name] = [item['id'] for item in result['violations']]
                    report['axe_manual'][name] = [item['id'] for item in result['incomplete']]
                if args.write_proof and width in (390, 1280) and name in {
                        'Z04-P34', 'Z11-P30', 'pilot-shelter', 'pilot-garden', 'atlas-comparison'}:
                    element = page.locator('.sheet').nth(1) if name == 'atlas-comparison' else page.locator('article.card').first
                    element.screenshot(path=COMPARISON / 'context' / f'{name}-{width}.jpg',
                                       type='jpeg', quality=86)
            browser_visit(page, galleries['atlas-comparison'])
            links = page.locator('.after a')
            require(links.count() > 8, 'Compact comparison lost source navigation')
            for link in links.evaluate_all('links => links.map(x => x.getAttribute("href"))'):
                require((galleries['atlas-comparison'].parent / link).is_file(), 'Missing compact source destination')
            page.locator('.after a[href="sources/Z13-P06.html"]').first.focus()
            page.keyboard.press('Enter')
            page.wait_for_url('**/sources/Z13-P06.html')
            require('portable generators' in page.locator('h1').inner_text(), 'Wrong compact atlas destination')
            if width == 1280:
                report['proofs'] = print_proofs(page, args.write_proof)
            context.close()
        browser.close()
    require(not (report['javascript_errors'] or report['network_requests'] or any(report['axe_violations'].values())),
            f'Offline or automated accessibility failure: {report}')
    if args.write_proof:
        (AUDIT / 'BROWSER_AND_PROOF_QA.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(f'PASS: {len(paths)} cards at 3 widths, {len(galleries)} galleries/pilot pages, '
          f'{len(report["axe_violations"])} axe scans and 4 tagged comparison proofs')


if __name__ == '__main__':
    main()
