"""Build the offline review edition from retained chapter sources. Run from repository root."""
import json
import mistune
import pymupdf
import shutil
import subprocess
import tempfile
from collections import defaultdict
from html import escape
from pathlib import Path
from zipfile import ZipFile

from bs4 import BeautifulSoup
from PIL import Image

from audit_b012_recovery import audit, DATA

OUT = Path('reader')
PROD = Path('production')
CHAPTERS = {'B012': 'Winter survival', 'B013': 'Minnesota ice safety',
            'B014': 'North Woods navigation · P11–P20 supplement'}
DRAFT = '<div class="edition">Editorial review edition · Not approved for field use</div>'
HEAD = ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">')
JUMP = '<a class="skip-link" href="#content">Skip to content</a>'
EMERGENCY = {'B013-P06': 'Ice breakthrough', 'B013-P07': 'Witness to immersion',
             'B012-P24': 'Hypothermia', 'B014-P20': 'Lost in winter'}
PHOTOS = json.loads((PROD/'photos/provenance.json').read_text())


def soup(markup):
    # The HTML5 parser preserves SVG viewBox and other mixed-case attributes.
    return BeautifulSoup(markup, 'html5lib')


def get_leaves():
    source = next(Path('imports/local-downloads').rglob('B012_28_PAGE_OFFLINE_DRAFT_READER.html'))
    with tempfile.TemporaryDirectory() as tmp:
        corrected = Path(tmp, 'winter.html')
        audit(source, Path('modules/B012/reconciliation/B012_P13_P18_EDITORIAL_OVERLAY_DRAFT.json'), corrected)
        for page in json.loads(DATA.search(corrected.read_text()).group(2)):
            raw = page['html']
            if page['id'] == 'P08':
                raw = raw.replace('Medical care; do not rewarm', 'Seek care; delay active thaw')
                raw = raw.replace('Plan warming only where refreezing can be prevented.',
                                  'Plan active rewarming only where refreezing can be prevented. Allow spontaneous thawing and protect the area.')
            if page['id'] == 'P25':
                raw = raw.replace('Avoid thawing if the tissue may freeze again before care.',
                                  'Delay active rewarming if tissue could refreeze. Allow natural thawing and protect the area.')
                raw = raw.replace('Do not thaw now', 'Delay active rewarming')
                old = '37–40°C (99–104°F)'
                assert raw.count(old) == 1
                raw = raw.replace(old, '37–39°C (98.6–102.2°F)').replace(
                    'Seek rescue rather than risking repeated freezing.',
                    'Seek rescue. Allow spontaneous thawing and protect against refreezing. Never use snow or ice to keep tissue frozen.')
            s = soup(raw)
            for diagram in s.select('svg[role="img"]:not([aria-label]):not([aria-labelledby])'):
                diagram['aria-label'] = ' '.join(t.get_text(' ',strip=True) for t in diagram.select('text'))
            heading = s.body.select_one('.title,h2')
            heading.name = 'h1'
            yield 'B012', page['id'], page['title'], s.style.string, s.body
    for module, pattern in [('B013', '*18*html'), ('B014', '*html')]:
        doc = soup(next(Path('modules',module,'reader').glob(pattern)).read_text())
        for page in doc.select('section.page'):
            if module == 'B013':
                for node in list(page.find_all(string=True)):
                    # Avoid rounding the four-inch conditional minimum downward.
                    revised = str(node).replace('(10 cm)', '(10.16 cm)')
                    revised = revised.replace('Wear proper flotation', 'Wear foam flotation')
                    revised = revised.replace('911 if confusion / drowsy', 'Seek emergency help')
                    revised = revised.replace('One participant calls “911” in the scenario',
                                              'One participant simulates the call without dialing 911')
                    if revised != node:
                        node.replace_with(revised)
            if module == 'B013' and page['id'] == 'P01':
                page.select_one('.lead').string = 'Stay on stable land when ice conditions are uncertain. Even measured ice can vary along a route.'
            if module == 'B014' and page['id'] == 'P14':
                scenario = page.select_one('.scenario')
                for node in scenario.find_all(string=True):
                    if 'while the map uses geographic north' in node:
                        node.replace_with(node.replace('while the map uses geographic north',
                                                       'while this example uses true north. Check your map legend for its actual north reference'))
            if module == 'B014' and page['id'] == 'P20':
                for node in page.find_all(string=lambda value: value and 'reset to the last verified point' in value):
                    node.replace_with(node.replace('reset to the last verified point',
                                                   'identify the last verified point. Retrace only if the route is certain and safe'))
            if module == 'B013' and page['id'] == 'P16':
                page.select_one('.lead').string = 'This guide recommends staying on land when you lack safe access, ice assessment equipment or rescue equipment. It does not recommend improvised hole-making.'
            if page['id'] == 'P15' and module == 'B013':
                page.select_one('.lead').append(' Long stationary loads have separate DNR guidelines. A walking measurement cannot clear a fishing site.')
            if page['id'] == 'P18' and module == 'B013':
                a,b = page.select('svg')
                a.replace_with(soup((PROD/'illustrations/immersion-roles.svg').read_text()).svg)
                b.find_parent(class_='diag').decompose()
                page.select_one('.steps h2').string = 'Actions by role'
                for number in page.select('.step .num'):
                    number.string = '•'
            yield module, page['id'], page.h1.text, '\n'.join(str(t.string) for t in doc.select('style')), page


def photo_assets():
    for photo in PHOTOS:
        path = Path(photo['original'])
        with Image.open(path) as im:
            im.thumbnail((960,640))
            im.convert('RGB').save(OUT/path.name,quality=86)
    subprocess.run(['pdftoppm','-scale-to','3200','-x','690','-y','1500','-W','1100','-H','550',
                    '-jpeg','-singlefile',str(next((PROD/'maps').glob('*.pdf'))),str(OUT/'ely-1965')], check=True)


def observation(key):
    for photo in PHOTOS:
        if key == photo['page']:
            caption = escape(photo['caption']+' Photograph by '+photo['credit']+'.')
            return f'<figure class="observation"><img src="{Path(photo["original"]).name}" alt="{caption}"><figcaption>{caption}</figcaption></figure>'
    if key in ('B014-P12','B014-P19'):
        return ('<figure class="observation"><img src="ely-1965.jpg" alt="Historical map excerpt showing lakes separated by land and elevation contours near Ely.">'
                '<figcaption>Water barriers near Ely, Minnesota. USGS, 1965. The original sheet was printed at 1:24,000. '
                'Use this historical excerpt to read symbols only. Travel conditions and routes require current information.</figcaption></figure>')
    return ''


def contents_link(key,title,index):
    return f'<li data-index="{escape((key+" "+title+" "+index).lower(),quote=True)}"><a href="{key}.html"><small>{key}</small> · {escape(title)}</a></li>'


def supplements():
    """Retain original pagination and index the selectable PDF text."""
    hist = Path('imports/track-b-history')
    files = {}
    for module, pattern in [('B003','*003.zip'), ('B008-original','*008*Complete.zip'),
                            ('B009-original','*009*Complete.zip')]:
        with ZipFile(next(hist.glob(pattern))) as archive:
            member, = [name for name in archive.namelist() if name.lower().endswith('.pdf')]
            files[module] = archive.read(member)
    files['B007A'] = (hist/'Bow_Drill_Cordage_Field_Plates_007A.pdf').read_bytes()
    for module in ('008','009'):
        files['B'+module] = next(hist.glob('Track_B_'+module+'*.pdf')).read_bytes()
    files['B010'] = next(Path('imports/local-downloads').rglob('Survival_Field_Encyclopedia_010_Mechanism_Plates.pdf')).read_bytes()
    entries = []
    for module, original in sorted(files.items()):
        # Extend each sheet outside the original artwork. Printed/extracted pages retain review status.
        with pymupdf.open(stream=original, filetype='pdf') as proof, pymupdf.open() as labelled:
            for sheet in proof:
                area = sheet.rect
                dest = labelled.new_page(width=area.width, height=area.height+20)
                dest.show_pdf_page(area, proof, sheet.number)
                dest.insert_text((12,area.height+13), 'EDITORIAL REVIEW  |  HISTORICAL PROOF  |  NOT APPROVED FOR FIELD USE', fontsize=8)
            labelled.save(OUT/(module+'.pdf'), deflate=True, garbage=4, no_new_id=True)
        pages = subprocess.check_output(['pdftotext','-layout',str(OUT/(module+'.pdf')),'-']).decode().split('\f')
        for i,page in enumerate(pages,1):
            if not page.strip(): continue
            lines = [s.strip() for s in page.splitlines() if s.strip()]
            title = next((s for s in lines[:5] if len(s)>8 and 'TRACK B' not in s.upper()),lines[0])
            text = escape((module+' '+' '.join(lines)).lower(),quote=True)
            entries.append(f'<li data-index="{text}"><a href="{module}.pdf#page={i}">{module} · p. {i} · {escape(title)}</a></li>')
    with ZipFile(next(hist.glob('*007*.zip'))) as z:
        plate = z.read(next(n for n in z.namelist() if n.endswith('READER_PLATE.md'))).decode()
    html = mistune.create_markdown(plugins=['table'])(plate)
    (OUT/'B007.html').write_text(HEAD+'<title>Wood selection · B007</title><link rel="stylesheet" href="library.css"></head><body class="library">'+DRAFT+
        '<div class="folio"><a href="index.html">Contents &amp; search</a></div><main id="content">'+html+'</main></body></html>')
    entries.append(contents_link('B007','Friction fire wood selection',soup(html).get_text(' ',strip=True)))
    return ''.join(entries)


def main():
    OUT.mkdir(exist_ok=True)
    for name in ('library.css','search.js'):
        shutil.copyfile(PROD/'templates'/name,OUT/name)
    photo_assets()
    leaves = list(get_leaves())
    keys = [m+'-'+p for m,p,*_ in leaves]
    assert len(keys)==len(set(keys))==56
    groups = defaultdict(list)
    for i,(module,pid,title,styles,fragment) in enumerate(leaves):
        key = keys[i]
        body = fragment.decode_contents() if fragment.name=='body' else str(fragment)
        mast = f'<a href="index.html#{module}">{escape(CHAPTERS[module])}</a>'
        for label,idx in [('Previous',i-1),('Next',i+1)]:
            if 0<=idx<len(keys):
                mast += f'<a href="{keys[idx]}.html">{label}</a>'
        nav = '<div class="folio" role="navigation" aria-label="Chapter navigation"><a href="index.html">Contents &amp; search</a>'+mast+'</div>'
        doc = (HEAD+f'<title>{escape(title)} · {key}</title><style>{styles}</style><link rel="stylesheet" href="library.css"></head><body>'
               +JUMP+DRAFT+nav+'<main class="leaf" id="content">'+body+observation(key)+'</main></body></html>')
        (OUT/(key+'.html')).write_text(doc)
        groups[module].append(contents_link(key,title,CHAPTERS[module]+' '+soup(body+observation(key)).get_text(' ',strip=True)))
    chapters = ''.join(f'<section id="{m}"><h2>{escape(CHAPTERS[m])}</h2><ul>{"".join(groups[m])}</ul></section>' for m in CHAPTERS)
    chapters += '<section><h2>Earlier illustrated proofs</h2><ul>'+supplements()+'</ul></section>'
    quick = ''.join(f'<a href="{k}.html">{v}</a>' for k,v in EMERGENCY.items())
    (OUT/'index.html').write_text(HEAD+'<title>Survival Field Encyclopedia · Review edition</title><link rel="stylesheet" href="library.css"></head><body class="library">'+JUMP+DRAFT+
        '<header class="cover-panel"><div><p>Minnesota &amp; the Upper Midwest</p><h1>Survival Field Encyclopedia</h1></div><img src="ice-breakup-0.jpg" alt="Broken river ice at Fisher, Minnesota, photographed by the USGS."></header>'
        '<main id="content"><h2>Emergency reference</h2><nav class="emergency" aria-label="Emergency reference">'+quick+
        '</nav><h2>Chapter directory</h2><div class="lookup"><label for="lookup">Search page titles and text</label><input type="search" id="lookup" placeholder="e.g. wet clothing"><p id="matches" role="status"></p></div><div class="catalog">'+chapters+
        '</div></main><script src="search.js"></script></body></html>')


if __name__ == '__main__':
    main()
