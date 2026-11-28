"""Wave 2C batch W2C-B02: household water and wastewater flow paths.

Each plate draws where water moves, under what pressure, and where contamination
can enter or be stopped. Sources are recorded per plate in the W2C ledger.
Run with --out DIR to preview, --write to refresh the revised SVGs, or --check.
"""
import argparse
from pathlib import Path

from w2c_svg import (AIR, FLOW, INK, REVERSE, SOIL, STEEL, WATER, WATER_EDGE, Plate, bucket, check, cross,
                     ground, hose, jug, pipe)

OUT = Path(__file__).resolve().parents[1] / 'foundations/visual/w2c_technical/revised'


def faucet(x, y, breaker=False):
    """Wall faucet (sill cock) at a wall face x; spout outlet returned."""
    parts = [f'<rect x="{x}" y="{y - 9}" width="34" height="18" rx="4" fill="{STEEL}" stroke="{INK}" stroke-width="2"/>',
             f'<rect x="{x + 8}" y="{y - 22}" width="14" height="13" rx="3" fill="#7c8c95" stroke="{INK}" stroke-width="1.6"/>',
             f'<rect x="{x + 22}" y="{y + 9}" width="12" height="12" fill="{STEEL}" stroke="{INK}" stroke-width="2"/>']
    outlet = (x + 28, y + 21)
    if breaker:
        bx, by = x + 20, y + 21
        parts.append(f'<rect x="{bx}" y="{by}" width="16" height="22" rx="3" fill="#e2c46b" stroke="{INK}" stroke-width="2"/>')
        for k in range(3):
            parts.append(f'<circle cx="{bx + 4 + k * 4}" cy="{by + 8}" r="1.6" fill="{INK}"/>')
        outlet = (bx + 8, by + 22)
    return ''.join(parts), outlet


def z13_p44():
    p = Plate('Z13-P44', 'Backsiphonage through a submerged hose and the two simple barriers',
              'Left: an outdoor faucet feeds a garden hose whose end sits under soapy or chemical liquid in a bucket. '
              'A main break or shutoff drops supply pressure, so the liquid is pulled back up the hose and into the '
              'house pipes. Right: a hose-bibb vacuum breaker on the faucet vents to air when pressure drops, the hose '
              'end is held above the bucket rim to keep an air gap, and a rain barrel or sump has no hard connection '
              'to house plumbing. Conceptual drawing, not to scale.')
    p.panel(24, 46, 414, 290, 'bad', '✕ HOW BACKSIPHONAGE HAPPENS')
    p.panel(462, 46, 414, 290, 'ok', '✓ BARRIERS THAT STOP IT')
    # --- left: the failure path
    p.add(ground(30, 300, 402, 32))
    p.add('<rect x="58" y="78" width="16" height="222" fill="#d7d0bd" stroke="#7d7462" stroke-width="1.5"/>')
    p.add(pipe([(66, 128), (66, 316), (420, 316)], 9))
    f, (ox, oy) = faucet(74, 128)
    p.add(f)
    p.add(bucket(236, 206, 92, 84, liquid='#cfd8a8', level=0.62))
    p.add(hose([(ox, oy), (ox, 174), (150, 178), (214, 182), (258, 188), (270, 230), (276, 268)]))
    p.add(f'<path d="M376 309l10-10 8 8 9-9" fill="none" stroke="{REVERSE}" stroke-width="3"/>')
    p.arrow('M270 258L262 214', 'reverse', 3.5)
    p.arrow('M232 186L170 180', 'reverse', 3.5)
    p.arrow('M78 200V262', 'reverse', 3.5)
    p.arrow('M120 316H300', 'reverse', 3.5)
    p.lead((282, 266), (334, 200)).lines(338, 194, ['hose end', 'under soapy', 'liquid'], 'tiny')
    p.lead((196, 172), (204, 132)).lines(150, 100, ['liquid pulled back', 'into house pipes'], 'tiny')
    p.lead((390, 300), (396, 290)).lines(332, 266, ['main break:', 'pressure drop'], 'tiny')
    # --- right: vacuum breaker, air gap, isolated cistern
    p.add(ground(468, 300, 402, 32))
    p.add('<rect x="496" y="78" width="16" height="222" fill="#d7d0bd" stroke="#7d7462" stroke-width="1.5"/>')
    p.add(pipe([(504, 128), (504, 316), (860, 316)], 9))
    f, (bx, by) = faucet(512, 128, breaker=True)
    p.add(f)
    p.arrow('M556 140L540 147', 'air', 2.5)
    p.arrow('M556 156L540 155', 'air', 2.5)
    p.add(bucket(640, 216, 92, 76, liquid='#bcd8e3', level=0.5))
    p.add(hose([(bx, by), (bx, 196), (590, 198), (640, 182), (676, 178), (684, 196)]))
    p.add(f'<path d="M684 199v42" stroke="{WATER_EDGE}" stroke-width="3" stroke-dasharray="4 4"/>')
    p.arrow('M594 188L636 176', 'flow', 3.2)
    p.add(f'<path d="M694 199h28M694 216h28" stroke="{INK}" stroke-width="1.4"/>'
          f'<path d="M716 199v17" stroke="{INK}" stroke-width="1.4"/>')
    p.lead((694, 207), (626, 236)).lines(520, 244, ['air gap:', 'end above rim'], 'tiny')
    p.lead((549, 150), (586, 118)).lines(590, 98, ['vacuum breaker', 'vents to air if', 'pressure drops'], 'tiny')
    p.add('<rect x="792" y="226" width="56" height="70" rx="8" fill="#9fb6a0" stroke="#3f5a46" stroke-width="2"/>'
          '<path d="M792 240h56M792 282h56" stroke="#3f5a46" stroke-width="1.5"/>')
    p.add(pipe([(792, 262), (760, 262), (760, 310)], 6, '#c4c9c0', '#7d857a'))
    p.add(cross(760, 286, 11))
    p.lines(722, 98, ['rain barrel, sump or', 'untreated pump: no', 'hard connection to', 'house plumbing'], 'tiny')
    p.lead((812, 224), (806, 184))
    p.band('Suspected backsiphonage: stop drinking tap water; call the utility and a licensed plumber.')
    return p.svg()


def z13_p37():
    p = Plate('Z13-P37', 'Appliances on the water line during a drinking water advisory',
              'Left: a refrigerator cutaway. Advisory tap water enters from the house supply line, passes through the '
              'filter cartridge and feeds both the icemaker and the door dispenser. The icemaker is switched off, ice '
              'made from advisory water is discarded, and the filter is marked as not making advisory water safe. '
              'Right: a humidifier or CPAP water chamber is filled from a jug of safe water, not from the advisory '
              'tap. Conceptual drawing, not to scale.')
    p.panel(24, 46, 520, 290, 'bad', 'WATER-LINE APPLIANCES DURING ANY ADVISORY')
    # house wall and supply valve
    p.add('<rect x="40" y="84" width="12" height="238" fill="#d7d0bd" stroke="#7d7462" stroke-width="1.5"/>')
    p.add(pipe([(46, 300), (92, 300)], 6, '#c79c8a', '#7d4a3a'))
    p.add(f'<circle cx="64" cy="300" r="7" fill="{STEEL}" stroke="{INK}" stroke-width="2"/>')
    # refrigerator body, freezer and fresh-food compartments
    p.add('<rect x="96" y="78" width="200" height="248" rx="12" fill="#f6f7f2" stroke="#183a30" stroke-width="2.6"/>'
          '<line x1="96" y1="166" x2="296" y2="166" stroke="#183a30" stroke-width="2.2"/>')
    p.add('<rect x="112" y="92" width="70" height="22" rx="4" fill="#d9dee0" stroke="#183a30" stroke-width="1.8"/>'
          '<rect x="112" y="118" width="70" height="38" rx="4" fill="#e8f1f6" stroke="#183a30" stroke-width="1.8"/>')
    for k, (cx, cy) in enumerate([(124, 140), (140, 134), (156, 142), (170, 136), (132, 148), (162, 150)]):
        p.add(f'<rect x="{cx - 5}" y="{cy - 5}" width="10" height="10" rx="2" fill="#ffffff" stroke="#6f8f9d" stroke-width="1.2"/>')
    p.add('<rect x="232" y="96" width="46" height="56" rx="6" fill="#dfe5e7" stroke="#183a30" stroke-width="1.8"/>'
          '<path d="M244 104h22v16h-22z" fill="#9aa8ad"/><path d="M247 126h16v20h-16z" fill="#ffffff" stroke="#183a30" stroke-width="1.4"/>')
    p.add('<rect x="250" y="178" width="18" height="58" rx="5" fill="#e9e1c4" stroke="#183a30" stroke-width="1.8"/>'
          '<path d="M250 194h18M250 206h18M250 218h18" stroke="#9a8a5b" stroke-width="1.2"/>')
    # advisory water path: supply -> filter -> icemaker and dispenser
    p.add(pipe([(92, 300), (286, 300), (286, 244), (259, 244), (259, 236)], 4, '#c79c8a', '#7d4a3a'))
    p.add(pipe([(259, 178), (259, 170), (200, 170), (200, 103), (182, 103)], 4, '#c79c8a', '#7d4a3a'))
    p.add(pipe([(259, 170), (259, 162), (255, 162), (255, 120)], 4, '#c79c8a', '#7d4a3a'))
    p.arrow('M130 300H208', 'reverse', 3)
    p.arrow('M286 290V262', 'reverse', 3)
    p.arrow('M206 150V116', 'reverse', 3)
    p.add(cross(170, 103, 9), cross(272, 144, 11))
    p.add('<rect x="116" y="96" width="34" height="14" rx="3" fill="#183a30"/><text x="133" y="107" class="tiny inv" text-anchor="middle" font-size="11">OFF</text>')
    p.lead((268, 206), (318, 214)).lines(322, 210, ['filter does not make', 'advisory water safe'], 'tiny')
    p.lead((182, 104), (322, 112)).lines(326, 98, ['icemaker off; discard', 'ice made from advisory', 'water (freezing does', 'not kill all germs)'], 'tiny')
    p.lines(322, 262, ['no dispenser water or', 'ice until the advisory', 'is lifted'], 'tiny')
    p.lead((276, 152), (318, 262))
    # right: reservoirs filled with safe water
    p.panel(562, 46, 314, 290, 'ok', 'RESERVOIRS: SAFE WATER ONLY')
    p.add('<rect x="700" y="196" width="130" height="86" rx="12" fill="#e9eef0" stroke="#183a30" stroke-width="2.4"/>'
          '<rect x="716" y="214" width="56" height="52" rx="6" fill="#d6ecf4" stroke="#3d7186" stroke-width="2"/>'
          '<rect x="716" y="238" width="56" height="28" fill="#9cc3cf"/>'
          '<path d="M830 226q26 0 26 30v26" fill="none" stroke="#6b7f8c" stroke-width="6"/>')
    p.add(jug(616, 124, 70, 'SAFE'))
    p.arrow('M666 146Q706 140 734 206', 'flow', 3.2)
    f, _ = faucet(588, 252)
    p.add(f)
    p.add(cross(650, 262, 11))
    p.lines(580, 102, ['bottled, distilled or as', 'directed by the utility'], 'tiny')
    p.lines(712, 306, ['humidifier or CPAP'], 'tiny')
    p.lines(578, 300, ['not advisory', 'tap water'], 'tiny')
    p.band('Reconnect the icemaker and dispenser only after the utility lifts the advisory.')
    return p.svg()


def tank(x, y, w, h, full=False, dashed=False):
    if dashed:
        return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="none" stroke="#6d6d6d" '
                'stroke-width="2" stroke-dasharray="7 5"/>')
    inner = (f'<rect x="{x + 8}" y="{y + 18}" width="{w - 16}" height="{h - 26}" fill="#8f7d55"/>' if full else '')
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="#d9d6cc" stroke="#55534c" stroke-width="3"/>'
            f'<rect x="{x + 8}" y="{y + 8}" width="{w - 16}" height="{h - 16}" fill="#f4f2ea"/>{inner}'
            f'<rect x="{x + w / 2 - 14}" y="{y - 14}" width="28" height="14" fill="#cfcbbf" stroke="#55534c" stroke-width="2"/>')


def z13_p48():
    p = Plate('Z13-P48', 'Septic tank in flooded, saturated soil',
              'Two ground cross-sections with floodwater over saturated soil. Left: a septic tank pumped empty while '
              'the soil is saturated; groundwater presses up on its base, the tank lifts from its original seat and '
              'the inlet and outlet pipes break at the joints. Right: the tank is left full and unopened, basement '
              'drains are plugged, indoor water use is cut sharply, and equipment stays off the wet drainfield until '
              'the water recedes and a professional inspects the system. Conceptual drawing, not to scale.')
    p.panel(24, 46, 414, 290, 'bad', '✕ PUMPED EMPTY IN SATURATED SOIL')
    p.panel(462, 46, 414, 290, 'ok', '✓ WHILE THE YARD IS FLOODED')
    for x0 in (30, 468):
        p.add(f'<rect x="{x0}" y="112" width="402" height="14" fill="{WATER}"/>')
        p.add(ground(x0, 126, 402, 204, water_top=126))
        p.add(f'<path d="M{x0} 112h402" stroke="{WATER_EDGE}" stroke-width="2"/>')
    # left: empty tank lifted out of its seat by buoyancy, joints broken
    p.add(tank(140, 196, 170, 92, dashed=True))
    p.add(tank(140, 168, 170, 92))
    p.add(pipe([(30, 210), (118, 210)], 8, '#c4c9c0', '#5f665c'), pipe([(332, 224), (432, 224)], 8, '#c4c9c0', '#5f665c'))
    p.add(pipe([(140, 186), (128, 186)], 8, '#c4c9c0', '#5f665c'), pipe([(310, 196), (322, 196)], 8, '#c4c9c0', '#5f665c'))
    p.add(f'<path d="M118 198l6 6-5 6 6 6M332 212l-6 6 5 6-6 6" fill="none" stroke="{REVERSE}" stroke-width="2.6"/>')
    for x in (170, 225, 280):
        p.arrow(f'M{x} 318V266', 'load', 4)
    p.arrow('M326 238V206', 'ink', 2.5, dash='5 4')
    p.lines(322, 268, ['groundwater', 'pushes up on', 'empty tank'], 'tiny')
    p.lead((118, 204), (92, 172)).lines(40, 150, ['pipes break', 'at joints'], 'tiny')
    p.lines(40, 300, ['original', 'seat'], 'tiny')
    p.lead((104, 300), (140, 288))
    # right: full tank stays seated; house with plugged drain; drainfield kept clear
    p.add(tank(560, 196, 150, 86, full=True))
    p.add(pipe([(468, 212), (560, 212)], 8, '#c4c9c0', '#5f665c'), pipe([(710, 222), (868, 222)], 8, '#c4c9c0', '#5f665c'))
    for x in (740, 790, 840):
        p.add(f'<path d="M{x} 236v40" stroke="#5f665c" stroke-width="3" stroke-dasharray="4 4"/>')
    p.add('<path d="M484 112V96l26-14 26 14v16" fill="#e9e2cf" stroke="#183a30" stroke-width="2.2"/>')
    p.add(f'<rect x="512" y="102" width="16" height="8" rx="2" fill="{INK}"/>')
    p.lines(552, 150, ['plug basement drains;', 'cut water use sharply'], 'tiny')
    p.lead((548, 146), (526, 110))
    p.lines(594, 302, ['leave full; do not', 'pump or open it'], 'tiny')
    p.lines(742, 162, ['keep equipment', 'off the wet', 'drainfield'], 'tiny')
    p.lead((790, 222), (790, 210))
    p.band('Sewage backing up or surfacing: stop using plumbing, keep away, call a septic professional.')
    return p.svg()


def z13_p41():
    p = Plate('Z13-P41', 'Private well during a power outage',
              'Cross-section of a house and private well with the power out. The breaker for the submersible pump has '
              'no power, so the pump in the well cannot run or refill the basement pressure tank. The tank pushes out '
              'only its small stored reserve, then the kitchen tap sputters and stops; common tanks deliver about 5 to '
              '16 gallons between pump starts. A side panel shows the plan: stored drinking water, a labelled pump '
              'breaker, and well cap and pump wiring left to licensed contractors. Conceptual drawing, not to scale.')
    p.add(ground(30, 150, 560, 182))
    p.add('<rect x="44" y="70" width="252" height="80" fill="#efe9d8" stroke="#183a30" stroke-width="2.4"/>'
          '<rect x="44" y="150" width="252" height="150" fill="#e8e4d6" stroke="#183a30" stroke-width="2.4"/>')
    # breaker panel with no power
    p.add('<rect x="54" y="168" width="34" height="50" rx="3" fill="#cfd5d8" stroke="#183a30" stroke-width="2"/>'
          '<rect x="60" y="186" width="22" height="8" fill="#183a30"/>')
    p.add(cross(71, 206 + 30, 10))
    p.add('<path d="M88 192H300M300 192h12V200H462" fill="none" stroke="#6b5b2f" stroke-width="2.2" stroke-dasharray="6 4"/>'
          '<path d="M462 200V300" fill="none" stroke="#6b5b2f" stroke-width="2.2" stroke-dasharray="6 4"/>')
    # pressure tank with low gauge
    p.add('<rect x="108" y="206" width="58" height="88" rx="22" fill="#5f8fa3" stroke="#183a30" stroke-width="2.4"/>'
          '<rect x="114" y="250" width="46" height="40" rx="14" fill="#9cc3cf"/>')
    p.add('<circle cx="190" cy="232" r="13" fill="#fff" stroke="#183a30" stroke-width="2"/>'
          '<path d="M190 232L181 241" stroke="#8b3825" stroke-width="2.6"/>')
    p.add(pipe([(166, 262), (232, 262), (232, 112), (252, 112)], 6))
    p.add(pipe([(232, 262), (300, 262), (300, 214), (470, 214)], 6))
    p.add('<rect x="246" y="100" width="26" height="12" fill="#c9cdd0" stroke="#183a30" stroke-width="1.8"/>'
          '<path d="M262 112v8" stroke="#183a30" stroke-width="2.4"/>')
    p.add(f'<path d="M262 124v4M262 134v4" stroke="{WATER_EDGE}" stroke-width="3"/>')
    # well casing, water level and idle submersible pump
    p.add('<rect x="462" y="136" width="20" height="196" fill="#d5d9db" stroke="#183a30" stroke-width="2"/>'
          '<rect x="458" y="128" width="28" height="10" rx="2" fill="#7c8c95" stroke="#183a30" stroke-width="1.8"/>'
          f'<rect x="464" y="236" width="16" height="96" fill="{WATER}"/>'
          '<rect x="465" y="286" width="14" height="38" rx="3" fill="#7c8c95" stroke="#183a30" stroke-width="1.6"/>')
    p.add(pipe([(472, 286), (472, 214)], 4))
    p.lead((488, 300), (520, 300)).lines(524, 290, ['pump idle:', 'no power'], 'tiny')
    p.lead((486, 134), (520, 120)).lines(524, 110, ['well cap'], 'tiny')
    p.lines(320, 84, ['tank pushes out a small', 'stored reserve, then the', 'tap sputters and stops'], 'tiny')
    p.lead((316, 100), (196, 222))
    p.lines(320, 250, ['common tanks: about', '5 to 16 gal between', 'pump starts (MDH)'], 'tiny')
    p.lead((316, 246), (170, 246))
    p.lines(58, 322, ['breaker: no power'], 'tiny')
    p.lead((72, 308), (71, 248))
    # plan column
    p.panel(604, 46, 272, 290, 'ok', 'PLAN BEFORE AN OUTAGE')
    for k in range(3):
        p.add(jug(624 + k * 44, 96, 56, None))
    p.lines(624, 178, ['stored drinking water,', 'at least 1 gal per', 'person per day'], 'tiny')
    p.add('<rect x="624" y="244" width="30" height="40" rx="3" fill="#cfd5d8" stroke="#183a30" stroke-width="2"/>'
          '<rect x="630" y="256" width="18" height="8" fill="#183a30"/><path d="M648 260h18" stroke="#183a30" stroke-width="1.6"/>'
          '<rect x="666" y="252" width="40" height="16" rx="3" fill="#f7e5a6" stroke="#183a30" stroke-width="1.4"/>')
    p.lines(716, 258, ['pump breaker', 'labelled'], 'tiny')
    p.lines(624, 306, ['cap and wiring: licensed', 'contractors only'], 'tiny')
    p.band('Muddy water, sputtering or a tripping breaker: switch the well off; call a licensed contractor.')
    return p.svg()


def z13_p53():
    p = Plate('Z13-P53', 'Non-potable water for flushing, only into a working drain',
              'Bathroom cross-section. A bucket marked non-potable is poured into the toilet bowl, and the flush goes '
              'down the drain only because the sewer or septic line is working. Drinking water and food preparation '
              'containers sit apart on their own shelf and never share containers with non-potable water. A stop '
              'panel shows the warning signs that end all flushing: gurgling, slow drains, sewage odour or backup, '
              'with a lined bucket toilet as the alternative. Conceptual drawing, not to scale.')
    p.add('<rect x="30" y="268" width="560" height="10" fill="#bdb6a3"/>')
    p.add(ground(30, 278, 560, 54))
    # drinking-water shelf kept apart
    p.add('<rect x="44" y="150" width="120" height="8" fill="#8d7d5c"/>')
    p.add(jug(56, 94, 54, None), jug(104, 94, 54, None))
    p.add('<path d="M186 70V262" stroke="#8b3825" stroke-width="2.4" stroke-dasharray="8 6"/>')
    p.lines(40, 182, ['drinking and', 'food water', 'kept apart'], 'tiny')
    # toilet in section with drain to sewer
    p.add('<path d="M330 150h70v70h-70z" fill="#f7f8f4" stroke="#183a30" stroke-width="2.4"/>'
          '<path d="M300 222h112q0 34-30 44h-52q-30-10-30-44z" fill="#f7f8f4" stroke="#183a30" stroke-width="2.4"/>'
          f'<path d="M320 232h82q-4 18-24 24h-34q-20-6-24-24z" fill="{WATER}"/>')
    p.add(pipe([(356, 268), (356, 296), (580, 312)], 9, '#b8b09a', '#6a624f'))
    p.arrow('M396 300L520 309', 'flow', 3)
    p.lines(376, 330, ['to working sewer or septic'], 'tiny')
    # labelled non-potable bucket being poured
    p.add('<g transform="rotate(-38 244 150)">' + bucket(214, 128, 64, 60, liquid='#c9c6a5', level=0.5) + '</g>')
    p.add('<rect x="196" y="222" width="104" height="22" rx="3" fill="#8b3825"/>'
          '<text x="248" y="238" class="tiny inv" text-anchor="middle" font-size="13">NON-POTABLE</text>')
    p.lead((236, 222), (232, 200))
    p.arrow('M286 150Q312 172 332 222', 'flow', 3.2)
    p.lines(430, 150, ['pour into the bowl', 'only if the drain', 'is working'], 'tiny')
    p.lead((426, 160), (402, 226))
    # stop panel
    p.panel(604, 46, 272, 290, 'bad', '✕ STOP ALL FLUSHING')
    p.lines(624, 104, ['gurgling pipes', 'slow drains', 'sewage smell', 'backup from a drain'], 'small')
    p.add('<rect x="640" y="214" width="62" height="62" rx="6" fill="#e9e6da" stroke="#183a30" stroke-width="2.2"/>'
          '<path d="M636 212h70" stroke="#183a30" stroke-width="5"/><path d="M646 222q25 30 50 0" fill="none" stroke="#6b7f8c" stroke-width="2"/>')
    p.lines(716, 236, ['use a lined', 'bucket toilet'], 'tiny')
    p.band('Never add water to a failed, flooded or backing-up sewer or septic system.')
    return p.svg()


PLATES = {'Z13-P44': z13_p44, 'Z13-P37': z13_p37, 'Z13-P48': z13_p48, 'Z13-P41': z13_p41, 'Z13-P53': z13_p53}


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
    print(f'{len(PLATES)} batch W2C-B02 plate(s) built')


if __name__ == '__main__':
    main()
