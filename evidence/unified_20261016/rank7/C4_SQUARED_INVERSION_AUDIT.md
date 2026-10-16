# Independent audit of inversion descent from NG(C4 x C4,16)

Status: **PASS for the unitary realization of R7_4_35**.
The categorical descent, group discriminator, and final source comparison
have all been checked independently.

The proposed input is the established unitary NG(C4 x C4,16) solution,
with a cyclic isotropic subgroup H=< (1,1) >, a|H=1, and quotient C4.
The source solution and the resulting rank-eight orbifold are the existing
construction inputs; this note addresses the additional symmetry.

## 1. The noncyclic inverse-algebra issue

It would be incorrect to use H²(C4 x C4,C*)=0: this group is nonzero.
Nevertheless, the actual regular-group self-Morita bimodule has the
untwisted algebra on both sides.

Use Izumi Theorem 11.3's fixed-point model. Its distinguished simple is
kappa:M^alpha -> M, with

    alpha_g kappa = kappa,
    kappa alpha'_g = Ad U(-g) kappa,
    alpha'_g = Ad U(-g)|_(M^alpha).

The original left internal end is the untwisted regular G algebra because
the left stabilizers alpha_g kappa=kappa are strict. On the right, choose

    u_g=U(g): kappa alpha'_g -> kappa.

The stabilizer comparison from kappa alpha'_g alpha'_h to kappa is
u_h composed with u_g right-whiskered by alpha'_h. Right whiskering
precomposes the domain homomorphism but leaves the implementing
intertwiner u_g unchanged. The composite is therefore

    U(h)U(g)=U(g+h).

Here U is the genuine unitary representation in Izumi's model. Thus the
right projective stabilizer cocycle is exactly trivial. One must not
replace this expression by alpha'_g(U(h)): in general U(h) does not even
belong to M^alpha, the domain of alpha'_g.

Passing to the opposite left module inverts or transposes this trivial
class, leaving it trivial. Hence the original and inverse left modules
are both determined by the same untwisted regular internal-end algebra.
They are equivalent. It follows that the square of the chosen
self-Morita bimodule is the regular bimodule with a tensor
autoequivalence G0 on the right.

## 2. Central action, descent, and coherence

The spectral-projection sign calculation in the independent R2665 audit
uses only the nondegenerate bicharacter, not cyclicity of G. It proves
that the parent center equivalence sends g to -g. Its square fixes all
central-invertible labels. Izumi Corollary 13.5, in the m=|G| case,
acts faithfully on these labels, so G0 is tensor-isomorphic to Id.
Inversion preserves H and the regular central algebra A.

Central base change, regularity of the descended left module, and the
left/right A-character calculation therefore apply exactly as in the
R2665 construction. They supply a tensor autoequivalence F of the
rank-eight orbifold D with

    F(r)=r^-1,     F(rho)=r^-1 rho,
    rho²=1+(1+r+r²+r³)rho.

The restriction of chi(g,-) to H for a quotient generator g is a
primitive character. Central monodromy gives T²=Inn(r) and a central
lift of r². The possible square is F²=Inn(r^ell)T^j; its identity
permutation implies 2ell+j=0 mod4. Thus F² is tensor-isomorphic to Id.
Since rho² contains rho and all r^j rho, U(D)=1, so the C2 coherence
condition follows from Aut_tensor(Id_D)=1.

This constructs an actual unitary crossed product D semidirect_F C2,
with invertible group D8 and its canonical reflection algebra 1+s.

## 3. Pointed associator and the integral-group discriminator

Choose the complement <(1,0)> to H in G=C4 x C4. It has order four.
The quotient generator r is represented by an actual order-four
automorphism alpha_(1,0) in the crossed-product factor realization:
on lambda_h its fourth power acts by chi((1,0),h)^4=1, and on the
original factor it is already the identity. Consequently the pointed
C4 subcategory of D has trivial associator. This is stronger than a
statement about the fusion rules of its invertibles.

Let Omega be the associator on the D8 pointed part of the extension.
Its restriction to the rotation C4 is trivial. Every other nontrivial
cyclic subgroup is a reflection C2, on which a third-cohomology class
has order at most two. Therefore Ng--Schauenburg Theorem 9.2 gives

    FSexp(C(D8,<s>,Omega,psi)) divides 4.

The integral sector of the reflection dual is Tambara--Yamagami on a
group of order four. It cannot have group C4. Indeed Shimizu,
*Frobenius--Schur indicators in Tambara--Yamagami categories*,
arXiv:1005.4500, Theorem 3.4 and its following displayed formula give

    nu_4(m) = |A|^(-1/2) sum_a chi(a,a)^(-1).

For A=C4, nondegeneracy forces chi(1,1)=i or -i, and hence
nu_4(m)=1-i or 1+i. Neither equals FPdim(m)=2, so the FS exponent
cannot divide four. This argument is independent of the sign of tau.
The group must instead be V4.

The irrational double-orbit analysis is the same as for R2665 except
that rho² has invertible term 1. Each irrational orbit is consequently
self-dual.

## 4. Final theorem and exact source replay

I independently read the finished `R35_INVERSION_CONSTRUCTION.md` and
ran

    python -O work/unified/two_dimension/verify_R35_inversion_model.py \
      --repo repo \
      --output work/unified/rank7_structural/R35_inversion_independent_replay_O.json

The result is PASS with model-to-census permutation [0,1,5,2,6,3,4].
The source-independent model checks all 343 coefficients, the rank-seven
and rank-sixteen fusion axioms, all eight mixed and irrational induction
identities, the finite-group input, and both exact fourth-indicator
values. Thus the reflection dual has the full R7_4_35 tensor, not merely
its dimension type. This completes the independent audit of a unitary
categorification. It does not decide R7_4_2053 or R7_4_2603.

Primary sources checked: Izumi arXiv:1512.04288v2, Theorem 11.3 and
Corollary 13.5; Ng--Schauenburg arXiv:math/0601012v3, Theorem 9.2;
Shimizu arXiv:1005.4500, Theorem 3.4 and page 10's fourth-indicator
formula. The R2665 second audit contains the shared base-change and
coherence details.
