"""Wave 2C batch W2C-B07: the household and field water-treatment chain.

Plates draw the physical order and limits of treatment: clarify, filter and disinfect in
sequence; one official bleach table per bottle (CDC and EPA differ for 8.25% bleach);
label-governed tablet contact time; absolute versus nominal filter pores; sanitizing a
storage container; and one-way raw, waiting and clean zones. Numbers appear only where a
cited CDC or EPA section states them (claims W31-W35, read 2026-11-28).
Run with --out DIR, --write or --check (includes content checks).
"""
import argparse
from pathlib import Path

from w2c_svg import FLOW, INK, REVERSE, WATER, WATER_EDGE, Plate, check, cross, jug

OUT = Path(__file__).resolve().parents[1] / 'foundations/visual/w2c_technical/revised'
MUD = '#b9a77d'
SILT = '#8a7350'


def bottle(x, y, h=64, fill='#dcecf3', cap='#5f8fa3'):
    w = h * 0.42
    return (f'<rect x="{x + w * .3:.1f}" y="{y}" width="{w * .4:.1f}" height="{h * .12:.1f}" rx="2" fill="{cap}" stroke="{INK}" stroke-width="1.6"/>'
            f'<rect x="{x}" y="{y + h * .12:.1f}" width="{w:.1f}" height="{h * .88:.1f}" rx="6" fill="{fill}" stroke="{INK}" stroke-width="2"/>')


def timer(cx, cy, r=16, text=''):
    out = (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#ffffff" stroke="{INK}" stroke-width="2"/>'
           f'<path d="M{cx} {cy}v-{r * .7:.1f}M{cx} {cy}l{r * .5:.1f} {r * .25:.1f}" stroke="{INK}" stroke-width="2"/>'
           f'<rect x="{cx - 4}" y="{cy - r - 6}" width="8" height="5" fill="{INK}"/>')
    return out


# ---------------------------------------------------------------- Z04-P42
def z04_p42():
    p = Plate('Z04-P42', 'Clarify, filter, then disinfect: the barrier order for raw water',
              'Cloudy raw water is first clarified by settling or straining through cloth, which is preparation, not '
              'treatment. It then passes through a filter rated absolute 1 micron or smaller, or certified to NSF/ANSI '
              '53 or 58 for cyst reduction, which removes parasites; only an absolute 0.3-micron rating also removes '
              'bacteria, and portable filters do not remove viruses. Chemical or UV disinfection follows to inactivate '
              'viruses and bacteria; UV works only in clear water. Water is drunk only from the clean side. Below, two '
              'wrong orders are crossed out: UV or bleach on cloudy water, and filtering after disinfection through a '
              'dirty cartridge. Conceptual, not to scale.')
    p.panel(24, 46, 852, 206, 'ok', '✓ CLARIFY, THEN FILTER, THEN DISINFECT')
    # raw jug
    p.add(jug(52, 104, 70, None, MUD))
    p.lines(40, 196, ['cloudy', 'raw water'], 'tiny')
    # clarify: settling jar
    p.add(f'<rect x="168" y="104" width="64" height="72" rx="6" fill="{WATER}" fill-opacity=".45" stroke="{INK}" stroke-width="2"/>'
          f'<rect x="170" y="156" width="60" height="18" fill="{SILT}" fill-opacity=".85"/>')
    p.lines(150, 96, ['1 CLARIFY'], 'tiny ok')
    p.lines(150, 196, ['settle or strain', '(not treatment)'], 'tiny')
    # filter cartridge
    p.add('<rect x="352" y="100" width="56" height="80" rx="10" fill="#e8eef0" stroke="#183a30" stroke-width="2.2"/>'
          + ''.join(f'<path d="M{360 + k * 8} 110v60" stroke="#9aa59c" stroke-width="2"/>' for k in range(6)))
    p.lines(330, 96, ['2 FILTER'], 'tiny ok')
    p.lines(330, 196, ['absolute ≤1 µm or', 'NSF 53/58 cyst claim'], 'tiny')
    # disinfect: bottle with drop and UV pen
    p.add(bottle(552, 112, 64))
    p.add('<path d="M566 101q-5 7 0 10q5-3 0-10z" fill="#5f8fa3" stroke="#183a30" stroke-width="1.2"/>'
          '<rect x="600" y="100" width="12" height="62" rx="5" fill="#4a4f52" stroke="#183a30" stroke-width="1.4"/>'
          '<rect x="602" y="150" width="8" height="10" fill="#9b7fd4"/>')
    p.lines(530, 96, ['3 DISINFECT'], 'tiny ok')
    p.lines(530, 196, ['chemical or UV', '(UV: clear water)'], 'tiny')
    # clean bottle
    p.add(bottle(742, 112, 64, '#cfe6ef'))
    p.add(check(790, 118, 11))
    p.lines(720, 196, ['drink only from', 'the clean side'], 'tiny')
    for x1, x2 in ((110, 158), (240, 342), (418, 540), (622, 732)):
        p.arrow(f'M{x1} 142H{x2}', 'flow', 3.5)
    p.lines(330, 244, ['portable filters do not remove viruses: disinfect after filtering'], 'tiny warn')
    # wrong orders
    p.panel(24, 262, 420, 74, 'bad', '✕ UV OR BLEACH ON CLOUDY WATER')
    p.lines(40, 320, ['particles shield germs: clarify first'], 'tiny')
    p.panel(456, 262, 420, 74, 'bad', '✕ FILTERING AFTER DISINFECTING')
    p.lines(472, 320, ['a dirty cartridge can recontaminate'], 'tiny')
    p.band('Barrier failed or chemicals suspected: boil if chemically safe, or switch to a safe supply.')
    return p.svg()


# ---------------------------------------------------------------- Z04-P39
def z04_p39():
    p = Plate('Z04-P39', 'One complete official bleach table for one bottle',
              'Left: a bottle of regular, unscented household bleach whose label gives its sodium hypochlorite '
              'strength, here 8.25 percent; the bleach must be fresh and free of scent or added cleaners. Centre: two '
              'current official tables give different drop counts for one gallon of that bottle: the CDC table for 5 '
              'to 9 percent bleach says 8 drops, the EPA column for 8.25 percent says 6 drops. One complete table is '
              'followed; tables are never mixed or averaged. Right: drops measured into a one-gallon jug, doubled only '
              'when the chosen table says so for cloudy, coloured or very cold water, then at least 30 minutes of '
              'waiting before drinking. Conceptual, not to scale.')
    p.panel(24, 46, 270, 290, 'neutral', 'CHECK THE BOTTLE')
    p.panel(308, 46, 314, 290, 'neutral', 'TWO TABLES, ONE BOTTLE')
    p.panel(636, 46, 240, 290, 'ok', '✓ DOSE AND WAIT')
    p.add('<path d="M74 118h56v-14h16v14h12q14 0 14 14v136q0 12-12 12h-86q-12 0-12-12V130q0-12 12-12z" '
          'fill="#f4f6f7" stroke="#183a30" stroke-width="2.2"/>'
          '<rect x="76" y="160" width="86" height="64" rx="4" fill="#ffffff" stroke="#9aa59c" stroke-width="1.4"/>')
    p.lines(84, 182, ['regular,', 'unscented'], 'tiny')
    p.lines(40, 304, ['label: sodium', 'hypochlorite 8.25%'], 'tiny')
    p.lead((104, 286), (118, 226))
    # tables
    for i, (head, row, n) in enumerate((('CDC table, 5% to 9%', '1 gallon: 8 drops', 8),
                                        ('EPA column, 8.25%', '1 gallon: 6 drops', 6))):
        y = 92 + i * 92
        p.add(f'<rect x="326" y="{y}" width="278" height="76" rx="6" fill="#ffffff" stroke="#183a30" stroke-width="1.8"/>'
              f'<rect x="326" y="{y}" width="278" height="26" rx="6" fill="#e7ece9"/>')
        p.text(338, y + 19, head, 'tiny')
        p.add(f'<text x="338" y="{y + 58}" class="small" data-drops="{n}">{row}</text>')
    p.lines(326, 290, ['follow ONE complete table;', 'never mix or average them'], 'tiny warn')
    # dose and wait
    p.add(jug(664, 150, 96, '1 gal'))
    p.add('<path d="M700 96v26" stroke="#183a30" stroke-width="3"/><rect x="694" y="80" width="12" height="18" rx="5" fill="#c4472f"/>'
          '<path d="M700 128q-4 6 0 9q4-3 0-9zM700 140q-4 6 0 9q4-3 0-9z" fill="#5f8fa3"/>')
    p.add(timer(808, 182, 22))
    p.lines(780, 230, ['30 min'], 'small')
    p.lines(652, 272, ['cloudy, coloured or', 'very cold: double only', 'as your table says'], 'tiny')
    p.band('Strength or steps uncertain, or chemicals, fuel or algal toxins suspected: use another supply.')
    return p.svg()


# ---------------------------------------------------------------- Z04-P40
def tablet(x, y, fill='#e9e4f5'):
    return f'<rect x="{x}" y="{y}" width="26" height="16" rx="8" fill="{fill}" stroke="{INK}" stroke-width="1.6"/>'


def z04_p40():
    p = Plate('Z04-P40', 'The product label sets tablet dose and contact time',
              'Left: the water conditions (temperature, clarity and volume) are read against the product label, which '
              'sets the dose and the full contact time; nobody drinks before the time is complete. Right: chemistries '
              'differ. Chlorine dioxide kills Giardia and is somewhat effective against Cryptosporidium, so filtering '
              'first is safest; chlorine and iodine kill viruses and bacteria but not parasites reliably; iodine-treated '
              'water is avoided in pregnancy, with thyroid problems or iodine hypersensitivity, and by anyone for more '
              'than a few weeks. Conceptual, not to scale.')
    p.panel(24, 46, 380, 290, 'neutral', 'CONDITIONS, THEN THE LABEL')
    p.panel(418, 46, 458, 290, 'neutral', 'CHEMISTRY DIFFERS')
    # conditions
    p.add(f'<rect x="52" y="92" width="16" height="70" rx="8" fill="#ffffff" stroke="{INK}" stroke-width="2"/>'
          f'<rect x="56" y="132" width="8" height="28" fill="{WATER_EDGE}"/>')
    p.lines(78, 120, ['water temperature'], 'tiny')
    p.add(f'<path d="M52 186h30l-4 40h-22z" fill="{MUD}" fill-opacity=".7" stroke="{INK}" stroke-width="1.8"/>')
    p.lines(92, 212, ['clarity'], 'tiny')
    p.add(bottle(54, 246, 52))
    p.lines(92, 280, ['volume'], 'tiny')
    for y in (128, 208, 272):
        p.arrow(f'M216 {y}L262 {y + (190 - y) * .55:.0f}', 'ink', 2.5)
    p.add('<rect x="270" y="150" width="112" height="84" rx="6" fill="#ffffff" stroke="#183a30" stroke-width="2"/>'
          '<path d="M282 176h88M282 194h88M282 212h60" stroke="#9aa59c" stroke-width="3"/>')
    p.lines(270, 142, ['LABEL'], 'tiny ok')
    p.add(timer(326, 288, 18))
    p.lines(206, 330, ['full contact time first'], 'tiny')
    # chemistry rows
    rows = [('chlorine dioxide', ['kills Giardia; somewhat effective on', 'Cryptosporidium: filter first']),
            ('chlorine', ['viruses and bacteria;', 'parasites not reliably']),
            ('iodine', ['not in pregnancy, thyroid problems or', 'iodine allergy; not beyond a few weeks'])]
    for i, (name, lines) in enumerate(rows):
        y = 96 + i * 78
        p.add(tablet(438, y - 12))
        p.text(474, y, name, 'small')
        p.lines(474, y + 22, lines, 'tiny')
    p.band('Unlabelled loose tablets, or fuel, chemicals or algal toxins suspected: do not rely on them.')
    return p.svg()


# ---------------------------------------------------------------- Z04-P35
def membrane(x, y, h, pores, big=()):
    """Vertical membrane at x with pore gaps; pores: list of y offsets; big: offsets of wide pores."""
    out = [f'<rect x="{x}" y="{y}" width="14" height="{h}" fill="#c9cdd0" stroke="{INK}" stroke-width="1.6"/>']
    for k in pores:
        gap = 12 if k in big else 3
        out.append(f'<rect x="{x - 1}" y="{y + k - gap / 2:.1f}" width="16" height="{gap}" fill="#ffffff"/>')
    return ''.join(out)


def cyst(x, y, r=7):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="#b5654a" stroke="#6e3b2a" stroke-width="1.4"/>'


def virus(x, y):
    return f'<circle cx="{x}" cy="{y}" r="2" fill="#2f3b40"/>'


def z04_p35():
    p = Plate('Z04-P35', 'Absolute versus nominal filter pores for parasite cysts',
              'Membrane cross-sections with water flowing left to right. Left: a filter rated absolute 1 micron or '
              'smaller has no hole larger than its rating, so parasite cysts stay on the raw side; tiny viruses still '
              'pass, so disinfection is needed when viruses are a risk. The label should state absolute 1 micron or '
              'smaller, or NSF/ANSI 53 or 58 certification for cyst reduction or removal. Right: a nominal 1-micron '
              'filter rates the average hole; some holes are larger and let cysts through. Below: routine chlorine or '
              'iodine alone does not reliably kill Cryptosporidium. Conceptual, not to scale.')
    p.panel(24, 46, 420, 234, 'ok', '✓ ABSOLUTE 1 µm OR SMALLER')
    p.panel(456, 46, 420, 234, 'bad', '✕ NOMINAL 1 µm (AN AVERAGE)')
    pores = [12, 30, 48, 66, 84, 102, 120]
    for x0, big in ((24, ()), (456, (48, 102))):
        mx = x0 + 200
        p.add(f'<rect x="{x0 + 18}" y="84" width="{182}" height="140" fill="{WATER}" fill-opacity=".35"/>'
              f'<rect x="{mx + 14}" y="84" width="{186}" height="140" fill="{WATER}" fill-opacity=".18"/>')
        p.add(membrane(mx, 84, 140, pores, big))
        for (cx, cy) in ((x0 + 60, 110), (x0 + 120, 150), (x0 + 80, 190), (x0 + 160, 120)):
            p.add(cyst(cx, cy))
        for (vx, vy) in ((x0 + 50, 140), (x0 + 140, 100), (x0 + 250, 120), (x0 + 300, 180), (x0 + 360, 140)):
            p.add(virus(vx, vy))
        p.arrow(f'M{x0 + 30} 216H{x0 + 380}', 'flow', 2.5)
    p.add(cyst(456 + 270, 136) + cyst(456 + 320, 190))
    p.arrow('M676 134L716 136', 'reverse', 2.5)
    p.lines(40, 248, ['cysts stay on the raw side;', 'viruses pass: disinfect too'], 'tiny')
    p.lines(472, 248, ['larger holes let some cysts through;', 'viruses pass as well'], 'tiny')
    p.panel(24, 290, 852, 46, 'bad')
    p.lines(40, 319, ['✕ routine chlorine or iodine alone does not reliably kill Cryptosporidium'], 'tiny warn')
    p.band('No cyst claim on the label, or seal or freeze damage: boil instead or use a known safe supply.')
    return p.svg()


# ---------------------------------------------------------------- Z04-P45
def z04_p45():
    p = Plate('Z04-P45', 'Clean and sanitize a water storage container',
              'Four steps. Wash the container with soap and rinse it completely. Sanitize with 1 teaspoon of '
              'unscented 5 to 9 percent bleach in 1 quart of water: cap and shake so the solution touches every inside '
              'surface. Wait at least 30 seconds, pour the solution out and let the empty container air-dry. Fill with '
              'safe water, cap and label it drinking water with the date, and replace the water every six months. '
              'Containers that held toxic chemicals are never used. Conceptual, not to scale.')
    steps = [('1 WASH', ['soap, then rinse', 'completely']),
             ('2 SANITIZE', ['1 tsp bleach per', 'quart; cap, shake', 'over all surfaces']),
             ('3 EMPTY, DRY', ['wait 30 s or more,', 'pour out, air-dry']),
             ('4 FILL, LABEL', ['safe water; label', 'drinking water + date'])]
    for i, (title, rows) in enumerate(steps):
        x = 24 + i * 214
        p.panel(x, 46, 200, 290, 'ok', title)
        p.lines(x + 14, 272, rows, 'tiny')
    p.add(jug(80, 112, 104, None) + '<circle cx="132" cy="104" r="7" fill="#ffffff" stroke="#9aa59c"/>'
          '<circle cx="150" cy="96" r="5" fill="#ffffff" stroke="#9aa59c"/><circle cx="146" cy="112" r="4" fill="#ffffff" stroke="#9aa59c"/>')
    p.add(jug(296, 112, 104, None, '#eef5f8'))
    p.add('<path d="M268 140q-10 30 0 60M380 140q10 30 0 60" fill="none" stroke="#4c5d55" stroke-width="2.4"/>')
    p.add('<path d="M330 100h28l-4 8h-20z" fill="#f2f2f2" stroke="#183a30" stroke-width="1.4"/>')
    p.add(f'<g transform="rotate(180 552 170)">{jug(520, 118, 104, None, "#f4f6f7")}</g>')
    p.add('<path d="M552 230v20" stroke="#3d7186" stroke-width="2.4" stroke-dasharray="3 4"/>')
    p.add(timer(620, 108, 16))
    p.add(jug(724, 112, 104, None, '#cfe6ef'))
    p.add('<rect x="732" y="164" width="48" height="30" rx="3" fill="#ffffff" stroke="#183a30" stroke-width="1.4"/>'
          '<path d="M738 176h36M738 186h24" stroke="#4c5d55" stroke-width="2"/>')
    p.band('Chemical odour, cracks, damaged gaskets or unknown history: discard the container.')
    return p.svg()


# ---------------------------------------------------------------- Z04-P49
def z04_p49():
    p = Plate('Z04-P49', 'Raw, waiting and clean water zones kept apart',
              'Three separated zones with one-way flow from left to right. Raw: collection bag, scoop and pre-filter '
              'marked with red tape stay here. Waiting: each disinfecting batch carries a tag with its finish time and '
              'a marked lid. Clean: sealed, labelled drinking water, cups and cooking pots. A raw scoop never crosses '
              'into the clean zone. If a vessel\'s status is uncertain or raw water touches a clean rim, the whole '
              'vessel goes back to raw. Conceptual, not to scale.')
    p.panel(24, 46, 270, 290, 'bad', 'RAW')
    p.panel(310, 46, 270, 290, 'neutral', 'WAITING')
    p.panel(596, 46, 280, 290, 'ok', 'CLEAN')
    # raw gear
    p.add(f'<path d="M52 120q30-14 60 0v80q-30 12-60 0z" fill="{MUD}" fill-opacity=".8" stroke="{INK}" stroke-width="2"/>'
          f'<rect x="52" y="130" width="60" height="10" fill="{REVERSE}"/>')
    p.add('<path d="M150 150h50v26h-50z" fill="#c9cdd0" stroke="#183a30" stroke-width="2"/><path d="M200 160h44" stroke="#183a30" stroke-width="5"/>'
          f'<rect x="150" y="150" width="50" height="8" fill="{REVERSE}"/>')
    p.add('<path d="M160 196h44l-14 22h-16z" fill="#e8eef0" stroke="#183a30" stroke-width="1.8"/>'
          '<path d="M176 218v10h12v-10" fill="none" stroke="#183a30" stroke-width="1.8"/>'
          f'<rect x="160" y="196" width="44" height="6" fill="{REVERSE}"/>')
    p.lines(40, 250, ['raw bag, scoop and', 'pre-filter stay here'], 'tiny')
    # waiting
    for k, t in enumerate(('14:30', '15:10')):
        x = 340 + k * 110
        p.add(bottle(x, 110, 80, '#eef2f3'))
        p.add(f'<rect x="{x - 4}" y="106" width="42" height="8" fill="#f2c94c"/>')
        p.add(f'<path d="M{x + 34} 140l20 10" stroke="#183a30" stroke-width="1.4"/>'
              f'<rect x="{x + 50}" y="140" width="50" height="24" rx="3" fill="#ffffff" stroke="#183a30" stroke-width="1.4"/>'
              f'<text x="{x + 75}" y="157" class="tiny" text-anchor="middle" font-size="12">{t}</text>')
    p.lines(326, 250, ['tag each batch with', 'its finish time'], 'tiny')
    # clean
    for k in range(3):
        p.add(bottle(620 + k * 46, 116, 76, '#cfe6ef'))
    p.add('<path d="M780 160h56l-6 34h-44z" fill="#ffffff" stroke="#183a30" stroke-width="2"/>')
    p.lines(612, 250, ['sealed, labelled', 'drinking water'], 'tiny')
    # one-way flow and the forbidden crossing
    p.arrow('M232 92H352', 'flow', 3)
    p.arrow('M520 92H640', 'flow', 3)
    p.add('<path d="M246 300Q420 270 640 300" fill="none" stroke="#8b3825" stroke-width="2.6" stroke-dasharray="7 5"/>')
    p.add(cross(440, 282, 11))
    p.lines(326, 324, ['raw scoop never enters CLEAN'], 'tiny warn')
    p.band('Status uncertain, or raw water touched a clean rim: treat the whole vessel as raw again.')
    return p.svg()


PLATES = {'Z04-P42': z04_p42, 'Z04-P39': z04_p39, 'Z04-P40': z04_p40, 'Z04-P35': z04_p35,
          'Z04-P45': z04_p45, 'Z04-P49': z04_p49}


def checks():
    from xml.etree import ElementTree
    ns = '{http://www.w3.org/2000/svg}'
    out = {}
    p42 = z04_p42()
    order = [p42.index(s) for s in ('1 CLARIFY', '2 FILTER', '3 DISINFECT')]
    out['Z04-P42'] = dict(barrier_order=order == sorted(order), viruses_note='do not remove viruses' in p42)
    root = ElementTree.fromstring(z04_p39())
    drops = sorted(int(e.get('data-drops')) for e in root.iter(ns + 'text') if e.get('data-drops'))
    out['Z04-P39'] = dict(tables_shown=drops == [6, 8], one_table_rule='ONE complete table' in z04_p39(),
                          thirty_minutes='30 min' in z04_p39())
    p40 = z04_p40()
    out['Z04-P40'] = dict(no_invented_times='hour' not in p40 and ' min<' not in p40.replace('30 min', ''),
                          label_governs='LABEL' in p40)
    p35 = z04_p35()
    out['Z04-P35'] = dict(absolute_ok='ABSOLUTE 1 µm' in p35, nominal_bad='NOMINAL' in p35, chlorine_limit='Cryptosporidium' in p35)
    p45 = z04_p45()
    out['Z04-P45'] = dict(no_rinse_after_sanitizing='rinse' not in p45.split('2 SANITIZE')[1], air_dry='air-dry' in p45,
                          thirty_seconds='30 s' in p45)
    p49 = z04_p49()
    out['Z04-P49'] = dict(three_zones=all(z in p49 for z in ('>RAW<', '>WAITING<', '>CLEAN<')), finish_time='finish time' in p49)
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
    print(f'{len(PLATES)} batch W2C-B07 plate(s) built; checks {result}')


if __name__ == '__main__':
    main()
