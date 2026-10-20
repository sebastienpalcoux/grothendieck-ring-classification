# Third relative moments and a Cauchy refinement for the final sqrt(5) cases

These notes concern `R7_5_3895` and `R7_5_5039`. They are necessary restrictions, not a categorification or a completed exclusion. The unrestricted three-moment experiment remains feasible on the four character-compatible low frames, even after imposing integer multiplicities of the eigenvalue one in the third rotation.

## An unrestricted finite three-moment domain

Let `K=Q(sqrt(5))`, and let `t_K` be normalized relative trace from a cyclotomic field containing the argument and `K`. For every root of unity `theta`, the vector

`(t_K(theta), t_K(theta^2), t_K(theta^3))`

lies in the convex hull of the tuples for the 180th roots of unity, together with their multiples by `-1/6`.

To prove this, write the order as `2^a 3^b 5^c u`, where `u` is coprime to 30. If `a>=3`, `b>=3`, `c>=2`, or `u` has a square factor, all three relative traces vanish: raising to any of the powers 1,2,3 leaves a prime-power factor on which the appropriate Ramanujan or induced quadratic Gauss sum vanishes. Otherwise `m=2^a 3^b 5^c` divides 180 and `u` is squarefree. Cyclotomic disjointness gives a common factor `mu(u)/phi(u)` multiplying a primitive `m`-root tuple. The primitive exponent absorbs the quadratic character of `u`. This common factor belongs to `[-1/6,1]`, since every prime divisor of a nontrivial `u` is at least seven. The zero tuple is itself obtained from a 180th root (for example a primitive 180th root).

The function `hull()` in `q5_third_moment.py` independently computes every base tuple in `Q[zeta_180]`, reducing modulo `Phi_180`. It averages over the 24 units congruent to 1 or 4 modulo 5 and uses

`sqrt(5)=1+2*zeta_180^36+2*zeta_180^144`.

The resulting endpoint set has 49 distinct tuples, all integral after multiplication by 48. These are stored in `q5_third_hull.json`. This is a complete conductor reduction for relative traces; it does not assert a bound of 180 on actual twists.

## Third rotation constraints

Ng–Schauenburg, *Frobenius–Schur Indicators and Exponents of Spherical Categories*, arXiv:math/0601012, Theorem 4.1, gives

`Tr(theta^3 | I(X)) = D * nu_3(X)`.

The third indicator is the trace of an order-three operator on `Hom(1,X^3)`. If that space has dimension `m=N_XX^{X*}` and the eigenvalue one has multiplicity `a`, then its normalized trace to `K` is

`(3a-m)/2`, with integer `0<=a<=m`.

This follows because `K` is disjoint from `Q(zeta_3)`. It does not require the third indicator to be real. Indicators agree on dual objects; this is also explicitly stated in Remark 4.2 of the same paper. In both source rings the rotation-space dimensions are `(1,2,2,4,4,4,4)`.

The exploratory program adds the third moment to the two-moment domain and first relaxes `a` to its interval. It verifies any returned Farkas covector exactly. It then uses a mixed-integer solver only as a feasibility diagnostic, making the rotation multiplicities integral while keeping center phase weights real. The retained feasible diagnostics are not evidence of a category. No infeasibility claim is made from the solver.

## Stronger published Cauchy restriction

Bruillard–Ng–Rowell–Wang, *Rank-finiteness for modular categories*, arXiv:1310.7050v3, Theorem 3.9, says that a spherical category's global dimension and Frobenius–Schur exponent have the same prime-ideal divisors in the cyclotomic integer ring. Here

`D=80*(9+4*sqrt(5))`,

and `9+4*sqrt(5)` is an algebraic-integer unit with inverse `9-4*sqrt(5)`. Consequently the exponent, and hence every center twist order, has only the rational prime divisors 2 and 5. This restriction is unconditional after the separately proved general-to-pseudo-unitary reduction.

For orders `2^a5^b`, the relative pair is exactly one of ten points. In the coefficient convention `(r,s,t,u)=(r+s sqrt(5), t+u sqrt(5))`, they are:

- `(1,0,1,0)`, `(-1,0,1,0)`, `(0,0,-1,0)`, `(0,0,0,0)`;
- `P_+`, `P_-`, where `P_e=(-1/4,e/4,-1/4,-e/4)`;
- `Q_+`, `Q_-`, where `Q_e=(1/4,e/4,-1/4,e/4)`;
- `R_+`, `R_-`, where `R_e=(0,0,1/4,e/4)`.

Nonzero values come from orders 1,2,4,5,10,20; all other allowed orders give zero for both moments. Thus these ten points form the exact value set, not only a convex-hull relaxation. For Galois/duality orbits of source multiplicity rows, the counts attached to each point are nonnegative integers, because these operations preserve the relative pair. This integrality is available for a stronger finite search.

Since 3 is coprime to the exponent, the third relative moment is the field conjugate of the first. Also `nu_3(X)` is rational integral, either directly from its simultaneous membership in `Q(zeta_3)` and `Q(zeta_N)` or from Lemma 3.3 of the same Cauchy paper. Consequently `nu_3(X)` is congruent to `m` modulo 3. No self-duality assumption is needed.

## A forced maximal third rotation

Let `T` be the full normalized row transport checked in `models/sqrt5/verify_transport.py`, and let `h=D/Dbar`. For a center simple with row `v` and dimension `z`, its Galois image has row `epsilon*T*v` and dimension `epsilon*h*zbar`; the signs cancel in their product. On an orbit with common relative phase, its dimension-weighted row sum `W` therefore satisfies

`W=h*T*Wbar`.

The complete first induction moment, including the induced-unit constituents, is the vector `L_1=D*e_0`. Since the third phase is the conjugate of the first, it follows that

`L_3=h*T*L_1bar=D*T*e_0`.

The exact source transport gives `T*e_0=(1,2,2,4,4,4,4)`. Thus every third indicator equals the dimension of its rotation space. An order-three operator with trace equal to its vector-space dimension has every eigenvalue one, so every third rotation is the identity. This is a categorical structural consequence, not by itself a contradiction.

Primary sources:

- https://arxiv.org/pdf/math/0601012 — Theorem 4.1 and Remark 4.2.
- https://arxiv.org/pdf/1310.7050 — Theorem 3.9 and Lemma 3.3.
