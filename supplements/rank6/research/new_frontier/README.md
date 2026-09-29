# Full Morita-action investigation

This directory records a new necessary condition and additional exact research
on R6_3_215. It does not claim that a feasible based-ring completion is a category.

## Full action Gram identity

Let M be an invertible C-D bimodule category with simple objects m_a. Let
L_i[a,b]=[X_i m_a:m_b] and R_j[a,b]=[m_a Y_j:m_b]. The associativity
identity m_a(m_b* m_c)=(m_a m_b*)m_c gives

    sum_j R_j[a,d] R_j[b,c] = sum_i L_i[b,a] L_i[c,d].

Thus, on vectorizing every right action matrix, the full matrix

    G[(a,d),(b,c)] = sum_i L_i[b,a] L_i[c,d]

is a sum of nonnegative integral rank-one matrices. Each vector is in im(G),
each entry is bounded by the square root of the corresponding diagonal entry,
and the corresponding matrix commutes with all L_i. Transposition permutes
these vectors. This couples the previously separate module-simple Gram tests.

For the algebra 1+g, where g is an invertible involution fixing a simple object,
the columns at the regular module form the unique nonnegative integral Gram
factorization of I+L_g: two unit columns at each fixed point and one pair-column
at every transposition. This supplies every permissible first column and,
by duality, every permissible first row. The unit right action is the identity.

`software/full_morita_gram.py` reconstructs all these finite domains. The
candidate enumeration is exact; an LP solver only proposes a separating vector,
which is checked using integers. A computational budget overrun is explicitly
incomplete, never an exclusion. The scan of all 47 input residuals has no new
whole-ring exclusion. There are 21 eligible tensors and 26 ineligible tensors.
All 54 supplied positive models were checked without a false exclusion.

## The first residual

`full_dual.py` and `solve_full_dual.py` explore all 16 module actions of the
forced algebra 1+g in R6_3_215. There are exact full action Gram completions for
two branches. Their right action matrices are linearly independent and their
products reconstruct the original fusion ring, under a based permutation.
This prevents the incorrect inference that this condensation must have one
of the known Asaeda-Haagerup rank-nine duals.

The initial numerical infeasibility outputs of `solve_full_dual.py` are discovery
data. They have now been superseded for this tensor by
`frontier_full_morita.json`: two rank obstructions, twelve exact Farkas
certificates, and two unique surviving full Gram frames.
`verify_frontier_full_morita.py` reconstructs all sixteen branches, verifies
the certificates and the uniqueness of the surviving frames, and checks the
complete right fusion tensors without calling an optimizer. Thus the based ring
of the involution Morita dual is forced to equal R6_3_215. No categorical
equivalence, extra algebra, or categorification follows from that based isomorphism.

`morita_closure_scan.py` explores complete action frames and their multiplication
on other residuals. It records explicit timeouts and does not infer exclusion
from rejecting a single possible frame. Its nonfaithful cases require additional
fusion data and are marked as such.

## Caution about the cyclic-eight model

The Z2-de-equivariantization of the generalized Haagerup category for Z8 has
rank-eight quadratic Z4 fusion rules and the same global dimension as R6_3_215.
The source is Grossman-Izumi, arXiv:1501.07679, Examples 4.4 and 6.10.
It has Q-systems 1+alpha_g rho for every g, by the same paper, Section 2.4,
Eq. (2.22) (Eq. (2.24) in the published version), and tensor functors preserve
these algebra structures.

For A=1+rho its module category has six simples. On the last two simples the
rho-action is [[a,7-a],[7-a,a]], where a is 3 or 4. The a=3 action is the
one-sigma case and forces the rank-six candidate as a possible based dual.
However Grossman-Izumi-Snyder, arXiv:1501.07324, Lemma 4.16 excludes this case
when the second Q-system 1+alpha_1 rho is present. The a=4 action has additional
possibilities when the hypothesis of their Lemma 4.11 is absent; their
Remark 4.14 explicitly warns of the additional dual graphs. Hence the canonical
A=1+rho dual is not a valid construction of R6_3_215.

This does not by itself exclude R6_3_215 in general, nor does it exclude every
possible Morita realization in the cyclic-eight quotient's Morita class.

## General categorifications reduce to the pseudo-unitary case

`frontier_spherical_reduction.py` and its frozen JSON certificate exhaust all
oriented signed quotients for R6_3_215 without indicator-sign normalization:
274,655 search nodes yield 1,480 quotients in 63 complete sign orbits. One
orbit consists of the 32 gauges of the original tensor. Every character
component in the other 62 orbits is impossible: 228 have a zero simple
dimension, and 43 violate formal-codegree norm divisibility at 17. The older
normalized twelve-table enumeration is retained as a regression control in
`frontier_spherical_reduction_normalized.json`; the default behavior of the
shared enumeration engine is unchanged.

For a gauge-original signed quotient, flip the corresponding lifts in the
sphericalization. Their signed tensor coefficients then equal the original
nonnegative coefficients. The opposite lifts consequently have multiplicity
zero, so the chosen lifts close under tensor product and project equivalently
to the original category. This proves sphericality. Of the original ring's
characters only the Frobenius–Perron quadratic orbit has no zero dimension.
Every categorification therefore has a pseudo-unitary Galois conjugate.
Existence itself remains unresolved. Replay uses no optimizer and also passes
with Python optimization enabled.

## The supplied restriction does not realize the actual cyclic-eight center

`cyclic8_morita_exclusion.md` gives a further, explicitly conditional categorical
obstruction: the supplied positive restriction matrix from the actual
Grossman–Izumi cyclic-eight center cannot be a central forgetful functor to an
R6_3_215 category. This is stronger than simply observing that the canonical
1+rho construction fails, while it still does not classify arbitrary centers.

`cyclic8_rank6_modules.py` exhausts 2,025 bounded integer action parameters and
finds precisely eight possible rank-six modules in two types. The right
action of g is uniquely forced. Condensing 1+g converts the second type to the
first using the exact involution-dual result above. The simultaneous second
small algebra in the actual source category then gives a dimension-square
contradiction, checked by `cyclic8_small_algebra_dimensions.py`. Both scripts
use exact integer/rational arithmetic, including under `python -O`.
