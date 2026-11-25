# Survival Field Encyclopedia — Complete 16-Zone Draft Edition (1,016 / 1,016 Draft Cards · Publication HOLD)

The [A03 technical audit](audit/a03/ASTRA_A03_EXECUTIVE_REPORT.md) and [V01 pilot](visual/VISUAL_PILOT_REVIEW_PACKAGE/index.html) record current corrections, visual candidates and evidence limits. The complete sixteen-zone draft remains on HOLD.

Extract the [core offline reader ZIP](proofs/foundations-offline.zip) (or any standalone zone package in [proofs/packages/](proofs/packages/PACKAGE-MANIFEST.json)) and open `reader/index.html` (consolidated searchable offline reader across all 1,016 cards), `reader/directory.html` (integrated 16-zone directory linking all 16 completed draft zones and the byte-identical embedded frozen Track B historical archive), or any standalone zone reader (`reader/zones/Z01/index.html`..`reader/zones/Z16/index.html`). To assemble a single combined local archive with consolidated proofs on demand, run `python3 scripts/check_foundations.py --assemble-complete /path/to/encyclopedia-complete.zip`.

The consolidated tagged encyclopedia proofs ([1,016-sheet Letter](proofs/encyclopedia-letter.pdf), [1,016-sheet A4](proofs/encyclopedia-a4.pdf)), foundational proofs ([177-sheet Letter](proofs/foundations.pdf), [177-sheet A4](proofs/foundations-a4.pdf)), separate tagged bookmarked Letter/A4 proofs for all 16 zones (`proofs/Z01-letter.pdf`..`proofs/Z16-a4.pdf`), [13-sheet reconstruction collection](proofs/reconstructions.pdf), [16-zone completion matrix](ZONE_COMPLETION_MATRIX.csv), [consolidated Astra escalation register](ASTRA_ESCALATION_REGISTER.md), [25-hold specialist review register](audit/SPECIALIST_REVIEW_REGISTER.csv), [Astra A03 review handoff](audit/ASTRA_A03_REVIEW_HANDOFF.md), and [sprint result](SPRINT_RESULT.md) cover the complete 16-zone draft encyclopedia on `publication: HOLD`.

Original Track B text, duplicate historical proofs (`B008-original.pdf`/`B008.pdf`, `B009-original.pdf`/`B009.pdf`), predecessor A01/A02 audit ledgers (`audit/a02/`), and illustration sources remain completely untouched in their frozen paths (`../reader/`, `../project/`, `../production/`).

## Authoring, evidence, taxonomy, and illustrations

- `manuscripts/01-pilot.cards` through `21-p20-z16-atlas.cards` store all **1,016 completed draft cards across all 16 zones** (`Z01` 22, `Z02` 55, `Z03` 45, `Z04` 55, `Z05` 135, `Z06` 48, `Z07` 30, `Z08` 60, `Z09` 53, `Z10` 80, `Z11` 68, `Z12` 75, `Z13` 70, `Z14` 80, `Z15` 65, `Z16` 75), including **13 explicitly labeled reconstruction drafts** (`Z11-R01`..`Z11-R10`, `Z13-R03`, `Z14-R01`, `Z15-R03`) preserving the unrecovered `B014 P01–P10` and historical primer recovery requirements.
- [Primary source register](evidence/sources.tsv) contains **253 registered sources** (`+61` live HTTP 200 sources in P16–P20). [Claim evidence](evidence/claims.tsv) contains **333 rows across 17 packs**, with **6,021 of 6,043 operational statements (99.64%)** carrying primary claim references (`333/333` distinct non-ED claims cited). Substantive verification remains open: all **116 unresolved A01/A02 evidence items** remain open in [a02/UNRESOLVED_EVIDENCE_REGISTER.csv](audit/a02/UNRESOLVED_EVIDENCE_REGISTER.csv), and all 86 P16–P20 claims await Astra A03 review.
- [Z05 taxonomic workflow](evidence/Z05_TAXONOMIC_WORKFLOW.md) and [Z05 taxonomic register](evidence/z05-taxonomic-register.tsv) strictly separate botanical (`89 Plantae`) and fungal (`24 Fungi`) evidence across **113 taxa** — 100% locked at `consumption_status = WITHHELD_HOLD` and `specialist_review = PENDING`.
- [Diagram specifications](evidence/diagram-specs.json) (`963` bespoke specs across `27` diagram families) and [p16_p20/VISUAL_REDESIGN_BACKLOG.csv](audit/p16_p20/VISUAL_REDESIGN_BACKLOG.csv) cover **1,016 editable local-only SVGs** across **59 distinct measured geometry groups** with **0 clipped labels and 0 intersecting text boxes** in Chromium measurement. All **490 A02 visual redesign candidates** are preserved alongside **237 P16–P20 shared-template candidates** (`727` total redesign candidates queued for Astra A03).
- [Photo requirements](evidence/photo-requirements.tsv) tracks **54 open authentic diagnostic photography requirements** (`35` A02 + `19` P16–P19; **0 expert-validated diagnostic photos acquired; 0 fabricated diagnostic photos**). Four photos in the [provenance manifest](evidence/photos/manifest.json) provide documentary context only; the historical 1965 USGS Ely quadrangle excerpt retains its symbols-only designation.
- [Page manifest](reader/page-manifest.json) classifies every page as `Adapted historical material` (**150**), `New manuscript` (**853**), or `Reconstruction draft` (**13**), enforcing a fixed `publication: HOLD` gate and **0 qualified human approvals** across **25 pending specialist holds** (`H01`–`H25`).

## Reproducible build and verification

From the repository root, using [review-requirements.txt](../production/review-requirements.txt) and local Chrome/Chromium:

```sh
python3 scripts/test_foundation_controls.py
python3 scripts/build_foundations.py
uv run --with-requirements production/review-requirements.txt python scripts/audit_foundation_vectors.py foundations foundations/audit/p16_p20 --fail-layout
uv run --with-requirements production/review-requirements.txt python scripts/print_foundations_tagged.py
uv run --with-requirements production/review-requirements.txt python scripts/verify_foundations.py --browser-only --name A03 --axe /absolute/path/to/axe.min.js
python3 scripts/check_foundations.py --write-package
```

All reader navigation, search, diagrams, 16 standalone zone readers, embedded historical archive links, and directory links operate offline from local files with zero network requests. Print PDFs are tagged, single-card-per-sheet bookmarked proofs for editorial and specialist review only; publication remains on `HOLD`.
