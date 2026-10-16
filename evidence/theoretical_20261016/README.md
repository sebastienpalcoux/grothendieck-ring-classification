# Theoretical residual update — 16 October 2026

This update gives **47 new general complex exclusions** among the **85 previously unresolved cases**. It supplies no new realization. **38 general categorification questions remain open**; this is not a completed classification.

| Rank | Analyzed rings | Generally excluded | Realized | Generally unresolved |
|---:|---:|---:|---:|---:|
| 6 | 25,421 | 25,362 | 57 | 2 |
| 7 | 4,201 | 4,164 | 27 | 10 |
| 8 | 973 | 875 | 72 | 26 |

## General exclusion proofs

| Mechanism | Cases | Proof |
|---|---|---|
| three fixed dual module Gram | `R7_2_11`, `R7_2_205`, `R7_2_275`, `R7_2_287`, `R7_3_387`, `R7_3_1055`, `R7_4_2473` | [Argument](rank7/THREE_FIXED_GRAM_PROOF.md) |
| anti invariant involution module | `R7_2_116`, `R7_2_261`, `R7_3_364`, `R7_3_938`, `R7_3_970`, `R7_4_2644`, `R7_4_2683` | [Argument](rank7/THREE_FIXED_PROOF.md) |
| C3 A4 Morita formal codegree | `R7_2_236`, `R7_4_2167`, `R7_4_2716` | [Argument](rank7/A4_C3_GENERAL_PROOF.md) |
| full induction compression parity | `R7_3_695` | [Argument](rank7/R695_GENERAL_PROOF.md) |
| signed C3 sphericality dimension block | `R7_3_783`, `R7_3_1015` | [Argument](rank7/C3_SIGNED_GENERAL_PROOF.md) |
| positive semidefinite module Gram | `R7_3_909`, `R7_4_776`, `R7_4_927`, `R7_4_2126` | [Argument](rank7/PSD_GRAM_PROOF.md) |
| cyclic stabilizer divisibility | `R7_4_1212`, `R7_4_1213`, `R7_4_1438`, `R7_4_1440`, `R7_4_2731` | [Argument](rank7/CYCLIC_MODULE_PROOF.md) |
| dimension block conductor | `R8_2_35`, `R8_2_38`, `R8_2_346`, `R8_2_406` | [Argument](rank8/DIMENSION_BLOCK_FOUR_PROOF.md) |
| quadratic subcategory index | `R8_2_209` | [Argument](rank8/R209_GENERAL_PROOF.md) |
| cyclic stabilizer divisibility | `R8_2_260`, `R8_2_380`, `R8_2_673` | [Argument](rank8/CYCLIC_STABILIZER_DIVISIBILITY.md) |
| involution anti module spectral | `R8_2_318`, `R8_2_319`, `R8_2_320`, `R8_2_368`, `R8_2_370`, `R8_2_735`, `R8_2_758`, `R8_2_760` | [Argument](rank8/ANTI_MODULE_EIGHT_GENERAL_PROOF.md) |
| Morita adjoint normality | `R8_2_745` | [Argument](rank8/R745_GENERAL_PROOF.md) |
| conductor32 signed Jacobi | `R8_2_857` | [Argument](compression/R857_GENERAL_PROOF.md) |

All listed decisions apply without assuming pivotality, sphericality, pseudo-unitarity or unitarity. The main arguments are theoretical. Exact scripts check source identification, every required tensor product, finite arithmetic and preservation of the previous decisions. The earlier exhaustive one-matrix proof for `R7_4_1212` and `R7_4_1213` is retained as an independent backup; the cyclic-module argument now proves both directly.

## Every original open case is accounted for

- [All 85 cases: CSV](all_cases.csv) · [JSON](all_cases.json).
- [Rank-seven remaining-case register](rank7/RESIDUAL_TAXONOMY.md).
- [All 44 original rank-eight cases](rank8/ALL44_COVERAGE.md).
- [Current general residual IDs](remaining_ids.json).
- [Rank-six research record](rank6/research_progress.json).

Passing a necessary condition is not a categorification. No unresolved record is relabelled by an incomplete search, a failed model match, or a scoped obstruction.

## Additional theorems and scoped results

The [full-induced-unit compression theorem](compression/README.md) uses all constituents of the induced unit, extending the dimension-block argument. It excludes pivotal and spherical categorifications of `R8_2_318` and `R8_2_735`; the independent anti-invariant module argument now excludes arbitrary complex categorifications of both. Its equality case supplies the general `R7_3_695` obstruction after an elementary parity argument. The proof uses the modular compression estimate directly and does not infer a grading from a rational spherical global dimension.

For `R6_8_1660`, the twist-one simple objects of the positive center are exactly the six constituents of `I(1)`. This sharpens the center constraints and yields a shorter tensor-functor-rigidity proof. For `R6_4_155`, all 226 larger local braid blocks have partitions passing the strengthened reflection tests; this constructs neither braid representations nor a category. Both rank-six cases remain open.

The [2D2 central-lift theorem](rank8_m1/README.md) rules out every central lift of its nontrivial invertible. The precise remaining gaps for the three rank-eight multiplicity-one cases are retained.

## Reproduce

From the current repository after `python3 tools/restore_data.py`:

```bash
python3 tools/verify_theoretical_20261016.py
python3 -O tools/verify_theoretical_20261016.py --historical
python3 tools/verify_theoretical_20261016.py --spectral
python3 tools/validate_release.py
```

Python 3, SymPy and NumPy are used by the source applications and historical replay. The optional independent spectral backup also requires a C++17 compiler. The historical option reconstructs the exact pre-update ledgers in a temporary copy and runs the frozen October 2 stage chain. Previous exclusions and realizations are preserved record for record. No fresh execution of every earlier discovery search is claimed.

The dated update archive contains the current proofs, manuscript PDFs and exact finite applications. The older rank-seven and rank-eight ZIPs remain historical October 2 snapshots; use them together with this update or use the current repository.

Primary inputs include Schopieray, [The dimension block of a spherical fusion category](https://arxiv.org/abs/2609.35287), Lemma 4.1 and Theorem 5.1; Etingof–Nikshych–Ostrik, [On fusion categories](https://arxiv.org/abs/math/0203060), Proposition 8.15; and the module-category and generalized near-group results cited individually in the proofs.
