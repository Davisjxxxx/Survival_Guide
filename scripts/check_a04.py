"""Validate A04 review coverage, baseline custody, and HOLD boundaries."""
from collections import Counter
import csv
from hashlib import sha256
from html.parser import HTMLParser
import json
from math import atan2, degrees, isclose
from subprocess import check_output
from xml.etree import ElementTree

from build_foundations import FOUND, ROOT, require
from check_foundations import LocalAssetCheck

BASE = '807ed366018c022cd6387352ad8442a5a32367c7'
AUDIT = FOUND / 'audit/a04'
VISUAL = FOUND / 'visual'
COMPARISON = VISUAL / 'a04_comparison'


def rows(name):
    with (AUDIT / name).open(newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def original(path):
    return check_output(['git', 'show', f'{BASE}:{path.relative_to(ROOT).as_posix()}'], cwd=ROOT)


class CompactRoutes(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = {}

    def handle_starttag(self, tag, attrs):
        props = dict(attrs)
        if tag == 'section':
            self.id = props.get('id')
        if tag == 'a' and props.get('href', '').startswith('sources/'):
            self.links.setdefault(self.id, set()).add(props['href'])


def w2c_records():
    """All W2C records by page, used to recognise A04-era snapshots of later revised figures."""
    path = VISUAL / 'w2c_technical/MANIFEST.json'
    return {r['page_id']: r for r in json.loads(path.read_text(encoding='utf-8'))} if path.is_file() else {}


def w2c_supersessions():
    """W2C records that replace an A04 candidate returned for reconstruction."""
    path = VISUAL / 'w2c_technical/MANIFEST.json'
    if not path.is_file():
        return {}
    return {r['page_id']: r for r in json.loads(path.read_text(encoding='utf-8'))
            if r.get('supersedes_a04_candidate_sha256')}


def check_plates():
    supersessions = w2c_supersessions()
    records = rows('V01_V02_VISUAL_QUALIFICATION.csv')
    require(Counter(r['series'] for r in records) == {'V01': 9, 'V02': 64}, 'Review plate count drift')
    require(len({row['page_id'] for row in records}) == 73, 'Duplicate or missing review plate')
    for r in records:
        name = r['page_id'] + '.svg'
        preserved = FOUND / r['predecessor']
        active = FOUND / 'reader/visuals' / name
        source = preserved.parent.parent / 'revised' / name
        prior = COMPARISON / 'incoming' / name
        require(preserved.read_bytes() == original(preserved) and digest(preserved) == r['predecessor_sha256'],
                f'Predecessor custody failure: {name}')
        superseded = supersessions.get(r['page_id'])
        if superseded:
            # A04 custody still applies: the A04 candidate stays byte-identical in place. Only a plate A04
            # returned for reconstruction may show a different active figure, and only through a W2C record
            # whose hashes chain the A04 candidate to the W2C predecessor, revision and active reader figure.
            w2c = VISUAL / 'w2c_technical'
            require(r['disposition'] == 'RECONSTRUCTION_REQUIRED'
                    and superseded['supersedes_a04_candidate_sha256'] == r['candidate_sha256']
                    and digest(source) == r['candidate_sha256']
                    and digest(w2c / superseded['predecessor']) == superseded['predecessor_sha256'] == r['candidate_sha256']
                    and digest(w2c / superseded['revised']) == superseded['revised_sha256'] == digest(active)
                    and r['publication'] == superseded['publication'] == 'HOLD',
                    f'W2C supersession custody failure: {name}')
        else:
            require(digest(source) == digest(active) == r['candidate_sha256'] and r['publication'] == 'HOLD',
                    f'Edited figure or publication drift: {name}')
        require((prior.read_bytes() if prior.is_file() else source.read_bytes()) == original(source)
                and digest(prior if prior.is_file() else source) == r['incoming'], f'PR #9 figure custody: {name}')
    returned = {r['page_id'] for r in records if r['disposition'] == 'RECONSTRUCTION_REQUIRED'}
    bearing = ElementTree.parse(FOUND / 'reader/visuals/Z11-P30.svg')
    a, b = (bearing.find(f".//{{http://www.w3.org/2000/svg}}circle[@id='azimuth-{end}']")
            for end in ('start', 'end'))
    east = float(b.get('cx')) - float(a.get('cx'))
    north = float(a.get('cy')) - float(b.get('cy'))
    require(isclose(degrees(atan2(east, north)), 60, abs_tol=0.01),
            'Z11-P30 plotted geometry no longer matches the labeled bearing')
    queue = rows('WAVE_2C_TECHNICAL_QUEUE.csv')
    require(sum(r['origin'] == 'UNATTEMPTED_V02' for r in queue) == 372 and
            {r['page_id'] for r in queue if r['origin'] == 'RETURNED_A04'} == returned,
            'Wave 2C queue count or returned assets drift')


def check_evidence_and_media():
    evidence = rows('EVIDENCE_RESOLUTION_VERIFICATION.csv')
    require(len({r['claim_id'] for r in evidence}) == 56 and all(
        r['a04_source'].startswith('https://') and r['a04_locator'] and not r['a04_locator'].startswith('HTTP')
        for r in evidence), 'Evidence verification rows or section locators missing')
    taxa = rows('TAXONOMIC_RECONCILIATION.csv')
    require(len(taxa) == 113 and sum(bool(r['new_gbif_lead']) for r in taxa) == 25
            and sum(bool(r['a04_naming_source']) for r in taxa) == 5
            and all(r['consumption_status'] == 'WITHHELD_HOLD' for r in taxa), 'Taxonomy hold or coverage drift')
    photos = rows('PHOTOGRAPHIC_EVIDENCE_AUDIT.csv')
    require(len(photos) == 40, 'Photo audit count drift')
    for r in photos:
        original_file, delivery = (FOUND / r[key] for key in ('path', 'display'))
        require(original_file.read_bytes() == original(original_file) and digest(original_file) == r['sha256']
                and digest(delivery) == r['display_sha256'] and r['diagnostic_qualification'] == 'WITHHELD',
                f'Photographic custody or approval drift: {r["photo_id"]}')
    briefs = rows('REALISTIC_ILLUSTRATION_QUALIFICATION.csv')
    require(len(briefs) == 82 and sum(r['a04_status'].endswith('_HOLD') for r in briefs) == 12
            and all(r['publication'] == 'HOLD' for r in briefs), 'Realistic brief hold or scope drift')
    pilot = VISUAL / 'v03_realistic/pilot'
    generated = json.loads((pilot / 'MANIFEST.json').read_text())
    require(len(generated) == 2, 'Pilot scope drift')
    for r in generated:
        require(digest(pilot / r['source_file']) == r['sha256']
                and digest(pilot / r['annotation']) == r['annotation_sha256']
                and r['classification'] == 'GENERATED_INSTRUCTIONAL_NON_DIAGNOSTIC',
                'Synthetic image custody or classification drift')


def check_atlas():
    for idx in range(1, 76):
        id = f'Z16-P{idx:02d}'
        for extension, directory in [('html', 'reader'), ('svg', 'reader/visuals')]:
            path = FOUND / directory / f'{id}.{extension}'
            require(path.read_bytes() == original(path), f'Owner-pending atlas was promoted: {id}')
    folder = COMPARISON / 'atlas'
    parser = CompactRoutes()
    parser.feed((folder / 'index.html').read_text())
    routes = json.loads((folder / 'ROUTES.json').read_text())
    records = {r['page_id']: {f'sources/{id}.html' for id in r['upstream'].split()} for r in routes}
    require(len(routes) == 8 and parser.links == records, 'Compact atlas comparison routing mismatch')
    records = w2c_records()
    for image in (folder / 'sources/visuals').glob('*.svg'):
        # The comparison is a frozen A04 snapshot. A bundled figure must match the active reader, or, for a page
        # later revised in W2C, the recorded W2C predecessor (the figure as it stood at the A04 checkpoint).
        record = records.get(image.stem)
        current = image.read_bytes() == (FOUND / 'reader/visuals' / image.name).read_bytes()
        snapshot = bool(record) and digest(image) == record['predecessor_sha256'] == digest(
            VISUAL / 'w2c_technical' / record['predecessor'])
        require(current or snapshot, f'Bundled source figure differs from the active reader: {image.name}')
    entries = {f.relative_to(folder).as_posix() for f in folder.rglob('*') if f.is_file()}
    for key in entries:
        if key.endswith('.html'):
            checker = LocalAssetCheck(key, entries)
            checker.feed((folder / key).read_text(encoding='utf-8'))


def main():
    check_plates()
    check_evidence_and_media()
    check_atlas()
    print(f'PASS: 73 plate comparisons ({len(w2c_supersessions())} returned plates superseded through W2C custody), '
          '40 photographic assets, focused evidence, and unpromoted atlas custody')


if __name__ == '__main__':
    main()
