# Foundational production edition (Z01–Z04 complete · 177 draft pages)

Extract the [offline ZIP](proofs/foundations-offline.zip) and open `reader/index.html` (consolidated searchable reader), `reader/directory.html` (integrated 16-zone directory linking the frozen Track B edition without modifying it), or any separate zone reader (`reader/zones/Z01/index.html` through `reader/zones/Z04/index.html`).

The consolidated [177-sheet Letter proof](proofs/foundations.pdf), [177-sheet A4 proof](proofs/foundations-a4.pdf), separate zone Letter/A4 proofs (`proofs/Z01-letter.pdf` .. `proofs/Z04-a4.pdf`), [5-sheet reconstruction proof](proofs/reconstructions.pdf), [updated 16-zone completion matrix](ZONE_COMPLETION_MATRIX.csv), and [sprint result](SPRINT_RESULT.md) cover the complete foundational production release candidate for editorial and specialist review.

Original Track B text, duplicate historical proofs (`B008-original.pdf`/`B008.pdf`, `B009-original.pdf`/`B009.pdf`), and illustration sources remain completely untouched in their frozen paths (`../reader/`, `../project/`, `../production/`).

## Authoring, evidence, and illustrations

- `manuscripts/01-pilot.cards` through `09-f08-z03-fire.cards` store all 177 foundational pages (`Z01-P01`..`Z01-P22`, `Z02-P01`..`Z02-P55`, `Z03-P01`..`Z03-P45`, `Z04-P01`..`Z04-P55`) plus 5 retained reconstruction drafts (`Z11-R02`, `Z11-R08`, `Z13-R03`, `Z14-R01`, `Z15-R03`). Every new F05–F08 card requires explicit `failure:` recognition, `verify:`, `stop:`, claim IDs (`@W..`, `@E..`, `@C..`, `@T..`, `@ED`), and a bespoke technical illustration specification.
- [Primary sources](evidence/sources.tsv) (74 dated agency/specialist references) and [claim evidence](evidence/claims.tsv) (100 claim rows across five packs) record source identity, revision/check date, exact section locator, applicable conditions, supporting statement, limitations, conflicting evidence, editorial note, and required specialist reviewer.
- [Diagram specifications](evidence/diagram-specs.json) retains all 129 generation specifications (cutaway views, exploded component views, material cross-sections, mechanism diagrams, comparative configurations, environmental relationships, decision trees, and failure-mode analyses), complementing 11 preserved hand-crafted cross-sections and 42 sequence schematics.
- [Asset manifest](reader/asset-manifest.json) binds all 182 editable local-only SVGs to SHA-256 digests and provenance. Authentic documentary photographs remain separately registered in [photo provenance](evidence/photos/manifest.json) and [photo requirements](evidence/photo-requirements.tsv); none are classified as approved diagnostic evidence.
- [Page manifest](reader/page-manifest.json) classifies every page as `Adapted historical material`, `New manuscript`, or `Reconstruction draft`, while enforcing a fixed `publication: HOLD` gate.

## Reproducible build and verification

From the repository root, using [review-requirements.txt](../production/review-requirements.txt) and local Chrome/Chromium:

```sh
python scripts/test_foundation_controls.py
python scripts/build_foundations.py
uv run --with-requirements production/review-requirements.txt python scripts/verify_foundations.py --foundations-only --formats letter,a4 --write-zone-pdfs --name foundations --axe /path/to/axe.min.js
python scripts/check_foundations.py --write-package
```

All reader navigation, search, diagrams, zone readers, and directory links operate offline from local files with zero network requests. Print PDFs are single-card-per-sheet bookmarked proofs for editorial and specialist review only; publication remains on `HOLD`.
