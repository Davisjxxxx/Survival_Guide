# Required regression tests

| | |
|---|---|
| Review | FABLE-REVIEW-001, step 4 |
| Commits | Specified against `a08104a540f8017ac8f60c3405e1585e542806e6`; every test marked "fails today" also fails at `dc678192da569638946ae9c8e4671cff2f7e8b0f` unless noted |
| Count | 102 example-based test specifications, 12 property tests, 20 sabotage checks |

## 1. Conventions

1. **Test first.** Each test is written and shown to fail on the current commit before the fix, as RUN-002 did for GA-001 and GA-002. A reviewer other than the implementer confirms the failure.
2. **Throwaway fixtures, neutral text.** Tests build temporary repositories with "Fixture …" strings, as the existing suite does. No test puts survival content on disk.
3. **Assert the verdict and the reason.** Each test asserts that a specific error code is raised. A test that only asserts "some error" passes for the wrong reason.
4. **Error codes below are suggestions.** The behaviour is the requirement.
5. **"Fails today"** means the scenario is currently eligible for release. The probe in brackets reproduces it (`evidence/probes*.py`). **"New"** means no code path exists yet.

## 2. Safety-review ledger

| ID | Finding | Given | Must result in | Today |
|---|---|---|---|---|
| RT-001 | FR-002 | Tagged entry with a valid pass pair; a `fail` row with empty `topics_reviewed` is appended | Blocked: `SAFETY_FAILURE_UNRESOLVED` | Fails (P04) |
| RT-002 | FR-002 | Same, but the fail names a topic the entry is not tagged with | Blocked, plus `HAZARD_REPORTED_NOT_TAGGED` naming the topic | Fails (P05) |
| RT-003 | FR-002 | Entry with no tags, not medical; any `fail` row for it | Blocked | Fails (P06) |
| RT-004 | FR-002 | Fail row carries another revision number, same content hash | Blocked | Fails (P52) |
| RT-005 | FR-002 | Any ledger row (safety, approval, image audit) whose entry or asset id does not exist | Error `LEDGER_ROW_ORPHAN`, for pass and non-pass rows alike | Fails (P53) |
| RT-006 | FR-002 | Fail row whose content hash matches no known state of the entry | Blocked, never dropped as stale | Fails |
| RT-007 | FR-002 | RT-001 to RT-004 repeated with `conditional` | Same results | Fails |
| RT-008 | FR-003 | Pass rows dated later than the ledger as-of date | Rows rejected: `LEDGER_DATE_IN_FUTURE` | Fails (P03a) |
| RT-009 | FR-003 | Fail appended after the passes, dated one day before them | Blocked | Fails (P03b) |
| RT-010 | FR-003 | Rows `[pass, pass, fail]` with one date, in each of the six file orders | Blocked in all six | Fails (P08b) |
| RT-011 | FR-003 | `2026-02-31`, `2026-13-45`, `0000-00-00` in each date column of each register and in `as_of_date`, `evidence_date` | Schema error in every case | Fails (P24) |
| RT-012 | FR-003 | A row inserted between two existing rows; two rows swapped | `LEDGER_SEQUENCE_BROKEN` | New |
| RT-013 | FR-004 | SME fail, then both original reviewers append new passes; content unchanged; no resolution row | Blocked | Fails (P07) |
| RT-014 | FR-004 | Fail, a resolution row citing its id from the failing reviewer, and the required passes | Eligible | New |
| RT-015 | FR-004 | Resolution row from a reviewer who is neither the failing reviewer nor a named adjudicator; resolution citing the wrong id; resolution with no reason | Blocked in each case | New |
| RT-016 | FR-004 | Fail, then the content changes and gets a full pass pair, with no resolution row | Blocked | New |
| RT-017 | FR-005 | A pass row citing a reviewer absent from the registry | Row does not count: `REVIEWER_NOT_REGISTERED` | New (P09) |
| RT-018 | FR-005 | A pass row whose reviewer is the entry's recorded author | Row does not count: `REVIEWER_IS_AUTHOR` | New |
| RT-019 | FR-005 | One reviewer id in both required classes | Error, and `release` refuses | Fails (P09b: warning only) |
| RT-020 | FR-005 | A class marked human-required, filled only by reviewers registered as AI | Blocked | Fails (P09) |
| RT-021 | FR-005 | A reviewer qualified for one domain passing a class in another | Row does not count | New |
| RT-022 | FR-006 | Medical entry with one hazard tag; the pair rows list only that topic | Blocked: `MEDICAL_REVIEW_MISSING` | Fails (P36) |
| RT-023 | FR-006 | Entry at `verified` with a reviewer name typed in the entry and no technical-review ledger row | Blocked | Fails (P93) |

## 3. Approvals ledger

| ID | Finding | Given | Must result in | Today |
|---|---|---|---|---|
| RT-030 | FR-004 | ChatGPT approves, ChatGPT withdraws, another role approves later | Blocked | Fails (P10a) |
| RT-031 | FR-004 | ChatGPT approves, SME rejects, owner approves later | Blocked until the rejection is resolved | Fails (P10b) |
| RT-032 | FR-003 | Approval dated 2099-01-01; withdrawal appended afterwards | Blocked | Fails (P11a) |
| RT-033 | FR-003 | Withdrawal appended later, dated one day before the approval | Blocked | Fails (P11b) |
| RT-034 | FR-029 | Approval row with no stored review packet | Blocked: `REVIEW_PACKET_MISSING` | New |
| RT-035 | FR-029 | Stored packet whose digest differs from the entry's current closure digest | `APPROVAL_STALE` | New |
| RT-036 | FR-029 | One character changed in the entry after the packet was generated; a stored pack whose hash no longer matches | Blocked; error | New |
| RT-037 | FR-006 | `release` with no owner authorization row for the exact manifest digest | Refused: `RELEASE_NOT_AUTHORIZED` | New |
| RT-038 | FR-022 | A row deleted, or one cell edited, relative to the last accepted tag | `LEDGER_NOT_APPEND_ONLY` | Fails (P08c) |
| RT-039 | FR-022 | Rows written under an older hash version after a schema change | Reported as needing a migration attestation, distinct from stale | New |

## 4. Classification and hazard policy

| ID | Finding | Given | Must result in | Today |
|---|---|---|---|---|
| RT-040 | FR-001 | Z05 entry typed `general`, no tags, no exemption | Error `ENTRY_TYPE_NOT_ALLOWED_IN_ZONE` | Fails (P18) |
| RT-041 | FR-001 | Z10 entry typed `technical_procedure`, no exemption | Error | Fails (P18b) |
| RT-042 | FR-001 | Every combination of 16 zones and all entry types | Each disallowed pair errors; each allowed pair passes | New |
| RT-043 | FR-001 | Entry citing a claim of type medical, identification, legal or safety_boundary, or of risk critical or high, without the matching hazard class | Error `HAZARD_CLASS_REQUIRED_BY_CLAIM` | Fails (P47) |
| RT-044 | FR-001 | Coverage row lists a hazard topic for the entry; the entry lacks it | Error | Fails (P46) |
| RT-045 | FR-001 | Entry with no hazard class and no hazard-screening row; a screening row written by the author | Blocked at `approved` in both cases | New |
| RT-046 | FR-001 | Exemption not approved by the owner; exemption whose bound hash no longer matches | Does not count | New |
| RT-047 | FR-001 | A hazard tag removed from an approved entry | Error by rule, in addition to hash staleness | New |
| RT-048 | FR-007 | A topic's checklist changes after the reviews were recorded | Reviews stale: `SAFETY_CHECKLIST_CHANGED` | Fails (P60) |
| RT-049 | FR-007 | Water-topic entry with no source meeting the topic's authority criteria; the same for preservation | Error | New |
| RT-050 | FR-007 | Meta-test: each key in the hazard policy file | Has a consumer, and a test that fails when the consumer is removed | New |
| RT-051 | FR-021 | `abort_if`, `verify`, `dangers`, contraindications or thresholds set to `N/A`, `n/a`, `none`, `-`, `—`, `.`, `?`, `TBA`, `not applicable` | Error for each token and field | Fails (P27) |

## 5. Species and images

Gate ids refer to `SPECIES_IDENTIFICATION_STANDARD.md` §14.

| ID | Finding / gate | Given | Must result in | Today |
|---|---|---|---|---|
| RT-060 | FR-012, SIS-G07 | One file hash in two manifest rows | Error | Fails (P13) |
| RT-061 | FR-012, SIS-G08 | One image as evidence for two taxa | Error | Fails (P13b) |
| RT-062 | FR-012, SIS-G04 | A target-view image whose taxon differs from the profile's | Error | Fails (P14) |
| RT-063 | FR-012, SIS-G05 | A plate made only of look-alike and "other" views | Perspective set incomplete | Fails (P15) |
| RT-064 | FR-012, SIS-G02 | Two profiles for one accepted taxon; a synonym that resolves to an existing record | Error | Fails (P32) |
| RT-065 | FR-012, SIS-G13 | Evidence image with no taxon id, locality or observation date | Error | Fails (P92) |
| RT-066 | FR-010 | Image audit with `decision: pass` and any applicable check false | Does not count | Fails (P12) |
| RT-067 | FR-010 | Image audit by an unregistered or unqualified reviewer | Does not count | Fails (P12; role part is OBS-1) |
| RT-068 | FR-010 | After approval, change each of: caption, alt text, subject names, role, perspective, licence, credit, overlay label | Entry approval stale in every case | Fails (P16) |
| RT-069 | FR-010 | After approval and safety review, swap the image file, update the manifest hash, add a new audit | Entry approval and safety reviews stale | Fails (P17) |
| RT-070 | FR-013, SIS-G11 | AI-generated or AI-enhanced image in an evidence role; a generated image with no label and blank subject | Error in both cases | Partly (P34) |
| RT-071 | FR-013, SIS-G10 | Evidence image with no source record and no original-file hash | Error | New (P91) |
| RT-072 | SIS-G09 | Determination basis below the tier minimum, for each code; determiner equal to the photographer | Error | New |
| RT-073 | FR-013 | A scan of artwork in an evidence role | Error | New |
| RT-074 | FR-014, SIS-G13 | Release built from a JPEG carrying EXIF artist and GPS | `pdfimages -all` output holds no EXIF or location data | Fails (P72) |
| RT-075 | FR-014, FR-026 | A derivative not listed against an audited original; an original changed after derivation | Error | New |
| RT-076 | FR-015 | Licence outside the controlled list; a no-derivatives licence when the pipeline crops or overlays; attribution elements missing | Error | Fails (P90) |
| RT-077 | SIS-G06 | Each required perspective removed in turn, per organism group | Error; a permitted gap renders the fixed notice text | New |
| RT-078 | SIS-G16 | Look-alike pair without its table, claims, severity, reciprocity or review; a pair edited after approval | Error; both profiles stale | New |
| RT-079 | SIS-G17 | Tier A profile with an empty look-alike list and no specialist statement | Error | New |
| RT-080 | SIS-G18 | A required character class left blank; a "not diagnostic" mark with no specialist row | Error | New |
| RT-081 | SIS-G20 | An E-DOC position with each of the 15 prohibiting conditions of §12.2 true in turn | Refused; profile renders at E0 with no use text | New |
| RT-082 | SIS-G03 | Profile with no tier; tier lowered without a specialist row | Treated as Tier A; error | New |
| RT-083 | SIS-G22 | Tier A row filled by a reviewer registered as AI; a review past its validity | Blocked | New |
| RT-084 | SIS-G23 | Protected status unverified at the edition date while harvest or use text is present | Error | New |
| RT-085 | SIS-G19, SIS-G21 | Separability label, determination basis, completeness statement and mandatory warnings | Each present in the PDF text layer | New |
| RT-086 | FR-025 | Z08 identification entry not typed `material_profile`; a zone flagged as needing reference specimens with none | Error | New |
| RT-087 | SIS-G01, G14, G15, G24 | Unreconciled name; range with no dated claim; free-text phenology; expired name-source version | Error in each case | New |

## 6. Evidence and traceability

| ID | Finding | Given | Must result in | Today |
|---|---|---|---|---|
| RT-090 | FR-008 | Medical entry with no claims; species profile with no claims | Error at `researched` and above | Fails (P19a, P19b) |
| RT-091 | FR-008 | One item of each safety-bearing field with no claim; a claim whose type does not fit the field | Error | New |
| RT-092 | FR-009 | Claim text or locator changed after verification | Verification stale; dependent approvals stale | Fails (P21) |
| RT-093 | FR-009 | A verified source row edited in place | Error; a new edition needs a new id | Fails (P21) |
| RT-094 | FR-009 | Verified source with no edition or date, no retrieval date, or no content hash | Error | Fails (P49) |
| RT-095 | FR-009 | A claim backed by a `background` source, a rights-rejected source, or an unhashed third-party mirror | Error | Fails (P22a, P22b) |
| RT-096 | FR-009 | A critical-risk claim resting only on a source below the required tier | Error | New |
| RT-097 | FR-009 | Release page | Source legend shows issuer, edition and date | Fails (P73) |
| RT-098 | FR-028 | Meta-test over every schema property | Each has a consumer; `claims.entry_ids` equals the set of entries that cite the claim | Fails (P46, P47) |
| RT-099 | FR-022 | A schema field added to entries that already have approvals | Old rows need a migration attestation; nothing passes silently and nothing is rewritten | New |

## 7. Units, dates and freshness

| ID | Finding | Given | Must result in | Today |
|---|---|---|---|---|
| RT-100 | FR-019 | `1 mi / 2 km`, `1 in / 3 cm`, `2 lb / 1 kg`, `3 ft / 1 m`, `1 gal / 4 L`, `1 qt / 1 L` | Rejected | Fails (P23) |
| RT-101 | FR-019 | A correct fraction, mixed number, range, temperature interval and household measure; an incorrect one of each | Correct accepted, incorrect rejected | Fails (P23: all rejected as unparseable) |
| RT-102 | FR-019 | A number with a unit inside any prose field, outside a structured quantity | Flagged | Fails (P28) |
| RT-103 | FR-019 | A quantity marked minimum whose metric value is below the exact conversion; one marked maximum whose value is above it | Error | New |
| RT-104 | FR-016 | A legal claim past its validity at the configured release date | `release` refused | Fails (P29) |
| RT-105 | FR-016 | Region `anywhere`; an unknown region or season code | Error | Fails (P29) |
| RT-106 | FR-016 | An entry carrying legal or regulatory claims with no as-of date, or one later than the release date | Error | Partly (one tag only) |
| RT-107 | FR-016, FR-017 | Every page of a release PDF | Carries the edition id and as-of date | Fails (P73) |

## 8. Rendering and release

| ID | Finding | Given | Must result in | Today |
|---|---|---|---|---|
| RT-110 | FR-011 | A unique token placed in every content field of every entry type | Every token found in the PDF text layer | Fails (P20) |
| RT-111 | FR-011 | A type-specific field on another entry type | Schema error | Fails (P20) |
| RT-112 | FR-011 | A non-empty body while no body renderer exists | `release` refused | Fails (P20) |
| RT-113 | FR-017 | A release, then a withdrawal, then a refused release | No PDF from the first release remains presented as current | Fails (P25) |
| RT-114 | FR-017 | Release manifest | Lists commit, register and ledger digests, asset hashes, layout, toolchain and font hashes; a rebuild from it is byte-identical | Fails (P20) |
| RT-115 | FR-017 | A zone that loses its last published entry | Its previous PDF is superseded, not left in place | Fails |
| RT-116 | FR-018 | Two entries in one zone citing one source | No duplicate destination; each source link resolves to the page expected | Fails (P26, P94) |
| RT-117 | FR-018 | Synthetic log lines of each warning shape, including `pdfTeX warning (ext4): …` | Each is reported | Fails (P26) |
| RT-118 | FR-020 | Entry with 60 danger lines; species and medical specimen entries | Builds with every line present; every required field rendered | Fails (P70); New |
| RT-119 | FR-023 | Every figure in a release PDF | Has a description reachable by assistive technology, or a printed one | Fails (P20) |
| RT-120 | Controls | Entry text edited after approval; any error anywhere; two builds of one tree; an overflowing panel | Approval stale; release refused; byte-identical; refused, not clipped | Passes; must keep passing |

## 9. Invariants

Property and metamorphic tests. Each generates many random cases; the invariant ids are those of `SAFETY_GATE_THREAT_MODEL.md` §6.

| ID | Invariant | Property |
|---|---|---|
| PT-01 | INV-1 | For any random ledger: if an unresolved non-pass row exists for an entry or an asset it cites, the entry is never eligible. |
| PT-02 | INV-2 | Shuffling the rows of any ledger, keeping their sequence ids, never changes any entry's verdict. |
| PT-03 | INV-2 | Appending a pass row never unblocks an entry blocked by a non-pass. Appending a non-pass row never unblocks anything. |
| PT-04 | INV-3 | Changing any single byte of any file or row in an approved entry's closure produces at least one error for that entry. |
| PT-05 | INV-3 | Changing something outside an entry's closure never makes that entry stale. Over-broad invalidation trains people to bypass the gate. |
| PT-06 | INV-4 | Removing a hazard tag, or changing the entry type, never reduces the set of reviews an entry needs. |
| PT-07 | INV-5 | For every eligible hazardous entry, the reviewers across its required classes are distinct, registered, and none is the author. |
| PT-08 | INV-6 | For random valid entries of each type, the set of approved strings is a subset of the PDF's text. |
| PT-09 | INV-9 | Moving the configured release date forward never turns a refused release into an accepted one. |
| PT-10 | INV-10 | Build, read the manifest, rebuild in a clean directory: identical bytes. Any change to a register yields a different edition id. |
| PT-11 | INV-11 | Corrupting any id in any ledger row yields an error. |
| PT-12 | INV-12 | Every policy key and schema property has a consumer and a test that fails when the consumer is removed. |

## 10. Sabotage checks

RUN-001 and RUN-002 validated their suites by breaking safeguards one at a time. The same is required for these corrections. Each change below, applied alone to a scratch copy, must make at least one test fail.

| # | Sabotage | Restores |
|---|---|---|
| S01 | Ignore non-pass rows that list no tagged topic | FR-002 |
| S02 | Ignore non-pass rows whose revision number differs | FR-002 |
| S03 | Skip the orphan-row check | FR-002 |
| S04 | Order rows by date instead of sequence | FR-003 |
| S05 | Accept dates by pattern only | FR-003 |
| S06 | Let any later pass clear a non-pass | FR-004 |
| S07 | Evaluate approvals as "latest row of any role" | FR-004 |
| S08 | Skip the reviewer registry lookup | FR-005 |
| S09 | Allow the reviewer to be the author | FR-005 |
| S10 | Make the same-reviewer check a warning | FR-005 |
| S11 | Treat hazard tags as declared only | FR-001 |
| S12 | Narrow the closure digest back to entry text | FR-010 |
| S13 | Ignore image-audit check flags | FR-010 |
| S14 | Skip the packet-digest comparison | FR-029 |
| S15 | Skip the render-totality check | FR-011 |
| S16 | Remove the target-taxon match; remove file-hash uniqueness | FR-012 |
| S17 | Accept an E-DOC position with one prohibiting condition true | FR-025 |
| S18 | Skip the append-only check | FR-022 |
| S19 | Remove the freshness gate; leave stale output on refusal | FR-016, FR-017 |
| S20 | Accept null-like tokens; restore the round-trip-only unit rule | FR-021, FR-019 |

## 11. Coverage of the step-4 focus list

| Focus area | Tests |
|---|---|
| Stale approvals | RT-032, RT-033, RT-035, RT-048, RT-092, RT-104, RT-113 |
| Multiple hazard classes | RT-001, RT-002, RT-003, RT-022, RT-043, RT-044 |
| Conflicting review decisions | RT-009, RT-010, RT-013 to RT-016, RT-030, RT-031, PT-01 to PT-03 |
| Missing reviewer roles | RT-017 to RT-023, RT-066, RT-067, RT-083, PT-07 |
| Reused photographs | RT-060, RT-061, RT-064 |
| Incorrect species labels | RT-062, RT-063, RT-065, RT-068, RT-072 |
| Unverified medical procedures | RT-041, RT-043, RT-090, RT-091, RT-110 |
| Incorrect unit conversions | RT-100 to RT-103 |
| Legal restrictions changing over time | RT-011, RT-104 to RT-107 |
| Approved text modified after review | RT-034 to RT-036, RT-068, RT-069, RT-092, RT-093, RT-110, PT-04 |
