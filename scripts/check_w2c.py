"""Validate Wave 2C custody, reproducibility, QA receipts and HOLD boundaries.

* the manifest and 375-row production register match the batch ledger;
* computed plates (knots, navigation) equal a fresh topology/geometry-checked build;
* every W2C predecessor equals the active reader figure at the A04 checkpoint, and
  every provisional revision is the active reader figure;
* A04 audit records and all preserved predecessor, pilot, photographic and comparison
  assets are byte-identical to the checkpoint;
* every batch with provisional plates has a visual QA receipt whose outputs exist,
  match their hashes and recorded no accessibility violations;
* publication stays HOLD.
"""
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys

from build_foundations import FOUND, ROOT, require

CHECKPOINT = '500f11ea28acead942fc0d89d9420e135f2d5316'
W2C = FOUND / 'visual/w2c_technical'
LEDGER = FOUND / 'audit/w2c/W2C_BATCHES.json'
FROZEN_TREES = [
    'foundations/audit/a04',
    'foundations/visual/v02_technical',
    'foundations/visual/VISUAL_PILOT_REVIEW_PACKAGE',
    'foundations/visual/v03_authentic_photos',
    'foundations/visual/v03_realistic',
    'foundations/visual/a04_comparison',
    'foundations/visual/v02_atlas_comparison',
]


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def at_checkpoint(rel):
    return subprocess.check_output(['git', 'show', f'{CHECKPOINT}:{rel}'], cwd=ROOT)


def run(script, *args):
    subprocess.run([sys.executable, str(ROOT / 'scripts' / script), *args], check=True, cwd=ROOT / 'scripts',
                   stdout=subprocess.DEVNULL)


def check_frozen_trees():
    listed = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', CHECKPOINT, '--', *FROZEN_TREES],
                                     cwd=ROOT).decode().splitlines()
    for rel in listed:
        require((ROOT / rel).is_file() and (ROOT / rel).read_bytes() == at_checkpoint(rel),
                f'Preserved checkpoint asset changed or removed: {rel}')
    return len(listed)


def check_records():
    specs = json.loads((FOUND / 'evidence/diagram-specs.json').read_text(encoding='utf-8'))
    records = json.loads((W2C / 'MANIFEST.json').read_text(encoding='utf-8'))
    provisional = set()
    for r in records:
        page = r['page_id']
        require(r['publication'] == 'HOLD', f'Publication drift on {page}')
        pred = W2C / r['predecessor']
        require(digest(pred) == r['predecessor_sha256']
                and pred.read_bytes() == at_checkpoint(f'foundations/reader/visuals/{page}.svg'),
                f'W2C predecessor is not the checkpoint figure: {page}')
        if r['disposition'] == 'PROVISIONAL_EDITORIAL_CANDIDATE':
            provisional.add(page)
            active = FOUND / 'reader/visuals' / f'{page}.svg'
            require(specs[page] == {'type': 'w2c_artwork'}
                    and digest(W2C / r['revised']) == r['revised_sha256'] == digest(active) == r['active_reader_sha256'],
                    f'W2C revision is not the active reader figure: {page}')
        else:
            require(specs[page].get('type') != 'w2c_artwork', f'Held or rejected plate is active: {page}')
    active_specs = {cid for cid, spec in specs.items() if spec.get('type') == 'w2c_artwork'}
    require(active_specs == provisional, f'W2C specs and manifest disagree: {sorted(active_specs ^ provisional)}')
    return records, provisional


def check_receipts(provisional):
    data = json.loads(LEDGER.read_text(encoding='utf-8'))
    batches = 0
    for batch in data['batches']:
        pages = [p['page_id'] for p in batch['plates'] if p['disposition'] == 'PROVISIONAL_EDITORIAL_CANDIDATE']
        if not pages:
            continue
        receipt = json.loads((W2C / 'qa' / f"{batch['batch']}-VISUAL-QA.json").read_text(encoding='utf-8'))
        require(receipt['pages'] == pages and not any(receipt['axe_violations'].values())
                and not receipt['network_requests'] and not receipt['javascript_errors'],
                f"Visual QA receipt incomplete for {batch['batch']}")
        for rel, info in receipt['outputs'].items():
            require(digest(FOUND / rel) == info['sha256'], f'QA output changed after inspection: {rel}')
        batches += 1
    return batches


def main():
    run('w2c_register.py', '--check')
    from w2c_register import BUILDERS
    for builder in BUILDERS:
        run(builder, '--check')
    run('w2c_photos.py', '--check')
    frozen = check_frozen_trees()
    records, provisional = check_records()
    batches = check_receipts(provisional)
    print(f'PASS: {len(records)} W2C records ({len(provisional)} provisional candidates), {batches} batch QA receipts, '
          f'{frozen} preserved checkpoint assets byte-identical, computed plates reproducible, publication HOLD')


if __name__ == '__main__':
    main()
