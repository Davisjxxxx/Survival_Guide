#!/usr/bin/env python3
"""Verify imported source bytes and ZIP structure without extracting or changing them.

This is a storage/format integrity check, not source-rights or field-safety approval.
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path, PurePosixPath
import sys
import zipfile

def verify(repo_root, manifest):
    repo = Path(repo_root).resolve()
    filelist = Path(manifest).resolve()
    if not filelist.is_relative_to(repo):
        raise ValueError('Manifest must be inside this repository')
    rows = list(csv.DictReader(filelist.open(encoding='utf-8'), delimiter='\t'))
    if not rows:
        raise ValueError('No imported files in manifest')
    seen = set()
    findings = []
    for row in rows:
        rel = row.get('repository_path', '')
        path = (repo / rel).resolve()
        if not path.is_relative_to(repo) or rel in seen or not path.is_file():
            raise ValueError('Duplicate, missing or escaping file: '+rel)
        seen.add(rel)
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest != row.get('sha256', '').lower():
            raise ValueError('SHA256 differs from original manifest: '+rel)
        detail = {'path': rel, 'bytes': path.stat().st_size,
                  'sha256_verified': True, 'type': path.suffix.lower()}
        if path.suffix.lower() == '.zip':
            with zipfile.ZipFile(path) as package:
                entries = package.infolist()
                for member in entries:
                    name = PurePosixPath(member.filename)
                    if name.is_absolute() or '..' in name.parts or member.filename.startswith('\\'):
                        raise ValueError('Unsafe ZIP member pathname: '+member.filename)
                broken = package.testzip()
                if broken:
                    raise ValueError('ZIP CRC failed in '+rel+': '+broken)
                detail['zip_entries'] = len(entries)
                detail['zip_crc_verified'] = True
        elif path.suffix.lower() == '.pdf':
            if not path.read_bytes().startswith(b'%PDF-'):
                raise ValueError('Invalid PDF signature: '+rel)
            detail['pdf_signature_verified'] = True
        elif path.suffix.lower() in ('.html', '.htm'):
            if b'<!doctype html>' not in path.read_bytes()[:200].lower():
                raise ValueError('Missing HTML doctype: '+rel)
            detail['html_signature_verified'] = True
        findings.append(detail)
    return {'manifest':str(filelist.relative_to(repo)), 'files':findings,
            'total_files':len(findings), 'verified_bytes':sum(f['bytes'] for f in findings),
            'release_status':'BLOCKED; format/storage verification does not certify field instructions'}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--manifest', type=Path)
    args = parser.parse_args()
    repo = args.repo.resolve()
    manifest = args.manifest or repo / 'imports/local-downloads/20261123T145517Z-405239/IMPORT_MANIFEST.tsv'
    try:
        print(json.dumps(verify(repo, manifest), indent=2))
    except Exception as exc:
        print('FAIL: '+str(exc), file=sys.stderr)
        return 1
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
