# Integral rank-eight decisions: recovered proofs and exact models

All exclusions below concern arbitrary fusion categories over the complex
field. No pivotal, spherical, pseudo-unitary, unitary or braided hypothesis
is used. Existence claims below give unitary fusion categories. The separate
R575 construction is in `r575/`. R694 is proved in the adjacent complete
`R694_DIM28_GRADING_PROOF.md`.

`verify_integral.py` loads the actual census, checks its published digest,
validates each ring, constructs its exact positive dimension character,
checks the relevant subcategory/module/adjoint data, and independently
reconstructs all512 coefficients of each of the five models described here.
No model tensor is copied from the census or from a stored certificate.
Checks use explicit exceptions, including in optimized Python.

## The rank-one module lemma

Let D be a fusion category and M an indecomposable D-module category with
one simple object. As an abelian category M is equivalent to Vec. Its module
action is consequently a tensor functor D -> End(Vec)=Vec, necessarily
exact and faithful; thus D has a fiber functor and is Rep(H) for a
semisimple Hopf algebra H. The dual category Fun_D(M,M) is Rep(H*) (up to
the harmless opposite convention).

If M is moreover an invertible D-D bimodule, its right action identifies
this dual tensor category with D. In a faithful group grading, every
homogeneous component is such an invertible bimodule. These statements
require no pivotal structure. They follow from reconstruction and the
standard characterization of invertible module categories; see EGNO,
Tensor Categories, Chapters7 and8. A rank-one homogeneous component is
also explicitly discussed in Dong--Chen--Wang, arXiv:2109.08787, Lemma2.1.

## R41, R86 and R162: the dimension16 Hopf dual obstruction

The source checker exhibits a faithful C2 grading with dimension16,
rank7 neutral category of type1^4,2^3 and a single dimension4 odd object.
The odd square is the regular neutral object. The lemma supplies a
semisimple Hopf algebra H of dimension16 with both Rep(H) and Rep(H*)
having four invertibles. Neither H nor H* can be a group algebra or its
dual: a group algebra has16 grouplikes and its dual has16 one-dimensional
representations. Kashina's classification, Theorem1.2 and Table1 of
arXiv:math/0004114, leaves only the self-dual Hopf algebra HC:sigma1.
Its representation fusion ring is Rep(D16), with V4 invertibles and
self-dual2-dimensional simples.

R41 and R86 have an invertible of order4, whereas R162 has a pair of
non-self-dual2-dimensional neutral objects. Neither invariant matches
Rep(D16). Therefore all three rings are generally excluded.

## R140: a cyclic-grouplike fiber-functor obstruction

The census indices[0,1,2,3,7] form a dimension8 subcategory D with
invertibles[0,1,2,7]=C4 and a dimension2 object E, whose square is the
sum of the four invertibles. Each of indices4,5,6 forms a rank-one left
D-module category: gM=M for invertible g, and EM=2M. Hence D has a
fiber functor and is Rep(H) for a semisimple Hopf algebra H of dimension8.
Its group G(H*) is cyclic of order4. Kashina's Theorem1.1 for prime-power
Hopf dimensions says that a semisimple Hopf algebra with cyclic grouplikes
must be the group algebra of the full cyclic group. Applied to H*, it
would give H*=C[C8], with eight grouplikes, a contradiction. This proof
does not presume that all categories of dimension56 are group-theoretical.

## A descent lemma used for R697 and R808

An integral fusion category E of type1^2,2^8 and dimension34 has E_ad=E.
Indeed the dimension of E_ad is an integer divisor of34. Dimension1
would make E pointed. Dimension17 would make E_ad pointed of prime
dimension, supplying17 invertibles although E has only two. Dimension2
is also impossible: X X* for a dimension2 simple would then be supported
on two invertibles, each with multiplicity at most1, although its total
dimension is4. The multiplicity assertion follows from
Hom(g,X X*)=Hom(gX,X).

Exactly the same argument for type1^3,3^10 and dimension93 excludes
proper adjoint dimensions1,3,31: prime dimension31 supplies too many
invertibles, and dimension3 cannot support a dimension9 product with
invertible multiplicities at most1.

Solvability and the prime cyclic extension/equivariantization description
of ENO imply that these categories are respectively
(Vec_C17^omega)^C2 and (Vec_C31^omega)^C3. An extension is impossible
because the adjoint category is the whole category. The other prime
equivariantization would supply more invertibles than exist. The action
on the underlying cyclic group is nontrivial, since a trivial action
would produce only invertibles. The pointed associator and possible
coherence do not change this conclusion.

For either E, U(E)=1. Two central structures on the same invertible
differ by a tensor automorphism of Id_E; this group is Hom(U(E),C*), so
the central lift is unique. Thus any outer tensor action preserves the
canonical central Rep(C2) or Rep(C3). Equivariantizing successively and
de-equivariantizing this invariant subcategory combines the actions into
an action of a group H fitting the corresponding exact sequence. This
is the standard equivariantization/de-equivariantization correspondence,
and embeds Rep(H) in the final category. The tensor action on the
pointed cyclic group restricts to the original nontrivial inner action.

## R697: dimension68

ENO's p^a q^b theorem gives solvability. The census adjoint category is
the whole category, so the last operation is a prime equivariantization.
It cannot be C17 because there are only four invertibles. Hence
C=E^C2. The sign invertible fixes every nonunit; orbit/stabilizer
dimensions therefore force E to have type1^2,2^8, dimension34. The
previous lemma applies. Combining the outer involution with the unique
inner central C2 gives H of order4. Its representation subcategory
exhausts the four invertibles, whose group is V4; thus H=V4.

Every homomorphism V4 -> Aut(C17)=C16 has image of order at most2.
Consequently nonzero orbits have size at most2. If the image has order2,
their stabilizer is cyclic of order2, whose projective irreducibles are
one-dimensional. If the action is trivial, projective representations
of V4 have degree at most2. In every case nonunit equivariant dimensions
are at most2. The census has only dimension4 nonunits, a contradiction.

## R808: dimension186

ENO Theorem9.2 makes an integral category of dimension2*3*31
group-theoretical. Its underlying group of order186 has a normal
Sylow31 subgroup (the Sylow count divides6 and is1 modulo31), with
solvable quotient of order6. Hence the group and its pointed category
are solvable. Solvability is invariant under Morita equivalence, so C
is solvable.

Again C_ad=C forces a final equivariantization; the two invertibles rule
out primes3 and31. Thus C=E^C2. Since the sign fixes every nonunit,
orbit/stabilizer dimensions give E of type1^3,3^10 and dimension93:
the dimension2 object descends to two swapped invertibles, and the five
dimension6 objects descend to ten dimension3 objects. The descent lemma
gives E=(Vec_C31^omega)^C3.

Combining the actions gives a group H of order6. Its representation
subcategory has type1^2,2, so H=S3 rather than C6. But every map
S3 -> Aut(C31)=C30 factors through its abelianization and kills the
normal C3. This contradicts the nontrivial C3 action already present
in E. Thus R808 is generally excluded.

## Four strict pointed equivariantizations

Use Vec_A with trivial associator and the indicated literal permutation
of its graded Hilbert spaces; it gives a strict unitary cyclic action.
The resulting equivariantization is a unitary category:

| Ring | A | cyclic group | generator on A |
|---|---|---|---|
| R244 | C4^2 | C3 | (x,y) -> (-y,x-y) |
| R289 | C2^4 | C3 | (x,y,z,w) -> (y,x+y,w,z+w) |
| R143 | C17 | C4 | x -> 4x |
| R179 | C2^4 | C5 | (x,y,z,w) -> (w,x+w,y+w,z+w) |

All nonzero orbits are free. Order the invertibles by the cyclic
stabilizer characters, then the nonzero orbits lexicographically by
their least member. For nonzero orbits O,P, the coefficient at a
nonzero orbit Q is the number of pairs(a,b) in O*P with a+b=q for
one q in Q. The zero-pair space is a direct sum of regular cyclic
representations, so each invertible coefficient is the zero-pair count
divided by the group order. This formula reconstructs all fusion
coefficients independently of the census. The exact maps are:

- R244: [0,1,2,3,7,4,5,6].
- R289: [0,1,2,3,4,5,6,7].
- R143: [0,1,7,2,3,5,6,4].
- R179: [0,1,4,3,2,5,6,7].

## R237: the affine semilinear group on F8

Let G=AGammaL(1,8), of order168, with elements(v,a,t) in
F8*(F8^*)*C3 acting by x -> v+a*x^(2^t). Multiplication is
(v,a,t)(w,b,u)=(v+a*w^(2^t),a*b^(2^t),t+u).
The representation category of this finite group is unitary.

Write F8=F2[z]/(z^3+z+1), choose generator z of its multiplicative
group, and use zeta21, so zeta3=zeta21^7 and zeta7=zeta21^3.
The three linear characters are zeta3^(s*t). The two degree3 characters
are inflated from F8^* semidirect C3 and are zero for t!=0; for t=0
their values are sum_(e in O) zeta7^(e*log_z(a)), with
O={1,2,4} or{3,5,6}. They arise by inducing the two nontrivial
Frobenius orbits of characters of C7.

The three degree7 characters are induced from the stabilizer C3 of a
nontrivial additive character of F8 and are
chi_s(v,a,t)=zeta3^(s*t) *
sum_(r!=0, a*r^(2^t-1)=1) (-1)^Tr(v/r).
This follows directly from the induced-character formula. The checker
evaluates these actual characters on all168 group elements in the exact
field Q(zeta21), proves64 orthogonality identities and completeness
1^2+1^2+1^2+3^2+3^2+7^2+7^2+7^2=168, and computes every tensor
coefficient by the usual character inner product. The basis map
[0,1,2,5,6,7,4,3] gives exactly R237.

## Primary references

- Kashina, Classification of semisimple Hopf algebras of dimension16,
  arXiv:math/0004114, Theorems1.1--1.2 and Table1.
- Etingof--Nikshych--Ostrik, Weakly group-theoretical and solvable fusion
  categories, arXiv:0809.3031, Definition1.2, Propositions4.4--4.5,
  Theorems1.6 and9.2,
  and the Morita invariance and prime cyclic construction results.
- Burciu--Natale, Fusion rules of equivariantizations of fusion categories,
  arXiv:1206.6625, orbit/stabilizer formula in Section2.
- EGNO, Tensor Categories, https://math.mit.edu/~etingof/egnobookfinal.pdf,
  module categories, reconstruction, and equivariantization.
- Dong--Chen--Wang, arXiv:2109.08787, Lemma2.1.
