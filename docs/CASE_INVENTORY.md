# Historical 38-case study and current proof references

<!-- current-research-continuation -->
**Current results · 24 October 2026.** Rank-nine exact multiplicity two has
2,043 general exclusions, 36 unitary models and four unresolved rings.
R8_3_436 is generally excluded by an independent spherical-equivariantization
proof; the old TPE completeness premise remains withdrawn. The project has
11 open cases. [Proofs, precise scope and replay](https://github.com/sebastienpalcoux/grothendieck-ring-classification/blob/main/evidence/research_20261024/README.md).
<!-- /current-research-continuation -->

The rank-eight multiplicity-three continuation addresses all 3,527 supplied exact-multiplicity-three rings: 3,507 general exclusions, 16 models and 4 unresolved cases. Every recorded model admits a unitary realization. The four remaining rings retain unresolved status for general complex categorification. R8_3_436 has an independent general exclusion.

The rank-seven multiplicity-five continuation addresses all 5,805 supplied exact-multiplicity-five rings: 5,804 general exclusions, 1 realization and 0 unresolved cases. The classification of the supplied census is complete through multiplicity 5. The new realization R7_5_5678 is Rep(AGL(1,7)).

> **AI-generated research · independent verification pending.** Treat these
> results, proofs, code and data with caution. They have not yet been
> independently verified by human experts or formalized in Lean. Automated
> checks establish only their stated computational scope.

**36 accepted decisions: 29 proposed general exclusions and seven unitary
constructions. Two general questions remain open.** This inventory covers
these 38 cases; it is not a count of every ring in the full census.

A general exclusion concerns arbitrary complex fusion categories, without an
initial pivotality, sphericality or unitarity assumption. A unitary construction
establishes at least one realization, not uniqueness or unitarity of every
realization. Necessary-condition witnesses do not settle a general question.
All accepted arguments remain subject to independent mathematical verification.

Read the [rank-six manuscript](../manuscripts/rank6/papers/manuscript.pdf),
[rank-seven manuscript](../manuscripts/rank7/papers/manuscript.pdf) and
[rank-eight manuscript](../manuscripts/rank8/paper/rank8.pdf).
The source links below identify the current integrated proof or open-case
section; the stable LaTeX label locates the exact statement in that source.

## Two open cases within the historical study

| Case | Current status and remaining task | Current manuscript section |
|---|---|---|
| `R6_4_155` | **Open.** Odd cyclic Clifford constraints pass on 1,144 tested blocks, and the all-order path divisibility condition holds. The surviving modular and module data do not supply coherent associators. | [Source](../manuscripts/rank6/papers/chapters/frontier_155_odd_clifford.tex) (`sec:r155-odd-clifford`) |
| `R6_8_1660` | **Open.** In the positive spherical representative, all indicators and central phase masses are determined; 640 labelled restriction profiles survive in branches 68, 286, 286. These necessary data do not construct a category or yield a general obstruction. | [Source](../manuscripts/rank6/papers/chapters/frontier_1660_phase_masses.tex) (`sec:1660-all-indicators-phase-masses`) |

## Rank 7: accepted decisions

| Case | Scope of decision | Argument or construction | Current proof |
|---|---|---|---|
| `R7_3_146` | General exclusion | Galois symmetry and two center moments | [Source](../manuscripts/rank7/papers/quadratic_center_trace.tex) (`thm:quadratic-center-trace`) |
| `R7_3_601` | General exclusion | Simple-center induction lattice | [Source](../manuscripts/rank7/papers/r601_center_lattice.tex) (`thm:r601-center-lattice`) |
| `R7_3_1022` | General exclusion | Inverse V4 Morita reduction to a near-group obstruction | [Source](../manuscripts/rank7/papers/inverse_v4_morita.tex) (`thm:r1022-general`) |
| `R7_4_35` | Unitary construction | Inversion orbifold and reflection Morita dual, from NG(C4 × C4,16) | [Source](../manuscripts/rank7/papers/inversion_orbifold_model.tex) (`thm:inversion-v4`) |
| `R7_4_106` | General exclusion | Galois symmetry and two center moments | [Source](../manuscripts/rank7/papers/quadratic_center_trace.tex) (`thm:quadratic-center-trace`) |
| `R7_4_2053` | General exclusion | Dihedral Morita reduction to the R8_1_18 obstruction | [Source](../manuscripts/rank7/papers/r2053_r18_reduction.tex) (`thm:r2053-final`) |
| `R7_4_2155` | General exclusion | Galois symmetry and two center moments | [Source](../manuscripts/rank7/papers/quadratic_center_trace.tex) (`thm:quadratic-center-trace`) |
| `R7_4_2591` | General exclusion | Twisted V4 Morita obstruction | [Source](../manuscripts/rank7/papers/r2591_staged_morita.tex) (`thm:r2591-staged-morita`) |
| `R7_4_2603` | General exclusion | Reciprocity and two center moments | [Source](../manuscripts/rank7/papers/r2603_center_moments.tex) (`thm:r2603-center-moments`) |
| `R7_4_2665` | Unitary construction | Inversion orbifold and reflection Morita dual, from NG(C16,16) | [Source](../manuscripts/rank7/papers/inversion_orbifold_model.tex) (`thm:inversion-orbifold`) |

## Rank 8: accepted decisions

| Case | Scope of decision | Argument or construction | Current proof |
|---|---|---|---|
| `R8_1_9` | General exclusion | Cyclic induction phase multiplicities | [Source](../manuscripts/rank8/paper/r9_pointed_class2.tex) (`thm:r9-center-trace`) |
| `R8_1_18` | General exclusion | Modular STS identity and a fourth-moment projection | [Source](../manuscripts/rank8/paper/r18_center_trace.tex) (`thm:r18-sts-moments`) |
| `R8_1_49` | General exclusion | Frobenius–Schur parity and inverse Morita reduction | [Source](../manuscripts/rank8/paper/unified_20261016.tex) (`prop:r49-fs-morita`) |
| `R8_2_24` | General exclusion | Inner-square obstruction from short gauge weights and tensor-functor rigidity | [Source](../manuscripts/rank8/paper/r24_inner_square.tex) (`thm:r24-general-exclusion`) |
| `R8_2_33` | General exclusion | Conductor-seventeen indicator balance | [Source](../manuscripts/rank8/paper/q17_indicator_balance.tex) (`thm:q17-five-exclusions`) |
| `R8_2_36` | General exclusion | Conductor-seventeen indicator balance | [Source](../manuscripts/rank8/paper/q17_indicator_balance.tex) (`thm:q17-five-exclusions`) |
| `R8_2_37` | Unitary construction | Nonsplit C2 extension of the unitary 2D2 category | [Source](../manuscripts/rank8/paper/unified_20261016.tex) (`prop:r37-model`) |
| `R8_2_76` | General exclusion | Conductor-seventeen indicator balance | [Source](../manuscripts/rank8/paper/q17_indicator_balance.tex) (`thm:q17-five-exclusions`) |
| `R8_2_152` | General exclusion | Algebraic rigidity of the 2D2 module graph | [Source](../manuscripts/rank8/paper/unified_20261016.tex) (`prop:2d2-four-general`) |
| `R8_2_153` | General exclusion | Algebraic rigidity of the 2D2 module graph | [Source](../manuscripts/rank8/paper/unified_20261016.tex) (`prop:2d2-four-general`) |
| `R8_2_166` | General exclusion | Algebraic rigidity of the 2D2 module graph | [Source](../manuscripts/rank8/paper/unified_20261016.tex) (`prop:2d2-four-general`) |
| `R8_2_170` | General exclusion | Odd-involution Morita reduction to a near-group obstruction | [Source](../manuscripts/rank8/paper/unified_20261016.tex) (`prop:r170-morita`) |
| `R8_2_190` | General exclusion | Fibonacci character parity | [Source](../manuscripts/rank8/paper/unified_20261016.tex) (`thm:fib-character-parity`) |
| `R8_2_314` | General exclusion | Pointed support of a twisted half-braiding | [Source](../manuscripts/rank8/paper/unified_20261016.tex) (`prop:twisted-two`) |
| `R8_2_342` | General exclusion | Quantum-group inverse-Morita rigidity | [Source](../manuscripts/rank8/paper/unified_20261016.tex) (`prop:r342-morita`) |
| `R8_2_412` | General exclusion | Conductor-seventeen indicator balance | [Source](../manuscripts/rank8/paper/q17_indicator_balance.tex) (`thm:q17-five-exclusions`) |
| `R8_2_432` | General exclusion | Pointed support of a twisted half-braiding | [Source](../manuscripts/rank8/paper/unified_20261016.tex) (`prop:twisted-two`) |
| `R8_2_446` | General exclusion | Conductor-seventeen indicator balance | [Source](../manuscripts/rank8/paper/q17_indicator_balance.tex) (`thm:q17-five-exclusions`) |
| `R8_2_489` | General exclusion | Fibonacci character parity | [Source](../manuscripts/rank8/paper/unified_20261016.tex) (`thm:fib-character-parity`) |
| `R8_2_495` | General exclusion | Algebraic rigidity of the 2D2 module graph | [Source](../manuscripts/rank8/paper/unified_20261016.tex) (`prop:2d2-four-general`) |
| `R8_2_535` | Unitary construction | Dual of the Q-system 1+rho in a unitary HI(C6) category | [Source](../manuscripts/rank8/paper/unified_20261016.tex) (`prop:r535-model`) |
| `R8_2_630` | General exclusion | Third-indicator triangle obstruction at conductor forty | [Source](../manuscripts/rank8/paper/q630_weighted_indicator.tex) (`thm:q630-exclusion`) |
| `R8_2_666` | Unitary construction | Pointed centralizer in the center of NG(C4,4) | [Source](../manuscripts/rank8/paper/unified_20261016.tex) (`prop:c4-centralizer`) |
| `R8_2_671` | General exclusion | Conductor-forty center trace obstruction | [Source](../manuscripts/rank8/paper/r671_center_trace.tex) (`thm:r671-center-trace`) |
| `R8_2_820` | Unitary construction | Nonpointed center factor of NG(C5,5); auxiliary group C3 × C3 | [Source](../manuscripts/rank8/paper/unified_20261016.tex) (`prop:near-group-centralizers`) |
| `R8_2_869` | Unitary construction | Nonpointed center factor of NG(C5,5); auxiliary group C9 | [Source](../manuscripts/rank8/paper/unified_20261016.tex) (`prop:near-group-centralizers`) |

## Classification boundary of the historical study

The following boundary describes the 17 October study; current M5 and M3 extensions are stated above.
Through multiplicity nine, rank six has 25,362 exclusions, 57 realizations and
two open cases. Rank seven is complete through multiplicity four with 4,172
exclusions and 29 models. Rank eight is complete through multiplicity two:
896 exclusions and 77 models, with no open case.

Run the current aggregate replay from the repository root:

```bash
python3 tools/restore_data.py
python3 tools/verify_current_publication.py --historical
python3 -O tools/verify_current_publication.py --historical
```

These checks validate the accepted inventory and its source-bound computational
dependencies. They do not replace the full base-certificate replays or prove
categorical coherence. See [verification scope](PREPUBLICATION_REVIEW.md),
[complete replay instructions](VERIFY.md) and [source provenance](PROVENANCE.md).
