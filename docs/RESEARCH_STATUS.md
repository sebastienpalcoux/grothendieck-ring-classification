# Research status and verification

The rank-eight multiplicity-three continuation addresses all 3,527 supplied exact-multiplicity-three rings: 3,504 general exclusions, 14 models and 9 unresolved cases. Every recorded model admits a unitary realization. The remaining rings retain unresolved status for general complex categorification.

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
**4400 exclusions and 91 realizations**,
with **9 open cases through multiplicity 3**; complete through multiplicity 2. The historical general exclusion of
`R8_2_24` uses an inner-square obstruction from short gauge weights and
tensor-functor rigidity.

### Rank-six open rings

| Open ring | Established necessary restrictions | Remaining question |
|---|---|---|
| `R6_4_155` | A unique rank-26 modular candidate and a rank-22 based module; odd cyclic Clifford constraints pass on all 1,144 tested blocks, and the all-order path divisibility condition holds. | Coherent associators and module-category structures, or a general obstruction. |
| `R6_8_1660` | In the positive spherical representative, all indicator sequences and central phase masses are determined; eight spin objects form four dual pairs, and 640 labelled restriction-data profiles remain in branches 68, 286, 286. | A categorification or an obstruction covering every possible profile. |

### Rank-seven classification frontier

Every supplied rank-seven fusion ring through multiplicity five has a recorded general exclusion or unitary model. The [continuation evidence](../evidence/rank7_m5_20261020/README.md) gives the accepted arguments and replay receipts. [Download all 11 current open tensors](../data/remaining_cases.py), including the two rank-six cases.

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

Canonical normal and optimized frontier replays each passed all 108 checks. Fresh replay after extraction from the publication archive is deferred.

## Further center-pattern constraints

A separately verified fourth-moment and center-action refinement excludes 2 of the four necessary center patterns for R8_3_721, leaving 2. For R8_3_1154, exact coordinate norm and interval bounds exclude 946 of 1,238 patterns, leaving 292. The surviving action matrices and patterns are necessary data only; no complete center fusion ring, associator or categorical model is constructed. Both source rings remain unresolved.

The integrated rank-eight article includes this separately verified addendum. Its proofs, complete pattern indices, necessary action matrices and independent reconstructions are in `evidence/rank8_center_followup_20261021/`. The original frontier ledger and audit remain unchanged.

The separate center-pattern addendum passed all eight checks in canonical normal and optimized Python, including independent arithmetic reconstructions and positive controls. Fresh replay after extraction from the publication archive is deferred.

```bash
python3 evidence/rank8_center_followup_20261021/verify.py --root .
python3 -O evidence/rank8_center_followup_20261021/verify.py --root .
```
