#!/usr/bin/env python3
"""Verify editorial HTML behavior without a local HTTP server.
Requirements: playwright Python binding and a local Chromium browser.
This verifies rendering/interaction only, not real-world safety content.
"""
from __future__ import annotations
import os, re, shutil, sys
from pathlib import Path
from xml.etree import ElementTree as ET
from playwright.sync_api import sync_playwright

HERE=Path(__file__).resolve().parent
out=HERE.parents[2]/'production/evidence/b014-standalone'
out.mkdir(parents=True,exist_ok=True)
reader=HERE.parent/'reader'/'B014_P11_P20_Standalone_Reader_REVIEW.html'
content=reader.read_text(encoding='utf-8')
assert len(re.findall(r'class="page" id="P\d\d"',content))==10
assert len(re.findall(r'<option value="P\d\d"',content))==10
assert len(list((HERE.parent/'visuals/stage1').glob('*.svg')))==10
for f in sorted((HERE.parent/'visuals/stage1').glob('*.svg')):ET.fromstring(f.read_text())
with sync_playwright() as pw:
    executable=os.getenv('PLAYWRIGHT_CHROMIUM') or shutil.which('chromium') or shutil.which('google-chrome')
    kwargs={'headless':True,'args':['--no-sandbox','--disable-dev-shm-usage']}
    if executable:kwargs['executable_path']=executable
    browser=pw.chromium.launch(**kwargs)
    desktop=browser.new_page(viewport={'width':1150,'height':900})
    desktop.set_content(content,wait_until='load')
    assert desktop.locator('section.page.active').get_attribute('id')=='P11'
    desktop.locator('#following').click()
    assert desktop.locator('section.page.active').get_attribute('id')=='P12'
    desktop.locator('#chooser').select_option('P19')
    assert desktop.locator('section.page.active').get_attribute('id')=='P19'
    desktop.keyboard.press('ArrowRight')
    assert desktop.locator('section.page.active').get_attribute('id')=='P20'
    assert desktop.locator('section.page.active img').evaluate('(img) => img.complete && img.naturalWidth > 0')
    desktop.screenshot(path=str(out/'B014_stage1_preview_P20.png'),full_page=True)
    mobile=browser.new_page(viewport={'width':390,'height':844},device_scale_factor=1)
    mobile.set_content(content,wait_until='load')
    assert mobile.evaluate('document.body.scrollWidth <= window.innerWidth')
    mobile.screenshot(path=str(out/'B014_stage1_mobile_P11.png'),full_page=True)
    browser.close()
print('PASS: static reader/pages/SVG, navigation controls, embedded image, responsive 390px width')
