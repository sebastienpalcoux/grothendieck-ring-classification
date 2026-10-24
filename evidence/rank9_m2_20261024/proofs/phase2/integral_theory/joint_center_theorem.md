# Joint center columns and modular integrality

This criterion applies to a **commutative integral fusion ring** R with simple
dimensions d_i, total dimension D=Σ_i d_i², and rational formal codegrees f_h.
It gives general-complex exclusions: an integral categorification has its
canonical positive spherical structure. No braiding on the source category is
assumed. The modular category used below is its Drinfeld center.

Let N_i denote the regular fusion matrices and

    B = Σ_i N_i N_iᵀ.

For a central simple Z, put v_Z,i=[F(Z):X_i] and z_Z=Σ_i d_i v_Z,i.
The following are necessary.

1. B=Σ_Z v_Z v_Zᵀ. In the commutative case every v_Z,0 is zero or one.
   Those with v_Z,0=1 are precisely the distinguished simples A_h in I(1),
   with z_Z=D/f_h and twist one. Thus, for each β, exactly as many such
   columns have dimension β as there are formal codegrees D/β.
2. Each v is a nonzero nonnegative integral vector, v vᵀ≤B in the positive
   semidefinite order, and v_i v_j≤B_ij entrywise. These conditions give a
   finite exhaustive list: v_i≤⌊√B_ii⌋. As the center is integral and modular,
   D²/z² is an algebraic integer and rational, so D/z is an integer. Hence z|D.
3. For each n≥1 and source simple X_i,

       Σ_Z z_Z v_Z,i θ_Zⁿ = D ν_n(X_i).

   This is the central induction formula for Frobenius–Schur indicators.
   In particular ν_1(X_i)=0 for i>0; ν_2 is zero for a nonselfdual simple
   and ±1 for a selfdual simple. If a selfdual X_i occurs with odd
   multiplicity in some X_j X_j*, the usual symmetric-pairing argument
   forces ν_2(X_i)=1. Allowing the remaining signs to vary continuously
   in [−1,1] only weakens the necessary conditions.

## Eliminating all unbounded twist orders

The primes dividing a central twist order belong to the prime support P of D,
by the Cauchy theorem for spherical fusion categories. Apply normalized Galois
trace to Q in the indicator formula. The normalized trace of a primitive
m-th root to Q, raised to the k-th power, is

    τ_k(m)=μ(m/gcd(m,k))/φ(m/gcd(m,k)).

For moments 1≤k≤H there are only finitely many distinct joint packets. All
nonzero packets arise from orders dividing

    L_H = ∏_{p∈P} p^(1+⌊log_p H⌋).

Indeed, any larger p-adic valuation leaves a square factor in m/gcd(m,k)
for every k≤H, giving the all-zero packet. The zero packet is included.
This proves exhaustive coverage of **all orders**, not a conductor cutoff.

For n≥3 let H_i,n=[X_iⁿ:1]. The rotation defining ν_n has order n and acts
on an H_i,n-dimensional space. Its normalized trace is a sum of normalized
traces of n-th roots. If p(n) is the smallest prime divisor of n, these lie
between −1/(p(n)−1) and 1. Thus

    −H_i,n/(p(n)−1) ≤ Tr_normalized(ν_n(X_i)) ≤ H_i,n.

The exact program uses the n=1,2 identities and these bounds for 3≤n≤H.

## Joint necessary linear system

Make one nonnegative variable for each candidate column with v_0=1, with
its forced twist-one packet. Make one variable for each pair of a candidate
with v_0=0 and an allowed trace packet. Impose the Gram identities, the exact
counts for the distinguished central dimensions, and all preceding indicator
equalities/inequalities. The actual category supplies nonnegative integral
values. Relaxing them to nonnegative rational/real values preserves necessity.

In contrast to the older implementation, the low I(1) columns are variables
inside this single system. They do not have to be enumerated as complete
frames first. This is a unified reformulation of the established center,
Gram, and finite-relative-trace conditions.

After introducing nonnegative slacks, write the system as A x=b, x≥0 with
integer coefficients. An integer vector y with Aᵀy≥0 and bᵀy<0 proves
impossibility. Each accepted certificate contains such a y. Floating-point
linear programming proposes y only; integer arithmetic verifies every
inequality. `verify_center.py` regenerates the finite list and all integer
rows and checks the saved certificate without calling an optimizer.

## A new splitting-field-free modular-integrality refinement

For any candidate restriction v of dimension z, define N_v=Σ_i v_i N_i and

    T_v = (D/z) B^(-1) N_v.

**Proposition.** Every coefficient of the monic characteristic polynomial
of T_v must be an integer.

**Proof.** Since R is commutative and semisimple, its scalar characters χ_h
simultaneously diagonalize N_v and B, with eigenvalues χ_h(v) and f_h.
The central-character identity is

    S_(A_h,Z) = (D/f_h) χ_h(F(Z)).

Consequently the eigenvalues of T_v are S_(A_h,Z)/z. By symmetry of S,
these are values of the modular fusion-ring character indexed by Z on
the simple A_h. Each is an algebraic integer. T_v is rational, so the
elementary symmetric polynomials in its eigenvalues are rational algebraic
integers and hence integers. This proves the proposition.

The test uses rational matrices and exact characteristic polynomials only.
It requires no choice of splitting field, no numerical algebraic-integrality
test, and no assumption that the center is pointed or group-theoretical.
In this campaign it gives the additional exclusion R9_2_366 when coupled
to the joint system. Its known PGL(2,7) companion R9_2_369 survives this
test and the joint system, as a positive control.

## Optional rational-character S symmetry

For every rational character χ_h, label its distinguished column v_h and
require exactly one selection. For rational χ_h,χ_k impose

    (D/f_h) χ_h(v_k) = (D/f_k) χ_k(v_h).

These are linear equations in the labelled column-selection variables.
Anonymous columns retain the remaining formal-codegree multiplicities.
The implementation `center_symmetry.py` adds these necessary equations to
the joint system. It never interprets feasibility as a categorical model.

## Accepted applications in the first integral campaign

The joint system at H=4 excludes R9_2_301, R9_2_352, R9_2_385,
R9_2_725, R9_2_727, R9_2_1028, R9_2_1134, R9_2_1238,
R9_2_1448, R9_2_1465, R9_2_1501, R9_2_1712, R9_2_1778,
and R9_2_1989. Modular-integrality filtering also excludes R9_2_366.
All fifteen saved integer rays have passed fresh exact replay.
The separate preserved-central-subcategory theorem excludes R9_2_907.

## Primary sources checked

- V. Ostrik, *Pivotal fusion categories of rank 3*, arXiv:1309.4822,
  https://arxiv.org/pdf/1309.4822, Section 2: central induction,
  distinguished formal-codegree simples, and their twists/dimensions.
- T. Deshpande, *On centers of bimodule categories and induction-restriction
  functors*, arXiv:1611.04486, https://arxiv.org/pdf/1611.04486,
  Section 2.7, equations (36),(39), and Section 4.3: central characters and S.
- P. Bruillard, S.-H. Ng, E. C. Rowell, Z. Wang, *Rank-finiteness for modular
  categories*, arXiv:1310.7050v3, https://arxiv.org/pdf/1310.7050,
  Theorem 3.9: exponent/global-dimension prime support.
- S.-H. Ng, P. Schauenburg, *Frobenius–Schur indicators and exponents of
  spherical categories*, Adv. Math. 211 (2007), 34–71: the central trace
  formula and tensor-rotation interpretation.

The existing project derivations and `sources/higher_traces.py` give the
same Ramanujan packets and rotation bounds. The new contribution here is
their joint column formulation and the exact rational-operator integrality
refinement, not a claim to have exhausted all modular constraints.
