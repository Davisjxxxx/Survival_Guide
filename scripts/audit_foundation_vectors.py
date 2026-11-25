"""Measure the actual SVG text bounds in Chromium and sample each figure family."""
import argparse
import csv
import hashlib
from io import BytesIO
import json
from pathlib import Path
import re
import shutil
import tempfile
from xml.etree import ElementTree

from PIL import Image, ImageDraw, ImageOps
from playwright.sync_api import sync_playwright


def svg_samples(rows):
    preferred = ['Z01-P01','Z02-P42','Z02-P35','Z03-P06','Z04-P39','Z04-P45','Z09-P44',
                 'Z11-R04','Z11-P65','Z12-P20','Z12-P58','Z12-P65','Z12-P42','Z12-P47','Z12-P48']
    selected = [row for row in rows if row['page'] in preferred]
    types = {row['category'] for row in selected}
    for row in rows:
        if row['category'] not in types:
            selected.append(row)
            types.add(row['category'])
    return selected


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('edition',type=Path)
    ap.add_argument('audit',type=Path)
    ap.add_argument('--fail-layout', action='store_true', help='Fail when any label clips or overlaps')
    ap.add_argument('--zones', help='Optional comma-separated zone filter (e.g. Z10,Z13,Z14,Z15)')
    args = ap.parse_args()
    zone_filter = {z.strip() for z in args.zones.split(',')} if args.zones else None
    reader = args.edition/'reader'
    cards = json.loads((reader/'asset-manifest.json').read_text())
    if zone_filter:
        cards = [c for c in cards if c['page'][:3] in zone_filter]
    specs = json.loads((args.edition/'evidence/diagram-specs.json').read_text())
    args.audit.mkdir(parents=True,exist_ok=True)
    rows = []
    vectors = {}
    for raw in cards:
        page = raw['page']
        svg = (reader/raw['file']).read_text()
        root = ElementTree.fromstring(svg)
        category = specs.get(page,{}).get('type','field_schematic')
        vectors[page] = f'<div data-page="{page}">{svg}</div>'
        geometry = [(node.tag.split('}')[-1],{k:v for k,v in node.attrib.items()
                     if k not in {'fill','stroke','stroke-width','id'}})
                    for group in root.iter() if group.get('id','').endswith('artwork')
                    for node in group.iter() if not node.tag.endswith(('text','g'))]
        rows.append(dict(page=page,figure=raw['id'],category=category,sha256=raw['sha256'],
                         geometry_sha12=hashlib.sha256(repr(geometry).encode()).hexdigest()[:12] if geometry else '',
                         provenance='Original conceptual SVG',clipped_labels='',overlap_pairs=0,
                         visual_inspection='Bounds checked. Subject review pending.'))
    checked = svg_samples(rows)
    for row in checked:
        row['visual_inspection'] = 'Representative render retained. Subject review pending.'
    with tempfile.TemporaryDirectory() as tmp, sync_playwright() as pw:
        html = Path(tmp)/'vectors.html'
        browser = pw.chromium.launch(executable_path=shutil.which('google-chrome') or shutil.which('chromium'))
        page = browser.new_page(offline=True,viewport={'width':980,'height':900})
        for i in range(0,len(rows),65):
            batch = rows[i:i+65]
            html.write_text('<!doctype html><meta charset="utf-8"><style>svg{display:block;width:720px}</style>'
                            + ''.join(vectors[row['page']] for row in batch))
            page.goto(html.as_uri())
            measured = page.evaluate("""() => [...document.querySelectorAll('svg')].map(svg=>{
                const v=svg.viewBox.baseVal;
                const labels=[...svg.querySelectorAll('text')].map(el=>({t:el.textContent,b:el.getBBox()}));
                const clipped=labels.filter(({b})=>b.x<v.x-0.1||b.y<v.y-0.1||b.x+b.width>v.x+v.width+0.1||b.y+b.height>v.y+v.height+0.1);
                let overlaps=0;
                labels.forEach(({b:p},i)=>labels.slice(i+1).forEach(({b:q})=>{
                    if (Math.min(p.x+p.width,q.x+q.width)-Math.max(p.x,q.x)>2 &&
                        Math.min(p.y+p.height,q.y+q.height)-Math.max(p.y,q.y)>2) overlaps++;
                }));
                return {clipped:clipped.map(x=>x.t),overlaps};
            })""")
            for row, result in zip(batch,measured,strict=True):
                row['clipped_labels'] = ' | '.join(result['clipped'])
                row['overlap_pairs'] = result['overlaps']
        w,h=500,220
        sheet = Image.new('RGB',(2*w,((len(checked)+1)//2)*h),'#eeeae0')
        draw=ImageDraw.Draw(sheet)
        for i,row in enumerate(checked):
            page.set_content('<meta charset="utf-8"><style>body{margin:0}svg{width:720px;display:block}</style>'+vectors[row['page']])
            screenshot = page.locator('svg').screenshot()
            image = Image.open(BytesIO(screenshot)).convert('RGB')
            image.thumbnail((w-16,(h-30)))
            x,y=i%2*w,i//2*h
            sheet.paste(image,(x+8,y+25))
            draw.text((x+8,y+8),row['page']+' · '+row['category'],fill='#263d35')
        sheet.save(args.audit/'VECTOR_REPRESENTATIVE.jpg',quality=88)
        ImageOps.grayscale(sheet).save(args.audit/'VECTOR_GRAYSCALE.jpg',quality=88)
        browser.close()
    with (args.audit/'ILLUSTRATION_AUDIT.csv').open('w',newline='') as file:
        writer=csv.DictWriter(file,fieldnames=list(rows[0]),lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)
    clipped = sum(bool(row['clipped_labels']) for row in rows)
    overlaps = sum(row['overlap_pairs'] > 0 for row in rows)
    geom_counts = {}
    for row in rows:
        g = row['geometry_sha12']
        if g:
            geom_counts[g] = geom_counts.get(g, 0) + 1
    print(f'{len(rows)} SVGs measured, {len(checked)} rendered samples, {len(geom_counts)} distinct geometry groups, '
          f'{clipped} out of bounds, {overlaps} with intersecting text boxes.')
    if args.fail_layout and (clipped or overlaps):
        raise SystemExit('Figure label layout failed. See ILLUSTRATION_AUDIT.csv.')


if __name__=='__main__':
    main()
