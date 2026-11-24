#!/usr/bin/env python3
"""Read-only B012 offline-reader structural audit and opt-in review-copy builder.

No external Python packages. Does not certify field safety or image authenticity.
The imported source is never edited or overwritten.
"""
import argparse
import base64
import csv
import hashlib
from html import escape
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys

DATA = re.compile(r'(<script\b[^>]*\bid=["\']b012_data["\'][^>]*>)(.*?)(</script>)', re.I | re.S)
MISSING = re.compile(r'\{html\.escape\((bad|fix|limit)\)\}')
SOURCE_SHA = '1596b10534fa6d3faac685a050311805e7ac386cf77fd93d29ac93db61638278'

class Tags(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.images = []
        self.svgs = 0
        self.external = []
    def handle_starttag(self, tag, attrs):
        fields = dict(attrs)
        if tag == 'img':
            src = fields.get('src', '')
            self.images.append(src)
            if not src.startswith('data:'):
                self.external.append(src)
        if tag == 'svg':
            self.svgs += 1
        if tag in ('script', 'link'):
            asset = fields.get('src') or fields.get('href')
            if asset:
                self.external.append(asset)

def audit(source, overlay=None, output=None):
    source = Path(source).resolve()
    raw = source.read_bytes()
    raw_hash = hashlib.sha256(raw).hexdigest()
    doc = raw.decode('utf-8')
    match = DATA.search(doc)
    if not match:
        raise ValueError('Missing embedded B012 JSON; no file changed')
    pages = json.loads(match.group(2))
    ids = [p.get('id') for p in pages]
    numbers = [p.get('number') for p in pages]
    ordered = ids == [f'P{i:02d}' for i in range(1, 29)] and numbers == list(range(1, 29))
    rows = []
    for page in pages:
        parser = Tags()
        parser.feed(page['html'])
        invalid = 0
        for src in parser.images:
            if src.startswith('data:image/'):
                try:
                    base64.b64decode(src.partition(',')[2], validate=True)
                except (ValueError, base64.binascii.Error):
                    invalid += 1
        gaps = MISSING.findall(page['html'])
        rows.append({
            'id': page['id'], 'source_group': page.get('source'),
            'title': page.get('title'), 'image_count': len(parser.images),
            'svg_count': parser.svgs, 'external_assets': len(parser.external),
            'invalid_embedded_images': invalid,
            'unresolved_placeholders': len(gaps),
            'placeholder_fields': ';'.join(sorted(set(gaps))),
            'has_original_text_digest': bool(page.get('text_digest'))
        })
    result = {
        'source_sha256': raw_hash,
        'matches_imported_source': raw_hash == SOURCE_SHA,
        'page_count': len(pages), 'ordered_unique_pages': ordered,
        'image_count': sum(r['image_count'] for r in rows),
        'svg_count': sum(r['svg_count'] for r in rows),
        'invalid_embedded_images': sum(r['invalid_embedded_images'] for r in rows),
        'external_asset_references': sum(r['external_assets'] for r in rows),
        'unresolved_placeholders': sum(r['unresolved_placeholders'] for r in rows),
        'source_group_counts': {
            name: sum(p.get('source') == name for p in pages) for name in 'ABCDE'
        },
        'release_status': 'BLOCKED: editorial and external safety review required',
        'pages': rows
    }
    if overlay:
        if not output:
            raise ValueError('The overlay requires --review-output')
        repairs = json.loads(Path(overlay).read_text(encoding='utf-8'))
        if sorted(repairs) != [f'P{i:02d}' for i in range(13, 19)]:
            raise ValueError('Overlay must contain exactly P13-P18')
        for page in pages:
            if page['id'] not in repairs:
                continue
            if sorted(MISSING.findall(page['html'])) != ['bad', 'fix', 'limit']:
                raise ValueError('Unexpected placeholder set in '+page['id'])
            for field in ('bad', 'fix', 'limit'):
                phrase = repairs[page['id']].get(field)
                if not isinstance(phrase, str) or not phrase.strip():
                    raise ValueError('Missing overlay text '+page['id']+'.'+field)
                page['html'] = page['html'].replace(
                    '{html.escape('+field+')}', escape(phrase, quote=True)
                )
            page['editorial_overlay_status'] = 'UNAPPROVED; source unchanged'
        target = Path(output).resolve()
        if target == source:
            raise ValueError('Never overwrite original B012 reader')
        if target.exists():
            raise FileExistsError('Review output already exists: '+str(target))
        target.parent.mkdir(parents=True, exist_ok=True)
        payload = json.dumps(pages, ensure_ascii=False, separators=(',', ':')).replace('</', '<\/')
        derived = doc[:match.start(2)] + payload + doc[match.end(2):]
        notice = ('<div role="note" style="padding:12px;background:#fff1bd;color:#4a3500;'
                  'font-weight:bold">EDITORIAL REVIEW COPY ONLY: source retained; '
                  'P13-P18 correction draft is not approved for field use.</div>')
        derived = derived.replace(
            '<script type="application/json" id="b012_data">',
            notice + '\n<script type="application/json" id="b012_data">', 1
        )
        target.write_text(derived, encoding='utf-8')
        followup = DATA.search(target.read_text(encoding='utf-8'))
        if not followup or any(MISSING.search(p['html']) for p in json.loads(followup.group(2))):
            raise ValueError('Derived reader validation failed')
        result['review_output'] = str(target)
    return result

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('source', type=Path)
    parser.add_argument('--overlay', type=Path)
    parser.add_argument('--review-output', type=Path)
    parser.add_argument('--json-output', type=Path)
    parser.add_argument('--csv-output', type=Path)
    a = parser.parse_args()
    report = audit(a.source, a.overlay, a.review_output)
    if a.json_output:
        a.json_output.parent.mkdir(parents=True, exist_ok=True)
        a.json_output.write_text(json.dumps(report, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
    if a.csv_output:
        a.csv_output.parent.mkdir(parents=True, exist_ok=True)
        with a.csv_output.open('w', newline='', encoding='utf-8') as f:
            names = ['id', 'source_group', 'title', 'image_count', 'svg_count',
                     'external_assets', 'invalid_embedded_images', 'unresolved_placeholders',
                     'placeholder_fields', 'has_original_text_digest']
            writer = csv.DictWriter(f, fieldnames=names)
            writer.writeheader()
            writer.writerows(report['pages'])
    summary = {k:v for k,v in report.items() if k != 'pages'}
    print(json.dumps(summary, indent=2))
    if not report['matches_imported_source'] or not report['ordered_unique_pages'] or report['invalid_embedded_images']:
        print('Structural verification failed.', file=sys.stderr)
        return 2
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
