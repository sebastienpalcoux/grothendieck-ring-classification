# R8_3_1154: anomaly cancellation and a rank-ten necessary Morita normal form

**Conclusion: R8_3_1154 remains unresolved.** This investigation gives a new
small theoretical reduction, not a categorification and not an exclusion.
It avoids the much larger simultaneous center-completion search.

The reduction uses the already proved positive spherical/Galois gate, the
already excluded untwisted pointed-associator branch, and the current
three-pattern center theorem. Under those inputs, any categorification
has a positive Galois representative C such that C times Semion has a
Morita representative with the single rank-ten based ring displayed below.
The pointed anomaly is cancelled before forming the algebra; no algebra
on 1+g in C itself is assumed.

## 1. Frozen inputs and scope

The input tensor is
`evidence/unresolved_retry_20261024/proofs/unresolved11_20261024/inputs/R8_3_1154.json`,
with compact tensor SHA-256
`c399505be76a64c8aba65feaf2cd55125dc7132f5894b74e58b64473d1387e25`.
Write

- a=6+3sqrt(5), b=a+1;
- FP dimensions (1,b,b,1,a,a,b,b);
- g=X3, with g^2=1;
- D0=Dim(C)=540+240sqrt(5).

Conjugation by g permutes labels as (X1 X2)(X6 X7) and fixes
1,g,X4,X5. Both X4 and X5 are selfdual; X1*=X2; X6 and X7 are selfdual.
The nontrivial pointed C2 associator is forced by
`evidence/rank8_next_20261021/review/R1154_UNTWISTED_MORITA_REVIEW.md`.
This conclusion is about any putative positive representative, not just
unitary categories.

The three surviving source-center patterns are 6971,8766,8772 in
`evidence/rank8_frontier_20261021/central_integrality/integer_gram_1154.json`.
Their accepted proof chain is described in
`evidence/rank8_next_20261021/r1154/README.md`.
The four-object packet theorem, including nonselfduality, is
`evidence/rank8_creative_20261022/r1154/PROOF.md`.
This investigation does not replace the proofs of those inputs.

## 2. Cancel the anomaly, then condense

Let S be a semion category, with nontrivial invertible s. Its underlying
pointed associator is the nontrivial class in H^3(C2,C*). In E=C tensor S,
put h=g tensor s. The associator restricted to <h> is now trivial, since
its class is the sum of two equal order-two classes. Thus

    A=1+h

is a genuine connected separable algebra: choose a trivialization of the
restricted cocycle and transport the ordinary regular C2 algebra.
Let B=E_{A-A}. It is fusion and Morita equivalent to E, and

    Dim(B)=2D0,       Z(B)=Z(C) tensor Z(S).

There is a useful equivariantization description. The semion-factor
C2 grading of E has neutral component C. The invertible h lies in the
odd component, has square 1, and has coherently trivial associator on
its generated subgroup. Hence E is a crossed product of C by the
coherent C2 action induced by conjugation with h. Its action on C's
labels is Ad(g). The standard dual of this crossed product, at the
regular pointed algebra A, is the equivariantization B=C^{C2}.
This description includes the action's coherence; label permutation
alone would not define an action.

The fixed labels 1,g,X4,X5 each have two equivariant lifts, since every
projective representation of their C2 stabilizer is one-dimensional
(H^2(C2,C*)=0). Each length-two orbit {X1,X2}, {X6,X7} has one lift.
Consequently B has simple dimensions

    1,1,1,1,a,a,a,a,2a+2,2a+2.

Let u be the nontrivial character object of Rep(C2) in B. Under the
canonical central embedding it is a boson. The central semion
1 tensor s in E transfers across Morita equivalence to a central
invertible v in B: its underlying bimodule is A tensor (1 tensor s).
Its square is 1, its indicator is -1, and its forgetful image in C is g.
It is distinct from 1,u. Therefore the group of invertibles is V4,
with generators u,v, and both generators commute with all objects.
This also proves that no unverified C4 alternative was discarded.

Choose a lift x of X4. Its four pointed translates x,ux,vx,uvx form the
a-dimensional torsor, with vx,uvx above X5. Let y lie over X1+X2;
then vy lies over X6+X7 and uy=y. The latter two lifts are selfdual
because their underlying orbits are selfdual and each orbit has only
one lift. We have x*=t x, with t either 1 or u.

## 3. Ten tiny candidate based rings, then two

Use basis (1,u,v,uv,x,ux,vx,uvx,y,vy). The three generating products are
forced by the forgetful tensor functor B -> C and u-equivariance:

    x^2 = t + [m+(2-m)u+n v+(2-n)uv]x +2(1+v)y,
    xy  = 2(1+u)(1+v)x +(4+5v)y,
    y^2 = 1+u +(4+5v)(1+u)x +(8+11v)y,

where m,n belong to {0,1,2}. Here u^2=v^2=1 and uy=y.
For example, the relevant products in C are

    X4^2 = 1+2X1+2X2+2X4+2X5+2X6+2X7,
    X4(X1+X2) =4X1+4X2+4X4+4X5+5X6+5X7,
    (X1+X2)^2 =2+8X1+8X2+8X4+10X5+11X6+11X7.

If t=u, taking duals of x^2 forces m=n=1. If t=1, all nine choices
satisfy the based-ring axioms. This small assertion is independently
verified on all tensor entries and associativity equations by
`r1154_rank10.py`; it is not a categorical existence assertion.

The known center dimension field immediately rules out most choices.
In a character with chi(u)=-1, y vanishes and

    x^2=chi(t)+P x,
    P=2(m-1)+chi(v)2(n-1).

For t=1, P=+/-2 produces formal codegrees 16+/-8sqrt(2).
Ostrik's induction theorem would produce a central simple of dimension
2D0/f, outside Q(sqrt(5)). But every central dimension of B belongs
to Q(sqrt(5)), since Z(B)=Z(C) tensor Z(S).
For P=+/-4 the two formal codegrees are 40+/-16sqrt(5), requiring
central dimensions

    15+6sqrt(5),       255+114sqrt(5).

Neither occurs in any of the three source-center patterns, and
multiplication by a simple of Z(S) leaves dimension unchanged. Thus
P must be zero for both choices chi(v)=+/-1, forcing m=n=1.
Only t=1 and t=u remain.

For both residual rings the formal codegrees, with multiplicity, are

    2D0, 2D0', 10,10, 40, 8,8,8,8,8.

The full exact character tables are in `r1154_character_check.json`.
There are FIVE codegrees equal to 8, including the character
u=1,v=-1,x=1,y=0. Counting only the four u=-1 characters would miss one.

## 4. Center duality rules out the all-selfdual branch

For a commutative spherical fusion ring, the simple constituents A_chi
of induction of the tensor unit correspond to its one-dimensional
characters. Their twists are 1 and their dimensions are Dim(B)/f_chi.
Duality takes A_chi to A_{chi^vee}, where chi^vee(b)=chi(b*). This is the
duality compatibility of the usual identification of the endomorphism
algebra of I(1) with the complexified Grothendieck algebra (equivalently,
reverse an annulus labelled by b). In particular, if every based object
is selfdual, each distinguished constituent is selfdual.

In the branch t=1 all ten objects of B are selfdual. The five f=8
characters therefore require five **selfdual**, twist-one simples of
Z(B) of dimension D0/4.

In every source-center pattern the only simples of dimension D0/4 are
A2 and the four packet objects Z0,Z1,Z2,Z3. A2 is selfdual and has twist
1. The packet theorem proves

    twists (i,i,-i,-i),   Z0*=Z1,   Z2*=Z3.

Z(S) has four selfdual invertibles, with twists 1,1,i,-i. Thus the
selfdual twist-one simples of dimension D0/4 in Z(B) are precisely
A2 tensor 1 and A2 tensor the boson: only TWO. The four other twist-one
simples of this dimension come from the Zi tensored with the opposite
semion, and remain nonselfdual. Five required selfdual objects cannot
fit into two available objects. The branch t=1 is impossible.

For t=u, four of the f=8 characters are nonreal and occur in two dual
pairs; the fifth is real. Their duality counts fit the available four
nonselfdual packet objects and one of the two selfdual objects. Hence
this same argument does not exclude the remaining ring.

## 5. The surviving necessary rank-ten ring

The unique remaining based ring in this reduction is

    G=V4=<u,v>,  uy=y,  x*=ux,  y*=y,
    x^2=u+(1+u+v+uv)x+2(1+v)y,
    xy=2(1+u)(1+v)x+(4+5v)y,
    y^2=1+u+(4+5v)(1+u)x+(8+11v)y.

All generators u,v are central. It has full adjoint subring, four
nonselfdual a-dimensional objects, and two selfdual (2a+2)-dimensional
objects. Its tensor appears in `r1154_rank10.json` as t=1,m=n=1, where
**the integer t=1 denotes u** (integer t=0 denotes the tensor unit).

This ring passes the bounded exact zero-spectrum scan. The two-candidate
scan took less than a second including compilation; no long computation
was used. Passing this test is only a necessary condition.

An attempted shortcut through a central-semion indicator product law
was not needed and is not asserted. Nor is a central semion inside
Z(B) treated as a braiding on B or as a proven Deligne decomposition of B.
The standard Morita equivalence does not turn the surviving ring into an
existing model: the starting category C remains hypothetical.

## 6. What is actually still missing

One must either construct a category with the displayed rank-ten ring
and the compatible central boson/semion data that de-equivariantizes to
the exact R1154 tensor, or obtain a categorical obstruction to that ring
in the specific Morita class. Its four nonselfdual objects remove the
most immediate second-indicator parity contradictions. The necessary
formal-codegree, center-dimension, and center-duality constraints above
are consistent for this final branch.

### A complete short second-indicator parity check

The total second indicator is Morita invariant and multiplicative under
Deligne products. Since the semion total is 1+(-1)=0, B must satisfy

    sum_Z dim(Z) nu_2(Z)=0.

The four pointed indicators are (1,1,-1,-1), as follows from their central
lifts in Z(S); all four x-translates are nonselfdual and have indicator
zero. Consequently nu_2(y)+nu_2(vy)=0. The coefficient of vy in y^2 is
11, so odd-multiplicity parity forces nu_2(vy)=+1. Thus necessarily

    nu_2(y)=-1,       nu_2(vy)=+1.

These forced signs are consistent. Indeed, reducing the ring modulo two,

    y^2 =1+u+v(x+ux)+vy,
    y^3 =v+uv+(x+ux)+y,
    y^4 =y^2.

The last equation follows by squaring y^2 in characteristic two: the
squares of 1+u and v(x+ux) vanish, while (vy)^2=y^2. Thus every even
positive power y^{2n} has the first displayed parity, and every odd
power y^{2n+1}, n>=1, has the second. In the even case its odd
selfdual constituents have indicator +1; in the odd case they have
indicator -1, exactly as required. Powers of vy are v^n y^n and pass
by the same calculation. More general palindromic words in selfdual
simples reduce to these powers and a possible central invertible
factor; the paired invertible factors square to 1, so they produce
no further parity contradiction. The total-indicator equation is
also exactly zero with these signs. This gives a uniform check,
not an inference from finitely many low tensor powers.

Thus the honest classification status remains **unresolved**. The new
result is a small and explicit Morita normal form after cancellation of
the pointed anomaly, together with the elimination of all other based
rings arising in this normal form.

## Verification and primary references

Run from this directory:

    python r1154_rank10.py
    python r1154_character_check.py

The first checks all ten ring tensors and their adjoint closures; the
second checks all ten characters of each of the final two rings, their
codegrees, and the dimensions in all three source-center patterns.
`r1154_zero_spectrum.json` records the additional bounded scan, using the
Liu-Palcoux-Ren criterion already implemented in the project.

For induction, its twist-one property, and formal codegrees, see Ostrik,
*Pivotal fusion categories of rank 3*, Theorems 2.5 and 2.13:
https://arxiv.org/abs/1309.4822 .
For the categorical relationship between extensions, equivariantization,
and central Rep(G), see Jones-Morrison-Penneys-Plavnik, *Extension Theory
for Braided-Enriched Fusion Categories*, particularly Section 7:
https://doi.org/10.1093/imrn/rnab133 .
The asserted fusion calculations and the three-pattern dimension tests
are supplied explicitly above and in the exact checkers; they do not
rely on a literature classification of hypothetical categories.
