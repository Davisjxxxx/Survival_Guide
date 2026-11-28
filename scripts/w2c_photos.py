"""Build the Wave 2C authentic photograph set from retained provider originals.

ACQUISITIONS.json (curated, one record per photograph) names the page(s), the
provider record, the exact original download, licence and rights notes, what is
actually visible, and which diagnostic views are still missing. Provider bytes
in originals/ are never modified. Display derivatives in display/ apply EXIF
orientation and resize to 1600 px on the long side. MANIFEST.json and
RIGHTS_AND_PROVENANCE_REGISTER.csv are generated from the record and the hashes.

--write regenerates derivatives, registers and the offline gallery (index.html);
--check verifies they match.
No photograph here carries diagnostic, identification or consumption approval.
"""
import argparse
import csv
from hashlib import sha256
from html import escape
from io import BytesIO, StringIO
import json
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / 'foundations/visual/w2c_authentic_photos'
FIELDS = ['photo_id', 'page_ids', 'subject_taxon', 'record_type', 'original_file', 'delivery_derivative',
          'original_download_url', 'catalogue_url', 'gbif_occurrence_url', 'institution_and_photographer',
          'license_and_attribution', 'rights_notes', 'specimen_or_accession_id', 'event_date', 'locality_and_precision',
          'acquisition_date', 'original_sha256', 'derivative_sha256', 'original_bytes', 'original_pixels',
          'visible_subject', 'required_diagnostic_features', 'missing_views', 'expert_validation_status',
          'diagnostic_qualification', 'consumption_status', 'classification']


def derivative(data):
    im = ImageOps.exif_transpose(Image.open(BytesIO(data))).convert('RGB')
    im.thumbnail((1600, 1600), Image.LANCZOS)
    out = BytesIO()
    im.save(out, format='JPEG', quality=85)
    return out.getvalue()


GALLERY_HEAD = ('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
                '<title>W2C authentic photographs · Publication HOLD</title><style>body{font:16px/1.45 system-ui,sans-serif;margin:0;'
                'background:#f4f3ec;color:#183a30}main{max-width:72rem;margin:0 auto;padding:1rem}.grid{display:grid;'
                'grid-template-columns:repeat(auto-fill,minmax(18rem,1fr));gap:1rem}.photo{background:#fffdf7;border:1px solid #c4bcab;'
                'padding:.8rem}.photo img{width:100%;height:auto;display:block}.photo p{overflow-wrap:anywhere}h1{font-size:1.6rem}'
                'h2{font-size:1.05rem;margin:.5rem 0}.hold{color:#7a2f15;font-weight:650}a{color:#1e4f5c}</style><main>'
                '<h1>Wave 2C authentic photographs</h1><p>Open-licence provider originals with EXIF-corrected display copies. '
                'Observation photographs are not vouchers, and a voucher image may show only its label. No photograph here supports '
                'identification, diagnosis or consumption. Publication HOLD.</p><div class="grid">')


def gallery(manifest):
    parts = [GALLERY_HEAD]
    for r in manifest:
        e = {k: escape(str(v)) for k, v in r.items() if isinstance(v, str)}
        parts.append(
            f'<article class="photo"><img src="{e["delivery_derivative"]}" alt="{e["subject_taxon"]}: {e["visible_subject"]}">'
            f'<h2>{e["photo_id"]} · <i>{e["subject_taxon"]}</i></h2>'
            f'<p><strong>Pages</strong> {escape(", ".join(r["page_ids"]))} · <strong>Record</strong> {e["record_type"]}</p>'
            f'<p><strong>Visible</strong> {e["visible_subject"]}</p><p><strong>Missing views</strong> {e["missing_views"]}</p>'
            f'<p><strong>Rights</strong> {e["license_and_attribution"]}. {e["rights_notes"]}</p>'
            f'<p><strong>Source</strong> <a href="{e["catalogue_url"]}">provider record</a> · <a href="{e["gbif_occurrence_url"]}">'
            f'GBIF occurrence</a> · original <a href="{e["original_file"]}">{r["original_sha256"][:12]}</a></p>'
            f'<p class="hold">Diagnostic qualification WITHHELD · expert validation PENDING · consumption {e["consumption_status"]}</p></article>')
    parts.append('</div></main></html>')
    return ''.join(parts)


def build():
    records = json.loads((DIR / 'ACQUISITIONS.json').read_text(encoding='utf-8'))
    manifest, files = [], {}
    for r in records:
        original = DIR / r['original_file']
        data = original.read_bytes()
        if data[:2] != b'\xff\xd8':
            raise SystemExit(f"Original is not a JPEG: {r['original_file']}")
        if sha256(data).hexdigest() != r['original_sha256']:
            raise SystemExit(f"Provider bytes changed: {r['original_file']}")
        disp = derivative(data)
        files[r['delivery_derivative']] = disp
        with Image.open(BytesIO(data)) as im:
            pixels = list(im.size)
        manifest.append(dict(r, derivative_sha256=sha256(disp).hexdigest(), original_bytes=len(data),
                             original_pixels=pixels, expert_validation_status='PENDING',
                             diagnostic_qualification='WITHHELD'))
    manifest_text = json.dumps(manifest, indent=2, ensure_ascii=False) + '\n'
    out = StringIO()
    w = csv.DictWriter(out, fieldnames=FIELDS, lineterminator='\n', extrasaction='ignore')
    w.writeheader()
    for m in manifest:
        w.writerow(dict(m, page_ids=' '.join(m['page_ids']), original_pixels='x'.join(map(str, m['original_pixels']))))
    return manifest, files, manifest_text, out.getvalue()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    manifest, files, manifest_text, register_text = build()
    targets = {DIR / 'MANIFEST.json': manifest_text.encode('utf-8'),
               DIR / 'index.html': gallery(manifest).encode('utf-8'),
               DIR / 'RIGHTS_AND_PROVENANCE_REGISTER.csv': register_text.encode('utf-8'),
               **{DIR / k: v for k, v in files.items()}}
    if args.write:
        for path, data in targets.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
    if args.check:
        for path, data in targets.items():
            if not path.is_file() or path.read_bytes() != data:
                raise SystemExit(f'{path.relative_to(ROOT)} differs from a fresh build')
    print(f'{len(manifest)} W2C photographs; diagnostic qualification WITHHELD for all')


if __name__ == '__main__':
    main()
