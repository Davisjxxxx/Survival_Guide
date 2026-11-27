# Opus resumption: implement RT01 before the next visual batch

## Objective and checkpoint

Correct the concrete defects in [RT01](README.md) and add the targeted controls that prevent them from recurring. Then resume the existing visual-production queue. This is an implementation brief for the paused Opus run, not a new full-encyclopedia audit or permission to publish.

The review examined `84967d75af91bbf0d2cb36c54394dcf67f2104a5` on `review/opus-wave-2c-production-20261125` (draft PR #11). At that checkpoint, the authoritative W2C register has 22 provisional plates across B01-B05 and 353 queued technical items. The PR body saying eight completed plates is stale. The review could not inspect uncommitted work on the source machine.

Inspect the current local status and remote head first. Preserve all uncommitted work. If local or remote production has advanced, compare the affected files with the pinned review before applying any proposed fix. Use the existing production branch or its established safe continuation; do not reset, clean, force-push or overwrite a newer checkpoint.

The review branch contains additive documentation under `reviews/rt01/` only. It does not contain implementation fixes. It can be read without merging or changing the paused worktree, for example:

```sh
git fetch origin review/astra-rt01-adversarial-20261127
git show FETCH_HEAD:reviews/rt01/README.md
git show FETCH_HEAD:reviews/rt01/OPUS_RESUME.md
```

## Batch R1: high-consequence instruction and propagation defects

Read the exact evidence, counterevidence and acceptance cases in [FINDINGS.json](FINDINGS.json), not just this summary.

1. **RT01-01 / Z11-P63:** Convert the six-item rescue report from a prerequisite to calling into a preparation/on-call aid. Preserve location-first communication and immediate activation when help is required. Do not substitute a new universal emergency-care sequence for clinician/dispatcher guidance.
2. **RT01-02 / Z10-P06:** Separate ongoing observation from periodic documentation. Remove the unsupported implication that checking an unstable patient's breathing can wait for a 15-minute logging interval. Do not invent a replacement fixed clinical interval.
3. **RT01-03 / Z10-P26:** Carry the existing substance-specific and qualified-isolation limits into the diagram, stage labels, caption and alternative text. Brushing and irrigation are not inherently wrong; the missing exceptions and scene-safety conditions are the issue. This plate sits outside the 375-row physical reconstruction queue, so add an explicit repair item.
4. **RT01-04 / Z04-P51:** Separate formula preparation from the generic safe-water task list. Carry the existing P26/Z14-P74 infant-specific boundary into the operational card, with a working offline route. Keep powder contamination distinct from source-water contamination and preserve chemical-advisory restrictions.
5. **RT01-05 / Z13-P49/P50:** Remove sanitizer-only equivalence after waste/diaper/vomit tasks in the norovirus scenario. Keep the legitimate interim fallback when soap and water truly are unavailable, with its limits; water conservation alone must not make it an equivalent replacement.

For each correction, trace all affected claim references, manuscript fields, diagram specifications, SVG visible text and `desc`, HTML alt/caption, atlas excerpts and print derivatives. Keep original custody and historical audit records. Write a new implementation decision with source URL, exact applicable section, scope, remaining specialist owner, before/after wording and acceptance receipt. Do not close a human hold or mark a source issue resolved merely because a URL loads.

## Batch R2: residual visual and navigation correctness

- **RT01-07 / Z14-P41:** Make the refrigerator and freezer paths distinct; require the applicable food-category row before keep/refreeze. Carry the existing A02 prose correction into the diagram and alternative text. The official chart's exceptions govern; no universal ice-crystal shortcut.
- **RT01-08 / Z11-P32:** Replace exact-line return guarantees with an approximate method and explicit uncertainty when stride or terrain changes. Keep the compact-obstacle and safe-ground limits. A matching bearing or pace count alone does not confirm position.

These proposed changes remain editorial candidates until the applicable clinical, food, navigation and other specialist reviews are supplied. Do not describe an AI review as a qualified approval.

## Batch R3: targeted production controls

- **RT01-09:** Make the compass check derive bearing relationships from delivered visible geometry, including transforms, rather than trusting `data-bearing`. Keep the separate byte-reproducibility check. A 90-degree visible-needle mutation with unchanged metadata must fail. The current unmodified compass is not alleged to be wrong.
- **RT01-10:** Extend safety checks to all instruction surfaces. Tie negation to the relevant instruction. Use the seven unsafe fixtures and safe control in `probes/probe_safety_linter.py` as targeted test cases. They are negative test data only; never copy them into a manuscript. Preserve the existing positive controls.
- **RT01-11:** Add a current evidence-assessment layer to reader evidence panels. Demonstrate it with K09 and its 25 referencing cards. Keep baseline assertions and historical ledgers intact while exposing the latest unresolved or bounded assessment. The owner decision on atlas design promotion does not automatically settle how a known source limitation is displayed.

Do not replace these focused tests with a claim that regex checks establish semantic or scientific safety. Report exactly which control is exercised and what remains outside it.

## Batch R4: prove current artifact consistency

Resolve **RT01-06** before another package is described as current. The inspected consolidated Letter proof has nine old B04/B05 figure headers. Both consolidated sizes and the packaged Z14 Letter proof retain the older Z14-P53 figure, despite corrected current HTML/SVG. Existing hashes match those older bytes.

Rebuild affected zone and consolidated proofs, or explicitly withhold/mark older proofs until rebuilt. Add a source-input fingerprint for the manuscripts, figures and print styles to print receipts. Preserve historical proofs under clearly historical custody if required. A valid byte hash alone must not authorize an older proof as the current edition.

Inspect the affected card at narrow and desktop widths, its figure by itself, its alternative text, and Letter/A4 renderings. For the food and chemical cases, test the adversarial scenario from the register against each form. Open the extracted zone ZIP offline and verify that its reader, diagrams and PDFs agree. Retain the normal relevant production, custody, package and accessibility checks; do not claim formal PDF/UA, assistive-device, field or human specialist approval from these checks.

## Separate follow-ups, without inflating the defect count

- **RT01-C01:** Ask the clinical reviewer about an early consultation branch for potentially high-risk tick bites. The current removal-and-symptom-watch text was not established as false.
- **RT01-C02:** Add/test a clear offline figure-enlargement route and a real-phone diagram-reading task. Small embedded labels are a usability candidate, not a demonstrated WCAG violation.
- **RT01-C03:** Confirm the process-duration condition for boiling-water canner water coverage, including elevation-adjusted processes longer than 30 minutes.

Continue the remaining visual queue only after the relevant fixes and their narrow regression checks are recorded. Preserve all 1,016 allocated cards, 16 zones, historical source custody, diagnostic and consumption holds, and all pending specialist gates. Publication remains **HOLD**. Do not merge or publish the stacked PR chain as part of this task.

## Completion report

Report which RT01 items were implemented, which remain open, the exact tests and artifact comparisons performed, the resulting production commit/PR, and any changed queue counts. Distinguish an implemented correction, an AI-checked editorial candidate and a qualified human approval. Keep the original RT01 findings and append implementation outcomes instead of rewriting the historical review.
