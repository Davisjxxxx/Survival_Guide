from playwright.sync_api import sync_playwright
from pathlib import Path
from functools import partial
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
import threading
import os
import shutil
p=next((Path(__file__).resolve().parents[1]/'reader').glob('*18*html'))
out=Path(__file__).resolve().parents[3]/'production/evidence/b013-standalone'
out.mkdir(parents=True,exist_ok=True)
httpd=ThreadingHTTPServer(('127.0.0.1', 0),partial(SimpleHTTPRequestHandler,directory=str(p.parent)))
threading.Thread(target=httpd.serve_forever,daemon=True).start()
with sync_playwright() as w:
 b=w.chromium.launch(headless=True,executable_path=os.environ.get('PLAYWRIGHT_CHROMIUM') or shutil.which('chromium') or shutil.which('google-chrome'),args=['--no-sandbox','--disable-gpu'])
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
  assert active == pid and box['height'] > 0 and count.startswith(str(int(pid[1:]))+' of ')
  print(pid,active,count,'height',round(box['height']))
 page.set_viewport_size({'width':390,'height':844})
 page.locator('#pages').select_option('P18')
 page.locator('#P18').screenshot(path=str(out/'P18_mobile.png'))
 print('mobile overflow:',page.evaluate('document.documentElement.scrollWidth > window.innerWidth'))
 assert not page.evaluate('document.documentElement.scrollWidth > window.innerWidth')
 assert not error, error
 print('script errors:',error)
 b.close()

httpd.shutdown()
