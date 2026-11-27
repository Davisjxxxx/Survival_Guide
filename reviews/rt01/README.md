# RT01: adversarial review of the paused Opus checkpoint

**Publication: HOLD. No qualified human approval was added.**

This review records **11 concrete content or control findings: six high and five medium**, plus three separate coverage/usability follow-ups. Proposed remedies are unimplemented. The review adds documentation and reproducible probes; it does not change the encyclopedia's manuscripts, figures, historical audits, source approvals or production packages.

## Checkpoint and scope

The inspected source is [PR #11](https://github.com/Davisjxxxx/Survival_Guide/pull/11), pinned at [`84967d7`](https://github.com/Davisjxxxx/Survival_Guide/commit/84967d75af91bbf0d2cb36c54394dcf67f2104a5). The production ledger contains **22 provisional plates in five batches and 353 queued items out of 375**, although the PR description still mentions eight completed plates. The canonical input parses as 1,016 cards in 16 zones, 353 claim records and 273 source records. These are inventory counts, not completion or safety certifications. The 25 existing specialist records remain pending. Uncommitted work on the Opus source machine was not available.

Three parallel AI review briefs covered medical/exposure decisions; water, utilities and food; and mechanics/navigation. The root checked source propagation, print/package consistency and automated guard behavior, and adjudicated the findings. A skeptical second reading narrowed the medical conclusions and moved the tick-bite suggestion out of the confirmed-defect count. These are separate review tasks, not independent licensed experts or a substitute for qualified human review.

| Track | Coverage actually performed | Limit |
|---|---|---|
| Medical/exposure | 80 Z10 texts, 19 selected Z12 texts and Z11-P63 screened; three current figure rasters inspected | Targeted primary-source verification for findings only |
| Water/utilities/food | 224 headings screened; 65 full card texts read; four figure rasters inspected; all 26 W2C evidence rows read | Fire coverage was selective; no complete water/food corpus certification |
| Mechanics/navigation | 32 selected full card texts; three current W2C plate revisions and retained phone/desktop captures | No physical knots, load test or navigation exercise |
| Root controls/delivery | All canonical input records parsed; 22 W2C print headers compared; focused source panels, PDFs, ZIP members and mutation probes checked | No fresh full browser, axe, PDF/UA, real-device or field validation |

Exact page lists and methods are in [COVERAGE.json](COVERAGE.json). The review tested plausible misuse: a reader opening only one card, following a figure without the prose, losing signal, selecting the wrong population or food category, or printing an older derivative from a current package. No participant was exposed to a real hazard.

## Ranked findings

Severity describes the consequence of the identified failure if the draft were relied on. It does not claim an observed injury or authorize field use. High findings need correction before the next broadly circulated owner-review package; medium findings improve bounded correctness and the controls that prevent recurrence.

| ID | Severity | Pages / surface | Finding |
|---|---|---|---|
| RT01-01 | High | Z11-P63 | Emergency-call checklist is an unintended activation gate |
| RT01-02 | High | Z10-P06 | Timed patient logs can be mistaken for ongoing observation |
| RT01-03 | High | Z10-P26 | Chemical/electrical figure drops substance-specific and qualified-isolation conditions |
| RT01-04 | High | Z04-P51, Z14-P74 | Water-use card omits the infant-specific powder-preparation boundary already required by its evidence record |
| RT01-05 | High | Z13-P49, Z13-P50 | Emergency sanitation permits sanitizer as an equivalent after waste handling, including the norovirus scenario it is meant to prevent |
| RT01-06 | High | Z15-P18, Z15-P22, Z15-P02, Z15-P23, Z14-P55, Z14-P56, Z14-P57, Z14-P53, Z14-P48 | Current zone packages contain superseded print instructions beside the corrected reader |
| RT01-07 | Medium | Z14-P41 | Frozen-food figure and alt retain the blanket refreeze shortcut that A02 removed from the prose |
| RT01-08 | Medium | Z11-P32, Z11-P33 | Equal pace counts are presented as an exact return to the original line |
| RT01-09 | Medium | Z11-R05 | Compass geometry validator trusts descriptive bearing metadata for the drawn needle and arrow |
| RT01-10 | Medium | Z04-P01, Z13-P20, Z12-P56 | Safety linter omits figure language and can misapply unrelated negations |
| RT01-11 | Medium | Z09-P14, Z09-P15, Z16-P43 | Adverse evidence decisions do not propagate to the reader's evidence panels |

## Findings and acceptance conditions

### RT01-01: Emergency-call checklist is an unintended activation gate

**Severity:** High. **Status:** Open, remedy proposed. **Pages:** Z11-P63.

**Evidence location:** [foundations/manuscripts/11-p10-z11-navigation.cards](https://github.com/Davisjxxxx/Survival_Guide/blob/84967d75af91bbf0d2cb36c54394dcf67f2104a5/foundations/manuscripts/11-p10-z11-navigation.cards) (lines [841, 853]); [foundations/reader/visuals/Z11-P63.svg](https://github.com/Davisjxxxx/Survival_Guide/blob/84967d75af91bbf0d2cb36c54394dcf67f2104a5/foundations/reader/visuals/Z11-P63.svg).

**Scenario.** Bystander with working phone completes six written items and rehearses before calling for an unconscious or severely bleeding companion.

**Failure mechanism.** Administrative preparation is made a precondition to emergency activation.

**Proposed correction.** Convert report to pre-trip/on-call checklist; preserve immediate life-threat activation and best-known-location-first without waiting for complete notes.

**Acceptance conditions.**

- With life-threatening signs and missing coordinate datum, reader activates help and relevant immediate care instead of completing a form.

**Existing work.** Navigation agent identified it; P63 is queued P2 drawing, no prior targeted delay finding found.

**Sources.**

- [https://cpr.heart.org/en/resuscitation-science/2024-first-aid-guidelines](https://cpr.heart.org/en/resuscitation-science/2024-first-aid-guidelines): Sections 4.2 General Approach, 4.3 Calling for Help, and 5.1 recommendation 2.

**Review dependency.** H09, H11, H18

### RT01-02: Timed patient logs can be mistaken for ongoing observation

**Severity:** High. **Status:** Open, remedy proposed. **Pages:** Z10-P06.

**Evidence location:** [foundations/manuscripts/13-p12-z10-medicine.cards](https://github.com/Davisjxxxx/Survival_Guide/blob/84967d75af91bbf0d2cb36c54394dcf67f2104a5/foundations/manuscripts/13-p12-z10-medicine.cards) (lines [71, 83]); [foundations/reader/visuals/Z10-P06.svg](https://github.com/Davisjxxxx/Survival_Guide/blob/84967d75af91bbf0d2cb36c54394dcf67f2104a5/foundations/reader/visuals/Z10-P06.svg).

**Scenario.** Caregiver follows only P06, sets a 15-minute timer, and misses worsening breathing during shelter tasks.

**Failure mechanism.** Conflates continuous life-threat observation with periodic written reassessment.

**Counterevidence and limits.** The card says initial stabilization comes first and requires immediate escalation when deterioration is noticed. It never literally instructs a caregiver to leave the patient. The problem is that checking and logging are combined into an unsupported fixed schedule without an explicit ongoing-observation distinction.

**Proposed correction.** Remove unsupported universal observation intervals; distinguish ongoing monitoring from documentation and retain qualified EMS timing review.

**Acceptance conditions.**

- An unstable-patient single-card exercise must not yield an unattended 15-minute interval; align prose, SVG, description, reader and print with P10/P30.

**Existing work.** Concrete defect under existing OPEN M20; A04/W2C QUEUED geometry item. Not a newly cleared evidence claim.

**Sources.**

- [https://www.redcross.org/take-a-class/resources/learn-first-aid/unresponsive-and-breathing-person](https://www.redcross.org/take-a-class/resources/learn-first-aid/unresponsive-and-breathing-person): General Care, items 3 and 7.
- [https://cpr.heart.org/en/resuscitation-science/2024-first-aid-guidelines](https://cpr.heart.org/en/resuscitation-science/2024-first-aid-guidelines): 5.1 recommendations 2–3 and supportive text 3.

**Review dependency.** H11, H18

### RT01-03: Chemical/electrical figure drops substance-specific and qualified-isolation conditions

**Severity:** High. **Status:** Open, remedy proposed. **Pages:** Z10-P26.

**Evidence location:** [foundations/manuscripts/13-p12-z10-medicine.cards](https://github.com/Davisjxxxx/Survival_Guide/blob/84967d75af91bbf0d2cb36c54394dcf67f2104a5/foundations/manuscripts/13-p12-z10-medicine.cards) (lines [351, 363]); [foundations/reader/visuals/Z10-P26.svg](https://github.com/Davisjxxxx/Survival_Guide/blob/84967d75af91bbf0d2cb36c54394dcf67f2104a5/foundations/reader/visuals/Z10-P26.svg).

**Scenario.** Reader follows figure alone for an unfamiliar chemical spill or energized injury.

**Failure mechanism.** Visible generic brush/20-minute-flush/shutdown route lacks the corrected body’s substance-specific and isolation conditions.

**Counterevidence and limits.** The body is substantially more cautious and the figure says never to touch an energized victim. Dry brushing and prompt irrigation are not intrinsically wrong: AHA/Red Cross supports them within stated conditions. The defect is loss of those conditions, not a claim that a 20-minute rinse itself is always unsafe.

**Proposed correction.** Align figure, accessible description and source fields with qualified isolation and chemical-specific care boundaries.

**Acceptance conditions.**

- Read visual alone for ordinary liquid, unknown/water-reactive material, and energized victim; no contradiction with corrected body allowed.

**Existing work.** Residual A02-04 prose correction; active visual provisionally retained and outside 375 technical items. A04 did not clear this plate.

**Sources.**

- [https://cpr.heart.org/en/resuscitation-science/2024-first-aid-guidelines](https://cpr.heart.org/en/resuscitation-science/2024-first-aid-guidelines): 8.2 Chemical Exposure to the Skin, recommendations 1–6 and supportive text 3,5,6.

**Review dependency.** H18

### RT01-04: Water-use card omits the infant-specific powder-preparation boundary already required by its evidence record

**Severity:** High. **Status:** Open, remedy proposed. **Pages:** Z04-P51, Z14-P74.

**Evidence location:** [foundations/manuscripts/07-f06-z04-water.cards](https://github.com/Davisjxxxx/Survival_Guide/blob/84967d75af91bbf0d2cb36c54394dcf67f2104a5/foundations/manuscripts/07-f06-z04-water.cards) (lines [533, 545]); [foundations/evidence/claims.tsv](https://github.com/Davisjxxxx/Survival_Guide/blob/84967d75af91bbf0d2cb36c54394dcf67f2104a5/foundations/evidence/claims.tsv) (lines [30, 30]); [foundations/evidence/claims.tsv](https://github.com/Davisjxxxx/Survival_Guide/blob/84967d75af91bbf0d2cb36c54394dcf67f2104a5/foundations/evidence/claims.tsv) (lines [248, 248]); [foundations/manuscripts/15-p14-z14-preservation.cards](https://github.com/Davisjxxxx/Survival_Guide/blob/84967d75af91bbf0d2cb36c54394dcf67f2104a5/foundations/manuscripts/15-p14-z14-preservation.cards) (lines [1013, 1013]); [foundations/reader/Z04-P51.html](https://github.com/Davisjxxxx/Survival_Guide/blob/84967d75af91bbf0d2cb36c54394dcf67f2104a5/foundations/reader/Z04-P51.html) (lines [1, 1]).

**Scenario.** A caregiver with a three-week-old, premature or immunocompromised infant opens only the water chapter during an outage. They use bottled water, or fully cool previously boiled water before mixing powder, and infer from the card that verified potable water completes the relevant feeding safety check.

**Failure mechanism.** The task-specific action and verification collapse water safety and powder safety. The card routes ready-to-feed formula only through inability to secure safe water. It has no age, prematurity or immune-status branch, although W29 explicitly requires the separate P26 conditions and the food chapter already has that branch. “Boiled-and-cooled” does not specify cooling before mixing versus cooling after mixing and can be read as room-temperature preparation. This finding does not assert that room-temperature preparation is unsafe for every infant.

**Counterevidence and limits.** The card correctly rejects prohibited advisory water, its evidence notes contain the P26 limitation, and Z14-P74 has an appropriate warning. These are useful controls but are not propagated into the operational action/figure or an offline cross-link where formula is named.

**Proposed correction.** Remove formula from the undifferentiated bottled/boiled-and-cooled task list. Add a concise infant-feeding branch that prioritizes ready-to-feed during outages and explicitly routes vulnerable-infant powdered preparation to Z14-P74/P26 and current applicable clinical/public-health instructions. Preserve safe-source and chemical-advisory rules. Distinguish preparation temperature from cooling before feeding; do not invent a new universal recipe.

**Acceptance conditions.**

- Read only Z04-P51 text and its figure/alt: a caregiver must see that safe water alone does not address nonsterile powder.
- Test three-week-old, premature, immunocompromised and healthy older-infant scenarios; do not force one universal preparation instruction across them.
- With networking disabled, the formula branch must link to the correct infant-specific card and P26 boundary.
- Retain rejection of chemically contaminated water; boiling must not be presented as resolving that boundary.

**Existing work.** Residual propagation gap after A02. P26 explicitly says it was added in A02 to separate a consequential source boundary. This is not a new discovery of that underlying risk and is not closure of a specialist hold.

**Sources.**

- [CDC — Infant Formula Preparation and Storage](https://www.cdc.gov/infant-toddler-nutrition/formula-feeding/preparation-and-storage.html): Different recommendations for preparing powdered formula; Extra precautions for some infants; Preparing formula during emergencies (retrieval lines 66–107).

**Review dependency.** Pediatrics/public health (P26 owner; cross-zone H18 and H17 applicability), drinking-water public health (H02/H03 where applicable), and H25 cross-zone fidelity. All remain pending.

### RT01-05: Emergency sanitation permits sanitizer as an equivalent after waste handling, including the norovirus scenario it is meant to prevent

**Severity:** High. **Status:** Open, remedy proposed. **Pages:** Z13-P49, Z13-P50.

**Evidence location:** [foundations/manuscripts/14-p13-z13-utilities.cards](https://github.com/Davisjxxxx/Survival_Guide/blob/84967d75af91bbf0d2cb36c54394dcf67f2104a5/foundations/manuscripts/14-p13-z13-utilities.cards) (lines [664, 664]); [foundations/manuscripts/14-p13-z13-utilities.cards](https://github.com/Davisjxxxx/Survival_Guide/blob/84967d75af91bbf0d2cb36c54394dcf67f2104a5/foundations/manuscripts/14-p13-z13-utilities.cards) (lines [678, 683]); [foundations/manuscripts/14-p13-z13-utilities.cards](https://github.com/Davisjxxxx/Survival_Guide/blob/84967d75af91bbf0d2cb36c54394dcf67f2104a5/foundations/manuscripts/14-p13-z13-utilities.cards) (lines [680, 680]); [foundations/evidence/claims.tsv](https://github.com/Davisjxxxx/Survival_Guide/blob/84967d75af91bbf0d2cb36c54394dcf67f2104a5/foundations/evidence/claims.tsv) (lines [188, 188]); [foundations/reader/visuals/Z13-P50.svg](https://github.com/Davisjxxxx/Survival_Guide/blob/84967d75af91bbf0d2cb36c54394dcf67f2104a5/foundations/reader/visuals/Z13-P50.svg) (lines [10, 11]).

**Scenario.** A water-rationed household with vomiting/diarrhea uses bucket toilets. After handling waste or changing a diaper, hands look clean. To conserve the available wash water, the caregiver selects the explicitly permitted alcohol-rub alternative and then handles food.

**Failure mechanism.** Visual cleanliness is treated as sufficient to choose sanitizer. That condition does not address norovirus or other sanitizer-resistant fecal–oral pathogens. The instruction makes a fallback equivalent to the principal control while the card explicitly names norovirus as the failure to prevent. A same-card soap instruction does not remove the conflicting “or” and “conserve water” permissions.

**Counterevidence and limits.** Z13-P49 and P50 both require a soap-and-water station; P50 recommends washing after waste tasks and the diagram calls sanitizer an aid. CDC also supports ≥60% alcohol sanitizer when soap and water truly are unavailable. The correction must retain that legitimate fallback and must not tell the reader to do nothing.

**Proposed correction.** Reserve soap and safe water for toilet/diaper and feces/vomit cleanup tasks and before food preparation. State that sanitizer is not a substitute for this control when norovirus is possible. Where soap and water are genuinely unavailable, describe alcohol sanitizer as an interim, incomplete fallback followed by soap-and-water washing as soon as possible; do not present routine conservation alone as the trigger for replacement. Update U13 and both figures/alt text so the same boundary appears at every point of use.

**Acceptance conditions.**

- Clean-looking hands after bucket-toilet use or a diaper change must not route directly to sanitizer-only clearance for food handling.
- A vomiting/diarrhea household scenario must select soap-and-water washing even when no visible residue is present.
- A true no-soap/no-water scenario must still provide the CDC fallback without implying equivalent norovirus control.
- Compare action, verification, image text, alt/desc and U13: none should reintroduce a generic visible-dirt-only decision.

**Existing work.** Newly localized application gap within the already pending U13/environmental-health scope. Targeted searches of A02/A03/A04 and W2C did not locate an explicit norovirus/sanitizer finding. This is not a claim of exhaustive duplicate clearance across every historical record.

**Sources.**

- [CDC — How to Prevent Norovirus](https://www.cdc.gov/norovirus/prevention/index.html): Wash your hands well; Be aware that (retrieval lines 46–57).
- [CDC — Hand Sanitizer Guidelines and Recommendations](https://www.cdc.gov/clean-hands/about/hand-sanitizer.html): Key points and Keep in mind (retrieval lines 28–46), tips line 64.

**Review dependency.** Environmental health/public health and onsite wastewater review (U13 owner; H19 where applicable), food/public-health review H17, and infectious-disease review as needed. No hold is closed.

### RT01-06: Current zone packages contain superseded print instructions beside the corrected reader

**Severity:** High. **Status:** Open, remedy proposed. **Pages:** Z15-P18, Z15-P22, Z15-P02, Z15-P23, Z14-P55, Z14-P56, Z14-P57, Z14-P53, Z14-P48.

**Evidence location:** [foundations/proofs/encyclopedia-letter.pdf](https://github.com/Davisjxxxx/Survival_Guide/blob/84967d75af91bbf0d2cb36c54394dcf67f2104a5/foundations/proofs/encyclopedia-letter.pdf) (sheets [844, 849, 851, 852, 853, 878, 894, 898, 899]); [foundations/proofs/encyclopedia-a4.pdf](https://github.com/Davisjxxxx/Survival_Guide/blob/84967d75af91bbf0d2cb36c54394dcf67f2104a5/foundations/proofs/encyclopedia-a4.pdf) (sheets [849]); [foundations/proofs/packages/zone-Z14.zip](https://github.com/Davisjxxxx/Survival_Guide/blob/84967d75af91bbf0d2cb36c54394dcf67f2104a5/foundations/proofs/packages/zone-Z14.zip); [scripts/check_foundations.py](https://github.com/Davisjxxxx/Survival_Guide/blob/84967d75af91bbf0d2cb36c54394dcf67f2104a5/scripts/check_foundations.py) (verify_retained_pdfs; zone_package_payload); [foundations/audit/w2c/README.md](https://github.com/Davisjxxxx/Survival_Guide/blob/84967d75af91bbf0d2cb36c54394dcf67f2104a5/foundations/audit/w2c/README.md) (Proof and package refresh policy).

**Scenario.** An owner opens the current Z14 ZIP, reviews the corrected HTML, then prints the accompanying zone PDF for another reviewer. The reviewer receives the older canning figure without a page-level notice that the reader now supersedes it.

**Failure mechanism.** The milestone policy allows retained PDF bytes to lag the reader; the package still includes them, and the PDF receipt verifies its own older bytes without binding them to the current manuscript and figure inputs. A checksum match therefore does not establish current content. Nine B04/B05 pages have an old figure header in the consolidated Letter PDF. Z14-P53's older figure says that either an overlong process or any low-acid food routes to a deep water-bath or pressure canner; the corrected active figure explicitly excludes low-acid foods and calls for the correct tested method. The obsolete figure creates an ambiguous water-bath fallback for low-acid food, although the prose remains more cautious.

**Reproduction.** Read proof_header_comparison.json for 22 W2C plate header checks (13 current headers, 9 older headers). Confirm Z14-P53 on consolidated Letter and A4 sheet 849 and packaged Z14 Letter sheet 53. Current Z14 ZIP HTML/SVG bytes match the active reader; its PDF still has the old clause. Both consolidated PDF SHA-256 values match tagged-print-qa.json.

**Counterevidence and limits.** The W2C README openly documents milestone regeneration, and new batch-specific proofs exist. No hidden tampering, false hash, or failure of the documented byte-integrity check is alleged. This finding concerns point-of-use freshness and contradictory distributed instructions.

**Proposed correction.** Before the next owner-review package, regenerate affected consolidated and zone proofs from the pinned reader, or omit/clearly mark superseded proofs at every download and printed page until regenerated. Add a generation input digest for manuscripts, figures and print styles to PDF receipts. Distinguish a valid historical proof from a current proof. Preserve historical artifacts under explicit historical paths if required; do not silently overwrite custody records.

**Acceptance conditions.**

- For a deliberate safety-relevant source or figure change, the current-proof gate must fail or explicitly mark/exclude the stale PDF until rebuilt. Then compare Z14-P53 in current HTML, standalone Letter/A4 and consolidated Letter/A4. The source-input digest must agree across every artifact advertised as the same edition.

**Existing work.** New concrete exposure demonstrated under the existing milestone policy. Not a claim that no batch proof was made. The root compared actual committed and packaged bytes at the pinned SHA.

**Sources.**

- [https://github.com/Davisjxxxx/Survival_Guide/blob/84967d75af91bbf0d2cb36c54394dcf67f2104a5/foundations/audit/w2c/README.md](https://github.com/Davisjxxxx/Survival_Guide/blob/84967d75af91bbf0d2cb36c54394dcf67f2104a5/foundations/audit/w2c/README.md): Proof and package refresh policy.
- [https://github.com/Davisjxxxx/Survival_Guide/blob/84967d75af91bbf0d2cb36c54394dcf67f2104a5/foundations/reader/visuals/Z14-P53.svg](https://github.com/Davisjxxxx/Survival_Guide/blob/84967d75af91bbf0d2cb36c54394dcf67f2104a5/foundations/reader/visuals/Z14-P53.svg): Current no-low-acid-foods text.

**Review dependency.** Production and packaging owner; food-preservation review H17 and delivery/accessibility H14/H25 remain open.

### RT01-07: Frozen-food figure and alt retain the blanket refreeze shortcut that A02 removed from the prose

**Severity:** Medium. **Status:** Open, remedy proposed. **Pages:** Z14-P41.

**Evidence location:** [foundations/manuscripts/15-p14-z14-preservation.cards](https://github.com/Davisjxxxx/Survival_Guide/blob/84967d75af91bbf0d2cb36c54394dcf67f2104a5/foundations/manuscripts/15-p14-z14-preservation.cards) (lines [552, 552]); [foundations/manuscripts/15-p14-z14-preservation.cards](https://github.com/Davisjxxxx/Survival_Guide/blob/84967d75af91bbf0d2cb36c54394dcf67f2104a5/foundations/manuscripts/15-p14-z14-preservation.cards) (lines [557, 557]); [foundations/reader/visuals/Z14-P41.svg](https://github.com/Davisjxxxx/Survival_Guide/blob/84967d75af91bbf0d2cb36c54394dcf67f2104a5/foundations/reader/visuals/Z14-P41.svg) (lines [3, 11]); [foundations/reader/Z14-P41.html](https://github.com/Davisjxxxx/Survival_Guide/blob/84967d75af91bbf0d2cb36c54394dcf67f2104a5/foundations/reader/Z14-P41.html) (lines [1, 1]); [foundations/audit/a02/REVISED_WORDING.csv](https://github.com/Davisjxxxx/Survival_Guide/blob/84967d75af91bbf0d2cb36c54394dcf67f2104a5/foundations/audit/a02/REVISED_WORDING.csv) (lines [133, 134]).

**Scenario.** After an outage, a reader follows the diagram/alt alone for softened ice cream that still has ice crystals. The shortcut says refreeze, while the official frozen-food chart specifically directs discard for ice cream/frozen yogurt. Separately, a reader tracing arrows must pass a refrigerator question before the frozen-food question, although these are distinct storage categories.

**Failure mechanism.** A correction was applied to action prose but not to the diagram specification, SVG desc/panel or HTML alt. The positive terminal does say “per official chart,” but the prominent lower instruction remains unconditional. The decision graph also serializes refrigerator and freezer paths rather than selecting the applicable storage category first.

**Counterevidence and limits.** The equipment list requires the official printed chart, action2 correctly preserves exceptions, verification requires per-food application, and the stop rule rejects uncertain histories. This is a residual visual/alternative-text contradiction, not an assertion that the full card lacks all safe instructions.

**Proposed correction.** Remove the universal refreeze arrow from the diagram specification, SVG text/desc and HTML alt. Select refrigerator versus freezer first, then require the applicable food category and official row before a keep/refreeze decision. Keep category exceptions available offline or explicitly stop when the chart is absent. Regenerate dependent figures and packages after correction.

**Acceptance conditions.**

- Using only the diagram or its alt, compare partially softened ice cream with frozen raw meat at the same measured temperature and ice-crystal condition: the result must follow their different official chart rows.
- Refrigerator items must not have to answer a freezer/ice-crystal question; freezer items must not be gated through a refrigerator history question.
- When food category, history or offline chart is unavailable, the figure must not grant a universal keep/refreeze decision.
- Check all derivative text surfaces after generation, including SVG desc, HTML alt, visible labels and the print proof.

**Existing work.** Residual A02 correction propagation failure, specifically REVISED_WORDING.csv lines 133–134. It belongs with root’s cross-cutting caption/figure coverage finding rather than being counted as a new food-safety rule.

**Sources.**

- [FoodSafety.gov — Food Safety During Power Outage](https://www.foodsafety.gov/food-safety-charts/food-safety-during-power-outage): Frozen Food and Power Outages; Dairy, eggs row “Ice cream, frozen yogurt” (retrieval lines 96–112).

**Review dependency.** H17 food preservation/public health; H14 accessible/print delivery; H25 cross-zone fidelity. Specialist approval remains pending.

### RT01-08: Equal pace counts are presented as an exact return to the original line

**Severity:** Medium. **Status:** Open, remedy proposed. **Pages:** Z11-P32, Z11-P33.

**Evidence location:** [foundations/manuscripts/11-p10-z11-navigation.cards](https://github.com/Davisjxxxx/Survival_Guide/blob/84967d75af91bbf0d2cb36c54394dcf67f2104a5/foundations/manuscripts/11-p10-z11-navigation.cards) (407-430).

**Scenario.** A reader opens Z11-P32 alone and boxes around a compact blowdown on firm ground. The outward offset is level and open; the return crosses brush or an uphill section with a shorter horizontal stride. The reader matches the count exactly and treats the route as regained.

**Failure mechanism.** Matching step counts does not match horizontal distance when stride or slope differs. Matching the original compass bearing also does not detect a lateral offset: parallel lines have the same bearing. The card asks for terrain verification, but its exact-return objective and prescribed count can overrule that caveat in a novice reading.

**Reproduction.** Illustrative arithmetic, not measured field data: 100 double paces at 1.5 m horizontal advance offset 150 m. The return 100 at 1.2 m returns 120 m, leaving a 30 m residual despite exact count and perfect right angles. More general residual is n*(a-b).

**Proposed correction.** Change exact-return wording to approximate return; state on this card that equal paces work only as an estimate and unequal stride/slope causes residual error. Require a positively recognized terrain feature or a usable back-sight to confirm reacquisition; otherwise remain uncertain and reroute or stop. Keep the existing compact-obstacle and safe-land limits. Link P33 explicitly where useful.

**Acceptance conditions.**

- A single-card tabletop scenario with different outbound/return strides must result in unconfirmed position, never exact line regained. Confirm objective, actions, caption and atlas excerpts use the same uncertainty. A navigator reviews the amended method.

**Existing work.** New card-level mismatch with A04 observation, not a new general specialist hold. P33 already acknowledges terrain shortening, but P32 does not carry the limit on its own. No matching explicit correction found in sampled A02/A03/A04/W2C technical-findings records.

**Sources.**

- [NC State Extension, Using a Compass and Pacing](https://content.ces.ncsu.edu/using-a-compass-and-pacing): Pacing, final two paragraphs; revised 2024-02-29.
- [https://github.com/Davisjxxxx/Survival_Guide/blob/84967d75af91bbf0d2cb36c54394dcf67f2104a5/foundations/audit/a04/V01_V02_VISUAL_QUALIFICATION.csv](https://github.com/Davisjxxxx/Survival_Guide/blob/84967d75af91bbf0d2cb36c54394dcf67f2104a5/foundations/audit/a04/V01_V02_VISUAL_QUALIFICATION.csv): Z11-P32 row.

**Review dependency.** Navigation/outdoor education and SAR review remains open.

### RT01-09: Compass geometry validator trusts descriptive bearing metadata for the drawn needle and arrow

**Severity:** Medium. **Status:** Open, remedy proposed. **Pages:** Z11-R05.

**Evidence location:** [scripts/build_w2c_navigation.py](https://github.com/Davisjxxxx/Survival_Guide/blob/84967d75af91bbf0d2cb36c54394dcf67f2104a5/scripts/build_w2c_navigation.py) (225-265; 277-294).

**Scenario.** A future change to the common compass renderer rotates or otherwise distorts the actual needle or orienting-arrow polygon but leaves data-bearing annotations correct. The plate is regenerated and its geometry receipt still reports acceptance.

**Failure mechanism.** bearing_of reads data-bearing; it never derives the arrow and needle bearings from visible polygon points or applies SVG transforms. The asserted rendered-geometry check therefore partly verifies the generator’s claims about its geometry.

**Reproduction.** Scratch-only mutation: add transform=rotate(90 513.7 244.0) to compass-after-needle, keep data-bearing unchanged, call z11_r05_checks. Baseline and mutant both return accepted:true and needle_in_orienting_arrow:true. Receipt: navigation_validator_mutation.json. This is the unit geometry validator; full file-equality --check was not bypassed. A second mutation rotates the polygon point coordinates themselves by 90 degrees (no SVG transform); it also passes.

**Proposed correction.** Calculate visible vectors from polygon geometry after transforms (or emit explicit pivot/tip geometry and independently resolve it), then compare with the physical relationships. Keep metadata only as explanatory data. Add a meaningful mutation test rotating the rendered needle while preserving metadata; test mirrored/rotated orienting arrows and parent transforms as appropriate.

**Acceptance conditions.**

- The 90-degree visible-needle mutation must fail the geometry validator, while the unmodified current plate passes. The validator must compare the geometry actually delivered to the browser. Do not describe this as current bearing corruption: current rendered compass passed the bounded visual/source check.

**Existing work.** New validation blind spot. Existing A04 instructions specifically require validating drawn numerical geometry independently of labels. W2C artifact equality helps detect isolated file edits but does not validate a faulty generator that regenerates matching artifacts.

**Sources.**

- [https://github.com/Davisjxxxx/Survival_Guide/blob/84967d75af91bbf0d2cb36c54394dcf67f2104a5/scripts/build_w2c_navigation.py](https://github.com/Davisjxxxx/Survival_Guide/blob/84967d75af91bbf0d2cb36c54394dcf67f2104a5/scripts/build_w2c_navigation.py): bearing_of; z11_r05_checks; main.
- [https://www.usgs.gov/educational-resources/how-get-your-map-and-compass-face-same-direction](https://www.usgs.gov/educational-resources/how-get-your-map-and-compass-face-same-direction): Orientation steps.

**Review dependency.** Editorial QA plus cartography review; no publication or scientific approval follows from this test.

### RT01-10: Safety linter omits figure language and can misapply unrelated negations

**Severity:** Medium. **Status:** Open, remedy proposed. **Pages:** Z04-P01, Z13-P20, Z12-P56.

**Evidence location:** [scripts/build_foundations.py](https://github.com/Davisjxxxx/Survival_Guide/blob/84967d75af91bbf0d2cb36c54394dcf67f2104a5/scripts/build_foundations.py) (lint_cards: full text construction, operational clauses, combustion and rip-current rules).

**Scenario.** A production writer corrects body prose but leaves or introduces a dangerous assertion in a caption or stage label, or includes an unrelated warning near an unsafe action. The linter reports no contradiction.

**Failure mechanism.** The linter excludes diagram and visual fields from its safety text and is not a semantic checker of generated SVG/alt text. Some exceptions search for any negative word in the clause or whole card, rather than whether it negates the dangerous instruction. The full-card rip-current exception is especially broad.

**Reproduction.** Eight isolated in-memory probes: seven intentionally unsafe fixtures and one safe control. Two unsafe action controls were rejected. Five unsafe variants were accepted: two caption placements, a stage-label placement, an unrelated same-clause warning, and a rip-current action masked by existing warnings elsewhere in the card. The safe control passed. Four existing relevant regression tests also passed. No fixture was written into a manuscript or publication artifact.

**Counterevidence and limits.** These are targeted tests of lint_cards, not proof that the complete build, human review or publication gates can be bypassed. Narrow syntactic rules are useful but cannot establish overall safety.

**Proposed correction.** Run appropriate checks over all reader-visible instruction surfaces and the actual generated SVG text/description and HTML alt. Scope a negation to the instruction it governs; use targeted negative tests for unrelated warnings and alternate phrasing. Keep scenario-based human/editorial review as an additional gate rather than claiming complete semantic coverage from regex checks.

**Acceptance conditions.**

- Retain the two unsafe positive controls and safe negation control. The five accepted unsafe variants must be rejected or routed to explicit review. A future correction to a claim boundary must identify its action, caption, diagram, alt and print derivatives together.

**Existing work.** New reproduced control gap explains residual propagation defects such as Z10-P26 and Z14-P41. Those concrete content findings are separately tracked; this is the shared prevention work, not another count of the same clinical or food rule.

**Sources.**

- [https://github.com/Davisjxxxx/Survival_Guide/blob/84967d75af91bbf0d2cb36c54394dcf67f2104a5/scripts/build_foundations.py](https://github.com/Davisjxxxx/Survival_Guide/blob/84967d75af91bbf0d2cb36c54394dcf67f2104a5/scripts/build_foundations.py): lint_cards.

**Review dependency.** Production/editorial QA. Domain review and all publication holds remain separate.

### RT01-11: Adverse evidence decisions do not propagate to the reader's evidence panels

**Severity:** Medium. **Status:** Open, remedy proposed. **Pages:** Z09-P14, Z09-P15, Z16-P43.

**Evidence location:** [foundations/audit/w2c/W2C_EVIDENCE_DECISIONS.csv](https://github.com/Davisjxxxx/Survival_Guide/blob/84967d75af91bbf0d2cb36c54394dcf67f2104a5/foundations/audit/w2c/W2C_EVIDENCE_DECISIONS.csv) (W2C-E004 / K09); [foundations/evidence/claims.tsv](https://github.com/Davisjxxxx/Survival_Guide/blob/84967d75af91bbf0d2cb36c54394dcf67f2104a5/foundations/evidence/claims.tsv) (K09); [foundations/reader/Z09-P14.html](https://github.com/Davisjxxxx/Survival_Guide/blob/84967d75af91bbf0d2cb36c54394dcf67f2104a5/foundations/reader/Z09-P14.html) (#evidence / K09); [scripts/build_foundations.py](https://github.com/Davisjxxxx/Survival_Guide/blob/84967d75af91bbf0d2cb36c54394dcf67f2104a5/scripts/build_foundations.py) (load_evidence and write_card evidence rendering).

**Scenario.** A reviewer opens a newly reconstructed knot card and checks its evidence panel. The card presents K09's affirmative support and source-checked date without displaying the later W2C determination that the cited locator was not found.

**Failure mechanism.** The reader is compiled from baseline claim fields without joining the later audit dispositions. K09 is still cited by 25 current cards, including the two new knot pages and the atlas. New K14/K15 support narrows some actions but does not remove K09 from the remaining statements. The reader can appear better supported than the latest audit permits. The historical record should remain intact, but current evidence views need the current assessment.

**Reproduction.** Read W2C-E004, then the K09 entry in Z09-P14's #evidence panel. The baseline locator Cordage, Anchors and Rigging Boundaries and affirmative Support remain, with no LOCATOR_NOT_FOUND_ESCALATED label. Parsed claim references identify 25 current cards using K09. The build evidence schema has no disposition field and does not import the W2C decision register.

**Counterevidence and limits.** The entire reader says specialist review is pending and publication is on hold. A checked date is not literally an approval, and the K09 problem is already recorded as W2C-E004. This finding is the missing presentation/propagation of that known decision, not rediscovery or a new determination of rope behavior.

**Proposed correction.** Add a current assessment layer that resolves claim IDs to the latest applicable bounded, partial, unsupported or unreviewed status and links the evidence decision. Keep historical audit files immutable. Preserve disputed source text as historical assertions, not as unqualified current support. Separate the owner decision on atlas layout promotion from correction of an inaccurate source-status display; do not silently grant release approval or alter the frozen historical atlas.

**Acceptance conditions.**

- Opening any of K09's 25 card evidence panels, including offline zone packages, must expose the current limitation and unresolved status. Confirm that a bounded replacement supports only its stated claims and does not close unrelated device, specialist or historical holds.

**Existing work.** Presentation-layer propagation gap using already known W2C-E004 as the counterexample. Existing A04 and earlier unresolved counts are not reclosed or recomputed by this review.

**Sources.**

- [https://github.com/Davisjxxxx/Survival_Guide/blob/84967d75af91bbf0d2cb36c54394dcf67f2104a5/foundations/audit/w2c/W2C_EVIDENCE_DECISIONS.csv](https://github.com/Davisjxxxx/Survival_Guide/blob/84967d75af91bbf0d2cb36c54394dcf67f2104a5/foundations/audit/w2c/W2C_EVIDENCE_DECISIONS.csv): W2C-E004.

**Review dependency.** Evidence editor and rigging/materials reviewer; publication HOLD persists.

## Three separate follow-ups

These are excluded from the 11 confirmed content/control findings.

### RT01-C01: Consider an early clinician-consultation branch after a potentially high-risk tick bite

Useful conditional coverage, but existing removal and symptom-follow-up advice matches general CDC advice and does not explicitly direct waiting only for symptoms. Excluded from confirmed-defect count.

**Next step.** Add bounded early clinician/public-health consultation about suitability of post-exposure prevention; preserve removal and later symptom watch; no lay prescribing or photo clearance.

- [https://www.cdc.gov/lyme/prevention/index.html](https://www.cdc.gov/lyme/prevention/index.html): Post-exposure antibiotics.
- [https://www.cdc.gov/lyme/media/pdfs/Lyme-Disease-Prophylaxis-After-Tick-Bite-Poster.pdf](https://www.cdc.gov/lyme/media/pdfs/Lyme-Disease-Prophylaxis-After-Tick-Bite-Poster.pdf): Page 1, step 2 and conditional pathway.

### RT01-C02: Test default phone-scale knot/compass readability and an accessible enlargement route

Retained 390-pixel captures and CSS arithmetic show very small embedded labels. Browser zoom is enabled. No real-device task or new WCAG failure was established.

**Next step.** Add an obvious keyboard-accessible offline way to open/enlarge a technical figure, preserving its stop rule and page ID. Consider stacking panels or moving labels out of artwork on narrow screens. Define a manual diagram-reading task, not just no-overflow/axe pass, before promoting the system.

- [https://github.com/Davisjxxxx/Survival_Guide/blob/84967d75af91bbf0d2cb36c54394dcf67f2104a5/foundations/visual/w2c_context/W2C-B01/W2C-B01-phone.jpg](https://github.com/Davisjxxxx/Survival_Guide/blob/84967d75af91bbf0d2cb36c54394dcf67f2104a5/foundations/visual/w2c_context/W2C-B01/W2C-B01-phone.jpg): Three captured 390-pixel cards.
- [https://github.com/Davisjxxxx/Survival_Guide/blob/84967d75af91bbf0d2cb36c54394dcf67f2104a5/foundations/reader/edition.css](https://github.com/Davisjxxxx/Survival_Guide/blob/84967d75af91bbf0d2cb36c54394dcf67f2104a5/foundations/reader/edition.css): figure sizing and v01-pilot overrides.

### RT01-C03: Carry the process-duration condition into boiling-water canner water depth

A 45-minute or elevation-extended tested process can select the lower end of the stated range. This is procedural incompleteness; it does not establish that any actual batch was underprocessed. Full tested-recipe compliance and the card’s existing cover/boil monitoring reduce the risk.

**Next step.** Express the process-length condition consistently in action, verify, figure and alt, subject to H17 approval. Test short and >30-minute processes, including an elevation adjustment that crosses 30 minutes.

- [NCHFP — Using Boiling Water Canners](https://nchfp.uga.edu/how/can/general-canning-information/using-boiling-water-canners): Steps for Successful Boiling Water Canning, step 4 (retrieval line 188).

## What the adversarial probes established

The existing four relevant regression tests passed. The additional linter probe ran seven intentionally unsafe fixtures in memory: two exact action-text controls were rejected, while five variants passed. One safe negation control passed. This demonstrates scope and negation defects in that linter. It does not establish a bypass of all build, review or publication gates. The negative fixtures are marked as test data and were never inserted into a production page.

The compass probe changed the visible needle by 90 degrees without changing its descriptive bearing metadata. Both a transform mutation and changed polygon coordinates were accepted by the unit geometry checker. The separate fresh-build byte-equality check was not bypassed. No wrong bearing is alleged in the current unmodified drawing.

The print comparison found nine old B04/B05 figure headers among the 22 W2C cards in the consolidated Letter PDF. The current and old Z14-P53 instructions were then compared directly in the source, both consolidated print sizes and the packaged standalone Letter proof. The retained consolidated PDFs match their recorded SHA-256 values. Integrity and freshness are different properties, and this review found a freshness failure.

Reproduction receipts and a small set of inspected renders are in [evidence/](evidence/). [EVIDENCE_MANIFEST.json](EVIDENCE_MANIFEST.json) pins their hashes and the source assets. The proof header screen is a mismatch detector; a matching header alone is not a semantic-equivalence proof.

## Existing issues retained without double counting

W2C already records the K09 missing source locator, device-specific CPAP/flushing scope, pump behavior during brownouts, an unsupported 24-hour flushing-water rule, smoke-alarm citation limits, structural failure-sequence wording, and several canning-source boundaries. This review does not relabel those as new discoveries or close them. K09 is used here to demonstrate the separate failure to expose current audit status in reader evidence panels.

Current sampled water text retains chemical/algal/brackish-water restrictions and model-specific filter limits. Current Z14-P53 retains its tested-recipe and equipment restrictions. The current compass example agrees with the reviewed USGS orientation procedure; the knot plates show distinct forms and crossings; Z09-P44 separates line tension from support reaction. These negative findings apply only to the stated samples and are not scientific clearance.

## Recommended production order

1. Apply RT01-01 through RT01-05 as a small, source-checked correction batch. Keep clinical and domain review pending. Change all relevant wording surfaces together, not only action prose. Bring Z10-P26 back into the repair queue despite its provisional-retain label.
2. Correct the residual food figure and pacing certainty (RT01-07 and RT01-08). Ask the named specialists to assess the proposed content; no AI sign-off closes their holds.
3. Repair the linter, geometry check and evidence-status propagation (RT01-09 through RT01-11), using the reproductions as targeted regression tests.
4. Rebuild and inspect affected reader, Letter/A4 and zone-package artifacts, and resolve RT01-06 before another owner-review package is called current.
5. Resume the remaining visual queue in the established small batches. Carry RT01-C01 through C03 to the relevant clinical, usability and food-review owners.

The operational continuation brief is [OPUS_RESUME.md](OPUS_RESUME.md). The machine-readable register is [FINDINGS.json](FINDINGS.json), with a compact [CSV index](FINDINGS.csv). All remedies remain proposed until a later implementation supplies before/after evidence and the applicable review receipts. Publication remains HOLD.
