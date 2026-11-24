"""Exercise the standalone offline edition and produce QA and a single-card-per-sheet print proof."""
import argparse
from collections import Counter
import hashlib
import io
import json
from pathlib import Path
import shutil
import tempfile
from xml.etree import ElementTree

import pymupdf
from PIL import Image, ImageDraw
from playwright.sync_api import sync_playwright

from build_foundations import FOUND, require


def contents(page, output, cards):
    page.goto((output/'index.html').as_uri())
    require(page.locator('.catalog li').count()==len(cards), 'Contents count drift')
    page.keyboard.press('Tab')
    require(page.locator(':focus').get_attribute('href')=='#content','Keyboard skip missing')
    search = page.get_by_role('searchbox')
    search.fill(cards[-1]['id'])
    require(page.locator('.catalog li:not([hidden])').count()==1,'Search filter failed')
    page.locator('.catalog li:not([hidden]) a').click()
    require(page.locator('h1').inner_text()==cards[-1]['title'],'Search navigation failed')
    if len(cards)>1:
        page.get_by_role('link',name='Previous').click()
        require(page.locator('h1').inner_text()==cards[-2]['title'],'Previous failed')
        page.get_by_role('link',name='Next').click()
        require(page.locator('h1').inner_text()==cards[-1]['title'],'Next failed')


def print_card(page, card, pdf):
    with pymupdf.open(stream=page.pdf(format='Letter',print_background=True,
                                     prefer_css_page_size=True),filetype='pdf') as single:
        require(len(single)==1, f'Print overflow on {card["id"]}')
        sheet = single[0].get_text()
        required = [card['id'], 'When it applies','Equipment','Actions','Verify','Stop or change course',
                    'Publication hold','Qualified review pending']
        normal = ' '.join(sheet.split())
        for text in [*required,*[item['text'] for item in card['action']]]:
            require(' '.join(text.split()) in normal,f'Print missing content on {card["id"]}: {text}')
        pdf.insert_pdf(single)


def contact_sheet(pdf, cards, path):
    columns = 4
    width, height = 270, 358
    rows = (len(cards)+columns-1)//columns
    image = Image.new('RGB',(columns*width,rows*height),'#e8e8e0')
    draw = ImageDraw.Draw(image)
    for i,card in enumerate(cards):
        pix = pdf[i].get_pixmap(matrix=pymupdf.Matrix(.41,.41),alpha=False)
        thumb = Image.frombytes('RGB',(pix.width,pix.height),pix.samples)
        thumb.thumbnail((width-14,height-26))
        x,y = i%columns*width,i//columns*height
        image.paste(thumb,(x+7,y+21))
        draw.text((x+7,y+4),card['id'],fill='#173c31')
    image.save(path,quality=88)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--reader',type=Path,default=FOUND/'reader')
    parser.add_argument('--proofs',type=Path,default=FOUND/'proofs')
    parser.add_argument('--axe',type=Path)
    parser.add_argument('--batch')
    parser.add_argument('--name',default='foundations')
    args = parser.parse_args()
    output, proofs = args.reader.resolve(), args.proofs.resolve()
    proofs.mkdir(parents=True,exist_ok=True)
    cards = json.loads((output/'page-manifest.json').read_text())
    assets = json.loads((output/'asset-manifest.json').read_text())
    require(len(cards)==len(assets)==len({c['id'] for c in cards}), 'Missing or duplicate card/asset')
    require({a['page'] for a in assets}=={c['id'] for c in cards},'Orphaned figure')
    for asset in assets:
        raw = (output/asset['file']).read_bytes()
        require(hashlib.sha256(raw).hexdigest()==asset['sha256'] and asset['diagnostic_photo'] is False,
                f'Figure authenticity metadata mismatch: {asset["id"]}')
        svg = ElementTree.fromstring(raw)
        require(svg.tag=='{http://www.w3.org/2000/svg}svg' and not any(
            tag.tag.rsplit('}',1)[-1] in {'image','script','foreignObject'} or
            any(k.rsplit('}',1)[-1] in {'href','src'} for k in tag.attrib)
            for tag in svg.iter()),f'Nonlocal or invalid visual {asset["id"]}')

    shots = []
    widths = (320,390,1280)
    chosen = [card for card in cards if not args.batch or card['batch']==args.batch]
    require(chosen,'No cards in selected batch')
    reports = {'tested_cards': len(cards),'printed_cards': len(chosen),'widths':list(widths),
               'actual_browser_errors':[], 'http_requests':[], 'axe_incomplete':{},'axe_violations':{}}
    with pymupdf.open() as pdf, sync_playwright() as pw, tempfile.TemporaryDirectory(dir=proofs) as tmp:
        browser = pw.chromium.launch(executable_path=shutil.which('google-chrome') or shutil.which('chromium'))
        reports['chromium'] = browser.version
        for width in widths:
            context = browser.new_context(viewport={'width':width,'height':920},offline=True)
            page = context.new_page()
            page.on('pageerror',lambda e: reports['actual_browser_errors'].append(str(e)))
            page.on('request',lambda q: reports['http_requests'].append(q.url) if q.url.startswith(('http:','https:')) else None)
            contents(page,output,cards)
            if args.axe and width==1280:
                page.goto((output/'index.html').as_uri())
                page.add_script_tag(path=str(args.axe.resolve()))
                reports['axe_version'] = page.evaluate('axe.version')
                result = page.evaluate('''async()=>await axe.run({runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa']}})''')
                reports['axe_incomplete']['index'] = [i['id'] for i in result['incomplete']]
                reports['axe_violations']['index'] = [i['id'] for i in result['violations']]
            for card in cards:
                page.goto((output/f'{card["id"]}.html').as_uri())
                require(page.locator('h1').inner_text()==card['title'] and
                        page.evaluate('document.documentElement.scrollWidth <= innerWidth+1') and
                        page.locator('figure img').evaluate('(i) => i.complete && i.naturalWidth > 0'),
                        f'Layout, content or figure failed at {width}: {card["id"]}')
                require(page.locator('[data-claims]').count()==len(card['action'])+2,
                        f'Missing evidence markers on {card["id"]}')
                if args.axe and width==1280:
                    page.add_script_tag(path=str(args.axe.resolve()))
                    result = page.evaluate('''async()=>await axe.run({runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa']}})''')
                    reports['axe_incomplete'][card['id']] = [i['id'] for i in result['incomplete']]
                    reports['axe_violations'][card['id']] = [i['id'] for i in result['violations']]
                if width in (390,1280) and card==chosen[0]:
                    shot = Path(tmp)/f'{args.name}-{width}.png'
                    page.screenshot(path=shot,full_page=True)
                    shots.append(shot)
                if width==1280 and card in chosen:
                    print_card(page,card,pdf)
            context.close()
        browser.close()
        require(not reports['actual_browser_errors'] and not reports['http_requests'] and
                not any(reports['axe_violations'].values()),f'Browser checks failed: {reports}')
        require(len(pdf)==len(chosen),'Unexpected PDF page count')
        pdf.set_toc([[1,card['id']+' · '+card['title'],i] for i,card in enumerate(chosen,1)])
        pdf.set_metadata({'title':'Survival Field Encyclopedia · Foundational proof','subject':'Editorial review draft'})
        pdf.save(proofs/f'{args.name}.pdf',garbage=4,deflate=True)
        contact_sheet(pdf,chosen,proofs/f'{args.name}-contact.jpg')
        for shot in shots:
            shutil.copyfile(shot,proofs/shot.name)
    reports['zones'] = dict(Counter(c['zone'] for c in chosen))
    (proofs/f'{args.name}-qa.json').write_text(json.dumps(reports,indent=2)+'\n')
    print(f'PASS: {len(cards)} cards at {len(widths)} widths, {len(chosen)} printed sheets, '
          f'{len(reports["axe_violations"])} axe audits; no HTTP requests or JavaScript errors.')


if __name__ == '__main__':
    main()
