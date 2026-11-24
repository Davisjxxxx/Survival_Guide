"""Build the C1 baseline, concordance, asset and claim review queues."""
import csv
import hashlib
import io
import json
from pathlib import Path
from zipfile import ZipFile
from bs4 import BeautifulSoup

BASE = '56645a0b2fb92421500511c058dc58d0503622f2'
DEST = Path('production/evidence')
ICE = Path('modules/B013')
DNR = 'https://www.dnr.state.mn.us/safety/ice/'
REFERENCES = {
    'T':DNR+'thickness.html', 'C':DNR+'ice-formations-conditions.html',
    'M':DNR+'check-ice-thickness.html', 'S':DNR+'survival.html', 'W':DNR+'saving.html',
    'G':DNR+'ice-safety-gear.html','R':DNR+'travel.html',
    'A':'https://www.cdc.gov/winter-weather/prevention/index.html',
    'N':'https://www.nps.gov/articles/gtgemergencyplan.htm',
    'F':'https://www.dnr.state.mn.us/regulations/fishing/index.html'}
# Pointers to actual sections. Scenario judgements remain explicitly open.
PAGE_REFS = ['R C','C T','C T','R N','T M G','S G','W','A S','C','C T','T M',
             'W R','W N','W G','F R T','F G R','C T M','S W A']
GROUPS = ('h1,.sheet-head p,.lead,.step,svg,.mobile-diag li,.checklist li,.faults tr,.caution')


def rows(path, header, records):
    with (DEST/path).open('w',newline='') as f:
        w=csv.writer(f)
        w.writerow(header.split('|'))
        w.writerows(records)


def read_archive(z, pattern):
    name = next(n for n in z.namelist() if pattern in n)
    return list(csv.DictReader(io.StringIO(z.read(name).decode('utf-8-sig'))))


def main():
    old,new=sorted((ICE/'reader').glob('*.html'))
    inputs=[old,new,*sorted(Path('imports/local-downloads').rglob('B013*.zip')),*sorted((ICE/'visuals').glob('*.svg')),*sorted((ICE/'review_packages').glob('*.zip'))]
    rows('ice-baseline.csv','commit|path|bytes|sha256',[(BASE,p,p.stat().st_size,hashlib.sha256(p.read_bytes()).hexdigest()) for p in inputs])
    before,after=[BeautifulSoup(p.read_text(),'html5lib') for p in (old,new)]
    ids=[p['id'] for p in after.select('section.page')]
    assert ids==[f'P{i:02}' for i in range(1,19)]==[o['value'] for o in after.select('#pages option')]
    decisions = {}
    with Path('production/ice-source-review.csv').open() as f:
        for row in csv.DictReader(f):
            for span in row['blocks'].split():
                ends = list(map(int,span.split('-')))
                for index in range(ends[0],ends[-1]+1):
                    decisions[row['page'],index]=(row['sources'],row['editorial disposition'])
    pages=[]; claims=[]; visuals=[]; used_decisions=set()
    for i,pid in enumerate(ids):
        page=after.select_one('#'+pid)
        prev=before.select_one('#'+pid)
        if i<14: assert prev is not None and str(prev)==str(page)
        pages.append([pid,page.h1.text,'Identical parsed page subtree' if prev else 'Stage 3 addition',pid in ids])
        owner='Ice rescue'
        if pid in ('P08','P18'): owner+=' and wilderness medicine'
        if pid in ('P15','P16'): owner+=' and Minnesota angling regulations'
        compiled = BeautifulSoup(Path('reader',f'B013-{pid}.html').read_text(),'html5lib')
        edition_blocks = compiled.select_one('#'+pid).select(GROUPS)
        historical = page.select(GROUPS)
        # P18 replaces the second figure and its four mobile repeats with the two-role figure.
        retained = [j for j in range(1,len(historical)+1) if pid!='P18' or not 9<=j<=13]
        assert len(edition_blocks)==len(retained)
        edition = dict(zip(retained,edition_blocks))
        for j,block in enumerate(historical,1):
            text=block.get_text(' ',strip=True)
            if (pid,j) in decisions:
                refs,note = decisions[pid,j]
                used_decisions.add((pid,j))
            elif 'someone has fallen through' in text:
                refs,note = 'W','Witness emergency footer.'
            elif block.name=='h1':
                refs,note = PAGE_REFS[i],'Editorial title. See the decision blocks on this page.'
            else:
                raise ValueError(f'Missing editorial disposition for {pid}-{j}')
            effective = edition[j].get_text(' ',strip=True) if j in edition else 'Removed from review edition'
            if j in edition:
                assert block.name == edition[j].name
            if 'someone has fallen through' in text:
                refs+=' W'
                note='Common emergency footer. DNR recommends calling 911 immediately for a witnessed immersion.'
            claims.append([pid+'-'+str(j),pid,block.name,' '.join(block.get('class',[])),text,effective,
                           ' '.join(REFERENCES[k] for k in refs.split()),
                           note,'2026-11-24',
                           owner,'HOLD'])
        for j,v in enumerate(page.select('img,svg'),1):
            visuals.append([pid+'-embedded-'+str(j),pid,'embedded '+v.name,
                            v.get('alt') or v.get('aria-label') or v.get_text(' ',strip=True),
                            str(new)+'#'+pid,'Staged scene' if v.name=='img' else 'Project schematic',
                            'Historical reader; use limited to review',owner,'Present; specialist validation HOLD'])
    assert set(decisions)==used_decisions, set(decisions)-used_decisions
    rows('ice-page-comparison.csv','page|title|comparison|navigation',pages)
    rows('ice-claim-queue.csv','id|page|element|class|exact claim or grouped diagram and correction|review edition wording|primary source pointers|AI disposition|source check date|review owner|release',claims)
    compact,stage2=sorted(Path('imports/local-downloads').rglob('B013*.zip'))
    for src in [compact,stage2]:
        with ZipFile(src) as z:
            for r in read_archive(z,'VISUAL_ASSET_REGISTER'):
                visuals.append([r['asset_id'],r.get('page_id') or r['page'],r.get('asset_type') or r['kind'],
                                r.get('intended_subject') or r['subject'],str(src),r.get('required_source') or r['kind'],
                                r.get('rights_status','No license recorded'),'Ice rescue',r['acquisition_status']])
    src=ICE/'research/B013_stage3_asset_manifest.csv'
    for r in csv.DictReader(src.open()):
        visuals.append([r['asset_id'],r['page'],r['role'],r['purpose'],str(src),r['origin'],r['rights'],'Ice rescue',r['status']])
    for r in json.loads(Path('production/photos/provenance.json').read_text()):
        if not r['page'].startswith('B013'): continue
        visuals.append([Path(r['original']).stem,r['page'][-3:],'documentary photo',r['caption'],r['source'],r['credit'],r['rights'],'Ice rescue',r['disposition']])
    visuals.append(['B013-P18-review-roles','P18','review edition SVG','Separate actions for witness and person in water',
                    'production/illustrations/immersion-roles.svg','Original editable project diagram','Editorial review',
                    'Ice rescue and wilderness medicine','Replaces two Stage 3 diagrams in the unified edition'])
    rows('ice-visual-register.csv','asset id|page|role|caption or planned subject|source artifact|origin or required provenance|rights|review owner|status',visuals)


if __name__=='__main__':main()
