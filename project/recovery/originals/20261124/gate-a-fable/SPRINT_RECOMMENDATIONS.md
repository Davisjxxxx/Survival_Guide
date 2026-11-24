# Sprint recommendations

| | |
|---|---|
| Review | FABLE-REVIEW-001, step 5 |
| Commits | `dc678192da569638946ae9c8e4671cff2f7e8b0f` (baseline), `a08104a540f8017ac8f60c3405e1585e542806e6` (RUN-002 remediation) |
| Question | Can the existing system reliably support a large, illustrated, offline reference, and what must change before S02, S06, S08, S13 and S15? |

Finding ids refer to `ARCHITECTURE_FINDINGS.md`. Every item below names the requirement it serves. Nothing here adds product scope; each item closes a gap between what the handoff requires and what the gates enforce.

## 1. Can the system support the planned reference?

The mechanism can. The assurance cannot yet.

| Need | State | Evidence |
|---|---|---|
| Volume of entries and registers | Adequate | 1,000 entries, 3,000 claims and 1,000 approvals validate in 2.8 s (P80) |
| Volume of pages | Adequate | A 120-entry, 120-page zone PDF builds in 34 s, in 2 LaTeX runs (P81). The plan's largest zone is 135 pages. |
| Deterministic output | Adequate on one toolchain | Two release builds are byte-identical (P73). The toolchain is recorded in proof manifests but not pinned, and not recorded in release manifests (FR-017). |
| Long procedures | Adequate | 40 steps flow over 2 pages with every step present (P71) |
| Long safety panels | Not adequate | 60 danger lines refuse to build (P70, FR-020). Refusal is the right failure; the limit is the problem. |
| Species and medical pages | Not built | Both entry types refuse to render (documented, `BUILD_PLAN.md` limitation 6) |
| Real photographs | Untested, with known defects | Location metadata passes into PDFs (FR-014); no derivative pipeline (FR-026); licence terms unchecked (FR-015) |
| Navigation: contents, indexes, cross-references, combined PDF | Not built | Documented, limitation 7. The fields the indexes need do not exist yet (FR-027). |
| Corrections to an offline book | Not supported | No edition identity, no errata record, stale output survives a refusal (FR-017) |
| Trust that an approved page is a reviewed page | Not adequate | 50 open counterexamples (`SAFETY_GATE_THREAT_MODEL.md` §4) |

No re-platforming is needed. CSV registers in Git and the pdfLaTeX pipeline are sufficient for the planned volume. The work is in what the gates bind to and what they refuse.

## 2. Sequencing principle

**Anything that changes what an approval covers must land before the first approval is recorded.**

Today an approval covers the entry's text. Corrections FR-008, FR-009, FR-010, FR-011 and FR-029 widen that to claims, sources, images and the reviewer's packet. Each widening changes the hash. Before any approval exists, that costs nothing. Afterwards it invalidates every approval on file, or tempts someone to narrow the hash to avoid that (FR-022).

So the order below follows hash impact, not the sprint in which the content arrives. Species schema is reserved before S02 although the first plate is due in S06.

**Research need not wait.** ChatGPT's S02 research does not depend on the repository. What must wait is ingestion into the registers and the recording of approvals.

## 3. Before the Gate A re-review closes (GA-R2)

These are the gate-logic corrections. They are local to `scripts/sfe/validate.py`, the ledger schemas and the tests.

| # | Change | Requirement it serves | Finding | Size |
|---|---|---|---|---|
| 1 | Any unresolved non-pass decision blocks the entry, whatever its topics, revision or date. Orphan ledger rows are errors. | Handoff §9 Gate C: "no publication of failing sections" | FR-002 | S |
| 2 | Order ledgers by validated sequence, not by typed date. Validate dates as dates. | GA-002 as reported | FR-003 | S |
| 3 | A failure is cleared only by an explicit resolution row. Approvals are evaluated per role. | Handoff §0: ChatGPT holds final safety sign-off; plan: specialists own high-risk verification | FR-004 | M |
| 4 | Derive hazard class and allowed entry type from zone, cited claims and the coverage plan. | Handoff §6: the physical fact checks "must be gate tests" | FR-001 | M |
| 5 | Reviewer registry; hash-bound `authored_by`; no self-review; same reviewer in two classes is an error. | GA-001 as reported; tracker: "No AI substitutes for qualification" | FR-005 | M |
| 6 | Renderer totality: an approved field that is not rendered fails the build. Type-specific fields only on their type. | `texgen.py` design rule. Handoff §9 Phase C requires that no unapproved text enters a published build; this is the converse, that no approved text leaves one. | FR-011 | S |
| 7 | Reject null-like values in required safety fields. | Handoff §10: step, verification check and abort condition | FR-021 | S |
| 8 | Invariant and sabotage tests for items 1–7. | RUN-002's own validation practice | FR-024 | M |

Size is relative: S is a contained change with tests, M needs a schema or policy decision as well, L spans several modules and needs outside input. These are estimates, not commitments.

Item 4 needs a policy table from ChatGPT (which zones require which types and classes). Item 5 needs the owner to say who is registered. The mechanisms can be built and tested with fixtures before either arrives.

## 4. Before S02 research ingestion

S02 brings the first real sources, claims and approvals for water, combustion, exposure, food safety and triage. These are the items whose absence would be baked into every row S02 writes.

| # | Change | Requirement it serves | Finding | Size |
|---|---|---|---|---|
| 1 | Review packets. The tool emits the exact text and closure digest for review; the reviewer's reply quotes the digest; both are stored. Packs are stored unchanged with hashes. | Handoff §12: "preserve the exact approved version of each chapter, and show a diff for every substantive change" | FR-029 | M |
| 2 | Closure digest: approvals and safety reviews cover cited claims, sources, asset files and printed manifest fields. | Handoff §0: never silently rewrite approved text; never substitute a diagram | FR-010 | M |
| 3 | Sources: one row per edition, immutable once verified, with edition, retrieval date and content hash. Claim verification as a ledger row bound to claim and source digests. Source tier by claim risk. | Handoff §5; plan gate B: "high-consequence claims linked to dated source IDs" | FR-009 | L |
| 4 | Claim binding for safety-bearing fields, with minimum claims per entry type. | Handoff §5: uncertain claims excluded from publishable output | FR-008 | M |
| 5 | Ledger append-only check, sequence ids, hash version, written migration procedure. | `BUILD_PLAN.md` limitation 2 relies on Git history; nothing reads it | FR-022 | M |
| 6 | Hazard policy: reviews bound to checklist version; authority requirement enforced; no unread keys. | Handoff §6: "follow current CDC/EPA guidance", "tested USDA/NCHFP procedures" | FR-007 | M |
| 7 | Technical review as a ledger row. | Handoff §3: `technical_reviewer` field | FR-006 | S |
| 8 | Controlled codes for region and season; validity dates on claims and entries by class. | Plan risk table: "jurisdiction and 'as of' dates"; handoff §7 indexes | FR-016, FR-027 | M |
| 9 | Unit policy: relative tolerance, quantity kinds, prose lint, limit direction. | Handoff §7: round-trip consistency; S02's water and food-safety quantities | FR-019 | M |
| 10 | Reference fields between entries; glossary term ids. | Handoff §7: cross-references and indexes | FR-027 | S |
| 11 | Enforce or remove decorative fields. | Handoff §10: validation rules | FR-028 | S |
| 12 | Reserve the species schema: `taxon_id` on entries and assets, look-alike pair and edibility records, `material_profile`. | Handoff §3 species requirements | FR-025 | S |
| 13 | Replace the Gate A snapshot tests with invariants on the real registers. | The tests' own docstring: update or retire at Gate B, "never silently" | FR-024 | S |
| 14 | **End-to-end dry run with dummy content:** one synthetic pack through ingestion, packet, review rows, release and withdrawal. | The Gate A specimen exercises layout only. No test has yet moved a pack through ingestion, review and release, which is the path FR-029 concerns. | FR-029, FR-017 | M |

## 5. Before S03 to S05 (field-entry pilot, navigation, medical beta)

| # | Change | Requirement it serves | Finding | When |
|---|---|---|---|---|
| 1 | Report every unclassified LaTeX warning; make duplicate link targets an error; test that each link lands on its expected page. | Handoff §10: detect broken links | FR-018 | Pre-S03 |
| 2 | Breakable CHECK and FAILURE / DANGER panels. | Plan: "concise language must never omit a critical step" | FR-020 | Pre-S03 |
| 3 | Render body text, or require it to be empty. | Handoff §9 Phase C | FR-011 | Pre-S03 |
| 4 | Medical layout that renders every required field. | Handoff §3 medical guidance fields | FR-020 | Pre-S05 |
| 5 | A registered human medical reviewer, engaged before content is drafted to its scope. | Plan S05: "Chat + external SME" | FR-005 | Pre-S05 |
| 6 | Edition identity on every page; one directory per edition; previous output withdrawn on refusal; full manifest. | S05 ships the first offline beta. Once a file leaves the machine, FR-017 is the only way to correct it. | FR-017 | Pre-S05 |

## 6. Before S06 plant atlas development

S06's exit is "taxon list and first 30 verified plates". "Verified" has no enforceable meaning until these exist.

| # | Change | Requirement it serves | Finding |
|---|---|---|---|
| 1 | Adopt `SPECIES_IDENTIFICATION_STANDARD.md`, with its §16 decisions made and its **[SME]** items confirmed by a botanist. | Handoff §3, §4, §10; plan gate D | FR-012, FR-025 |
| 2 | Implement gates SIS-G01 to SIS-G19 and SIS-G21 to SIS-G24, each with passing and failing fixtures. | Handoff §10: "at least two complementary diagnostic views, plus explicit uncertainty and look-alike review" | FR-012 |
| 3 | Image provenance evidence and generation attestation. | Handoff §4: no AI-generated specimens as identification evidence | FR-013 |
| 4 | Originals and derivatives with lineage; metadata stripped from published files; storage decision for 350–600 photographs. | Handoff §4 manifest; plan photo targets | FR-014, FR-026 |
| 5 | Controlled licence list with obligations; attribution ledger. | Handoff §4: verify each asset individually; plan gate H | FR-015 |
| 6 | Species plate layout, at a size a specialist confirms legible on phone and print. | Handoff §7: each profile starts with a real photograph | FR-020, FR-026 |
| 7 | Look-alike matrix as pair records, reciprocal, rendered side by side. | S06 deliverable: "toxic-lookalike matrix" | FR-025 |
| 8 | A dummy plate through every SIS gate before the first real photograph, as the specimen did for the card layout. | Handoff §9 Phase A principle: prove the structure on labelled dummy content | FR-012 |
| 9 | A small set of real, licensed photographs chosen by ChatGPT, to test JPEG, colour profile and size handling. Needs the owner's authorization to acquire. | `BUILD_PLAN.md` limitation 5: real photographs are untested | FR-026 |
| 10 | Botanical specialists registered. If none can be engaged, the owner decides the scope of S06 and S07 before work starts. | Plan: "qualified independent species/edibility review" | FR-005 |

## 7. Before S08 mushroom atlas development

Everything in §6, plus the parts of the standard that exist because the consequence here is death.

| # | Change | Requirement it serves | Finding |
|---|---|---|---|
| 1 | Every fungus is Tier A. Two human specialists where the owner adopts that rule. | Plan S08: "qualified mushroom experts"; risk table: "severe injury/death" | FR-005, FR-012 |
| 2 | Gate SIS-G20: the edibility record, default E0, and all 15 prohibiting conditions with a fixture each. | Plan S08: "strict non-edibility gates"; gate E1: "no photo-only edibility claims" | FR-025 |
| 3 | Determination basis D1 or D2 for fungal evidence images, or D3 with concurrence and the printed "determined from photographs" notice. | Plan gate D: "photos alone never establish edible safety" | FR-012, FR-013 |
| 4 | Fungal perspective set in the layout, including the complete base, section and spore print with colour reference. Confirmed by a mycologist. | Handoff §10: "for hard-to-ID groups, demand additional expert criteria" | FR-012 |
| 5 | Lethal and severe look-alike pairs complete for both taxa before the target profile can publish. | Tracker Z05: "lethal confusions" | FR-025 |
| 6 | The errata process in use, not only built. | The Midwest early-access target (2027-04-04) follows S09, and the plan says "do not release an unreviewed edibility atlas" | FR-017 |
| 7 | Owner decision recorded on the fallback: with no qualified mycologist, fungal profiles publish at E0 identification-only, or not at all. | Tracker gate GG: "experts available and paid if required" | FR-005 |

## 8. Before S09 (materials, hunting, fishing, trapping)

| # | Change | Requirement it serves | Finding |
|---|---|---|---|
| 1 | `material_profile` entry type with its own character classes and perspective set; zone flags enforced. | Handoff §2: Z08 "photographic reference specimens" | FR-025 |
| 2 | Legal claims carry jurisdiction code, as-of date and validity; the release date gate refuses expired ones. | Handoff §6: "no blanket assertion about what is legal"; tracker risk R06 | FR-016 |

## 9. Before S13 integration

| # | Change | Requirement it serves | Finding |
|---|---|---|---|
| 1 | Indexes generated only from controlled fields; no hand-built index. | Handoff §7: indexes by species, technique, hazard, environment, season | FR-027 |
| 2 | Cross-reference gate: every reference resolves to a published entry in the same edition; link test on the combined PDF. | Handoff §10: broken links, missing bookmarks | FR-018, FR-027 |
| 3 | Coverage report that lists omitted and incomplete subjects with the reason for each. | Handoff §9 Phase D: "do not call incomplete editions 'complete'" | FR-017 |
| 4 | Execute decision D1 (tagged output) and emit alt text. | Plan gate H: accessibility | FR-023 |
| 5 | Render totality across the whole edition; size budgets per output profile with the real photo set. | Handoff §7: phone and print outputs | FR-011, FR-026 |
| 6 | Integration contract for Astra: it consumes edition directories with manifests and authorization, never loose files from `dist/`. | Handoff §0: publishing only after the approval gate | FR-017 |

## 10. Before S15 final release

| # | Change | Requirement it serves | Finding |
|---|---|---|---|
| 1 | Owner's release authorization as a ledger row bound to the manifest digest. | Handoff §9 Phase D: "require explicit user authorization" | FR-006 |
| 2 | Full-closure manifest; rebuild from a clean checkout in a pinned toolchain gives identical bytes. | Plan gate H2: "reproducible release package" | FR-017 |
| 3 | Freshness gate at the configured release date, across legal, medical, source and review validity. | Plan: "scheduled review before release" | FR-016 |
| 4 | Attribution ledger and licence compliance report generated from the manifest. | Handoff §9 Phase D: "figure attribution ledger" | FR-015 |
| 5 | Errata ledger and superseded-edition list published with the release. | Handoff §7: "revision and errata history" | FR-017 |
| 6 | Independent release audit: a model that did not build the release re-derives the manifest and traces a sample of entries from source edition to claim to entry to printed page. | Plan S14: "independent technical/ID/medical/legal reviews" | FR-024 |

## 11. Input on the open decisions

| Decision | Recommendation | Why |
|---|---|---|
| D1 Accessibility and engine | Agree: spike before S13. Add alt-text emission to its scope. | FR-023 |
| D3 Unit policy | Do not approve as stated. Adopt the FR-019 corrections first. | `1 mi / 2 km` and `1 gal / 4 L` pass the rule presented as strict (P23) |
| D9 Hazard topics | Approve the mechanism change before extending the list. Remove the test that pins exactly six topics. | Tags are author-declared, so a longer list changes little (FR-001) |
| D10 Same reviewer in both classes | Error, together with the reviewer registry. | The warning does not stop a release (P09b) |
| D11 Role-gate image audits | Yes, and also read the check flags and bind audits to the manifest row. | Role gating alone leaves P12 and P17 open (FR-010) |
| D12 Strict precedence | Keep it, and add explicit resolution. | Strict precedence is still cleared by re-passing (P07, FR-004) |
| Gate A | Not this review's decision. The evidence does not support closing Gate A on `dc67819` or on `a08104a`. §3 is the minimum before a re-review. | 3 Critical and 12 High findings open at both commits |

New decisions the owner is asked for:

1. Who adjudicates a disputed failure (FR-004).
2. Who may be registered as a specialist, per domain, and how that is evidenced (FR-005).
3. The distribution model, free or commercial, which decides which image licences are usable (FR-015).
4. The ten decisions in `SPECIES_IDENTIFICATION_STANDARD.md` §16.
5. Whether ingestion and approvals pause until §4 lands, if §4 is not complete by the planned S02 start on 2026-12-14.

## 12. What should not change

| Keep | Reason |
|---|---|
| CSV registers in Git | Adequate at 1,000 entries (P80); reviewable in diffs; no new infrastructure |
| The pdfLaTeX pipeline | Deterministic and fast enough (P73, P81) |
| Release refusing on any error, anywhere | The strongest control in the system |
| Hash binding of entry text | Works as designed; widen it, do not replace it |
| Test-first remediation with sabotage checks | RUN-002's method is sound; this review's tests assume it |
| Stating limitations plainly in the build plan | Half of this review's leads came from those notes |

Not needed for any correction here: a database, cryptographic signing, network features, or a different typesetting engine.

## 13. Schedule note

The plan ends S01 on 2026-12-13 and starts S02 on 2026-12-14. Sections 3 and 4 together are larger than RUN-002, whose code commits changed about 1,000 lines for two findings and one toolchain fix. Two of the section 4 items (sources and claims, review packets) also need ChatGPT to settle formats it will emit.

If both sections cannot land by the S02 start, the lower-risk choice is to let research proceed and hold ingestion and approval recording. The higher-risk choice is to record approvals under the current hash and re-approve everything later. That is the owner's call.
