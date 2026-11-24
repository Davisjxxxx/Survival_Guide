# Foundational production edition

[Open the offline reader](reader/index.html) or use the [pilot proof](proofs/pilot.pdf). The first twelve review drafts adapt eleven B012 pages and the B003 rain-catchment plate. Original Track B text and illustration sources remain in their versioned historical paths. The production branch adds its own standalone edition using the original library stylesheet and search script.

## Authoring and evidence

- `manuscripts/*.cards` contains editable, stable page IDs, instructional objectives, applicability, equipment, action and verification steps, stop conditions and visual instruction. Use `@ED` for an explicit editorial inference or workflow check. Use primary claim IDs for factual statements.
- [Primary sources](evidence/sources.tsv) and [claim evidence](evidence/claims.tsv) provide the five dated packs with exact section labels, applicability and source-supported conclusions. The statement references under each card connect to these rows. Product selection, jurisdiction, audience and procedure scope still require review.
- [Track B crosswalk](evidence/track-b-crosswalk.tsv) maps the recovered chapter pages and historical proofs to the zone architecture. Range mappings preserve original versus revised documents. Only cards with actual source lineage get adaptation credit.
- [Asset manifest](reader/asset-manifest.json) identifies editable original diagrams, SHA-256 and subject review status. SVGs depict declared concepts or relationships. Authentic photo requirements remain separate.
- [Page manifest](reader/page-manifest.json) records the rendered inputs and review state. The builder issues editorial review material only. It carries forward explicit approval and publication holds from the historical Gate A decisions. Source URL collisions, missing fields, unresolved IDs, image checks, and one-sheet print integrity are checked. Human custody pinning, release approval, legal freshness and photo identity remain governed by the original Gate A record.

From the repository root, with the dependencies in [review-requirements.txt](../production/review-requirements.txt) and a local Chrome or Chromium installation:

```sh
python scripts/build_foundations.py
python scripts/verify_foundations.py --name pilot --batch 01-pilot --axe /path/to/axe.min.js
```

The reader itself needs only a browser. Source links require internet access when opened. The content, diagrams, evidence summaries, navigation and search work from local files. The PDF is a print proof for editorial and specialist inspection.
