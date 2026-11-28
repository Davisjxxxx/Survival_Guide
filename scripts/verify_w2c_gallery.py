"""Open the W2C photo gallery offline at 390 and 1280 px; record image loading, network requests, page errors,
horizontal overflow and axe-core WCAG 2.1 A/AA violations.

Usage: python verify_w2c_gallery.py ../foundations/visual/w2c_authentic_photos/index.html AXE.js OUT.json
"""
import json, sys
from pathlib import Path
from shutil import which
from playwright.sync_api import sync_playwright
page_path, axe, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).read_text(), Path(sys.argv[3])
rec = dict(page='visual/w2c_authentic_photos/index.html', widths=[390, 1280], network=[], errors=[], axe_violations=[], images={})
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=which('google-chrome'))
    for w in (390, 1280):
        ctx = b.new_context(viewport={'width': w, 'height': 900}); pg = ctx.new_page()
        pg.on('request', lambda r: rec['network'].append(r.url) if not r.url.startswith('file:') else None)
        pg.on('pageerror', lambda e: rec['errors'].append(str(e)))
        pg.goto(page_path.as_uri()); pg.wait_for_load_state('load')
        imgs = pg.evaluate('[...document.images].map(i => i.complete && i.naturalWidth > 0)')
        rec['images'][str(w)] = dict(count=len(imgs), loaded=sum(imgs))
        overflow = pg.evaluate('document.documentElement.scrollWidth > window.innerWidth + 1')
        if overflow: rec['errors'].append(f'horizontal overflow at {w}px')
        if w == 1280:
            pg.add_script_tag(content=axe)
            res = pg.evaluate('axe.run(document, {runOnly: {type: "tag", values: ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"]}})')
            rec['axe_violations'] = [v['id'] for v in res['violations']]
        ctx.close()
    b.close()
out.write_text(json.dumps(rec, indent=1) + '\n')
print(json.dumps(rec))
