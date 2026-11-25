# Opus continuation · Wave 2C

The qualified input is the A04 draft stacked on `807ed366018c022cd6387352ad8442a5a32367c7` from PR #9. Start from the final A04 draft PR head referenced by the A04 executive report and compare it with the remote ref before editing. Keep publication HOLD and preserve original and independently qualified versions.

## Work to take forward

| Workstream | Scope | Start here |
|---|---:|---|
| Technical plates | 372 unattempted plus 3 returned reconstructions | [Technical queue](WAVE_2C_TECHNICAL_QUEUE.csv). Start with the three returned examples and smallest coherent safety-critical family. |
| Cold-water posture | One previously drawn plate awaiting staged authentic evidence | [Qualification row Z12-P66](V01_V02_VISUAL_QUALIFICATION.csv). Require a matched vest, body pose, airway and waterline under an instructor-approved controlled setup. |
| Realistic scenes | 70 non-diagnostic allocated, 2 pilot candidates, 68 still to produce | [Brief qualification](REALISTIC_ILLUSTRATION_QUALIFICATION.csv). Built-in ImageGen produced the two pilots. Use that capability only where available without external charges. Historical Gemini capacity remains unverified after its 503 failure. |
| Clinical illustrations | 12 specialist holds | Qualified clinicians define depicted technique, anatomy, decision conditions and imagery. Preserve the clinical and diagnostic restrictions. |
| Authentic diagnostic evidence | 157 active requests, zero diagnostic approvals | [Acquisition register](../../visual/DIAGNOSTIC_PHOTOGRAPHY_ACQUISITION_REGISTER.csv) and [A04 photo audit](PHOTOGRAPHIC_EVIDENCE_AUDIT.csv). Prioritize paired toxic lookalike views and fully verified vouchers. |
| Evidence | 145 items still open in the 172-row V02/V03 queue | [A04 source decisions](EVIDENCE_RESOLUTION_VERIFICATION.csv). Twenty-three escalations are still partial or unsupported, six closures were reopened, and 116 inherited records were outside the focused review. |
| Atlas | 75 entries pending owner decision | [Comparison rationale](ATLAS_LAYOUT_RECOMMENDATION.md). Use the eight working offline comparisons as prototypes. |

## Production acceptance

1. Group four to eight plates by the same actual visual relationship, such as a flow path, exploded seal stack, tool contact, or map reference. Establish a source-supported reference and acceptance cue before drawing. Reserve shared components for geometry that really is shared.
2. Anchor arrows at their physical point of application. Distinguish motion, load, reaction and direction. Use a measured comparator when a numerical angle or scale is shown. For a quantitative illustration, validate the drawn geometry separately from checking the label text.
3. Use the assembled equipment, material change or visible failure as the subject. Remove card prose that merely duplicates it. Label no safety rating, threshold or diagnostic identity without support applicable to the exact view. Make opposing cases understandable in grayscale.
4. Inspect the actual narrow and desktop page, both print sizes, and informative alt text. Verify fit, label separation, reader action, stop conditions and original custody. Keep the rendered comparison and exact source locator with the asset.
5. Route clinical techniques, ice/water rescue posture, structural loads, rigging mechanics, hazardous materials and regulated installation boundaries to Astra or the named qualified reviewer before batch approval. Opus can implement source-confirmed editorial corrections, production geometry, QA, packaging and routine rights/acquisition work.
6. For authorized diagnostic acquisition, match the accession, exact item-level license, source file, date, geometry views, context and scale. Keep unedited provider bytes and apply EXIF orientation only in display derivatives. Flag iNaturalist as observations and partial vouchers as limited leads. Label generated media as illustration and preserve the prompt, model metadata and editable annotations.
7. For images needing an advanced model, run a one- or two-page trial with exact shot instructions and negatives. Review action, equipment, viewpoint, geometry and misleading inferences before committing to a batch. Stop clinical or diagnostic generations at briefing until the required evidence exists.

## Commands

Run from the repository root with the established Python production environment that has Playwright, Chromium, Beautiful Soup, PyMuPDF and Pillow. Pass the local axe-core script to browser QA.

```sh
python scripts/test_foundation_controls.py
python scripts/build_foundations.py
python scripts/audit_foundation_vectors.py foundations /tmp/sfe-vector-qa --fail-layout
python scripts/print_foundations_tagged.py
python scripts/verify_a04_visual.py --axe /path/to/axe.min.js
python scripts/check_foundations.py --write-package
python scripts/check_foundations.py
python scripts/check_a04.py
```

Field, physical print and assistive-device verification, PDF/UA validation, scientific release clearances and publication authorization remain separate.
