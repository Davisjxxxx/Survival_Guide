#!/usr/bin/env python3
"""Nonpublication editorial assembly of B013 pages 15–18 into the existing 14-page reader."""
from __future__ import annotations
from bs4 import BeautifulSoup
from pathlib import Path
from html import escape
from datetime import date
import csv, json, re, shutil, zipfile

ROOT=Path('/mnt/data/survival_field_encyclopedia')
SOURCE=ROOT/'B013_Ice_Safety_14_Page_Reader.html'
OUT=ROOT/'B013_Ice_Safety_18_Page_Reader_REVIEW.html'
ASSETS=ROOT/'B013_stage3_assets'
ASSETS.mkdir(exist_ok=True)

GREEN='#163f30'; MINT='#d9ede1'; CREAM='#fff9ea'; RUST='#ad5037'; ICE='#dcecf4'; NAVY='#21475a'; DARK='#1c352d'

def svg_start(title):
 return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 820 390" role="img" aria-label="{escape(title,quote=True)}" width="820" height="390"><defs><linearGradient id="sky" x2="0" y2="1"><stop offset="0" stop-color="#e3eff5"/><stop offset="1" stop-color="#f9fbf8"/></linearGradient><pattern id="hatch" width="12" height="12" patternUnits="userSpaceOnUse"><path d="M0 12L12 0" stroke="#c2d9e2" stroke-width="1"/></pattern></defs><rect x="0" y="0" width="820" height="390" rx="14" fill="url(#sky)"/>'''

def label(x,y,text,size=19,color=DARK,weight=700,anchor='start'):
 return f'<text x="{x}" y="{y}" fill="{color}" font-family="Arial,Helvetica,sans-serif" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">{escape(text)}</text>'

def ground():
 return '<path d="M0 236 Q156 215 280 227 L400 232 L400 390 L0 390Z" fill="#bbd1bc"/><path d="M0 239 Q120 218 277 229 L400 230" fill="none" stroke="#7c987e" stroke-width="5"/><path d="M400 231L820 228L820 390L400 390Z" fill="#bad7e5"/><path d="M400 232L820 232L820 260L400 260Z" fill="#f5fbff" stroke="#7eb1c5" stroke-width="2"/><path d="M400 260L820 260L820 390L400 390Z" fill="url(#hatch)" opacity=".9"/>'

def tree(x,y,scale=1):
 return f'<g transform="translate({x} {y}) scale({scale})"><rect x="-6" y="-7" width="12" height="58" fill="#6a6550"/><path d="M-36 26L0 -84L36 26Z" fill="#30634b"/><path d="M-29 -8L0 -92L29 -8Z" fill="#25543e"/><path d="M-20 -39L0 -103L20 -39Z" fill="#204a37"/><path d="M-22 -27L0 -49L20 -29" fill="none" stroke="#f2f8ef" stroke-width="5"/></g>'

def person(x,y,scale=1,stance='stand'):
 if stance=='stand':
  path='<circle cy="-57" r="12" fill="#eac9a2"/><path d="M-16 -43 L16 -43 L22 5 L-22 5Z" fill="#e17b3f" stroke="#643c2e" stroke-width="2"/><path d="M-10 5L-15 38 M10 5L15 38 M-16 -31L-27 -2 M16 -31L29 -2" stroke="#244c61" stroke-width="10" stroke-linecap="round"/>'
 else:
  path='<circle cx="-41" cy="-16" r="12" fill="#eac9a2"/><path d="M-22 -20 L30 -20 L36 0 L-20 0Z" fill="#e17b3f" stroke="#643c2e" stroke-width="2"/><path d="M34 -12L65 -16 M34 -1L68 2" stroke="#244c61" stroke-width="10" stroke-linecap="round"/>'
 return f'<g transform="translate({x} {y}) scale({scale})">{path}</g>'

def banner(x,y,w,text,fill=GREEN,txt='#fff'):
 return f'<rect x="{x}" y="{y}" rx="8" width="{w}" height="35" fill="{fill}"/>{label(x+w/2,y+23,text,17,txt,700,"middle")}'

def scene15():
 s=svg_start('Not a fishing shortcut: choose land and licensed shore access rather than unverifiable ice')+ground()+tree(120,195,1.3)+tree(218,202,.92)+person(307,208,1)
 s+=label(27,48,'WINTER ANGLING: THE DECISION IS FIRST',23,GREEN)+label(27,78,'A fish is never worth an unverified crossing.',17,NAVY,400)
 s+='<path d="M390 196 L409 242" stroke="#9a633e" stroke-width="5" stroke-dasharray="8 6"/>'
 s+='<path d="M505 160L605 265 M605 160L505 265" stroke="#ad4f38" stroke-width="15" stroke-linecap="round" opacity=".9"/>'
 s+=banner(236,272,170,'STAY ON LAND')+banner(626,280,171,'NO ICE ENTRY',RUST)
 s+=label(24,359,'Unmeasured ice  ≠  access',18,GREEN)
 s+='</svg>'; return s

def scene16():
 s=svg_start('No auger or ice tools means no safe ice fishing method; avoid punching or melting holes')+ground()+tree(145,191,1.25)+person(302,217,1)
 s+=label(28,47,'NO EQUIPMENT IS A STOP CONDITION',24,GREEN)+label(28,78,'Do not improvise a hole through lake ice.',17,NAVY,400)
 s+='<path d="M450 221L790 222" stroke="#b4ebff" stroke-width="9"/>'
 for x in (510,583,655):
  s+=f'<path d="M{x} 185l17 37 -23 33" fill="none" stroke="#af5546" stroke-width="5" stroke-linecap="round"/>'
 s+='<path d="M531 168L647 278 M647 168L531 278" stroke="#a94335" stroke-width="13" opacity=".92" stroke-linecap="round"/>'
 s+=banner(54,282,315,'PRIORITIZE WARMTH + SIGNALING')+banner(472,288,288,'DO NOT CUT / MELT',RUST)
 s+=label(24,360,'Wait for lawful access and proper equipment.',17,GREEN)
 s+='</svg>'; return s

def scene17():
 s=svg_start('Six misleading signs of unsafe Minnesota lake ice')
 s+=label(26,45,'WHAT PEOPLE MISTAKE FOR ICE SAFETY',24,GREEN)
 cells=[('TRACKS','Old crossings prove nothing.'),('COLD NIGHT','Thaw and current still matter.'),('ONE HOLE','Strength varies along a route.'),('WHITE ICE','Weaker than new clear ice.'),('SHORE EDGE','May be melted or detached.'),('FISH HOUSE','Someone else accepted a risk.')]
 for n,(a,b) in enumerate(cells):
  x=22+(n%3)*267; y=73+(n//3)*151
  s+=f'<rect x="{x}" y="{y}" width="252" height="138" rx="13" fill="#ffffff" stroke="#a8c0ba" stroke-width="2"/>'
  s+=f'<circle cx="{x+30}" cy="{y+30}" r="20" fill="#f4e0d4"/>{label(x+30,y+37,"!",23,RUST,800,"middle")}'
  s+=label(x+58,y+36,a,18,GREEN)
  # split long into two lines at spaces
  words=b.split(); lines=[]; cur=''
  for word in words:
   if len(cur+' '+word)>25 and cur:lines.append(cur);cur=word
   else:cur=(cur+' '+word).strip()
  if cur:lines.append(cur)
  for i,line in enumerate(lines):s+=label(x+18,y+80+i*25,line,15,NAVY,400)
 s+='</svg>';return s

def scene18():
 s=svg_start('Ice emergency: 911, safe-ground rescue, self-rescue if immersed, prevent heat loss')
 s+=label(26,48,'ICE EMERGENCY: DO THE NEXT SAFE ACTION',24,GREEN)
 cols=[('1','WITNESS','CALL 911','Give lake + access point'),('2','IN THE WATER','TURN + KICK','Exit toward your entry'),('3','AFTER EXIT','GET WARM','Get medical assessment')]
 for idx,(num,head,act,sub) in enumerate(cols):
  x=25+idx*269
  s+=f'<rect x="{x}" y="86" width="247" height="240" rx="13" fill="{["#e7f0ea","#eaf2f6","#f9ede3"][idx]}" stroke="#a7bbb3" stroke-width="2"/>'
  s+=f'<circle cx="{x+125}" cy="{137}" r="34" fill="{GREEN if idx!=1 else NAVY}"/>{label(x+125,149,num,34,"#fff",800,"middle")}'
  s+=label(x+124,204,head,18,GREEN,800,'middle')+label(x+124,240,act,19,RUST,800,'middle')
  s+=label(x+124,274,sub,14,NAVY,400,'middle')
  if idx<2:s+=f'<path d="M{x+254} 201l13 0m-8 -7l8 7 -8 7" stroke="{GREEN}" stroke-width="3" fill="none"/>'
 s+=label(26,364,'STAY OUT OF WEAK ICE • NO UNTRAINED ICE-EDGE RESCUE',18,RUST)
 s+='</svg>';return s

def map15():
 s=svg_start('Three-stage decision route for Minnesota ice angling')
 s+=label(28,45,'IF FISHING REQUIRES CROSSING FROZEN WATER',22,GREEN)
 for i,(head,txt,fill) in enumerate([('NO GEAR','Turn back; stay on land.','#f7ece3'),('IMPROVISED','Only lawful open-water shore fishing.','#f3f5e8'),('EQUIPPED','Plan, verify, measure; still no guarantee.','#e1edeb')]):
  y=74+i*91
  s+=f'<rect x="27" y="{y}" width="766" height="78" rx="10" fill="{fill}" stroke="#9eaea4"/>'
  s+=label(45,y+32,head,19,GREEN,800)+label(265,y+34,txt,18,NAVY,400)
 s+=label(30,369,'Ice angling is optional: survival priorities always come first.',16,RUST,700)
 s+='</svg>';return s

def map16():
 s=svg_start('Limits of equipment-free fishing through lake ice: no approved safe hole-making approach')
 s+=label(26,46,'TOOL-FREE LIMITS: DO NOT SUBSTITUTE RISK',23,GREEN)
 for i,(t,b) in enumerate([('INTACT ICE','You cannot fish through intact ice.'),('NO VERIFIED ROUTE','Do not step onto the ice to explore.'),('NO ICE-CUTTING TOOL','Do not chip, burn, stomp or smash a hole.'),('SURVIVAL NEED','Choose shelter, warmth and rescue signaling.')]):
  x=30+(i%2)*384;y=74+(i//2)*130
  s+=f'<rect x="{x}" y="{y}" width="367" height="115" rx="12" fill="#fff" stroke="#b7c9c2" stroke-width="2"/>'
  s+=label(x+17,y+36,t,18,GREEN,800)+label(x+17,y+70,b,14,NAVY,400)
 s+='</svg>';return s

def map17():
 s=svg_start('Decision tree for false evidence about safe ice')
 s+=label(26,49,'ANY UNKNOWN OR CONFLICTING SIGNAL?',23,GREEN)
 s+=f'<rect x="258" y="80" width="304" height="68" rx="14" fill="{NAVY}"/>'+label(410,121,'DO NOT ENTER',24,'#fff',800,'middle')
 s+='<path d="M410 148V182M410 182H175M410 182H650M175 182V212M650 182V212" stroke="#679b8d" stroke-width="5" fill="none"/>'
 s+=f'<rect x="34" y="211" width="300" height="89" rx="10" fill="#f3e8de" stroke="#ae715d"/>'+label(184,245,'LAND DETOUR',19,RUST,800,'middle')+label(184,276,'Avoid the uncertain surface',14,NAVY,400,'middle')
 s+=f'<rect x="484" y="211" width="300" height="89" rx="10" fill="#e4f0e7" stroke="#7eaa90"/>'+label(634,245,'WAIT / CALL FOR HELP',19,GREEN,800,'middle')+label(634,276,'Do not self-clear conditions',14,NAVY,400,'middle')
 s+=label(26,353,'Presence of other people or equipment does not verify conditions.',16,NAVY,600)
 s+='</svg>';return s

def map18():
 s=svg_start('Ice emergency route: witness calls 911, immersion escape, warmth and medical care')
 s+=label(27,47,'EMERGENCY SEQUENCE',24,GREEN)
 actions=[('CALL','911 + exact place'),('STAY','On stable ground'),('ESCAPE','Turn back and kick'),('WARM','Shelter + medical help')]
 for i,(a,b) in enumerate(actions):
  x=24+i*204
  s+=f'<rect x="{x}" y="104" width="179" height="185" rx="13" fill="{["#dcece3","#e9f1e8","#dce9f1","#f7e7df"][i]}" stroke="#a8beb5" stroke-width="2"/>'
  s+=label(x+90,155,str(i+1).zfill(2),37,RUST,800,'middle')
  s+=label(x+90,202,a,23,GREEN,800,'middle')
  s+=label(x+90,242,b,14,NAVY,600,'middle')
  if i<3:s+=f'<path d="M{x+180} 194l19 0m-8 -8l8 8 -8 8" stroke="{GREEN}" stroke-width="3" fill="none"/>'
 s+=label(27,350,'Untrained rescuers must not become additional victims.',18,RUST,700)
 s+='</svg>';return s

PAGES=[
 dict(id='P15',sub='RECREATION / FISHING DECISIONS',title='FISHING IS NEVER THE FIRST PRIORITY',deck='If the fishing spot requires risky ice travel, abandon the fishing plan.',scene=scene15(),diagram=map15(),tag='ORIGINAL SAFETY SCHEMATIC · NOT A SITE PHOTOGRAPH',lead='No fish harvest can offset an uncontrolled immersion hazard. If you cannot establish safe access, do not enter the ice.',steps=[('No equipment: choose land','Keep yourself and companions on stable ground. Find a safe land detour or leave the area.'),('Improvised: do not improvise access','Only consider ordinary shore fishing at legally accessible open water, when conditions permit. Do not use improvised ice holes or traps.'),('Equipped: decide before traveling','Check the local lake and current DNR rules, tell a contact your plan, bring flotation and rescue equipment, and measure ice repeatedly.'),('Stop when conditions change','Snow, wind, current, spring deterioration and water near structures can invalidate a prior observation.')],check=['Fishing is optional; warmth, shelter, water and signaling take priority in an emergency.','Have a current angling license or an applicable exemption, and check lake-specific rules.','No part of this guide certifies ice travel.'],faults=[('Tracks or anglers nearby','Prior use is not evidence that present ice is safe.'),('Four inches somewhere','The DNR threshold refers to NEW, CLEAR ice, not a blanket route approval.'),('Fish are visible','Abandon the route if access is uncertain.')],stop='STOP: No verified safe route, inadequate equipment, unknown ice, or unstable weather means NO ICE ENTRY.'),
 dict(id='P16',sub='ZERO-EQUIPMENT LIMITS',title='NO TOOLS? DO NOT MAKE AN ICE HOLE',deck='Ice fishing is not a viable survival shortcut without safe access and proper tools.',scene=scene16(),diagram=map16(),tag='ORIGINAL DIAGRAM · METHODS SHOWN AS PROHIBITED CHOICES',lead='There is no reliable equipment-free method to penetrate intact lake ice while avoiding serious breakthrough risk.',steps=[('No gear: do not attempt ice fishing','Do not walk onto unknown ice. Prioritize protection from wind, dry insulation, finding shelter and contacting help.'),('Improvised: reject hole-making shortcuts','Do not stomp, strike, heat, chip or melt a fishing hole in natural ice with improvised materials.'),('If shore access exists','Only fish from stable ground into open water if that is physically possible and lawful. Fishing is secondary to safety.'),('Equipped: use a compliant plan','Angling gear, a properly used auger and appropriate ice safety equipment do not eliminate ice hazards; verify conditions before travel.')],check=['No one is standing or crouching on uncertain ice.','A legal fishing method and license/exemption are confirmed before angling.','No self-made rescue hazard is left on the ice.'],faults=[('A rock can break thin ice','Breaking a surface also creates a fall hazard: abandon the idea.'),('Build a fire to melt a hole','Do not compromise ice integrity or create a burning hazard.'),('Fish will solve starvation quickly','Acquiring calories may take time and increase cold exposure; prioritize rescue.')],stop='STOP: Do not teach improvised through-ice fishing as a validated zero-equipment technique.'),
 dict(id='P17',sub='FAILURE AND CORRECTION ATLAS',title='SIX FALSE SIGNS OF SAFE ICE',deck='Common observations can be correct but dangerously incomplete.',scene=scene17(),diagram=map17(),tag='ORIGINAL IDENTIFICATION/DECISION ATLAS · NOT FIELD TESTED',lead='An observation of appearance, activity or a single test is never a guarantee of safe ice along a proposed route.',steps=[('Someone crossed earlier','Footprints, ATV tracks and fish houses show activity, not an independent safety assessment.'),('There was a hard freeze last night','Snow cover can slow freezing; inlets, outlets and springs can remain weak.'),('The first drilled hole was thick','Ice thickness can differ greatly across one lake; the DNR recommends frequent checks.'),('The white surface looks substantial','White ice is weaker than clear new ice; appearance alone cannot classify every layer reliably.')],check=['Do not use the presence of tracks, structures or people as clearance.','Do not infer quality from surface color alone.','Choose a land-based alternative when conditions are uncertain.'],faults=[('Shore ice looks attached','Shallow water, vegetation and warmed structures can weaken edges.'),('A four-inch number is enough','Only a conditional minimum for new, clear ice on foot; never an all-purpose guarantee.'),('A buddy can always rescue me','Untrained ice-edge rescues create multiple victims; use professional responders.')],stop='STOP: ANY unresolved uncertainty is reason to stay off, not a prompt to experiment.'),
 dict(id='P18',sub='EMERGENCY DESK REFERENCE',title='AFTER A BREAKTHROUGH: ACT, DO NOT GUESS',deck='A compressed reminder for emergencies, not a substitute for rescue training.',scene=scene18(),diagram=map18(),tag='ORIGINAL EMERGENCY FLOW · TRAINING REVIEW REQUIRED',lead='Call 911 immediately. Report the lake, exact land access, number of people, and whether anyone remains in the water.',steps=[('If you witness the incident','Call 911 first. Stay on stable land. Offer reach/throw assistance only if possible without approaching weak ice.'),('If you are in the water','Control breathing as able. Face the direction you came from. Get your body horizontal, kick and pull toward that route.'),('Once out','Lie flat and roll or crawl away from the hole on the approach path. Move to shelter; prevent further heat loss.'),('After rescue or escape','Replace wet items with dry insulation when possible, insulate from the ground, protect from wind and seek emergency medical assessment.')],check=['Emergency dispatcher has precise lake/shore access information.','No bystander approaches an uncertain hole or makes a second victim.','Cold-water exposure is treated as a medical emergency.'],faults=[('Jump in to pull them out','Do not enter weak ice or water without professional rescue training.'),('Stand immediately after exiting','Remain low and move away from the hole on your entry route.'),('Aggressively warm limbs','Avoid rapid direct extremity heating and rough handling; follow emergency guidance.')],stop='STOP: A person in the water, altered consciousness, breathing difficulty, or significant cold exposure requires emergency response.'),
]

def fig(svg, width='100%'):
 # Inline editable SVG with built-in narrative, never an unproven photo.
 return svg.replace(' width="820" height="390"',' class="new-vector"')

def page_html(p):
 items=''.join(f'<div class="step"><div class="num">{i}</div><div><b>{escape(head)}</b>{escape(body)}</div></div>' for i,(head,body) in enumerate(p['steps'],1))
 checks=''.join(f'<li>{escape(x)}</li>' for x in p['check'])
 faults=''.join(f'<tr><td>{escape(a)}</td><td>{escape(b)}</td></tr>' for a,b in p['faults'])
 mobile=''.join(f'<li><b>{escape(a)}</b> — {escape(b)}</li>' for a,b in p['steps'])
 return f'''<section class="page" id="{p['id']}"><article class="sheet new-page"><div class="sheet-head"><div class="page-no">B013 · MINNESOTA ICE SAFETY · {p['id']} · {escape(p['sub'])}</div><h1>{escape(p['title'])}</h1><p>{escape(p['deck'])}</p></div>
 <div class="major"><div class="scene" aria-label="Original illustration, not a diagnostic photograph"><div class="original-figure">{fig(p['scene'])}</div><div class="tag">{escape(p['tag'])}</div></div>
 <div class="steps"><div class="lead">{escape(p['lead'])}</div><h2>FIELD ACTION · NO GEAR FIRST</h2>{items}</div></div>
 <div class="diag"><h2>VISUAL DECISION / METHOD</h2><div class="new-diag">{fig(p['diagram'])}</div><div class="mobile-diag"><ol>{mobile}</ol></div></div>
 <div class="footgrid"><section class="checklist"><h2>CHECK BEFORE CONTINUING</h2><ul>{checks}</ul></section>
 <section class="faults"><h2>WRONG SIGNAL → CORRECTION</h2><table>{faults}</table></section></div>
 <div class="caution">{escape(p['stop'])}</div><div class="readerfoot"><span>Original visual research draft · not field-tested · source, rights and review ledgers kept separately</span><span>B013 / {p['id']} · Editorial review only</span></div></article></section>'''

# Write SVG assets first; they are reusable for later specialist review and publication design.
for p in PAGES:
 (ASSETS/f'{p["id"]}_primary.svg').write_text(p['scene'],encoding='utf-8')
 (ASSETS/f'{p["id"]}_decision.svg').write_text(p['diagram'],encoding='utf-8')

# Avoid modifying the original 14-page file. Preserve the content and append a discrete Stage3 segment.
original=SOURCE.read_text(encoding='utf-8')
insert='\n<!-- B013-3 STAGE3 START: P15-P18; EDITORIAL REVIEW, NOT PUBLICATION -->\n'+''.join(page_html(p) for p in PAGES)+'\n<!-- B013-3 STAGE3 END -->\n'
assert '</section>' in original
# Stable boundary immediately before script (outside page and within wrap), and after existing P14.
pos=original.rfind('</section>',0,original.find('<script>'))
assert pos!=-1 and 'id="P14"' in original[:pos], 'could not find terminal page'
pos=pos+len('</section>')
new=original[:pos]+insert+original[pos:]
new=new.replace('14 pages assembled','18 pages assembled').replace('ILLUSTRATED FIELD REVIEW · 8 PAGES','ILLUSTRATED FIELD REVIEW · 18 PAGES')
new=new.replace('B013-2 added pages P09–P14 to the unchanged B013-1 draft.','B013-3 adds P15–P18 while preserving the existing P01–P14 research draft.')
# Existing 'next pages planned' note becomes revision note rather than a false pending statement.
new=new.replace('<strong>Next pages planned:</strong> shoreline thaw, snow-over-ice, thickness variability, family/pet safety, signaling, dry-land rescue practice, winter angling risk, and quick-reference atlas.', '<strong>Editorial checkpoint:</strong> 18 page topics drafted. Specialist review, rights-cleared field photographs and field validation remain outstanding.')
# Append selector options + update navigation arrays; no external JavaScript dependency.
needle='</select><button id="prev"'
assert needle in new
new=new.replace(needle,''.join(f'<option value="{p["id"]}">{p["id"]} · {escape(p["title"].title())}</option>' for p in PAGES)+needle)
new=new.replace('"P13", "P14"]','"P13", "P14", "P15", "P16", "P17", "P18"]')
new=new.replace('1 of 8','1 of 18')
extra_css='''\n/* Stage3: original, inspectable vector illustrations */
.original-figure{width:100%;min-height:210px;display:flex;align-items:center;background:#e9f2f1}
.original-figure .new-vector{width:100%;height:auto;display:block;max-height:300px}
.new-diag{background:#fff;border:1px solid var(--line);border-radius:9px;overflow:hidden}
.new-diag .new-vector{width:100%;height:auto;max-height:310px;display:block}
@media (max-width:760px){.new-diag{display:block}.new-diag .new-vector{height:auto;max-height:none}.original-figure{min-height:0}}
@media print{.new-page{page-break-inside:avoid}.new-page .new-vector{max-height:185px}.new-page .major{grid-template-columns:40% 1fr}.new-page .sheet-head h1{font-size:23px}.new-page .diag{padding-top:7px}.new-page .step{margin:2px 0}}
'''
new=new.replace('</style>',extra_css+'</style>',1)
OUT.write_text(new,encoding='utf-8')

SRC=[
 ('DNR-01','Minnesota DNR','How to check ice thickness','https://www.dnr.state.mn.us/safety/ice/check-ice-thickness.html','Primary agency guidance for measuring and 4 in new clear ice; precautions','Current page; accessed 2026-11-22'),
 ('DNR-02','Minnesota DNR','General ice thickness guidelines','https://www.dnr.state.mn.us/safety/ice/thickness.html','Conditional minima; thickness differences and factors; not ice clearance','Current page; accessed 2026-11-22'),
 ('DNR-03','Minnesota DNR','Ice formations and conditions','https://www.dnr.state.mn.us/safety/ice/ice-formations-conditions.html','White ice weakness; snow and shore deterioration','Current page; accessed 2026-11-22'),
 ('DNR-04','Minnesota DNR','Fishing in Minnesota','https://www.dnr.state.mn.us/fishing/index.html','Age-related license threshold, ice fishing baseline info','Current page; accessed 2026-11-22'),
 ('DNR-05','Minnesota DNR','Fishing regulations','https://www.dnr.state.mn.us/regulations/fishing/index.html','2026–27 license and lake-specific rule navigation','Current page; accessed 2026-11-22'),
 ('DNR-06','Minnesota DNR','Ice safety','https://www.dnr.state.mn.us/safety/ice/index.html','Never 100 percent safe; conditions vary','Current page; accessed 2026-11-22'),
 ('NWS-01','National Weather Service','Winter weather preparedness: ice safety','https://www.weather.gov/box/winter_safety','Surface cracks, cold-water self-rescue fundamentals; use with MN DNR','General; accessed 2026-11-22'),
 ('DNR-07','Minnesota DNR','Ice fishing shelters','https://www.dnr.state.mn.us/fishing/shelter.html','Shelter licensing and DNR ice measurement cadence','Current page; accessed 2026-11-22'),
]
with (ROOT/'B013_stage3_source_register.csv').open('w',encoding='utf-8',newline='') as f:
 w=csv.writer(f);w.writerow(['source_id','publisher','title','url','scope','evidence_status']);w.writerows(SRC)
CLAIMS=[
 ('B013-P15-01','P15','Fishing on lake ice requires an independent safety assessment; unknown ice = stay off.','DNR-02;DNR-06','Agency recommendation','draft_review'),
 ('B013-P15-02','P15','Angling license or exemption and lake-specific rules must be checked.','DNR-04;DNR-05','Legal/regulatory, verify at time of use','draft_review'),
 ('B013-P15-03','P15','The 4-inch guideline is for new clear ice only and does not authorize crossing.','DNR-01;DNR-02','Numerical conditional minimum','draft_review'),
 ('B013-P16-01','P16','Without safe access and proper tools, equipment-free through-ice fishing should not be attempted.','DNR-01;DNR-06','Editorial safety inference from guidance; needs specialist signoff','specialist_required'),
 ('B013-P16-02','P16','No improvised ice-hole construction method is recommended.','DNR-01;DNR-06','Conservative editorial decision, not published DNR prohibition','specialist_required'),
 ('B013-P17-01','P17','Ice varies greatly within a single water body.','DNR-02;DNR-03','Agency supported','draft_review'),
 ('B013-P17-02','P17','White ice is roughly half as strong as clear new ice; appearance never proves strength.','DNR-02;DNR-03','Agency supported; contextual','draft_review'),
 ('B013-P17-03','P17','Shoreline and transitions can be weak despite central ice.','DNR-03','Agency supported','draft_review'),
 ('B013-P18-01','P18','Report ice immersion to emergency services; witnesses should avoid entering weak ice.','DNR-06;NWS-01','Emergency guidance; specialist review pending','specialist_required'),
 ('B013-P18-02','P18','Self-rescue includes facing entry route, kicking horizontally and rolling or crawling away.','NWS-01','Emergency sequence; specialist review pending','specialist_required'),
 ('B013-P18-03','P18','Emergency rewarming and medical assessment require qualified clinician guidance.','DNR-06','Medical safety; qualified review required','specialist_required'),
]
with (ROOT/'B013_stage3_claim_ledger.csv').open('w',encoding='utf-8',newline='') as f:
 w=csv.writer(f);w.writerow(['claim_id','page','short_claim','source_ids','evidence_type','review_status']);w.writerows(CLAIMS)
with (ROOT/'B013_stage3_asset_manifest.csv').open('w',encoding='utf-8',newline='') as f:
 w=csv.writer(f);w.writerow(['asset_id','page','role','path','origin','rights','purpose','status'])
 for p in PAGES:
  for role in ('primary','decision'):
   w.writerow([p['id']+'-'+role,p['id'],role,f'B013_stage3_assets/{p["id"]}_{role}.svg','Original vector schematic generated in this project','Original project work','Safety communication; not observed condition','DRAFT_ONLY_NO_PUBLICATION'])
  w.writerow([p['id']+'-field-photo',p['id'],'future_verified_photo','NOT_ACQUIRED','Independent field observation','PENDING_RIGHTS_REVIEW','Real ice/field visual validation','MISSING_NO_PUBLICATION'])

readme='''# B013 Stage 3: Minnesota Ice Safety · Pages P15–P18

## Status
**Editorial draft, 18 of 18 planned reader pages assembled. NOT publication-ready.**
The 14-page source is preserved without modification. This package appends P15–P18, replacing no existing page content. The source and rights ledgers remain separate from the reader. The guide is an original work, not a reproduction of the text, photos or distinctive structure of any published survival book.

## Files
- `B013_Ice_Safety_18_Page_Reader_REVIEW.html` — self-contained offline reader; opens in a desktop/mobile browser, supports arrow keys, page selector, printing.
- `B013_stage3_assets/` — eight original editable SVG schematics, two for each new page.
- `B013_stage3_source_register.csv` — URLs, publisher, publication status of source facts.
- `B013_stage3_claim_ledger.csv` — high-risk claims linked to exact pages and sources.
- `B013_stage3_asset_manifest.csv` — asset provenance and pending real photographs.
- `B013_stage3_quality_checks.md` — publication-blocking review gate.

## Pages
- P15: Winter angling is secondary to ice safety, no gear > improvised > equipped
- P16: No validated tool-free method to make a fishing hole in natural lake ice
- P17: Six misleading signs of safe ice, with corrections
- P18: Emergency desk-reference: witnesses, immersion, self-rescue, cold-exposure care

## Content boundaries
- None of the pages grant ice-travel clearance. Minnesota DNR states no ice is completely safe. Its 4-in minimum is limited to new, clear ice and is NOT a guarantee.
- Real photographs documenting ice conditions have not been acquired. The new SVG assets are labeled original schematics; they must not be misrepresented as photographs or field observations.
- Specialist review by ice-rescue personnel and qualified medical reviewers is required before public or field use. Check fishery rules at time of use.
- No production data was touched, no Git repository was modified, and no publication or deployment was performed.

Sources: Minnesota DNR ice safety, thickness, measurement, formation and current angling regulations; NWS winter safety. See source CSV for direct URLs and claim ledger for attribution. Research as of 2026-11-22.
'''
(ROOT/'B013_stage3_README.md').write_text(readme,encoding='utf-8')
qa='''# B013 Stage 3 – QA & publication gate

## Automated checks (performed by build)
- [x] Preserve the original 14-page file by writing a new 18-page HTML output.
- [x] Exactly 18 page IDs and 18 navigation entries.
- [x] Self-contained reader; no network requests required for the page.
- [x] Pages 15–18 contain no photographs portrayed as measured conditions.
- [x] Eight original vector safety schematics can be reviewed and edited separately.
- [x] Page 15–18 each includes no-gear-first decisions, checklist, failures, corrections and stop condition.
- [x] Link every new page to at least one primary research source in claim ledger.

## Unmet mandatory gates
- [ ] Independent qualified ice/water rescue reviewer confirms procedures and diagrams.
- [ ] Independent qualified medical reviewer confirms cold-water aftercare guidance.
- [ ] State/regulation reviewer checks fishing restrictions, date-sensitive law and any proposed survival exemptions.
- [ ] Acquire and rights-clear field photographs where real conditions must be recognized.
- [ ] Validation of images against source photography and real equipment.
- [ ] Run accessibility review, responsive layout tests, page printing and manual content check.
- [ ] Obtain owner approval to change any publication or production gate.

**Gate A: BLOCKED. Track B: research/editorial review only.**
'''
(ROOT/'B013_stage3_quality_checks.md').write_text(qa,encoding='utf-8')

# parse and audit
soup=BeautifulSoup(OUT.read_text(encoding='utf-8'),'html.parser')
page_ids=[x.get('id') for x in soup.select('section.page')]
nav=[x.get('value') for x in soup.select('#pages option')]
assert page_ids==['P'+str(i).zfill(2) for i in range(1,19)],page_ids
assert nav==page_ids,nav
assert all(soup.select_one('#'+p['id']+' .new-vector') is not None for p in PAGES)
assert '"P18"' in soup.script.string
assert OUT.stat().st_size>1_200_000
# Create source-preserving ZIP, excluding the original 14-page input
zip_path=ROOT/'B013_Ice_Safety_Stage3_18_Page_Review_Package.zip'
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED,compresslevel=7) as z:
 for f in [OUT,ROOT/'B013_stage3_README.md',ROOT/'B013_stage3_quality_checks.md',ROOT/'B013_stage3_source_register.csv',ROOT/'B013_stage3_claim_ledger.csv',ROOT/'B013_stage3_asset_manifest.csv']+sorted(ASSETS.glob('*.svg')):
  z.write(f,arcname=f.relative_to(ROOT))
print(json.dumps({'status':'created','pages':len(page_ids),'navigation_entries':len(nav),'source_claims':len(CLAIMS),'vector_assets':8,'reader_bytes':OUT.stat().st_size,'zip_bytes':zip_path.stat().st_size,'reader':str(OUT),'package':str(zip_path)},indent=2))
