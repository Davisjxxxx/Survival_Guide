# FABLE-REVIEW-001 — Independent preproduction adversarial review

| | |
|---|---|
| Project | Survival Field Encyclopedia |
| Review ID | FABLE-REVIEW-001 |
| Date | 2026-11-17 |
| Reviewer | Claude Code (Fable 5.2), acting as independent systems architect, adversarial reviewer and safety-validation specialist. Not the author of any reviewed code. |
| Workspace reviewed | `/home/jd/Survival_Guide` (read only) |
| **Primary commit examined** | **`dc678192da569638946ae9c8e4671cff2f7e8b0f`** — branch `gate-a/scaffold`, tag `gate-a-submission` |
| Secondary commit examined | `a08104a540f8017ac8f60c3405e1585e542806e6` — branch `gate-a/remediation-1`, tag `gate-a-remediation-1` (RUN-002) |
| Output | `/home/jd/Survival_Guide_Fable_Review/` |
| Gate A | **Not approved by this review.** This review has no authority to approve a gate and does not. |

## 1. Conclusion

The scaffold is careful engineering. It parses strictly, refuses to release on any error, binds each approval to the exact text of its entry, builds byte-identical PDFs, and scales to the planned volume.

It is not yet safe to put real content behind it. The gates stop malformed input. They do not stop well-formed input that is wrongly classified, weakly reviewed or changed where the approval hash does not look.

Three results carry the review:

1. **An author can skip the safety gate by omission.** Hazard tags and entry type are typed by the author, and the safety gate runs only on what is declared. A wild-foods entry typed `general` with no tags reaches `published` with one approval row and no safety review (FR-001).
2. **A recorded safety failure often blocks nothing.** At the remediation commit, a failure is ignored if its topic list is empty, if it names a hazard the entry is not tagged with, if the entry has no tags, if its revision number differs, if its date is earlier than the passes, or if the entry id is mistyped. Any later pair of passes clears it (FR-002, FR-003, FR-004).
3. **A species plate can pass with one photograph of the wrong organism.** One image file listed twice satisfies the two-view rule, and nothing compares a photo's subject with the entry's species (FR-012).

GA-001 and GA-002 are fixed at `a08104a` in the form RUN-002 describes. Their causes are not: of 53 concrete counterexamples in the threat model, the remediation closes 2.

The register holds 29 findings: 3 Critical, 12 High, 11 Medium, 3 Low. All are present at both commits.

## 2. Scope and method

### 2.1 What was read

Committed source only, at the two commits above. Nothing uncommitted was relied on.

| Area | Files |
|---|---|
| Handoff | `handoff/SURVIVAL_FIELD_ENCYCLOPEDIA_ASTRA_CLI_HANDOFF.md`, `Survival_Field_Encyclopedia_Master_Sprint_Plan_v1.md`, `Survival_Field_Encyclopedia_Sprint_Tracker_v1.xlsx` (all six sheets), `README_INSTALL.md` |
| Run records | `BUILD_PLAN.md`, `PROJECT_AUDIT.md`, `RUN-001.md`, `RUN-002.md`, `GOVERNANCE.md`, `BASELINE_AUDIT_20261116.md`, `README.md`, `CHANGELOG.md`, `RUN-LOG.md`, `research/unresolved-research.md` |
| Schemas and policy | All nine JSON Schemas, `schemas/hazard_topics.yaml`, `content/zones.yaml`, the four templates |
| Gates and pipeline | Every module in `scripts/sfe/` (`validate`, `registry`, `entries`, `assets`, `units`, `texgen`, `pdfbuild`, `qa`, `cli`, `common`), `layouts/sfe.sty`, `layouts/build.yaml`, `Makefile` |
| Tests, read in full | `factories.py`, `conftest.py`, `test_validation_gates`, `test_hazard_gates`, `test_species_gates`, `test_assets`, `test_registers`, `test_gate_a_snapshot`, `test_units` |
| Tests, read in part | The release and hardening tests in `test_pdf_pipeline`; the hash tests in `test_schemas` |
| Tests, run but not read | `test_cli`, `test_texgen`, `test_zones`, `test_handoff_consistency`, `test_layout_contrast`, `test_preservation`; and the three test files RUN-002 added |
| Remediation | At `a08104a`: the full diff of every changed code, schema and policy file and of `tests/factories.py`, `BUILD_PLAN.md` and `GOVERNANCE.md`; `RUN-002.md` in full |

### 2.2 What was run

1. Both commits were exported with `git archive` into a scratch directory outside the repository. `git archive` reads the object store and does not touch the working tree.
2. The project's own suites were run on the exports: **447 passed, 2 skipped** at `dc67819`; **609 passed, 2 skipped** at `a08104a`. The two skips need a Git checkout. This matches what RUN-001 and RUN-002 report for exported trees.
3. Fifty-nine adversarial probes were written and run against both exports. Each builds a throwaway fixture repository with neutral "Fixture" text, sets up one scenario, and reports whether the validator and the release build accept it.
4. Probe sources and outputs are in `evidence/`. `ARCHITECTURE_FINDINGS.md` gives the commands to rerun them.

### 2.3 Constraints honoured

| Constraint | Status |
|---|---|
| Do not modify the active repository | Honoured. Only `git archive`, `git diff`, `git log`, `git status` and similar read commands were run in it. No tracked file changed; `git status` is unchanged from the start of the review. |
| Do not interfere with RUN-002; no branches; no approval records touched | Honoured. Branches and tags are as found: `gate-a/scaffold` and `gate-a-submission` at `dc67819`, `gate-a/remediation-1` and `gate-a-remediation-1` at `a08104a`. |
| No survival instructions, no fabricated citations or specimen images | Honoured. Fixtures are neutral strings and synthetic grey images. The species standard states evidence requirements and no identification facts. |
| Do not approve Gate A; do not publish; no unrelated projects; do not restart the implementation | Honoured. |

One thing to know about the working tree: it holds an untracked `.serena/` directory, created at 2026-11-16 20:12 when this session's tooling started, before any review command ran. It is tool cache, not review output. It was left in place. No tracked file is affected.

## 3. Status of the known findings

| Finding | At `dc67819` | At `a08104a` | What remains |
|---|---|---|---|
| **GA-001** Required independent reviewer roles not enforced | Reproduced (P01: one `user` row satisfies a hazard topic) | The reported case is blocked | Both classes can be filled by rows naming AI models (P09). One named person in both classes gives a warning and the release still builds (P09b). One class is self-review by design: ChatGPT authors, approves and validates. No reviewer registry, no author record. → FR-005 |
| **GA-002** A newer failed review did not revoke an older pass | Reproduced (P02) | The reported case is blocked | The failure is ignored in five forms (P04, P05, P06, P52, P53), outranked by typed dates (P03a, P03b), dependent on file order (P08b), and cleared by re-passing (P07). The approvals ledger has the same weakness and was not changed (P10a, P10b, P11a, P11b). → FR-002, FR-003, FR-004 |

Neither finding should be treated as resolved for the purpose of Gate A.

## 4. Assessment against the sixteen review areas

"Adequate" means the control does what the handoff requires. "Partial" means it works for the declared case and not for the undeclared one. "Inadequate" means a concrete counterexample exists.

| # | Area | Assessment | Findings |
|---|---|---|---|
| 1 | Source reliability and evidence provenance | Inadequate. A verified source may have no edition, no retrieval date and no hash; a rights-rejected mirror or a background-only source can back a published claim. | FR-009, FR-007 |
| 2 | Claims linked to exact source editions | Inadequate. A claim points to a row whose edition can be edited in place; verification is a flag in the row it describes. | FR-009 |
| 3 | Review independence and approval revocation | Inadequate. See §3. | FR-002 – FR-006, FR-022, FR-029 |
| 4 | Biological species misidentification controls | Inadequate. The plate rule counts labels, not organisms. | FR-012, FR-025 |
| 5 | Toxic look-alike photographic validation | Inadequate. Look-alikes are free-text names; a look-alike photo counts toward the target's own minimum. | FR-012, FR-025 |
| 6 | AI-generated image contamination | Partial. Imagery declared as AI is contained. Imagery not declared as AI is indistinguishable to the gate. | FR-013 |
| 7 | Image licensing and attribution | Partial. Presence of metadata is checked; "All rights reserved" passes as an approved licence. | FR-015, FR-014, FR-010 |
| 8 | Hazardous procedural guidance | Inadequate. The hazard gate depends on author-declared tags; "N/A" satisfies an abort condition. | FR-001, FR-021, FR-011 |
| 9 | Medical and food-safety review requirements | Inadequate. A medical entry can publish with no claims; medical content typed otherwise gets no safety review; authority requirements are unread text. | FR-001, FR-005, FR-007, FR-008 |
| 10 | Regional and seasonal accuracy | Inadequate. Region and season are free text. | FR-016, FR-027 |
| 11 | Outdated legal or regulatory information | Inadequate. Nothing expires; an as-of date of 1990 passes. | FR-016 |
| 12 | Version drift between chapters and diagrams | Inadequate. A diagram can be replaced after approval without making the approval stale. | FR-010, FR-022 |
| 13 | Unsafe instructions surviving later corrections | Inadequate. A refused release leaves the previous PDF in place; PDFs carry no edition identity. | FR-017, FR-002, FR-004 |
| 14 | Cross-reference and indexing integrity | Not built (documented). Already wrong for the one link type that exists; the fields indexes need are absent. | FR-018, FR-027 |
| 15 | PDF reproducibility and accessibility | Reproducibility adequate on one toolchain (verified, P73); release manifests are too thin to reproduce from. Accessibility inadequate (documented D1); alt text never emitted. | FR-017, FR-023 |
| 16 | Failure behaviour when evidence is incomplete | Mixed. Structural gaps fail closed, reliably. Semantic gaps fail open: missing tag, missing claim, missing rendered field, unresolved failure. | FR-001, FR-002, FR-008, FR-011 |

## 5. Findings at a glance

Full records, each with evidence, consequence, correction, acceptance criteria, remediation model and target sprint, are in `ARCHITECTURE_FINDINGS.md`.

| ID | Sev. | Finding | Target |
|---|---|---|---|
| FR-001 | **Critical** | Hazard class and entry type are chosen by the author; a mistyped or untagged entry skips every safety control | GA-R2 |
| FR-002 | **Critical** | A recorded safety failure blocks only when it names a topic the entry is already tagged with | GA-R2 |
| FR-012 | **Critical** | The species plate rule passes without two real views of the stated organism | Pre-S06 |
| FR-003 | High | Precedence is decided by a reviewer-typed date and by file position | GA-R2 |
| FR-004 | High | Conflicting decisions are settled by recency, not by resolution | GA-R2 |
| FR-005 | High | The two "independent" reviews can be the author and an unqualified or non-human reviewer | GA-R2 |
| FR-008 | High | Species and medical entries can be published with no claims at all | Pre-S02 |
| FR-009 | High | Claims are not tied to an exact source edition, and verification is an editable flag | Pre-S02 |
| FR-010 | High | Approvals and safety reviews do not cover the images, captions and labels the page prints | Pre-S02 |
| FR-011 | High | Approved safety text can be absent from the released PDF | GA-R2 |
| FR-013 | High | Whether an image is a real photograph is self-declared | Pre-S06 |
| FR-016 | High | Nothing expires: legal, medical and regulatory content has no freshness control | Pre-S02 / Pre-S15 |
| FR-017 | High | A correction does not withdraw what was already built | Pre-S05 / Pre-S15 |
| FR-025 | High | No data model for taxon identity, look-alikes, edibility or minerals | Pre-S06 |
| FR-029 | High | The approval hash is computed by the operator after review; nothing records what the reviewer read | Pre-S02 |
| FR-006 | Medium | "verified" and "published" rest on self-typed fields; no release authorization record | Pre-S02 / Pre-S15 |
| FR-007 | Medium | Hazard policy fields are declarative; reviews are not bound to the checklist they attest to | Pre-S02 |
| FR-014 | Medium | Photo metadata, including GPS position, is copied into release PDFs | Pre-S06 |
| FR-015 | Medium | Licence checks accept restrictive or meaningless terms | Pre-S06 |
| FR-018 | Medium | The log gate misses a warning class; shared source links point to another entry | Pre-S03 |
| FR-019 | Medium | The unit check accepts large errors and cannot express common quantities | Pre-S02 |
| FR-020 | Medium | Layout limits push authors toward weaker entry types and shorter safety text | Pre-S03 / Pre-S06 |
| FR-021 | Medium | Required safety fields accept "N/A" | GA-R2 |
| FR-022 | Medium | Ledger history is not checked; hash and schema are unversioned | Pre-S02 |
| FR-026 | Medium | No originals/derivatives split and no storage plan for the photo library | Pre-S06 |
| FR-027 | Medium | No controlled vocabularies or reference fields for indexes and cross-references | Pre-S02 / Pre-S13 |
| FR-023 | Low | Alt text is required but never reaches the reader | Pre-S13 |
| FR-024 | Low | Tests assert configuration text; none assert gate invariants | GA-R2 |
| FR-028 | Low | Decorative fields give an impression of control | Pre-S02 |

GA-R2 is a second Gate A remediation, before the re-review closes. "Pre-S02" items are marked early because they change what the approval hash covers; after approvals exist, each such change invalidates them (FR-022).

## 6. What held

Probed and found working. The corrections should not disturb these.

| Control | Evidence |
|---|---|
| Strict parsing; any structural error refuses the whole release | Existing suite; release probes |
| Entry text bound to its approval and safety reviews | Existing suite; baseline state of P16 and P21 |
| Layout overflow fails closed instead of clipping | P70 |
| Long procedures flow across pages with nothing lost | P71 |
| Deterministic release builds | P73 |
| Scale: 1,000 entries validate in 2.8 s; a 120-page zone builds in 34 s | P80, P81 |
| Declared AI imagery cannot be a photo or evidence | Existing suite |
| The run records state their limitations plainly | `BUILD_PLAN.md` §8; RUN-002 §8 |

The architecture does not need replacing. No database, signing system or new typesetting engine is required for any correction in this review.

## 7. Limits of this review

1. **No content exists, so none was reviewed.** Every finding concerns what the gates would accept. Nothing here says anything about the truth of any survival claim.
2. **Probes use fixtures.** They show what the validator and release build accept. They do not show that a person or model would in fact produce that input; §2 of the threat model argues why they plausibly would.
3. **One toolchain.** Python 3.13.0, pdfTeX 1.40.25 (TeX Live 2023), poppler 26.01.0. Behaviour on other versions was not tested.
4. **The remediation commit was probed, not re-audited line by line.** Its diff was read in full and its suite was run. New defects introduced by RUN-002 outside the probed behaviour could exist.
5. **Not attacked afresh:** TeX escaping, shell-escape hardening and the PDF QA thresholds. The existing tests for these were read and run, and no new attack was attempted beyond them.
6. **The species standard is a framework, not a specialist determination.** Its character classes, perspective sets and minimum counts are marked for confirmation by a botanist, a mycologist and a geologist.
7. **Severity is this reviewer's judgement.** The scale is defined in `ARCHITECTURE_FINDINGS.md`. The owner and ChatGPT may weigh consequences differently.

## 8. Deliverables

| File | Contents |
|---|---|
| `FABLE-REVIEW-001.md` | This report |
| `ARCHITECTURE_FINDINGS.md` | The 29 findings in full, the reproduction recipe, and the controls that held |
| `SAFETY_GATE_THREAT_MODEL.md` | Who can cause a bad publication, what each decision is bound to, 53 counterexamples, 13 invariants |
| `SPECIES_IDENTIFICATION_STANDARD.md` | The verification framework for plants, berries, seeds, mushrooms and minerals, with 24 machine gates |
| `REQUIRED_REGRESSION_TESTS.md` | 102 test specifications, 12 property tests, 20 sabotage checks |
| `SPRINT_RECOMMENDATIONS.md` | What must change before S02, S06, S08, S13 and S15, and input on decisions D1–D12 |
| `EXECUTIVE_HANDOFF.md` | Two-page summary and handback block |
| `evidence/` | `probes.py`, `probes2.py`, `probes3.py` and their outputs for both commits |
