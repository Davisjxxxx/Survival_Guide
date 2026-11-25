# Survival Field Encyclopedia — Production Edition (11 of 16 Zones Complete · 668 Draft Cards)

Extract the [offline ZIP](proofs/foundations-offline.zip) and open `reader/index.html` (consolidated searchable offline reader across all 668 cards), `reader/directory.html` (integrated 16-zone directory linking all 11 active zones and the byte-identical embedded frozen Track B historical archive), or any standalone zone reader (`reader/zones/Z01/index.html`..`Z04`, `Z09`..`Z15`).

The consolidated tagged encyclopedia proofs ([668-sheet Letter](proofs/encyclopedia-letter.pdf), [668-sheet A4](proofs/encyclopedia-a4.pdf)), foundational proofs ([177-sheet Letter](proofs/foundations.pdf), [177-sheet A4](proofs/foundations-a4.pdf)), separate tagged bookmarked Letter/A4 proofs for all 11 completed zones (`proofs/Z01-letter.pdf`..`proofs/Z15-a4.pdf`), [13-sheet reconstruction collection](proofs/reconstructions.pdf), [updated 16-zone completion matrix](ZONE_COMPLETION_MATRIX.csv), [consolidated Astra escalation register](ASTRA_ESCALATION_REGISTER.md), [A01/P12–P15 specialist hold register](audit/SPECIALIST_REVIEW_REGISTER.csv), and [sprint result](SPRINT_RESULT.md) cover all completed foundational (F05–F08), extended (P09–P11), Astra A01 audited, and P12–P15 continuation drafts on `publication: HOLD`.

Original Track B text, duplicate historical proofs (`B008-original.pdf`/`B008.pdf`, `B009-original.pdf`/`B009.pdf`), and illustration sources remain completely untouched in their frozen paths (`../reader/`, `../project/`, `../production/`).

## Authoring, evidence, and illustrations

- `manuscripts/01-pilot.cards` through `16-p15-z15-disasters.cards` store all **668 completed zone draft cards** across 11 zones (`Z01` 22, `Z02` 55, `Z03` 45, `Z04` 55, `Z09` 53, `Z10` 80, `Z11` 68, `Z12` 75, `Z13` 70, `Z14` 80, `Z15` 65), including **13 explicitly labeled reconstruction drafts** (`Z11-R01`..`Z11-R10`, `Z13-R03`, `Z14-R01`, `Z15-R03`) preserving the unrecovered `B014 P01–P10` and historical primer recovery requirements.
- [Primary sources](evidence/sources.tsv) (**161 verified agency/specialist references**, including 48 newly live-verified HTTP 200 sources added in P12–P15) and [claim evidence](evidence/claims.tsv) (**230 10-column claim rows** across 12 packs: `water`, `fire`, `exposure`, `food`, `triage`, `tools`, `navigation`, `environments`, `medicine`, `utilities`, `preservation`, `disasters`) bind **3,932 of 3,955 operational assertions (99.4%)** to primary evidence (230/230 distinct claims cited). All 59 unresolved A01 baseline claims remain preserved open in [CLAIM_COVERAGE_AUDIT.csv](audit/CLAIM_COVERAGE_AUDIT.csv).
- [Diagram specifications](evidence/diagram-specs.json) retains all **615 bespoke generation specifications** across 16 technical illustration families (adding 6 purpose-built families in P12–P15: `correct_vs_wrong`, `sequence_plate`, `system_boundary`, `escalation_ladder`, `anatomy_zone`, `seasonal_timeline`), increasing distinct SVG artwork geometry groups from 16 to **31** across **668 editable local-only SVGs** with **0 clipped labels and 0 text overlaps** verified in Chromium ([p12_p15/ILLUSTRATION_AUDIT.csv](audit/p12_p15/ILLUSTRATION_AUDIT.csv)).
- [Photo requirements](evidence/photo-requirements.tsv) registers **35 open authentic diagnostic photography requirements** (`23` A01 baseline + `12` added across Z10, Z13, Z14, Z15). Documentary context photographs (`PHOTO-NPS-01`, `PHOTO-USGS-01`, `diagnostic_photo: false`) and the public-domain USGS 1965 Ely quadrangle excerpt (`reader/maps/ely-1965.jpg`, symbols-only disclaimer) retain their original provenance classifications. Zero staged or generated imagery is classified as diagnostic evidence.
- [Page manifest](reader/page-manifest.json) classifies every page as `Adapted historical material` (141), `New manuscript` (514), or `Reconstruction draft` (13), while enforcing a fixed `publication: HOLD` gate and **0 qualified human approvals** across **21 pending specialist holds** (`H01`–`H21`).

## Reproducible build and verification

From the repository root, using [review-requirements.txt](../production/review-requirements.txt) and local Chrome/Chromium:

```sh
python scripts/test_foundation_controls.py
python scripts/build_foundations.py
uv run --with-requirements production/review-requirements.txt python scripts/audit_foundation_vectors.py foundations foundations/audit/p12_p15 --fail-layout
uv run --with-requirements production/review-requirements.txt python scripts/print_foundations_tagged.py
uv run --with-requirements production/review-requirements.txt python scripts/verify_foundations.py --browser-only --zone Z15 --name Z15 --axe /path/to/axe.min.js
python scripts/check_foundations.py --write-package
```

All reader navigation, search, diagrams, zone readers, embedded historical archive links, and directory links operate offline from local files with zero network requests. Print PDFs are tagged, single-card-per-sheet bookmarked proofs for editorial and specialist review only; publication remains on `HOLD`.
