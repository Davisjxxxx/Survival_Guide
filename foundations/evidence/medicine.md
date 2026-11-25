# Medicine evidence pack (`medicine`, M01–M30)

The A02 [claim audit](../audit/a02/CLAIM_SUPPORT_AUDIT.csv) links exact sections, conditions, exclusions and specialist dependencies. The [technical findings](../audit/a02/TECHNICAL_FINDINGS.csv) record the changes made after P12–P15.

Grounds Zone `Z10` (Wilderness Medicine — 80 pages) in current authoritative lay-responder clinical and emergency-response guidance from the American College of Surgeons (STOP THE BLEED), American Red Cross, NIH/MedlinePlus, National Capital Poison Center, CDC, and Wilderness Medical Society (2024 frostbite update).

- **Scope boundary:** Explicitly separates layperson immediate actions, 911/Poison Control dispatcher-guided actions, and qualified clinical/EMS interventions.
- **Hard-stop exclusions:** Never presents lay medication dosage prescriptions, invasive field surgery (cutting/sucking snakebites, improvised airways), fracture reduction, or snow-rubbing frostbite as field procedures.
- **Specialist hold:** All 80 Z10 pages inherit `publication: HOLD` and require qualified wilderness medicine, EMS/trauma, toxicology, and infectious-disease review (`SPECIALIST_REVIEW_REGISTER.csv` H11 and P12–P15 additions).
