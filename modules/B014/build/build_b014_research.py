from pathlib import Path
import csv, zipfile
p=Path('/mnt/data/survival_field_encyclopedia')
out=p/'B014_North_Woods_Navigation_Research_Continuation.md'
rows=[
 ('P11','North Woods whiteout: whether to stop or move','No-gear cold/visibility triage; known-route safe retrace vs shelter + help','Four-stage annotated snowstorm sequence; visibility inset; stop/move failure pair','NPS-PLAN;NWS-MN','P0'),
 ('P12','Lake, marsh and river barriers','No unmeasured frozen-water shortcut; route assessment must use verified land','Original conceptual map; rights-cleared USGS topo excerpt; bog/lake detour overlay','USGS-MAP;DNR-ICE','P0'),
 ('P13','No-compass orientation: limitations','Stop if clues conflict; sun/shadow only conditional; moss is not a compass','Comparative clue reliability matrix; uncertainty diagram; rejected-moss photo','NPS-PLAN;DNR-FOREST','P1'),
 ('P14','Compass bearing errors and local declination','Use current date/location-specific declination; verify map/grid and compass consistency','Diagram true vs magnetic north; bearing change examples with neutral numerical placeholders','NOAA-DECL;USGS-MAP','P1'),
 ('P15','Phone GPS failure, offline maps and battery','Device position may remain useful offline; no communications assumed; map/compass backup','Offline vs network comparison; lost-phone/no-battery decision chart','NPS-WINTER;NPS-PLAN','P1'),
 ('P16','Visibility and signaling under canopy','Whistle, bright contrast, location description; do not climb dangerous trees','Forest canopy cross-section; aerial versus ground visibility; distress sequence','NPS-PLAN;DNR-HIKE','P1'),
 ('P17','Group / child lost-person protocol','Keep parties together, establish meet-up; for separated children teach stay-put/Hug-a-Tree','Group accountability diagram; child-safe 4-frame instruction; reunion failure pair','NPS-PLAN','P0'),
 ('P18','Overnight decision and energy conservation','Short daylight, wetness, cold injury and safe shelter decisions; no speculative night travel','Daylight timeline with weather conditions; shelter / calling decision map','NWS-MN;DNR-FOREST','P0'),
 ('P19','Navigation failure atlas','Wrong single clue, unwarranted river-following, snow tracks, unverified landmarks, ice shortcut','Six original misconception/correction plates; verified topo examples','NPS-PLAN;USGS-MAP;DNR-ICE','P0'),
 ('P20','Lost in winter: tear-out action reference','Stop/assess/identify/safely retrace; call 911; shelter and signal if cannot','One-page illustrated no-gear → improvised → equipped rescue decision card','NPS-PLAN;DNR-FOREST;NWS-MN','P0')
]
sources=[
 ('NPS-PLAN','US National Park Service','Outdoor Emergency Plan','https://www.nps.gov/articles/gtgemergencyplan.htm','Lost-person decisions, calling 911, stay put, child protocol'),
 ('NPS-WINTER','US National Park Service','Winter Hiking Tips','https://home.nps.gov/articles/000/winterhikingtips.htm','Winter map/compass and digital backup'),
 ('DNR-FOREST','Minnesota DNR','Safety in state forests','https://www.dnr.state.mn.us/state-forests/safety.html','Minnesota backcountry preparation, trails, topo, cold risk'),
 ('DNR-HIKE','Minnesota DNR','Hiking safety tips','https://www.dnr.state.mn.us/hiking/safety.html','Group, route, signaling, basic equipment'),
 ('NWS-MN','NOAA National Weather Service','Minnesota Winter Hazard Awareness Week','https://www.weather.gov/mpx/winterpns1','Whiteout / severe winter warning environment'),
 ('USGS-MAP','US Geological Survey','US Topo Map Symbol Guide','https://www.usgs.gov/ngp-standards-and-specifications/us-topo-map-symbol-guide','Map symbols, water, roads, contours'),
 ('NOAA-DECL','NOAA National Centers for Environmental Information','Magnetic Declination','https://www.ngdc.noaa.gov/geomag/declination.shtml','True vs magnetic bearings; change by place and date'),
 ('DNR-ICE','Minnesota DNR','Ice safety','https://www.dnr.state.mn.us/safety/ice/index.html','No assurance of ice strength or shortcut')
]
with (p/'B014_stage0_source_register.csv').open('w',encoding='utf-8',newline='') as f:
 w=csv.writer(f);w.writerow(['source_id','agency','title','url','evidence_scope']);w.writerows(sources)
with (p/'B014_stage0_page_and_visual_register.csv').open('w',encoding='utf-8',newline='') as f:
 w=csv.writer(f);w.writerow(['page','provisional_title','content_requirement','visual_targets','evidence_ids','priority','status']);w.writerows([(*r,'EDITORIAL_PLAN_ONLY') for r in rows])

svg='''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 675" role="img" aria-label="Original schematic lost in North Woods blizzard decision chart; not a real map or field test">
<defs><linearGradient id="bg" x2="0.8" y2="1"><stop stop-color="#e7f2f5"/><stop offset="1" stop-color="#fdfbf2"/></linearGradient></defs>
<rect width="1200" height="675" fill="url(#bg)"/><rect width="1200" height="84" fill="#153f31"/><text x="43" y="52" font-family="Arial" font-size="30" fill="white" font-weight="700">LOST IN MINNESOTA'S NORTH WOODS · WINTER DECISION</text>
<text x="42" y="119" font-family="Arial" fill="#38574b" font-size="20">No equipment first. Unknown location is NOT a reason to walk at random.</text>
<rect x="365" y="144" width="468" height="93" rx="13" fill="#214b3e"/><text x="600" y="180" text-anchor="middle" font-family="Arial" font-weight="700" fill="white" font-size="23">STOP. ASSESS IMMEDIATE RISK.</text><text x="600" y="209" text-anchor="middle" font-family="Arial" fill="#d7e8d8" font-size="17">injury • wet clothing • wind • daylight • danger</text>
<path d="M600 236V272 M600 272H294 M600 272H905 M294 272V305 M905 272V305" fill="none" stroke="#669b89" stroke-width="5"/>
<rect x="67" y="302" width="451" height="170" rx="15" fill="#e2eee6" stroke="#8bac9a" stroke-width="2"/><text x="292" y="343" text-anchor="middle" font-family="Arial" fill="#173d30" font-size="23" font-weight="700">SAFE, KNOWN ROUTE?</text><text x="292" y="383" text-anchor="middle" font-family="Arial" fill="#235146" font-size="18">Locate with reliable evidence</text><text x="292" y="418" text-anchor="middle" font-family="Arial" fill="#235146" font-size="18">Retrace only if safe and certain</text><text x="292" y="448" text-anchor="middle" font-family="Arial" fill="#a24e38" font-size="16">Stop if landmarks or conditions conflict</text>
<rect x="684" y="302" width="451" height="170" rx="15" fill="#f8ebe1" stroke="#ce9d83" stroke-width="2"/><text x="910" y="343" text-anchor="middle" font-family="Arial" fill="#9f4030" font-size="23" font-weight="700">UNKNOWN / UNSAFE?</text><text x="910" y="382" text-anchor="middle" font-family="Arial" fill="#235146" font-size="18">Avoid unnecessary travel</text><text x="910" y="414" text-anchor="middle" font-family="Arial" fill="#235146" font-size="18">Call 911 if possible</text><text x="910" y="446" text-anchor="middle" font-family="Arial" fill="#235146" font-size="18">Shelter, warmth and signaling</text>
<path d="M294 472V511 M910 472V511" stroke="#669b89" stroke-width="5"/>
<rect x="68" y="510" width="1066" height="100" rx="13" fill="#dce9ed" stroke="#9eb4bd"/><text x="601" y="546" text-anchor="middle" font-family="Arial" font-size="21" font-weight="700" fill="#153f31">NO GEAR: conserve heat and keep location stable · IMPROVISED: shelter + contrast signals</text><text x="601" y="581" text-anchor="middle" font-family="Arial" font-size="19" fill="#1c4c62">EQUIPPED: map + compass + offline GPS + whistle + SOS communications</text>
<text x="44" y="649" font-family="Arial" font-size="15" font-weight="700" fill="#a14936">ORIGINAL CONCEPT SCHEMATIC — NOT A REAL ROUTE, WEATHER OBSERVATION, OR FIELD-TESTED PROCEDURE</text>
</svg>'''
(p/'B014_Lost_In_Snowstorm_Decision_Schematic.svg').write_text(svg,encoding='utf-8')
md='''# B014 · North Woods Navigation | Continuation research brief

**Survival Field Encyclopedia / Track B**  
**Research date:** 2026-11-22  
**Status:** Source-backed editorial outline; **NOT PUBLICATION READY**. Existing B014 P01–P10 coverage was described in a prior production package, but those source files are not mounted here. Do not claim they were rewritten or inspected. The following are provisional **P11–P20** drafts that must be reconciled against that existing package before integration.

## Objective and fixed boundaries
Build an original, offline-first Minnesota North Woods navigation chapter. First teach what a person does with no tools, then improvised or salvaged alternatives, then properly equipped methods. Each reader page has concrete prerequisites, 4 sequential actions when warranted, verification cues, failure/correction and an abort condition. Unsafe uncertainty has a no-go outcome. References, reviewer decisions and rights/provenance remain outside the reader. No real field photographs, authentic species images or actual maps have been acquired in this brief.

## P11–P20 continuation storyboard

| Page | Illustrated topic | Required visual / key stop condition |
|---|---|---|
'''
for page,title,content,visual,ids,priority in rows:
 md+=f'| {page} | {title} | {visual}; **stop** if route, landmark, weather or terrain confidence fails |\n'
md+='''
## Research findings that change the editorial treatment

1. **Lost-person decision is conditional, not always “stay put” or always “walk out.”** The NPS recommends stopping, establishing position from reliable evidence and retracing only if safe. If the person cannot confidently retrace, call for help, stay put unless an immediate life threat requires relocation, protect from weather and signal. That must be the central decision diagram. Source: NPS-PLAN.
2. **The Minnesota-specific winter layer matters.** Terrain, short daylight, moisture, snow-obscured tracks, winds and rapidly decreasing visibility may make travel less safe than sheltering. Source: DNR-FOREST; NWS-MN; NPS-WINTER.
3. **A map is not the ground truth.** Use current USGS-style topology to interpret wetlands, water and elevation; locate ground landmarks, and never treat a simplified schematic as a real route. Source: USGS-MAP.
4. **Declination cannot be permanently hard-coded.** The angle between magnetic and true north changes with location and time; future field examples need a dated NOAA lookup for a specified map area. Source: NOAA-DECL.
5. **Do not promote natural orientation myths.** Moss, stream flow, a single shadow or tree growth do not independently establish safe travel direction in the North Woods. Present any observational clue with limitations, cross-checks, and a stop condition. The no-gear fallback is protect yourself and signal, not an invented bearing. Editorial risk item: SME review required.
6. **Child scenarios require distinct presentation.** NPS provides a stay-in-one-place, Hug-a-Tree approach for lost children; illustrate it separately from adult navigation methods. Source: NPS-PLAN.

## Illustration reproduction plan

- One original scenario map (conceptual only), showing trail, wetland, lake and winter obstruction without claiming actual geography.
- Four visual actions for P11/P20: stop and assess → verify known route → decide whether safe to retrace → if not, shelter/signal.
- Close-up gear/method panels: compass housing, map legend, whistle, phone offline-map status, battery insulation and signaling material. Separate gearless method from equipped method.
- Failure and correction comparisons: tracks hidden by new snow; cold-battery loss; lake ice shortcut; moss as false compass; wetland drawn as passable land; self-directed random search.
- Authentic, rights-cleared and independently verified Minnesota topographic/map excerpts needed for P12/P14/P19. **None acquired**; generic synthetic maps must carry “not for actual navigation.”
- Rights and provenance ledger must record source URL, author/agency, reuse rights, EXIF or capture context, reviewer, and approval.

## Claim and acceptance gate

- Assert no compass bearing, declination value, route distance or field-safe ice without verified location, measurement and authority.
- Qualified navigation/search-rescue reviewer must confirm adult and child lost-person procedures, scenarios, diagrams and field consequences.
- A local winter safety reviewer must check storm/exposure priorities and all stop conditions.
- Owner must approve after independent review; **Track B editorial stage only, Gate A BLOCKED**. No production ingestion, publishing or repo modifications.

## Primary references (full links in CSV)
'''
for sid,agency,title,url,scope in sources:
 md+=f'- **{sid}:** {agency}, [{title}]({url}). {scope}.\n'
out.write_text(md,encoding='utf-8')

zip_path=p/'B014_North_Woods_Research_Continuation_Packet.zip'
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED,compresslevel=7) as z:
 for n in [out.name,'B014_stage0_source_register.csv','B014_stage0_page_and_visual_register.csv','B014_Lost_In_Snowstorm_Decision_Schematic.svg']:
  z.write(p/n,arcname=n)
print('Created',out, out.stat().st_size,'bytes')
print('Created',zip_path,zip_path.stat().st_size,'bytes')
