# Research status and verification

The rank-eight multiplicity-three continuation addresses all 3,527 supplied exact-multiplicity-three rings: 3,507 general exclusions, 16 models and 4 unresolved cases. Every recorded model admits a unitary realization. The remaining rings retain unresolved status for general complex categorification.

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

The [historical 38-case continuation](../docs/RESEARCH_STATUS.md) records **36 decisions among 38 cases**: 29 proposed general exclusions and 7 unitary constructions. Within that historical 38-case study, two questions remain open: `R6_4_155` and `R6_8_1660`. The historical residual program before the rank-eight M3 extensions records 140 decisions (120 exclusions and 20 constructions), all subject to independent mathematical verification.

[All 38 cases and current proof references](CASE_INVENTORY.md).

Rank six records **25,362 exclusions, 57 realizations and
2 open cases** through multiplicity nine. Its complete contiguous
range ends at three; exact bands 1, 2, 3, 5, 6, 7, 9 are complete. Rank seven records
**9,976 exclusions and 30 realizations**,
with **0 open cases through multiplicity 5**; complete through multiplicity 5. Rank eight records
**4403 exclusions and 93 realizations**,
with **4 open cases through multiplicity 3**; complete through multiplicity 2. The historical general exclusion of
`R8_2_24` uses an inner-square obstruction from short gauge weights and
tensor-functor rigidity.

### Rank-six open rings

| Open ring | Established necessary restrictions | Remaining question |
|---|---|---|
| `R6_4_155` | A unique rank-26 modular candidate and a rank-22 based module; odd cyclic Clifford constraints pass on all 1,144 tested blocks, and the all-order path divisibility condition holds. | Coherent associators and module-category structures, or a general obstruction. |
| `R6_8_1660` | In the positive spherical representative, all indicator sequences and central phase masses are determined; eight spin objects form four dual pairs, and 640 labelled restriction-data profiles remain in branches 68, 286, 286. | A categorification or an obstruction covering every possible profile. |

### Rank-seven classification frontier

Every supplied rank-seven fusion ring through multiplicity five has a recorded general exclusion or unitary model. The [continuation evidence](../evidence/rank7_m5_20261020/README.md) gives the accepted arguments and replay receipts. [Download all 6 current open tensors](../data/remaining_cases.py), including the two rank-six cases.

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

R8_3_721 is realized by the inherited 1+rho Q-system Morita dual of the C2 de-equivariantization of GH(C8). Exact rank and coefficient bounds identify its unique dimension type in the supplied complete rank-eight multiplicity-at-most-three census. The earlier center-action analysis leaves three necessary R8_3_1154 patterns. These results are in evidence/rank8_next_20261021/; the later R8_3_65 general exclusion is in evidence/rank8_research_20261022/.

The integrated rank-eight article includes the new construction and restrictions. Categorical arguments, targeted mathematical replay receipts and independent reconstructions are in `evidence/rank8_next_20261021/`. The original frontier ledger, audit and completed replay receipts remain unchanged.

The following commands validate the accepted overlay metadata; they do not repeat the targeted mathematical checks:

```bash
python3 tools/rank8_next.py --check
python3 -O tools/rank8_next.py --check
```

A separately reviewed Galois follow-up reduces the 36 retained R8_3_1154 pair histograms to 25 across the same three center patterns. Its proof and exact replay are in `evidence/rank8_postpublication_20261021/r1154_galois_review/`; the ring remains unresolved.

## General exclusion of R8_3_3472

R8_3_3472 admits no fusion categorification over the complex numbers. The sphericalization and Galois reduction covers general complex categories; complete center-frame and twist-orbit domains reduce the remaining case to 628 exact equations in 572 integer variables. A certificate of 1648 rational bound deductions and a final strictly positive separating gap proves infeasibility, with two independent exact checkers. The proof and reproducible certificate are in evidence/r3472_exclusion_20261022/. This complete obstruction supersedes the earlier feasible necessary systems and conditional Morita restrictions for R3472. R8_3_982 remains unitarily realized by the neutral triality component of the exceptional E21 chiral fusion category, with all 512 canonical fusion coefficients identified exactly. Four rank-eight general categorification questions remain: R8_3_928, R8_3_941, R8_3_1154 and R8_3_1768. Every hypothetical categorification of these four rings admits a spherical structure and has a pseudo-unitary Galois conjugate; none has a braided Morita representative. The R928 phase refinement leaves four of ten necessary center patterns, all fourteen R941 allocations survive the stated refinements, and R1154 retains its forced semionic data. R1768 has 39 of 40 necessary Gram/indicator branches excluded, while its final cone survives. These necessary data do not construct categories or settle the four remaining questions.

The complete center-domain reduction and exact infeasibility certificates are in `evidence/r3472_exclusion_20261022/README.md`. This accepted decision removes R8_3_3472 from the unresolved ledger. The earlier E21 construction and its research receipts retain their historical scope.

```bash
python3 tools/verify_rank8_exclusion_20261022.py
python3 -O tools/verify_rank8_exclusion_20261022.py
```

Use `--metadata-only` to check source identities and completed replay receipts. Use `--historical` to replay the preceding rank-eight stages in their preserved contexts. That replay explicitly records the reconstructed helper missing from the creative archive and its four revised cache-state diagnostics in a separate checkpoint; it also restores the omitted canonical tensor with its original receipt hash. The current ledger and proof have separate bindings from those historical releases.
