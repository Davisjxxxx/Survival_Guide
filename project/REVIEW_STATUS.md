# B013/B014 retention and review checkpoint · 2026-11-22

All project artifacts created in this stage are stored in this review branch. See `project/ASSET_INVENTORY.json` for SHA-256 and Git blob SHA checksums.

## Contents
- B013 ice safety: preserved 14-page reader; expanded 18-page reader; production ZIP; 8 editable SVG diagrams; screenshot contact sheet and images; research claim ledger, source register and image asset manifest; build and verification scripts.
- B014 North Woods navigation: research continuation packet; text research, page/visual register, source register; editable decision diagram and preview; build script.

## Release gates
**REVIEW / NOT APPROVED FOR FIELD USE OR PUBLICATION.**
- Field photos and independent qualified safety review outstanding.
- Staged scenic images are not real-world measurements or verification of safe ice conditions.
- ZIP content integrity checked locally and passed.
- Original file bytes uploaded as Git blobs; Git SHA match checked for each file.
- Playwright interactive browser test attempted but the sandbox blocked local server requests with `ERR_BLOCKED_BY_ADMINISTRATOR`; this is an environment blocker, not a recorded product test pass.
- Full browser QA, cold-weather field validation and publication acceptance remain pending.

## Non-destructive process
Keep all original sources and generated revisions. Continue on review branches, preserve the reviewed base, use an explicit owner approval gate for any public field-use release. Do not overwrite earlier safety content without retained history.

## B014 stage 1 continuation · 2026-11-22
- Added a separately staged P11–P20 standalone reader, ten original editable vector diagrams, source/claim links, build and browser verification scripts, two responsive screenshots, and an independent ZIP package.
- Desktop Chromium smoke test passed page selector, keyboard arrows, next-page navigation and embedded image checks. Mobile 390 px smoke test passed without horizontal overflow.
- Local ZIP integrity passed. All 21 new file Git hashes matched before tree integration.
- These pages have **not** been reconciled with the original B014 P01–P10 source; publication remains blocked.
- Safety and map/right-to-use gates remain blocked. See `modules/B014/stage1/B014_STAGE1_QA.md`.

## B012 Winter Survival recovery and reconciliation · 2026-11-23

- All seven matching local downloads were imported from Ubuntu and SHA-256-recorded in imports/local-downloads/20261123T145517Z-405239 (commit b7c0e8c0). The unrelated Career Search CSS files were excluded.
- The B012 28-page offline draft reader is byte-identical to its recorded SHA-256. It has 28 ordered pages, 51 embedded raster illustrations, 22 inline SVG diagrams and no external page-fragment assets.
- **Critical inherited defect:** P13–P18 each contain three unresolved safety text placeholders (18 total). The same placeholders exist in the original B012_Winter_Proof_2_Offline.zip page sources. Original material remains unchanged; six candidate correction triplets are separately retained in modules/B012/reconciliation/B012_P13_P18_EDITORIAL_OVERLAY_DRAFT.json.
- **Clinical discrepancy:** P25 has 37–40°C for water-bath frostbite rewarming; WMS 2024 guidance specifies 37–39°C when field rewarming is otherwise appropriate. Independent medical review is required.
- The original B012 production archive's 17-source register, 143-slot asset register, six photo candidates, page map, review gates, production brief and README are now separate, byte-verified GitHub source files. Six individual proof2 shelter pages, its review ledger, asset status and storyboard image were also recovered without modification (16 files total).
- Every original asset-register row remains NEEDED and NO_PUBLICATION, with rights_verified=NO and subject_verified=NO. These are requirements, not 143 acquired assets; diagnostic photos and specialist review remain outstanding.
- scripts/audit_b012_recovery.py audits B012 and can generate a distinctly labeled unapproved preview without overwriting the original. scripts/verify_recovered_downloads.py verifies all imported SHA-256s, all ZIP CRCs and the recovered source members' exact byte identity.
- GitHub Actions recovery-integrity workflow has passed on both PR and push events after B012 source recovery (e.g. run 45207887297). A test pass only validates the software/storage checks, not medical or field safety.
- The detailed audit, 28-page register, rights/visual gap matrix and P25 clinical hold are in modules/B012/reconciliation. **No merge, deployment, publication or specialist approval.**

## Next high-priority gates

1. Obtain specialist review of P13–P18 structural/snow/ventilation decisions and P25 frostbite wording.
2. Map high-consequence B012 claims to individual records S01–S17 and acquire authentic, licensed visual evidence for the 143 planned slots as necessary; do not equate embedded staged images with approved real photos.
3. Preserve B013 ice safety and B014 navigation separately; recover B014 P01–P10 source material and reconcile before constructing a single B014 reader.
4. Recheck source and image rights, mobile/print accessibility, and human-reviewed field mechanics before seeking any release authorization.
