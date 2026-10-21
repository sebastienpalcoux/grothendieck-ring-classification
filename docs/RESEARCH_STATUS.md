# Research status and verification

The rank-eight multiplicity-three continuation addresses all 3,527 supplied exact-multiplicity-three rings: 3,506 general exclusions, 15 models and 6 unresolved cases. Every recorded model admits a unitary realization. The remaining rings retain unresolved status for general complex categorification.

The rank-seven multiplicity-five continuation addresses all 5,805 supplied exact-multiplicity-five rings: 5,804 general exclusions, 1 realization and 0 unresolved cases. The classification of the supplied census is complete through multiplicity 5. The new realization R7_5_5678 is Rep(AGL(1,7)).

> **AI-generated research · independent verification pending.** Treat these
> results, proofs, code and data with caution. They have not yet been
> independently verified by human experts or formalized in Lean. Automated
> checks establish only their stated computational scope.

The [public atlas](https://sebastienpalcoux.github.io/grothendieck-ring-classification/)
connects the current manuscripts, fusion rules, classification tables and
reproducible evidence. Publication makes the material accessible; it does not
confer mathematical validation.

## Current classification

The [historical 38-case continuation](../docs/RESEARCH_STATUS.md) records **36 decisions among 38 cases**: 29 proposed general exclusions and 7 unitary constructions. Within that historical 38-case study, two questions remain open: `R6_4_155` and `R6_8_1660`. The combined residual program records 140 decisions (120 exclusions and 20 constructions), all subject to independent mathematical verification.

[All 38 cases and current proof references](CASE_INVENTORY.md).

Rank six records **25,362 exclusions, 57 realizations and
2 open cases** through multiplicity nine. Its complete contiguous
range ends at three; exact bands 1, 2, 3, 5, 6, 7, 9 are complete. Rank seven records
**9,976 exclusions and 30 realizations**,
with **0 open cases through multiplicity 5**; complete through multiplicity 5. Rank eight records
**4402 exclusions and 92 realizations**,
with **6 open cases through multiplicity 3**; complete through multiplicity 2. The historical general exclusion of
`R8_2_24` uses an inner-square obstruction from short gauge weights and
tensor-functor rigidity.

### Rank-six open rings

| Open ring | Established necessary restrictions | Remaining question |
|---|---|---|
| `R6_4_155` | A unique rank-26 modular candidate and a rank-22 based module; odd cyclic Clifford constraints pass on all 1,144 tested blocks, and the all-order path divisibility condition holds. | Coherent associators and module-category structures, or a general obstruction. |
| `R6_8_1660` | In the positive spherical representative, all indicator sequences and central phase masses are determined; eight spin objects form four dual pairs, and 640 labelled restriction-data profiles remain in branches 68, 286, 286. | A categorification or an obstruction covering every possible profile. |

### Rank-seven classification frontier

Every supplied rank-seven fusion ring through multiplicity five has a recorded general exclusion or unitary model. The [continuation evidence](../evidence/rank7_m5_20261020/README.md) gives the accepted arguments and replay receipts. [Download all 8 current open tensors](../data/remaining_cases.py), including the two rank-six cases.

A necessary-condition witness is neither a categorification nor a general
nonexistence proof. Scoped unitary, pseudo-unitary, pivotal or braided
obstructions retain their assumptions and do not change a general open status.

## Reading the labels

| Label | Meaning within this project |
|---|---|
| **Realized** | A categorical construction is recorded, subject to mathematical review. |
| **Excluded** | An obstruction is recorded under its stated assumptions. |
| **Complete** | Each ring in the specified band has a recorded realization or general exclusion. |
| **Unresolved** | Neither a general exclusion nor a categorification is established. |
| **Certified**, **verified**, **PASS** | The stated program checks passed; read their scope and hypotheses. |

Reports described as independent audits are separate AI review passes unless
an explicitly identified human review says otherwise. They are not independent
human verification. Hashes establish source identity; they do not prove the
mathematics. Successful computation does not validate the categorical reduction
making that computation relevant.

Read the [verification scope](PREPUBLICATION_REVIEW.md), [replay guide](VERIFY.md)
and [provenance](PROVENANCE.md) together with the
[manuscripts](../manuscripts/README.md). A [repository issue](https://github.com/sebastienpalcoux/grothendieck-ring-classification/issues)
identifying the ring, theorem and exact failing step makes a reported gap actionable.

## Current rank-eight replay status

Canonical normal and optimized frontier replays each passed all 108 checks. These receipts cover the historical frontier stage. Fresh replay after extraction from the publication archive is deferred.

## Generalized Haagerup construction and further restrictions

R8_3_721 is realized by the inherited 1+rho Q-system Morita dual of the C2 de-equivariantization of the known GH(C8) category. Its rank and coefficient bound are proved exactly; identification uses its unique dimension type in the supplied complete rank-eight multiplicity-at-most-three census. The earlier center-action analysis reduces R8_3_1154 to three necessary center patterns. These model and pattern results are preserved in evidence/rank8_next_20261021/; the later R8_3_65 general exclusion is recorded separately in evidence/rank8_research_20261022/.

The integrated rank-eight article includes the new construction and restrictions. Categorical arguments, targeted mathematical replay receipts and independent reconstructions are in `evidence/rank8_next_20261021/`. The original frontier ledger, audit and completed replay receipts remain unchanged.

The following commands validate the accepted overlay metadata; they do not repeat the targeted mathematical checks:

```bash
python3 tools/rank8_next.py --check
python3 -O tools/rank8_next.py --check
```

A separately reviewed Galois follow-up reduces the 36 retained R8_3_1154 pair histograms to 25 across the same three center patterns. Its proof and exact replay are in `evidence/rank8_postpublication_20261021/r1154_galois_review/`; the ring remains unresolved.

## 22 October rank-eight research

R8_3_65 and R8_3_1795 have general-complex exclusions from pointed-induction Fourier integrality. Six exact separating certificates cover all four pointed associator classes for R8_3_65; sixteen cover both pointed classes and every admissible second-indicator assignment for R8_3_1795. The verified Galois reductions remove the pseudo-unitarity hypotheses. Every hypothetical categorification of each of the 6 remaining rank-eight rings admits a spherical structure and is Galois conjugate to a pseudo-unitary category. None is categorically Morita equivalent to a braided fusion category. For R8_3_1768 the pointed C2 associator must be nontrivial, forcing its nonidentity invertible to act freely on the simple objects of every indecomposable module category. R8_3_982 has a complete necessary based-module analysis; its remaining module data do not establish coherent module categories. A separate dimension-spectrum restriction for R8_3_3472 covers one specified rank-two module action only. These restrictions leave 6 general categorification questions unresolved.

The proof and exact verifier inventory is `evidence/rank8_research_20261022/README.md`. The current research stage has its own accepted ledger and source manifest; its exact replay is:

```bash
python3 tools/verify_rank8_research_20261022.py
python3 -O tools/verify_rank8_research_20261022.py
```

Run `python3 tools/rank8_research_20261022.py --check` for metadata reconciliation only. The original M3 replay and 108-check frontier receipts retain their historical scope. They do not replace the new targeted mathematical checks.
