# A conductor-saturation obstruction to the metric C3 branch

This note gives a complete exclusion of R12_1_561 and R12_1_628.
It uses the previously proved forced central C3 lift and independently closes
both its Tannakian and metric branches. It does not assume that the
original category is braided or unitary.

## 1. Exact saturation

Pass to a pseudo-unitary Galois conjugate using the published corrected
Schopieray Lemma 3.1. Put d=3+sqrt(10) and D=6(1+d^2)=120+36sqrt(10).
The simple-dimension field and global-dimension field both equal Q(sqrt(10)).
Its nontrivial Dirichlet character chi has conductor 40, and

    (1/D - 1/D')^2 = 1/40.

Thus the dimension-block bound in A. Schopieray, *The dimension block of a
spherical fusion category*, arXiv:2609.35287v1, Theorem 5.1, is an equality.
We use the proof, not only the numerical inequality. Let N=FSexp(C), and let
rho be the canonical unitary modular representation of Z(C), factoring
through SL2(Z/N). Let B0 denote the simple summand of I(1) associated to the
conjugate dimension character. Its dimension is d^2. The nonzero vector

    w = e_1 - e_B0

is fixed by T and lies in the chi-isotypic subspace for the diagonal torus.
Theorem 5.1 and Lemma 3.1 give

    |<w,S w>| = ||w||^2/sqrt(40).

## 2. Equality at an auxiliary prime forces local invariance

Here is an equality refinement of that proof. Write the CRT factorization
SL2(Z/N)=product_l Gamma_l, Gamma_l=SL2(Z/l^{v_l(N)}). Let U_l be its upper
unipotent subgroup, P_l its fixed-space projection, and s_l its Weyl element.
Write A_l=P_l rho(s_l)P_l. On the relevant torus character space the local
compression estimate of Lemma 4.1 is

    ||A_l|| <= cond(chi_l)^(-1/2).

Suppose p divides N but not 40. Then chi_p=1. The remaining commuting local
compressions have product norm at most 1/sqrt(40). Equality in the displayed
matrix coefficient and Cauchy--Schwarz therefore forces

    ||P_p rho(s_p) w|| = ||w||.

Since P_p w=w and rho(s_p) is unitary, rho(s_p)w is U_p-fixed. Consequently w
is fixed by both U_p and s_p^{-1}U_p s_p. These two elementary-unipotent
subgroups generate SL2(Z/p^a), so w is fixed by the entire local factor.
This argument can be applied constituentwise to the orthogonal tensor-product
decomposition used in the proof of Theorem 5.1, or directly to the commuting
compressions: applying A_p preserves all other local torus character spaces.

In particular, if 3 divides N then w is fixed by the local 3-factor.

## 3. A metric C3 factor makes that impossible

The previously proved central lift H=C3 is either Tannakian or a metric
pointed category B=C(C3,q), with q(a)=zeta_3^{r a^2}, r=1 or 2.

In the Tannakian case the actual central regular algebra permits tensor
de-equivariantization. Its dimension is D/3. The H-action on every source
simple is free, so the quotient has four simples, of dimensions 1,1,d,d.
Passing to a pseudo-unitary Galois conjugate if necessary, the same conductor
bound would require

    |3/D - 3/D'|^2 <= 1/40,

whereas its left side is 9/40. Thus the Tannakian branch is impossible without
needing a separate rank-four classification.
In the metric case B is a nondegenerate braided subcategory of Z(C). Therefore

    Z(C) = B boxtimes D0

as ribbon categories, where D0 is its centralizer. This is a splitting inside
the braided Drinfeld center, not inside C.

B0 centralizes B. Indeed the central-induction character identity gives

    S_{B0,h} = dim(B0) dim'(F(h)) = dim(B0)

for h in H, because F(h) is invertible and both dimension characters take
value 1 on it. Positive categorical dimensions imply centralization. Thus
B0=1 boxtimes B1, and

    w=e_0 boxtimes (e_1-e_B1).

This is a nonzero simple tensor.

The metric C3 modular data have T_B=diag(1,zeta_3^r,zeta_3^r) and normalized
S_B the Fourier matrix with entries zeta_3^{2rab}/sqrt(3). Let 3^a be the
full 3-primary part of N and put n=N/3^a. This n is coprime to 3 and divisible
by every other prime-power factor of N. Consequently the element

    L = s t^n s^{-1}

of SL2(Z/N) belongs to the local 3-factor. The saturation argument forces
rho(L)w=w.

Under the EXACT modular factorization S=S_B tensor S_D and T=T_B tensor T_D,

    rho(L)w = (S_B T_B^n S_B^{-1} e_0)
              tensor (S_D T_D^n S_D^{-1}(e_1-e_B1)).

The second factor is nonzero by invertibility. With z=zeta_3^{rn}, which is
nontrivial since gcd(n,3)=1, the first factor is

    ((1+2z)/3, (1-z)/3, (1-z)/3).

Its two non-vacuum coordinates are nonzero. It is not proportional to e_0,
so the displayed pure tensor cannot equal w. This is the desired contradiction.
No separate congruence-level statement for either modular factor, no choice
of a projective modular-representation phase, and no unknown-exponent bound
is needed. The exact Fourier calculation is replayed in verify_saturation.py.

Thus neither nondegenerate C3 braiding can occur. Together with the conductor-bound
Tannakian-quotient exclusion, this excludes both original fusion rings over C.

## 4. Scope and dependencies

The only recent-source input is the explicitly pinned preprint
arXiv:2609.35287v1, Lemma 4.1 and the CRT proof of Theorem 5.1. The equality
refinement above is proved here. No finite FS-exponent bound is assumed; the
unknown exponent N is arbitrary. Only its forced divisor 3 is used. No
unitarizability of C is assumed: the canonical modular representation of the
center of a spherical fusion category is unitary in its standard basis.

The C2 central lift newly found elsewhere in this round is unnecessary for
this proof. Both rings are covered by exactly the same argument.

Primary source checked directly:
https://arxiv.org/pdf/2609.35287v1 (Sections 2--5, especially Lemma 4.1 and
Theorem 5.1). The modular decomposition and character-centralization steps
are the usual nondegenerate-subcategory and central-induction theorems.
