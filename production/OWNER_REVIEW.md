# Survival Field Encyclopedia · owner review edition

Open the [offline directory](../reader/index.html) after extracting the ZIP. Search includes the text of the illustrated pages and earlier proofs. The four emergency links also appear on the first sheet of the [numbered print proof](Survival-Field-Encyclopedia-Review.pdf). See the [outstanding issues and owners](OUTSTANDING_ISSUES.md) before making any acceptance decision.

## Edition contents

| Section | Retained material |
|---|---|
| B012 Winter Survival | 28 pages, including the P13–P18 correction overlay and consistent P08/P25 frostbite advice |
| B013 Minnesota Ice Safety | 18 pages, including separate witness and immersed-person actions on P18 |
| B014 North Woods Navigation | Ten supplemental pages, P11–P20, including the Ely map examples |
| Earlier proofs | B003 field procedure cards, B007 wood selection, two recovered B007A cordage plates, B008 friction fire and B009 water (original and revised), B010 mechanism plates |

The directory has 126 searchable entries. The print edition has 142 physical sheets including its directory. Standalone historical readers and original source packages retain earlier wording. Use reader/ or the consolidated PDF to inspect the corrections.

See the [safety source review](SAFETY_SOURCE_REVIEW.md) for specific editorial decisions and primary references.

## Evidence and custody

- The review continues Git checkpoint 56645a0b2fb92421500511c058dc58d0503622f2. Original B013 reader subtrees P01–P14 match the expanded standalone edition. Each page and navigation entry was checked. See [baseline hashes](evidence/ice-baseline.csv), [page comparisons](evidence/ice-page-comparison.csv) and the [rebuild comparison](evidence/standalone-rebuild.json). ZIP timestamps can change the container digest while every member matches.
- The [B013 claim ledger](evidence/ice-claim-queue.csv) includes the source block, its effective edition wording, agency pointers, AI assessment and reviewer assignment. Mobile repetitions are recorded. P18 replaces the two historical figures with one two-role diagram and removes four repeated instructions from the old mobile figure. The [visual register](evidence/ice-visual-register.csv) retains separately named requests and their provenance.
- B013 photo requirements reconcile as 54 original whole/detail/failure identifiers on P01–P18, 24 more specific identifiers on P09–P14, and four later field-photo identifiers on P15–P18. All 82 identifiers are distinct. The earlier estimate of 24 covers only the middle register. A P14 dry-land rehearsal can address more than one request if its detail and subject are independently accepted. A broad P15–P18 photo request does not itself establish a distinct scene. Three B013 documentary images are additions with separate IDs. No acquired image was counted against those requirements.
- The [photo ledger](photos/provenance.json) identifies the five original agency files and the [map note](maps/README.md) identifies the original GeoPDF. Previously staged visuals retain their draft classifications. The full Git branch also retains production archives and the [original master plan](../project/historical-scope/Survival_Field_Encyclopedia_Master_Sprint_Plan_v1.md).
- Source recovery compared the review branch and available Git history, the local Gate A checkout and historical review, and Downloads. The top-level Downloads check included 107 ZIP directories and 107 PDF candidates, including page-count and first-page checks for possible primer volumes. The 9- and 10-page survival hits were later B008/B010 proofs. No original B014 P01–P10 file was identified. Review history and planning are preserved separately from reading material.

## Rebuilding and checking the review

To check an extracted package offline, run `sha256sum -c PACKAGE-SHA256.txt` in its top directory. To rebuild from a Git checkout with the edition files tracked, use Python 3.13, the dependencies in review-requirements.txt, Poppler (pdftotext and pdftoppm), and local Chrome or Chromium. The accessibility check takes a local axe-core 4.14.1 script. A reader only needs the extracted files and a browser.

```sh
python scripts/verify_recovered_downloads.py
python scripts/verify_b012_claim_triage.py
python scripts/build_review_library.py
python scripts/reconcile_ice.py
python scripts/test_review_library.py
python scripts/audit_review_accessibility.py /path/to/axe.min.js
python modules/B013/build/verify_b013_stage3.py
python modules/B014/build/verify_b014_stage1.py
python scripts/print_review_library.py
python scripts/check_print_proof.py
python scripts/package_owner_review.py
```

The [browser receipt](evidence/browser.json) covers the 56 chapter pages at three widths, local navigation, keyboard skip, search, image loading, page errors and HTTP requests. The [axe receipt](evidence/accessibility.json) covers 58 HTML files and lists incomplete checks per file. Full-page desktop contact sheets cover all 56 chapter pages. The [print contact sheet](evidence/print-contact.jpg) samples the actual PDF, including the directory. Test evidence comes from the review workstation. Both chapter approval and public release require the decisions in the outstanding-issues register.
