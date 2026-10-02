# Exact scope and correctness of the local braid test

This is a necessary-condition calculation for a positive-ribbon
categorification of the retained rank-26 modular datum attached to R6_4_155.
It is not a general-complex-categorification theorem on its own.

## Exact periodic spectra

Write θ_j=ζ24^{t_j}, with the normalized modular matrix S supplied in
Q(ζ24). All arithmetic uses integer coefficient vectors in
Z[z]/(z^8−z^4+1) or Z[z]/(z^24−z^12+1). A common denominator for S is retained
explicitly; no floating-point arithmetic enters any spectrum or search verdict.

For simple a,b put H=Hom(b,a³), n=dim(H). On H write A=σ1, B=σ1σ2,
D=σ1σ2σ1. The braid relations imply D=BA and D²=B³=Z I,
where Z=θ_b/θ_a³ by the ribbon identity.

The A-eigenvalue ζ48^{t_c−2t_a+24s} has multiplicity
the previously checked self-braiding sign multiplicity for (a,c,s),
multiplied by N_ca^b and summed over c.

Barter–Jones–Tucker, arXiv:1611.00071, Corollary 4.1 and Proposition 4.2, identify
the periodic braid operators with generalized rotations. In their conventions,
the D-eigenvalues are ζ48^{t_b−3t_a+24s}. Their multiplicities are the existing
normalized order-two indicator multiplicities for base a and center target
(b,a*). This is the reciprocal of the target (a*,b) in their displayed diagram;
reciprocation leaves the two signs unchanged.

Their formula also gives

    Tr(B)=θ_a^(-1) Σ_de S_1d conjugate(S_be) (θ_d/θ_e)^3 N_de^a.

For λ_j=ζ72^{t_b−3t_a+24j}, j=0,1,2, the λ_j multiplicity is

    [n + λ_j^(-1)Tr(B) + λ_j conjugate(Tr(B))]/3.

Indeed, B³=Z I and λ_j³=Z, so the spectral projector is
(I+λ_j^(-1)B+λ_j^(-2)B²)/3. Moreover B is diagonalizable with roots-of-unity
eigenvalues, so Tr(B^(-1))=conjugate(Tr(B)), whether or not the representation
is unitary. The code requires every recovered multiplicity to be a
nonnegative integer and checks the exact trace reconstruction.

## Constituentwise necessary inequalities

Use the identity-product triple (D^(-1),B,A). On an irreducible constituent
of dimension r, let m_A,m_B,m_D be its eigenvalue multiplicity functions.
The determinant relation is

    Σ_e e m_A(e) + Σ_e e m_B(e) − Σ_e e m_D(e) = 0 mod 144.

For r=1 this scalar relation is the constituent condition. For r>1 the
following necessary conditions are imposed.

1. For each pair of operators, their largest eigenspace dimensions sum to
   at most r. Otherwise two eigenspaces intersect in a common eigenvector;
   because any two of A,B,D generate the third, this contradicts irreducibility.

2. Scott's inequality, applied to conjugation on End(C^r), gives

       Σ_e m_A(e)² + Σ_e m_B(e)² + Σ_e m_D(e)² ≤ r²+2.

   The common invariant and coinvariant dimensions for conjugation are both 1
   by Schur's lemma. Each individual fixed space is a matrix centralizer of
   dimension the sum of squared eigenvalue multiplicities.

3. For αβ=δ, Scott's inequality on C^r, applied to the scalar-normalized
   identity-product triple (δD^(-1),β^(-1)B,α^(-1)A), gives

       m_A(α)+m_B(β)+m_D(δ) ≤ r.

   There is no common invariant vector or covector for an irreducible
   representation of dimension greater than 1. The code applies this condition
   **only** when the eigenvalue exponents satisfy α+β=δ modulo 144. Pair conditions
   cover cases where one of the three specified scalars is not an eigenvalue.

Scott's rank inequality for matrices T_i with product 1 is
Σ rank(T_i−I) ≥ 2 dim(V)−dim(V^G)−dim((V*)^G).
The argument above uses it directly, not any generic-eigenvalue or
semisimplicity hypothesis on the whole braid representation.

## Why the exhaustive search is safe

A,B,D satisfy separable root-of-unity polynomials. Their restrictions to
submodules and induced quotient maps are therefore diagonalizable. Along a
Jordan–Hölder series their eigenvalue multiplicities add exactly. Consequently
the whole spectra must admit a partition into constituents satisfying the
conditions above, even when the braid representation itself is not semisimple.

The recursion fixes one still-unused A-eigenvalue and enumerates all bounded
submultisets containing it. This loses no partition, since that occurrence
belongs to some constituent. It considers every possible positive constituent
size, every bounded B-multiplicity vector of that size, and every bounded
D-multiplicity vector of that size. The early A bound m_A≤floor(r/2) follows
from condition1 and the fact that D has at most two eigenvalues. The other
pruning tests are conditions stated above. Successful partitions are rechecked
independently of the recursive path. Failed states are memoized only after
their complete constituent enumeration.

A budget interruption raises a separate exception and returns UNKNOWN. It
does not enter the failed-state cache as a proved impossibility. The checkpoint
stores completed blocks; after an interruption the current block restarts.
A negative complete search is reported as CANDIDATE_OBSTRUCTION for independent
replay and theoretical review, not as an automatic new census decision.

The simultaneous normalization A→ζ144^(-e)A, B→ζ144^(-2e)B,
D→ζ144^(-3e)D preserves all equations and inequalities. It permits exact
reuse of identical normalized spectral problems.

Primary sources:

* Barter–Jones–Tucker, https://arxiv.org/pdf/1611.00071 , §4.
* L. L. Scott, *Matrices and cohomology*, Annals of Mathematics 105 (1977),
  473–492, https://doi.org/10.2307/1970920, for the rank inequality. The application to matrix centralizers
  is also the standard necessary dimension inequality in the
  multiplicative Deligne–Simpson problem.
