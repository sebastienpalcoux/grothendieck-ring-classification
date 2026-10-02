# The four dimension-48 cases: an odd module forces an S4 Morita neutral

**Conclusion: none of the four rings admits a fusion category over the
complex field.** The independent proof audit and normal/optimized exact
receipts are stored beside this file.

This argument applies to R158, R186, R579 and R682. It uses no pivotal
structure and no explicit center enumeration.

## 1. Source structure and the first prime descent

Each ring has type `1^4,2,4,(2sqrt(3))^2`, of FP dimension 48. Its
integral simples form the even component D, of FP dimension 24, and
the two irrational simples form the odd component M of a faithful C2
grading. The common neutral ring has basis `1,a,b,c,Y,Z`, with V4 units,
all units fixing Y and Z, and

    Y*=Y, Z*=Z,
    Y^2=1+a+b+c,
    YZ=ZY=2Z,
    Z^2=1+a+b+c+2Y+2Z.

In particular D_ad=D and U(D)=1. Its source-bound checker validates
the entire ring and grading, rather than just this abbreviated display.

Solvability of dimension 24 and U(D)=1 force D to be a prime
equivariantization. Inv(D)=V4 rules out C3, so

    D=E^{C2},   FPdim(E)=12.

The canonical sign epsilon is one of the three nontrivial units. Since
it fixes Y and Z, the de-equivariantized ring E has type `1^4,2^2`.
The outer involution swaps the two 2-dimensional simples coming from Z,
and swaps two of the four units, leaving two fixed. Its Inv(E) is V4 or
C4.

There is a tiny exact ring classification with these hypotheses. All
associative rank-six fusion rings of type `1^4,2^2` with such an
involution are

    X*=Y, X^2=2Y, Y^2=2X, XY=sum_{g in A}g,
    gX=X, gY=Y,  A=V4 or C4.

For completeness, the classifier exhausts the two groups A of order
four, both actions of A on the two nonunits (trivial or transitive),
both dualities (self-dual pair or exchanged pair), and all nonnegative
nonunit product coefficients allowed by the dimension-four product.
Duality relates the right unit action to the inverse left action through
the dual permutation of the two nonunits. Since S2 is abelian and each
action has exponent two, the two unit actions coincide. The classifier
nevertheless enumerates XY and YX independently, allowing an oriented
noncommutative candidate tensor. Reciprocity fixes the unit coefficients.
The 100 oriented candidates yield six valid based rings and exactly two
eligible R_{3,A} rings. It checks every
associativity equation and every possible outer involution. The only
self-dual alternatives have no involution swapping X and Y: their squares
are equal and contain exactly one of X,Y. The output above is complete.

Jordan--Larson Theorem 1.4 excludes the C4 case: the group in R_{3,A}
must have an even multiplicity of every cyclic prime-power factor.
Consequently E has ring R_{3,V4}. It is faithfully C3 graded over its
pointed subcategory B. Each nonneutral component has rank one and
therefore trivializes the associator of B. Thus `B=Vec_V4`.

## 2. De-equivariantizing the odd module

The odd component M is a genuine D-module category. Let
`A_epsilon=1+epsilon` be the central regular algebra of Rep(C2).
De-equivariantizing modules gives the E-module category

    M_epsilon = M_{A_epsilon}.

If epsilon swaps the two simples of M, this category has rank one.
If epsilon fixes both simples, it has rank four: each fixed simple has
two algebra-module structures, since H^2(C2,C*)=0. These are the only
possibilities, independent of equivariant coherence.

There are exactly six indecomposable Vec_V4 module categories:

| Stabilizer and cocycle | Number of classes | Rank |
| --- | --- | --- |
| 1 | 1 | 4 |
| V4, trivial or nontrivial H^2 class | 2 | 1 |
| each order-two subgroup, trivial cocycle | 3 | 2 |

Every one has pointed dual. For the rank-two classes the dual is
the untwisted Vec_V4, by the direct-product decomposition of V4.

The C3 action of E on these module classes sends the regular rank-four
class to the rank-one X component and then to the distinct rank-one Y
component. Thus the ranks 4,1,1 form a three-cycle. On the remaining
three rank-two classes it either fixes them or cycles them. Every
nontrivial orbit of module classes has total rank at least six.

Apply Galindo's Clifford theorem, Proposition 4.1 and Theorem 1.1, to
M_epsilon as an E-module. The indecomposable B-submodule categories are
permuted by C3 with the stated equivalences. A category of total rank
one or four cannot contain a nontrivial orbit. Hence rank one is
impossible, and rank four consists of two fixed rank-two B-submodule
categories. The group C3 cannot interchange two actual summands; each
is an actual rank-two E-module extension N of a rank-two B-module.

## 3. E is Morita equivalent to the untwisted Vec_A4

Use one of these coherent module extensions N. Galindo Theorem 1.3
makes the dual of the **induced** module `E tensor_B N` a semidirect
C3 product of the pointed dual `B*_N=Vec_V4`. The original rank-one
C3 component is nontrivial in BrPic(B), so the transported action is
nontrivial of order three.

The tensor autoequivalence classes of Vec_V4 form
`H^2(V4,C*) rtimes Aut(V4)=C2 times S3`. An order-three element has
trivial component in the C2 kernel, and acts on V4 by an order-three
automorphism. Choose the tensor functors to be the pure group action.
The remaining action coherence is classified by
`H^2(C3,V4-hat)=0`, since the orders are coprime. Therefore the action
is equivalent to this strict group action. Its semidirect product is
the **untwisted** Vec_A4. No unaccounted C3 associator twist remains:
Galindo's theorem provides a semidirect product, including its graded
tensor section, rather than a general crossed product.

Thus E is Morita equivalent to Vec_A4.

## 4. D is Morita equivalent to Vec_S4^omega

The equivariantization D is Morita equivalent to the crossed product
`E rtimes C2`. Transport this C2 extension through the preceding Morita
equivalence to a C2 extension T of Vec_A4.

The center of Vec_A4 has exactly three Lagrangian subcategories,
corresponding to the normal abelian subgroups 1 and V4 and the two
cocycle classes on V4. Nikshych--Riepel Proposition 7.6 and Section 8.3
put all three in the Brauer--Picard orbit of the canonical Rep(A4).
Consequently each corresponding pointed Morita dual is the untwisted
Vec_A4. For a direct verification one may also note
that A4 is V4 rtimes C3 and the nontrivial H^2(V4) class extends to A4,
so the subgroup module's cocycle is removed by a tensor autoequivalence.

A C2 action on this set of three Lagrangians fixes at least one. Its
corresponding pointed module N is invariant. Galindo Proposition 5.3
explicitly states that the dual of the induced module
`T tensor_{Vec_A4} N` is a C2 crossed product with neutral component
`(Vec_A4)*_N=Vec_A4`. It is therefore pointed and gives a Morita
realization of T compatibly with its C2 grading. This step needs only
invariance of N, not an additional coherent extension of N. Its
invertible group G fits into

    1 -> A4 -> G -> C2 -> 1.

As A4 is centerless and Out(A4)=C2, the group G is either S4 or
A4 times C2. In the latter case the pointed center contains at least
six invertibles supported at the identity: the six ordinary linear
characters of G. This remains true for any associator omega.

Morita equivalence identifies this center with Z(D). The forgetful
map `Inv(Z(D))->Inv(D)` has kernel `Hom(U(D),C*)=1`, so is injective.
But Inv(D) has order four. Therefore the six characters exclude
G=A4 times C2. We conclude that D is Morita equivalent to
`Vec_S4^omega` for some omega.

## 5. Integral extensions give the contradiction

The only normal abelian subgroups of S4 are 1 and its normal V4;
their orders are squares. The extension-integrality lemma from
`R53_R93_GENERAL_PROOF.md` therefore makes every graded extension of
D integral, for arbitrary omega. A putative census category is a C2
extension of D but has two simples of FP dimension `2sqrt(3)`.
This contradiction excludes all four rings over the complex field.

## Primary sources and audit points

- ENO, https://arxiv.org/pdf/0809.3031: solvability and prime descent.
- Jordan--Larson, https://arxiv.org/pdf/0812.1603, Theorem 1.4:
  the R_{3,C4} nonexistence criterion.
- Galindo, https://arxiv.org/pdf/1010.5283, Proposition 4.1,
  Proposition 5.3, Theorems 1.1--1.3: actual module extensions, induced-module dual,
  and stable pointed-module criterion for group-theoretical extensions.
- Nikshych--Riepel, https://arxiv.org/pdf/1309.5026, Proposition 7.6 and Section 8.3:
  the three A4 Lagrangians and their action; the extension of the
  nontrivial V4 cocycle is established by the restriction-isomorphism
  statement there.
- ENO, https://arxiv.org/pdf/0909.3140, Corollary 3.13 and Theorem 1.3:
  Morita transport of the entire graded extension.
- Gelaki--Naidu, https://arxiv.org/pdf/0709.4326, Theorem 4.1:
  the identity Rep(H) block in the arbitrary twisted bimodule criterion.

Independent audit should verify module de-equivariantization, the rank
orbit count, strictification of the C3 action, and the pointed Morita
group in the stable-Lagrangian step. Exact source, finite ring exhaustion
and finite group checks are separate from these categorical statements.
