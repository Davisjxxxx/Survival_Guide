"""Check frozen-path custody, review assets, zone PDFs, and the offline package without network or browser."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

from build_foundations import FOUND, ROOT, require

BASE = '890c66ac1d51465d3a4315e50fb2dbe1e0f78f6f'
BUNDLE = FOUND / 'proofs/foundations-offline.zip'
PACKAGES_DIR = FOUND / 'proofs/packages'
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


def package_members(include_consolidated_pdfs=False):
    files = [p for path in ('reader', 'manuscripts', 'evidence', 'audit') for p in (FOUND / path).rglob('*') if p.is_file()]
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
    return {path.relative_to(FOUND).as_posix(): path.read_bytes() for path in sorted(set(files))}


def package_payload(include_consolidated_pdfs=False):
    entries = package_members(include_consolidated_pdfs=include_consolidated_pdfs)
    entries['PACKAGE-SHA256.txt'] = ''.join(
        f'{hash_bytes(data)}  {name}\n' for name, data in entries.items()
    ).encode('utf-8')
    return entries


def zone_package_payload(zone, cards_manifest):
    zone_ids = {c['id'] for c in cards_manifest if c['zone'] == zone}
    files = []
    reader = FOUND / 'reader'
    for base_asset in ('library.css', 'edition.css', 'search.js', 'index.html', 'directory.html',
                       'page-manifest.json', 'asset-manifest.json'):
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
    for doc in ('ZONE_COMPLETION_MATRIX.csv', 'SPRINT_RESULT.md'):
        p = FOUND / doc
        if p.is_file():
            files.append(p)
    entries = {path.relative_to(FOUND).as_posix(): path.read_bytes() for path in sorted(set(files))}
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
          f'{len(manifest)-1} zone packages (all <= 45 MB)')
    print(f'{BUNDLE.name} ({BUNDLE.stat().st_size} bytes) SHA-256 {hash_bytes(BUNDLE.read_bytes())}')


if __name__ == '__main__':
    main()
