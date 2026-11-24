# Species and specimen identification standard

| | |
|---|---|
| Review | FABLE-REVIEW-001, step 3 deliverable |
| Applies to | Plants, berries and other fruits, seeds and nuts, mushrooms and other fungi, rocks, minerals and materials (zones Z05, Z08, Z16, and any entry elsewhere that identifies an organism or material) |
| Status | Proposed. Not adopted, not implemented, and not a substitute for specialist judgement. |
| Closes | FR-012, FR-013, FR-014, FR-025, and the species parts of FR-005, FR-008, FR-010 |

## 0. What this document is and is not

This is a verification framework: the evidence a profile needs, who must attest to it, and what the build must refuse. It contains no identification facts about any organism or material, and no field guidance.

Three things here need a qualified specialist before adoption, and are marked **[SME]**:
the character classes in §4, the perspective sets in §5, and the minimum counts in §5.3. They follow ordinary descriptive practice in botany, mycology and mineralogy, but this review is not a specialist determination of what suffices for any group.

"Must" means a machine gate enforces it or a registered reviewer attests to it in a ledger row. Section 14 lists the gates.

## 1. Principles

1. **Evidence, not illustration.** A profile is published only with identification evidence: real photographs of determined specimens, with a recorded chain from capture to page.
2. **AI output is never identification evidence.** No AI-generated, AI-enhanced or AI-identified image or label counts toward any requirement in this standard. This includes generative upscaling, denoising, fill and background replacement, which invent detail.
3. **A source's label is a claim, not a determination.** Every diagnostic image needs a determination recorded in this project by a registered, qualified person, whatever its source says.
4. **Photographs never establish edibility.** An edibility position is a separate, claim-traced record with its own prohibitions (§12).
5. **The default is silence.** With evidence missing, the profile says nothing about use, or is not published. A missing plate is better than a wrong one.
6. **The dangerous neighbour is part of the profile.** A profile is incomplete until its look-alikes are documented to the same standard as the target.
7. **Uncertainty is printed.** What is not known, not photographed or not separable in the field appears on the page, in fixed words.
8. **Classification cannot be lowered by the author.** Risk tier, required reviews and evidence levels are assigned by a specialist and derived by rule (FR-001).

## 2. Record model

The current schema holds a species as free text inside one entry. This standard needs five records. Field names are suggestions; the content is the requirement.

### 2.1 Taxon or material record

One per accepted taxon or material, shared by every entry and image that refers to it.

| Field | Requirement |
|---|---|
| `taxon_id` | Stable project id. Entries and images refer to this, never to a typed name. |
| Kind | plant, fungus, lichen, mineral, rock, other material |
| Accepted scientific name and author citation | Required for organisms. For minerals, the accepted species or variety name; for rocks, the classification name. |
| Name source, with version or access date | The nomenclatural authority used (§9) |
| Synonyms and misapplied names | Each with its source |
| Rank and resolution | Species, subspecies, variety, or "species complex" with the reason it is not resolved further |
| Common names | Each tagged with a region. Never used as an identifier. |
| Risk tier | §3. Assigned by a registered specialist; bound to the record's hash. |
| Organism group | Selects the character classes (§4) and perspective set (§5) |

### 2.2 Specimen or observation record

One per individual organism, collection or hand sample that was photographed.

| Field | Requirement |
|---|---|
| `specimen_id` | Groups the images of one individual |
| Observer or collector, date observed | Required |
| Locality | Recorded at full precision; published precision set separately (§6) |
| Habitat, substrate or host, associated species | Required for organisms. For materials: geological setting and occurrence. |
| Growth stage, or condition for materials | Controlled vocabulary per group (§7) |
| Determination | Who determined it, on what basis (§11.1), and when |
| Voucher | Institution and accession number where one exists |

### 2.3 Image record

Extends the present asset manifest row.

| Field | Requirement |
|---|---|
| `taxon_id`, `specimen_id` | Required for any image in a role of evidence |
| Perspective | Controlled vocabulary per organism group (§5). Replaces the five generic `view` values. |
| Scale reference | Present in frame, or measured size recorded |
| Original file hash and derivative hashes | Lineage from capture file to printed derivative (FR-014, FR-026) |
| Source record | Institution record identifier, or a named photographer's original file with recorded permission |
| Generation attestation | Method, who attested it, and the checks done (§13) |
| Edits applied | Limited to the permitted list in §13.3 |

### 2.4 Look-alike pair record

One per pair of taxa that can be confused. Fields in §8.

### 2.5 Edibility assertion record

One per profile, defaulting to "no information given". Fields and prohibitions in §12.

## 3. Risk tiers

A registered specialist assigns the tier. The author cannot lower it. A lower tier needs a specialist's ledger row with a reason.

| Tier | Assigned when | Effect |
|---|---|---|
| **A** | Any fungus. Any taxon carrying a use by ingestion or on the body. Any taxon with a documented toxic look-alike. Any taxon presented as poisonous for avoidance. | Full evidence set, human specialist review, look-alike matrix complete, default edibility position E0 |
| **B** | Organisms presented for non-ingestion use (cordage, tinder, tool material) with a documented contact, smoke or handling hazard, or a look-alike with one | Full evidence set, specialist review; look-alike matrix for hazardous confusions |
| **C** | Organisms presented for recognition only, with no use and no documented hazardous confusion | Reduced perspective set **[SME]**; specialist determination of images still required |
| **M-H** | Rocks, minerals and materials with a documented hazard in handling, working, heating or use | Full evidence set, hazard fields claim-traced, specialist review |
| **M** | Other rocks, minerals and materials | Reduced set **[SME]**; determination still required |

A profile with no tier is treated as Tier A.

## 4. Required diagnostic characteristics

For each character class listed for its group, the profile must do one of two things:

- state the character, each statement traced to a verified claim (FR-008); or
- carry a specialist's explicit mark that the class is not diagnostic for this taxon.

A class left blank blocks the profile. The lists are **[SME]**.

| Group | Character classes that must be addressed |
|---|---|
| Plants (herbaceous) | Growth habit and size; stem; leaf arrangement, division, shape, margin, venation and surfaces; flower and inflorescence; fruit and seed; underground parts; sap, odour or other non-visual characters; habitat |
| Plants (woody) | The above, plus bark at more than one age; twigs, buds and leaf scars for the leafless season; overall form |
| Berries and other fruits | Fruit type and internal structure in section; arrangement on the plant; colour and surface through the ripening stages; seed number and form; remnant flower parts; and the full plant profile above. A fruit is never documented apart from the plant that bears it. |
| Seeds and nuts | Husk or enclosing structure; shell; kernel; attachment and arrangement; maturity stage; and the full profile of the parent plant |
| Mushrooms and other fungi | Cap; spore-bearing surface and its attachment; stem; ring or other veil remnants; stem base including any part below the surface; flesh, including any colour change on cutting or bruising; odour; spore print colour; substrate or host; growth habit; microscopic or chemical characters where the group needs them |
| Minerals | Lustre; hardness; streak; cleavage and fracture; crystal form and habit; density or heft; diagnostic reactions; colour, recorded as a weak character; occurrence |
| Rocks and materials | Texture and grain; composition visible at hand-sample scale; structure; fracture behaviour; weathered and fresh surfaces; geological setting |

Two further rules apply to every group.

- **Variation is a character.** The record states the documented range of variation, by age, season, region and condition, or states that it is not documented.
- **Characters that need equipment are named as such.** If separation from a look-alike needs a hand lens, a microscope, a reagent or a reference sample, the profile says so, and §11.2 sets the separability label accordingly.

## 5. Required photographic perspectives

### 5.1 General rules

1. Every image used as evidence shows a real specimen of the stated taxon, determined under §11.1.
2. A perspective set is a named list for the organism group. A plate must hold every required perspective for every growth stage it covers (§7).
3. At least one complete set must come from a single individual (`specimen_id`), so the characters are shown to occur together.
4. A scale reference is required for every perspective marked "scale" below.
5. Colour must be judged against a reference where colour is diagnostic: a grey or colour card in frame, or the profile states that colour in the images is not calibrated.
6. Look-alike images are held under the look-alike's own taxon record. They never count toward the target's set.
7. Images print at a size at which the specialist confirms the diagnostic character is legible on the phone and print profiles. The present 3 cm slot (FR-026) is not presumed sufficient.

### 5.2 Perspective sets **[SME]**

| Group | Required perspectives |
|---|---|
| Plants (herbaceous) | Whole plant in habitat (scale); stem with leaf attachment; leaf upper surface; leaf lower surface; flower or inflorescence, close; fruit or seed, close (scale); underground part where the profile refers to it (scale) |
| Plants (woody) | Whole form; bark, young and mature; twig with buds; leaf, both surfaces; flower; fruit (scale) |
| Berries and other fruits | Fruit cluster on the plant; single fruit, exterior (scale); fruit in section showing seeds (scale); plus the plant set |
| Seeds and nuts | In husk on the plant; husk removed (scale); section or kernel (scale); plus the parent plant set |
| Mushrooms and other fungi | In place before collection, showing substrate; cap from above (scale); spore-bearing surface, close; side view of the whole fruit body **including the complete base** (scale); lengthwise section; spore print with its colour reference; young and mature stages where form changes |
| Minerals | Hand sample, fresh surface (scale); weathered surface; streak result; cleavage or fracture surface, close; crystal form where present |
| Rocks and materials | Outcrop or setting; hand sample fresh and weathered (scale); close view of texture; worked or fractured surface where the profile concerns use |

### 5.3 Minimum independent evidence **[SME]**

Proposed defaults for Tier A and M-H:

- at least three capture events of the target taxon, from at least two specimens;
- at least one complete single-specimen set (rule 5.1.3);
- for each look-alike flagged lethal or severe, one complete set of the look-alike.

Two files that are crops, re-exports or edits of one capture are one capture. One file listed twice is one capture (FR-012, probe P13).

## 6. Habitat and geographic evidence

1. Each specimen record carries locality, date, habitat and substrate or host. For materials: geological unit or setting.
2. The profile's range statement is a claim, traced to a dated source that is authoritative for that region.
3. Regions are controlled codes (FR-016, FR-027). The profile's `region` must lie within the documented range, or the profile prints "not documented in this region".
4. A specimen photographed outside the edition's focus region is allowed, and the plate prints where it was photographed. A profile whose evidence is all from outside the focus region carries a fixed notice that regional forms may differ.
5. Locality is published only at an approved precision. For protected, regulated or over-harvested taxa the published precision is no finer than a region. Coordinates are removed from every published file (FR-014).
6. Protected and regulated status is a structured record: jurisdiction, status, source, as-of date. Where collection is prohibited, or the status is not verified as of the edition date, the profile is identification-only and no harvest or use text is rendered.

## 7. Growth stage and seasonal variation

1. Each organism group has a controlled list of stages, for example seedling, vegetative, flowering, fruiting, dormant for plants; button, young, mature, old for fungi; fresh and weathered for materials **[SME]**.
2. Phenology is structured: stage by month, by region code. Free text is not accepted.
3. The profile lists the stages at which a reader would meet or collect the organism. Each such stage needs its perspective set (§5), or the plate prints a fixed gap notice: "No verified image of this stage. Do not identify at this stage from this plate."
4. A stage at which a Tier A look-alike is hardest to separate must be covered for both taxa, or the edibility position is forced to E0 (§12).
5. The observation date of each image must be consistent with the stated phenology for its locality. An inconsistency does not auto-reject; it sends the image to the specialist with the conflict recorded.

## 8. Dangerous look-alike handling

1. Look-alikes are pair records between two `taxon_id` values, not names in prose.

   | Field | Requirement |
   |---|---|
   | Taxa | Both ids. The look-alike need not have a full profile, but it must have a taxon record and a verified image set. |
   | Severity of confusion | lethal, severe, moderate, nuisance. Assigned by the specialist. |
   | Distinguishing characters | A table: character, state in A, state in B, the stage at which it applies, equipment needed. Each row traced to a claim. |
   | Reliability | Whether the pair is separable in the field (§11.2) |
   | Region and stage overlap | Where and when both occur |
   | Review | Specialist row bound to the pair's digest |

2. Pairs are reciprocal. If A lists B, B's profile shows A.
3. A lethal or severe pair is presented on the target's plate, side by side, with the look-alike's own images under its own name, and the distinguishing table.
4. Every Tier A profile prints a coverage statement: which region and date the look-alike review covered, and that other similar species may exist.
5. An empty look-alike list is a specialist's positive statement ("none documented for this region as of this date"), recorded as a ledger row. It is never a default.
6. A new or changed pair record makes the approvals of both profiles stale.

## 9. Scientific-name reconciliation

1. The research owner selects one nomenclatural authority per organism group and pins its version or access date. Candidates in common use include the USDA PLANTS database, the Integrated Taxonomic Information System and World Flora Online for vascular plants; Index Fungorum and MycoBank for fungi; and the International Mineralogical Association's list of minerals. These are candidates to evaluate, not recommendations this review has verified for fitness.
2. Each taxon record stores the accepted name exactly as the authority gives it, with author citation and the authority's identifier where it has one.
3. Every name met in a source, an image record or a pack is mapped to a taxon record through the synonym list. An unmapped name blocks the item that carries it.
4. Where sources disagree on circumscription (one species or several), the record is marked a complex. For a complex, any statement that differs between its members, including toxicity, is prohibited at the complex level.
5. A source that uses an older or different name is cited with the name it used, and the mapping is shown in the source legend.
6. When the authority changes a name, the taxon record is revised, every dependent profile and image goes stale, and the previous name is kept as a synonym. Printed profiles show the previous name for at least one edition.
7. Two profiles for one accepted taxon in one edition are an error (probe P32).

## 10. Expert review requirements

Reviews are ledger rows citing a registered reviewer (FR-005), bound to the closure digest of what was reviewed (FR-010), with no unresolved non-pass decision (FR-002, FR-004).

| Review | Tier A | Tier B, M-H | Tier C, M |
|---|---|---|---|
| Determination of every evidence image (§11.1) | Human specialist in the organism group | Human specialist | Human specialist, or institution voucher record accepted by one |
| Profile review: characters, stages, range, look-alike matrix | Human specialist, not the determiner's only reviewer where two are required below | Human specialist | Technical reviewer |
| Second independent human specialist | Required for fungi, and for any profile whose edibility position is not E0 | Not required | Not required |
| ChatGPT validation: claims, sources, wording, internal consistency | Required | Required | Required |
| Edibility assertion (§12), where not E0 | Both human specialists, plus an owner decision per taxon for fungi | n/a | n/a |

Rules:

1. No reviewer reviews their own photograph, determination or text.
2. A specialist's qualification for the organism group and region is recorded in the registry with an evidence reference. The owner accepts each registration.
3. An AI system may assist a reviewer. It cannot be the reviewer of record for any row in the first three lines of the table.
4. A review covers a named scope. A row that reviews images does not count as a profile review.
5. Reviews carry a validity period set by tier. An expired review blocks release (FR-016).

Tracker gate GG notes that experts must be "available and paid if required". If qualified human reviewers cannot be engaged for a group, the fail-closed outcome under this standard is that Tier A profiles for that group are not published. That is a scope decision for the owner, to be made before S06, not a reason to relax the table.

## 11. Confidence and uncertainty labels

Labels are controlled values. They are printed in fixed words and never paraphrased by the author.

### 11.1 Determination basis, per image

| Code | Meaning | May serve as diagnostic evidence |
|---|---|---|
| D1 | Determined from a preserved voucher held by an institution; the image shows that specimen or the organism it came from | All tiers |
| D2 | Determined by a qualified specialist who examined the physical specimen | All tiers |
| D3 | Determined by a qualified specialist from the complete perspective set alone | Tiers B, C, M-H, M. Tier A only with a second specialist's concurrence, and the plate prints "determined from photographs". |
| D4 | Labelled by the source institution; determiner not recorded | No. Supporting role only, until re-determined to D1–D3. |
| D5 | Labelled by the photographer, uploader or a community platform | No |
| D0 | Undetermined, or labelled by software | No. Quarantined. |

### 11.2 Field separability, per profile and per look-alike pair

| Code | Printed statement |
|---|---|
| S1 | Separable in the field by the characters shown, at the stages shown |
| S2 | Separable only with the additional examination named in this entry |
| S3 | Not reliably separable without specialist examination |
| S0 | Not assessed |

### 11.3 Evidence completeness, per plate

The plate prints which required perspectives and stages are present and which are absent, the number of independent specimens behind it, and the as-of date of the review. Gap notices from §7.3 are part of the plate, not of the caption.

### 11.4 What may not be printed

No profile prints a numeric "confidence score", a percentage, or a rating produced by a model. They suggest a precision the evidence does not have.

## 12. Conditions that prohibit an edibility claim

### 12.1 The three positions

| Code | Meaning |
|---|---|
| E0 | No information about eating is given. The default for every profile. |
| E-TOX | Documented as poisonous or harmful. Presented for avoidance. |
| E-DOC | Documented as eaten, under stated preparation and limits, with sources. Never worded as "safe" or "edible" without those limits, and never as a guarantee (handoff §6). |

The wording for each position is fixed text owned by the research owner. The author supplies the limits and the claims, not the framing.

### 12.2 Prohibitions

An E-DOC position is refused if any one of these holds. Each is a gate or an attested check.

| # | Condition |
|---|---|
| 1 | The taxon is not reconciled (§9), or is a complex whose members differ in documented effects |
| 2 | A look-alike pair of severity lethal or severe lacks a complete, reviewed distinguishing table, or lacks a verified image set of the look-alike |
| 3 | The profile or any lethal or severe pair is labelled S3 or S0. For S2, the named examination is not itself a documented, claim-traced step. |
| 4 | Fewer than two independent authoritative sources support the statement, or any authoritative source reports toxicity, adverse reactions, or regional or seasonal variation in effects that the entry does not carry |
| 5 | Edibility depends on plant part, growth stage, preparation or quantity, and any of those lacks claim-traced specifics in the entry |
| 6 | No complete, determined perspective set exists for the stage at which the organism would be collected |
| 7 | The taxon is not documented as occurring in the stated region |
| 8 | Protected or regulated status prohibits collection in the stated jurisdiction, or has not been verified as of the edition date |
| 9 | A required review (§10) is missing, expired, or has an unresolved non-pass decision |
| 10 | Any diagnostic image is below the tier's minimum determination basis, or has an unresolved image audit |
| 11 | Sources document risks for particular groups of people, or interactions, and the entry does not state them |
| 12 | The identification rests on a single photograph, an AI system, an identification app, or a crowd identification without specialist determination |
| 13 | The entry, or any claim it cites, presents a general-purpose test or rule of thumb as establishing that something can be eaten |
| 14 | For fungi: no owner decision is recorded for this taxon, in addition to every condition above |
| 15 | The mandatory warnings (positive identification, uncertainty, processing restrictions) are not present in the rendered page (FR-011) |

When E-DOC is refused, the profile reverts to E0 and renders no use text. It does not render a weakened claim.

An E-TOX position needs conditions 1, 4 (one authoritative source suffices), 9 and 10. Absence of an E-TOX statement is never to be read as safety, and the plate says so in fixed words.

## 13. Rejection of fabricated or mislabelled images

### 13.1 What an evidence image must have

1. **A source record.** Either an institution's record identifier for the image or specimen, or the original capture file from a named photographer with recorded permission.
2. **The original, retained.** The hash of the unmodified file is recorded. Published derivatives trace to it.
3. **Capture evidence.** Capture metadata consistent with the stated date and place, or an institutional record that supplies them. Metadata is evidence for the audit and is stripped from what is published.
4. **A generation attestation.** The image auditor records the method (camera photograph, scan of a photograph, scan of artwork, drawn, rendered, AI-generated, AI-enhanced), who attests it, and what was checked.
5. **A determination** under §11.1, by someone other than the photographer.
6. **A licence** from the controlled list, permitting the derivatives the layout makes (FR-015).

### 13.2 Automatic rejection as evidence

An image is quarantined, with the reason recorded, if any of these holds.

| # | Trigger |
|---|---|
| 1 | No source record and no original file |
| 2 | The only provenance is a search result, an aggregator, a social platform, a stock library without a capture record, or any AI image service |
| 3 | Attested or found to be AI-generated or AI-enhanced, in whole or in part |
| 4 | The same or a near-duplicate image exists elsewhere under a different taxon name, or in this manifest under a different `taxon_id` (probe P13b) |
| 5 | The file hash already exists in the manifest (probe P13) |
| 6 | Capture date, place or season conflicts with the specimen record, and the specialist does not resolve it |
| 7 | Edits beyond §13.3, including compositing, retouching, mirroring, generative fill, or removal of a watermark or label |
| 8 | The source's label and the project determination disagree and the conflict is not resolved by a D1 or D2 determination |
| 9 | A scan of artwork, a field-guide plate or any printed publication is offered as a photograph |
| 10 | The image's taxon differs from the profile it is cited in as a target view (probe P14) |

Detection software for AI imagery is fallible in both directions. A detector result is recorded as one input; it never clears an image that lacks a provenance chain, and never condemns one that has a complete chain without a human decision.

### 13.3 Permitted edits to a published derivative

Crop, resize, rotation by right angles, uniform exposure and white-balance adjustment, conversion to the output colour space, and metadata removal. Each derivative records its recipe. Nothing else.

### 13.4 Reuse

1. One image is evidence for exactly one taxon.
2. It may appear in another profile only as a look-alike view, by reference to its own taxon record, so the printed name is always its own.
3. One image may be cited by several entries about the same taxon. Its caption, credit and labels come from the image record and cannot vary by entry.
4. Changing any printed or evidentiary field of an image record makes every citing entry's approval stale (FR-010).

### 13.5 Illustrations

1. A drawing or diagram may explain a term or a structure. It carries the label `ILLUSTRATION — NOT FOR SPECIES IDENTIFICATION`, whether or not a subject is recorded (probe P34), and never counts toward any requirement.
2. An AI-generated depiction of an organism or mineral specimen never serves as identification evidence.
3. **Recommended, stricter than the handoff, for the owner to decide:** no AI-generated depiction of an organism or specimen appears on a Tier A or M-H plate at all, labelled or not. A label lives in the layout. Images are cropped and screenshotted out of PDFs and travel without it.

### 13.6 Quarantine

Rejected items stay in `assets/rejected_unverified/` with the reason and the reviewer. They are never deleted, since the record is what stops the same image being proposed again, and never rendered.

## 14. Machine gates

Each gate needs a passing fixture and a failing fixture (`REQUIRED_REGRESSION_TESTS.md` §5).

| Gate | Refuses when |
|---|---|
| SIS-G01 | A profile has no reconciled taxon record (§2.1, §9) |
| SIS-G02 | Two profiles in one edition share an accepted taxon, or a synonym resolves to a second record |
| SIS-G03 | No risk tier assigned by a registered specialist, or the tier was lowered without a specialist row |
| SIS-G04 | A target-view image cites a different `taxon_id` than the profile |
| SIS-G05 | A look-alike view lacks a pair record or the look-alike's own taxon id, or is counted toward the target set |
| SIS-G06 | A required perspective is missing for a covered stage and no permitted gap notice applies |
| SIS-G07 | The independent-capture minimum is not met; a file hash repeats in the manifest; near-duplicates are unresolved |
| SIS-G08 | One image is evidence for two taxa |
| SIS-G09 | A diagnostic image has no determination, a basis below the tier minimum, or a determiner who is the photographer or author |
| SIS-G10 | The provenance chain is incomplete, the original hash is absent, or a derivative has no lineage |
| SIS-G11 | The generation attestation is missing; an AI-generated or AI-enhanced image is in an evidence role |
| SIS-G12 | A perspective that requires scale has none |
| SIS-G13 | Locality, date or habitat is missing from a specimen record; a published file carries location metadata; published precision is finer than approved |
| SIS-G14 | The range statement has no dated authoritative claim, a region code is unknown, or the profile's region lies outside the documented range without the notice |
| SIS-G15 | Phenology is not structured. An image date that conflicts with it is unresolved. |
| SIS-G16 | A look-alike pair lacks its distinguishing table, claims, severity, reciprocity or review |
| SIS-G17 | A Tier A profile has no look-alike coverage statement, or an empty list without the specialist's positive statement |
| SIS-G18 | A required character class is neither documented with claims nor marked not diagnostic by a specialist |
| SIS-G19 | Separability, determination-basis or completeness labels are missing or not rendered |
| SIS-G20 | The edibility record is missing, or is E-DOC while any §12.2 condition holds |
| SIS-G21 | A mandatory warning or any approved field is absent from the rendered page |
| SIS-G22 | A required review (§10) is missing, out of scope, expired, by an unregistered or non-human reviewer where a human is required, or has an unresolved non-pass |
| SIS-G23 | Protected status is unstructured or unverified as of the edition, and harvest or use text is present |
| SIS-G24 | The name source version, range source, legal status or any review is outside its validity at the release date |

## 15. Behaviour when evidence is incomplete

| Situation | Outcome |
|---|---|
| Any SIS gate fails for a Tier A, B or M-H profile | The profile is not published. The coverage report lists it as omitted, with the reason. |
| A permitted gap (a stage with no verified image) | Published with the fixed gap notice on the plate |
| The edibility conditions fail | Published as identification-only at E0, with no use text, if every other gate passes |
| A look-alike has no verified image set | The target profile is not published at Tier A |
| A correction arrives after publication | The profile's approvals go stale, the next edition omits or corrects it, and the errata ledger names the affected editions (FR-017) |

The build never substitutes a placeholder, a generated image or softened wording for missing evidence.

## 16. Decisions this standard needs

| # | Decision | Who |
|---|---|---|
| 1 | Nomenclatural authority per organism group, and its pinned version | GPT, confirmed by SME |
| 2 | Character classes (§4), perspective sets (§5.2) and minimum counts (§5.3) | SME per group |
| 3 | Who qualifies as a specialist for each group and region, and how that is evidenced | OWNER |
| 4 | Whether two human specialists are required for fungi and for every E-DOC position (§10) | OWNER |
| 5 | Whether fungi default to E0 with a per-taxon owner decision (§12.2 condition 14) | OWNER |
| 6 | Whether AI-generated depictions are barred from Tier A plates entirely (§13.5) | OWNER |
| 7 | Published locality precision, and the list of taxa that need the coarsest level | SME + OWNER |
| 8 | Validity periods for reviews, range sources and legal status | GPT |
| 9 | Fixed wording for E0, E-TOX, E-DOC, gap notices and separability statements | GPT |
| 10 | Scope if qualified reviewers cannot be engaged for a group | OWNER, before S06 |
