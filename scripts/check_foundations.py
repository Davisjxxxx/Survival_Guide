"""Check frozen-path custody, review assets and the offline package without network or browser."""
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


def package_members():
    files = [p for path in ('reader', 'manuscripts', 'evidence') for p in (FOUND / path).rglob('*') if p.is_file()]
    files.extend([FOUND / 'README.md', FOUND / 'SPRINT_RESULT.md'])
    matrix = FOUND / 'ZONE_COMPLETION_MATRIX.csv'
    if matrix.exists():
        files.append(matrix)
    # Include consolidated proofs and zone proofs (exclude superseded pilot/core PDFs if redundant or include primary PDFs).
    for pdf in sorted((FOUND / 'proofs').glob('*.pdf')):
        if pdf.name in {'foundations.pdf', 'foundations-a4.pdf', 'reconstructions.pdf',
                        'Z01-letter.pdf', 'Z01-a4.pdf', 'Z02-letter.pdf', 'Z02-a4.pdf',
                        'Z03-letter.pdf', 'Z03-a4.pdf', 'Z04-letter.pdf', 'Z04-a4.pdf'}:
            files.append(pdf)
    return {path.relative_to(FOUND).as_posix(): path.read_bytes() for path in sorted(set(files))}


def package_payload():
    entries = package_members()
    entries['PACKAGE-SHA256.txt'] = ''.join(
        f'{hash_bytes(data)}  {name}\n' for name, data in entries.items()
    ).encode('utf-8')
    return entries


def package_write(entries):
    with tempfile.TemporaryDirectory(dir=BUNDLE.parent) as temp:
        path = Path(temp) / BUNDLE.name
        with ZipFile(path, 'w') as zip_file:
            for name, data in entries.items():
                member = ZipInfo(name, (2026, 11, 24, 0, 0, 0))
                member.compress_type = ZIP_DEFLATED
                member.external_attr = 0o100644 << 16
                zip_file.writestr(member, data)
        path.replace(BUNDLE)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write-package', action='store_true')
    args = parser.parse_args()
    diff = subprocess.check_output(['git', 'diff', '--name-status', BASE, '--'], cwd=ROOT).decode()
    require(all(line.startswith('A\t') for line in diff.splitlines()),
            'Recovery checkpoint contains an edit or deletion')
    verify_generation()
    verify_photos()
    entries = package_payload()
    if args.write_package:
        package_write(entries)
    with ZipFile(BUNDLE) as zipped:
        require(
            zipped.testzip() is None
            and sorted(zipped.namelist()) == sorted(entries)
            and all(hash_bytes(zipped.read(name)) == hash_bytes(data) for name, data in entries.items()),
            'Offline package does not match checked-in bytes',
        )
    print(f'PASS: frozen paths, reproducible reader, photo provenance, {len(entries)-1} offline members')
    print(f'{BUNDLE.name} SHA-256 {hash_bytes(BUNDLE.read_bytes())}')


if __name__ == '__main__':
    main()
