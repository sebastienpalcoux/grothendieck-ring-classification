# The proposed inversion action on the two known C4 Haagerup categories

The proposed rank-seven construction would start with a generalized
Haagerup category for C4 and require a tensor autoequivalence inducing

    alpha_g -> alpha_{-g},       alpha_g rho -> alpha_{1-g} rho.

The resulting orbit dimensions would have the desired form, but this
based-ring symmetry does **not** lift for either of the two known unitary
C4 generalized Haagerup categories. Thus this construction does not decide
`R7_4_35` or `R7_4_2053`.

These obstructions also cover tensor autoequivalences not initially
required to preserve the unitary structure: Reutter's Theorem 1 makes
every tensor equivalence between unitary fusion categories monoidally
isomorphic to a unitary one, preserving its permutation of simple labels.

## Standard category P1

Grossman, *Fusion Categories Associated to Subfactors with Index 3+sqrt(5)*,
Lemma 4.5, proves `Out(P1)=C2`. Grossman–Izumi–Snyder, *Graded extensions
of generalized Haagerup categories*, the opening of Section 3 (page 10 of
the arXiv version), explicitly identifies the generator as an outer
automorphism which fixes the invertible objects and sends rho to
alpha_p rho for odd p. Inner autoequivalences also fix every alpha_g,
because C4 is abelian. Therefore every tensor autoequivalence of P1 fixes
the invertible labels. In particular, none sends alpha_1 to alpha_3.

The outer group being C2 does not supply a C2 action with the proposed
permutation: the known odd translation on noninvertibles has order four
on those labels, whereas the proposed inversion-plus-translation is a
different based-ring involution.

## Companion category P4

There is also a direct obstruction for the companion solution. Use Izumi,
*The classification of 3^n subfactors and related fusion categories*,
Definition 3.7, Lemma 5.8, Theorem 5.10, and Section 9.3. Put

    x_h = A_g(h,0).

For the C4 solutions these numbers do not depend on g. Gauge
transformations multiply this entry by delta_g^2 delta_{g+h}^2=1.
Replacing rho by alpha_p rho does not change x_h either: in Lemma 5.8,
the phase at k=0 is

    nu(p+g+h)^2 overline(nu(p+g)^2 chi(h))
      = chi(p+g+h) overline(chi(p+g) chi(h)) = 1.

There is no additional cohomological action because H^2(C4,T)=0.
Thus the ordered tuple (x_0,x_1,x_2,x_3) is invariant under both gauge and
translation of the distinguished noninvertible object.

For the companion solution, the second tuple in Equation (9.4) gives

    x_1 = (1-sqrt(5)+sqrt(2(-1+sqrt(5))))/4,
    x_3 = (1-sqrt(5)-sqrt(2(-1+sqrt(5))))/4.

These are unequal. Inversion of C4 exchanges x_1 and x_3, so inversion
cannot stabilize the gauge class, even after any translation rho ->
alpha_p rho. Theorem 5.10 therefore excludes the proposed tensor
autoequivalence of P4 as well.

In fact, every tensor autoequivalence of either P1 or P4 fixes all four
invertible labels. Any coherent C2 action on either category therefore
gives two invertible equivariant lifts of each alpha_g: the stabilizer is
C2, and its projective representations over C are two one-dimensional
representations after trivializing the scalar 2-cocycle. Consequently
every such equivariantization has at least eight invertible simple
objects, and in particular cannot have rank seven.

## Scope and primary sources

This rules out the specified equivariantization construction from P1 or
P4. It does not classify arbitrary complex categorifications of the
rank-seven rings, and it does not rule out other input categories or
Morita-related constructions. No realization or exclusion is entered in
the ledger from this observation.

- P. Grossman, arXiv:1612.07185, Lemma 4.5 and Remark 4.16:
  https://arxiv.org/pdf/1612.07185
- P. Grossman, M. Izumi, N. Snyder, arXiv:2201.11901, Sections 2.5 and 3:
  https://arxiv.org/pdf/2201.11901
- M. Izumi, arXiv:1609.07604v2, Definition 3.7, Lemma 5.8,
  Theorem 5.10, and Section 9.3:
  https://arxiv.org/pdf/1609.07604
- D. Reutter, *Uniqueness of Unitary Structure for Unitarizable Fusion
  Categories*, Communications in Mathematical Physics 397 (2023), 37–52,
  Theorem 1: https://doi.org/10.1007/s00220-022-04425-7

The formulas in Lemma 5.8 were checked against the rendered primary PDF
to preserve the complex conjugation bars that PDF text extraction omits.
