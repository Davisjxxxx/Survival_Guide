"""Check printed destinations, visible edition markings and text; render review samples."""
import re
from pathlib import Path

import pymupdf
from PIL import Image, ImageDraw
from bs4 import BeautifulSoup

from build_review_library import EMERGENCY

root = Path(__file__).resolve().parents[1]
output = root / 'production'
with pymupdf.open(output/'Survival-Field-Encyclopedia-Review.pdf') as doc:
    toc = doc.get_toc()
    pages = {title.split(' · ')[0]: number for level,title,number in toc if level==2}
    assert set(pages)=={p.stem for p in (root/'reader').glob('*-P*.html')}
    cover = doc[0].get_text()
    for key,title in EMERGENCY.items():
        assert re.search(re.escape(title)+r'\s+'+str(pages[key])+r'\b',cover), title
    for level,title,number in toc:
        if level==1:
            assert re.search(re.escape(title.replace(' proof',''))+r'\s+'+str(number)+r'\b',cover),title
    for i,page in enumerate(doc,1):
        text = page.get_text().strip()
        assert 'NOT APPROVED FOR FIELD USE' in text.upper() and text.endswith('\n'+str(i)),i
    for key,number in pages.items():
        text = doc[number-1].get_text()
        heading = BeautifulSoup((root/'reader'/(key+'.html')).read_text(),'html.parser').h1.get_text(' ',strip=True)
        normalize = lambda s: ''.join(c for c in s.casefold() if c.isalnum())
        assert normalize(heading) in normalize(text),key
    winter = ' '.join(doc[n].get_text() for n in range(pages['B012-P25']-1,pages['B012-P26']-1))
    assert '37–39°C' in winter and 'Do not thaw now' not in winter
    sample = [1, pages['B012-P15'], pages['B012-P25'], pages['B013-P18'], pages['B014-P12'],
              pages['B014-P20'],next(n for _,t,n in toc if t.startswith('B007A ·')),
              next(n for _,t,n in toc if t.startswith('B008 ·')),next(n for _,t,n in toc if t.startswith('B010 ·'))]
    sheet = Image.new('RGB',(1110,1290),'#ece9df')
    draw = ImageDraw.Draw(sheet)
    for index,number in enumerate(sample):
        pix = doc[number-1].get_pixmap(matrix=pymupdf.Matrix(.65,.65),alpha=False)
        image = Image.frombytes('RGB',(pix.width,pix.height),pix.samples)
        image.thumbnail((360,400))
        x,y=index%3*370,index//3*430
        sheet.paste(image,(x,y+21))
        draw.text((x+5,y+3),f'Print proof page {number}',fill='#111')
    sheet.save(output/'evidence/print-contact.jpg',quality=90)
    print(f'{len(doc)} numbered sheets; {len(pages)} chapter destinations; directory and edition labels verified')
