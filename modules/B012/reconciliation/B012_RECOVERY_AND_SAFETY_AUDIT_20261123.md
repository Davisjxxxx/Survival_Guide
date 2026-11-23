# B012 Minnesota Winter Survival: Recovery and Safety Reconciliation

**Audit date:** 2026-11-23
**Review status:** BLOCKED / draft only. This is an editorial and structural audit, not a field test, image-authentication exercise, medical approval, or publication clearance.
**Authoritative repository:** https://github.com/Davisjxxxx/Survival_Guide
**Review branch:** review/b013-b014-field-drafts-20261122
**Imported checkpoint:** https://github.com/Davisjxxxx/Survival_Guide/commit/b7c0e8c0854c2b49c123b904c204e5b6f53f5c54

## Exact source and custody

The existing original 28-page HTML is preserved byte-for-byte in:

imports/local-downloads/20261123T145517Z-405239/B012_28_PAGE_OFFLINE_DRAFT_READER.html

- SHA-256: 1596b10534fa6d3faac685a050311805e7ac386cf77fd93d29ac93db61638278
- The digest matches the imported GitHub IMPORT_MANIFEST.tsv.
- The reader includes 28 ordered P01–P28 records in embedded JSON (b012_data).
- Editorial group codes A:6, B:6, C:5, D:5, E:6. These are draft provenance labels, **not** scientific source citations.
- Its page fragments contain 51 embedded raster illustrations and 22 inline SVGs. All 51 embedded data-image payloads passed basic base64 decoding; no external image, CSS or script asset URLs occur in the page fragments. This proves packaging structure, **not** correctness, image origin, or field usability.
- Original text_digest fields exist on all pages. Their generation algorithm and linkage to source files have not been independently validated.

Recovered artifacts already in GitHub include a production ZIP, two B012 proof ZIPs, two B013 ZIPs, and a ten-mechanism-plates PDF. None were overwritten by this work.

## Archive evidence

- B012_Winter_Survival_Production_Package.zip: 12 central-directory entries, including B012_SOURCE_REGISTER.csv, B012_PAGE_MAP.csv, B012_ASSET_REGISTER.csv, production brief, review gates, workbook and build scripts.
- B012_Winter_Proof_2_Offline.zip: 17 entries, including *original* pages/P13.html through pages/P18.html and one staged bedding image.
- Examined the decompressed original P13–P18 HTML page files in that proof archive. Each still displays the three literal expressions {html.escape(bad)}, {html.escape(fix)}, and {html.escape(limit)}.
- B013_Ice_Safety_Compact_Reader.zip: nine entries including editable page content, source register, visual asset register, render QA and SHA256SUMS.
- B012_Winter_Visual_Proof_1.zip and B013_Ice_Safety_Stage2_Offline.zip: original bytes saved to GitHub. All five imported ZIP archives now pass CRC and safe-path integrity checks in GitHub CI; this does **not** verify visual subjects, copyright permissions, safety instructions or expert review.

Thus, the 18 visible P13–P18 gaps are inherited from the earlier source proof, not introduced by the 28-page reader assembly.

## Directly recovered editable originals (GitHub-verified)

- Seven unmodified source/research files have been extracted from the B012 production ZIP under modules/B012/recovered_source/production_package.
- Nine unmodified proof/source assets have been extracted from B012_Winter_Proof_2_Offline.zip under modules/B012/recovered_source/proof2, including original P13–P18 HTML, the source/review ledger and staged storyboard JPG.
- Every recovered file was checked against its originating ZIP member (exact bytes) by scripts/verify_recovered_downloads.py. Both pull-request and push integrity workflows passed at commit 56ef52cb309c5e6e9105fac88cc30edaad8e0411.
- The original B012_SOURCE_REGISTER.csv contains **17 source leads** (S01–S17), not 17 individually validated page claims.
- B012_ASSET_REGISTER.csv contains **143 planning slots**. All 143 remain marked NEEDED and NO_PUBLICATION; the register records rights_verified=NO and subject_verified=NO throughout. These are asset requirements, not acquired or validated photographs.
- Six photographic candidate leads are cataloged, all with status SOURCE_PAGE_ONLY. The candidate URLs are **not permissions or diagnostic confirmation**.
- The reader's 51 embedded raster images and 22 SVGs are separate draft renderings, not evidence that the 143 asset requirements have been satisfied.

## Critical findings and dispositions

| ID | Severity | Observation | Action and status |
| --- | --- | --- | --- |
| B012-F001 | Critical editorial | P13–P18 contain 18 unresolved expressions in FAILURE / CHANGE COURSE / LIMIT fields, three per page | Block release. Six-page editorial overlay saved separately; approval pending |
| B012-F002 | High clinical | P25 proposes frostbite water at 37–40°C (99–104°F). Wilderness Medical Society 2024 summary specifies **37–39°C (98.6–102.2°F)** and protection against refreezing | Do not silently revise archived text. Independent first-aid review and source-linked correction required |
| B012-F003 | High evidence | The main HTML does not expose page-level source IDs, licensing records or specialist approval | Original production source/asset/photo registries are now recovered; map each high-risk claim to dated supporting source evidence, page ID, rights and reviewer separately |
| B012-F004 | High visual | Staged illustrative scenes are not real frostbite images, measured thermal results, snow-load tests, or diagnostic identification images | License/provenance and independent technique/diagram review before public release |
| B012-F005 | High procedural | Snow trench, snow cave, leaning shelter, and earth/stone shelter pages depend on local snow/soil strength, heat, ventilation, exit and weather assumptions | Keep no-gear fallback and stop conditions. Require qualified snow/structural assessment |
| B012-F006 | Medium coherence | P07 vs P24 (hypothermia) and P08 vs P25 (frostbite) overlap but differ in operational detail | Make one authoritative claim register; keep both reading levels if consistent |
| B012-F007 | Medium build | B012 has a source reader, but no canonical per-page standalone source set currently checked into modules/B012 | Use a reproducible non-destructive extraction/build pipeline; never regenerate archived originals in place |
| B012-F008 | High release | Existing B013 ice-safety illustrations and B014 navigation entries have different source/review states | Cross-reference only; do not promote unverified field instructions |

## Source-informed technical checks (not approval)

1. **Hypothermia and cold exposure:** CDC lists confusion, fumbling, slurred speech and drowsiness as serious signs; serious hypothermia requires medical assistance. Reference: https://www.cdc.gov/winter-weather/prevention/
2. **Frostbite:** CDC warns against rubbing and direct heat, and advises prompt medical assessment. Reference: https://www.cdc.gov/winter-weather/prevention/preventing-frostbite.html
3. **Frostbite treatment precision:** WMS 2024 summary specifies 37–39°C water in the appropriate scenario and requires prevention of refreezing; page P25 currently uses 37–40°C. Reference: https://wms.org/magazine/1494/Frostbite-Summary-2024/default.aspx
4. **Winter shelter and signaling:** NOAA/NWS recommends shelter, staying dry, limiting overexertion and melting snow before drinking. These summaries are not structural certification for a field-built snow cave. Reference: https://www.weather.gov/safety/winter-during
5. **Water treatment:** CDC recommends clear water at a rolling boil for one minute (three minutes above 6,500 feet), and explicitly notes that boiling does not remove fuels, chemical contaminants or radioactive substances. The P22 distinction between melting and microbial treatment is directionally consistent; source and execution review still required. Reference: https://www.cdc.gov/water-emergency/about/index.html
6. **Minnesota ice:** MN DNR states ice cannot be judged reliably from one visual or thickness cue; no ice is guaranteed safe. B012/B013 cross-references must retain that boundary. Reference: https://www.dnr.state.mn.us/safety/ice/index.html

## Non-destructive correction route

- Preserve original HTML, ZIPs, PDF and IMPORT_MANIFEST.tsv unchanged.
- Maintain all P13–P18 candidate correction text in B012_P13_P18_EDITORIAL_OVERLAY_DRAFT.json; none is certified.
- scripts/audit_b012_recovery.py audits the original reader and optionally produces a **separate** labeled review copy. The original page text_digest values are retained as original provenance metadata, not represented as digest proofs for modified text.
- Re-run source checks, reader navigation/print/phone QA, snow-shelter mechanism review, frostbite clinical review, ZIP CRC and rights checks before requesting approval.
- Do not merge the draft PR or release the manual until gate owners approve. No publication authorization is implied by successful software tests.

## Local read-only validation (after cloning this branch)

python3 scripts/audit_b012_recovery.py \
  imports/local-downloads/20261123T145517Z-405239/B012_28_PAGE_OFFLINE_DRAFT_READER.html \
  --csv-output /tmp/B012_PAGE_REGISTER.csv \
  --json-output /tmp/B012_AUDIT.json

To build a distinct, unapproved preview file, add:

  --overlay modules/B012/reconciliation/B012_P13_P18_EDITORIAL_OVERLAY_DRAFT.json \
  --review-output /tmp/B012_28_PAGE_RECONCILED_REVIEW.html

No programmatic scan establishes factual, medical, engineering, image licensing or offline field performance.
