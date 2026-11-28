# RT01 implementation outcomes

**Publication: HOLD. No qualified human approval was added.**

The RT01 adversarial review (draft PR #12, `review/astra-rt01-adversarial-20261127` at `1adab90`) examined `84967d7` and recorded 11 findings. This record appends what was implemented on `review/opus-wave-2c-production-20261125`; the review itself is unchanged on its own branch. Before/after wording, source sections and receipts are in [RT01_IMPLEMENTATION.json](RT01_IMPLEMENTATION.json). Rerun the receipts with `python scripts/check_rt01.py`.

An *implemented editorial candidate* is a source-checked correction inspected by an AI reviewer. It is not a clinical, food-safety, navigation or other qualified approval; every named specialist review remains pending.

| ID | Pages | Outcome | Acceptance receipt | Remaining owner |
|---|---|---|---|---|
| RT01-01 | Z11-P63 | implemented editorial candidate: The six-item report became a prepared aid; the call comes first and leads with location; a W2C plate replaces the generic exploded template. | call-first wording on card, figure description, labels and alt; T17 cited | Emergency dispatch and search and rescue (H09, H11, H18) |
| RT01-02 | Z10-P06 | implemented editorial candidate: Continuous watching of an unstable patient separated from timed documentation in prose, figure spec, SVG description and alt; the 15-minute interval removed and no replacement interval invented. | no fixed interval in prose, spec, SVG or alt; continuous watching separated from logging | Wilderness EMS and clinical documentation (H11, H18) |
| RT01-03 | Z10-P26 | implemented editorial candidate: Generated figure labels, hazard bar, stage labels, caption and alt now carry the qualified electrical isolation condition and the label/SDS/Poison Control boundary; explicit repair item added for a clinical reconstruction. | figure labels, alt and caption carry the isolation and label/SDS/Poison Control limits; repair item queued | Burn care, occupational safety, and toxicology (H18) |
| RT01-04 | Z04-P51, Z14-P74 | implemented editorial candidate: Infant formula removed from the generic safe-water list and given its own action (ready-to-feed safest; powder not sterile; chemical advisory needs bottled water or ready-to-feed) with a (see Z14-P74) link; W2C plate draws formula in its own panel. | formula separated with P26/P36, powder and chemical limits, working link in the full offline edition | Pediatrics and public health |
| RT01-05 | Z13-P49, Z13-P50 | implemented editorial candidate: Sanitizer equivalence after toilet, diaper or vomit tasks removed from both cards, captions, stage labels and figures; sanitizer kept as an interim fallback only when soap and water are truly unavailable; U13 recorded as narrowed (W2C-E035). | soap and water after waste tasks on both cards and plates; sanitizer only as a fallback | Environmental health and sanitation specialist |
| RT01-06 | Z15-P18, Z15-P22, Z15-P02, Z15-P23, Z14-P55, Z14-P56, Z14-P57, Z14-P53, Z14-P48 | control implemented proofs rebuilt: Print receipts now record per-card source-input fingerprints (printed body plus figure bytes) and a print-style digest; check_foundations fails on any stale proof unless PROOF-CURRENCY.json withholds it with exactly the changed pages, and packaged zone and reconstruction proofs can never be withheld. All 37 tagged proofs were reprinted at milestone M2. | proof currency gate passes; 36 printed sheets (9 RT01-06 pages, zone and consolidated, Letter and A4) show a current-only figure label and none of the superseded labels | Production owner |
| RT01-07 | Z14-P41 | implemented editorial candidate: Refrigerator and freezer paths drawn separately; each food goes to its chart row; ice cream and frozen yogurt discard in both columns; card action, stage labels, caption and alt corrected. | separate refrigerator and freezer paths; ice cream and frozen yogurt discard in both columns; F08 cited | Food safety and public health |
| RT01-08 | Z11-P32, Z11-P33 | implemented editorial candidate: Exact-return wording replaced by an approximate paced return confirmed on the map in the card, caption, stage labels and the A04-accepted V02 plate (revised through W2C custody with a recorded supersession basis); Z11-P33 cites the pacing limits. | approximate paced return on card, plate, description and alt; N15 cited | Navigation and outdoor education |
| RT01-09 | Z11-R05 | control implemented: The compass check measures needle and orienting-arrow bearings from the drawn polygons after every transform (pivot to tip) and requires data-bearing merely to agree; it also checks the delivered reader figure. | delivered plate passes; 90-degree visible-needle mutation with unchanged data-bearing fails | Production owner; navigation reviewer for the plate |
| RT01-10 | Z04-P01, Z13-P20, Z12-P56 | control implemented: The safety linter covers actions, verify, stop, stage labels (alt text of generated figures), captions and delivered figure text, ties negation to the instruction it governs, and has RT01's eight fixtures as unit tests. | 7 unsafe fixtures rejected (2 positive controls and 5 previously accepted variants), safe negation accepted | Production owner |
| RT01-11 | Z09-P14, Z09-P15, Z16-P43 | control implemented: Evidence panels show the current A04/W2C assessment of each cited claim (evidence/assessments.tsv, derived by scripts/w2c_assessments.py); K09's escalated decision reaches all 25 citing cards and the offline zone packages. | K09 limitation shown on all 25 citing panels, in the Z09 package and on atlas card Z16-P43 | Production owner; rigging specialist for K09 |

## Sources read for the corrections

- RT01-01 · T17 · https://cpr.heart.org/en/resuscitation-science/2024-first-aid-guidelines · 4.2 General Approach; 4.3 Calling for Help · accessed 2026-11-28
- RT01-01 · T06 · https://home.nps.gov/articles/gtgemergencyplan.htm · If you get lost or hurt; call for help · accessed 2026-11-24 (existing claim)
- RT01-02 · M31 · https://www.redcross.org/take-a-class/resources/learn-first-aid/unresponsive-and-breathing-person · General Care (continue checking; watch for changes in breathing and responsiveness) · accessed 2026-11-28 via Internet Archive capture 20261029053523; live page refused automated access
- RT01-02 · M22 · https://cpr.heart.org/en/resuscitation-science/2024-first-aid-guidelines · 5.1 Positioning, recommendations 2-3 and supportive text · accessed 2026-11-28
- RT01-03 · M32 · https://cpr.heart.org/en/resuscitation-science/2024-first-aid-guidelines · 8.2 Chemical Exposure to the Skin, recommendations 1-6 and supportive text 3, 5, 6 · accessed 2026-11-28
- RT01-04 · P26 · https://www.cdc.gov/infant-feeding-emergencies-toolkit/php/powdered-infant-formula.html · Ready-to-feed preference; Important: powder is not sterile · accessed 2026-11-28 (page updated 2026-08-10)
- RT01-04 · P36 · https://www.cdc.gov/infant-toddler-nutrition/formula-feeding/preparation-and-storage.html · Extra precautions for some infants; Preparing formula during emergencies · accessed 2026-11-28 (page dated 2026-05-14)
- RT01-05 · U26 · https://www.cdc.gov/norovirus/prevention/index.html · Wash your hands well; Key points · accessed 2026-11-28 (page dated 2025-01-13)
- RT01-05 · U27 · https://www.cdc.gov/clean-hands/about/hand-sanitizer.html · Key points; Keep in mind · accessed 2026-11-28 (page dated 2024-03-12)
- RT01-07 · F08 · https://www.foodsafety.gov/food-safety-charts/food-safety-during-power-outage · Frozen Food and Power Outages chart rows (Ice cream, frozen yogurt: Discard / Discard) · accessed 2026-11-28 via Internet Archive capture 20261105024130 (last reviewed 2024-08-08); live page refused automated access
- RT01-08 · N15 · https://content.ces.ncsu.edu/using-a-compass-and-pacing · Pacing, final two paragraphs (reviewed 2024-02-29) · accessed 2026-11-28

## Separate follow-ups

- **RT01-C01** (open specialist question): Early clinician consultation branch after a potentially high-risk tick bite (Z10-P58): routed to the clinical reviewer; no change made.
- **RT01-C02** (open): Offline figure enlargement route and a real-phone diagram-reading task: not implemented in this commit.
- **RT01-C03** (implemented editorial candidate, W2C-B07): Z14-P52 keeps at least 1 inch of water over the jar tops, and at least 2 inches when the process time at the canner altitude is over 30 minutes; new claim P38 cites USDA Complete Guide, Guide 1 page 1-18, steps 4-9.

## Related changes found while implementing

- The W2C label audit found panel-edge defects in the accepted B02 plates Z13-P44 and Z13-P41; both were fixed and B02 QA re-run.
- The uncommitted B06 draft repeated the RT01-07 shortcut on Z14-P41 and depicted two unsourced dry-ice and snow details; the committed B06 plates follow the cited sources and the unsourced clauses are flagged (W2C-E041, W2C-E042).
- P17 cites a FoodSafety.gov page that no longer carries its thermometer, ice and ventilation statements (W2C-E038); Z14-P39 and Z14-P40 now cite FDA, CDC and New York State Department of Health pages for them.
