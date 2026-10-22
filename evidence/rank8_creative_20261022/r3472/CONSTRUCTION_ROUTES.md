# A common cyclic-parent obstruction for R1768 and R3472

This is a **construction-route obstruction**, not an exclusion of either
rank-eight fusion ring. It applies to a direct ordinary
de-equivariantization of a cyclic near-group category. It neither assumes
that such a parent has been constructed nor excludes noncyclic parents,
other Morita representatives, or generalized-Haagerup parents.

## A cyclic stabilizer divisibility lemma

Let C be a complex fusion category, let H be a cyclic subgroup of its
invertible objects, and let X be a simple object satisfying X h = X for all
h in H. Suppose H lifts to a Tannakian pointed subcategory of Z(C), with
fully faithful forgetful image in C. Let A be its regular algebra and let
D=C_A be the ordinary de-equivariantization. Then

    FPdim_C(X) / |H| is an algebraic integer.

Here the Tannakian group is the character group of H; it is again cyclic of
order |H|. The algebra A has underlying object the sum of the distinct h in
H. A-module structures supported on copies of X are described by a twisted
group algebra of H: choose isomorphisms X h -> X, and their associativity
discrepancies define a scalar two-cocycle. Every such two-cocycle on a cyclic
group over C is a coboundary. Indeed, a projective generator T obeys
T^|H|=lambda; rescaling T by a |H|-th root of lambda gives T^|H|=1.
The twisted group algebra therefore has exactly |H| one-dimensional simple
modules. Consequently D has |H| simple objects M whose underlying object
in C is X.

The dimension normalization is

    FPdim_D(M) = FPdim_C(U(M)) / FPdim_C(A).

One can see the normalization without assuming pivotality. The positive
module dimension vector FPdim_C(U(M)) and the vector FPdim_D(M) are
proportional: both satisfy the C-module eigenvector equations for the free
tensor functor C -> D. The C-module category is indecomposable, since this
functor is dominant and D is a fusion category. Evaluating at the tensor
unit A of D gives proportionality constant FPdim_C(A)=|H|. Thus each of the
above simple modules has dimension FPdim_C(X)/|H|, which must be an
algebraic integer. This proves the lemma. In contrast, dimensions in an
arbitrary module category do not have this algebraic-integrality
normalization; the fusion structure supplied by centrality is essential.

The categorical construction and its fully faithful hypothesis are those
of EGNO, Theorem 8.23.3 and Definition 8.23.4. The projective-stabilizer
description is the same elementary mechanism as Remark 4.15.8. No unitary
center formula is required for this argument.

## The uniform failed scalar parent

In particular, for a cyclic near-group category NG(C_n,n), an ordinary
de-equivariantization of order h necessarily satisfies **h^2 divides n**.
Indeed its unique noninvertible has dimension d with d^2=n+nd and
quadratic norm -n; the lemma makes d/h integral, whose norm is -n/h^2.
For n>=1 the number n^2+4n lies strictly between (n+1)^2 and (n+2)^2
(with the lower inequality still strict at n=1), so the quadratic norm is
genuine. As the rational norm of an algebraic integer it must be integral.
The image of the de-equivariantizing representation category is cyclic
pointed by the argument below. This is a dimension-theoretic version of
the cyclic isotropic-subgroup restriction, valid without unitarity.

For any integer g>=1, set

    delta = g + sqrt(g^2+1),   delta^2 = 1+2g*delta,
    D_g = g*(1+delta^2),      n=4g^2.

A near-group category NG(C_n,n), if it exists, has noninvertible dimension
rho=2g*delta and global dimension 4g*D_g. A direct ordinary
de-equivariantization reducing this dimension to D_g would have group order
4g. Its pointed image is the unique cyclic subgroup H of order 4g in C_n.
To justify that no nonpointed Tannakian image is missed, every simple of
Rep(K) has integer dimension; the only integer-dimensional simples of this
near-group category are invertible. A fully faithful tensor image is
therefore pointed, so K is abelian and its character group embeds in the
cyclic group C_n. Hence this image really is cyclic.

The unique noninvertible is H-stable, so the lemma requires

    rho/(4g) = delta/2

to be an algebraic integer. Its minimal polynomial over Q is

    x^2 - g*x - 1/4,

and its norm is -1/4. Since g^2+1 is not a square for g>=1, this is a
genuine quadratic norm and proves nonintegrality. Thus **no such direct
ordinary de-equivariantization exists**, for any categorification of this
cyclic near-group fusion ring. No existence theorem for the parent is
used in the exclusion.

| Target scalar profile | g | Cyclic parent | Required division | Forced simple dimension | Norm |
|---|---:|---|---:|---|---:|
| R8_3_1768: 444+72 sqrt(37) | 6 | NG(C144,144) | 24 | (6+sqrt(37))/2 | -1/4 |
| R8_3_3472: 700+490 sqrt(2) | 7 | NG(C196,196) | 28 | (7+5 sqrt(2))/2 | -1/4 |

`verify_construction_routes.py` checks these identities and norms with exact
rational arithmetic. Its receipt is `construction_routes.json`.

For the unitary near-group centers computed by Evans--Gannon, Section 4.3,
equation (4.49), the pointed twist is q(x)=chi(x,x). A nondegenerate cyclic
bicharacter is chi(x,y)=exp(2 pi i*a*x*y/n), gcd(a,n)=1. The generator g of
H has q(g)=exp(2 pi i*a/4), hence twist i or -i rather than 1. This agrees
with the preceding obstruction, but the proof above does not transfer
unitary formulas to an unverified nonunitary family.

## What remains possible

The generalized-near-group profile relevant to the first line has six
invertibles and six noninvertibles of dimension 6+sqrt(37). The second line
has seven and seven, with noninvertible dimension 7+5 sqrt(2). In each case
the formal uniform multiplicity-two relation is

    rho^2 = 1 + 2*sum_(h in G) h*rho,   |G|=g.

This is not the ordinary near-group relation with just one noninvertible.
Neither the profile nor the uniform fusion-rule ansatz supplies an
associator or a Morita identification with a given rank-eight tensor.

A generalized-Haagerup C_(2g) parent followed by an ordinary C2 quotient has
the right global dimension. The known-sign discussion in Grossman--Izumi,
Section 6, permits the relevant bosonic sign for g=6, while its known g=7
sign is fermionic. Their statement epsilon_n(1)=-1 is explicitly about
known examples, and their additional Q-system hypothesis must be retained.
It is not a universal obstruction to C14 parents. Their supplied cyclic
solutions cover C6, C8 and C10, not C12. No explicit C12 solution or
rank-eight ring identification was obtained here. The two R1768 rank-12
module factors retained in the earlier pointed-associator analysis are
still conditional possible Morita routes, not constructed module
categories.

Noncyclic near-group parents remain open. In that setting a stabilizer may
have nontrivial projective irreducibles of dimension greater than one, so
the cyclic splitting argument must not be reused. Ordinary module-category
Morita changes likewise are not ruled out by the direct quotient lemma.

Recent sources supply worthwhile construction leads but no target model:

* He--Liu--Lu--Palcoux--Ren, arXiv:2610.11652v1, Theorems 2.3 and 2.10,
  states spherical reconstruction and a cyclic scalar construction; its
  abstract states pseudo-unitary Galois conjugates at every cyclic order.
  General unitarity is conjectural there. This new preprint claim is not
  independently verified here and is not needed for the obstruction.
* Gannon--Schopieray--Yadav, arXiv:2609.25185, constructs the odd-order cyclic
  HI family. Its near-group equivariantizations have group C_N times C_N
  for odd N. That theorem does not construct the required even-order C12
  or C14 parent.
* Radchenko--Wheeler, arXiv:2609.21892, studies finite quantum dilogarithms
  and Izumi polynomial solutions. Applying these data to a noncyclic
  parent here would still require checking the relevant bicharacter,
  associator, Tannakian lift, quotient fusion rules and Morita match.

Primary sources:

* https://math.mit.edu/~etingof/egnobookfinal.pdf
* https://arxiv.org/html/1208.1500v1 (Section 4.3, (4.49))
* https://ems.press/content/serial-article-files/36923 (Sections 2 and 6)
* https://arxiv.org/html/2610.11652
* https://arxiv.org/pdf/2609.25185
* https://arxiv.org/pdf/2609.21892

Both R1768 and R3472 remain unresolved. These results remove a tempting
dimension-matched cyclic construction, while retaining the genuine gaps
in the generalized-Haagerup and noncyclic-parent approaches.
