#!/usr/bin/env python3
"""Verify the recovery archive, scope allocation, and unchanged owner-review files."""
import csv
from collections import defaultdict
import hashlib
from pathlib import Path
import re
import subprocess
import xml.etree.ElementTree as ET
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parents[1]
RECOVERY = ROOT / 'project/recovery'
PLANNING = ROOT / 'project/planning'
FROZEN = '6adbb05848bbadebe5a6df82689d99c20de7855d'
SCRIPT = 'scripts/verify_s02_s03_recovery.py'


def git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT), *args])


def check(condition, message):
    if not condition:
        raise SystemExit(f'FAIL: {message}')


def digest(data):
    return hashlib.sha256(data).hexdigest()


def csv_rows(path):
    with path.open(newline='', encoding='utf-8') as file:
        return list(csv.DictReader(file))


def verify_frozen():
    tree = git('ls-tree', '-r', '-z', FROZEN).split(b'\0')
    count = 0
    for row in filter(None, tree):
        entry, relative = row.split(b'\t', 1)
        mode, kind, oid = entry.split()
        path = ROOT / relative.decode()
        check(kind == b'blob' and path.is_file(), f'Frozen path missing: {path}')
        data = path.read_bytes()
        object_data = f'blob {len(data)}\0'.encode() + data
        check(hashlib.sha1(object_data).hexdigest().encode() == oid, f'Changed frozen file: {path}')
        executable = bool(path.stat().st_mode & 0o111)
        check(executable == (mode == b'100755'), f'Changed frozen mode: {path}')
        count += 1
    return count


def verify_checksum_register():
    allowed = [*RECOVERY.rglob('*'), *PLANNING.rglob('*'), ROOT/SCRIPT]
    expected = {p.relative_to(ROOT).as_posix() for p in allowed
                if p.is_file() and p.name != 'SHA256SUMS.txt'}
    found = set()
    for line in (RECOVERY/'SHA256SUMS.txt').read_text().splitlines():
        claimed, relative = line.split('  ', 1)
        check(relative in expected and relative not in found, f'Invalid checksum path: {relative}')
        check(digest((ROOT/relative).read_bytes()) == claimed, f'Digest mismatch: {relative}')
        found.add(relative)
    check(found == expected, 'Recovery/planning checksum inventory is incomplete')
    return len(found)


def verify_evidence():
    groups = defaultdict(list)
    members = {}
    for row in csv_rows(RECOVERY/'evidence/BASELINE_ARCHIVE_MEMBERS.csv'):
        groups[row['archive']].append(row)
    for archive, rows in groups.items():
        with ZipFile(ROOT/archive) as actual:
            check(actual.testzip() is None, f'Corrupt ZIP: {archive}')
            check([i.filename for i in actual.infolist() if not i.is_dir()] ==
                  [row['member'] for row in rows], f'Member list changed: {archive}')
            for row, info in zip(rows, (i for i in actual.infolist() if not i.is_dir())):
                data = actual.read(info)
                check(len(data) == int(row['bytes']) and digest(data) == row['sha256'],
                      f'Member hash mismatch: {archive}!{info.filename}')
                key = archive + '!' + info.filename
                check(key not in members, f'Duplicate member name: {key}')
                members[key] = (len(data), row['sha256'])
    originals = set()
    for row in csv_rows(RECOVERY/'RECOVERED_ARTIFACT_MANIFEST.csv'):
        name = row['retained_path_or_archive_member']
        if not name:
            check(row['classification'] == 'UNVERIFIED_CANDIDATE', f'Missing retained destination: {row["source"]}')
            continue
        if name in members:
            result = members[name]
        else:
            data = (ROOT/name).read_bytes()
            result = (len(data), digest(data))
        check(result == (int(row['bytes']), row['sha256']), f'Artifact mismatch: {name}')
        if row['classification'] != 'EXACT_DUPLICATE':
            originals.add(name)
    actual = {p.relative_to(ROOT).as_posix() for p in (RECOVERY/'originals').rglob('*') if p.is_file()}
    check(originals == actual, 'Original inventory differs from retained file set')
    for row in csv_rows(ROOT/'imports/gate-a-history/fable-review-inventory.csv'):
        path = RECOVERY/'originals/20261124/gate-a-fable'/row['local review artifact']
        if path.is_file():
            check(digest(path.read_bytes()) == row['sha256'], f'Fable custody mismatch: {path}')
    bundle = str(RECOVERY/'evidence/gate-a-local-history.bundle')
    git('bundle', 'verify', bundle)
    check(len(git('bundle', 'list-heads', bundle).splitlines()) == 7, 'Gate A ref count changed')
    return len(originals), len(members)


def verify_scope():
    historical = ROOT/'project/historical-scope'
    plan = (historical/'Survival_Field_Encyclopedia_Master_Sprint_Plan_v1.md').read_text()
    historical_pages = dict(re.findall(r'^\| (Z\d{2}) \| [^|]+\| (\d+) \|', plan, re.M))
    zones = csv_rows(PLANNING/'ZONE_COMPLETION_MATRIX.csv')
    observed = {z['zone']:z['draft_pages'] for z in zones}
    check(len(zones) == 16 and observed == historical_pages, 'Zone plan allocations changed')
    check(sum(map(int,observed.values())) == 1016, 'Incorrect page allocation total')
    tracker = historical/'Survival_Field_Encyclopedia_Sprint_Tracker_v1.xlsx'
    namespace = {'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
    with ZipFile(tracker) as book:
        check(book.testzip() is None, 'Corrupt original tracker')
        workbook = ET.fromstring(book.read('xl/workbook.xml'))
        check([sheet.attrib['name'] for sheet in workbook.findall('s:sheets/s:sheet', namespace)] ==
              ['Sprints','Zones','Review Gates','Risks','Evidence','Dashboard'], 'Historical tracker sheet mismatch')
    trace = csv_rows(PLANNING/'MASTER_SCOPE_RECONCILIATION.csv')
    ids = {row['id'] for row in trace}
    check(len(ids) == len(trace) and set(observed) <= ids, 'Invalid scope trace coverage')
    check(all(z['release'] == 'HOLD' and z['specialist_approval'] == '0 accepted' for z in zones),
          'Zone status exceeds review authority')
    return len(trace)


if __name__ == '__main__':
    frozen = verify_frozen()
    checksums = verify_checksum_register()
    originals, members = verify_evidence()
    scope = verify_scope()
    print(f'PASS: {frozen} frozen paths, {checksums} sealed files, {originals} recovered files, '
          f'{members} archive members, seven Gate A refs, and {scope} traced requirements.')
