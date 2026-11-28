"""Check frozen-path custody, review assets, zone PDFs, and the offline package without network or browser."""
import argparse
from hashlib import sha256
import json
from html import escape, unescape
from html.parser import HTMLParser
from posixpath import dirname, join, normpath
import re
from pathlib import Path
import subprocess
import sys
import tempfile
from urllib.parse import urlsplit
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

from build_foundations import FOUND, ROOT, ZONES, doc, require

BASE = '890c66ac1d51465d3a4315e50fb2dbe1e0f78f6f'
BUNDLE = FOUND / 'proofs/foundations-offline.zip'
PACKAGES_DIR = FOUND / 'proofs/packages'
PILOT_DIR = FOUND / 'visual/VISUAL_PILOT_REVIEW_PACKAGE'
VISUAL_COMPANION_DIRS = (
    ('v02-technical.zip', FOUND / 'visual/v02_technical', 'Original and reconstructed V02 editable technical SVGs, comparison gallery and proofs'),
    ('v03-realistic.zip', FOUND / 'visual/v03_realistic', 'Controlled realistic instructional illustration briefs, generated non-diagnostic illustrations and proofs'),
    ('v03-authentic-photos.zip', FOUND / 'visual/v03_authentic_photos', 'Authentic V03 acquired photographs, display derivatives and full provenance manifests'),
    ('v02-atlas-comparison.zip', FOUND / 'visual/v02_atlas_comparison', 'Z16 atlas before-and-after optimization comparison package pending owner acceptance'),
    ('a04-review.zip', FOUND / 'visual/a04_comparison', 'A04 actual reader comparison captures, incoming plate custody, and linked atlas owner comparison'),
    ('w2c-technical.zip', FOUND / 'visual/w2c_technical', 'Wave 2C technical plates: preserved predecessors, revised editable SVGs, geometry and topology receipts and visual QA receipts'),
    ('w2c-authentic-photos.zip', FOUND / 'visual/w2c_authentic_photos', 'Wave 2C open-licence provider originals, EXIF-corrected display copies, acquisition records and rights register'),
    ('w2c-context.zip', FOUND / 'visual/w2c_context', 'Wave 2C actual reader captures at 390 and 1280 px, predecessor comparisons in colour and grayscale, and tagged Letter/A4 batch proofs'),
)
MAX_GITHUB_SAFE_BYTES = 45 * 1024 * 1024  # Strictly under GitHub's 50 MB warning and 100 MB hard limit


def hash_bytes(data):
    return sha256(data).hexdigest()


def verify_generation():
    with tempfile.TemporaryDirectory() as temp:
        generated = Path(temp)
        subprocess.run([sys.executable, str(ROOT / 'scripts/build_foundations.py'),
                        '--output', str(generated)], check=True)
        fresh = {p.relative_to(generated).as_posix(): hash_bytes(p.read_bytes())
                 for p in generated.rglob('*') if p.is_file()}
    reader = FOUND / 'reader'
    retained = {p.relative_to(reader).as_posix(): hash_bytes(p.read_bytes())
                for p in reader.rglob('*') if p.is_file()}
    require(fresh == retained, 'Checked-in reader differs from canonical build')


def verify_photos():
    directory = FOUND / 'evidence/photos'
    records = json.loads((directory / 'manifest.json').read_text(encoding='utf-8'))
    manifests = {a['file']: a for a in records}
    require(len(manifests) == len(records), 'Duplicate photo file')
    files = {p.name for p in directory.glob('*.jpg')}
    require(files == set(manifests), 'Photo manifest differs from retained files')
    for filename, record in manifests.items():
        data = (directory / filename).read_bytes()
        require(
            data[:2] == b'\xff\xd8' and hash_bytes(data) == record['sha256']
            and record['rights'] == 'Public Domain' and record['classification'] == 'Documentary context'
            and record['diagnostic_photo'] is False
            and all(record[k].startswith('https://') for k in ('source', 'download')),
            f'Photo provenance check failed: {filename}',
        )


def verify_retained_pdfs():
    proofs = FOUND / 'proofs'
    receipt_path = proofs / 'tagged-print-qa.json'
    if receipt_path.is_file():
        receipt = json.loads(receipt_path.read_text())
        required = {'encyclopedia-letter.pdf', 'encyclopedia-a4.pdf'}
        require(required <= set(receipt), 'Missing consolidated tagged proof receipt')
        for name, record in receipt.items():
            digest = hash_bytes((proofs / name).read_bytes())
            require(digest == record['sha256'], f'Tagged proof receipt differs from {name}')
    for pdf in sorted(proofs.glob('*.pdf')):
        head = pdf.read_bytes()[:5]
        require(head == b'%PDF-' and pdf.stat().st_size > 10_000, f'Invalid PDF proof: {pdf.name}')
    verify_proof_currency(proofs)


def verify_proof_currency(proofs):
    """RT01-06: a receipted proof must have been printed from the current manuscripts, figures and
    print styles. A stale proof fails unless PROOF-CURRENCY.json withholds it with exactly the
    changed pages, and packaged proofs (zone editions, reconstructions) can never be withheld."""
    from proof_inputs import PACKAGED_PROOF_NAMES, edition_of, editions, fingerprint, stale_pages
    receipt = json.loads((proofs / 'tagged-print-qa.json').read_text())
    reader = FOUND / 'reader'
    cards = json.loads((reader / 'page-manifest.json').read_text(encoding='utf-8'))
    by_name = editions(cards)
    cache, stale = {}, {}
    for filename, record in receipt.items():
        name = edition_of(filename)
        require(name in by_name, f'Receipted proof for an unknown edition: {filename}')
        require('page_inputs' in record and 'style_inputs' in record,
                f'{filename}: receipt records no source-input fingerprint; reprint it')
        changed = stale_pages(record, fingerprint(reader, by_name[name], cache))
        if changed:
            stale[filename] = changed
    currency_path = proofs / 'PROOF-CURRENCY.json'
    currency = json.loads(currency_path.read_text()) if currency_path.is_file() else {'withheld': {}}
    withheld = currency.get('withheld', {})
    for filename, pages in stale.items():
        require(edition_of(filename) not in PACKAGED_PROOF_NAMES,
                f'Packaged proof {filename} is stale ({len(pages)} pages changed, e.g. {pages[:3]}); '
                f'reprint it with print_foundations_tagged.py --editions {edition_of(filename)}')
        require(filename in withheld and sorted(withheld[filename].get('pages', [])) == pages,
                f'Stale proof {filename} ({len(pages)} pages changed, e.g. {pages[:3]}) is neither reprinted '
                'nor withheld with exactly those pages in PROOF-CURRENCY.json')
    require(set(withheld) <= set(stale), f'PROOF-CURRENCY.json withholds current proofs: {sorted(set(withheld) - set(stale))}')


def package_members(include_consolidated_pdfs=False):
    files = [p for path in ('reader', 'manuscripts', 'evidence', 'audit', 'visual') for p in (FOUND / path).rglob('*') if p.is_file()]
    if not include_consolidated_pdfs:
        excluded_dirs = (PILOT_DIR,) + tuple(d for _, d, _ in VISUAL_COMPANION_DIRS)
        files = [p for p in files if not any(p.is_relative_to(d) for d in excluded_dirs)]
    files.extend([FOUND / 'README.md', FOUND / 'SPRINT_RESULT.md'])
    for extra in ('ZONE_COMPLETION_MATRIX.csv', 'ASTRA_ESCALATION_REGISTER.md'):
        path = FOUND / extra
        if path.exists():
            files.append(path)
    pdf_names = ['reconstructions.pdf']
    if include_consolidated_pdfs:
        pdf_names.extend(['foundations.pdf', 'foundations-a4.pdf', 'encyclopedia-letter.pdf', 'encyclopedia-a4.pdf'])
    for pdf_name in pdf_names:
        pdf = FOUND / 'proofs' / pdf_name
        if pdf.exists():
            files.append(pdf)
    receipt = FOUND / 'proofs/tagged-print-qa.json'
    if receipt.is_file():
        files.append(receipt)
    entries = {path.relative_to(FOUND).as_posix(): path.read_bytes() for path in sorted(set(files))}
    if PILOT_DIR.is_dir() and not include_consolidated_pdfs:
        pilot_notice = ('<!doctype html><html lang="en"><meta charset="utf-8"><title>V01 companion archive</title>'
                        '<main><h1>V01 companion archive</h1><p>Extract the separate v01-pilot.zip package '
                        'and open its index.html for the full gallery, archival media and proofs.</p></main></html>')
        key = (PILOT_DIR / 'index.html').relative_to(FOUND).as_posix()
        entries[key] = pilot_notice.encode('utf-8')
    return entries


def package_payload(include_consolidated_pdfs=False):
    entries = package_members(include_consolidated_pdfs=include_consolidated_pdfs)
    entries['PACKAGE-SHA256.txt'] = ''.join(
        f'{hash_bytes(data)}  {name}\n' for name, data in entries.items()
    ).encode('utf-8')
    return entries


def local_target(page, href):
    target = urlsplit(unescape(href))
    if target.scheme or target.netloc or not target.path:
        return None
    return normpath(join(dirname(page), target.path))


def scope_zone_links(page, html, available):
    """Keep links within the extracted zone and label references to other packages."""
    def replace(match):
        href, label = match.groups()
        destination = local_target(page, href)
        if destination and destination not in available:
            return f'<span class="external-zone-ref">{label} (full edition)</span>'
        return match[0]

    return re.sub(r'<a\b[^>]*\bhref="([^"]+)"[^>]*>(.*?)</a>', replace, html, flags=re.S)


class LocalAssetCheck(HTMLParser):
    def __init__(self, page, available):
        super().__init__()
        self.page = page
        self.available = available

    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if name in {'href', 'src'} and value:
                destination = local_target(self.page, value)
                require(not destination or destination in self.available,
                        f'Broken packaged reference on {self.page}: {value}')


def zone_package_payload(zone, cards_manifest):
    zone_ids = {c['id'] for c in cards_manifest if c['zone'] == zone}
    files = []
    reader = FOUND / 'reader'
    for base_asset in ('library.css', 'edition.css', 'search.js', 'page-manifest.json', 'asset-manifest.json'):
        p = reader / base_asset
        if p.is_file():
            files.append(p)
    zreader = reader / 'zones' / zone / 'index.html'
    if zreader.is_file():
        files.append(zreader)
    for cid in sorted(zone_ids):
        for rel in (f'{cid}.html', f'visuals/{cid}.svg'):
            p = reader / rel
            if p.is_file():
                files.append(p)
    if zone == 'Z11' and (reader / 'maps/ely-1965.jpg').is_file():
        files.append(reader / 'maps/ely-1965.jpg')
    for ev in ('sources.tsv', 'claims.tsv', 'photo-requirements.tsv'):
        p = FOUND / 'evidence' / ev
        if p.is_file():
            files.append(p)
    for pdf_name in (f'{zone}-letter.pdf', f'{zone}-a4.pdf'):
        p = FOUND / 'proofs' / pdf_name
        if p.is_file():
            files.append(p)
    for filename in ('ZONE_COMPLETION_MATRIX.csv', 'SPRINT_RESULT.md'):
        p = FOUND / filename
        if p.is_file():
            files.append(p)
    entries = {path.relative_to(FOUND).as_posix(): path.read_bytes() for path in sorted(set(files))}
    label = f'{zone} · {ZONES[zone]}'
    landing = doc(label, '<main id="content"><h1>' + escape(label) + '</h1>'
                  + f'<p><a href="zones/{zone}/index.html">Open this zone reader</a></p>'
                  + '<p>This archive contains one zone. Use the complete offline edition for other zones and the historical library.</p></main>')
    entries['reader/index.html'] = landing.encode('utf-8')
    entries['reader/directory.html'] = landing.encode('utf-8')
    for manifest, key in [('page-manifest.json', 'id'), ('asset-manifest.json', 'page')]:
        path = 'reader/' + manifest
        records = json.loads(entries[path])
        entries[path] = (json.dumps([r for r in records if r[key] in zone_ids], ensure_ascii=False, indent=2)
                         + '\n').encode('utf-8')
    for page in entries:
        if page.endswith('.html'):
            html = scope_zone_links(page, entries[page].decode('utf-8'), entries)
            LocalAssetCheck(page, entries).feed(html)
            entries[page] = html.encode('utf-8')
    entries['PACKAGE-SHA256.txt'] = ''.join(
        f'{hash_bytes(data)}  {name}\n' for name, data in entries.items()
    ).encode('utf-8')
    return entries


def write_deterministic_zip(dest, entries):
    dest.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=dest.parent) as temp:
        path = Path(temp) / dest.name
        with ZipFile(path, 'w') as zip_file:
            for name, data in entries.items():
                member = ZipInfo(name, (2026, 11, 25, 0, 0, 0))
                member.compress_type = ZIP_DEFLATED
                member.external_attr = 0o100644 << 16
                zip_file.writestr(member, data)
        path.replace(dest)


def verify_zip_entries(zip_path, entries, enforce_size_limit=True):
    if enforce_size_limit:
        require(zip_path.stat().st_size <= MAX_GITHUB_SAFE_BYTES,
                f'Archive exceeds GitHub-safe 45 MB ceiling: {zip_path.name} ({zip_path.stat().st_size} bytes)')
    with ZipFile(zip_path) as zipped:
        require(
            zipped.testzip() is None
            and sorted(zipped.namelist()) == sorted(entries)
            and all(hash_bytes(zipped.read(name)) == hash_bytes(data) for name, data in entries.items()),
            f'Archive does not match deterministic payload: {zip_path.name}',
        )


def write_or_verify_zone_packages(write=False):
    cards = json.loads((FOUND / 'reader/page-manifest.json').read_text(encoding='utf-8'))
    zones = sorted({c['zone'] for c in cards if c['id'][4] == 'P'})
    manifest = {}
    if write:
        PACKAGES_DIR.mkdir(parents=True, exist_ok=True)
    for zone in zones:
        zpath = PACKAGES_DIR / f'zone-{zone}.zip'
        entries = zone_package_payload(zone, cards)
        if write:
            write_deterministic_zip(zpath, entries)
        verify_zip_entries(zpath, entries, enforce_size_limit=True)
        manifest[f'packages/zone-{zone}.zip'] = {
            'zone': zone,
            'pages': sum(1 for c in cards if c['zone'] == zone),
            'members': len(entries) - 1,
            'bytes': zpath.stat().st_size,
            'sha256': hash_bytes(zpath.read_bytes()),
        }
    manifest['foundations-offline.zip'] = {
        'scope': 'Core offline HTML reader, SVGs, manuscripts, evidence, audit registers & reconstructions (consolidated PDFs kept separately in proofs/ for GitHub scalability)',
        'members': len(package_payload(False)) - 1,
        'bytes': BUNDLE.stat().st_size,
        'sha256': hash_bytes(BUNDLE.read_bytes()),
    }
    if PILOT_DIR.is_dir():
        pilot = PACKAGES_DIR / 'v01-pilot.zip'
        entries = {p.relative_to(PILOT_DIR).as_posix(): p.read_bytes()
                   for p in sorted(PILOT_DIR.rglob('*')) if p.is_file()}
        entries['PACKAGE-SHA256.txt'] = ''.join(
            f'{hash_bytes(data)}  {name}\n' for name, data in entries.items()
        ).encode('utf-8')
        if write:
            write_deterministic_zip(pilot, entries)
        verify_zip_entries(pilot, entries)
        manifest['packages/v01-pilot.zip'] = {
            'scope': 'Original and revised V01 plates, review proofs and authentic voucher study media',
            'members': len(entries) - 1,
            'bytes': pilot.stat().st_size,
            'sha256': hash_bytes(pilot.read_bytes()),
        }
    for zip_name, comp_dir, comp_scope in VISUAL_COMPANION_DIRS:
        if comp_dir.is_dir():
            cpath = PACKAGES_DIR / zip_name
            centries = {p.relative_to(comp_dir).as_posix(): p.read_bytes()
                        for p in sorted(comp_dir.rglob('*')) if p.is_file()}
            if centries:
                centries['PACKAGE-SHA256.txt'] = ''.join(
                    f'{hash_bytes(data)}  {name}\n' for name, data in centries.items()
                ).encode('utf-8')
                if write:
                    write_deterministic_zip(cpath, centries)
                verify_zip_entries(cpath, centries)
                manifest[f'packages/{zip_name}'] = {
                    'scope': comp_scope,
                    'members': len(centries) - 1,
                    'bytes': cpath.stat().st_size,
                    'sha256': hash_bytes(cpath.read_bytes()),
                }
    m_json = PACKAGES_DIR / 'PACKAGE-MANIFEST.json'
    m_sha = PACKAGES_DIR / 'PACKAGE-MANIFEST-SHA256.txt'
    m_bytes = (json.dumps(manifest, indent=2, sort_keys=True) + '\n').encode('utf-8')
    sha_lines = ''.join(f'{info["sha256"]}  {name}\n' for name, info in sorted(manifest.items())).encode('utf-8')
    if write:
        m_json.write_bytes(m_bytes)
        m_sha.write_bytes(sha_lines)
    require(m_json.is_file() and m_json.read_bytes() == m_bytes, 'PACKAGE-MANIFEST.json drift')
    require(m_sha.is_file() and m_sha.read_bytes() == sha_lines, 'PACKAGE-MANIFEST-SHA256.txt drift')
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write-package', action='store_true')
    parser.add_argument('--assemble-complete', type=Path,
                        help='Build a complete single-file offline ZIP (including consolidated PDFs) at this local path')
    args = parser.parse_args()
    diff = subprocess.check_output(['git', 'diff', '--name-status', BASE, '--'], cwd=ROOT).decode()
    require(all(line.startswith('A\t') for line in diff.splitlines()),
            'Recovery checkpoint contains an edit or deletion')
    verify_generation()
    verify_photos()
    verify_retained_pdfs()
    entries = package_payload(include_consolidated_pdfs=False)
    if args.write_package:
        write_deterministic_zip(BUNDLE, entries)
    verify_zip_entries(BUNDLE, entries, enforce_size_limit=True)
    manifest = write_or_verify_zone_packages(write=args.write_package)
    if args.assemble_complete:
        full_entries = package_payload(include_consolidated_pdfs=True)
        for pdf in sorted((FOUND / 'proofs').glob('Z*-*.pdf')):
            full_entries[f'proofs/{pdf.name}'] = pdf.read_bytes()
        full_entries['PACKAGE-SHA256.txt'] = ''.join(
            f'{hash_bytes(data)}  {name}\n' for name, data in sorted(full_entries.items()) if name != 'PACKAGE-SHA256.txt'
        ).encode('utf-8')
        write_deterministic_zip(args.assemble_complete, full_entries)
        print(f'Assembled complete bundle {args.assemble_complete} ({args.assemble_complete.stat().st_size} bytes, '
              f'SHA-256 {hash_bytes(args.assemble_complete.read_bytes())})')
    print(f'PASS: frozen paths, reproducible reader, photo provenance, valid PDFs, {len(entries)-1} core offline members, '
          f'{sum("zone" in item for item in manifest.values())} zone packages (all <= 45 MB)')
    print(f'{BUNDLE.name} ({BUNDLE.stat().st_size} bytes) SHA-256 {hash_bytes(BUNDLE.read_bytes())}')


if __name__ == '__main__':
    main()
