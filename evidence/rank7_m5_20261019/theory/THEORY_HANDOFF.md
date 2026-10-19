# Rank-seven multiplicity-five theory handoff

All statements concern complex fusion categories. The computations use exact
integer/rational arithmetic except `structural_invariants.json`, whose
`dimensions_approx` and `dimension_approx` fields are discovery diagnostics only.
Their floating-point values assign no classification status.

## Certified general exclusions

1. **Closed rank-six subring descent** — `rank6_subring_descent.py` and
   `rank6_subring_certificates.json`. Five nested general certificates replayed
   successfully against the actual restricted tensor, after exact closure and
   dual-stability checks:

   | Rank-seven ring | Restricted rank-six ring | Basis |
   |---|---|---|
   | R7_5_1033 | R6_4_304 | 0,1,2,3,5,6 |
   | R7_5_1283 | R6_3_194 | 0,1,2,3,5,6 |
   | R7_5_2019 | R6_3_244 | 0,1,2,3,5,6 |
   | R7_5_5232 | R6_2_51 | 0,1,2,4,5,6 |
   | R7_5_5681 | R6_4_19 | 0,1,2,3,4,6 |

   The recorded census IDs are provenance only; the verifier checks the nested
   certificate on the tensor and does not accept status by ID.

2. **Spectral involution modules** — `spectral_module_results.jsonl`, produced
   by `scan_spectral.py` using the existing generic-rank
   `supplements/rank6/software/new_module_spectral.py`. All 178 inputs completed,
   with no budget failures. Seven exclusions were independently replayed:
   R7_5_1396, R7_5_1781, R7_5_2181, R7_5_2247, R7_5_2454,
   R7_5_3078, R7_5_3102. These extend the cheap involution test, whose original
   implementation restricted the fixed-object block to size at most two.

3. **Cubic Fourier module** — `cyclic3_spectral.py`,
   `cyclic3_spectral_certificate.json`, and the complete written proof
   `cyclic3_spectral.tex` (proposition label `prop:cubic-Fourier-module`).
   This excludes R7_5_5007 without assuming pivotality. Its forced C3 Fourier
   action would have a Hermitian four-by-four matrix with moments (0,10,15),
   whereas its entry constraints and first two moments allow exactly 81
   matrices with cubic traces only -3 or 6. The root and the independent
   census reviewer both checked the categorical reduction and exact replay.

4. **Published quadratic rank-three descent** —
   `quadratic_rank3_descent.py`, `quadratic_rank3_certificates.json`.
   R7_5_3373 and R7_5_3374 contain the same subring on basis (0,1,6):
   X²=1+4X+4Y, XY=4X+5Y, Y²=1+5X+5Y. Its codegree polynomial is
   (t-3)(t²-168t+252). Ostrik, arXiv:1309.4822, Theorem 5.1 makes every
   hypothetical categorification spherical; Theorem 1.1 then excludes this
   multiplicity-five ring. These two rings were already excluded independently
   by the general-induction pipeline, so this is an alternative short proof.
   The source PDF was checked directly, including its exact theorem scope.

## R7_5_4982: a verified necessary module representation, not a model

The C3 Fourier-module analysis does **not** exclude R7_5_4982. It supplies
18 feasible matrices; these have no demonstrated coherent associators and
must not be called categorifications. The calculation is reproducible with
`test4982.py`; the resulting lists are `4982_matrix_candidates.json` and
`4982_full_representations.json`.

More precisely, let g=b1, X=b3, Y=b4, Z=b5, W=b6. The four noninvertibles
are g-fixed. The nonzero residues modulo three force the left-g action to be
identity on each nontrivial Fourier sector. On such a sector,
T_X=diag(-1,3,3,3); the last three coordinates carry a Hermitian matrix T_Y
with characteristic polynomial t³+t²-12t+11. Its first three moments are
(-1,25,-70). An exact enumeration gives 639 matrices satisfying the first
two moments, and 18 also satisfying the third. Every one extends to the
full fusion-ring representation by

    T_Z = 7 I - 3 T_Y - T_Y²,
    T_W = -8 I + 2 T_Y + T_Y²

on the three-dimensional block. All Eisenstein entries have the required
nonnegative multiplicity distributions.

A hypothetical categorification would therefore give a right-module
category for A=1+g+g² with 13 simple modules. With the module A normalized
to dimension one, their FP dimensions are (1^4,4^9). The action of A on
this module category is 3I. The usual Morita restriction Gram identity
then forces the dual fusion category to have dimension type (1^12,4^27),
again of total FP dimension 444. This is a necessary reduction only; no
coherent category or associator is constructed here, and no claim about
the isomorphism type of the invertible group is needed.

## Structural overview

`scan_structure.py` records all proper based subrings, duality, exact
formal-codegree factorizations and rank-six matches for the original 178
survivors in `structural_invariants.json`. The number of invertibles is
1 for 56 rows, 2 for 84, 3 for 6, 4 for 28, 5 for 2, and 6 for 2.
The 12 integral rows were sent to the model/arithmetic reviewers. Their
classifications must be taken from the final pipeline ledger rather than
from this original invariant snapshot.
