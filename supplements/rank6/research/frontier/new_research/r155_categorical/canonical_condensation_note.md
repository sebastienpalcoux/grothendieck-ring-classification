# The canonical dimension-eight local condensation of profile 296

This is a necessary structural consequence, not an existence or exclusion
theorem for R6_4_155. Work in the positive spherical representative and use
the frozen notation: Z(C)=Semion tensor B, dim(B)=8b^2, fermion f, and the
restricted adjoint algebra E=1+A+L in B, with dimensions 1,b-1,b and twists
all equal to one. The first two summands are even for f-monodromy, while L
is odd and fL=L.

The even part E0=1+A is a connected etale subalgebra of E, of dimension b.
Indeed the f-monodromy grading gives an algebra involution of E, and E0 is
its invariant subalgebra. In characteristic zero the invariant algebra is
separable. Thus the modular local-module category

    K = B^0_(E0)

has dimension eight. The algebra E, regarded as an algebra over E0, has
dimension two. Its nonunit summand ell has underlying B-object L, so it is
simple, local, and of dimension one. Consequently ell is a boson of order
two.

The free module f0=f tensor E0 is a distinct invertible local module of
twist -1: f centralizes E0, and the underlying objects E0=1+A and
fE0=f+fA are different. Since ell is invertible, f0 ell differs from ell.
Nevertheless both have underlying B-object L because fL=L. Local-module
twists are inherited from B, so ell and f0 ell both have twist one.

The four invertibles 1,f0,ell,f0 ell therefore form the nondegenerate toric
code category, with twists 1,-1,1,1. Its modular centralizer in K has
dimension two. Connected-etale condensation preserves multiplicative
central charge. Since B has central charge exp(-pi i/4), the remaining
dimension-two factor is Semion^rev. Hence

    B^0_(1+A) = ToricCode tensor Semion^rev

as braided categories with their positive ribbon structures.

This agrees with the general intermediate-algebra picture: 1+A is the
part of the adjoint algebra corresponding to the pointed subcategory of C,
whose associator is Semion tensor Vec(C2). It does not construct B, prove
that its remaining modular data exist, or force a coherent action
exchanging X and Y.

In fact the canonical action obtained here cannot be the desired exchange
action. Write D=B_(E0) for all E0-modules. The central boson ell gives
D_(C2)=B_E=C, so D is a C2-equivariantization of C. The two odd simples of B
of dimension d forget individually to X and Y. A free E-module is isomorphic
to its twist by the algebra involution of E, hence this induced action fixes
X and Y. It also fixes all four invertibles: any tensor autoequivalence of C
preserves the unique central lifts and their canonical positive twists
1,-1,i,-i, which distinguish the four invertibles. All six simple objects
of C are consequently fixed by this C2 action. Since H^2(C2,C*)=0, each
has two equivariant structures. Thus D has rank twelve, eight invertibles,
and four simples of dimension d. It is not the proposed near-group category
with eight invertibles and a unique noninvertible of dimension 2d.

This also checks dimensions: dim(D)=8b=2 dim(C), and the displayed simple
dimensions sum in squares to 8+4d^2=2 dim(C).

## The canonical rank-twelve category splits

In fact D is tensor equivalent to C tensor Rep(C2). Here is a proof that
does not assume that an action fixing simples is monoidally trivial.

The local category K embeds fully faithfully into D and already supplies
all eight invertibles. The center decomposition

    Z(D) = B tensor K^rev

has precisely sixteen invertibles. Its forgetful homomorphism onto Inv(D)
is surjective because the canonical central lift of K supplies all eight
invertibles of D. Its kernel thus has order two. This kernel is
Aut_tensor(Id_D), or the character group of the universal grading group U.

Every component of the universal grading has the same Frobenius--Perron
dimension. If a component contains a invertibles and c noninvertibles,
then comparison of the irrational coefficients in

    a+c d^2 = (16+32d)/|U|,    d^2=2+8d,

gives c=4/|U|. Hence |U| divides four. Groups of order dividing four are
abelian, so their character group has the same order. Since that character
group has order two, U=C2. The adjoint component D_ad has four invertibles
and two noninvertibles.

Let F:D->C be the de-equivariantization. The two noninvertibles in D_ad
cannot both map to X: their tensor-square would then have an image
containing Y, although no D_ad simple maps to Y. Likewise both cannot map
to Y. Thus one maps to X and one to Y. Their products, using the displayed
R155 rules, require all four invertibles 1,h,g,hg to occur as images of
the four invertibles in D_ad. The restriction F:D_ad->C is therefore
bijective on simples, and hence a tensor equivalence.

The kernel boson ell is outside D_ad, since otherwise two distinct
invertibles 1 and ell in D_ad would have the same image under F. Its
central structure gives a fully faithful tensor-product functor

    <ell> tensor D_ad -> D.

The two factors have trivial intersection and their dimensions multiply
to dim(D), so this is an equivalence. Since ell is an order-two boson,
<ell> is Rep(C2) as a fusion category. This proves the stated splitting.

## Fully determined local branching

Let M1,M2 be the dual pair of B-simples of dimension 1+2d and twist -i;
write N1,N2=fM1,fM2, of twist i, and let L' be the second odd b-dimensional
simple, of twist -i. In the order

    1, f0, ell, f0 ell, s, f0 s, ell s, f0 ell s

for K=ToricCode tensor Semion^rev, its eight restriction columns to B are

    1+A; f+fA; L; L; M1+M2; N1+N2; L'; L'.

The first four were proved above. For the remaining four, the twists are
-i,i,-i,-i. The i-twist column has dimension b and must be N1+N2:
the only i-twist B-simples are N1,N2, and self-duality of every K-simple
rules out 2N1 and 2N2. Its f-translate similarly gives M1+M2. The two
remaining -i columns cannot also be M1+M2, since their f-translates would
give further i-twist simples in K. They therefore have underlying L'.

Consequently the branching matrix is supported entirely on the ten low
B-simples {1,f,A,fA,L,L',M1,M2,N1,N2}. The modular branching identity
S_B N=N S_K and its modular-invariant form with NN^T therefore involve
only low S rows or columns. They impose no direct equation on an entry
whose row and column both lie outside these ten objects. In particular,
this branching identity alone cannot determine the outstanding high-high
S block. The additional all-module fusion data would still be needed.

The categorical inputs are the standard connected-etale local-module
dimension formula, transitivity of algebra extensions, preservation of
central charge, and Muger decomposition. Primary references are Davydov,
Muger, Nikshych, Ostrik, *The Witt group of non-degenerate braided fusion
categories*, arXiv:1009.2117, and Drinfeld, Gelaki, Nikshych, Ostrik,
*On braided fusion categories I*, arXiv:0906.0620.
