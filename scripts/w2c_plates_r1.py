"""Wave 2C batch W2C-R1: RT01 instruction-surface corrections drawn as plates.

RT01 (draft PR #12) found instructions that a reader could follow from the figure alone
in a harmful order or with a missing boundary. These plates draw the corrected physical
or procedural relationship:

* Z11-P63  the call comes first and leads with location; the six-item report is prepared
           ahead and completed while help is on the way (RT01-01);
* Z04-P51  potable water feeds drinking, oral, food and dish tasks; infant formula keeps its
           own rules; a Do Not Use notice stops all tap contact (RT01-04);
* Z13-P49  the two-bucket toilet beside a soap-and-water handwashing station (RT01-05);
* Z13-P50  the low-water handwashing station, with sanitizer only as a fallback (RT01-05);
* Z11-P32  the A04-accepted V02 boxing plate with the exact-return wording replaced by an
           approximate paced return checked against the map (RT01-08).

Run with --out DIR, --write or --check. --check also runs the label audit.
"""
import argparse
from pathlib import Path

from w2c_svg import FLOW, INK, REVERSE, WATER, WATER_EDGE, Plate, bucket, check, cross, jug

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'foundations/visual/w2c_technical/revised'
V02 = ROOT / 'foundations/visual/v02_technical/revised'
SKIN = '#c99a7b'


def limb(points, width=11, color='#5a6f78'):
    d = 'M' + 'L'.join(f'{x} {y}' for x, y in points)
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"/>'


def phone(x, y, w=13, h=24, screen='#dcecf3'):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="#2f3b40" stroke="{INK}" stroke-width="1.4"/>'
            f'<rect x="{x + 2}" y="{y + 3}" width="{w - 4}" height="{h - 7}" fill="{screen}"/>')


# ---------------------------------------------------------------- Z11-P63
def z11_p63():
    p = Plate('Z11-P63', 'Call at once with your location first; the report card is prepared ahead',
              'Left: a caller kneels beside a person who is unresponsive, breathing abnormally or bleeding severely, '
              'calls at once on a phone and keeps giving care while talking, saying the location first: trail, '
              'landmark or coordinates with their format. Centre: if the call drops, dispatch already has the '
              'location. Right: a six-item report card filled in before the trip (location and last known point, '
              'people and injuries, breathing, bleeding and warmth, access hazards, shelter, water and battery, '
              'stay-put plan and callback number) and completed while help is on the way; it is never a reason to '
              'delay the call. Conceptual, not to scale.')
    p.panel(24, 46, 300, 290, 'ok', '✓ LIFE THREAT: CALL NOW')
    p.panel(338, 46, 232, 290, 'neutral', 'IF THE CALL DROPS')
    p.panel(584, 46, 292, 290, 'ok', '✓ REPORT CARD READY')
    # casualty on the ground and kneeling caller
    p.add('<path d="M40 300H308" stroke="#8a7350" stroke-width="3"/>')
    p.add('<circle cx="62" cy="287" r="10" fill="#7b8b92"/><rect x="76" y="279" width="94" height="18" rx="9" fill="#7b8b92"/>')
    p.add(limb([(214, 258), (192, 297), (238, 297)], 12))                      # thigh, shin on the ground
    p.add(limb([(214, 258), (214, 214)], 16))                                    # torso
    p.add('<circle cx="214" cy="198" r="12" fill="#5a6f78"/>')
    p.add(limb([(210, 222), (186, 252), (160, 278)], 9))                        # hand on the casualty
    p.add(limb([(218, 222), (240, 234), (232, 204)], 9))                        # hand holding the phone
    p.add(phone(226, 184))
    # speech bubble from the phone
    p.add('<path d="M112 86h200a10 10 0 0 1 10 10v54a10 10 0 0 1-10 10h-74l-8 24-8-24H112a10 10 0 0 1-10-10V96a10 10 0 0 1 10-10z" '
          'fill="#ffffff" stroke="#205b68" stroke-width="2"/>')
    p.lines(116, 107, ['Location first:'], 'tiny ok')
    p.lines(116, 128, ['trail, landmark or', 'coordinates + format'], 'tiny')
    p.lines(40, 184, ['unresponsive,', 'abnormal breathing', 'or severe bleeding'], 'tiny')
    p.lines(40, 324, ['keep giving care while you talk'], 'tiny')
    # dropped call: location already with dispatch
    p.add(phone(372, 104, 56, 100))
    for k, h in enumerate((6, 10, 14, 18)):
        p.add(f'<rect x="{384 + k * 8}" y="{136 - h}" width="5" height="{h}" fill="#4c5d55"/>')
    p.add(f'<path d="M380 140L418 112" stroke="{REVERSE}" stroke-width="3"/>')
    p.add('<rect x="388" y="150" width="24" height="9" rx="2" fill="#205b68"/>')
    p.add(f'<path d="M432 152h18l6-8 6 16 6-8h18" fill="none" stroke="{INK}" stroke-width="2.2" stroke-dasharray="5 4"/>')
    p.add('<rect x="488" y="122" width="66" height="50" rx="4" fill="#e8eef0" stroke="#183a30" stroke-width="2"/>'
          '<rect x="512" y="172" width="18" height="10" fill="#7c8c95"/><rect x="500" y="182" width="42" height="5" fill="#7c8c95"/>')
    p.add('<path d="M521 135c-7 0-12 5-12 11 0 8 12 18 12 18s12-10 12-18c0-6-5-11-12-11z" fill="#c4472f"/>'
          '<circle cx="521" cy="146" r="4" fill="#ffffff"/>')
    p.lines(488, 114, ['dispatch'], 'tiny')
    p.add(check(552, 128, 10))
    p.lines(354, 232, ['location given first', 'is already received:', 'dispatch still knows', 'where to send help'],
            'tiny', pitch=21)
    # report card
    p.add('<rect x="600" y="86" width="260" height="176" rx="6" fill="#fffdf4" stroke="#183a30" stroke-width="2"/>')
    rows = ['location, last known point', 'people and injuries', 'breathing, bleeding, warmth',
            'access hazards', 'shelter, water, battery', 'stay-put plan, callback no.']
    for i, row in enumerate(rows):
        y = 110 + i * 26
        p.add(f'<circle cx="618" cy="{y - 5}" r="9" fill="#205b68"/>'
              f'<text x="618" y="{y}" class="tiny inv" text-anchor="middle" font-size="12">{i + 1}</text>')
        p.text(634, y, row, 'tiny')
    p.lines(600, 288, ['filled in before the trip,', 'finished while help comes'], 'tiny')
    p.band('Never hang up until the dispatcher says so; follow their instructions within your training.')
    return p.svg()


# ---------------------------------------------------------------- Z04-P51
def cup(x, y):
    return f'<path d="M{x} {y}h30l-4 34h-22z" fill="#dcecf3" stroke="{INK}" stroke-width="2"/>'


def toothbrush(x, y):
    return (f'<rect x="{x}" y="{y + 26}" width="44" height="7" rx="3" fill="#5f8fa3" stroke="{INK}" stroke-width="1.4"/>'
            + ''.join(f'<rect x="{x + 30 + k * 4}" y="{y + 16}" width="2.6" height="10" fill="#ffffff" stroke="#4c5d55" stroke-width=".8"/>'
                      for k in range(4)))


def produce(x, y):
    return (f'<circle cx="{x + 16}" cy="{y + 22}" r="14" fill="#7fa65a" stroke="{INK}" stroke-width="1.8"/>'
            f'<path d="M{x + 16} {y + 8}q4-8 10-8" fill="none" stroke="#5b4630" stroke-width="2"/>')


def ice_tray(x, y):
    return (f'<rect x="{x}" y="{y + 12}" width="46" height="22" rx="3" fill="#eef5f8" stroke="{INK}" stroke-width="1.8"/>'
            + ''.join(f'<rect x="{x + 4 + k * 14}" y="{y + 16}" width="10" height="14" rx="2" fill="#cfe6ef"/>' for k in range(3)))


def dish(x, y):
    return (f'<ellipse cx="{x + 22}" cy="{y + 26}" rx="22" ry="8" fill="#ffffff" stroke="{INK}" stroke-width="1.8"/>'
            f'<ellipse cx="{x + 22}" cy="{y + 25}" rx="12" ry="4" fill="none" stroke="#9aa59c" stroke-width="1.4"/>')


def bandage(x, y):
    return (f'<rect x="{x}" y="{y + 16}" width="44" height="16" rx="8" fill="#e7c9a9" stroke="{INK}" stroke-width="1.6"/>'
            f'<rect x="{x + 15}" y="{y + 18}" width="14" height="12" fill="#f6efe2"/>')


def z04_p51():
    p = Plate('Z04-P51', 'Safe water for each household task, with infant formula kept separate',
              'Left: water that is bottled or boiled and cooled feeds drinking, tooth brushing, washing produce, making '
              'ice and washing dishes; wounds are rinsed only with clean potable water or sterile saline. Upper right: '
              'infant formula follows its own rules. Ready-to-feed formula is safest, especially for infants under 2 '
              'months, born prematurely or with a weakened immune system. Powdered formula is not sterile, so safe '
              'water alone does not make it safe; follow current CDC directions for the infant. Under a chemical '
              'advisory, boiling does not help: use bottled water or ready-to-feed. Lower right: a Do Not Use notice '
              'means no tap contact at all. Conceptual, not to scale.')
    p.panel(24, 46, 410, 290, 'ok', '✓ POTABLE WATER ONLY')
    p.panel(448, 46, 428, 200, 'neutral', 'INFANT FORMULA: ITS OWN RULES')
    p.panel(448, 254, 428, 82, 'bad', '✕ DO NOT USE NOTICE')
    p.add(jug(44, 110, 92, 'SAFE'))
    p.lines(36, 226, ['bottled, or', 'boiled and', 'cooled'], 'tiny')
    p.add(f'<path d="M104 160H140" stroke="{FLOW}" stroke-width="4"/><path d="M140 112V268" stroke="{FLOW}" stroke-width="4"/>')
    tasks = [(cup, 'drinking', 108), (toothbrush, 'teeth', 108), (produce, 'produce', 108),
             (ice_tray, 'ice', 200), (dish, 'dishes', 200)]
    xs = [168, 254, 344, 168, 254]
    for (icon, label, y), x in zip(tasks, xs):
        p.add(icon(x, y - 20))
        p.lines(x, y + 38, [label], 'tiny')
    for y in (112, 204):
        p.arrow(f'M140 {y}H158', 'flow', 3)
    p.add(bandage(168, 244))
    p.arrow('M140 268H160', 'flow', 3)
    p.lines(222, 264, ['wounds: clean potable', 'water or sterile saline'], 'tiny')
    p.lines(40, 306, ['never stream, flood or advisory tap water', 'for any of these tasks'], 'tiny warn')
    # infant formula
    p.add('<rect x="468" y="84" width="36" height="58" rx="4" fill="#f4f1e6" stroke="#183a30" stroke-width="2"/>'
          '<path d="M468 96l18-12 18 12" fill="#f4f1e6" stroke="#183a30" stroke-width="2"/>'
          '<rect x="474" y="108" width="24" height="16" fill="#9cc3cf"/>')
    p.add(check(504, 90, 10))
    p.lines(522, 104, ['ready-to-feed: safest, especially', 'under 2 months, premature or weak immunity'], 'tiny')
    p.add('<rect x="466" y="158" width="40" height="38" rx="5" fill="#d9c7a3" stroke="#183a30" stroke-width="2"/>'
          '<rect x="466" y="152" width="40" height="9" rx="3" fill="#8a7350" stroke="#183a30" stroke-width="1.6"/>')
    p.lines(522, 166, ['powder is not sterile: safe water alone is', 'not enough; follow CDC steps (Z14-P74)'], 'tiny')
    p.add('<path d="M486 210l14 24h-28z" fill="#f2c94c" stroke="#183a30" stroke-width="1.6"/>'
          '<path d="M486 218v8" stroke="#183a30" stroke-width="2"/>')
    p.lines(522, 218, ['chemical advisory: boiling does not', 'help; use bottled or ready-to-feed'], 'tiny warn')
    # do not use
    p.add('<path d="M470 300h22v-10h10v22h-10v-4h-22z" fill="#c9cdd0" stroke="#183a30" stroke-width="1.8"/>'
          '<path d="M497 312v8" stroke="#3d7186" stroke-width="3"/>')
    p.add(cross(488, 316, 10))
    p.lines(522, 306, ['no tap contact: no drinking, bathing,', 'dishwashing or skin contact'], 'tiny')
    p.band('No safe water for formula or wounds: use ready-to-feed and get public-health or medical help.')
    return p.svg()


# ---------------------------------------------------------------- Z13-P49
def lidded_bucket(x, y, w, h, label, bag=True):
    out = bucket(x, y, w, h, '#ffffff', 0.0)
    if bag:
        out += (f'<path d="M{x + 3} {y + 2}l-6 -10M{x + w - 3} {y + 2}l6 -10" stroke="#3b3b3b" stroke-width="2.4"/>'
                f'<path d="M{x + 6} {y + 4}L{x + w * .14} {y + h - 4}L{x + w * .86} {y + h - 4}L{x + w - 6} {y + 4}" '
                f'fill="none" stroke="#3b3b3b" stroke-width="1.4" stroke-dasharray="4 3"/>')
    out += (f'<rect x="{x - 6}" y="{y - 16}" width="{w + 12}" height="10" rx="3" fill="#6b8577" stroke="{INK}" stroke-width="2"/>'
            f'<text x="{x + w / 2}" y="{y + h * .62}" class="tiny" text-anchor="middle">{label}</text>')
    return out


def hands(x, y):
    return (f'<path d="M{x} {y}q10-14 22-2q4 6 0 14h-18q-6-4-4-12z" fill="{SKIN}" stroke="{INK}" stroke-width="1.4"/>'
            f'<path d="M{x + 30} {y}q-10-14-22-2q-4 6 0 14h18q6-4 4-12z" fill="{SKIN}" stroke="{INK}" stroke-width="1.4" '
            f'transform="translate(14 0)"/>')


def spigot_station(x, y):
    """Spigot jug on a stand with a thin stream over hands into a catch basin. (x, y): jug top-left."""
    return (f'<rect x="{x}" y="{y}" width="58" height="66" rx="8" fill="#dcecf3" stroke="{INK}" stroke-width="2.2"/>'
            f'<rect x="{x + 22}" y="{y - 8}" width="14" height="8" fill="#7c8c95"/>'
            f'<rect x="{x + 46}" y="{y + 52}" width="16" height="7" fill="#7c8c95" stroke="{INK}" stroke-width="1.2"/>'
            f'<rect x="{x - 10}" y="{y + 66}" width="78" height="8" fill="#9a8466"/>'
            f'<path d="M{x + 58} {y + 59}v38" stroke="{WATER_EDGE}" stroke-width="2.4"/>'
            + hands(x + 44, y + 102)
            + f'<path d="M{x + 28} {y + 136}h80l-8 30h-64z" fill="{WATER}" fill-opacity=".55" stroke="{INK}" stroke-width="2"/>')


def z13_p49():
    p = Plate('Z13-P49', 'Two-bucket emergency toilet beside a soap-and-water handwashing station',
              'A solid-waste bucket lined with two heavy bags, with dry cover material such as sawdust added after '
              'each use and a tight lid; a separate bucket for liquids; and a handwashing station with a spigot jug, '
              'soap and a catch basin right beside them. Hands are washed with soap and safe water after every use; '
              'alcohol rub does not replace handwashing after toilet, diaper or vomit tasks. Tied bags go into a '
              'lidded outdoor bin for disposal under local health rules, away from food areas, wells, gardens and '
              'storm drains. Conceptual, not to scale.')
    p.panel(24, 46, 560, 290, 'ok', '✓ TOILET STATION')
    p.panel(598, 46, 278, 290, 'neutral', 'WASTE AND DISPOSAL')
    p.add(lidded_bucket(52, 158, 100, 116, 'SOLIDS'))
    p.add('<path d="M62 174h80" stroke="#b08a5a" stroke-width="7" stroke-linecap="round"/>')
    p.add(lidded_bucket(180, 174, 80, 100, 'LIQUIDS', bag=False))
    p.lines(40, 100, ['two heavy bags, tight lid;', 'sawdust cover after each use'], 'tiny')
    p.lead((102, 126), (102, 140))
    p.lines(40, 304, ['solids and liquids in separate', 'buckets when practical'], 'tiny')
    p.add(spigot_station(338, 104))
    p.add('<rect x="404" y="140" width="18" height="26" rx="4" fill="#f2c94c" stroke="#183a30" stroke-width="1.6"/>')
    p.lines(430, 152, ['soap'], 'tiny')
    p.lines(418, 90, ['soap and safe water', 'after every use'], 'tiny ok')
    p.lines(456, 234, ['catch basin:', 'empty away', 'from wells, food'], 'tiny')
    p.lines(330, 306, ['alcohol rub does not replace', 'handwashing after toilet tasks'], 'tiny warn')
    # waste and disposal: two never rows, one required route
    p.add('<rect x="622" y="96" width="48" height="40" rx="4" fill="#c9cdd0" stroke="#183a30" stroke-width="2"/>'
          '<path d="M626 136l20-14 20 14" fill="none" stroke="#183a30" stroke-width="2"/>')
    p.add(cross(670, 98, 10))
    p.lines(684, 116, ['waste into storm', 'drains or creeks'], 'tiny')
    p.add('<path d="M630 200c10-16 30-16 40 0" fill="#7fa65a" stroke="#183a30" stroke-width="1.8"/>'
          '<path d="M650 184v16" stroke="#5b4630" stroke-width="2"/>')
    p.add(cross(672, 182, 10))
    p.lines(684, 198, ['near wells, gardens', 'or food areas'], 'tiny')
    p.add('<rect x="626" y="250" width="40" height="34" rx="3" fill="#5f6b70" stroke="#183a30" stroke-width="2"/>'
          '<rect x="622" y="244" width="48" height="8" rx="2" fill="#4a5459"/>')
    p.add(check(670, 248, 10))
    p.lines(684, 262, ['tied bags: lidded', 'outdoor bin, local', 'disposal rules'], 'tiny ok')
    p.band('Leaking bags, overflow or diarrheal illness at home: move to working sanitary facilities.')
    return p.svg()


# ---------------------------------------------------------------- Z13-P50
def z13_p50():
    p = Plate('Z13-P50', 'Low-water handwashing station with soap and water first',
              'Left: a spigot jug on a stand pours a thin stream of safe water over soapy hands into a catch basin, so '
              'a 20-second soap wash uses little water; the basin is emptied away from wells and food gardens. Right: '
              'after using the toilet, changing a diaper, cleaning up vomit or handling waste, and before handling '
              'food, wash with soap and water; hand sanitizer does not work well against norovirus and is not a '
              'substitute. Sanitizer with at least 60 percent alcohol is an interim fallback only when soap and water '
              'truly are unavailable and hands are not visibly dirty; saving water does not make it equivalent. '
              'Disposable plates save potable water. Conceptual, not to scale.')
    p.panel(24, 46, 380, 290, 'ok', '✓ THIN-STREAM STATION')
    p.panel(418, 46, 458, 290, 'neutral', 'WHICH HAND HYGIENE?')
    p.add(spigot_station(70, 96))
    p.add('<rect x="146" y="134" width="18" height="26" rx="4" fill="#f2c94c" stroke="#183a30" stroke-width="1.6"/>')
    p.lines(172, 146, ['soap'], 'tiny')
    p.lines(196, 104, ['thin stream of', 'safe water'], 'tiny')
    p.lead((194, 112), (132, 170))
    p.lines(196, 210, ['scrub 20 s'], 'tiny')
    p.lead((194, 206), (156, 208))
    p.lines(40, 290, ['catch basin: empty away', 'from wells and food gardens'], 'tiny')
    p.add('<ellipse cx="328" cy="246" rx="26" ry="8" fill="#ffffff" stroke="#183a30" stroke-width="1.8"/>'
          '<ellipse cx="328" cy="238" rx="26" ry="8" fill="#ffffff" stroke="#183a30" stroke-width="1.8"/>')
    p.lines(298, 274, ['paper plates', 'save water'], 'tiny')
    # decision rows
    p.add('<rect x="436" y="86" width="422" height="118" rx="8" fill="#e7f0ea" stroke="#7ea08d" stroke-width="1.4"/>')
    p.add(check(458, 112, 12))
    p.lines(478, 110, ['After toilet, diaper, vomit or waste,', 'and before food: SOAP AND WATER'], 'small', pitch=24)
    p.lines(478, 162, ['sanitizer does not work well against', 'norovirus and is not a substitute'], 'tiny warn')
    p.add('<rect x="436" y="216" width="422" height="104" rx="8" fill="#f7f4e6" stroke="#b9a87a" stroke-width="1.4"/>')
    p.add('<rect x="450" y="236" width="20" height="40" rx="4" fill="#cfe6ef" stroke="#183a30" stroke-width="1.6"/>'
          '<rect x="454" y="228" width="12" height="8" fill="#7c8c95"/>')
    p.lines(482, 242, ['Sanitizer, at least 60% alcohol: only if', 'soap and water are truly unavailable',
                       'and hands are not visibly dirty'], 'tiny', pitch=21)
    p.band('Vomiting or diarrhea in a water-rationed home: tighten hygiene and plan relocation to care.')
    return p.svg()


# ---------------------------------------------------------------- Z11-P32 (revision of the V02 plate)
Z11_P32_EDITS = [
    ('Z11-P32 · V02 TECHNICAL ILLUSTRATION · NOT TO SCALE', 'Z11-P32 · W2C REVISION OF V02 · NOT TO SCALE'),
    ('<desc id="desc">Plan-view geometric box detour showing four 90-degree right-angle turns and matched pace counts '
     'around a pond back onto the exact original bearing line.</desc>',
     '<desc id="desc">Plan-view box detour around a compact obstacle: four 90-degree turns, an offset leg counted in '
     'paces, a return leg paced to the same distance with extra paces where slope or brush shortens the stride, and a '
     'regained line that stays approximate until checked against the map. A matching count does not confirm '
     'position. Conceptual, not to scale.</desc>'),
    ('<text class="sm" x="72" y="164">Count N paces</text>', '<text class="sm" x="72" y="164">Count paces (N)</text>'),
    ('<text x="385" y="224">Pond / blowdown</text>', '<text x="450" y="254" text-anchor="middle">Pond / blowdown</text>'),
    ('<text class="sm" x="670" y="164">Exact N paces</text>',
     '<text class="sm" x="670" y="164">Same distance: about N,</text>'
     '<text class="sm" x="670" y="186">add paces on slope, brush</text>'),
    ('<text x="665" y="252">4. Resume line</text>',
     '<text x="665" y="252">4. Resume line</text><text class="sm" x="665" y="276">approximate: check map</text>'),
    ('<text class="guard" x="36" y="369">Keep offset legs perpendicular and count identical paces out and back; '
     'record pace total.</text>',
     '<text class="guard" x="36" y="369">Paced offsets are approximate; a matching count does not confirm position. '
     'Check the map.</text>'),
]


def z11_p32():
    svg = (V02 / 'Z11-P32.svg').read_text(encoding='utf-8')
    for old, new in Z11_P32_EDITS:
        if svg.count(old) != 1:
            raise SystemExit(f'Z11-P32 revision: expected one match for {old[:60]!r}')
        svg = svg.replace(old, new)
    return svg


PLATES = {'Z11-P63': z11_p63, 'Z04-P51': z04_p51, 'Z13-P49': z13_p49, 'Z13-P50': z13_p50, 'Z11-P32': z11_p32}


def checks():
    """Content checks that the corrected relationship is what the plate states."""
    out = {}
    p63 = z11_p63()
    out['Z11-P63'] = dict(location_first='Location first:' in p63, report_card_rows=p63.count('class="tiny inv"') == 6,
                          no_precondition='BEFORE dialing' not in p63)
    p51 = z04_p51()
    out['Z04-P51'] = dict(formula_separate='INFANT FORMULA' in p51, powder_not_sterile='not sterile' in p51,
                          formula_not_in_task_list='formula' not in p51.split('POTABLE WATER ONLY')[1].split('INFANT')[0])
    p49, p50 = z13_p49(), z13_p50()
    out['Z13-P49'] = dict(handwash_beside_toilet='soap and safe water' in p49,
                          sanitizer_not_equivalent='alcohol rub does not replace handwashing' in p49)
    out['Z13-P50'] = dict(soap_after_waste='SOAP AND WATER' in p50, sanitizer_fallback_only='truly unavailable' in p50,
                          no_clean_looking_shortcut='when hands look clean' not in p50)
    p32 = z11_p32()
    out['Z11-P32'] = dict(no_exact_claim='Exact' not in p32 and 'exact' not in p32, approximate='approximate' in p32,
                          geometry_unchanged=all(seg in p32 for seg in ('d="M250 218V108"', 'd="M250 108h400"', 'd="M650 108v104"')))
    for v in out.values():
        v['accepted'] = all(v.values())
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path)
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--only')
    args = parser.parse_args()
    for page, make in PLATES.items():
        if args.only and page != args.only:
            continue
        svg = make()
        if args.out:
            args.out.mkdir(parents=True, exist_ok=True)
            (args.out / f'{page}.svg').write_text(svg, encoding='utf-8')
        if args.write:
            (OUT / f'{page}.svg').write_text(svg, encoding='utf-8')
        if args.check and (OUT / f'{page}.svg').read_text(encoding='utf-8') != svg:
            raise SystemExit(f'{page} differs from a fresh build')
    result = checks()
    if not all(v['accepted'] for v in result.values()):
        raise SystemExit(f'Plate content check failed: {result}')
    print(f'{len(PLATES)} batch W2C-R1 plate(s) built; checks {result}')


if __name__ == '__main__':
    main()
