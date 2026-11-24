"""Run locally installed axe-core against the offline HTML review edition."""
import argparse
import json
import shutil
from pathlib import Path
from playwright.sync_api import sync_playwright

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('axe',type=Path,help='Path to axe.min.js from the axe-core package')
args=parser.parse_args()
root=Path(__file__).resolve().parents[1]
files=sorted((root/'reader').glob('*.html'))
results={}
with sync_playwright() as w:
    browser=w.chromium.launch(executable_path=shutil.which('google-chrome') or shutil.which('chromium'))
    page=browser.new_page(offline=True)
    for f in files:
        page.goto(f.as_uri())
        page.add_script_tag(path=str(args.axe.resolve()))
        result=page.evaluate("""async()=>{const r=await axe.run({runOnly:{type:'tag',values:
        ['wcag2a','wcag2aa','wcag21a','wcag21aa']}});return {
        violations:r.violations.map(v=>({rule:v.id,nodes:v.nodes.map(n=>n.target)})),
        incomplete:r.incomplete.map(v=>v.id)}}""")
        results[f.name]=result
    report={'axe':page.evaluate('axe.version'),'engine':browser.version,'pages':results}
    browser.close()
(root/'production/evidence/accessibility.json').write_text(json.dumps(report,indent=2)+'\n')
fail=[p for p,r in results.items() if r['violations']]
print(len(files),'pages checked;',len(fail),'with violations')
assert not fail, fail
