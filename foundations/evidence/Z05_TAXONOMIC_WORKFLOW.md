# Z05 Taxonomic and Diagnostic Identification Workflow (P19-A)

A03 adds an [independent name and voucher screen](../audit/a03/TAXONOMIC_VERIFICATION_REGISTER.csv) and expands the [multi-view acquisition register](../visual/DIAGNOSTIC_PHOTOGRAPHY_ACQUISITION_REGISTER.csv). Voucher and media leads remain under qualified review. Every taxon remains on WITHHELD_HOLD.

**Status:** Editorial Draft Pipeline Qualified · **Consumption Status:** `WITHHELD_HOLD` across all 135 Z05 pages · **Qualified Human Approvals:** `0`

## 1. Separation of Recognition and Consumption

- **Recognition** documents morphology, habitat, phenology, and lookalike contrasts strictly for education, hazard avoidance, and museum-style voucher recording.
- **Consumption suitability** is a separate clinical, toxicological, site-contamination, preparation, and individual-allergy decision. No draft text, conceptual SVG diagram, or incomplete photograph in this encyclopedia authorizes eating any wild plant, berry, root, seed, or fungus.
- Every taxonomic profile in [z05-taxonomic-register.tsv](z05-taxonomic-register.tsv) carries `consumption_status = WITHHELD_HOLD` until independent botanist, mycologist, and medical-toxicology reviews complete.

## 2. Separate Botanical (`Plantae`) and Mycological (`Fungi`) Evidence Schemas

| Schema Dimension | Botanical (`Plantae`) Requirement | Mycological (`Fungi`) Requirement |
|---|---|---|
| Nomenclature | Accepted Latin binomial, author, USDA PLANTS & ITIS synonyms | Accepted Latin binomial, author, MyCoPortal & NAMA current taxonomy |
| Regional Voucher | Bell Museum Minnesota Biodiversity Atlas & Herbarium records | Bell Museum Fungarium & MyCoPortal North American vouchers |
| Required Characters | Leaf arrangement/margin/venation, stem/sap, flower/fruit, underground part, phenology | Cap/cuticle, fertile surface (gills/pores/teeth) & attachment, stipe, annulus ring, basal volva, spore print, substrate/host |
| Stop Threshold | Missing flowers/fruit/stem cues or wet-ground Apiaceae umbel -> STOP | Missing intact base/volva, immature button stage, or uncertain spore print -> STOP |
| Emergency Referral | Minnesota Poison Control `1-800-222-1222` / `911` | Minnesota Poison Control `1-800-222-1222` / `911` + retain uneaten pieces in paper bag |

## 3. Image Provenance & Rights Gate

- Zero AI-generated botanical or fungal illustrations are classified as diagnostic photography.
- Every conceptual vector plate carries an explicit `CONCEPTUAL, NOT TO SCALE` header and `HOLD` banner.
- Every open diagnostic photograph need is tracked in [photo-requirements.tsv](photo-requirements.tsv) requiring matched multi-view provider originals, metric scale, locality, license verification, and curator sign-off.
