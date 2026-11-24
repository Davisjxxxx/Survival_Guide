# Architecture findings — FABLE-REVIEW-001

| | |
|---|---|
| Review | FABLE-REVIEW-001, independent preproduction adversarial review |
| Primary commit examined | `dc678192da569638946ae9c8e4671cff2f7e8b0f` (branch `gate-a/scaffold`, tag `gate-a-submission`) |
| Secondary commit examined | `a08104a540f8017ac8f60c3405e1585e542806e6` (tag `gate-a-remediation-1`), to test whether findings survive the RUN-002 remediation |
| Method | Both commits exported with `git archive` to a scratch directory. Every result below comes from running probes against those exports. The live repository was only read. |
| Evidence | `evidence/probes.py`, `probes2.py`, `probes3.py`; outputs in `evidence/results_<commit>_batch<n>.txt` |

This register holds 29 findings: 3 Critical, 12 High, 11 Medium, 3 Low. All 29 are present at **both** commits unless a finding says otherwise.
None repeats a documented finding without adding a new reproduction or consequence; where a finding touches a documented item (GA-001, GA-002, OBS-1, OBS-2, D1, D3, D9–D12, BUILD_PLAN limitations 1–10) it says what is new.

## How to read a finding

**Severity**

| Level | Meaning |
|---|---|
| Critical | Unsafe or misidentified content can receive publication approval through an ordinary, honest sequence of actions, with no gate reporting an error, in a domain where the handoff names death or serious injury as the consequence. |
| High | A stated control can be bypassed or silently stops working. It needs a specific but plausible sequence, or it damages revocation or traceability for high-risk content. |
| Medium | Weakens assurance, traceability or legal distribution. No direct path to unsafe publication on its own. |
| Low | Hygiene. |

**Probe verdicts.** `ELIGIBLE` means the validator returned zero errors for a scenario that ought to be blocked: the counterexample works. `BLOCKED` means a gate caught it.

**Remediation model**

| Code | Who |
|---|---|
| ENG | CLI engineering model: implementation and tests (the project's division of responsibility) |
| GPT | ChatGPT GPT-6 High / Extra High: policy, standard wording, source and content rules |
| OWNER | A decision only the owner can make |
| SME | Qualified human specialist input |
| REVIEW | Independent adversarial re-review by a model that did not write the fix |

**Target sprint**

| Code | Meaning |
|---|---|
| GA-R2 | Gate A remediation 2: before the Gate A re-review closes |
| Pre-S02 | Before the first research pack is ingested or the first approval is recorded |
| Pre-S03 … Pre-S15 | Before that sprint starts |

Several findings are marked Pre-S02 although the affected content arrives later. The reason is in FR-022: these corrections change what the approval hash covers, and after approvals exist every such change invalidates them.

## Reproducing the evidence

```bash
mkdir -p /tmp/fr001/base /tmp/fr001/rem /tmp/fr001/tmp
cd /home/jd/Survival_Guide          # read-only: git archive does not touch the working tree
git archive dc678192da569638946ae9c8e4671cff2f7e8b0f | tar -x -C /tmp/fr001/base
git archive a08104a540f8017ac8f60c3405e1585e542806e6 | tar -x -C /tmp/fr001/rem
cd /home/jd/Survival_Guide_Fable_Review/evidence
export TMPDIR=/tmp/fr001/tmp
python3 -B probes.py  /tmp/fr001/base /tmp/fr001/tmp    # then again with /tmp/fr001/rem
python3 -B probes2.py /tmp/fr001/rem  /tmp/fr001/tmp
python3 -B probes3.py /tmp/fr001/rem  /tmp/fr001/tmp
```

Needs Python 3.13 with the project's `requirements.txt`, pdfLaTeX and poppler. Every fixture string is neutral ("Fixture …"); no survival content is created.

## Summary

| ID | Sev. | Finding | Target |
|---|---|---|---|
| FR-001 | Critical | Hazard class and entry type are chosen by the author; a mistyped or untagged entry skips every safety control | GA-R2 |
| FR-002 | Critical | A recorded safety failure blocks only when it names a topic the entry is already tagged with | GA-R2 |
| FR-003 | High | Precedence is decided by a reviewer-typed date and by file position | GA-R2 |
| FR-004 | High | Conflicting decisions are settled by recency, not by resolution | GA-R2 |
| FR-005 | High | The two "independent" reviews can be the author and an unqualified or non-human reviewer | GA-R2 |
| FR-006 | Medium | "verified" and "published" rest on self-typed fields; no release authorization record | Pre-S02 / Pre-S15 |
| FR-007 | Medium | Hazard policy fields are declarative; reviews are not bound to the checklist they attest to | Pre-S02 |
| FR-008 | High | Species and medical entries can be published with no claims at all | Pre-S02 |
| FR-009 | High | Claims are not tied to an exact source edition, and verification is an editable flag | Pre-S02 |
| FR-010 | High | Approvals and safety reviews do not cover the images, captions and labels the page prints | Pre-S02 |
| FR-011 | High | Approved safety text can be absent from the released PDF | GA-R2 |
| FR-012 | Critical | The species plate rule passes without two real views of the stated organism | Pre-S06 |
| FR-013 | High | Whether an image is a real photograph is self-declared | Pre-S06 |
| FR-014 | Medium | Photo metadata, including GPS position, is copied into release PDFs | Pre-S06 |
| FR-015 | Medium | Licence checks accept restrictive or meaningless terms | Pre-S06 |
| FR-016 | High | Nothing expires: legal, medical and regulatory content has no freshness control | Pre-S02 / Pre-S15 |
| FR-017 | High | A correction does not withdraw what was already built | Pre-S05 / Pre-S15 |
| FR-018 | Medium | The log gate misses a warning class; shared source links point to another entry | Pre-S03 |
| FR-019 | Medium | The unit check accepts large errors and cannot express common quantities | Pre-S02 |
| FR-020 | Medium | Layout limits push authors toward weaker entry types and shorter safety text | Pre-S03 / Pre-S06 |
| FR-021 | Medium | Required safety fields accept "N/A" | GA-R2 |
| FR-022 | Medium | Ledger history is not checked; hash and schema are unversioned | Pre-S02 |
| FR-023 | Low | Alt text is required but never reaches the reader | Pre-S13 |
| FR-024 | Low | Tests assert configuration text; none assert gate invariants | GA-R2 |
| FR-025 | High | No data model for taxon identity, look-alikes, edibility or minerals | Pre-S06 |
| FR-026 | Medium | No originals/derivatives split and no storage plan for the photo library | Pre-S06 |
| FR-027 | Medium | No controlled vocabularies or reference fields for indexes and cross-references | Pre-S02 / Pre-S13 |
| FR-028 | Low | Decorative fields give an impression of control | Pre-S02 |
| FR-029 | High | The approval hash is computed by the operator after review; nothing records what the reviewer read | Pre-S02 |

---

## A. Review independence and revocation

### FR-001 — Hazard class and entry type are chosen by the author; a mistyped or untagged entry skips every safety control

- **Severity:** Critical
- **Evidence:** `_is_hazardous` returns true only for a non-empty `hazard_tags` or `entry_type: medical_guidance` (`scripts/sfe/validate.py:325-326` at `dc67819`, `:328` at `a08104a`). Nothing derives either value.
  - P18: a Z05 (wild foods) entry typed `general` with no tags reaches `published` with one approval row and **0 safety rows**.
  - P18b: a Z10 (wilderness medicine) entry typed `technical_procedure` does the same.
  - P47: an entry resting on a claim typed `medical`, risk `critical`, is unaffected.
  - P46: a coverage row plans the entry with `hazard_topics: [HZ-FORAGING-ID]`; the entry carries none; no finding.
  - Only `general` and `technical_procedure` can be rendered (`scripts/sfe/texgen.py:20`). The type that avoids the species and medical rules is also the only type that can be released today.
- **Failure consequence:** Mushroom, plant, medical, water or preservation content reaches a release PDF with one ChatGPT approval row, no domain review, no plate rules and no positive-identification warning. It takes an omission, not an attack.
- **Required correction:** Classification is derived and cross-checked, never only declared.
  1. A zone policy table sets the allowed entry types and minimum hazard classes per zone. An exemption is a per-entry record, approved by the owner and bound to the content hash.
  2. Cited claims propagate: a claim of type identification, medical, legal or safety_boundary, or of risk critical or high, forces the matching hazard class.
  3. The coverage matrix's `hazard_topics` for a planned entry must be a subset of that entry's tags.
  4. An entry with no hazard class needs an explicit hazard-screening row, bound to the hash, from a reviewer who is not the author.
  5. Type-specific fields are legal only on their own type (see FR-011).
- **Acceptance criteria:** P18, P18b, P46 and P47 return errors. A matrix test over 16 zones × 4 entry types proves each disallowed combination fails. Removing a tag from an approved entry fails by rule, not only because the hash changed.
- **Recommended remediation model:** GPT (zone and hazard policy table) → ENG → REVIEW
- **Target sprint:** GA-R2 for the mechanism; Pre-S02 for the content of the policy table

### FR-002 — A recorded safety failure blocks only when it names a topic the entry is already tagged with

- **Severity:** Critical
- **Evidence** (at `a08104a`, `_evaluate_safety_subject`, `scripts/sfe/validate.py:463-477`): the rows considered for a topic are those that list it; the barrier is drawn only from those rows; rows are filtered by the entry's revision number first.
  - P04: pass pair, then a fail with **empty** `topics_reviewed` → ELIGIBLE. The schema allows an empty list (`schemas/safety_audit.schema.json`, no `minItems`).
  - P05: pass pair, then a fail naming a topic the entry is **not tagged with** → ELIGIBLE.
  - P06: any fail on an **untagged** entry → ELIGIBLE (safety rows are not read at all).
  - P52: fail keyed to revision 2 while the entry says revision 1, same content hash → ELIGIBLE.
  - P53: fail whose `entry_id` has a one-character typo → ELIGIBLE, and no warning.
- **Failure consequence:** GA-002 ("a newer failed safety review did not revoke an older passing review") persists in five forms after RUN-002. The case that matters most, a reviewer reporting a hazard the author did not tag, is exactly the case the gate ignores.
- **Required correction:** Every non-pass row bound to an entry id blocks that entry, whatever its topics, its revision number or the entry's tags. A non-pass naming an untagged topic raises its own error. Every ledger row must resolve (known entry id, revision not above the current one, known content hash) or the run fails. `topics_reviewed` may be empty only together with an explicit whole-entry scope value.
- **Acceptance criteria:** P04, P05, P06, P52 and P53 return errors. Metamorphic test: appending any non-pass row for an entry never leaves it eligible.
- **Recommended remediation model:** ENG → REVIEW
- **Target sprint:** GA-R2

### FR-003 — Precedence is decided by a reviewer-typed date and by file position

- **Severity:** High
- **Evidence:** order is `(reviewed_on, row position)` (`a08104a` `validate.py:431-433`); approvals and image audits use the same idea (`dc67819` `validate.py:86-87`). Dates are checked by pattern only.
  - P03a: pass pair dated 2099-01-01, fail appended afterwards → ELIGIBLE.
  - P03b: fail appended later but dated one day earlier, which is its true review date → ELIGIBLE.
  - P08a / P08b: the same three same-day rows are BLOCKED in one file order and ELIGIBLE in another. Sorting the CSV in a spreadsheet flips the outcome.
  - P11a / P11b: the same two behaviours for an approval withdrawal.
  - P24: `2026-02-31` and `2026-13-45` are accepted.
- **Failure consequence:** `reviewed_on` records when a review happened, not when it was entered. An honest reviewer who dates a failure correctly can be outranked by passes entered earlier with a later date. A mistyped year makes a pass permanent.
- **Required correction:** Order by ledger sequence, not by date: monotonic sequence ids, validated as strictly increasing and append-only against the last accepted commit. Parse dates as real dates and reject any later than a configured ledger as-of date. Negative decisions should not depend on order at all (FR-004).
- **Acceptance criteria:** P03a, P03b, P11a and P11b are blocked. P08a and P08b give the same result. Invalid and future dates are rejected. A row-permutation property test passes.
- **Recommended remediation model:** ENG → REVIEW
- **Target sprint:** GA-R2

### FR-004 — Conflicting decisions are settled by recency, not by resolution

- **Severity:** High
- **Evidence:**
  - P07 (`a08104a`): an external SME fails the entry; the same two original reviewers append new passes; the content is unchanged → ELIGIBLE.
  - P10a: ChatGPT approves, ChatGPT withdraws, a `technical_reviewer` approves later → ELIGIBLE. The gate checks the latest row of any role, plus "some `chatgpt_editorial` approval with this hash exists" (`dc67819` `validate.py:396-406`).
  - P10b: an SME rejects, the owner approves later → ELIGIBLE.
- **Failure consequence:** A specialist's objection to unchanged text disappears when anyone re-asserts. ChatGPT's own withdrawal of sign-off is overridden by another role. RUN-002 (decision D12) describes re-passing as the intended remediation path; for unchanged content that is reviewer shopping.
- **Required correction:** A non-pass decision stays in force until a resolution row cites its id. The resolution gives a reason, comes from the reviewer who recorded the failure or from a named adjudicator, and is bound to the content it clears. Changing the content does not clear a failure by itself, and neither do new passes from other reviewers: the full set of required passes is needed in addition to the resolution. Approvals are evaluated per role: the latest `chatgpt_editorial` decision must be `approved`, and any role's unresolved `rejected` or `withdrawn` blocks.
- **Acceptance criteria:** P07, P10a and P10b are blocked. A resolution-path test passes only with a row that cites the failing id and comes from an allowed reviewer.
- **Recommended remediation model:** GPT + OWNER (adjudication rule) → ENG → REVIEW
- **Target sprint:** GA-R2

### FR-005 — The two "independent" reviews can be the author and an unqualified or non-human reviewer

- **Severity:** High
- **Evidence:** the remediated policy maps `chatgpt_validation` to role `chatgpt_editorial`, and `domain_expert` to `technical_reviewer` or `external_sme` (`a08104a` `schemas/hazard_topics.yaml`, `review_policy`). The handoff makes ChatGPT the author and the approver (§0). Entries record no author.
  - P09: reviewer "GPT-6 High" as `technical_reviewer` plus "GPT-6 Extra High" as `chatgpt_editorial` → ELIGIBLE, no warning.
  - P09b: the same name in both classes gives a warning only, and the release **builds** (`release_ok: true`); `make validate` and `build_release` never use `--strict`.
  - No topic requires `external_sme`. There is no reviewer registry: identity, human or AI, qualification and scope are unrecorded.
- **Failure consequence:** One of the two reviews is self-review by design, so the effective independent control is a single row carrying a role label that any actor can type. Plan gates E1, F2 and G ("qualified mushroom experts", "food-safety experts") cannot be evidenced.
- **What is new:** decision D10 covers identical reviewer names only.
- **Required correction:** A reviewer registry (id, kind, qualifications by domain with an evidence reference, active dates). Ledger rows cite reviewer ids. Entries carry a hash-bound `authored_by`. No reviewer may review their own work. Each hazard class states the qualification it needs and whether a human is mandatory. The same reviewer in two classes is an error.
- **Acceptance criteria:** P09 and P09b are blocked. A row citing an unregistered or out-of-scope reviewer fails. Tier A classes (see `SPECIES_IDENTIFICATION_STANDARD.md` §10) fail without a registered human specialist.
- **Recommended remediation model:** OWNER + GPT (who qualifies) → ENG → REVIEW
- **Target sprint:** GA-R2 for the registry and author binding; Pre-S02 for the qualification table

### FR-006 — "verified" and "published" rest on self-typed fields; no release authorization record

- **Severity:** Medium
- **Evidence:**
  - P93: `technical_reviewer: "x"` satisfies the verified rung (`validate.py:339-340`). The field is outside the content hash (`scripts/sfe/entries.py:18-20`) and no ledger row stands behind it.
  - `published` adds only caption, alt-text and asset-review checks (`validate.py:438-450`). The status is typed by whoever edits the file. No row of role `user` is ever required, although handoff §9 Phase D and the plan reserve release authorization to the owner.
  - P36: for medical guidance, any safety row counts as the medical review, including rows that list a single unrelated topic.
- **Failure consequence:** The non-hazard path to release is one approval row plus typed names. The owner's release decision leaves no record that the build checks.
- **Required correction:** Technical review becomes a ledger row (hash-bound, registered reviewer). `published` requires a release-authorization row from the owner, bound to a release manifest digest. A medical review is marked by an explicit scope value.
- **Acceptance criteria:** verified without a technical-review row fails. A release without an owner authorization for the exact manifest digest fails. P36 fails.
- **Recommended remediation model:** ENG → REVIEW; OWNER for the authorization rule
- **Target sprint:** Pre-S02 (ledger row); Pre-S15 (release authorization)

### FR-007 — Hazard policy fields are declarative; reviews are not bound to the checklist they attest to

- **Severity:** Medium
- **Evidence:** `load_hazards` checks only that fields exist (`scripts/sfe/registry.py:160-183`). `authority_requirement` ("current CDC/EPA guidance", "tested USDA/NCHFP procedures"), `applies_when`, `reviewer_must_confirm` and `requires_region_and_as_of_date` are read by no gate; the legal rule is hard-coded to one tag (`validate.py:347`). The tests assert the YAML text (`tests/test_hazard_gates.py:24-33`).
  - P60: a mandatory confirmation added to a topic after the reviews were recorded → still ELIGIBLE.
- **Failure consequence:** This is the root cause of GA-001 (`required_reviews` was never read), still present for the sibling fields. A water entry can pass with no CDC or EPA source. When a checklist is tightened after an incident, earlier passes go on counting.
- **Required correction:** Each audit row carries the SHA-256 of the topic definition that was reviewed; a changed definition needs re-attestation. The authority requirement becomes structured source criteria, such as an issuing-body list per topic. Every key in the policy file is either enforced or removed.
- **Acceptance criteria:** P60 is blocked. A water or preservation entry with no source meeting the topic's criteria fails. A test proves every policy key has a consumer.
- **Recommended remediation model:** GPT (authority lists) → ENG → REVIEW
- **Target sprint:** Pre-S02

### FR-029 — The approval hash is computed by the operator after review; nothing records what the reviewer read

- **Severity:** High
- **Evidence:** `python -m sfe hash-entry FILE` prints "the content hash an approval row must carry" (`BUILD_PLAN.md` §3; `scripts/sfe/cli.py:74-83`). The reviewer works in a chat on pasted text; the operator hashes the local file and writes the ledger row. `BUILD_PLAN.md` §10 proposes a pack-ingest command that turns a ChatGPT pack into registers and entry files. No reviewer-originated artifact is stored, and no gate compares the pack with the entry.
- **Failure consequence:** The row proves that the operator bound an approval to the file as it stood when the row was written. It does not prove the reviewer saw that file. A step dropped or a number mistyped while a pack is restructured into front matter is hashed, and so counts as approved. Handoff §12 ("preserve the exact approved version of each chapter, and show a diff for every substantive change") has no mechanism.
- **Required correction:** The tool generates a review packet per entry: one file holding the full rendered text, images and the closure digest of FR-010. The reviewer's decision quotes the packet digest. The packet and the reviewer's reply are stored verbatim and their hashes go in the ledger row. The gate checks that the packet digest equals the current closure digest. Packs are stored unchanged with their hashes, and the mapping from pack to entry is deterministic and diffable.
- **Acceptance criteria:** An approval row with no stored packet fails. A packet whose digest differs from the current closure fails. A test changes one character between packet and entry and expects a block.
- **Recommended remediation model:** GPT (pack format it can emit) → ENG → REVIEW
- **Target sprint:** Pre-S02

---

## B. Evidence, traceability and what approvals cover

### FR-008 — Species and medical entries can be published with no claims at all

- **Severity:** High
- **Evidence:** claims are required only for procedure steps and unit-table rows (`validate.py:260-265`, `308-322`).
  - P19a: a medical entry with `procedure: []` and `claim_ids: []` reaches `published`.
  - P19b: a species profile with zero claims reaches `approved`.
  - Diagnostic features, look-alikes, dangers, contraindications, evacuation thresholds and processing restrictions are untraced prose. Every step may cite the same single claim.
- **Failure consequence:** Handoff §5 traceability and plan gate B ("high-consequence claims linked to dated source IDs") are not enforced for the two highest-risk entry types.
- **Required correction:** Safety-bearing fields become lists of `{text, claim_ids}`. Each entry type has minimum claim rules. The claim type must fit the field (identification, medical, legal, safety_boundary).
- **Acceptance criteria:** P19a and P19b fail. Any item in the listed fields without a verified claim fails at `researched` and above.
- **Recommended remediation model:** GPT (which fields) → ENG → REVIEW
- **Target sprint:** Pre-S02

### FR-009 — Claims are not tied to an exact source edition, and verification is an editable flag

- **Severity:** High
- **Evidence:**
  - P21: after approval, the claim text and locator are rewritten and the source edition and URL changed → still ELIGIBLE. The entry hash covers claim ids only, and `verified` is a cell in the same row as the text it describes.
  - P49: a verified source with edition `UNKNOWN`, revision `UNKNOWN`, no retrieval date, no hash, type `website` backs a published entry.
  - P22a: a source with rights `rejected` on a third-party mirror backs a published entry.
  - P22b: a `background` source backs a verified claim, contradicting `research/unresolved-research.md` ("background only").
  - The printed source legend shows id, title, rights, verification and use: no issuer, edition or date (P73 page text).
- **Failure consequence:** The evidence behind an approved instruction can change, or be unrecoverable, without any approval going stale. A reader cannot tell which edition was used.
- **Required correction:** One source row per edition, immutable once verified; a new edition is a new id with a `supersedes` link. A verified source needs an edition or date, a retrieval date and the content hash of an archived copy. Claim verification moves to a ledger row bound to a digest of claim text, source id, locator and source content hash. The entry approval covers the digests of its cited claims and sources. A source-tier rule scales with claim risk. Background and rights-rejected sources cannot back claims. The legend prints issuer, edition and date.
- **Acceptance criteria:** P21 goes stale. P49, P22a and P22b fail. Changing any byte of a cited claim or source row invalidates the approvals that depend on it.
- **Recommended remediation model:** GPT (source-tier policy) → ENG → REVIEW
- **Target sprint:** Pre-S02

### FR-010 — Approvals and safety reviews do not cover the images, captions and labels the page prints

- **Severity:** High
- **Evidence:**
  - P16: after approval and audits, the manifest caption, subject names, licence text and credit are rewritten → ELIGIBLE. The caption is printed on the page (`texgen.py:86-104`).
  - P17: the image file is replaced, the manifest hash updated, and a new image audit added by role `user` with all four checks false → ELIGIBLE. The entry approval and safety reviews stay valid because the entry hash holds asset ids only.
  - P12: an audit with `decision: pass` and identification, licence and provenance checks all false counts. The gate reads only the decision and the hash (`validate.py:421-434`).
- **What is new:** OBS-1 covers role gating only.
- **Failure consequence:** The photograph or diagram a specialist approved can be replaced and relabelled afterwards. Handoff §0 ("never substitute a plausible diagram for a factually verified diagram") cannot be enforced.
- **Required correction:** Approvals bind to a render-closure digest: the entry content, plus for each cited asset the file hash and every manifest field that is printed or evidentiary, plus the digests of cited claims and sources. An image-audit pass requires every applicable check to be true and a qualified registered reviewer. The audit binds to the manifest-row digest as well as the file hash.
- **Acceptance criteria:** P12, P16 and P17 fail. Changing one printed character of a caption makes the entry's approval stale.
- **Recommended remediation model:** ENG → REVIEW
- **Target sprint:** Pre-S02 for the hash scope; enforced before the first photograph at S06

### FR-011 — Approved safety text can be absent from the released PDF

- **Severity:** High
- **Evidence:**
  - P20: a `general` entry carrying `contraindications`, `emergency_evacuation_threshold`, `positive_identification_warning`, `identification_uncertainty` and `processing_restrictions` validates and releases (`release_ok: true`). **None of the five strings is in the PDF.** The body text is absent as well.
  - The schema permits type-specific fields on any entry type; `render_entry` ignores them (`texgen.py:130-209`).
  - Release QA requires only that entry ids appear in the text (`scripts/sfe/pdfbuild.py:314-317`).
  - The renderer's own docstring calls a silently dropped mandatory field "worse than no page at all".
- **Failure consequence:** The approver signs text that includes a warning. The reader's page lacks it. No gate reports anything.
- **Required correction:** Renderer totality: every non-empty, non-workflow field is rendered or the build fails. Type-specific fields are rejected on other types. A post-render check confirms each approved string occurs in the PDF text layer. Body text is rendered, or required to be empty until it can be.
- **Acceptance criteria:** P20 fails at validation or at render. A coverage test puts a unique token in every schema field and finds each one in the PDF.
- **Recommended remediation model:** ENG → REVIEW
- **Target sprint:** GA-R2 for the totality check; Pre-S03 for body rendering

### FR-022 — Ledger history is not checked; hash and schema are unversioned

- **Severity:** Medium
- **Evidence:**
  - P08c: deleting the failing row restores eligibility. No gate compares a ledger with its previous committed state.
  - The content hash covers every non-workflow key (`entries.py:78-81`) and the ledgers have no hash-version column. Adding a schema field, or changing `WORKFLOW_FIELDS`, changes every hash, and old rows become indistinguishable from stale ones.
  - The corrections for FR-008 to FR-011 and FR-029 all change what the hash covers.
- **What is new:** unsigned ledgers are documented (`BUILD_PLAN.md` limitation 2). Append-only checking and versioning are not.
- **Failure consequence:** Revocations are not durable. The first schema change after approvals exist forces mass re-approval, or invites narrowing the hash to avoid it.
- **Required correction:** An append-only check against the last accepted tag. Sequence ids. A hash-version column. A written migration procedure in which re-attestation is an explicit row, never an edit.
- **Acceptance criteria:** P08c fails. A migration test moves a fixture approval across a schema bump using an attestation row.
- **Recommended remediation model:** ENG → REVIEW
- **Target sprint:** Pre-S02

---

## C. Species identification and images

### FR-012 — The species plate rule passes without two real views of the stated organism

- **Severity:** Critical
- **Evidence:** the rule counts `verified_diagnostic` rows and distinct view labels, and nothing else (`validate.py:381-384`).
  - P13: **one image file** listed under two asset ids with two view labels satisfies the two-view rule.
  - P14: both photos are catalogued as a different subject than the entry's `scientific_name` → passes.
  - P15: views `look_alike` + `other` only, so no photo of the target organism → passes.
  - P13b: one file is verified diagnostic evidence for two different subjects → no error.
  - P32: two entries for the same scientific name using the same photos → no error.
  - P92: a diagnostic photo needs no scientific name, locality or observation date.
- **Failure consequence:** Handoff §3 ("no field-use identification based on a single photo") can be satisfied with one photograph. A plate can show a different, possibly toxic, organism than its title. The only remaining control is the image audit, which FR-010 shows passing with every check false.
- **Required correction:** `SPECIES_IDENTIFICATION_STANDARD.md` §§2–5 and §13, implemented as gates SIS-G01 to SIS-G24. In short: one manifest row per file hash and near-duplicate screening; the asset's taxon must equal the entry's taxon for target views; look-alike views are excluded from the minimum and must cite the look-alike's taxon; a perspective set per organism group; independent captures; one entry per accepted name.
- **Acceptance criteria:** P13, P13b, P14, P15, P32 and P92 fail. Each SIS gate has a failing fixture.
- **Recommended remediation model:** GPT + SME (perspective sets) → ENG → REVIEW
- **Target sprint:** Pre-S06; schema reserved Pre-S02

### FR-013 — Whether an image is a real photograph is self-declared

- **Severity:** High
- **Evidence:**
  - P91: `generation_method: camera_photo` or `scan` is accepted as typed. The AI rules (`scripts/sfe/assets.py:110-116`) fire only when the row itself says `ai_generated`.
  - `scan` qualifies as a real photograph whatever was scanned.
  - P34: an AI-generated illustration with blank subject fields needs no label and renders with the generic tag "ILLUSTRATION" (`assets.py:124`).
  - The hosts treated as recommended (`assets.py:29`) include open media repositories, where the host says nothing about how an image was made.
  - No original capture file, capture metadata, observation or accession identifier, or determiner is required.
- **Failure consequence:** The handoff's absolute rule (no AI specimen imagery as identification evidence) is enforced only against images whose cataloguer admits they are AI-generated.
- **Required correction:** Standard §13. A diagnostic photograph needs a source record id from an institution, or a named photographer's original file with its hash and capture metadata, plus the determiner and the basis of determination. AI screening is an attested check. Every generated image carries the label, with or without a subject. `scan` is split into scan-of-photograph and scan-of-artwork.
- **Acceptance criteria:** A diagnostic row with no source record or original-file evidence fails. P34 fails. Each rejection rule has a negative fixture.
- **Recommended remediation model:** GPT (evidence rules) → ENG → REVIEW; SME for the basis of determination
- **Target sprint:** Pre-S06

### FR-014 — Photo metadata, including GPS position, is copied into release PDFs

- **Severity:** Medium
- **Evidence:** P72: a JPEG with EXIF artist, description and GPS fields is embedded unchanged. `pdfimages -all` on the release PDF recovers the artist name and the coordinates.
- **Failure consequence:** Collection localities of protected or over-harvested species, and contributors' personal locations, are published. The manifest's `location_region` field controls nothing.
- **Required correction:** Publish derivatives only: a deterministic re-encode with metadata stripped. Archive the originals. Record and audit the lineage from original hash to derivative hash. Print locality only at an approved precision.
- **Acceptance criteria:** P72 recovers no EXIF. A lineage test passes.
- **Recommended remediation model:** ENG
- **Target sprint:** Pre-S06

### FR-015 — Licence checks accept restrictive or meaningless terms

- **Severity:** Medium
- **Evidence:** P90: "All rights reserved", "CC BY-NC-ND 4.0" with derivatives "none", and "Fair use" are accepted as approved licences. Only a short list of bare words is rejected (`assets.py:20-23`). There is no licence vocabulary, version or URL. `allowed_derivatives` is free text although the layout resizes every image and overlays a tag on it (`layouts/sfe.sty:130-146`). The printed credit line omits the work's title and the licence link.
- **What is new:** `BUILD_PLAN.md` limitation 3 says rights are checked as metadata only. The specific accepted values and the conflict between no-derivatives terms and the overlay are new.
- **Failure consequence:** Plan gate H ("legally cleared images") cannot be evidenced. Images under no-derivatives terms are modified by the layout.
- **Required correction:** A controlled licence list with each licence's obligations (attribution elements, derivatives, commercial use, share-alike). A machine check that the pipeline's operations are permitted. An attribution ledger generated from the manifest.
- **Acceptance criteria:** The restrictive P90 cases fail. An attribution-completeness test passes.
- **Recommended remediation model:** OWNER (distribution model: free or commercial) + GPT → ENG
- **Target sprint:** Pre-S06

### FR-025 — No data model for taxon identity, look-alikes, edibility or minerals

- **Severity:** High
- **Evidence:**
  - `scientific_name` is free text. `taxonomic_authority` may be null at `published` (`schemas/entry.schema.json:80-81`; `_species_rules` does not require it).
  - `lookalikes_or_confusions` is a list of strings with no link to another entry or taxon.
  - No field states an edibility position, so "no eat/not-eat guarantee" exists only as a reviewer checklist line.
  - `species_profile` is the only identification type and its fields are biological (phenology). Z08 rocks and minerals fall to `general`, which has no plate rule.
  - The zone flag `requires_photographic_reference_specimens` (Z04, Z08) feeds README text only (`registry.py:40-44`).
- **Failure consequence:** Gates D1, E1 and E2 cannot be evaluated by machine. The toxic look-alike matrix, an S06 deliverable, has nowhere to live.
- **Required correction:** Standard §2: taxon, look-alike pair and edibility-assertion records; a `material_profile` entry type; zone flags enforced.
- **Acceptance criteria:** Schemas and gates as the standard specifies, with a fixture for each prohibition in §12.
- **Recommended remediation model:** GPT + SME (content of the standard) → ENG → REVIEW
- **Target sprint:** schema reserved Pre-S02; complete Pre-S06 (plants), Pre-S08 (fungi), Pre-S09 (minerals)

### FR-026 — No originals/derivatives split and no storage plan for the photo library

- **Severity:** Medium
- **Evidence:** one manifest row is one file and one hash, and the image audit binds to that hash (`schemas/image_audit.schema.json`). Any resize or colour conversion changes the hash and makes the audit stale. So either full-resolution originals go into the PDFs, or every derivative is audited again. Photos live in the Git tree (`assets/original_photos`) with no large-file policy for the planned 350–600 photographs. Images are rendered at most 3.0 cm high (`texgen.py:110`).
- **What is new:** `BUILD_PLAN.md` limitation 5 says real photographs are untested. The conflict between audit hashes and derivatives, and the printed size, are new. (OBS-2 already records the TIFF mismatch.)
- **Failure consequence:** Either phone PDFs become unusably large, or the audit evidence is detached from what is printed. Diagnostic features may be illegible at card size.
- **Required correction:** Original and derivative records with lineage. A deterministic derivative recipe. A storage decision. A minimum printed size and resolution per perspective in the species layout.
- **Acceptance criteria:** A lineage test. A size-budget test per output profile. Legibility criteria in the plate layout review.
- **Recommended remediation model:** ENG; OWNER for storage
- **Target sprint:** Pre-S06

---

## D. Time, region and release

### FR-016 — Nothing expires: legal, medical and regulatory content has no freshness control

- **Severity:** High
- **Evidence:**
  - P29: a harvest-law entry with `as_of_date: 1990-01-01` and `region: ["anywhere"]` reaches `approved`.
  - `as_of_date` is required for one tag only (`validate.py:347`), and any date string is accepted (P24).
  - `region` and `season` are free text (`entry.schema.json:33-34`).
  - No gate compares any date with a release date; the build is deliberately free of the wall clock.
  - The released page shows no edition or as-of date (P73 page text).
- **Failure consequence:** Tracker risk R06's control ("region/date-stamped legal notes and revision trigger") has no trigger. A rebuild years later reissues old legal text as current.
- **Required correction:** Review-by or valid-until dates on claims and entries, by class (legal, medical, regulatory, source currency). A release-time gate against an explicit `release_as_of` in the build configuration, which keeps builds deterministic. Jurisdiction and season as controlled codes. An edition id and as-of date printed on every page.
- **Acceptance criteria:** P29 fails. A release holding any expired item fails. An unknown region code fails.
- **Recommended remediation model:** GPT (validity periods) → ENG
- **Target sprint:** Pre-S02 (vocabularies and fields); Pre-S09 (legal content); Pre-S15 (release gate)

### FR-017 — A correction does not withdraw what was already built

- **Severity:** High
- **Evidence:**
  - P25: a release builds a zone PDF. An approval is then withdrawn. The next release refuses (`APPROVAL_NOT_CURRENT`) and **leaves the old PDF and manifest in `dist/zones`**. A zone that loses its last published entry is neither rebuilt nor removed.
  - The release manifest holds entry hashes only (P20: keys `artifact, entries, environment, kind, latex_runs, output, pipeline, zone`). It has no commit, register, ledger, asset, layout, toolchain or font hashes. The proof manifest is richer than the release manifest.
  - The PDF carries no edition identifier. There is no errata or recall record.
- **Failure consequence:** Stale output containing a failed entry sits where releases are collected. A distributed offline PDF cannot be matched to the approvals in force when it was built.
- **Required correction:** One immutable directory per edition, written atomically. On refusal, the previous output is marked superseded or quarantined. A full-closure manifest. An errata ledger. An edition id and date printed in the PDF.
- **Acceptance criteria:** P25 leaves no current-looking stale PDF. The manifest reproduces the build from a clean checkout. The edition id is on every page.
- **Recommended remediation model:** ENG → REVIEW; Astra at integration
- **Target sprint:** Pre-S05 (first beta); Pre-S15

### FR-027 — No controlled vocabularies or reference fields for indexes and cross-references

- **Severity:** Medium
- **Evidence:** `region`, `season`, materials and techniques are free strings. Entries have no field for references to other entries. Look-alikes are names in prose. Handoff §7 requires indexes by species, technique, hazard, environment and season, and S13 builds them.
- **Failure consequence:** Every entry written before the vocabularies exist must be edited and approved again to be indexable, because the hash changes. Spelling variants split index entries. A renamed or withdrawn entry leaves dangling prose references that no gate can see.
- **Required correction:** Vocabularies and id-based reference fields now. Glossary term ids. A gate that every reference resolves to a published entry in the same edition.
- **Acceptance criteria:** An unknown code fails. A dangling reference fails. Indexes are generated from fields only.
- **Recommended remediation model:** GPT (vocabularies) → ENG
- **Target sprint:** Pre-S02 (fields); Pre-S13 (indexes)

---

## E. Pipeline and checks

### FR-018 — The log gate misses a warning class; shared source links point to another entry

- **Severity:** Medium
- **Evidence:**
  - P26: a zone PDF with two entries citing one source. The LaTeX log has `pdfTeX warning (ext4): destination with the same identifier (name{sfe:src:SRC-0001})` three times. The release reports only `PDF_UNTAGGED`. `_GENERIC_WARNING` (`pdfbuild.py:125`) requires "warning:" directly after "pdfTeX".
  - P94: one destination exists, on page 1. Entry two's source link on page 2 jumps to entry one's legend.
  - Release QA for a multi-entry PDF checks entry ids, page size and fonts, and no bookmark or link expectations.
- **Failure consequence:** From the first zone PDF with two entries, link integrity is silently wrong. Unknown warning classes pass unseen.
- **Required correction:** Unclassified warning lines are reported. A duplicate destination is an error. One legend per document, or destinations unique per entry. A test that resolves every link to its expected page.
- **Acceptance criteria:** P26 errors or produces no duplicates. The link-resolution test passes.
- **Recommended remediation model:** ENG
- **Target sprint:** Pre-S03

### FR-019 — The unit check accepts large errors and cannot express common quantities

- **Severity:** Medium
- **Evidence:**
  - P23, accepted as consistent: `1 mi / 2 km` (24 % apart), `1 in / 3 cm` (18 %), `2 lb / 1 kg` (10 %), `3 ft / 1 m` (9 %), `1 gal / 4 L` and `1 qt / 1 L` (6 %).
  - P23, rejected as unparseable: `1/4 in`, `4-6 in`, `1 tsp`. A correct temperature interval, `18 °F / 10 °C`, is rejected because every temperature is treated as absolute.
  - P28: an inconsistent conversion inside step text passes. Only `dimension_unit_table` is checked.
- **What is new:** decision D3 presents the policy as strict. It is strict only at high displayed precision.
- **Failure consequence:** Dose-like and distance quantities with material discrepancies pass. Authors move awkward quantities into prose, where nothing is checked.
- **Required correction:** A relative tolerance or a minimum number of significant figures. Quantity kinds for interval temperatures, ranges, fractions and household measures. A prose lint that flags number-plus-unit text outside the structured table. A limit direction (minimum or maximum) so rounding stays conservative.
- **Acceptance criteria:** The loose P23 pairs fail. A valid fraction, range and interval pass. P28 is flagged.
- **Recommended remediation model:** GPT (tolerance by quantity kind) → ENG
- **Target sprint:** Pre-S02 (water and food-safety packs depend on it)

### FR-020 — Layout limits push authors toward weaker entry types and shorter safety text

- **Severity:** Medium
- **Evidence:**
  - P70: 60 danger lines produce `LAYOUT_OVERFLOW` and `PDF_OUTSIDE_MARGIN`, and the release is refused. That is correct and fails closed. The cause is that the CHECK and FAILURE / DANGER panels are unbreakable minipages (`sfe.sty:111-114`).
  - P71: 40 procedure steps flow across pages correctly.
  - Species and medical layouts do not exist (`BUILD_PLAN.md` limitation 6).
- **What is new:** the consequence below. The missing layouts are documented; what they push authors to do is not.
- **Failure consequence:** Combined with FR-001 and FR-011, the cheapest way to make an entry build is to retype it as `general` or to cut safety text. An entry with a long danger list cannot be released at all until the layout changes.
- **Required correction:** Breakable safety panels. Species and medical layouts before those entry types are authored. A rule that a layout failure can be cleared only by a layout change or by a re-approved revision.
- **Acceptance criteria:** P70 builds with all 60 lines present. Species and medical specimens render every required field.
- **Recommended remediation model:** ENG
- **Target sprint:** Pre-S03 (panels); Pre-S05 (medical layout); Pre-S06 (species layout)

### FR-021 — Required safety fields accept "N/A"

- **Severity:** Medium
- **Evidence:** P27: `abort_if: "N/A"`, `verify: "-"` and `dangers: ["n/a"]` pass the verified rung on a hazard-tagged entry (`nonempty`, `validate.py:65-72`; placeholder list, `:36-40`).
- **Failure consequence:** Handoff §10 ("every physical procedure has a step, a verification check, and an error/abort condition") is met by filler.
- **Required correction:** Reject null-like tokens and one-word values in required safety fields. An explicit "no abort condition applies" needs a claim and a reviewer attestation.
- **Acceptance criteria:** P27 fails.
- **Recommended remediation model:** ENG
- **Target sprint:** GA-R2

### FR-023 — Alt text is required but never reaches the reader

- **Severity:** Low
- **Evidence:** P20: alt text is neither visible nor present as `/Alt` in the release PDF. It is printed in proofs only (`texgen.py:100-101`).
- **What is new:** this adds to decision D1 (untagged PDF). The gate enforces authoring effort that yields no accessibility result.
- **Failure consequence:** A reader using assistive technology gets no description of any figure, though each one was written and reviewed.
- **Required correction:** Emit alt text with the tagging solution chosen under D1. Until then, print a text description or state the limitation in the release notes.
- **Acceptance criteria:** An accessibility checker finds a description for every figure.
- **Recommended remediation model:** ENG
- **Target sprint:** Pre-S13, with the D1 spike

### FR-024 — Tests assert configuration text; none assert gate invariants

- **Severity:** Low
- **Evidence:** `tests/test_hazard_gates.py:24-33` checks that the YAML mentions "CDC/EPA" and holds exactly six topics, so extending the hazard list (decision D9) breaks a test. GA-001 existed while 449 of 449 tests passed. There are no property or metamorphic tests on the ledgers. The Gate A snapshot tests (`tests/test_gate_a_snapshot.py`) must be retired at Gate B, which leaves the real registers with no invariant tests.
- **Failure consequence:** A green suite says the configuration is worded as intended. It does not say the gate behaves as intended.
- **Required correction:** The invariant suite in `REQUIRED_REGRESSION_TESTS.md` §9. A test that each policy key has a consumer. Replacement invariants on the real registers when the snapshot tests retire.
- **Acceptance criteria:** The suite fails on each sabotage listed in `REQUIRED_REGRESSION_TESTS.md` §10.
- **Recommended remediation model:** ENG → REVIEW
- **Target sprint:** GA-R2

### FR-028 — Decorative fields give an impression of control

- **Severity:** Low
- **Evidence:** `claims.entry_ids`, the coverage matrix's `planned_entry_id`, `hazard_topics` and `risk_level`, the claim's `risk_level`, the zone flags and the source's `reliability_notes` are stored and never cross-checked (P46, P47).
- **Failure consequence:** A reviewer reading the schemas assumes controls that do not exist.
- **Required correction:** Enforce or remove each field. Add a test that lists every schema property with its consumer.
- **Acceptance criteria:** The property-consumer test passes with no exemptions that lack a written reason.
- **Recommended remediation model:** ENG
- **Target sprint:** Pre-S02

---

## Controls that held

These were probed and worked. They are listed so the corrections above do not disturb them.

| Control | Evidence |
|---|---|
| The baseline test suite reproduces on a clean export | `dc67819`: 447 passed, 2 skipped (both need a Git checkout). `a08104a`: 609 passed, 2 skipped. |
| GA-001 and GA-002, in the form RUN-002 describes, are fixed at `a08104a` | P01 and P02 are ELIGIBLE at `dc67819` and BLOCKED at `a08104a` |
| Entry text is bound to its approval | Any change to front matter or body makes the approval and safety reviews stale (existing tests; "before" state in P16 and P21) |
| Release fails closed on structural problems | Any error anywhere refuses the whole release; only `published` entries are built; unparseable files, unknown ids and schema violations are errors |
| Layout overflow fails closed | P70 refuses instead of clipping |
| Long procedures flow | P71: 40 steps, 2 pages, every step present |
| Builds are deterministic | P73: two release builds are byte-identical |
| The mechanism scales | P80: 1,000 entries, 3,000 claims and 1,000 approvals validate in 2.8 s. P81: a 120-entry zone PDF builds in 34 s, in 2 LaTeX runs. |
| Declared AI imagery is contained | A row that says `ai_generated` cannot be a photo or diagnostic evidence |
| TeX injection and shell escape | Existing tests hold; not re-attacked beyond reading the escaper |

The architecture does not need replacing. CSV registers in Git and the pdfLaTeX pipeline are adequate for the planned volume. What is missing is what the gates bind to and what they refuse.
