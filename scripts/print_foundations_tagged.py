"""Render document-level tagged HTML proofs while retaining their logical structure."""
import argparse
from hashlib import sha256
from html import escape
import json
from pathlib import Path
import re
import shutil
import tempfile

from bs4 import BeautifulSoup
import pymupdf
from playwright.sync_api import sync_playwright

from build_foundations import FOUND, FOUNDATIONAL_ZONES, require
from verify_foundations import PAPER_SIZES, contact_sheet


def content(reader, card):
    soup = BeautifulSoup((reader/f'{card["id"]}.html').read_text(encoding='utf-8'),'html.parser')
    article = soup.find('article')
    article.find('details').decompose()
    for ref in article.select('sup a, a.atlas-link, a.xref'):
        ref.unwrap()
    for image in article.find_all('img'):
        image['src'] = (reader/image['src']).as_uri()
    return f'<section class="proof">{soup.select_one("aside.edition")}{article}</section>'


def normalize(value):
    joined = re.sub(r'(?<=\S)\n([-–—/])(?=\S)',r'\1',value)
    return ' '.join(re.sub(r'(?<=\S)([-–—/])\n(?=\S)',r'\1',joined).replace('**','').split())


def inspect(path, cards, fmt_key, bookmarks=False):
    fmt, width, height = PAPER_SIZES[fmt_key]
    with pymupdf.open(path) as proof:
        require(len(proof)==len(cards),f'{path.name}: expected {len(cards)} sheets, got {len(proof)}')
        catalog = proof.pdf_catalog()
        structure = proof.xref_get_key(catalog,'StructTreeRoot')
        lang = proof.xref_get_key(catalog,'Lang')
        require(structure[0]=='xref' and lang==('string','en'),f'Missing structure or language: {path}')
        require('/Marked true' in proof.xref_get_key(catalog,'MarkInfo')[1],f'Missing marked status: {path}')
        root_object = proof.xref_object(int(structure[1].split()[0]))
        require('/ParentTree' in root_object, f'Missing structure parent tree: {path}')
        figure_alts = sum(1 for xref in range(1,proof.xref_length())
                          if proof.xref_get_key(xref,'S')[1]=='/Figure'
                          and proof.xref_get_key(xref,'Alt')[0]=='string')
        require(figure_alts>=len(cards),f'Missing figure alternative text in {path}')
        toc = [[1, c['id']+' · '+c['title'], i] for i,c in enumerate(cards,1)]
        headings = ('When it applies ·', 'Equipment ·', 'Actions', 'Verify ·', 'Stop or change course ·')
        for page, card in zip(proof,cards,strict=True):
            require(abs(page.rect.width-width)<4 and abs(page.rect.height-height)<4,f'Wrong {fmt} sheet size')
            extracted = page.get_text()
            text = normalize(extracted)
            lines = [line.strip() for line in extracted.splitlines()]
            positions = [
                next((i for i, line in enumerate(lines)
                      if line == heading or heading.endswith('·') and line.startswith(heading + ' ')), -1)
                for heading in headings
            ]
            require(min(positions) >= 0 and positions == sorted(positions),
                    f'{path.name}: extracted section order changed on {card["id"]}')
            lines = [card['id'],card['title'],card['objective'],card['applies'],card['equipment'],
                     'Publication hold','Qualified review pending']
            lines += [item['text'] for item in [*card['action'],card['verify'],card['stop']]]
            if 'failure' in card:
                lines.append(card['failure']['text'])
            missing = [line for line in lines if normalize(line) not in text]
            require(not missing, f'{path.name}: content drift or clipping on {card["id"]}: {missing}')
            for block in page.get_text('blocks'):
                x0,y0,x1,y1 = block[:4]
                require(x0>=31 and y0>=28 and x1<=page.rect.width-30 and y1<=page.rect.height-27,
                        f'{path.name}: text outside margin bounds on {card["id"]}')
        if bookmarks:
            require(proof.get_toc()==toc,f'{path.name}: bookmark direction or label drift')
        else:
            proof.set_toc(toc)
            proof.saveIncr()
        return dict(sheets=len(cards),format=fmt,structure=True,language='en',
                    figure_alt_entries=figure_alts,bookmarks=len(toc),extracted_section_order=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--reader',type=Path,default=FOUND/'reader')
    parser.add_argument('--proofs',type=Path,default=FOUND/'proofs')
    parser.add_argument('--zone')
    parser.add_argument('--verify-only', action='store_true', help='Recheck retained PDFs and update their receipt')
    args = parser.parse_args()
    reader, proofs = args.reader.resolve(), args.proofs.resolve()
    proofs.mkdir(parents=True,exist_ok=True)
    cards = json.loads((reader/'page-manifest.json').read_text())
    zones = {zone:[c for c in cards if c['zone']==zone] for zone in sorted({c['zone'] for c in cards})}
    foundations = [c for c in cards if c['zone'] in FOUNDATIONAL_ZONES]
    recon = [c for c in cards if c['category']=='Reconstruction draft']
    editions = {'foundations':foundations,'encyclopedia':cards,
                **{zone: cs for zone,cs in zones.items() if len(cs)>1}}
    if args.zone:
        editions = {args.zone: zones[args.zone]}
    else:
        editions['reconstructions'] = recon
    outputs = []
    for name, selection in editions.items():
        letter = name if name in {'foundations', 'reconstructions'} else f'{name}-letter'
        outputs.append((f'{letter}.pdf', selection, 'letter', name))
        if name != 'reconstructions':
            outputs.append((f'{name}-a4.pdf', selection, 'a4', name))
    receipt = proofs/('tagged-print-qa.json' if not args.zone else f'{args.zone}-tagged-print-qa.json')
    if args.verify_only:
        results = {}
        for filename, selection, fmt, _ in outputs:
            output = proofs / filename
            results[filename] = inspect(output, selection, fmt, bookmarks=True)
            results[filename]['sha256'] = sha256(output.read_bytes()).hexdigest()
            print(filename, len(selection), 'verified retained sheets', flush=True)
        receipt.write_text(json.dumps(results, indent=2)+'\n')
        return
    parts = {c['id']:content(reader,c) for c in cards}
    results = {}
    with tempfile.TemporaryDirectory(dir=proofs) as tmp, sync_playwright() as pw:
        tmp = Path(tmp)
        browser = pw.chromium.launch(executable_path=shutil.which('google-chrome') or shutil.which('chromium'))
        page = browser.new_page(offline=True)
        for filename, selection, fmt, name in outputs:
            html = tmp/'proof.html'
            sections = ''.join(parts[c['id']] for c in selection)
            html.write_text(
                '<!doctype html><html lang="en"><meta charset="utf-8">'
                f'<title>Survival Field Encyclopedia · {escape(name)}</title>'
                f'<link rel="stylesheet" href="{(reader/"library.css").as_uri()}">'
                f'<link rel="stylesheet" href="{(reader/"edition.css").as_uri()}">'
                '<style>.proof+.proof{break-before:page}</style>'
                f'<body class="library foundation"><main>{sections}</main></body></html>', encoding='utf-8')
            page.goto(html.as_uri())
            output = tmp / filename
            page.pdf(path=output,format=PAPER_SIZES[fmt][0],print_background=True,tagged=True)
            inspect(output,selection,fmt)
            results[filename] = inspect(output,selection,fmt,bookmarks=True)
            results[filename]['sha256'] = sha256(output.read_bytes()).hexdigest()
            output.replace(proofs/filename)
            print(filename, len(selection), 'sheets with tags, language, alt text and verified bookmarks',flush=True)
        browser.close()
    receipt.write_text(json.dumps(results,indent=2)+'\n')


if __name__=='__main__':
    main()
