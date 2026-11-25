# A02 production controls and verification

## Authoring and safety controls

The compiler now requires a direct claim reference on each action and stop in an expanded manuscript batch. Editorial readbacks and verification can retain `ED`. Legacy statements stay traceable through the [editorial-only audit](EDITORIAL_ONLY_AUDIT.csv). The coverage audit distinguishes direct primary support, a narrower corrected claim, partial support, editorial application and unresolved evidence. Each high-consequence sentence should carry its own source conditions, and the reviewer should be able to find the precise source section offline from the manuscript metadata.

Four regressions extend the existing 25 tests. They cover CO evacuation delayed by equipment shutdown, a fixed lay delay before CPR, conflicting tourniquet placement rules, and ED-only actions in expanded batches. The controls address tested language patterns. Maintain independent editorial review for synonyms, compound statements and false reassurance in figures, captions and titles.

The original scope regression compares all 16 zones against the frozen matrix. It blocks identifier drift in the active matrix and handoff. The separate A02 receipt checker verifies the compiled directory, the assertion and figure inventory, and open hold coverage. Revalidate any new source pack and page-ID range before a zone is generated. Z05 wild foods extends to `Z05-P135`; Z08 materials and Z10 medicine are separate.

## Figures and photography

Screen all SVG label boxes in Chromium with `--fail-layout`. Compare geometry fingerprints within each figure family. Reuse a schema when the same relationship genuinely recurs. A distinct path or text string alone gives little assurance of instructional value. Use a conceptual layout for physical content if a technical drawing still requires expert validation. Keep model and orientation visible, keep installation illustrations separate from safety-boundary material, and apply the correct caution without relying on color alone.

For each row of the [photo plan](DIAGNOSTIC_PHOTOGRAPHY_ACQUISITION_PLAN.csv), begin with the recorded documentary or diagnostic need. Ask for the relevant scale, orientation, site, date, model and related series. Record the item-specific owner/rights statement, source and download URLs, rights scope, attribution, access date, subject limitation and SHA-256. Keep provider bytes. Save any crop or annotated version separately with source linkage. Record training, simulation, consent and patient privacy where relevant. Have the responsible expert validate the photographed subject and conditions before claiming diagnostic use. When rights or the diagnostic facts are uncertain, retain the candidate as open.

Two acquired documentary records are credited to [CDC PHIL / Lauren Bishop](https://wwwn.cdc.gov/phil/Details.aspx?pid=31569) and [NOAA / NWS Video Lab](https://www.weather.gov/safety/ripcurrent-photos). The associated assets illustrate context in the archive. They do not settle the registered diagnostic needs.

## Build and QA sequence

```sh
python scripts/test_foundation_controls.py
python scripts/build_foundations.py
python scripts/audit_foundation_vectors.py foundations /absolute/path/to/new-receipts --fail-layout
python scripts/verify_foundations.py --browser-only --name A02 --axe /absolute/path/to/axe.min.js
python scripts/print_foundations_tagged.py
python scripts/print_foundations_tagged.py --verify-only
python scripts/check_foundations.py --write-package
python scripts/check_foundations.py
python scripts/check_a02_audit.py
```

Run browser, figure and PDF checks using the production requirements and Chromium. Archive the HTML receipts, sampled true-size views and print digest records with each batch. Verify the downloaded package from the checked commit by SHA-256, ZIP CRC and member checksums. The observed pipeline size is 668 cards. As the edition grows, keep checking Chromium memory, tag and bookmark completeness, archive size and browser accessibility. Physical print and independent assistive-device tests stay assigned to H14. Maintain publication HOLD.
