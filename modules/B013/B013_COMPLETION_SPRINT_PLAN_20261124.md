# B013 Minnesota Ice Safety — Completion Sprint Plan (2026-11-24)

## Verified repository baseline
- Branch: `review/b013-b014-field-drafts-20261122`; draft PR #1; do not merge or publish without approval.
- `modules/B013/reader/B013_Ice_Safety_14_Page_Reader.html` preserved.
- `modules/B013/reader/B013_Ice_Safety_18_Page_Reader_REVIEW.html` present, 18 of 18 draft pages.
- P15–P18 Stage 3 have eight original SVGs, a screenshot contact sheet, claim/source/asset registers, a ZIP review package, build and verification scripts.
- Source and rights records are separate from reader by design.
- The Stage 3 QA record reports structural checks, but the project review status records a previously blocked browser run. Do not claim comprehensive browser testing until a fresh run is evidenced.
- Stage 3 manifests identify four pending field photographs (one each P15–P18). The prior 14-page handoff reported 24 outstanding real-photo requirements; reconcile against the complete asset register before treating this count as current.
- Neither specialist ice-rescue review nor medical aftercare review is signed off.

## Sprint B013-C1 — Inventory and evidence reconciliation
Tasks:
1. Establish SHA-256 and Git commit baseline for 14-page HTML, 18-page HTML, production ZIP and each original SVG; retain all originals.
2. Compare P01–P14 and P15–P18 page-by-page; check page numbers, navigation, text preservation and duplicate/contradictory advice.
3. Compile a single P01–P18 claim ledger and a master photo/diagram register. Each image: role, caption, original/staged/photo classification, provenance, license, rights status, and review owner.
4. Reconcile the 24 unacquired-photo estimate with the four Stage 3 placeholders and earlier asset registers. Record unique slots, not guessed totals.
Acceptance: reproducible inventory; no source loss; all 18 pages uniquely mapped; zero untracked high-risk claims. Release: BLOCKED.

## Sprint B013-C2 — Safety and source review
Tasks:
1. Check current Minnesota DNR ice thickness, ice conditions, self-rescue, and helping-others guidance against every high-risk sentence and diagram.
2. Review 4-inch guidance strictly as a conditional minimum for NEW, CLEAR ice, not a route permission. Ice is never fully safe; thickness varies within a water body.
3. Assign P15–P16 ice-fishing/gear content to ice-rescue and regulatory review; do not present improvised fishing or ice holes as validated survival techniques.
4. Assign P18 cold-water immersion, self-rescue, emergency handoff and aftercare to qualified ice-rescue and medical specialists.
5. Record sources, access date, source excerpts or claim pointers, reviewer disposition and unresolved claims in a claim-level ledger.
Acceptance: every high-risk claim source-traceable; open safety questions explicitly HOLD; qualified reviewer sign-off recorded before field release. Release: BLOCKED until independent reviewers sign off.

## Sprint B013-C3 — Visual rights, usability and QA
Tasks:
1. Do not substitute AI-generated scenic imagery for real observations of safety-critical ice conditions. Obtain authentic photos with usable rights and subject-level validation, or redesign specific photo-dependent claims as clearly labeled schematics with review approval.
2. Check line work, contrast, captions, alt text, responsive layout, keyboard controls, logical reading order, print pagination, offline functionality and no external dependencies.
3. Run Stage 3 verifier; desktop and 390px mobile browser interaction checks; print-to-PDF layout review; package unzip/rebuild checksum validation; archive CRC. Record environment failures as untested rather than passed.
4. Confirm no links imply real-time lake safety, ice-clearance certification, or legal fishing exceptions.
Acceptance: automated test report; manual visual/accessibility review; rights and authenticity ledger; no unresolved P0/P1 safety defects. Release: BLOCKED pending specialist approval.

## Sprint B013-C4 — Review freeze and sign-off
Tasks:
1. Produce one versioned 18-page review reader, reproducible source build, full manifest, sources, editable diagrams, screenshots, ZIP archive, verification report and open-issues register.
2. Commit and push every artifact to GitHub; re-read branch ref and verify uploaded hashes. Link PR #1; do not overwrite 14-page original or move main.
3. Independent ice/water rescue and medical reviewer dispositions; regulation check; owner acceptance. Any unresolved severe issue remains explicitly HOLD.
4. Only with affirmative documented approval: separately authorize a publication merge/deployment. Until then all packages labeled EDITORIAL DRAFT / NOT FOR FIELD USE.

## Practical finish definition
- **Editorial package complete:** can be achieved without external sign-off if C1–C3 QA pass; retain as review-only.
- **Field/publication-ready:** requires verified real-photo substitutions or approved schematics, safety/medical/regulatory reviews, full QA and owner authorization. No assumed same-day approval.
- Other workstreams B012 and B014 remain separate, with their own release blockers.

## Primary source checkpoints
- https://www.dnr.state.mn.us/safety/ice/index.html
- https://www.dnr.state.mn.us/safety/ice/thickness.html
- https://www.dnr.state.mn.us/safety/ice/check-ice-thickness.html
- https://www.dnr.state.mn.us/safety/ice/ice-formations-conditions.html

Status: PLAN / REVIEW ONLY. This document does not assert that outstanding tests, reviews or acquisitions are complete.
