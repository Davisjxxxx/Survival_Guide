#!/usr/bin/env python3
"""Rate-limit-respecting Commons photo downloader and manual research importer.

This works alongside the existing Track B 011 files. It never asserts botanical
identity, does not automatically authorize copyright use, and never bypasses a
429 response. Only research-graded derivatives are created.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import os
import re
import shutil
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
API = 'https://commons.wikimedia.org/w/api.php'
MAX_BYTES = 20 * 1024 * 1024
CACHE = ROOT / 'commons_metadata_cache.json'
RECEIPTS = ROOT / 'recovery_receipts.csv'


def rows():
    return list(csv.DictReader((ROOT / 'PHOTO_MANIFEST.csv').open(encoding='utf-8', newline='')))


def status():
    manifest = rows()
    originals, photos = ROOT / 'originals', ROOT / 'photos'
    items = []
    for r in manifest:
        asset = r['asset_id']
        original = originals / (asset + '.jpg')
        derivative = photos / (asset + '.jpg')
        items.append((asset, original.exists(), derivative.exists()))
    for asset, o, d in items:
        print(f'{asset:<12} original={"YES" if o else "NO ":<3} display={"YES" if d else "NO"}')
    print(f'Present display images: {sum(d for _, _, d in items)}/{len(items)}')
    print('Photo identity and publication rights still require human verification.')


def sha1(b: bytes) -> str:
    return hashlib.sha1(b).hexdigest()


def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def norm(t: str) -> str:
    return re.sub(r'[^a-z0-9]', '', t.lower().replace('unported', '').replace('international', ''))


def license_matches(expected: str, actual: str, url: str) -> bool:
    """Conservative licence match; provenance still needs human review."""
    e, a, u = norm(expected), norm(actual), norm(url)
    if e == 'publicdomain':
        return 'publicdomain' in a or 'publicdomain' in u or a in ('cc0', 'cczero')
    if e in ('cc01', 'cc010', 'cczero10'):
        return 'cc0' in a or 'cc0' in u
    if not e.startswith('ccby'):
        return False
    if any(bad in a + u for bad in ('noncommercial', 'nonderivative', 'bync', 'bynd')):
        return False
    # Require the same specific family/version, not merely any BY-SA licence.
    # Prefer explicit Commons LicenseShortName; reject contradictions with URL.
    if a.startswith('ccby'):
        return a == e and (not u or e[2:] in u)
    if 'bysa' in e:
        return e[2:] in u and 'bysa' not in a
    return e[2:] in u and 'bysa' not in a


def user_agent(contact: str) -> str:
    c = contact.strip()
    if not c or (('@' not in c or ' ' in c) and not c.startswith('https://')):
        raise ValueError('Supply a real public contact email or HTTPS contact URL via --contact.')
    return f'SurvivalFieldEncyclopediaResearch/0.2 ({c}) Python-urllib/3'


class Throttled(Exception):
    pass


def throttled_error(ex: urllib.error.HTTPError) -> Throttled:
    hint = ex.headers.get('Retry-After') if ex.headers else None
    return Throttled(f'HTTP {ex.code}; Retry-After: {hint or "not specified"}. '
                     'Stop this run and resume after the server permits it.')


def request(url: str, agent: str, json_type=False) -> bytes:
    uri = urllib.parse.urlsplit(url)
    if uri.scheme != 'https' or uri.hostname not in ('commons.wikimedia.org', 'upload.wikimedia.org'):
        raise ValueError(f'Unexpected host: {uri.hostname}')
    hdr = {'User-Agent': agent, 'Accept': 'application/json' if json_type else 'image/jpeg,image/png,image/webp'}
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=hdr), timeout=45) as response:
            ct = response.headers.get('Content-Type', '').lower()
            if json_type and 'json' not in ct:
                raise ValueError('Unexpected API response content type: ' + ct)
            if not json_type and not ct.startswith(('image/jpeg', 'image/png', 'image/webp')):
                raise ValueError('Unexpected image response content type: ' + ct)
            data = response.read((5 if json_type else MAX_BYTES) * 1024 * 1024 + 1 if json_type else MAX_BYTES + 1)
            if len(data) > (5 * 1024 * 1024 if json_type else MAX_BYTES):
                raise ValueError('Response too large')
            return data
    except urllib.error.HTTPError as exc:
        if exc.code in (429, 503):
            raise throttled_error(exc) from exc
        raise


def key(name: str) -> str:
    return name.replace('_', ' ').removeprefix('File:').strip().casefold()


def metadata_batch(request_rows, agent: str):
    from urllib.parse import urlencode
    params = {
        'action': 'query', 'format': 'json', 'formatversion': '2', 'maxlag': '5',
        'prop': 'imageinfo', 'iiprop': 'url|sha1|size|extmetadata',
        'titles': '|'.join('File:' + r['commons_filename'] for r in request_rows)
    }
    response = json.loads(request(API + '?' + urlencode(params), agent, json_type=True))
    if response.get('error'):
        raise ValueError('Commons API error: ' + str(response['error'].get('code', 'unknown')))
    pgs = response.get('query', {}).get('pages', [])
    result = {}
    for p in pgs:
        if p.get('imageinfo'):
            result[key(p.get('title', ''))] = p['imageinfo'][0]
    return result


def metadata_license(info):
    m = info.get('extmetadata') or {}
    def get(field):
        return re.sub(r'<[^>]+>', '', str(m.get(field, {}).get('value', '')))
    return get('LicenseShortName'), get('LicenseUrl'), get('Artist')


def make_derivative(data, dst):
    from PIL import Image, ImageOps
    with Image.open(io.BytesIO(data)) as im:
        im.verify()
    with Image.open(io.BytesIO(data)) as im:
        image = ImageOps.exif_transpose(im).convert('RGB')
        image.thumbnail((1350, 1350), Image.Resampling.LANCZOS)
        dst.parent.mkdir(exist_ok=True)
        fd, tempname = tempfile.mkstemp(prefix='.display-', suffix='.jpg', dir=str(dst.parent))
        os.close(fd)
        try:
            image.save(tempname, 'JPEG', quality=83, optimize=True, exif=b'')
            os.replace(tempname, dst)
        finally:
            if os.path.exists(tempname):
                os.unlink(tempname)
        return image.size


def save_bytes(data, dst):
    dst.parent.mkdir(exist_ok=True)
    fd, name = tempfile.mkstemp(prefix='.original-', dir=str(dst.parent))
    try:
        with os.fdopen(fd, 'wb') as f:
            f.write(data)
        os.replace(name, dst)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def save_receipts(result):
    columns = ['asset_id', 'state', 'original_sha1', 'original_sha256',
               'derivative_sha256', 'rights_checked_at_download', 'source_page',
               'reviewer', 'species_identity_review', 'pixel_dimensions', 'error']
    # Merge by asset ID so a partial manual import or resumable run never drops
    # receipt history for the other assets. Last status replaces previous status.
    existing = {}
    if RECEIPTS.exists():
        with RECEIPTS.open(encoding='utf-8', newline='') as f:
            existing = {r['asset_id']: r for r in csv.DictReader(f)}
    existing.update({r['asset_id']: r for r in result})
    ordered = [existing[r['asset_id']] for r in rows() if r['asset_id'] in existing]
    with RECEIPTS.open('w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=columns, extrasaction='ignore')
        w.writeheader(); w.writerows(ordered)


def receipt(asset, state, b=None, derivative=None, license_name='', source_page='', error=''):
    result = dict(asset_id=asset, state=state, original_sha1=sha1(b) if b else '',
                  original_sha256=sha256(b) if b else '',
                  derivative_sha256=sha256(derivative.read_bytes()) if derivative and derivative.exists() else '',
                  rights_checked_at_download=license_name, source_page=source_page,
                  reviewer='', species_identity_review='PENDING', pixel_dimensions='', error=error)
    return result


def import_manual(directory: Path):
    """Offline candidates; neither species ID nor current Commons rights are certified."""
    allowed = {r['asset_id']: r for r in rows()}
    imports = []
    directory = directory.expanduser().resolve()
    if not directory.is_dir():
        raise ValueError('Manual import folder not found: ' + str(directory))
    for p in sorted(directory.iterdir()):
        if not p.is_file() or p.suffix.lower() not in ('.jpg', '.jpeg', '.png', '.webp'):
            continue
        asset = p.stem
        if asset not in allowed:
            print('SKIP unknown photo ID:', p.name)
            continue
        data = p.read_bytes()
        if len(data) > MAX_BYTES:
            print('SKIP oversized photo:', p.name)
            continue
        original = ROOT / 'originals' / (asset + '.jpg')
        derived = ROOT / 'photos' / (asset + '.jpg')
        if original.exists() and original.read_bytes() != data:
            print('SKIP existing original differs, refusing overwrite:', asset)
            continue
        try:
            from PIL import Image
            with Image.open(io.BytesIO(data)) as im:
                im.verify()
            if not original.exists():
                save_bytes(data, original)
            size = make_derivative(data, derived)
            rec = receipt(asset, 'MANUAL_CANDIDATE_RIGHTS_HASH_PENDING', data, derived,
                          source_page=allowed[asset]['source_page'],
                          error='API verification unavailable: visual ID and file-specific reuse rights pending')
            rec['pixel_dimensions'] = str(size)
            imports.append(rec)
            print('IMPORTED AS UNVERIFIED CANDIDATE:', asset, size)
        except Exception as exc:
            print('INVALID IMAGE:', asset, exc, file=sys.stderr)
    save_receipts(imports)
    print('Manual research candidates:', len(imports), '(not publication approved)')
    return 0 if imports else 2


def fetch(contact: str, limit=0, gap=1.5):
    agent = user_agent(contact)
    manifest = rows()
    if limit: manifest = manifest[:limit]
    original_dir = ROOT / 'originals'; photo_dir = ROOT / 'photos'
    previous = {}
    if RECEIPTS.exists():
        with RECEIPTS.open(encoding='utf-8', newline='') as f:
            previous = {r['asset_id']: r for r in csv.DictReader(f)}
    manifest = [r for r in manifest
                if not (original_dir / (r['asset_id'] + '.jpg')).exists()
                or not (photo_dir / (r['asset_id'] + '.jpg')).exists()
                or previous.get(r['asset_id'], {}).get('state') != 'DOWNLOADED_NOT_TAXON_VERIFIED']
    # Manual files therefore remain candidates until the live Commons SHA-1 and
    # licence are checked, even when originals and display files exist.
    if not manifest:
        print('No missing files in requested range. Run --status and inspect receipts.')
        return 0
    print(f'Querying Commons metadata once for {len(manifest)} assets (no concurrent requests).')
    try:
        infos = metadata_batch(manifest, agent)
    except Throttled as exc:
        print('COMMONS RATE LIMIT:', exc, file=sys.stderr)
        print('No image requests attempted. Do NOT repeat immediately; use --manual-dir for independently obtained candidates.', file=sys.stderr)
        return 3
    result=[]
    for i,r in enumerate(manifest):
        asset = r['asset_id']; info=infos.get(key(r['commons_filename']))
        if info is None:
            print('NOT FOUND:', asset, r['commons_filename'])
            result.append(receipt(asset,'FAILED',source_page=r['source_page'],error='File missing from Commons API batch'))
            continue
        lic,licurl,artist=metadata_license(info)
        if not license_matches(r['declared_license'], lic, licurl):
            print('LICENSE MISMATCH:', asset, lic, licurl)
            result.append(receipt(asset, 'QUARANTINED_LICENSE',
                                  source_page=r['source_page'], error=f'expected {r["declared_license"]}, current {lic} {licurl}'))
            continue
        try:
            if i: time.sleep(gap)
            original=original_dir / (asset + '.jpg')
            derived=photo_dir / (asset + '.jpg')
            if original.exists():
                b=original.read_bytes()
            else:
                url=info['url']; b=request(url,agent)
            if sha1(b) != info['sha1'].lower():
                raise ValueError('Existing/downloaded original differs from Commons SHA-1; preserving it for review')
            if not original.exists():
                save_bytes(b, original)
            dims=make_derivative(b, derived)
            rec=receipt(asset,'DOWNLOADED_NOT_TAXON_VERIFIED',b,derived,lic,r['source_page'])
            rec['pixel_dimensions']=str(dims)
            result.append(rec)
            print('OK:', asset, dims)
        except Throttled as exc:
            print('COMMONS RATE LIMIT:', exc, file=sys.stderr)
            result.append(receipt(asset,'DEFERRED_429',source_page=r['source_page'],error=str(exc)))
            for rr in manifest[i+1:]:
                result.append(receipt(rr['asset_id'], 'DEFERRED_429',
                                      source_page=rr['source_page'], error='Not requested after 429'))
            save_receipts(result)
            print('Stopped immediately on rate limit; existing photos preserved.', file=sys.stderr)
            return 3
        except Exception as exc:
            print('FAILED:', asset, exc, file=sys.stderr)
            result.append(receipt(asset,'FAILED',source_page=r['source_page'],error=str(exc)))
    save_receipts(result)
    print('Completed:',sum(r['state']=='DOWNLOADED_NOT_TAXON_VERIFIED' for r in result), '/',len(result))
    return 0 if all(r['state']=='DOWNLOADED_NOT_TAXON_VERIFIED' for r in result) else 1


def self_test():
    from PIL import Image
    assert license_matches('CC BY-SA 4.0','CC BY-SA 4.0','https://creativecommons.org/licenses/by-sa/4.0/')
    assert license_matches('CC BY 3.0 US','CC BY 3.0 US','https://creativecommons.org/licenses/by/3.0/us/')
    assert not license_matches('CC BY 4.0','CC BY-SA 4.0','')
    assert not license_matches('CC BY-SA 4.0','CC BY-NC-SA 4.0','')
    assert not license_matches('CC BY-SA 4.0','CC BY-SA 3.0','https://creativecommons.org/licenses/by-sa/3.0/')
    assert license_matches('Public domain','Public domain','')
    assert key('File:Leaf_Tilia_americana_01.jpg')==key('Leaf Tilia americana 01.jpg')
    im=Image.new('RGB',(31,38),'navy'); buf=io.BytesIO();im.save(buf,'JPEG',exif=b'Exif\x00\x00GPS fake')
    with tempfile.TemporaryDirectory() as t:
        o=Path(t)/'display.jpg';make_derivative(buf.getvalue(),o)
        assert b'Exif' not in o.read_bytes()
    class Fake429(urllib.error.HTTPError):pass
    fake=urllib.error.HTTPError('https://commons.wikimedia.org/w/api.php',429,'Too Many Requests',{'Retry-After':'45'},None)
    assert '45' in str(throttled_error(fake))
    print('SELF-TEST PASS: license checks, title mapping, EXIF removal, 429 stop signal')


def main():
    p=argparse.ArgumentParser(description=__doc__)
    group=p.add_mutually_exclusive_group()
    group.add_argument('--status',action='store_true',help='Show local candidates without network calls')
    group.add_argument('--self-test',action='store_true',help='Run offline tests')
    group.add_argument('--manual-dir',type=Path,help='Import images named ASSET-ID.jpg/png as unverified candidates')
    p.add_argument('--contact',default=os.getenv('SFE_WIKIMEDIA_CONTACT',''),
                   help='Real public email or HTTPS contact URL for required compliant User-Agent')
    p.add_argument('--limit',type=int,default=0,help='Only first N manifest items (for a small trial)')
    p.add_argument('--gap',type=float,default=1.5,help='Delay between image requests, minimum 1.0 seconds')
    opts=p.parse_args()
    if opts.self_test:
        self_test();return 0
    if opts.status:
        status();return 0
    if opts.manual_dir is not None:
        return import_manual(opts.manual_dir)
    if opts.limit<0 or opts.gap<1.0:
        p.error('limit must be >=0 and gap must be >=1 second')
    try:
        return fetch(opts.contact,opts.limit,opts.gap)
    except (ValueError, OSError) as exc:
        print('STOP:',exc,file=sys.stderr)
        return 2

if __name__=='__main__':sys.exit(main())
