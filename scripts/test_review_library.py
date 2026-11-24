"""File-URL Chromium validation with blocked networking and actual full-page captures."""
import json
import shutil
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw
import io

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'production/evidence'
OUT.mkdir(exist_ok=True)
library = ROOT/'reader'
leaves = sorted(library.glob('*-P*.html'))
assert len(leaves)==56
report = {'pages':len(leaves),'viewports':{},'errors':[],'network':[]}
with sync_playwright() as pw:
    browser = pw.chromium.launch(executable_path=shutil.which('google-chrome') or shutil.which('chromium'))
    report['chromium'] = browser.version
    for width in (1280,390,320):
        ctx = browser.new_context(viewport={'width':width,'height':900},offline=True)
        page = ctx.new_page()
        page.on('pageerror', lambda e: report['errors'].append(str(e)))
        page.on('request',lambda r: report['network'].append(r.url) if r.url.startswith(('https:','http:')) else None)
        defects = []
        page.goto((library/'index.html').as_uri())
        assert page.locator('h1').is_visible()
        assert page.locator('.emergency a').count()==4
        assert page.locator('.catalog a').evaluate_all(
            "(links)=>links.every(a=>a.href.startsWith('file:'))")
        for link in page.locator('.catalog a').all():
            assert (library/link.get_attribute('href').split('#')[0]).is_file()
        page.get_by_role('link',name='Witness to immersion').click()
        assert page.url.endswith('B013-P07.html')
        page.get_by_role('link',name='Next',exact=True).click()
        assert page.url.endswith('B013-P08.html')
        page.get_by_role('link',name='Previous',exact=True).click()
        page.keyboard.press('Control+Home')
        page.goto((library/'index.html').as_uri())
        page.keyboard.press('Tab')
        assert page.locator('.skip-link').evaluate('(a)=>a===document.activeElement')
        page.keyboard.press('Enter')
        assert page.url.endswith('#content')
        query = page.get_by_label('Search page titles and text')
        query.fill('saturated clothing')
        assert page.locator('li:visible a[href="B013-P08.html"]').count()==1
        query.fill('zzzzzzqqqq')
        assert 'No matching' in page.locator('#matches').inner_text()
        query.fill('')
        page.locator('#lookup').blur()
        page.evaluate('window.scrollTo(0,0)')
        if width in (390,1280):
            page.screenshot(path=OUT/f'contents-{width}.png')
        for i,f in enumerate(leaves):
            page.goto(f.as_uri())
            assert page.locator('main h1').is_visible(), f
            assert page.locator('.edition').is_visible()
            checks = page.evaluate("""() => ({
                overflow: document.documentElement.scrollWidth>innerWidth+1,
                broken: [...document.images].some(i=>!i.complete || !i.naturalWidth),
                missingAlt: [...document.images].filter(i=>!i.hasAttribute('alt')).length,
                hiddenBody: document.querySelector('main').getBoundingClientRect().height<180
            })""")
            if any(checks.values()): defects.append([f.name,checks])
            if width == 1280:
                shot = Image.open(io.BytesIO(page.screenshot(full_page=True))).convert('RGB')
                if f.stem in ('B012-P25','B013-P18','B014-P12'):
                    shot.save(OUT/(f.stem+'-desktop.png'))
                if i%8==0:
                    sheet=Image.new('RGB',(4*280,2*450),'white')
                    draw=ImageDraw.Draw(sheet)
                shot.thumbnail((274,420))
                x,y=(i%4)*280,((i%8)//4)*450
                sheet.paste(shot,(x,y+23));draw.text((x+4,y+4),f.stem,fill='black')
                if i%8==7:sheet.save(OUT/f'pages-{i-6:02}-{i+1:02}.jpg',quality=90)
            if width==390 and f.stem in ('B013-P18','B012-P25','B014-P12'):
                page.screenshot(path=OUT/(f.stem+'-mobile.png'),full_page=True)
        report['viewports'][width]=defects
        ctx.close()
    browser.close()
(OUT/'browser.json').write_text(json.dumps(report,indent=2)+'\n')
print(report)
assert not any(report['viewports'].values()) and not report['errors'] and not report['network']
