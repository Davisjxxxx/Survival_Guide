# Survival Field Encyclopedia — Production Edition (11 of 16 Zones Complete · 668 Draft Cards)

Extract the [offline ZIP](proofs/foundations-offline.zip) and open `reader/index.html` (consolidated searchable offline reader across all 668 cards), `reader/directory.html` (integrated 16-zone directory linking all 11 active zones and the byte-identical embedded frozen Track B historical archive), or any standalone zone reader (`reader/zones/Z01/index.html`..`Z04`, `Z09`..`Z15`).

The consolidated tagged encyclopedia proofs ([668-sheet Letter](proofs/encyclopedia-letter.pdf), [668-sheet A4](proofs/encyclopedia-a4.pdf)), foundational proofs ([177-sheet Letter](proofs/foundations.pdf), [177-sheet A4](proofs/foundations-a4.pdf)), separate tagged bookmarked Letter/A4 proofs for all 11 completed zones (`proofs/Z01-letter.pdf`..`proofs/Z15-a4.pdf`), [13-sheet reconstruction collection](proofs/reconstructions.pdf), [updated 16-zone completion matrix](ZONE_COMPLETION_MATRIX.csv), [consolidated Astra escalation register](ASTRA_ESCALATION_REGISTER.md), [A01/P12–P15 specialist hold register](audit/SPECIALIST_REVIEW_REGISTER.csv), and [sprint result](SPRINT_RESULT.md) cover all completed foundational (F05–F08), extended (P09–P11), Astra A01 audited, and P12–P15 continuation drafts on `publication: HOLD`.

Original Track B text, duplicate historical proofs (`B008-original.pdf`/`B008.pdf`, `B009-original.pdf`/`B009.pdf`), and illustration sources remain completely untouched in their frozen paths (`../reader/`, `../project/`, `../production/`).

The [A02 report](audit/a02/ASTRA_A02_EXECUTIVE_REPORT.md) records the review results and links to the [final Neon handoff](audit/a02/NEON_FINAL_PRODUCTION_HANDOFF.md).

## Authoring, evidence, and illustrations

- `manuscripts/01-pilot.cards` through `16-p15-z15-disasters.cards` store all **668 completed zone draft cards** across 11 zones (`Z01` 22, `Z02` 55, `Z03` 45, `Z04` 55, `Z09` 53, `Z10` 80, `Z11` 68, `Z12` 75, `Z13` 70, `Z14` 80, `Z15` 65), including **13 explicitly labeled reconstruction drafts** (`Z11-R01`..`Z11-R10`, `Z13-R03`, `Z14-R01`, `Z15-R03`) preserving the unrecovered `B014 P01–P10` and historical primer recovery requirements.
- [Primary source register](evidence/sources.tsv) contains 192 registered sources. [Claim evidence](evidence/claims.tsv) contains 247 rows across 12 packs. 3,933 of 3,955 operational statements carry source references. See [A02 claim support](audit/a02/CLAIM_SUPPORT_AUDIT.csv) and the [unresolved evidence register](audit/a02/UNRESOLVED_EVIDENCE_REGISTER.csv) for substantive review status.
- [Diagram specifications](evidence/diagram-specs.json) and the [A02 visual classification](audit/a02/VISUAL_QUALITY_CLASSIFICATION.csv) cover 668 editable local-only vectors with 32 measured geometry groups. The A02 label layout check found zero clipping or overlap.
- [Photo requirements](evidence/photo-requirements.tsv) tracks 35 open diagnostic needs. Four photos in the [provenance manifest](evidence/photos/manifest.json) provide documentary context; A02 added the CDC and NOAA files. The historical USGS map retains its symbols-only designation.
- [Page manifest](reader/page-manifest.json) classifies every page as `Adapted historical material` (141), `New manuscript` (514), or `Reconstruction draft` (13), while enforcing a fixed `publication: HOLD` gate and **0 qualified human approvals** across **21 pending specialist holds** (`H01`–`H21`).

## Reproducible build and verification

From the repository root, using [review-requirements.txt](../production/review-requirements.txt) and local Chrome/Chromium:

```sh
python scripts/test_foundation_controls.py
python scripts/build_foundations.py
uv run --with-requirements production/review-requirements.txt python scripts/audit_foundation_vectors.py foundations /absolute/path/to/new-receipts --fail-layout
uv run --with-requirements production/review-requirements.txt python scripts/print_foundations_tagged.py
uv run --with-requirements production/review-requirements.txt python scripts/verify_foundations.py --browser-only --name A02 --axe /absolute/path/to/axe.min.js
python scripts/check_foundations.py --write-package
```

All reader navigation, search, diagrams, zone readers, embedded historical archive links, and directory links operate offline from local files with zero network requests. Print PDFs are tagged, single-card-per-sheet bookmarked proofs for editorial and specialist review only; publication remains on `HOLD`.
