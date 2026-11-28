"""Inspect a Wave 2C batch in its actual reader pages and print proofs.

For every plate in the batch (from foundations/audit/w2c/W2C_BATCHES.json):
* open the reader page offline at 390 and 1280 px, require no horizontal
  overflow, loaded images and no network requests, and run axe-core (WCAG 2.1
  A/AA) at 1280 px;
* capture the card from its title through the figure caption at both widths;
* render the preserved predecessor beside the revision, in colour and grayscale;
* print the batch pages to tagged Letter and A4 PDFs and check them with the
  established proof inspection (content, section order, margins, figure alt
  text and bookmarks), then rasterize each sheet (Letter in colour, A4 in grayscale).

Outputs go to foundations/visual/w2c_context/<batch>/ with a receipt
foundations/visual/w2c_technical/qa/<batch>-VISUAL-QA.json.
"""
import argparse
import base64
from hashlib import sha256
from html import escape
from io import BytesIO
import json
from pathlib import Path
from shutil import which
import tempfile

from PIL import Image, ImageDraw, ImageOps
import pymupdf
from playwright.sync_api import sync_playwright

from build_foundations import FOUND, require
from print_foundations_tagged import content, inspect
from verify_foundations import run_axe

W2C = FOUND / 'visual/w2c_technical'
CONTEXT = FOUND / 'visual/w2c_context'
LEDGER = FOUND / 'audit/w2c/W2C_BATCHES.json'
READER = FOUND / 'reader'
BG = (238, 236, 226)


def batch_pages(batch):
    data = json.loads(LEDGER.read_text(encoding='utf-8'))
    for entry in data['batches']:
        if entry['batch'] == batch:
            return [p['page_id'] for p in entry['plates'] if p['disposition'] == 'PROVISIONAL_EDITORIAL_CANDIDATE']
    raise SystemExit(f'Unknown batch {batch}')


def render_svg(page, path, width):
    data = base64.b64encode(path.read_bytes()).decode()
    page.set_content(f'<meta charset="utf-8"><style>body{{margin:0;background:#fff}}img{{display:block;width:{width}px}}'
                     f'</style><img src="data:image/svg+xml;base64,{data}">')
    page.wait_for_timeout(30)
    return Image.open(BytesIO(page.locator('img').screenshot())).convert('RGB')


def card_capture(page):
    card = page.locator('article.card').bounding_box()
    fig = page.locator('article.card figure').first.bounding_box()
    clip = dict(x=card['x'], y=card['y'], width=card['width'], height=fig['y'] + fig['height'] - card['y'] + 8)
    return Image.open(BytesIO(page.screenshot(clip=clip, full_page=True))).convert('RGB')


def sheet(tiles, columns, label_h=22, pad=10):
    """tiles: list of (label, image). Returns a contact sheet image."""
    w = max(im.width for _, im in tiles)
    h = max(im.height for _, im in tiles)
    rows = (len(tiles) + columns - 1) // columns
    out = Image.new('RGB', (columns * (w + pad) + pad, rows * (h + label_h + pad) + pad), BG)
    draw = ImageDraw.Draw(out)
    for i, (label, im) in enumerate(tiles):
        x = pad + (i % columns) * (w + pad)
        y = pad + (i // columns) * (h + label_h + pad)
        draw.text((x, y + 4), label, fill=(23, 60, 49))
        out.paste(im, (x, y + label_h))
    return out


def fit(im, width):
    if im.width <= width:
        return im
    return im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('batch')
    parser.add_argument('--axe', type=Path, required=True)
    args = parser.parse_args()
    pages = batch_pages(args.batch)
    require(pages, f'No provisional plates in {args.batch}')
    out = CONTEXT / args.batch
    out.mkdir(parents=True, exist_ok=True)
    cards = {c['id']: c for c in json.loads((READER / 'page-manifest.json').read_text(encoding='utf-8'))}
    report = dict(batch=args.batch, pages=pages, widths=[390, 1280], network_requests=[], javascript_errors=[],
                  axe_violations={}, axe_incomplete={}, figure_alt={}, outputs={})
    compare, compare_gray, phone, desktop = [], [], [], []
    with sync_playwright() as pw:
        browser = pw.chromium.launch(executable_path=which('google-chrome') or which('chromium'))
        report['chromium'] = browser.version
        scratch = browser.new_page(offline=True, viewport={'width': 1000, 'height': 900})
        for pid in pages:
            before = render_svg(scratch, W2C / 'original' / f'{pid}.svg', 600)
            after = render_svg(scratch, W2C / 'revised' / f'{pid}.svg', 600)
            compare += [(f'{pid} preserved predecessor', before), (f'{pid} W2C revision', after)]
            compare_gray += [(f'{pid} predecessor (grayscale)', ImageOps.grayscale(before).convert('RGB')),
                             (f'{pid} revision (grayscale)', ImageOps.grayscale(after).convert('RGB'))]
        for width in report['widths']:
            context = browser.new_context(offline=True, viewport={'width': width, 'height': 1000})
            page = context.new_page()
            page.on('pageerror', lambda e: report['javascript_errors'].append(str(e)))
            page.on('request', lambda r: report['network_requests'].append(r.url)
                    if r.url.startswith(('http:', 'https:')) else None)
            for pid in pages:
                page.goto((READER / f'{pid}.html').as_uri())
                require(page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1'),
                        f'Horizontal overflow on {pid} at {width}px')
                require(page.locator('img').evaluate_all('i => i.every(x => x.complete && x.naturalWidth)'),
                        f'Broken image on {pid} at {width}px')
                shot = card_capture(page)
                if width == 390:
                    phone.append((f'{pid} · 390 px reader', fit(shot, 390)))
                else:
                    desktop.append((f'{pid} · 1280 px reader', fit(shot, 640)))
                    alt = page.locator('article.card figure img').first.get_attribute('alt')
                    require(alt and len(alt) > 80, f'Uninformative figure alternative text on {pid}')
                    report['figure_alt'][pid] = alt
                    result = run_axe(page, args.axe)
                    report['axe_violations'][pid] = [v['id'] for v in result['violations']]
                    report['axe_incomplete'][pid] = [v['id'] for v in result['incomplete']]
            context.close()
        # tagged batch proofs in both paper sizes, inspected with the established proof checks
        selection = [cards[p] for p in pages]
        sections = ''.join(content(READER, c) for c in selection)
        proof_tiles = []
        with tempfile.TemporaryDirectory() as tmp:
            html = Path(tmp) / 'proof.html'
            html.write_text('<!doctype html><html lang="en"><meta charset="utf-8">'
                            f'<title>Survival Field Encyclopedia · {escape(args.batch)} · Publication HOLD</title>'
                            f'<link rel="stylesheet" href="{(READER / "library.css").as_uri()}">'
                            f'<link rel="stylesheet" href="{(READER / "edition.css").as_uri()}">'
                            '<style>.proof+.proof{break-before:page}</style>'
                            f'<body class="library foundation"><main>{sections}</main></body></html>', encoding='utf-8')
            page = browser.new_page(offline=True)
            page.goto(html.as_uri())
            for paper in ('letter', 'a4'):
                target = out / f'{args.batch}-{paper}.pdf'
                page.pdf(path=str(target), format=paper.capitalize() if paper == 'letter' else 'A4',
                         print_background=True, tagged=True)
                inspect(target, selection, paper)
                report['outputs'][target.relative_to(FOUND).as_posix()] = dict(
                    inspection=inspect(target, selection, paper, bookmarks=True),
                    sha256=sha256(target.read_bytes()).hexdigest())
                with pymupdf.open(target) as doc:
                    for pid, sheet_page in zip(pages, doc):
                        pix = sheet_page.get_pixmap(matrix=pymupdf.Matrix(0.62, 0.62), alpha=False)
                        im = Image.frombytes('RGB', (pix.width, pix.height), pix.samples)
                        if paper == 'a4':
                            im = ImageOps.grayscale(im).convert('RGB')
                        proof_tiles.append((f'{pid} · {paper.upper()}{" grayscale" if paper == "a4" else ""}', im))
        browser.close()
    require(not report['network_requests'] and not report['javascript_errors']
            and not any(report['axe_violations'].values()), f'Offline or accessibility failure: {report}')
    proof_tiles.sort(key=lambda t: (pages.index(t[0].split(' · ')[0]), t[0]))
    images = {
        f'{args.batch}-compare.jpg': sheet(compare, 2),
        f'{args.batch}-compare-gray.jpg': sheet(compare_gray, 2),
        f'{args.batch}-phone.jpg': sheet(phone, min(4, len(phone))),
        f'{args.batch}-desktop.jpg': sheet(desktop, 2),
        f'{args.batch}-print.jpg': sheet(proof_tiles, 4),
    }
    for name, im in images.items():
        target = out / name
        im.save(target, quality=74, optimize=True)
        report['outputs'][target.relative_to(FOUND).as_posix()] = dict(sha256=sha256(target.read_bytes()).hexdigest(),
                                                                       size=list(im.size))
    receipt = W2C / 'qa' / f'{args.batch}-VISUAL-QA.json'
    receipt.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(f'PASS: {args.batch} · {len(pages)} pages at 390/1280 px, {len(pages)} axe scans, tagged Letter/A4 proofs; '
          f'captures in {out.relative_to(FOUND)}')


if __name__ == '__main__':
    main()
