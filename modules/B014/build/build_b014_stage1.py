#!/usr/bin/env python3
"""Build B014 P11-P20 stand-alone editorial reader and original diagrams.
No external assets, no real-world route claims, and no release approval implied.
"""
from __future__ import annotations
from pathlib import Path
import base64, csv, hashlib, html, json, re, zipfile
from xml.etree import ElementTree as ET

ROOT=Path(__file__).resolve().parent
DEST=ROOT/'B014_stage1'
SVG_DIR=DEST/'svg'
SVG_DIR.mkdir(parents=True,exist_ok=True)

SOURCES={
'NPS-PLAN':('National Park Service — Outdoor Emergency Plan','https://www.nps.gov/articles/gtgemergencyplan.htm'),
'NPS-WINTER':('National Park Service — Winter Hiking Tips','https://home.nps.gov/articles/000/winterhikingtips.htm'),
'DNR-FOREST':('Minnesota DNR — Safety in State Forests','https://www.dnr.state.mn.us/state-forests/safety.html'),
'DNR-HIKE':('Minnesota DNR — Hiking Safety Tips','https://www.dnr.state.mn.us/hiking/safety.html'),
'DNR-ICE':('Minnesota DNR — Ice Safety','https://www.dnr.state.mn.us/safety/ice/index.html'),
'NWS-WINTER':('NWS Twin Cities — Watch, Warning and Advisory Criteria','https://www.weather.gov/mpx/wwa_criteria'),
'NWS-COLD':('National Weather Service — During Extremely Cold Weather','https://www.weather.gov/safety/cold-during'),
'USGS-MAP':('USGS — US Topo Map Symbol Guide','https://www.usgs.gov/ngp-standards-and-specifications/us-topo-map-symbol-guide'),
'NOAA-DECL':('NOAA NCEI — Magnetic Declination','https://www.ncei.noaa.gov/products/magnetic-declination')
}

PAGES=[
 dict(id='P11',title='WHEN WHITEOUT ERASES THE TRAIL',subtitle='Visibility failure is a stop signal, not a navigation challenge.',eyebrow='SNOWSTORM / LOST-ROUTE DECISION',scene='A familiar track disappears as wind and falling snow remove your reference points.',
 steps=[('STOP','Stop moving. Gather everyone and name the last verified place.'),('ASSESS','Check for immediate hazards: exposure, falling branches, unstable banks or traffic.'),('VERIFY','Retrace only when you can identify the route with reliable evidence and it remains safe.'),('SHELTER + SIGNAL','If you cannot verify a safe route, remain near a safe location, protect yourself from weather and seek rescue.')],
 no_gear='On stable ground, reduce wind exposure, keep the group together and make your location obvious to searchers.',
 improvised='Use a bright garment for visibility; insulate yourself from snow using safe dry material.',
 equipped='Use an offline map, GPS coordinates, whistle or emergency communicator to contact responders.',
 checks=['Can you name and verify the last known location?','Is retracing safer than remaining and sheltering?','Is the group protected from wind and wet snow?'],
 faults=[('Follow faint tracks','Tracks may be unrelated or erased; use verified landmarks.'),('Keep walking to stay warm','Uncertain travel risks disorientation and exhaustion.')],
 stop='No confirmed route, worsening visibility or exposure: stop discretionary travel and seek help. Move only as needed to escape an immediate threat.',sources=['NPS-PLAN','NPS-WINTER','NWS-WINTER']),
 dict(id='P12',title='THE WATER BARRIER IS NOT A SHORTCUT',subtitle='A lake, river, beaver pond or bog can interrupt a planned route.',eyebrow='CONCEPTUAL MAP / WATER + WETLANDS',scene='Your remembered trail appears to lead toward a frozen lake and an unmarked marsh.',
 steps=[('STOP SHORT','Observe from stable ground, away from unstable banks and shore ice.'),('READ TERRAIN','Use known map features and visible landmarks to identify water and wetland boundaries.'),('REJECT RISK','Do not cross uncertain ice, flooded ground or bog to shorten a route.'),('DECIDE','Choose only a verified safe land detour. Otherwise stay in a safe place and request help.')],
 no_gear='Remain on stable ground; do not test ice strength or mud depth with your body.',
 improvised='Mark your own safe stationary location with visible materials. Do not build unverified bridges or rafts.',
 equipped='Use current topographic maps and an official trail route; verify them against actual terrain.',
 checks=['Is the route an authorized land route, not a water crossing?','Are shoreline and bank conditions observed from safe ground?','Does the map match the actual landmarks?'],
 faults=[('White surface looks walkable','Snow can conceal weak ice and open water.'),('A blue patch is easy to detour','Wetlands may be larger or less passable than a schematic suggests.')],
 stop='Unknown ice, deep mud, moving water, unstable shoreline or no verified detour: do not enter.',sources=['DNR-ICE','DNR-FOREST','USGS-MAP']),
 dict(id='P13',title='NATURE DOES NOT GIVE A SAFE BEARING',subtitle='Single environmental clues are not dependable navigation instruments.',eyebrow='NO-COMPASS ORIENTATION / LIMITS',scene='You have no compass or charged device and are tempted to use moss or one tree as a north arrow.',
 steps=[('ADMIT UNCERTAINTY','Do not convert a visual hint into a precise direction.'),('RECONSTRUCT','Recall the last verified trail, signed junction or distinctive landmark.'),('CROSS-CHECK','Confirm multiple independent features; do not trust one shadow, stream or tree.'),('STOP IF UNSURE','If you cannot safely identify your route, stop searching, seek shelter and signal.')],
 no_gear='A stationary safe location is better than walking a guessed heading in dense woods.',
 improvised='Use a visible note or markers only to describe your current location for rescuers, not to invent a route.',
 equipped='Use a reliable map and compass only if you can interpret the map and verify the surrounding terrain.',
 checks=['Can you identify an actual route feature?','Are any directional clues independently verified?','Would movement increase distance from your last known point?'],
 faults=[('Moss faces north','Moss growth depends on local moisture, shade and substrate.'),('Streams lead to people','A stream can lead into swamps, rapids or more remote terrain.')],
 stop='No verified direction and no immediate need to relocate: stay in a safe place and seek rescue.',sources=['NPS-PLAN','DNR-FOREST']),
 dict(id='P14',title='TWO NORTHS, ONE UNVERIFIED NUMBER',subtitle='A compass reading and map bearing can differ because of magnetic declination.',eyebrow='COMPASS / TRUE NORTH / DECLINATION',scene='A compass needle aligns to local magnetic north while the map uses geographic north.',
 steps=[('IDENTIFY NORTH','Read the map legend and the compass reference before taking a bearing.'),('LOOK UP','Obtain the magnetic declination for that location and date from a verified source.'),('CHECK METHOD','Use the compass manufacturer’s procedure to convert map and magnetic bearings.'),('GROUND-TRUTH','Confirm the intended path against reliable terrain features before moving.')],
 no_gear='Without a reliable direction, do not guess a compass-equivalent heading.',
 improvised='Write down the last known position and reference points. Improvised magnetic needles are not a reliable emergency substitute.',
 equipped='Use an appropriate map, an understood compass and a current local NOAA declination value.',
 checks=['Is the declination value location- and date-specific?','Are you distinguishing true north and magnetic north?','Do observable features agree with your map?'],
 faults=[('Copy a bearing from an old guide','Declination changes with time and geography.'),('Use one compass reading','Local interference or incorrect technique can mislead.')],
 stop='Unknown declination, unverified map orientation or inconsistent features: do not follow a calculated bearing.',sources=['NOAA-DECL','USGS-MAP','DNR-FOREST']),
 dict(id='P15',title='WHEN THE PHONE STOPS HELPING',subtitle='Offline data, GPS reception, cellular service and battery power are separate dependencies.',eyebrow='PHONE GPS / MAP / BATTERY',scene='The phone shows low battery, a stale map or no service under heavy forest canopy.',
 steps=[('CHECK LOCATION','See whether a trustworthy current position and an already-downloaded map are available.'),('VERIFY MAP','Compare the display against known junctions and visible features; a dot is not a safe route.'),('CONTACT HELP','If connected, call 911 or use a supported emergency feature and provide your position.'),('CONSERVE','Keep the phone protected from cold, minimize nonessential activity and avoid random travel.')],
 no_gear='If the device is unusable, return to the last verified location decision: stop, shelter and signal.',
 improvised='Protect the phone against moisture and excessive cold using existing dry layers without hiding it from needed signals.',
 equipped='Bring downloaded offline maps, a fully charged power bank, a paper map and an independent emergency communicator.',
 checks=['Does the map data actually exist offline?','Is the position current and consistent with landmarks?','Can you communicate without relying on a map app?'],
 faults=[('No bars means no location','Position and map availability are separate from cellular data service.'),('The blue dot proves trail access','A position estimate does not prove a route is passable.')],
 stop='Missing map, uncertain fix or critically low power: do not navigate on an unverified display.',sources=['NPS-PLAN','NPS-WINTER','DNR-HIKE']),
 dict(id='P16',title='MAKE YOUR POSITION FINDABLE',subtitle='Searchers cannot always see someone beneath dense forest canopy.',eyebrow='SIGNALING / FOREST CANOPY',scene='You are safe enough to remain in place, but the forest conceals you from a road or aircraft.',
 steps=[('CALL','Use 911 or an emergency communicator if available; report your location and last known route.'),('SIGNAL','Use a whistle, visible clothing or a light from stable ground.'),('STAY TOGETHER','Keep the group at the reported location unless a life threat requires movement.'),('REPEAT CAREFULLY','Signal when responders are near; conserve battery and energy while awaiting help.')],
 no_gear='Use your voice, bright clothing or deliberate movement that does not put you in danger.',
 improvised='Arrange contrasting materials on safe open ground without damaging the environment.',
 equipped='Use a whistle, signaling mirror, light or personal locator beacon as appropriate.',
 checks=['Can a dispatcher describe your actual position?','Does a signal risk pushing someone onto water, roads or unstable ground?','Can the group remain together and visible?'],
 faults=[('Run toward every sound','Unknown direction can disperse the group.'),('Build a signal fire anywhere','Fire can cause wildfire or injury; avoid without safe legal conditions and skill.')],
 stop='Do not travel toward distant voices or aircraft unless responders give a safe, verified instruction.',sources=['NPS-PLAN','DNR-HIKE']),
 dict(id='P17',title='IF A CHILD OR PARTNER DISAPPEARS',subtitle='The lost person and the searching group need different actions.',eyebrow='GROUP ACCOUNTABILITY / HUG-A-TREE',scene='At a trail junction, someone discovers a child or hiking partner is missing.',
 steps=[('STOP THE GROUP','Keep everyone else together and account for all members.'),('VERIFY LAST SEEN','Identify the last confirmed location and time; avoid speculative trail splitting.'),('CONTACT RESPONDERS','Call 911 promptly with clothing, last-known location, area and medical concerns.'),('HOLD / FOLLOW','Follow official directions; do not scatter into the woods for an improvised search.')],
 no_gear='For a lost child: remain in one safe place near a tree or clear landmark, keep warm and respond to searchers.',
 improvised='A child may use bright clothing and a loud voice to signal without wandering.',
 equipped='Adults use a phone, whistle, map, group roster and written last-seen details for responders.',
 checks=['Is every remaining person accounted for?','Do searchers have the correct last-known point?','Are the child instructions distinct from adult search tasks?'],
 faults=[('Everybody fans out','An uncoordinated search can create more missing people.'),('A child walks toward random voices','A child should stay in a safe place and make themself visible.')],
 stop='Missing person and uncertain direction: contact authorities early. Avoid off-trail self-directed searches.',sources=['NPS-PLAN','DNR-HIKE']),
 dict(id='P18',title='THE LAST LIGHT DECISION',subtitle='Daylight and weather may run out before an uncertain detour ends.',eyebrow='OVERNIGHT / EXPOSURE CHOICE',scene='The trail is unclear and visibility is decreasing before nightfall.',
 steps=[('ASSESS TIME','Estimate remaining usable daylight without assuming a known sunset time.'),('COMPARE HAZARDS','Check whether travel or staying exposes you to greater immediate danger.'),('PROTECT','Choose safer stable ground, block wind and preserve dry insulation.'),('SIGNAL + WAIT','Notify responders when possible; remain findable and monitor everyone for cold stress.')],
 no_gear='Stay out of wind and wet terrain. Avoid unnecessary exertion that increases sweat and heat loss.',
 improvised='Use safe natural shelter features and dry materials for wind protection and insulation from the ground.',
 equipped='Use a planned emergency shelter, dry layers, headlamp, food/water and an emergency communicator.',
 checks=['Is remaining in place protected from wind and wet ground?','Is anyone wet, confused, unusually sleepy or unable to walk safely?','Are responders aware of the likely overnight situation?'],
 faults=[('Push on until dark','Navigating uncertain obstacles without light compounds risk.'),('Sweat heavily to stay warm','Wet clothing increases cold exposure risk.')],
 stop='When darkness, uncertain route or cold injury changes the risk, stop discretionary travel and seek emergency help.',sources=['DNR-FOREST','DNR-HIKE','NWS-COLD','NPS-PLAN']),
 dict(id='P19',title='SIX WAYS A GOOD-LOOKING ROUTE FAILS',subtitle='Use the failure atlas to recognize false confidence before moving.',eyebrow='NAVIGATION FAILURE / CORRECTION ATLAS',scene='A single confident assumption can turn a nearby trail into a dangerous detour.',
 steps=[('NOTICE','Look for a route assumption rather than a measured fact.'),('COMPARE','Check terrain, weather, map and navigation tools independently.'),('CORRECT','Reject unsupported shortcuts and reset to a verified known location.'),('ABORT','If contradictions remain, shelter and contact help rather than continue.')],
 no_gear='Do not improvise a heading from moss, wind or stream flow.',
 improvised='Use simple notes or signs to describe the last known position, not to invent a track.',
 equipped='Use verified map features and a working compass/GPS, cross-checking both.',
 checks=['Do route signs and current terrain agree?','Have conditions made an earlier trail or water crossing unsafe?','Could one tool, clue or memory be wrong?'],
 faults=[('Follow boot tracks','Snow-covered tracks can lead away or vanish.'),('Cross a white lake','Ice can vary and fail without warning.'),('Moss means north','Environmental growth is not a bearing.'),('GPS dot means trail','Coordinates are not passability.'),('Map omits swamp','Map age/scale and change matter.'),('Keep walking to search','Random movement increases search area.')],
 stop='If the navigation evidence is inconsistent, do not guess. Stop in a safe location and request help.',sources=['NPS-PLAN','NPS-WINTER','DNR-ICE','USGS-MAP']),
 dict(id='P20',title='LOST IN WINTER: POCKET ACTION CARD',subtitle='When uncertain, stop discretionary travel and make rescue easier.',eyebrow='TEAR-OUT / NO GEAR FIRST',scene='A concise reference for an unfamiliar North Woods route in snow, wind or fading light.',
 steps=[('STOP','Pause. Gather the group and identify immediate threats.'),('VERIFY','Name the last known place; retrace only if the route is certain and safe.'),('CONTACT','Call 911 when possible; supply last known point, coordinates and landmarks.'),('PROTECT + SIGNAL','If you cannot verify a route, remain findable, block wind and await responders.')],
 no_gear='Stay together. Stay on stable ground. Avoid unknown ice, wetlands and steep banks.',
 improvised='Use bright materials for visibility and dry insulation under the body.',
 equipped='Use map/compass, offline GPS, whistle, emergency communicator and spare warmth.',
 checks=['Immediate hazard addressed?','Last-known place recorded?','911 or rescue contact attempted?','Group warmth and visibility addressed?'],
 faults=[('Guess and keep moving','Stop and reset to the last verified point.'),('Use an ice shortcut','Keep to known safe land routes.')],
 stop='No verified route or immediate cold, water or terrain hazard: stop, shelter and seek rescue.',sources=['NPS-PLAN','DNR-FOREST','DNR-ICE','NPS-WINTER'])
]

# All vectors are conceptual teaching diagrams, with no map, measurement, or safe-route claim.
VHEAD='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 400" role="img" aria-labelledby="title"><title id="title">{title}</title><rect width="760" height="400" rx="16" fill="#f8f7f0"/><rect x="12" y="12" width="736" height="376" rx="12" fill="#eef2e9" stroke="#adc2af" stroke-width="2"/>'
VFOOT='<rect x="22" y="350" width="716" height="30" rx="5" fill="#143e32"/><text x="380" y="371" text-anchor="middle" fill="#fff" font-family="Arial" font-size="13" font-weight="bold">CONCEPTUAL TRAINING DIAGRAM · NOT A REAL ROUTE OR SAFE-ICE ASSESSMENT</text></svg>'

def T(x,y,s,size=18,color='#163c2e',weight='normal',anchor='start'):
 return f'<text x="{x}" y="{y}" fill="{color}" font-family="Arial,sans-serif" font-weight="{weight}" text-anchor="{anchor}" font-size="{size}">{html.escape(s)}</text>'

def rect(x,y,w,h,fill='#e6efdf',stroke='#a3baab',rx=8):
 return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'

def arrow(x1,y1,x2,y2,stroke='#bf753b',width=5):
 return f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{stroke}" stroke-width="{width}" fill="none" stroke-linecap="round"/><path d="M{x2-9} {y2-7} L{x2} {y2} L{x2-9} {y2+7}" stroke="{stroke}" stroke-width="{width-1}" fill="none" stroke-linejoin="round"/>'

def forest():
 s=''
 for x,y in [(90,90),(144,70),(205,105),(603,85),(677,100),(118,250),(641,255),(694,246)]:
  s+=f'<path d="M{x} {y-27} l-27 65 h54 z" fill="#628773" stroke="#416b55"/><rect x="{x-4}" y="{y+34}" width="8" height="17" fill="#816e50"/>'
 return s

def fig_svg(page):
 n=int(page['id'][1:]); s=VHEAD.format(title=html.escape(page['title']))
 s+=T(36,50,page['eyebrow'],22,'#153e32','bold')
 if n in (11,20):
  labels=['STOP','VERIFY','CONTACT','PROTECT + SIGNAL']
  for i,label in enumerate(labels):
   x=45+i*177;s+=rect(x,120,160,125,'#fffaf1' if i%2 else '#e0ecdf')+T(x+80,163,str(i+1),27,'#9a532c','bold','middle')+T(x+80,193,label,17,'#1a4433','bold','middle')
   if i<3:s+=arrow(x+160,182,x+174,182)
  s+=T(380,285,'Unknown route + no immediate threat → remain in a safe place',19,'#883d2e','bold','middle')
 elif n==12:
  s+=rect(38,75,680,262,'#e3eddd')
  s+='<path d="M375 85 C510 70 515 156 599 179 C650 216 575 321 446 300 C324 303 296 226 338 153Z" fill="#a3cee0" stroke="#477e9a" stroke-width="3"/>'
  s+='<path d="M48 225 C150 205 185 120 303 195 Q322 210 343 214" stroke="#ac8e65" stroke-width="16" fill="none" stroke-dasharray="12 12"/>'
  s+=forest()+T(490,166,'LAKE / ICE',21,'#244b64','bold','middle')+T(175,105,'KNOWN LAND',18,'#1d4936','bold','middle')+T(192,274,'TRAIL STOPS',17,'#883d2e','bold','middle')
  s+='<path d="M330 180 L382 236 M382 180 L330 236" stroke="#a93a32" stroke-width="12"/>'
  s+=T(557,322,'NO CROSSING',22,'#9b3d30','bold','middle')
 elif n==13:
  for i,(name,label) in enumerate([('MOSS','not a compass'),('STREAM','not a highway'),('SHADOW','one clue is weak')]):
   x=42+235*i;s+=rect(x,108,213,134,'#fffaf1')+T(x+106,156,name,22,'#264938','bold','middle')+T(x+106,192,label,17,'#9b4033','bold','middle')
  s+=T(380,294,'Safe default: verified landmark or stop + signal',21,'#163e32','bold','middle')
 elif n==14:
  s+='<circle cx="282" cy="219" r="120" fill="#fbfcf8" stroke="#658a77" stroke-width="4"/>'
  s+='<line x1="282" y1="219" x2="282" y2="101" stroke="#2d765b" stroke-width="8"/>'
  s+='<line x1="282" y1="219" x2="349" y2="128" stroke="#b76935" stroke-width="8"/>'
  s+=T(272,92,'TRUE N',19,'#236a50','bold','middle')+T(398,122,'MAGNETIC N',17,'#9d532e','bold','middle')
  s+=T(520,179,'DECLINATION',25,'#1b4739','bold','middle')+T(520,213,'Varies by place',19,'#24483a','normal','middle')+T(520,241,'and date',19,'#24483a','normal','middle')+T(380,321,'No angle or bearing is specified in this schematic',15,'#913e35','bold','middle')
 elif n==15:
  for i,(name,sub) in enumerate([('POSITION','GPS fix'),('MAP','downloaded data'),('SIGNAL','mobile / SOS')]):
   x=45+i*238;s+=rect(x,102,214,143,'#fdfcf7')+T(x+107,156,name,22,'#25513d','bold','middle')+T(x+107,190,sub,16,'#566c5e','normal','middle')
  s+=T(380,298,'These are three different dependencies',22,'#9a4737','bold','middle')
 elif n==16:
  s+=forest()+T(379,111,'FOREST CANOPY',20,'#23533f','bold','middle')
  s+=rect(250,178,264,74,'#fffaf2')+T(382,209,'SAFE BASE POINT',20,'#1d513d','bold','middle')+T(382,234,'report + signal',17,'#557163','normal','middle')
  s+=arrow(382,176,382,125,'#ba792d')+T(382,310,'Visibility is limited; do not wander toward sounds',17,'#9b3e32','bold','middle')
 elif n==17:
  s+=rect(40,105,308,175,'#e0eddf')+T(194,142,'SEARCH PARTY',22,'#185039','bold','middle')+T(194,181,'stay together',19,'#1f503c','normal','middle')+T(194,210,'call 911',19,'#1f503c','normal','middle')
  s+=rect(413,105,306,175,'#fff5db')+T(565,142,'LOST CHILD',22,'#81532a','bold','middle')+T(565,181,'Hug a Tree',19,'#7e572c','normal','middle')+T(565,210,'stay + signal',19,'#7e572c','normal','middle')
  s+=T(382,315,'Do not spread the group into an uncoordinated search',19,'#963f32','bold','middle')
 elif n==18:
  s+=rect(45,110,670,170,'#fdfbf5')
  s+='<path d="M70 182 H688" stroke="#b8ad86" stroke-width="8"/>'
  for x,col,label in [(115,'#4e8b68','KNOWN LIGHT'),(367,'#d19e57','FADING'),(620,'#8f665a','DARK')]:
   s+=f'<circle cx="{x}" cy="182" r="18" fill="{col}"/>'+T(x,152,label,17,'#274735','bold','middle')
  s+=T(381,239,'Do not begin an uncertain detour as light fades',20,'#9b3d31','bold','middle')
 elif n==19:
  labels=[('TRAIL PRINTS','not route proof'),('WHITE LAKE','not safe ice'),('MOSS','not north'),('GPS DOT','not passability'),('OLD MAP','not real-time'),('RANDOM WALK','not a search plan')]
  for i,(name,sub) in enumerate(labels):
   x=40+(i%3)*234;y=98+(i//3)*119;s+=rect(x,y,214,102,'#fffaf1')+T(x+107,y+37,name,18,'#274b3a','bold','middle')+T(x+107,y+67,sub,16,'#9e4436','normal','middle')
 s+=VFOOT
 ET.fromstring(s)
 return s

# Original figures
visual_rows=[]
for p in PAGES:
 svg=fig_svg(p)
 out=SVG_DIR/(p['id']+'_conceptual.svg');out.write_text(svg,encoding='utf-8')
 visual_rows.append({'page':p['id'],'file':out.name,'type':'editable original SVG','classification':'conceptual non-geographic illustration','rights':'original source created for this project','real_world_navigation':'NO','sha256':hashlib.sha256(out.read_bytes()).hexdigest()})

STYLE='''
:root{--pine:#143d31;--deep:#0d3026;--cream:#f8f5e9;--ink:#23392e;--mid:#5c6e62;--rust:#953c32;--gold:#c39154;--line:#c8d2c8}
*{box-sizing:border-box}body{margin:0;background:#e9ede7;color:var(--ink);font-family:system-ui,-apple-system,Segoe UI,sans-serif;line-height:1.45}header{background:var(--pine);color:white;padding:16px 22px;display:flex;justify-content:space-between;align-items:center}header small{display:block;opacity:.77}.wrap{max-width:1100px;margin:auto;padding:16px}.toolbar{display:flex;flex-wrap:wrap;gap:8px;align-items:center;background:white;padding:13px 14px;border-radius:9px;margin:8px 0 14px}.toolbar button,.toolbar select{border:1px solid #9caf9e;background:#fff;font:inherit;padding:8px;border-radius:6px;cursor:pointer}.toolbar button:hover{background:#e1ecdf}.toolbar select{max-width:100%;min-width:0;flex:1 1 200px}.notice{background:#fff6e9;color:#713d2a;padding:10px 14px;border-left:5px solid #b66d43;margin:10px 0 14px}.page{display:none}.page.active{display:block}.sheet{background:#fffef9;padding:25px 29px 24px;box-shadow:0 8px 23px #19372822;border-radius:9px;max-width:1000px;margin:0 auto 22px}.eyebrow{color:#607b63;font-size:12px;font-weight:800;letter-spacing:.12em}.sheet h1{font-size:33px;line-height:1.05;margin:6px 0}.sub{font-size:17px;color:var(--mid);margin:0 0 12px}.layout{display:grid;grid-template-columns:47% 1fr;gap:18px}.art{background:#eaf0e6;border:1px solid #c4d3c4;padding:7px;border-radius:8px}.art img{width:100%;height:auto;display:block}.scenario{font-size:14px;padding:9px 13px;background:#f4f6ef;border-left:4px solid #8cae94}.sectionhead{font-size:14px;font-weight:800;text-transform:uppercase;letter-spacing:.05em;margin:14px 0 8px;color:var(--pine)}.steps{counter-reset:step;list-style:none;padding:0;margin:0}.steps li{padding:8px 9px 8px 42px;position:relative;border-bottom:1px solid #e3e9df;font-size:14px}.steps li:before{counter-increment:step;content:counter(step);position:absolute;left:0;top:10px;width:26px;height:26px;border-radius:50%;background:#e5eee2;color:#234a32;text-align:center;line-height:26px;font-weight:800}.tiers{display:grid;grid-template-columns:1fr;gap:7px;margin:11px 0}.tier{background:#f5f7f1;border:1px solid #dce4da;padding:7px 9px;border-radius:5px;font-size:13px}.tier strong{color:#1e503b}.bottom{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:12px}.bottom section{background:#f5f7f1;padding:11px 12px;border-radius:6px}.bottom h2{font-size:13px;text-transform:uppercase;letter-spacing:.07em;margin:0 0 7px}.bottom ul{font-size:13px;padding-left:19px;margin:4px}.fault{font-size:13px;padding:6px 0;border-top:1px solid #d8e0d6}.fault b{color:#9a3e33}.stop{background:#f9eeea;border-left:5px solid var(--rust);padding:9px 12px;margin-top:10px;font-size:14px}.foot{display:flex;justify-content:space-between;align-items:center;color:#61746a;font-size:11px;border-top:1px solid #d6e0d5;padding-top:8px;margin-top:10px}@media(max-width:720px){.layout,.bottom{grid-template-columns:1fr}.sheet{padding:15px}.sheet h1{font-size:27px}header{display:block}}@media print{body{background:white}.toolbar,header,.notice{display:none!important}.wrap{max-width:none;padding:0}.page{display:block!important;break-after:page}.sheet{box-shadow:none;page-break-inside:avoid;max-width:none;margin:0;padding:10px}.layout{grid-template-columns:43% 1fr}}
'''

def E(s):return html.escape(s)

def render_page(p):
 figure=base64.b64encode((SVG_DIR/(p['id']+'_conceptual.svg')).read_bytes()).decode('ascii')
 steps=''.join('<li><b>'+E(a)+'</b> — '+E(b)+'</li>' for a,b in p['steps'])
 checks=''.join('<li>'+E(x)+'</li>' for x in p['checks'])
 faults=''.join('<div class="fault"><b>'+E(a)+'</b> → '+E(b)+'</div>' for a,b in p['faults'])
 tiers=''.join('<div class="tier"><strong>'+a+'</strong> '+E(p[k])+'</div>' for a,k in [('NO GEAR:','no_gear'),('IMPROVISED:','improvised'),('EQUIPPED:','equipped')])
 return f'''<section class="page" id="{p['id']}"><article class="sheet"><div class="eyebrow">B014 · NORTH WOODS NAVIGATION · {p['id']} · {E(p['eyebrow'])}</div><h1>{E(p['title'])}</h1><p class="sub">{E(p['subtitle'])}</p><div class="layout"><div><div class="art"><img src="data:image/svg+xml;base64,{figure}" alt="{E(p['id'])} original conceptual safety diagram, not a real route"/></div><div class="scenario"><b>SCENARIO</b> · {E(p['scene'])}</div><div class="sectionhead">Options from least equipment</div><div class="tiers">{tiers}</div></div><div><div class="sectionhead">Four-action sequence</div><ol class="steps">{steps}</ol></div></div><div class="bottom"><section><h2>Check before continuing</h2><ul>{checks}</ul></section><section><h2>Wrong signal → correction</h2>{faults}</section></div><div class="stop"><b>STOP / ABORT CONDITION:</b> {E(p['stop'])}</div><div class="foot"><span>Conceptual editorial draft · source/review ledger external to reader · not field tested</span><span>{p['id']} · B014 Track B</span></div></article></section>'''

options=''.join('<option value="'+p['id']+'">'+p['id']+' · '+E(p['title'])+'</option>' for p in PAGES)
html_file=DEST/'B014_P11_P20_Standalone_Reader_REVIEW.html'
html_content='''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>B014 North Woods Navigation · P11–P20 Supplemental Reader</title><style>'''+STYLE+'''</style></head><body><header><div><strong>SURVIVAL FIELD ENCYCLOPEDIA</strong><small>B014 North Woods navigation · editorial supplement P11–P20</small></div><span>10 ORIGINAL RESEARCH-BASED DRAFT PAGES</span></header><div class="wrap"><nav class="toolbar" aria-label="Page navigation"><label for="chooser"><b>Page</b></label><select id="chooser" aria-label="Choose reader page">'''+options+'''</select><button id="previous" type="button">Previous</button><button id="following" type="button">Next</button><span id="counter" role="status"></span></nav><aside class="notice">DRAFT / NOT APPROVED FOR FIELD USE. P11–P20 are a supplemental manuscript, not a complete B014 chapter. Original P01–P10 files must be reconciled. Diagrams are conceptual. No actual safe route, compass bearing or verified field photograph is represented.</aside>'''+''.join(render_page(p) for p in PAGES)+'''</div><script>
(function(){const ids=['P11','P12','P13','P14','P15','P16','P17','P18','P19','P20'];const chooser=document.getElementById('chooser');let i=Math.max(0,ids.indexOf(location.hash.substring(1).toUpperCase()));function render(){for(const id of ids){const node=document.getElementById(id);node.classList.toggle('active',id===ids[i]);}chooser.value=ids[i];document.getElementById('counter').textContent=(i+1)+' / '+ids.length;history.replaceState(null,'','#'+ids[i]);}function go(delta){i=Math.min(ids.length-1,Math.max(0,i+delta));render();}document.getElementById('previous').addEventListener('click',()=>go(-1));document.getElementById('following').addEventListener('click',()=>go(1));chooser.addEventListener('change',()=>{i=ids.indexOf(chooser.value);render();});window.addEventListener('hashchange',()=>{const j=ids.indexOf(location.hash.substring(1).toUpperCase());if(j>=0){i=j;render();}});document.addEventListener('keydown',e=>{if(e.key==='ArrowRight')go(1);if(e.key==='ArrowLeft')go(-1);});render();})();
</script></body></html>'''
html_file.write_text(html_content,encoding='utf-8')

claims=[]
for p in PAGES:
 for j,src in enumerate(p['sources'],1):
  claims.append({'page':p['id'],'claim_id':f"{p['id']}-S{j:02}",'editorial_claim_or_coverage':p['subtitle']+' / '+p['steps'][0][1],'source_id':src,'source_url':SOURCES[src][1],'source_status':'Official source checked 2026-11-22; specific illustration requires editorial review','publication_gate':'BLOCKED / SME review'})

def csvout(name,rows):
 with (DEST/name).open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

csvout('B014_stage1_claim_source_ledger.csv',claims)
csvout('B014_stage1_visual_manifest.csv',visual_rows)
(DEST/'B014_stage1_references.json').write_text(json.dumps({k:{'title':v[0],'url':v[1]} for k,v in SOURCES.items()},indent=2)+'\n',encoding='utf-8')
(DEST/'README.md').write_text('''# B014 North Woods Navigation · P11–P20 editorial reader

**Status: TRACK B EDITORIAL DRAFT ONLY. Gate A BLOCKED.**

A standalone ten-page, offline-read HTML reader, with ten individually editable conceptual SVG illustrations, a page-to-source ledger, and a visual provenance manifest. It is an extension manuscript only: B014 P01–P10 have **not** been recovered/verified in this workspace, so do not merge these pages over existing B014 content.

## Use

Open `B014_P11_P20_Standalone_Reader_REVIEW.html` in an offline browser. Navigation uses its page selector, keyboard arrows, or previous/next. Printing exposes all ten pages. `svg/` contains editable originals; HTML embeds their content for offline portability. Build from the root project using `python build_b014_stage1.py`.

## Release blockers

1. Recover original B014 P01–P10, map sections and reconcile page numbering and content.
2. Obtain authentic and rights-cleared topo/map photography where a real source is needed.
3. Subject-matter expert review for lost-person decisions, navigation and winter exposure.
4. Independent proofread, browser/accessibility/print QA, author approval.
5. Never present conceptual diagrams as actual routes, measured compass angles, real ice conditions or authoritative safety clearance.

Source register and provenance remain separate from the reader. All illustrations here are original, not copied from a book or map.
''',encoding='utf-8')

assert len(re.findall(r'class="page" id="P\d\d"',html_content))==10
assert len(re.findall(r'<option value="P\d\d"',html_content))==10
assert all(html_content.count(f'id="{p["id"]}"')>=1 for p in PAGES)
assert 'https://' not in html_content and 'http://' not in html_content
for p in PAGES:
 assert len(p['steps'])==4 and p['stop'] and p['sources']
 assert (SVG_DIR/(p['id']+'_conceptual.svg')).exists()
 with open(SVG_DIR/(p['id']+'_conceptual.svg'),encoding='utf-8') as f:ET.fromstring(f.read())

with zipfile.ZipFile(DEST/'B014_Stage1_P11_P20_Editorial_Review_Package.zip','w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for f in [html_file,DEST/'README.md',DEST/'B014_stage1_claim_source_ledger.csv',DEST/'B014_stage1_visual_manifest.csv',DEST/'B014_stage1_references.json',*sorted(SVG_DIR.glob('*.svg'))]:
  z.write(f,f.relative_to(DEST))

with zipfile.ZipFile(DEST/'B014_Stage1_P11_P20_Editorial_Review_Package.zip') as z:assert z.testzip() is None

(DEST/'B014_STAGE1_QA.md').write_text('''# B014 Stage 1 editorial verification\n\n- [x] Ten unique P11–P20 pages exist in standalone reader.\n- [x] Each page has 4 sequential decisions, no-gear, improvised, equipped tiers, check cues, fault/correction and abort condition.\n- [x] Ten original conceptual SVG diagrams parse as valid XML.\n- [x] All SVGs embedded into a single offline HTML reader; no HTTP requests in HTML.\n- [x] Source/claim ledger, visual/rights manifest and README generated.\n- [x] ZIP archive CRC integrity check passed.\n- [ ] Original B014 P01–P10 reconciled.\n- [ ] Qualified navigation / rescue / cold-weather reviewer.\n- [ ] Real diagnostic imagery and map rights review.\n- [ ] Interactive browser and responsive/print inspection.\n- [ ] Explicit owner release approval.\n\n**No publication or field clearance implied.**\n''')
print(json.dumps({'pages':len(PAGES),'svg':len(visual_rows),'claims_source_links':len(claims),'html_bytes':html_file.stat().st_size,'package_bytes':(DEST/'B014_Stage1_P11_P20_Editorial_Review_Package.zip').stat().st_size,'output':str(DEST)},indent=2))
