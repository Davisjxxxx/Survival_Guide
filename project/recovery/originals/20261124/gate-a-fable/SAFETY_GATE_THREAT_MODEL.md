# Safety gate threat model

| | |
|---|---|
| Review | FABLE-REVIEW-001, steps 2 and 4 |
| Commits | `dc678192da569638946ae9c8e4671cff2f7e8b0f` (baseline) and `a08104a540f8017ac8f60c3405e1585e542806e6` (RUN-002 remediation) |
| Question | By what paths can invalid information receive publication approval? |
| Evidence | Probe ids (P01 …) refer to `evidence/probes*.py` and the result files beside them |

## 1. Summary

The gates are strong against malformed input and weak against plausible input.
A file that will not parse, an unknown id, a changed sentence in an approved entry: all refuse the release.
An entry that is well formed, wrongly classified and supported by the cheapest values that satisfy each rule passes.

Three structural causes account for almost every counterexample in this document.

1. **The author chooses the entry's risk class.** Hazard tags and entry type are typed in by the author, and the safety gate runs only on what they declare (FR-001).
2. **Negative decisions are weak.** A failure counts only if it lands in the right topic, revision, date order and file position. Any later pass clears it (FR-002, FR-003, FR-004).
3. **Approvals bind to less than the page.** The hash covers the entry's text. It does not cover the images, captions, claims, sources or checklist the approval relied on, or what the renderer finally prints (FR-009, FR-010, FR-011, FR-029).

## 2. Who can cause a bad publication

The realistic threat is not an attacker. It is an honest participant, human or model, doing the cheapest thing that turns a red check green.

| Actor | Role in the project | How it produces a bad outcome without intending one |
|---|---|---|
| Authoring model (ChatGPT) | Writes content, approves it, gives final safety sign-off | Omits a hazard tag. Approves its own text. Its approval arrives as pasted text that someone else binds to a hash. |
| Ingesting model or operator (CLI) | Turns packs into entry files and ledger rows | Restructures prose into fields and drops or alters a value. Picks `general` because species and medical layouts do not render. Fills a required field with "N/A". Writes the hash after the fact. |
| Reviewer (model or person) | Records a pass or a fail | Dates a failure with the day it was done, not the day it was entered. Leaves `topics_reviewed` empty to mean "the whole entry". Flags a hazard the entry is not tagged with. Mistypes an entry id. |
| Cataloguer | Registers images | Lists one photograph under two ids. Keeps the source's species label. Improves a caption after the audit. |
| Maintainer | Edits registers | Sorts a CSV in a spreadsheet. Resolves a merge by reordering rows. Corrects a "typo" in a verified claim. |
| Integrator (Astra) | Final assembly | Collects PDFs from `dist/` that a later refusal should have withdrawn. |
| Deliberate insider | Any of the above | Every path above is also available on purpose. The ledgers are unsigned (documented, `BUILD_PLAN.md` limitation 2). |

One property of this project raises the stakes: the party being gated often writes the gate's evidence. The model that ingests a pack also appends the approval row for it. A gate that can be satisfied by typing a value will be satisfied by typing a value.

## 3. What each decision is actually bound to

"Bound" means a change to the thing makes the decision stale.

| Decision | Bound to | Not bound to |
|---|---|---|
| Entry approval (`reviews/approvals.csv`) | Entry id; revision number, which is itself outside the hash; SHA-256 of front matter minus five workflow fields, plus body | Image files. Manifest rows: caption, subject, role, view, licence, credit. Claim text and locator. Source edition. Hazard checklist. Layout. What the reviewer was shown. |
| Safety review (`reviews/safety-audit.csv`) | The same hash; the topics the row lists | Everything above, and the version of the checklist it attests to |
| Image audit (`reviews/image-audit.csv`) | Asset id; file SHA-256 | The manifest row describing the file. Its own four check flags, which are never read. |
| Claim "verified" | Nothing. It is a cell in the row it describes. | The claim text, locator, source, source edition |
| Source "verified" | Nothing, likewise | Edition, URL, retrieved copy |
| Technical and editorial reviewer | Nothing. A name typed in the entry, outside the hash. | Any ledger row |
| `published` status | Nothing. A word typed in the entry. | Any authorization by the owner |
| Released PDF | A manifest listing entry ids, revisions and hashes | The commit, registers, ledgers, assets, layout, toolchain, fonts |

## 4. Counterexamples

Each row is a concrete scenario in which content that should be blocked is eligible for release.
"Yes" under a commit means the counterexample works there.

### 4.1 Stale approvals

| # | Scenario | Probe | `dc67819` | `a08104a` | Finding |
|---|---|---|---|---|---|
| T01 | An approval dated 2099-01-01 survives a withdrawal entered afterwards | P11a | Yes | Yes | FR-003 |
| T02 | A withdrawal entered later, but dated one day before the approval, is ignored | P11b | Yes | Yes | FR-003 |
| T03 | A harvest-law entry stamped as of 1990-01-01, region "anywhere", is approved | P29 | Yes | Yes | FR-016 |
| T04 | A hazard checklist gains a mandatory item; reviews recorded before it still count | P60 | Yes | Yes | FR-007 |
| T05 | A claim's text, locator and source edition change after approval; nothing goes stale | P21 | Yes | Yes | FR-009 |
| T06 | A release is refused after a withdrawal; the previous PDF stays in `dist/` | P25 | Yes | Yes | FR-017 |

### 4.2 Multiple hazard classes

| # | Scenario | Probe | `dc67819` | `a08104a` | Finding |
|---|---|---|---|---|---|
| T07 | A reviewer fails the entry for a hazard class it is not tagged with; the failure is ignored | P05 | Yes | Yes | FR-002 |
| T08 | A reviewer fails the whole entry and leaves the topic list empty; ignored | P04 | Yes | Yes | FR-002 |
| T09 | An untagged entry carries a recorded safety failure; ignored | P06 | Yes | Yes | FR-002 |
| T10 | A medical entry tagged with one topic: two rows about that topic also count as its medical review | P36 | Yes | Yes | FR-006 |
| T11 | The coverage plan lists a hazard class for the entry; the entry omits it; no finding | P46 | Yes | Yes | FR-001 |

### 4.3 Conflicting review decisions

| # | Scenario | Probe | `dc67819` | `a08104a` | Finding |
|---|---|---|---|---|---|
| T12 | Pass pair, then a later-dated failure (GA-002 as documented) | P02 | Yes | **No** | Fixed |
| T13 | SME fails; the same two reviewers re-pass; content unchanged | P07 | Yes | Yes | FR-004 |
| T14 | Passes dated in the future outrank a failure entered afterwards | P03a | Yes | Yes | FR-003 |
| T15 | A failure dated with its true, earlier review date is outranked | P03b | Yes | Yes | FR-003 |
| T16 | Three same-day rows: blocked in one file order, eligible in another | P08a, P08b | n/a (always eligible) | Yes | FR-003 |
| T17 | ChatGPT withdraws approval; another role approves later | P10a | Yes | Yes | FR-004 |
| T18 | SME rejects; owner approves later | P10b | Yes | Yes | FR-004 |
| T19 | The failing row is deleted from the ledger | P08c | Yes | Yes | FR-022 |

### 4.4 Missing reviewer roles

| # | Scenario | Probe | `dc67819` | `a08104a` | Finding |
|---|---|---|---|---|---|
| T20 | One `user` row satisfies a hazard topic (GA-001 as documented) | P01 | Yes | **No** | Fixed |
| T21 | Both classes filled by rows naming two AI model labels | P09 | Yes | Yes | FR-005 |
| T22 | Both classes filled by one named person; warning only; release builds | P09b | Yes | Yes | FR-005 |
| T23 | The verified rung is met by `technical_reviewer: "x"` with no ledger row | P93 | Yes | Yes | FR-006 |
| T24 | Image audits pass by role `user` with every check false | P12 | Yes | Yes | FR-010 |
| T25 | A failure row with a one-character typo in the entry id vanishes silently | P53 | Yes | Yes | FR-002 |
| T26 | A failure keyed to another revision number of identical content is ignored | P52 | Yes | Yes | FR-002 |

### 4.5 Reused photographs

| # | Scenario | Probe | `dc67819` | `a08104a` | Finding |
|---|---|---|---|---|---|
| T27 | One image file under two asset ids meets the two-view rule | P13 | Yes | Yes | FR-012 |
| T28 | One image file is diagnostic evidence for two different subjects | P13b | Yes | Yes | FR-012 |
| T29 | Two entries for the same scientific name share the same photos | P32 | Yes | Yes | FR-012 |

### 4.6 Incorrect species labels

| # | Scenario | Probe | `dc67819` | `a08104a` | Finding |
|---|---|---|---|---|---|
| T30 | Both plate photos are catalogued as a different subject than the entry's species | P14 | Yes | Yes | FR-012 |
| T31 | The plate holds only `look_alike` and `other` views | P15 | Yes | Yes | FR-012 |
| T32 | Subject names and caption are rewritten after audit and approval | P16 | Yes | Yes | FR-010 |
| T33 | A diagnostic photo has no scientific name, locality or date | P92 | Yes | Yes | FR-012 |
| T34 | An image typed as `camera_photo` is accepted as one | P91 | Yes | Yes | FR-013 |
| T35 | An AI illustration with blank subject fields needs no label | P34 | Yes | Yes | FR-013 |

### 4.7 Unverified medical procedures

| # | Scenario | Probe | `dc67819` | `a08104a` | Finding |
|---|---|---|---|---|---|
| T36 | A Z10 entry typed `technical_procedure`, no tags: published with no safety review | P18b | Yes | Yes | FR-001 |
| T37 | A medical entry with zero claims is published | P19a | Yes | Yes | FR-008 |
| T38 | An untagged entry rests on a claim typed medical, risk critical | P47 | Yes | Yes | FR-001 |
| T39 | Approved contraindications and evacuation threshold are missing from the PDF | P20 | Yes | Yes | FR-011 |
| T40 | A Z05 entry typed `general`: published with no safety review and no plate rules | P18 | Yes | Yes | FR-001 |

### 4.8 Incorrect unit conversions

| # | Scenario | Probe | `dc67819` | `a08104a` | Finding |
|---|---|---|---|---|---|
| T41 | `1 mi / 2 km`, `1 in / 3 cm`, `2 lb / 1 kg`, `1 gal / 4 L` are accepted as consistent | P23 | Yes | Yes | FR-019 |
| T42 | An inconsistent conversion inside step text is not checked | P28 | Yes | Yes | FR-019 |
| T43 | Fractions, ranges and household measures cannot be entered, so they move to prose | P23 | Yes | Yes | FR-019 |

### 4.9 Legal restrictions changing over time

| # | Scenario | Probe | `dc67819` | `a08104a` | Finding |
|---|---|---|---|---|---|
| T44 | No date in any register is compared with a release date | P29 | Yes | Yes | FR-016 |
| T45 | Calendar-impossible dates are accepted | P24 | Yes | Yes | FR-003 |
| T46 | Region is free text; "anywhere" satisfies "region-specific" | P29 | Yes | Yes | FR-016 |
| T47 | A released PDF shows no edition or as-of date | P73 | Yes | Yes | FR-017 |

### 4.10 Approved text modified after review

| # | Scenario | Probe | `dc67819` | `a08104a` | Finding |
|---|---|---|---|---|---|
| T48 | Entry text is edited after approval | existing tests | **No** | **No** | Control holds |
| T49 | An image is swapped after approval and safety review | P17 | Yes | Yes | FR-010 |
| T50 | Captions and credits are rewritten after approval | P16 | Yes | Yes | FR-010 |
| T51 | Text is altered between the reviewer's reading and the hashing | by design; no artifact records what was read | Yes | Yes | FR-029 |
| T52 | Approved fields are dropped by the renderer | P20 | Yes | Yes | FR-011 |
| T53 | A source rated background-only, or rights-rejected, backs a published claim | P22a, P22b | Yes | Yes | FR-009 |

Of 53 scenarios, the remediation closes 2 (T12, T20). One was already closed (T48). Fifty remain open at `a08104a`.

## 5. Why the remediation's precedence rule is not sufficient

RUN-002 fixed the reported shape of GA-002: pass, then a later-dated fail on a tagged topic in the same revision. The rule it introduced has four dependencies, and each one can fail on its own.

| The barrier takes effect only if … | Otherwise | Probe |
|---|---|---|
| the failing row lists a topic the entry is tagged with | the failure is not a barrier for anything | P04, P05, P06 |
| the failing row carries the entry's current revision number, a field outside the hash | the row is filtered out before evaluation | P52 |
| the failing row's date is not earlier than the passes | the passes outrank it | P03a, P03b |
| on a tie, the failing row sits lower in the file | the passes outrank it | P08b |

And once it takes effect, any new pair of passes dated after it clears it, without the content changing and without the failing reviewer's agreement (P07).

A revocation that depends on four free-text fields being filled in the expected way is not a revocation. The fix is to invert the default: a non-pass decision blocks unless something explicitly resolves it.

## 6. Invariants the gate must hold

These are the oracle for `REQUIRED_REGRESSION_TESTS.md`. None holds at `a08104a`.

| ID | Invariant | Violated by |
|---|---|---|
| INV-1 | **Negative decisions are absorbing.** While any non-pass decision bound to an entry, or to an asset it cites, is unresolved, the entry is not eligible. Topics, tags, revision numbers, dates and row order do not affect this. | T07–T09, T13–T18, T25, T26 |
| INV-2 | **Ledgers are monotonic.** Appending a row can block, or unblock only by explicit resolution. Permuting rows never changes eligibility. Editing or deleting a row relative to the last accepted commit is an error. | T16, T19 |
| INV-3 | **Approvals cover the closure.** Every byte that is printed for an entry, or that evidences it, is covered by the digest each approval and review carries: entry, image files, manifest fields, claims, sources, checklist version. | T04, T05, T32, T49, T50 |
| INV-4 | **Classification is derived.** Hazard classes, entry type and required reviews are a function of zone, cited claims and the coverage plan. An author can raise them, never lower them. | T11, T36, T38, T40 |
| INV-5 | **Duties are separated.** No review counts if the reviewer is the author. Required classes are filled by distinct, registered reviewers qualified for the class, human where the class says so. | T21–T24 |
| INV-6 | **Rendering is total.** Every approved, non-empty content field appears in the output, or the build fails. | T39, T52 |
| INV-7 | **Evidence is complete.** Every safety-bearing statement has a verified claim, bound to an immutable source edition with a content hash. | T37, T53 |
| INV-8 | **Identification evidence is real and matches.** Target views show the entry's taxon, from independent captures, in the required perspectives, with a recorded determination and no generated imagery. | T27–T31, T33–T35 |
| INV-9 | **Nothing is released past its validity.** At the configured release date, no claim, review, legal status or source is expired. | T03, T44 |
| INV-10 | **A release has an identity.** Each PDF maps to one manifest that reproduces it and lists the approvals in force. Superseded output cannot sit where current output is collected. | T06, T47 |
| INV-11 | **Ledger rows resolve.** Every row refers to an entry, revision, hash, asset and reviewer that exist. An orphan row is an error, most of all an orphan negative row. | T25, T26 |
| INV-12 | **No decorative policy.** Every policy key and schema field has a consumer that enforces it, or is removed. | T04, T11, T38 |
| INV-13 | **The reviewer's reading is recorded.** Each decision cites a stored packet whose digest equals the closure digest. | T51 |

## 7. What no gate can close

The build plan already says the gates check evidence and consistency, never truth (`BUILD_PLAN.md` limitation 1). Three residual risks remain after every correction in this review, and need controls outside the code.

| Residual risk | Why code cannot close it | Compensating control |
|---|---|---|
| A qualified reviewer is wrong | The ledger can show who reviewed, not whether they were right | Two human specialists for the highest tier (standard §10); errata process (FR-017); tracker risk R08's field checks |
| A registered reviewer does not exist or did not review | Ledgers are unsigned | Review packets returned by the reviewer through a channel the operator does not control; owner spot-checks against the registry; signing if the owner later wants it |
| Sources are authoritative and wrong, or change after retrieval | Verification compares text to source, not source to the world | Archived copies with hashes (FR-009); validity periods (FR-016); a scheduled source re-check before each edition |

## 8. Order of correction

Fix the three structural causes in this order. Each later step relies on the earlier one.

1. **Make negative decisions absorbing and ledgers resolvable** (INV-1, INV-2, INV-11). Small, local to the gate, and it closes the most scenarios.
2. **Derive classification** (INV-4). Without it, the safety gate can be skipped entirely.
3. **Record who authored and who reviewed** (INV-5).
4. **Widen what approvals bind to, and record what was read** (INV-3, INV-13). Do this before the first real approval exists, because it changes the hash.
5. **Make rendering total** (INV-6).
6. Evidence completeness, identification evidence, validity and release identity (INV-7 to INV-10), in the sprints `SPRINT_RECOMMENDATIONS.md` assigns.
