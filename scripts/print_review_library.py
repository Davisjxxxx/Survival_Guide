"""Assemble the bookmarked, numbered owner proof from the offline reader."""
import io
import shutil
from html import escape
from pathlib import Path

import pymupdf
from playwright.sync_api import sync_playwright
from pypdf import PdfReader, PdfWriter

from build_review_library import CHAPTERS, EMERGENCY

root = Path(__file__).resolve().parents[1]
library = root / 'reader'
output = root / 'production/Survival-Field-Encyclopedia-Review.pdf'
writer = PdfWriter()
directory = {}
emergencies = {}


def render(page, scale=1):
    pdf = page.pdf(format='Letter', print_background=True, scale=scale,
                   display_header_footer=True, header_template='<span></span>',
                   footer_template='<div style="text-align:center;width:100%;font:9px sans-serif">EDITORIAL REVIEW · NOT APPROVED FOR FIELD USE</div>',
                   margin={'top':'0.45in','bottom':'0.5in','left':'0.4in','right':'0.4in'})
    return PdfReader(io.BytesIO(pdf))


def contents_table(entries):
    return ''.join(f'<tr><td>{escape(title)}</td><td>{number}</td></tr>'
                   for title, number in entries.items())


with sync_playwright() as pw:
    browser = pw.chromium.launch(executable_path=shutil.which('google-chrome') or shutil.which('chromium'))
    page = browser.new_page(offline=True)
    for module, title in CHAPTERS.items():
        parent = None
        directory[title] = len(writer.pages) + 2
        for source in sorted(library.glob(module+'-P*.html')):
            page.goto(source.as_uri())
            doc = render(page,.83)
            for scale, threshold in ((.76,400),(.70,220)):
                if len(doc.pages)>1 and len(doc.pages[-1].extract_text().strip())<threshold:
                    doc = render(page,scale)
            first = len(writer.pages)
            if source.stem in EMERGENCY:
                emergencies[EMERGENCY[source.stem]] = first + 2
            writer.append(doc, import_outline=False)
            if parent is None:
                parent = writer.add_outline_item(title=title, page_number=first)
            writer.add_outline_item(title=source.stem+' · '+page.locator('main h1').inner_text(),
                                    page_number=first, parent=parent)
    page.goto((library/'B007.html').as_uri())
    directory['B007 · Wood selection'] = len(writer.pages)+2
    writer.append(render(page),outline_item='B007 · Wood selection proof')
    titles = {'B003':'Field procedure cards','B007A':'Bow-drill cordage',
              'B008':'Friction fire (revision)','B008-original':'Friction fire (original)',
              'B009':'Water (revision)','B009-original':'Water (original)','B010':'Mechanism plates'}
    for module, title in titles.items():
        label = module + ' · ' + title
        directory[label] = len(writer.pages)+2
        writer.append(str(library/(module+'.pdf')),outline_item=label)
    assert len(emergencies)==len(EMERGENCY)
    page.set_content('<html lang="en"><title>Review edition directory</title><style>'
                     'body{font:12pt Arial;color:#173e32;margin:0.35in}h1{font:38pt Georgia;line-height:1;margin:.2em 0}'
                     'h2{font:21pt Georgia;margin:.55em 0 .2em}table{border-collapse:collapse;width:100%}'
                     'td{border-bottom:1px solid #cad4cc;padding:4px 0}td+td{text-align:right}'
                     '</style><p>Minnesota &amp; the Upper Midwest</p><h1>Survival Field Encyclopedia</h1>'
                     '<p>Owner review edition · November 24, 2026</p><h2>Emergency reference</h2><table>'
                     +contents_table(emergencies)+'</table><h2>Contents</h2><table>'+contents_table(directory)
                     +'</table><p>North Woods navigation begins at P11. Historical proofs retain their original pagination within each sheet.</p></html>')
    cover = render(page)
    assert len(cover.pages)==1
    writer.insert_page(cover.pages[0],0)
    browser.close()

writer.add_metadata({'/Title':'Survival Field Encyclopedia — owner review proof','/Subject':'Not approved for field use'})
assembled = io.BytesIO()
writer.write(assembled)
with pymupdf.open(stream=assembled.getvalue(),filetype='pdf') as doc:
    for number, sheet in enumerate(doc,1):
        sheet.insert_text((sheet.rect.width-47,sheet.rect.height-7), str(number),fontsize=8,color=(.12,.22,.18))
    doc.save(output,garbage=4,deflate=True)
print(output, len(writer.pages))
