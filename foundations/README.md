# Survival Field Encyclopedia — Complete 16-Zone Illustrated Review Edition (`1,016` Pages · V02/V03 Visual Reconstruction · `publication: HOLD`)

The [A04 qualification report](audit/a04/ASTRA_A04_EXECUTIVE_REPORT.md) records the focused V02/V03 visual and evidence review. The [Opus handoff](audit/a04/OPUS_WAVE_2C_CONTINUATION.md) gives the next production queue. Publication HOLD.

Extract the [core offline reader ZIP](proofs/foundations-offline.zip) (or any standalone zone/visual package in [proofs/packages/](proofs/packages/PACKAGE-MANIFEST.json)) and open `reader/index.html` (consolidated searchable offline reader across all 1,016 cards), `reader/directory.html` (integrated 16-zone directory linking all 16 zones and the byte-identical embedded frozen Track B archive), or any standalone zone reader (`reader/zones/Z01/index.html`..`reader/zones/Z16/index.html`).

Companion review galleries and modular packages (kept outside core `foundations-offline.zip` so every committed file remains strictly `<= 45 MB`):
- **V01 Visual Pilot (`packages/v01-pilot.zip`):** [V01 Pilot Gallery](visual/VISUAL_PILOT_REVIEW_PACKAGE/index.html) (9 pilot plates + 6 Bell Museum archival JPEGs, preserved pending owner acceptance).
- **V02 Technical Illustration Reconstruction (`packages/v02-technical.zip`):** [V02 Technical Gallery](visual/v02_technical/index.html) (**64 bespoke object-centered editable SVGs** across all 8 priority domains, originals preserved verbatim, color & grayscale contact sheets).
- **V03 Realistic Illustration Briefs (`packages/v03-realistic.zip`):** [82-Item Brief Register](visual/v03_realistic/REALISTIC_ILLUSTRATION_BRIEFS.csv) & [Generation Status Receipt](visual/v03_realistic/GENERATION_STATUS.md) (`HTTP 503` external capacity block recorded; `0` synthetic images fabricated).
- **V03 Authentic Photography Archive (`packages/v03-authentic-photos.zip`):** [V03 Authentic Photo Gallery](visual/v03_authentic_photos/index.html) (**30 visually verified open-license original JPEGs** + display derivatives + full [Rights & Provenance Register](visual/v03_authentic_photos/RIGHTS_AND_PROVENANCE_REGISTER.csv), strictly `PENDING / WITHHELD`).
- **Z16 Atlas Optimization Comparison (`packages/v02-atlas-comparison.zip`):** [Z16 Before/After Comparison Package](visual/v02_atlas_comparison/index.html) & [75-Page Register](visual/v02_atlas_comparison/Z16_ATLAS_OPTIMIZATION_REGISTER.csv) (all 75 original Z16 SVGs preserved untouched pending owner decision).

## Authoritative Governance & Audit Registers

- [Visual Disposition Register](visual/VISUAL_ASSET_DISPOSITION_REGISTER.csv) (`1,016` pages), [Phase 1 Backlog Reconciliation](visual/V02_BACKLOG_RECONCILIATION.csv) (`854` rows), [Illustration Replacement Backlog](visual/ILLUSTRATION_REPLACEMENT_BACKLOG.csv) (`854` rows), and [Diagnostic Photography Acquisition Register](visual/DIAGNOSTIC_PHOTOGRAPHY_ACQUISITION_REGISTER.csv) (`157` active requirements).
- [Taxonomic Diagnostic Evidence](visual/V03_TAXONOMIC_DIAGNOSTIC_EVIDENCE.csv) (`113` profiles: `104` regional specimen leads, `5` naming conflicts reconciled, 100% `WITHHELD_HOLD`).
- [V02/V03 Evidence Resolution Register](visual/V02_V03_EVIDENCE_RESOLUTION_REGISTER.csv) (`172` records: `24` live-verified bounded primary sources, `148` explicitly open) and [Astra Visual & Scientific Escalation Register](visual/V02_V03_ASTRA_ESCALATION_REGISTER.csv) (`40` escalations).
- [16-Zone Completion Matrix](ZONE_COMPLETION_MATRIX.csv), [25-Hold Specialist Register](audit/a03/SPECIALIST_REVIEW_REGISTER.csv), [A03 Executive Report](audit/a03/ASTRA_A03_EXECUTIVE_REPORT.md), and [V02/V03 Sprint Result](SPRINT_RESULT.md).

## Reproducible Build & Verification

```sh
python3 scripts/test_foundation_controls.py
python3 scripts/build_foundations.py
python3 scripts/check_a03_v01.py
/tmp/sfe-production-env/bin/python scripts/audit_foundation_vectors.py foundations foundations/audit/v02_v03 --fail-layout
/tmp/sfe-production-env/bin/python scripts/print_foundations_tagged.py
python3 scripts/check_foundations.py --write-package
```

All 1,016 pages, 37 tagged Letter/A4 PDFs, and offline packages remain strictly on **`publication: HOLD`** with **`0` qualified human approvals**.
