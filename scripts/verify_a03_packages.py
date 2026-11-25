"""Exercise the A03 core, standalone atlas and V01 pilot as extracted offline packages."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
from shutil import which
from subprocess import check_output
from tempfile import TemporaryDirectory
from zipfile import ZipFile

from playwright.sync_api import sync_playwright

from build_foundations import FOUND, require
from check_foundations import BUNDLE, PACKAGES_DIR
from verify_foundations import run_axe


def unpack(path, destination):
    with ZipFile(path) as archive:
        members = archive.namelist()
        require(all(not Path(name).is_absolute() and '..' not in Path(name).parts for name in members),
                f'Unsafe archive path in {path.name}')
        archive.extractall(destination)
    return sha256(path.read_bytes()).hexdigest()


def visit(page, path):
    page.goto(path.as_uri())
    require(page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1'),
            f'Horizontal overflow on {path.name}')
    require(page.locator('img').evaluate_all('(imgs) => imgs.every((i) => i.complete && i.naturalWidth > 0)'),
            f'Broken image on {path.name}')


def check_index_navigation(page, index, card_id, count):
    visit(page, index)
    require(page.locator('.catalog li').count() == count, f'Wrong catalog size in {index}')
    page.get_by_role('searchbox').fill(card_id)
    match = page.locator('.catalog li:not([hidden]) a')
    require(match.count() == 1, f'Broken search for {card_id}')
    match.click()
    require(page.url.endswith(f'/{card_id}.html'), f'Broken catalog link for {card_id}')


def changed_cards(reader):
    baseline = '8f1345b1b9a2df2efb52a777f446c61263fbffd8'
    changed = set()
    for filename, key in [('page-manifest.json', 'id'), ('asset-manifest.json', 'page')]:
        path = f'foundations/reader/{filename}'
        original = json.loads(check_output(['git', 'show', f'{baseline}:{path}'], cwd=FOUND.parent))
        prior = {row[key]: row for row in original}
        current = json.loads((reader / filename).read_text())
        changed.update(row[key] for row in current if row != prior[row[key]])
    return sorted(changed)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--axe', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    archives = (BUNDLE, PACKAGES_DIR / 'zone-Z16.zip', PACKAGES_DIR / 'v01-pilot.zip')
    receipt = {'archive_sha256': {}, 'viewports': [320, 390, 1280],
               'javascript_errors': [], 'http_requests': [], 'axe_violations': {}, 'axe_manual': {}}

    with TemporaryDirectory() as folder, sync_playwright() as pw:
        core, atlas, pilot = (Path(folder) / z for z in ('core', 'atlas', 'pilot'))
        for archive, destination in zip(archives, (core, atlas, pilot), strict=True):
            receipt['archive_sha256'][archive.name] = unpack(archive, destination)
        browser = pw.chromium.launch(executable_path=which('google-chrome') or which('chromium'))
        receipt['browser'] = browser.version
        reader = core / 'reader'
        changed = changed_cards(reader)
        receipt['changed_cards'] = len(changed)
        reports = {}
        for width in receipt['viewports']:
            context = browser.new_context(offline=True, viewport={'width': width, 'height': 900})
            page = context.new_page()
            page.on('pageerror', lambda error: receipt['javascript_errors'].append(str(error)))
            page.on('request', lambda request: receipt['http_requests'].append(request.url)
                    if request.url.startswith(('http:', 'https:')) else None)
            check_index_navigation(page, reader / 'index.html', 'Z16-P04', 1016)
            page.locator('a.atlas-link[href="Z13-P06.html"]').click()
            require(page.url.endswith('/Z13-P06.html'), 'Consolidated atlas lost its exact source target')
            visit(page, reader / 'directory.html')
            previous = page.locator('a[href^="history/"]').first.get_attribute('href')
            visit(page, reader / previous)

            visit(page, atlas / 'reader/index.html')
            page.get_by_role('link', name='Open this zone reader').click()
            check_index_navigation(page, atlas / 'reader/zones/Z16/index.html', 'Z16-P04', 75)
            require(page.locator('.external-zone-ref').filter(has_text='Z13-P06').count() > 0
                    and not page.locator('a[href="Z13-P06.html"]').count(), 'Standalone atlas has a broken cross-zone route')
            visit(page, pilot / 'index.html')
            require(page.locator('img').count() == 24, 'Pilot has incomplete comparison or voucher images')
            for card_id in changed:
                visit(page, reader / f'{card_id}.html')
            if width == 1280:
                targets = {card_id: reader / f'{card_id}.html' for card_id in changed}
                targets.update({'standalone-atlas': atlas / 'reader/Z16-P04.html',
                                'pilot-gallery': pilot / 'index.html'})
                for label, path in targets.items():
                    visit(page, path)
                    reports[label] = run_axe(page, args.axe)
                receipt['axe_version'] = page.evaluate('axe.version')
            context.close()
        browser.close()
    for label, report in reports.items():
        receipt['axe_violations'][label] = [issue['id'] for issue in report['violations']]
        receipt['axe_manual'][label] = [issue['id'] for issue in report['incomplete']]
    require(not receipt['http_requests'] and not receipt['javascript_errors']
            and not any(receipt['axe_violations'].values()), f'Packaged browser errors: {receipt}')
    args.output.write_text(json.dumps(receipt, indent=2) + '\n')
    print(f'PASS: three extracted archives, three viewport widths, {len(reports)} axe scans')


if __name__ == '__main__':
    main()
