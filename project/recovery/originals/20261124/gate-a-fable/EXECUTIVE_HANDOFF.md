# Executive handoff — FABLE-REVIEW-001

**For:** the owner, ChatGPT (research and editorial), the CLI engineering models, and Astra.
**Date:** 2026-11-17
**Commit reviewed:** `dc678192da569638946ae9c8e4671cff2f7e8b0f` (tag `gate-a-submission`). Also probed: `a08104a540f8017ac8f60c3405e1585e542806e6` (tag `gate-a-remediation-1`, RUN-002).

## The decision in front of you

Whether to close Gate A, and whether S02 may start recording sources, claims and approvals on 2026-12-14.

**This review does not approve Gate A, and the evidence does not support closing it on either commit.**
The scaffold is well built and does not need replacing. But its safety gates can be passed by content that is wrongly classified, weakly reviewed, or changed in places the approval does not cover. Three Critical and twelve High findings are open at both commits.

## What was found

**1. The author decides whether the safety gate runs.**
Hazard tags and entry type are typed by the author. A wild-foods or first-aid entry typed as an ordinary entry, with no tags, reaches `published` with one approval and no safety review. Only the ordinary entry types can be rendered today, so that is also the easiest way to get a page to build. *(FR-001, Critical)*

**2. A recorded safety failure often blocks nothing.**
RUN-002 fixed the reported case. After it, a failure is still ignored when the reviewer leaves the topic list empty, flags a hazard the entry is not tagged with, dates the failure earlier than the passes, mistypes the entry id, or uses another revision number. When a failure does block, two new passes clear it, with no change to the text and no agreement from the reviewer who failed it. *(FR-002 Critical; FR-003, FR-004 High)*

**3. One photograph of the wrong organism can pass as a verified plate.**
The same image file listed under two ids satisfies the "two complementary views" rule. Nothing compares a photograph's subject with the species the entry is about. *(FR-012, Critical)*

**4. "Independent review" can be one model reviewing itself.**
ChatGPT writes the entry, approves it, and supplies one of the two safety reviews. The other can be any row labelled `technical_reviewer`, including one that names another AI model. There is no record of who wrote an entry and no registry of who is qualified. *(FR-005, High)*

**5. An approval covers the entry's words and nothing else on the page.**
Images, captions, species labels, the claims and the source editions behind the text can all change after approval without making it stale. Approved warnings can be missing from the PDF: in one probe, five approved safety fields were absent from the released page and nothing reported it. *(FR-009, FR-010, FR-011, FR-029, High)*

**6. Nothing expires, and nothing is withdrawn.**
A legal entry dated 1990 passes. When a release is refused after a withdrawal, the previous PDF stays in the output folder. A released PDF shows no edition or date. *(FR-016, FR-017, High)*

In total: 29 findings (3 Critical, 12 High, 11 Medium, 3 Low), each reproduced by a probe on an exported copy of the commit, or cited to file and line.

## What is sound

- Any malformed input refuses the whole release.
- The text of an approved entry cannot change without the approval going stale.
- Builds are byte-identical, and the pipeline handles the planned volume: 1,000 entries validate in 2.8 seconds, and a 120-page zone builds in 34 seconds.
- A layout overflow refuses to build instead of clipping text.
- The run records are candid about their limits.

## What to do, in order

| When | What | Who |
|---|---|---|
| **Now, before Gate A re-review** | Make every unresolved failure block the entry. Order ledgers by sequence, not typed dates. Clear a failure only by an explicit resolution. Derive hazard class from zone and claims. Add a reviewer registry and an author record. Refuse to build when an approved field is not rendered. | Engineering model, then an independent re-review. ChatGPT supplies the zone and hazard policy table. The owner names who can be registered. |
| **Before S02 ingestion** | Widen what an approval covers to claims, sources and images, and store what the reviewer was shown. Pin sources to editions with hashes. Require claims for safety statements. Version the ledgers. | Engineering model with ChatGPT, since ChatGPT must emit packs in the agreed form |
| **Before S06 and S08** | Adopt the species identification standard: a real determination for every evidence photo, look-alikes documented to the same standard as the target, a default of no edibility statement, and human specialists for the highest-risk groups. | ChatGPT and qualified specialists set the content; the engineering model implements the gates |
| **Before S13 and S15** | Indexes from controlled fields. Edition identity, errata and a full release manifest. A freshness check and the owner's recorded authorization at release. | Engineering model; Astra consumes editions, never loose files |

The reason for the order: the "before S02" items change what the approval hash covers. Done now, that costs nothing. Done after approvals exist, it invalidates all of them. Research itself does not have to wait; only ingestion and the recording of approvals do.

## Decisions needed from the owner

1. **Gate A.** Hold it until the first row of the table above is fixed and re-reviewed?
2. **S02.** If the "before S02" work is not finished by 2026-12-14, pause ingestion and approvals while research continues?
3. **Reviewers.** Who may be registered as a specialist for medical, plant, fungus, food-safety and legal content, and who settles a disputed failure?
4. **Fungi.** With no qualified mycologist engaged, do mushroom profiles publish as identification-only with no edibility statement, or not at all?
5. **Images.** Is the book free or sold? That decides which image licences can be used.

Input on the build plan's open decisions D1, D3 and D9–D12 is in `SPRINT_RECOMMENDATIONS.md` §11. In short: do not approve the unit policy (D3) as written, because `1 mi / 2 km` and `1 gal / 4 L` pass it.

## Where to read more

| If you want | Read |
|---|---|
| The full report and method | `FABLE-REVIEW-001.md` |
| Every finding with evidence, fix and acceptance criteria | `ARCHITECTURE_FINDINGS.md` |
| How a bad page gets approved: 53 scenarios | `SAFETY_GATE_THREAT_MODEL.md` |
| The identification standard | `SPECIES_IDENTIFICATION_STANDARD.md` |
| The tests the fixes must pass | `REQUIRED_REGRESSION_TESTS.md` |
| The sprint-by-sprint plan | `SPRINT_RECOMMENDATIONS.md` |
| The probes and their output | `evidence/` |

All files are in `/home/jd/Survival_Guide_Fable_Review/`.

## Handback block

```
REVIEW ID: FABLE-REVIEW-001 (independent preproduction adversarial review)
REVIEWER: Claude Code (Fable 5.2); not the author of any reviewed code
COMMIT REVIEWED: dc678192da569638946ae9c8e4671cff2f7e8b0f (gate-a/scaffold, tag gate-a-submission)
ALSO PROBED: a08104a540f8017ac8f60c3405e1585e542806e6 (gate-a/remediation-1, tag gate-a-remediation-1)
CHANGED FILES IN THE REPOSITORY: none. Output is outside it, in /home/jd/Survival_Guide_Fable_Review/
WHAT WAS VERIFIED: project suites reproduce on clean exports (447 passed + 2 skipped; 609 passed + 2 skipped);
  GA-001 and GA-002 reproduce at dc67819 and their reported cases are blocked at a08104a;
  59 probes run against both commits; release determinism and scale confirmed.
WHAT WAS FOUND: 29 findings: 3 Critical (FR-001, FR-002, FR-012), 12 High, 11 Medium, 3 Low; all present at both commits.
  Of 53 counterexample scenarios, RUN-002 closes 2.
WHAT IS STILL UNVERIFIED: truth of any content (none exists); behaviour on other toolchains; whether the species
  standard's character classes and photo sets suffice (needs a botanist, a mycologist and a geologist).
GATE A: NOT APPROVED by this review. Recommendation: do not close on either commit.
BLOCKING DECISIONS FOR THE OWNER: hold Gate A; S02 ingestion timing; reviewer registry and adjudicator;
  fungi fallback; distribution model.
NEXT STEP: Gate A remediation 2 (SPRINT_RECOMMENDATIONS.md section 3), test-first against
  REQUIRED_REGRESSION_TESTS.md, then an independent re-review by a model that did not write the fix.
```
