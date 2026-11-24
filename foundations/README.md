# Survival Field Encyclopedia — Production Edition (Z01–Z04, Z09, Z11, Z12 · 376 draft cards)

Extract the [offline ZIP](proofs/foundations-offline.zip) and open `reader/index.html` (consolidated searchable offline reader across all 376 cards), `reader/directory.html` (integrated 16-zone directory linking all 7 active zones, starter reconstructions, and the frozen Track B edition without modifying it), or any standalone zone reader (`reader/zones/Z01/index.html` through `reader/zones/Z04/index.html`, `Z09`, `Z11`, and `Z12`).

The A01 candidate includes a [technical audit and Neon handoff](audit/ASTRA_A01_EXECUTIVE_REPORT.md) and new tagged encyclopedia proofs covering all 376 cards ([Letter](proofs/encyclopedia-letter.pdf) and [A4](proofs/encyclopedia-a4.pdf)). Publication remains on HOLD.

The consolidated foundational proofs ([177-sheet Letter](proofs/foundations.pdf), [177-sheet A4](proofs/foundations-a4.pdf)), separate bookmarked Letter/A4 proofs for all 7 completed zones (`proofs/Z01-letter.pdf`..`proofs/Z04-a4.pdf`, `proofs/Z09-letter.pdf`/`a4.pdf`, `proofs/Z11-letter.pdf`/`a4.pdf`, `proofs/Z12-letter.pdf`/`a4.pdf`), [13-sheet reconstruction proof](proofs/reconstructions.pdf), [updated 16-zone completion matrix](ZONE_COMPLETION_MATRIX.csv), [consolidated Astra escalation register](ASTRA_ESCALATION_REGISTER.md), and [sprint result](SPRINT_RESULT.md) cover the completed foundational (F05–F08) and extended production (P09–P11) draft editions for independent technical and qualified specialist review.

Original Track B text, duplicate historical proofs (`B008-original.pdf`/`B008.pdf`, `B009-original.pdf`/`B009.pdf`), and illustration sources remain completely untouched in their frozen paths (`../reader/`, `../project/`, `../production/`).

## Authoring, evidence, and illustrations

- `manuscripts/01-pilot.cards` through `12-p11-z12-environments.cards` store all **373 completed zone draft pages** (`Z01-P01`..`Z01-P22`, `Z02-P01`..`Z02-P55`, `Z03-P01`..`Z03-P45`, `Z04-P01`..`Z04-P55`, `Z09-P01`..`Z09-P53`, `Z11-R01`..`Z11-R10` + `Z11-P11`..`Z11-P68`, and `Z12-P01`..`Z12-P75`) plus **3 retained starter reconstruction drafts** in pending zones (`Z13-R03`, `Z14-R01`, `Z15-R03`) = **376 total reader cards**. Every expanded page requires explicit `objective:`, `applies:`, `equipment:`, `failure:`, `verify:`, `stop:`, claim IDs (`@W..`, `@E..`, `@C..`, `@T..`, `@K..`, `@N..`, `@X..`, `@ED`), and a bespoke technical illustration specification.
- [Primary sources](evidence/sources.tsv) (**113 registered agency/specialist references**) and [claim evidence](evidence/claims.tsv) (**150 10-column claim rows** across 8 packs: `water`, `fire`, `exposure`, `food`, `triage`, `tools`, `navigation`, `environments`) record source identity, check/revision date, exact supporting section, applicable conditions, support statement, limitations, conflicting evidence, editorial note, and required specialist reviewer.
- [Diagram specifications](evidence/diagram-specs.json) retains all **323 generation specifications** across reusable diagram families, complementing 11 preserved hand-crafted cross-sections and 42 pilot/core schematics (**376 editable local-only SVGs** total).
- [Asset manifest](reader/asset-manifest.json) binds all 376 editable local-only SVGs to SHA-256 digests and provenance. Authentic documentary photographs (`PHOTO-NPS-01`, `PHOTO-USGS-01`, `diagnostic_photo: false`) and the public-domain USGS 1965 Ely quadrangle excerpt (`reader/maps/ely-1965.jpg`, embedded with a symbols-only disclaimer on `Z11-R04`, `Z11-P12`, and `Z11-P19`) remain separately documented; [photo requirements](evidence/photo-requirements.tsv) registers **23 open authentic diagnostic photography requirements** across completed zones. Zero staged or generated scenes are classified as diagnostic evidence.
- [Page manifest](reader/page-manifest.json) classifies every page as `Adapted historical material` (135), `New manuscript` (228), or `Reconstruction draft` (13 — including `Z11-R01`..`Z11-R10` explicitly preserving the open historical recovery requirement for missing `B014 P01–P10`), while enforcing a fixed `publication: HOLD` gate.

## Reproducible build and verification

From the repository root, using [review-requirements.txt](../production/review-requirements.txt) and local Chrome/Chromium:

```sh
python scripts/test_foundation_controls.py
python scripts/build_foundations.py
uv run --with-requirements production/review-requirements.txt python scripts/verify_foundations.py --browser-only --name A01 --axe /absolute/path/to/axe.min.js
uv run --with-requirements production/review-requirements.txt python scripts/print_foundations_tagged.py
python scripts/check_foundations.py --write-package
```

All reader navigation, search, diagrams, zone readers, and directory links operate offline from local files with zero network requests. Print PDFs are single-card-per-sheet bookmarked proofs for editorial and specialist review only; publication remains on `HOLD`.
