# Local involution commutator and cubic rotation

This note independently derives the local lemma proposed in the round-two
M3 audit. It does not use a braided structure, a central lift of the
involution, unitarity, or a fermionic quotient. The global application
requires the separately verified module-action and center certificates.

## Proposition

Let C be a pivotal fusion category over C. Let g be an invertible object
of order two whose pointed associator is trivial. Let Y be simple with
g tensor Y isomorphic to Y isomorphic to Y tensor g. Choose coherent
multiplication m:g tensor g -> 1 and isomorphisms

    l:g tensor Y -> Y,       r:Y tensor g -> Y.

After scaling l and r, their squares are the identity, with the coherent
copies of m understood. Define the mixed commutator kappa by

    r (l tensor id_g) = kappa l (id_g tensor r).

If kappa=-1 and V=Hom(1,Y tensor Y tensor Y) is nonzero, its cyclic
pivotal rotation is not a scalar operator. Consequently, if dim(V)=2
and the third Frobenius--Schur indicator is rational, then nu_3(Y)=-1.

## Proof with explicit operators

Suppress associators by coherence, but retain the multiplication inverse
eta=m^{-1}:1 -> g tensor g. Define the isomorphism

    a = (r tensor l) (id_Y tensor eta tensor id_Y) : Y^2 -> Y^2.

The maps r,l,eta are all isomorphisms, so a is an isomorphism. On Y^3 put

    a_12=a tensor id_Y,       a_23=id_Y tensor a.

Expand both products by first inserting the two copies of eta. The
resulting word is

    Y g g Y g g Y.

At the first and last Y the two products apply the same map. At the
middle Y their order is, respectively, l(id_g tensor r) and
r(l tensor id_g). The tensor interchange law therefore gives the exact
identity

    a_12 a_23 = kappa^{-1} a_23 a_12.

This is an overlap relation at the middle Y. It is not an assertion that
operators on disjoint tensor factors anticommute. Postcomposition gives
invertible operators A_12,A_23 on V satisfying the same identity.

Write E=E_Y^(3) for the Ng--Schauenburg rotation moving the first tensor
factor to the end. Naturality of the two-block pivotal rotation
Hom(1,U tensor W) -> Hom(1,W tensor U), with U=Y and W=Y^2, gives

    E A_23 = A_12 E.

Equivalently, for the reverse rotation R=E^{-1},

    R A_12 = A_23 R.

If E (or R) were scalar, this would imply A_12=A_23. The relation
A_12 A_23=-A_23 A_12 would then imply A_12^2=0, contradicting
invertibility on the nonzero space V. Thus E is not scalar.

The general pivotal rotation theorem gives E^3=I. In dimension two,
its two eigenvalues are distinct members of {1,zeta_3,zeta_3^2}.
Its trace belongs to {-1,-zeta_3,-zeta_3^2}. Rationality leaves only -1.
No assumption on nu_2(Y) is used.

## Translation from the involution module action

The algebra A=1+g exists because the pointed associator is trivial.
The two right A-module structures on the underlying simple object Y
have g-actions r and -r. Transport the right g-action on g tensor Y
across l:g tensor Y -> Y. The transported map is

    l (id_g tensor r) (l^{-1} tensor id_g) = kappa^{-1} r.

Consequently left tensoring by g interchanges these two module
structures precisely when kappa=-1. On the difference of their two
classes it then acts by -1. Thus the diagonal anti-action entry T_g=-1
used in the package's split-module calculation is exactly the local
commutator condition in this proposition.

The rescalings of l and r cancel from the mixed commutator. Changing the
coherent choice of m or rescaling eta rescales a, without affecting its
invertibility, the overlap relation, or the rotation argument.

## Rationality in the R6_3_215 application

For a pseudo-unitary categorification of this ring put d=4+sqrt(17).
All object dimensions belong to K=Q(sqrt(17)), and

    Dim(C)=8+32d=136+32sqrt(17),
    Norm_{K/Q}(Dim(C))=1088=2^6 * 17.

The Cauchy theorem for spherical fusion categories forces the prime
support of N=FSexp(C) to be {2,17}; in particular 3 does not divide N.
The indicator formula through the center shows

    nu_3(Y) in K(zeta_N).

Here every central object's dimension is in K because it equals the
dimension of its underlying object in C. Since K is contained in
Q(zeta_17), K(zeta_N) is contained in Q(zeta_lcm(17,N)), a cyclotomic
field of conductor coprime to 3. On the other hand E^3=I gives
nu_3(Y) in Q(zeta_3). The intersection of these two fields is Q.
Thus nu_3(Y) is rational (indeed an integer).

In R6_3_215 the two g-fixed simples b4,b5 each have
Hom(1,Y^3) of dimension two. Therefore a complete proof that their
split-module anti-action entries are -1 forces

    nu_3(b4)=nu_3(b5)=-1.

This last deduction is a necessary condition, not by itself a
categorification exclusion. An exclusion still requires a complete,
exact certificate that no permitted center-indicator branch satisfies
both equalities.

## Primary references checked

1. S.-H. Ng and P. Schauenburg, *Higher Frobenius--Schur indicators for
   pivotal categories*, arXiv:math/0503167v2, Definition 3.1, Lemma 3.4,
   and Theorem 5.1. These provide the two-block rotation, its trace
   definition, and E^n=I. The two-block naturality used above follows
   directly from the adjunction and pivotal maps in Definition 3.1.
   https://arxiv.org/pdf/math/0503167
   Existing bibliography key: NSpiv.
2. S.-H. Ng and P. Schauenburg, *Frobenius--Schur indicators and exponents
   of spherical categories*, arXiv:math/0601012v3, Theorems 4.1 and 5.5.
   These give the central twist formula and its order N=FSexp(C).
   https://arxiv.org/pdf/math/0601012
   Existing bibliography key: NS.
3. P. Bruillard, S.-H. Ng, E. C. Rowell and Z. Wang, *Rank-finiteness for
   modular categories*, arXiv:1310.7050v3, Theorem 3.9.
   https://arxiv.org/pdf/1310.7050
   Existing bibliography key: BNRW.

The overlap argument itself is supplied above; it is not attributed to
an unverified external Clifford-algebra theorem.
