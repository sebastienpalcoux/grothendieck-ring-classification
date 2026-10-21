# An unbounded cyclic near-group construction filter

This is a construction-family obstruction, not a new general categorification
obstruction. It covers every positive integer n, every complex categorification
of the near-group ring `NG(C_n,n)`, and the single operations stated below. It
therefore includes the October 2026 cyclic construction of He--Liu--Lu--Palcoux--Ren,
[Triangular prism equations for near-group categories](https://arxiv.org/pdf/2610.11652),
Theorem 2.10 and Remark 2.11, regardless of its still conditional general
unitarity statement. FP dimensions depend on the ring, so negative categorical
dimensions or other Galois embeddings do not evade this filter.

## Exact infinite-parameter elimination

The noninvertible dimension is `d_n=(n+sqrt(n(n+4)))/2`, and the total FP
dimension is `D_n=n+d_n²=2n+n d_n`. It has minimal polynomial

`x²-n(n+4)x+n²(n+4)`.

For positive integer n the discriminant n(n+4) is not a square: otherwise
`(n+2-m)(n+2+m)=4` for positive integers, which forces n=0. Hence D_n has
degree two. If an exact target FP dimension D is a positive rational multiple
`s D_n`, then, with T and N its quadratic trace and norm,

`n=T²/N-4`, and `s=T/(n(n+4))`.

Thus there is at most one n; there is no search bound. A target of degree one,
four or any degree other than two cannot be such a rational multiple. The
verifier derives the minimal polynomial of D directly from the source tensor:
the matrix `sum_i N_i N_i^T` is the Casimir matrix, with largest eigenvalue
`sum_i FPdim(i)²`. It factors its characteristic polynomial over Q and uses
disjoint rational root-isolating intervals to select the largest-root factor.
This works for noncommutative rings as well. No floating-point dimension match
or presumed embedding is used.

Direct tensor equivalence and Morita equivalence require `s=1`. A faithful
group extension or equivariantization of NG requires positive integral s. A
target obtained by de-equivariantizing NG, or as a neutral component of a
faithful grading on NG, requires `1/s` to be an integer. These are necessary
conditions, not constructions.

## Complete single-operation checks

Every NG(C_n,n) category has full adjoint subcategory: the square of its
noninvertible contains that noninvertible and every invertible. It therefore
has no nontrivial faithful group grading. This rules out the neutral-component
route without an order bound.

Suppose `NG(C_n,n) = B^G` is an equivariantization, equivalently B is its
standard de-equivariantization by a full central copy of Rep(G). Write
`k=|G|>1`. Any proper fusion subcategory of NG is pointed, since containing its
noninvertible would generate all of NG. Rep(G) is integral whereas NG has an
irrational simple dimension, so this copy is proper and pointed. Consequently
G is abelian and its character group embeds in C_n. It follows that G is cyclic
and k divides n.

Every subgroup of a cyclic group has trivial H² with coefficients C*. Use the
equivariantization simple-object parametrization of Burciu--Natale,
[Fusion rules of equivariantizations of fusion categories](https://arxiv.org/pdf/1206.6625),
Corollary 2.13: an orbit with stabilizer H produces |H| simples, of dimension
`[G:H] FPdim(Y)`. If Y is invertible, these dimensions are integers, so they
cannot equal the irrational NG dimension d_n. Thus its orbit is fixed and it
produces k invertibles. Conversely every invertible of NG forgets to an
invertible, giving exactly n/k invertibles in B. The forgetful group homomorphism
from C_n is surjective onto these invertibles, so their group is cyclic.
This also follows directly from Burciu--Natale, Remark 3.1.

There is exactly one noninvertible simple in the equivariantization. Hence
there is exactly one orbit of noninvertible simples of B and its stabilizer
must be trivial (otherwise it would produce at least two simples). Thus B
has exactly k noninvertibles, each of FP dimension d_n/k. We have proved the
necessary constraints

`rank(B)=n/k+k`, `|G(B)|=n/k`, and `G(B)` cyclic.

These arguments require neither a C* structure nor sphericality.

## Results for all 34 original frontier tensors

All direct/Morita matches have the wrong exact FP dimension. The sole
positive-integral upward scaling is R436, with n=3 and s=2; its separately
verified general TPE obstruction excludes both the extension and
equivariantization routes. The audit replays that independent proof before
using it. All other upward scalings fail integrality or polynomial degree.

The reciprocal-integral quadratic cases have the following unique parameters:

| Target IDs | n | k=1/s | Additional obstruction |
|---|---:|---:|---|
| R439, R567 | 12 | 2 | Required invertibles C6; source invertibles S3 |
| R721 | 64 | 16 | Required rank 20 |
| R921 | 36 | 6 | Required rank 12 |
| R1055, R1768 | 144 | 24 | Required rank 30 |
| R1154, R1203, R1795, R2842 | 320 | 96 | 96 does not divide 320 |
| R3258, R3413 | 45 | 7 | 7 does not divide 45 |
| R3472 | 196 | 28 | Required rank 35 |

For example R65 uniquely gives n=121 and s=4/121; neither s nor its reciprocal
is an integer. R455 gives n=9 and s=2/3. R1350 and R2885 give n=196 and
s=3/98. The quartic families are eliminated by degree, including R901 and
R1463; one must not mistakenly use a different quadratic Casimir factor in
place of their quartic FP-global-dimension factor. The two integral targets
are also excluded by degree. Newly generally excluded rows are retained as
controls in this original 34-row audit.

## Scope and replay

```
python evidence/rank8_frontier_20261021/structural_models/near_group_scaling.py
python -O evidence/rank8_frontier_20261021/structural_models/near_group_scaling.py
```

The default commands are read-only and compare deterministic JSON evidence.
All34 source tensor hashes, exact FP minimal polynomials, rational isolating
intervals, unique n and s where applicable, and route-specific contradictions
are retained. The operations are **direct/Morita equivalence**, **one group
extension**, **one equivariantization**, **one neutral-component extraction**,
and **one standard de-equivariantization**, starting from NG(C_n,n). We have
not excluded arbitrary chains, Morita changes inserted before or after other
operations, general noncentral algebra condensations, or unrelated
constructions. In particular, a rank obstruction is not invariant under a
subsequent Morita change. No unclassified ring is promoted to a general
negative by this family audit.
