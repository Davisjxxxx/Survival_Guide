# SURVIVAL FIELD ENCYCLOPEDIA — ASTRA CLI HANDOFF

**Handoff version:** 1.0  
**Issued:** 2026-11-08  
**Status:** IMPLEMENTATION AUTHORIZATION FOR SCAFFOLDING AND PRODUCTION PIPELINE ONLY. Content must be approved in ChatGPT before publication.  
**Audience:** Astra CLI operating in the user's local development environment.

## 0. Division of responsibility — non-negotiable

**ChatGPT, GPT-6 High or Extra High, owns:**
- Deep research, source evaluation, and factual claims.
- Original procedural drafting and technical analysis, including safety, regional applicability, and legal limitations.
- Selection of references and verification status for real photographs and species/specimen identification.
- Editorial tone, glossary terminology, content requirements, content approval, and final safety sign-off.
- Coverage gap and risk analysis. ChatGPT supplies approved chapter packs and changes as files or paste-in text to the local repo.

**Astra CLI owns:**
- Project scaffolding, repository structure, schemas, validation tools, build automation, and version control.
- Source and image asset cataloging, rights metadata, provenance checking, and quarantining unverified items.
- Technical diagrams ONLY from ChatGPT-approved specifications; layouts, maps, flowcharts, tables, worksheets, and infographics.
- PDF and optional print-friendly/EPUB/HTML production, bookmarks, cross-references, index, accessibility, render QA, link checking, and automated tests.
- Packaging approved content, generation of proofs for review, publishing only after the approval gate.

**Never** invent survival claims or write safety-critical field advice to fill gaps. Never substitute a plausible diagram for a factually verified diagram. Never silently rewrite approved source text. Never publish unreviewed AI-generated botanical/mushroom/rock IDs as authoritative. Do not copy copyrighted text, images, figures, or distinctive expressive structure from commercial guides.

## 1. Product objective

Build a comprehensive, original, offline-first, illustrated **Survival Field Encyclopedia**. This is a field-operational manual, NOT a condensed marketing-style prepper overview. Coverage prioritizes Minnesota / Upper Midwest (deciduous forests, wetlands, cold winters, severe weather) with regional extensions to other environments. Provide separately downloadable zone PDFs and a fully indexed combined reference.

Success requires a short, highly standardized entry: **WHAT → WHERE → WHEN → IDENTIFY → MATERIALS → STEPS → CHECK → FAILURE / DANGER → REGIONAL / LEGAL LIMITATIONS → SOURCES**. Be concise, not shallow.

Target clear, high-information layouts for phone and print. Approximate overall length is *to be derived from verified content*: do not claim a 500- to 900-page guide exists until it does.

## 2. Initial zone map

| ID | Zone | Coverage examples |
|----|------|------------------|
| Z01 | Survival fundamentals | priorities, decision making, lost-person rules, safety and equipment |
| Z02 | Shelter and housing | lean-tos, debris shelters, tents/tarps, cold-weather insulation, site selection, structures |
| Z03 | Fire and ignition | tinder, fuel preparation, controlled ignition, flint-and-steel, ferro rod, weather-specific fire |
| Z04 | Water | source selection, rain capture, leaf/branch runoff, snow/ice, settling, filtration and disinfection, storage |
| Z05 | Wild foods and poisonous look-alikes | plants, mushrooms, berries, seeds, nuts, roots, tree foods; seasonality and hazard plates |
| Z06 | Hunting and fishing | tracking, ecology, lawful harvest, gear, field hygiene, food safety |
| Z07 | Traps and snares | identification, mechanical principles, legal/ethical constraints, safe operation where lawful |
| Z08 | Rocks, minerals and materials | flint/chert, quartz, other materials, rock identification, clay, fibers, wood, tool materials |
| Z09 | Tools and construction | knots, cordage, repair, improvised containers, woodworking, campsite tools |
| Z10 | Wilderness medicine | layperson first aid, hygiene, exposure, heat/cold illness, evacuation criteria |
| Z11 | Navigation, weather and rescue | map/compass, positioning, signaling, rescue practices and weather recognition |
| Z12 | Extreme environments | Upper Midwest winter, desert, mountain, wetland, coast, maritime |
| Z13 | Home survival and utilities | power loss, heating safety, CO, water, sanitation, security and communication |
| Z14 | Food production and preservation | cultivation, processing, drying, storage, safe preservation and sustainability |
| Z15 | Disaster scenarios | severe storms, tornadoes, floods, wildfire, prolonged outages and decision trees |
| Z16 | Field reference atlas | species comparison plates, seasonal indexes, materials reference, checklists |

Z05 **must be a standalone major zone**, not a brief appendix. Z08 and Z04 must include Midwest-relevant field examples and photographic reference specimens. Begin by building the structures for all zones, not hallucinating missing content.

## 3. Required entry templates / schemas

Create structured content (YAML/JSON front matter + Markdown or equivalent) with fields at minimum:

```
id: Z08-CHERT-001
zone: Z08
title: Chert (incl. flint varieties)
status: draft | researched | verified | approved | published
region: [upper_midwest, ...]
season: [year_round]
what_it_is: ...
find_where: ...
find_when: ...
diagnostic_features: [...]
lookalikes_or_confusions: [...]
materials: [...]
procedure: [{step: 1, action: ..., verify: ...}]
conditions_and_limits: [...]
dangers: [...]
source_ids: [...]
photo_ids: [...]
illustration_ids: [...]
technical_reviewer: null
editorial_reviewer: null
approved_by_chatgpt: false
revision: 1
```

For **species profiles** add scientific name, taxonomic authority where available, multiple photos (whole organism, key features, habitat, look-alike), geographic range, phenology, identification uncertainty, regulated/protected status where applicable, processing restrictions, and **positive-identification warning**. No field-use identification based on a single photo or on AI alone.

For **engineering procedures** add materials/tools, dimension/unit table, environmental constraints, step sequence, inspection/acceptance criteria, failure modes, and hazard boundaries.

For **medical guidance** add audience/scope, evidence date, emergency/evacuation threshold, contraindications and local emergency service guidance. Do not invent medical procedures.

## 4. Photographic and illustration accuracy gate

Each real reference photo must be logged in an `assets/manifest.csv` with:
- asset ID and local path
- subject (common/scientific name or rock/material name)
- provenance URL / organization / credited photographer
- license or explicit permission and allowed derivatives
- image acquisition date
- location / region / date observed if available
- whether image is a verified diagnostic photograph, supporting habitat photograph, or decorative only
- reviewer and review status
- caption and alt text

Make the **source photo** clearly distinguishable from original schematic illustrations. Generate diagram art from approved briefs only. Do NOT use AI-generated mushrooms, edible/poisonous look-alikes, berries, flowers, seeds, or mineral specimens as identification evidence. Generated images must carry `ILLUSTRATION — NOT FOR SPECIES IDENTIFICATION` where relevant.

Potential repositories to source authorized reference images: USDA/USFS, USGS, Minnesota DNR, US NPS, university herbaria, public-domain government photography, and explicitly licensed Wikimedia Commons assets. Permission/restrictions vary per asset: verify individually, do not assume all images are public domain.

## 5. Source register and claim traceability

Create `research/sources.csv`, `research/claims.csv`, and `research/coverage-matrix.csv`.

Mandatory fields in sources: source_id, document_title, issuing_body/author, edition/date, URL or local origin, source_type, access/usage rights, revision date, reliability notes, sections/pages relevant.

Every actionable field procedure must have traceable claim IDs with direct source locators; label uncertain claims as `UNVERIFIED` and exclude them from publishable outputs.

Use only original writing. Commercial comparator titles are for coverage and structural benchmarking, not for cloning chapters or reproducing copyrighted figures:
- John "Lofty" Wiseman, *SAS Survival Handbook*
- Arthur T. Bradley, *Handbook to Practical Disaster Preparedness for the Family*
- Abigail R. Gehring, *Back to Basics*
- Joel Lambert, *A Navy SEAL's Bug-In Guide*
- Hesperian, *Where There Is No Doctor* (use official PDF sources when permitted)

**Never** represent a PDF as authorized solely because it appears on a third-party download site. Research outputs from previous chats are not automatically local. If missing, create explicit `NEEDS_CHAT_RESEARCH` cards, and request exported source material, rather than inventing them.

## 6. Physical fact checks that must be gate tests

Flag for domain expert/ChatGPT validation:
- Flint + ordinary rock does not by itself equal reliable sparks; traditional steel-striking produces hot particles of steel. Demonstrations must specify components, tinder, and fire-control safety.
- Water that looks clean or came from rainfall/foliage is not necessarily potable. Distinguish turbidity removal from pathogen inactivation and chemical contaminants. Follow current CDC/EPA guidance.
- Fire, indoor combustion, generator use and makeshift heating can cause fatal carbon monoxide poisoning or structural fires.
- Mushrooms, poisonous look-alikes, and plants: photos alone cannot establish edibility. Do not publish an eat/not-eat guarantee.
- Hunting/trapping must be region-specific, comply with licensing/season/equipment and protected-species requirements; no blanket assertion about what is legal.
- Canning/preservation: temperature, pressure, processing time, altitude and food acidity matter; use tested USDA/NCHFP procedures rather than improvisation.

## 7. UX, editorial and graphic design

- Compact, action-led language with short sentences. Define specialist terms on first use.
- Each profile starts with a real photograph when identification is involved and a summary field box.
- Use consistent icons for `FIND`, `IDENTIFY`, `USE`, `CHECK`, `AVOID`, `CAUTION`, `SOURCE` (icons are assistive, never the only signal).
- Number procedural steps and illustrate only consequential details.
- Apply US customary AND metric units when useful, with round-trip consistency checks.
- Use strong captions, labels, contrast, scalable diagrams, and source credits.
- Bookmarks/TOC, glossary, indexes by species, technique, hazard, environment, and season.
- A portable phone-friendly PDF and print-ready Letter / A4 outputs; include color and grayscale test rendering.
- Required pages: cover, how to use, field emergency index, full contents, source legend, safety note, revision and errata history.

## 8. Proposed file/folder layout

```
survival-field-encyclopedia/
  README.md
  GOVERNANCE.md
  CHANGELOG.md
  RUN-LOG.md
  content/
    Z01_fundamentals/ ... Z16_field_atlas/
  templates/
    entry.md
    species_profile.md
    technical_procedure.md
  research/
    sources.csv
    claims.csv
    coverage-matrix.csv
    unresolved-research.md
  assets/
    manifest.csv
    original_photos/
    diagrams/
    rejected_unverified/
  layouts/
  scripts/
  tests/
  proofs/
  dist/
    zones/
    complete/
  reviews/
    approvals.csv
    image-audit.csv
    safety-audit.csv
```

If a current repo already exists, inspect it and avoid reinitializing or overwriting existing work. Create a feature branch and commit coherent changes. Do not push to remote or deploy until the user authorizes it.

## 9. Execution phases and review gates

**Phase A: Audit and scaffold**
1. Inspect current working directory, git status, and any existing project.
2. Create governance docs, directory structure, schema, source register, asset manifest, sample placeholder entries, and automated validation rules.
3. Build one proof-of-layout only from a clearly labeled *illustrative sample*, not invented operational advice.
4. Provide a run record and exact paths to preview artifacts.

**Gate A:** ChatGPT/user reviews architecture, source schema, layouts and safety warnings.

**Phase B: Research ingestion, strictly controlled**
1. Ingest approved research packs and source notes supplied by ChatGPT.
2. Trace each claim to sources, report contradictions and gaps. Do not invent missing content.
3. Acquire/track only appropriately licensed original reference photos; quarantine uncertain rights or identifications.

**Gate B:** ChatGPT validates claims, species lists and image assignments.

**Phase C: Typesetting and visual production**
1. Generate diagrams from approved step specifications and clearly mark concept illustrations.
2. Build zone PDFs and combined PDF; generate bookmarks and indexes.
3. Render every page and run automated overflow/orphan/missing-figure checks.
4. Validate no unapproved text or unverifiable image IDs enter published builds.

**Gate C:** Technical/editorial review in ChatGPT; no publication of failing sections.

**Phase D: Release**
- Package PDFs, source files, figure attribution ledger, claim-source audit, and revision notes.
- Produce a coverage report with explicitly incomplete subjects; do not call incomplete editions 'complete'.
- Require explicit user authorization before upload, deployment, commit to main, or release.

## 10. Validation rules to implement

- Every published entry has `approved_by_chatgpt: true` plus verified status and nonempty source IDs.
- Every cited source ID exists in source register; every real photo ID exists in manifest and has license status approved.
- All species identification plates include at least two complementary diagnostic views, **plus explicit uncertainty and look-alike review**. For hard-to-ID groups, demand additional expert criteria; number of photos never substitutes for expertise.
- All hazardous entries include danger boundaries.
- Every physical procedure has a step, a verification check, and an error/abort condition.
- Detect missing captions, alt text, broken links, missing bookmarks, page overflow, conflicting measurement units, and uncited specifications.
- Run source/rights checker and manually audit at least representative pages in every zone.

## 11. First Astra CLI action — immediately authorized

**Do not write 16 zones of survival advice.** Start with a quick audit of the local worktree, scaffold the production repository and build the versioned validation/typesetting pipeline. Output:

1. `PROJECT_AUDIT.md`: directories/repos found, state, and no-overwrite plan.
2. `BUILD_PLAN.md`: toolchain decisions, estimated technical dependencies, build/test commands.
3. Working content schemas + source/photo manifests with placeholder headers.
4. One single-page `SPECIMEN_LAYOUT_PROOF.pdf` using unmistakably dummy content and labeled imagery.
5. `RUN-001.md`: commands, files changed, tests, failures and blocked research items.
6. Short copy/paste handback for ChatGPT to inspect the actual build architecture.

**Stop at Gate A.** Never claim research or approval has already occurred. Do not move into content fabrication. Protect any existing work and provide a deterministic continuation point.

## 12. Handoff / response protocol

At the end of each CLI run, return:

```
RUN ID:
GIT BRANCH / COMMIT:
CHANGED FILES:
WHAT WAS VERIFIED:
WHAT IS STILL UNVERIFIED:
TESTS AND OUTPUT:
PROOFS (ABSOLUTE PATHS):
BLOCKING DECISIONS FOR CHATGPT:
NEXT GATE:
```

The original ChatGPT research is the editorial source of truth. The CLI build is an implementation artifact, not an independent scientific authority. Preserve the exact approved version of each chapter, and show a diff for every substantive change.
