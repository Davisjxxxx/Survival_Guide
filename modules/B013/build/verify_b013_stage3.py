from playwright.sync_api import sync_playwright
from pathlib import Path
from functools import partial
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
import threading
p=Path('/mnt/data/survival_field_encyclopedia/B013_Ice_Safety_18_Page_Reader_REVIEW.html')
out=p.parent/'review_screenshots';out.mkdir(exist_ok=True)
httpd=ThreadingHTTPServer(('127.0.0.1', 0),partial(SimpleHTTPRequestHandler,directory=str(p.parent)))
threading.Thread(target=httpd.serve_forever,daemon=True).start()
with sync_playwright() as w:
 b=w.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-gpu'])
 page=b.new_page(viewport={'width':1280,'height':1050},device_scale_factor=1)
 error=[]
 page.on('pageerror',lambda e:error.append(str(e)))
 page.goto(f'http://127.0.0.1:{httpd.server_port}/{p.name}#p15',wait_until='load')
 for pid in ('P15','P16','P17','P18'):
  page.locator('#pages').select_option(pid)
  page.wait_for_timeout(100)
  active=page.locator('section.page.active').get_attribute('id')
  count=page.locator('#count').inner_text()
  box=page.locator('#'+pid).bounding_box()
  page.locator('#'+pid).screenshot(path=str(out/f'{pid}.png'))
  print(pid,active,count,'height',round(box['height']))
 page.set_viewport_size({'width':390,'height':844})
 page.locator('#pages').select_option('P18')
 page.locator('#P18').screenshot(path=str(out/'P18_mobile.png'))
 print('mobile overflow:',page.evaluate('document.documentElement.scrollWidth > window.innerWidth'))
 print('script errors:',error)
 b.close()

httpd.shutdown()
