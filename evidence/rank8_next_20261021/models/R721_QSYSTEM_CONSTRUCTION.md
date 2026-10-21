# R721: the inherited generalized-Haagerup Q-system route

**Theorem.** R8_3_721 is unitarily realized by the category of bimodules over
the inherited Q-system A=1+rho in the C2 de-equivariantization of the known
C8 generalized-Haagerup category.

The independent Gram enumeration and center rank cut are in the sibling
`semion_fermion/construction` evidence. The full fusion tensor is identified
using the proven multiplicity bound and exhaustive census uniqueness below.

## Source category and existing algebra

Use the Z8 generalized Haagerup category of Grossman--Izumi,
*Drinfeld centers of fusion categories arising from generalized Haagerup
subfactors*, arXiv:1501.07679v2, Example 4.4. It satisfies equation (2.22),
so `1+rho` has a Q-system by (2.21). Apply the C2 de-equivariantization in
Section 6. The image is a connected separable algebra A in the resulting
category C. The source has simples `g^i,g^i rho`, 0<=i<4, with

    g^4=1,  g rho=rho g^-1,
    rho^2=1+2 sum_i g^i rho,
    dim(rho)=d=4+sqrt(17).

The category D of A-bimodules exists and is Morita equivalent to C. Its
global dimension is therefore 136+32sqrt(17). Example 6.10 and Theorem 6.8
give the center data used in the independent rank cut. The script
`r721_gi_identification.py` also checks the exact correspondence with
Definition 6.1 and Section 6.1.6 of arXiv:1906.07397v2.

## A uniform cyclic generalized-Haagerup lemma

More generally, let the source be any existing generalized-Haagerup category
for C_(4m) satisfying the Section 6 hypotheses
epsilon_(2m)(h)=(-1)^h and admitting the inherited Q-system 1+rho with
nonzero vertex proportional to t_0. In its C2 de-equivariantization, the
invertible group is C_(2m), and the noninvertible dimension is
d=2m+sqrt(4m^2+1). The Morita dual of the inherited algebra has **trivial
group of invertible objects**.

Indeed an invertible A-bimodule has underlying dimension 1+d. Since d is
irrational and the source simple dimensions are 1 and d, its underlying
object must be g^j+g^k rho. Left and right free-module adjunction, together
with equality of dimensions, identify its respective underlying objects
with A g^j and g^j A. Their noninvertible summands are g^-j rho and
g^j rho. Hence 2j=0 modulo 2m, so j is either 0 or m.

For j=0, the only possibility is an automorphism-twisted copy of A. Its
automorphism is trivial: the nonzero rho*rho-to-1 and rho*rho-to-rho
components require the scalar z on rho to satisfy z^2=1 and z^2=z.
For j=m, conjugation by alpha'_m changes the inherited vertex to
t_(2m) lambda, orthogonal to t_0. The calculation below applies verbatim
with 2 replaced by m and 4 by 2m, and excludes that algebra conjugacy.

This is a uniform construction theorem for each category whose stated
existence and Q-system hypotheses hold. It does not assert existence of
generalized-Haagerup categories for every m.

## The explicit m=2 conjugacy obstruction

We use the explicit endomorphism realization of Section 6, first paragraph
(printed page 37). Write r=rho', a=alpha'_2. The crossed-product unitary
lambda has lambda^2=1 and satisfies

    r(lambda)=lambda,
    alpha'_4=Ad(lambda),
    alpha'_2(t_0)=t_4.

The two isometries t_0 and t_4 lambda are orthogonal elements of
Hom(r,r^2). The inherited Q-system A=1+r has its nonzero r-to-r^2 vertex
proportional to t_0. This is the Q-system from equation (2.21), transported
by the de-equivariantization functor.

Let beta be conjugation by a. The relation alpha'_h r=r alpha'_-h gives

    beta(r)=Ad(lambda) r.

Thus u=lambda is an intertwiner r -> beta(r). Its tensor square is the
identity because r(lambda)=lambda and lambda^2=1. Transporting beta(A)
back to the underlying object 1+r consequently changes its r-to-r^2
vertex to

    beta(t_0) u = t_4 lambda.

It is not proportional to t_0: t_0^* t_4 lambda=0. A unit-preserving
algebra isomorphism on 1+r must be scalar on the simple r summand. Such
an isomorphism can only multiply this vertex by a scalar. Therefore
beta(A) and A are not isomorphic as algebras.

An invertible A-bimodule whose underlying object contains g^2 would be
isomorphic to A tensor g^2 as a left A-module: by adjunction there is a
nonzero map from this free module, and both objects have C-dimension
dim(A). The compatible right action would then identify the algebras
g^2 A g^-2 and A. The preceding calculation rules this out.

An invertible A-bimodule whose underlying object contains 1 is similarly
A with a right action twisted by an algebra automorphism. But Aut(A)
is trivial. A unit-preserving automorphism is scalar z on r; the nonzero
r*r-to-1 and r*r-to-r multiplication components require z^2=1 and z^2=z,
respectively, hence z=1. Thus this bimodule is the tensor unit.

The complete free-bimodule Gram enumeration has possible ranks 6,8,9,11.
Its only extra-invertible possibility surviving the known-center rank cut
is the rank-six branch, where that invertible has underlying g^2 A.
The center rank cut leaves ranks 6 and 8; the preceding argument eliminates
6. The actual Morita dual D therefore has rank eight, with dimensions

    1, a, a, a+1, a+1, 2a+1, 2a, 2a+2,
    a=(3+sqrt(17))/2.

## From the actual dual to the complete fusion census

The forgetful columns of the unique rank-eight Gram factor are written
explicitly in `r721_dual_fusion.py`. If I(X)=A tensor X tensor A, then

    I(X) tensor_A I(Y) = I(X tensor A tensor Y).

The script imposes this identity in all 512 source-product/output
coordinates, together with unit, duality, Frobenius reciprocity and both
rational components of the dimension character. It considers all four
possible duality choices on the two equal-dimension pairs. No commutativity
or upper bound on multiplicity is assumed.

`r721_dual_multiplicity_bound.py` constructs rational dual inequalities
for these necessary linear systems. The certificates prove that every
fusion coefficient in every duality case is at most three. Verification
reconstructs the equations and checks exact rational domination and right
hand sides; floating-point optimization is only a discovery method.

Consequently the actual rank-eight dual occurs in the complete
rank-eight/multiplicity-at-most-three census. The independent verifier
`../r721/census_dimension_crosswalk.py` exhausts all 4,500 cumulative rings
(96 of exact multiplicity one, 877 of exact multiplicity two, and 3,527 of
exact multiplicity three). Exactly one has the mandatory dimension multiset:
R8_3_721. This identifies the entire based ring, because the complete census
contains all based rings within the independently proved rank and
multiplicity bounds. It does not assume that a dimension match by itself
proves a categorical construction.

The census tensor has SHA256

    76e26a815651476dfda5c2aa654f0d1327bdc890e08086cb6dbfe39ef9a1cdc5.

All 512 coefficients of R8_3_721 satisfy the induction/dimension/reciprocity
identities under the dual-basis to census-basis permutation

    [0,1,2,4,6,3,5,7].

This is a construction from an existing Q-system. Modular-data agreement
alone was not used to assume existence of a Lagrangian algebra.

Independent reviews are `../review/R721_CATEGORICAL_REVIEW.md`,
`R721_RANK_INDEPENDENT_REVIEW.json`, and
`../quadratic/r721_bound_review.json`. The coefficient-bound reviewer
independently reconstructs every necessary equation from the Gram factor,
without importing the producer implementation. Both normal and optimized
Python replay the exact certificates.
