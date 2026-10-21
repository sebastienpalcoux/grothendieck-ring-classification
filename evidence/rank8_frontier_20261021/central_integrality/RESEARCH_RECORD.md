# Complete additional central calculations

The general scope gate in `GENERAL_GALOIS_PU.md` proves that every complex
categorification of R8_3_721 or R8_3_1154 is spherical and has a pseudo-unitary
Galois conjugate. Its canonical replay exhausts all parity-compatible ordered
signed quotients: 64 for 721 and 288 for 1154. It uses every scalar dimension
character and all formal codegrees, including the matrix block. This is a
proved reduction of the existence problem; it does not assert existence or
unitarity. Both rings remain unresolved.

For R8_3_1154, the earlier complete central-support, duality, rotation and
partial-modular calculations leave only low frame 31 and the second-indicator
tuple (0,0,-1,1,1,1,1). This frame has sixteen allowed high restriction types.
The complete integer Gram system has rank six. Exact affine bounds enumerate
all 14,211 nonnegative integral completions, visiting 40,583 nodes instead of
the 2,634,508,800 points in its unconstrained free-coordinate box. Every
completion is checked against all 28 original Gram equations.

The independently maintained noncommutative calculation in
`../noncommutative/central_integral_filters.py` computes every low-low-low
Verlinde coefficient. Exactly 1,238 Gram patterns have nonnegative integral
coefficients; every one also passes the full quadratic spectral-multiplicity
test. The follow-up `../noncommutative/cubic_tensor.py` gives exact nonnegative
rational solutions for all ten distinguished-pair tensor cones for all 1,238
patterns. These are necessary equations, not constructed tensor categories.

The new `fixed_gram_rotation_1154.py` fixes each of those 1,238 integer Gram
patterns simultaneously with the full joint tensor-rotation equations
through order six and the distinguished-character modular STS equations.
The common matrix is checked with exact primal families and integer Farkas
rays. All patterns are covered: eight are excluded by four exact rays, and
1,230 have exact nonnegative rational solutions. The receipt uses 434
certificate families in total. There are no numerical-only decisions or
unprocessed patterns. A family of primal weights is accepted only after
checking its original matrix equation and nonnegativity for every pattern
assigned to that family, including any affine subspace restrictions.

The intrinsic arithmetic setup is pseudo-unitary. The separately verified
Galois-pseudo-unitary gate makes it a necessary condition for general complex
existence after Galois transport. Its surviving rational solutions do not
construct the unobserved central fusion coefficients, coherent associators,
or a categorification. The bounded rotation order is six; no categorical
exponent bound is claimed. The earlier lower and higher-order searches and
the complete construction-family attempts remain recorded in the
noncommutative and model evidence directories.

Canonical read-only commands, from the repository root:

```sh
python evidence/rank8_frontier_20261021/central_integrality/general_galois_pu_gate.py
python -O evidence/rank8_frontier_20261021/central_integrality/general_galois_pu_gate.py
python evidence/rank8_frontier_20261021/central_integrality/integer_gram_1154.py
python -O evidence/rank8_frontier_20261021/central_integrality/integer_gram_1154.py
python evidence/rank8_frontier_20261021/noncommutative/central_integral_filters.py
python evidence/rank8_frontier_20261021/noncommutative/cubic_tensor.py
python evidence/rank8_frontier_20261021/central_integrality/fixed_gram_rotation_1154.py
python -O evidence/rank8_frontier_20261021/central_integrality/fixed_gram_rotation_1154.py
```

This directory also contains the independent acceptance review of the
separate R8_3_926 general exclusion (`R926_REVIEW.md` and
`review_r926_partial_s.py`). That review rechecks every partial-S column
filter, all dimension-compatible character-label permutations and the two
complete-domain separating rays. It is not an additional 1154 criterion.
