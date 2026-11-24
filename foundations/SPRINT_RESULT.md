# Survival Field Encyclopedia — Production Sprints F05–F08 & P09–P11 Result

Historical production receipt for `4adfbd4`. Its metrics describe the delivered predecessor. The [A01 technical audit](audit/ASTRA_A01_EXECUTIVE_REPORT.md) records current changes and the remaining technical work.

Review edition built strictly additively from frozen historical recovery checkpoint `890c66ac1d51465d3a4315e50fb2dbe1e0f78f6f` (extending Draft PR #3 foundational checkpoint `ef27447bc28a8efef615d55b2074e601ebe0fb3b`). Frozen predecessor branches (`main` `1db1efc`, `review/b013-b014-field-drafts-20261122` `6adbb05`, `review/s02-s03-historical-recovery-20261124` `890c66a`) and all frozen files remain completely untouched.

Production Sprints **P09 (Z09 Tools and Construction)**, **P10 (Z11 Navigation, Weather and Rescue)**, and **P11 (Z12 Extreme Environments)** drafted, illustrated, verified, and packaged **194 new manuscript and reconstruction pages** (joining the 2 retained Z11 reconstruction cards from `05-reconstruction.cards` for **196 completed pages across Z09, Z11, and Z12**), advancing overall encyclopedia draft production from **177** to **373 completed pages across 7 active zones** (plus **3 starter reconstructions** in Z13/Z14/Z15 = **376 total reader cards**).

| Zone | Sprint | Planned allocation | Complete draft pages | Still to draft | Adapted historical | New manuscripts | Reconstruction drafts | Qualified approval |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| Z01 Survival fundamentals | F05 | 22 | 22 | 0 | 9 | 13 | 0 | 0 |
| Z02 Shelter and housing | F07 | 55 | 55 | 0 | 28 | 27 | 0 | 0 |
| Z03 Fire and ignition | F08 | 45 | 45 | 0 | 22 | 23 | 0 | 0 |
| Z04 Water | F06 | 55 | 55 | 0 | 22 | 33 | 0 | 0 |
| **Foundational subtotal (Z01–Z04)** | **F05–F08** | **177** | **177** | **0** | **81** | **96** | **0** | **0** |
| Z09 Tools and construction | P09 | 53 | 53 | 0 | 8 | 45 | 0 | 0 |
| Z11 Navigation, weather and rescue | P10 | 68 | 68 | 0 | 27 | 31 | 10 | 0 |
| Z12 Extreme environments | P11 | 75 | 75 | 0 | 19 | 56 | 0 | 0 |
| **Extended subtotal (Z09, Z11, Z12)** | **P09–P11** | **196** | **196** | **0** | **54** | **132** | **10** | **0** |
| **Completed zones total (7 of 16)** | **F05–P11** | **373** | **373** | **0** | **135** | **228** | **10** | **0** |
| Starter reconstructions (Z13/Z14/Z15) | S03 | — | 3 | — | 0 | 0 | 3 | 0 |
| Remaining unplanned/partial zones (Z05–Z08, Z10, Z13–Z16) | Pending | 643 | 0 | 643 | 0 | 0 | 0 | 0 |

All 16 encyclopedia zones (1,016 total planned pages) remain tracked in the updated [master zone completion matrix](ZONE_COMPLETION_MATRIX.csv), superseding the frozen `890c66a` snapshot without altering `project/planning/ZONE_COMPLETION_MATRIX.csv`. Original missing `B014 P01–P10` remains explicitly flagged as an open historical recovery requirement behind the 10 labeled reconstruction drafts `Z11-R01`..`Z11-R10`.

## Delivered evidence, illustrations, and readers (F05–F08 + P09–P11)

- **Expanded evidence packs (106 primary sources · 140 claim rows across 8 packs):** P09–P11 added **32 live-checked federal/state agency primary sources** (OSHA handtools, USFS trail handtools/crosscut saws, USGS topographic maps/symbols/public-domain rights, NOAA SARSAT/JetStream/Marine/Tides/Coast/NWR, NWS cold-water/rip-current/tsunami/hurricane/fog/drought/Turn-Around-Don't-Drown, USCG Boating/PFD, CDC high-altitude, EPA/NPS wetlands, NPS Death Valley & Rocky Mountain safety, MN DNR ice thickness & cold-water safety, Ready.gov tsunamis & landslides) and **40 new 10-column claims** (`K01–K12` in [tools.md](evidence/tools.md), `N01–N10` in [navigation.md](evidence/navigation.md), and `X01–X18` in [environments.md](evidence/environments.md)) on top of the 74-source / 100-claim foundational baseline (`water`, `fire`, `exposure`, `food`, `triage`).
- **Technical illustrations (376 editable local-only SVGs · 323 bespoke specs):** P09–P11 added **194 new editable SVGs and declarative diagram specifications** (`53` in Z09, `66` in Z11, `75` in Z12) to [diagram-specs.json](evidence/diagram-specs.json). Across all 323 bespoke specs: 50 decision trees, 48 comparative configurations, 48 failure-mode illustrations, 42 exploded component views, 42 mechanism diagrams, 39 environmental relationships, 32 cutaway views, and 22 material cross-sections (plus 11 preserved hand cross-sections and 42 pilot/core schematics = 376 SVGs total). All SVGs carry explicit `CONCEPTUAL, NOT TO SCALE` notices and zero engineering certification claims.
- **Rights-verified historical map & diagnostic photography register:** Deterministic build pipeline copies the authentic public-domain USGS 1965 Ely quadrangle excerpt (`reader/maps/ely-1965.jpg`) into the offline reader and embeds it with a symbols-only non-navigation disclaimer in the evidence drawer of `Z11-R04`, `Z11-P12`, and `Z11-P19`. Documentary context photographs (`PHOTO-NPS-01`, `PHOTO-USGS-01`, `diagnostic_photo: false`) remain in [photo provenance](evidence/photos/manifest.json). [photo-requirements.tsv](evidence/photo-requirements.tsv) now tracks **23 open authentic diagnostic photography requirements** (`11` foundational Z02–Z04 + `3` Z09 + `4` Z11 + `5` Z12). Zero staged or generated imagery is classified as diagnostic evidence.
- **Standalone zone readers, integrated directory, and bookmarked Letter/A4 proofs:** Generated standalone searchable offline zone readers (`reader/zones/Z01/index.html`..`Z04`, `Z09`, `Z11`, `Z12`), updated the consolidated 376-card offline reader (`reader/index.html`) and integrated 16-zone directory (`reader/directory.html`), and produced single-card-per-sheet bookmarked Letter (612×792 pt) and A4 (595.9×842.9 pt) proofs for Z09 (`53 pp`), Z11 (`68 pp`), and Z12 (`75 pp`) alongside all Z01–Z04 zone and 177-page consolidated proofs, visual contact sheets, desktop/mobile screenshots, QA receipts (`Z09-qa.json`, `Z11-qa.json`, `Z12-qa.json`), and deterministic `proofs/foundations-offline.zip`.

## Verification summary

- **Control & domain contradiction regression suite (`scripts/test_foundation_controls.py`):** **13/13 tests pass**, enforcing `publication: HOLD`, duplicate ID/title rejection, unknown claim rejection, required reviewer/failure fields, visual-clarity potability prohibition, enclosed-combustion prohibition, boiling altitude rule consistency, portable generator ≥20 ft rule, zero unvalidated Z02 structural load ratings, zero unvalidated Z09 cordage/rigging load ratings, Z11 moss-on-north folklore guard, Z12 universal-ice-safety prohibition, and Z12 rip-current swimming guard.
- **Offline browser, accessibility, and Letter/A4 print QA (`scripts/verify_foundations.py`):**
  - **Z09 (`Z09-qa.json`):** 235 cards checked at 320/390/1280 px, 53 sheets × Letter/A4, 61 axe-core WCAG 2.0/2.1 A/AA audits — 0 violations, 0 HTTP requests, 0 JS errors; contact sheet & screenshots visually verified.
  - **Z11 (`Z11-qa.json`):** 301 cards checked at 320/390/1280 px, 68 sheets × Letter/A4, 76 axe-core audits — 0 violations, 0 HTTP requests, 0 JS errors; authentic USGS 1965 Ely excerpt verified loading on `Z11-R04`, `Z11-P12`, `Z11-P19`; contact sheet & screenshots visually verified.
  - **Z12 (`Z12-qa.json`):** 376 cards checked at 320/390/1280 px, 75 sheets × Letter/A4, 84 axe-core audits — 0 violations, 0 HTTP requests, 0 JS errors; contact sheet & screenshots visually verified.
- **Custody, reproducibility, and archive integrity (`scripts/check_foundations.py`):** Verified strictly additive git diff relative to `890c66a`, byte-for-byte reproducible reader generation, all 376 SVG XML local-only checks + SHA-256 manifests, photo provenance hashes, valid bookmarks and Letter/A4 dimensions across all 26 retained PDFs, and deterministic `foundations-offline.zip` integrity.

## Independent technical review & qualified specialist review requirements

All **376 draft cards** carry `publication: HOLD` and **0 qualified human approvals**. Physical field validation, assistive-technology testing, and legal/clinical/rescue sign-off remain separate mandatory gates.

- **Consolidated Astra review queue ([ASTRA_ESCALATION_REGISTER.md](ASTRA_ESCALATION_REGISTER.md)):** Tracks **8 prioritized escalations (`ASTRA-001`..`ASTRA-008`)** spanning Z02 structural/snow load disclaimers, Z04 cold-water disinfection/HAB/filter kinetics, Z03 high-altitude CO & conceptual historical firecraft boundaries, PDF/UA structural tagging & grayscale print contrast, Z09 pulley anchor-load doubling & saw-bind/non-certification boundaries, Z11 missing `B014 P01–P10` recovery + declination/datum/SAR helicopter extraction risks, Z12 ice/cold-water rescue + heat-stroke cooling + HAPE/HACE descent + avalanche/debris-flow + rip-current/tsunami/maritime distress, and cross-zone terminology/contradiction harmonization.
- **Qualified human domain specialist sign-off required before publication:**
  - **Z01–Z04:** SAR/EMS/accessibility, cold-weather/structural/avalanche/CO safety, wildland fire prevention & portable fuel appliances, drinking-water microbiology & HAB toxicology.
  - **Z09:** Tool/rigging mechanics, forestry/sawyer operations, and equipment-maintenance safety.
  - **Z11:** Cartography/geodesy (declination & datum), meteorology, backcountry SAR, aviation/helicopter rescue, and emergency radio/SARSAT communications.
  - **Z12:** Wilderness medicine (hypothermia, frostbite, heat stroke, HAPE/HACE), Minnesota/cold-water ice rescue, avalanche/mountaineering safety, desert/wetland field safety, and USCG/NOAA coastal & maritime safety.
- **Remaining encyclopedia scope (643 planned pages across 9 zones):** Z05 Wild foods & poisonous lookalikes (135), Z06 Hunting & fishing (48), Z07 Traps & snares (30), Z08 Rocks, minerals & materials (60), Z10 Wilderness medicine (80), Z13 Home survival & utilities (70; 1 starter reconstruction), Z14 Food production & preservation (80; 1 starter reconstruction), Z15 Disaster scenarios (65; 1 starter reconstruction), and Z16 Field reference atlas (75).
- **Release boundary:** Do NOT merge into `main` or lift `publication: HOLD` until Astra consolidated technical review, authentic diagnostic photo acquisition where required, historical recovery disposition for `B014 P01–P10` and primers, and qualified human domain approvals are recorded in the custody ledger.
