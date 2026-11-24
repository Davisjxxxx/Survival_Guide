# A01 production controls

## Controls implemented

| Area | Change and verification |
|---|---|
| Scope and stable IDs | The compiler uses the original 16-zone allocation and accepts two- or three-digit page numbers as required. Z05 can reach P135. Duplicates, noncanonical numbers and IDs beyond the zone allocation fail. A reconstruction-only zone remains a starter until it has production pages. |
| Evidence packs | Original pack coverage remains required. New zones can add domain-specific packs. Every reference resolves to a registered claim. Evidence review records expose each linked statement, current source locator, applicability and disposition. An `ED` reference is an editorial decision and must remain auditable as such. |
| Combustion language | Negation and warnings are scoped locally. A prohibited instruction in one sentence fails even when a different sentence contains a warning. This is a regression guard for checked patterns. |
| Diagram contracts | The generator validates the exact type, keys and list lengths. Fields that would previously fall through to generic art now fail. Branch and force-redirect drawings support meaningful relationships. Chromium records real text bounds and collisions. |
| Display and offline custody | Inline emphasis renders as escaped semantic HTML. The compiler copies the historical reader into the extracted package with byte-for-byte custody so its directory link works offline. |
| Print and bundle | The tagged renderer produces whole-document proofs before adding bookmarks. It verifies text, bounds, language, tags, figure alternative text and outline destinations after reopen. The integrity check ties proof receipts to SHA-256 and checks every archive member against the retained file. |

Six targeted regressions were added to the original 13. They cover negation scope, missing figure fields, truncated figure lists, escaped emphasis, ID boundaries and active-zone inference. Run both the static and rendered checks. Keep dated originals from the relevant commit under Git custody before making corrections.

```sh
python scripts/test_foundation_controls.py
python scripts/build_foundations.py
python scripts/verify_foundations.py --browser-only --name A01 --axe /absolute/path/to/axe.min.js
python scripts/audit_foundation_vectors.py foundations foundations/audit
python scripts/print_foundations_tagged.py
python scripts/check_foundations.py --write-package
python scripts/check_foundations.py
```

Browser, vector and print commands use local Chrome or Chromium and `production/review-requirements.txt`. Run vector checks into a new receipt directory for later batches to preserve A01 observations. Digital and physical print evidence should carry explicit dates and conditions.

## Required editorial review for successive batches

Put each new high-consequence assertion on its own sentence or line, including decisive thresholds, contraindications and stop conditions. Bind each to a specific source section and applicability. Separate normative guidance, source observations, mathematical derivation and editorial implementation. Require consistent units and conditions across actions, captions, warnings, excerpts and quick-reference tables. Manufacturer claims need the exact compatible model and instruction. Local rules need jurisdiction and a date. Failed, changed or ambiguous source retrieval stays open in the register. A successful fetch or compiler run does not grant source approval.

Compare repeated geometry for its instructional value. Draw critical physical relationships and annotate orientation, force direction, contact surfaces and failure states when these details change the safe decision. Keep conceptual, documentary, staged and diagnostic classes explicit. Review a full-size and reduced-size render, and preserve a grayscale sample for each new instructional figure family. Recheck accessible reading order, contrast and zoom for both HTML and print. Arrange qualified review when the instruction depends on an unresolved clinical, engineered, species, regulatory or rescue judgment. Leave publication on HOLD.
