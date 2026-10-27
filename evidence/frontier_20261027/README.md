# Three exclusions and seven unresolved rings

**27 October 2026.** R9_2_1607, R9_2_1975 and R9_2_1976 are excluded from
fusion categorification over the complex numbers. A fresh separate audit
retains all three arguments. No further census model or exclusion was obtained.

The rank-nine exact-multiplicity-two partition is **2,046 excluded, 36 modeled
and 1 unresolved among 2,083 rings**. Through multiplicity two, rank nine has
2,148 exclusions, 76 models and 1 unresolved among 2,225 rings. The project now
has **seven unresolved cases**. Census data and all earlier accepted decisions
are preserved. These are AI-generated research claims; independent human
verification and formalization remain pending.

| Ring | Current result | Status |
|---|---|---|
| R6_4_155 | Forced nonpointed algebra and complete small-support reduction; its module returns to the known pointed route. | Unresolved |
| R6_8_1660 | Two module realizations and one center subcase excluded. Any connected separable algebra 1+X in its pseudo-unitary form would produce R941. | Unresolved |
| R8_3_928 | Simple modular centralizer; exactly one nontrivial connected etale algebra there. No rank-six Morita partner. | Unresolved |
| R8_3_941 | Nonsplit, s-simple rank-22 fermion centralizer; conditional R1660 algebra construction. | Unresolved |
| R8_3_1154 | All six noninvertible third rotations are identity; integral center Vec; specified construction families excluded. | Unresolved |
| R8_3_1768 | Every GH(C6,2) Morita construction is ruled out, for any associator and any algebra. | Unresolved |
| R9_2_137 | Forced algebra returns to the central-involution module; both TY signs pass the strengthened exact constraints. | Unresolved |

## Proofs and source identities

- [R1975 general exclusion](../unresolved10_20261027/r9_noncommutative/GALOIS_PARITY_EXCLUSION.md)
  and [fresh audit](../unresolved7_20261027/audit_parity/AUDIT_R1975.md).
- [R1607 and R1976 general exclusions](../unresolved10_20261027/r9_commutative/GALOIS_FS2_EXCLUSION.md)
  and [fresh pairing audit](../unresolved7_20261027/audit_fs2/AUDIT.md).
- [Precise R1660–R941 construction implication](MORITA_R1660_R941.md).
- [All seven individual investigations](../unresolved7_20261027/RESEARCH_REPORT.md).
- [Accepted transitions and proof hashes](accepted.json) and
  [current exact-M2 rank-nine ledger](rank9_m2_ledger.json).
- [PDF report](../../site/dist/papers/prepublication-review-2026-10-27.pdf) and
  [frozen proofs and certificates](../../site/dist/downloads/Seven-Fusion-Rings-Proofs-and-Checks.zip).

## Exact replay

From the repository root:

```bash
python3 tools/replay_frontier_20261027.py
python3 tools/verify_frontier_20261027.py --metadata-only
```

The replay adapter checks the immutable archive, extracts its complete source
context into a temporary directory, compares all ten source tensor identities
with the current case records, and runs the exclusion-specific and continuation
checks there. The archived `data/current_remaining_cases.py` intentionally has
ten cases: it is the proof-input snapshot before three decisions. The current
download has seven. Their common tensors agree exactly. Do not substitute the
current seven-case file for the frozen proof input.

Each short verifier certifies its explicitly stated finite claim. The
categorical lemmas and the inherited spherical/Galois reductions are separate
mathematical premises in the proofs. Necessary center witnesses, based modules,
precursor categories and route exclusions are not census-ring models or
general nonexistence proofs. In particular, R1768 is still unresolved.

The original classification source is commit
`6a426acf6465dd674351be92dcca41b72f371521`. Earlier receipts are unchanged;
current display replacements have an explicit before/after record in
`publication_replacements.json`.
