# AH1 and EH1 primary-table audit

Both imported rank-six models pass a fresh comparison against their actual primary fusion tables. No candidate modular-data identification is used.

- **R6_6_1764 (AH1):** Grossman–Snyder, arXiv:1202.4396v2, Table 1, printed page27. The six-object even part exists by the Asaeda–Haagerup subfactor construction; the source's introductory discussion identifies the category. I rendered the primary table and independently transcribed its fifteen upper-triangular nonunit products, expanding its abbreviation Lambda. This reproduces every one of the216 constructor coefficients and matches the census under the permutation recorded in the receipt. The table's order differs from the associated data-file order described below it; the audit uses the table headings explicitly.
- **R6_7_2274 (EH1):** Grossman–Morrison–Penneys–Peters–Snyder, arXiv:1810.06076, Section2.1, printed page5. This is an actual even part of the Extended Haagerup subfactor constructed by Bigelow–Morrison–Peters–Snyder, arXiv:0909.4099. I independently transcribed its fifteen nonunit products from the rendered table, in order(1,f2,f4,f6,P',Q'), then compared all216 entries and the complete census association. The project constructor uses dimension order(1,f2,f4,Q',f6,P'); the exact permutation is checked. Both constructions are unitary.

The audit-only `verify_rank6_ah_eh_primary.py` constructs both primary tables before importing the project constructors or loading the census. It checks all1296 associativity equations for each table, enumerates every unit-fixing permutation, and binds the downloaded primary PDFs and its own code by SHA256. Normal Python and optimized Python both pass; all conditions are explicit and survive disabled assertions. See `rank6-ah-eh-primary-receipt.json`.

One minor documentation correction is needed: `supplements/rank6/software/residual_models.py` calls EH1 the principal even part. The cited GMPPS convention calls EH1 the **dual** even half and EH2 the principal half. The category name, fusion tensor and classification are unaffected. This should be corrected with the later publication overlay.

Scope: this directly checks the source-table-to-constructor-to-census chain. It does not claim to reconstruct the original subfactor planar algebra or reprove the external existence theorems. Those are explicit primary mathematical inputs, not inferred from the table satisfying ring axioms. No repository or online content was edited.

Sources: <https://arxiv.org/pdf/1202.4396>, <https://arxiv.org/pdf/1810.06076>, <https://arxiv.org/pdf/0909.4099>. The secondary matrix presentation in <https://arxiv.org/pdf/2210.13936> was inspected for reference identity but is not needed for the independent table reconstruction.
