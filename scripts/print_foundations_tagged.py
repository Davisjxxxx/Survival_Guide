"""Render document-level tagged HTML proofs while retaining their logical structure.

Each receipt entry records the source inputs the PDF was printed from (RT01-06): per-card
fingerprints of the printed body and embedded figure, and a digest of the print stylesheets
(scripts/proof_inputs.py). --editions prints a subset and merges it into the main receipt;
--verify-only rechecks retained PDFs without restamping their recorded inputs.
"""
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

from build_foundations import FOUND, require
from proof_inputs import PROOF_TEMPLATE, editions as proof_editions, fingerprint, proof_section
from verify_foundations import PAPER_SIZES, contact_sheet


def content(reader, card):
    return proof_section(reader, card, absolute=True)[0]


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
    parser.add_argument('--zone', help='Print one zone edition (same as --editions ZONE)')
    parser.add_argument('--editions', help='Comma-separated editions to print, e.g. Z14,Z15,reconstructions')
    parser.add_argument('--verify-only', action='store_true', help='Recheck retained PDFs without restamping inputs')
    args = parser.parse_args()
    reader, proofs = args.reader.resolve(), args.proofs.resolve()
    proofs.mkdir(parents=True,exist_ok=True)
    cards = json.loads((reader/'page-manifest.json').read_text())
    editions = proof_editions(cards)
    wanted = args.editions or args.zone
    if wanted:
        names = [n.strip() for n in wanted.split(',') if n.strip()]
        require(set(names) <= set(editions), f'Unknown proof edition: {sorted(set(names) - set(editions))}')
        editions = {n: editions[n] for n in names}
    outputs = []
    for name, selection in editions.items():
        letter = name if name in {'foundations', 'reconstructions'} else f'{name}-letter'
        outputs.append((f'{letter}.pdf', selection, 'letter', name))
        if name != 'reconstructions':
            outputs.append((f'{name}-a4.pdf', selection, 'a4', name))
    receipt = proofs/'tagged-print-qa.json'
    previous = json.loads(receipt.read_text()) if receipt.is_file() else {}
    if args.verify_only:
        results = dict(previous)
        for filename, selection, fmt, _ in outputs:
            output = proofs / filename
            results[filename] = inspect(output, selection, fmt, bookmarks=True)
            results[filename]['sha256'] = sha256(output.read_bytes()).hexdigest()
            for key in ('style_inputs', 'page_inputs'):          # keep what the PDF was printed from
                if key in previous.get(filename, {}):
                    results[filename][key] = previous[filename][key]
            print(filename, len(selection), 'verified retained sheets', flush=True)
        receipt.write_text(json.dumps(results, indent=2)+'\n')
        return
    selected = {c['id'] for _, selection, _, _ in outputs for c in selection}
    parts = {c['id']:content(reader,c) for c in cards if c['id'] in selected}
    cache = {}
    results = dict(previous)
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
                f'{PROOF_TEMPLATE}{sections}</main></body></html>', encoding='utf-8')
            page.goto(html.as_uri())
            output = tmp / filename
            page.pdf(path=output,format=PAPER_SIZES[fmt][0],print_background=True,tagged=True)
            inspect(output,selection,fmt)
            results[filename] = inspect(output,selection,fmt,bookmarks=True)
            results[filename]['sha256'] = sha256(output.read_bytes()).hexdigest()
            results[filename].update(fingerprint(reader, selection, cache))
            output.replace(proofs/filename)
            print(filename, len(selection), 'sheets with tags, language, alt text and verified bookmarks',flush=True)
        browser.close()
    receipt.write_text(json.dumps(dict(sorted(results.items())),indent=2)+'\n')


if __name__=='__main__':
    main()
