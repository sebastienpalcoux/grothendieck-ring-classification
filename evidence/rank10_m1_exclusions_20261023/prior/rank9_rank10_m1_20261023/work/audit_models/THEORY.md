# Positive-model audit

## Outcome and exact scope

The 84-case positive baseline survives this audit. There are 79 inputs with
stored model tensors, one additional Haagerup--Izumi(C5) input, and four
additional inputs realized by the Liptrap phase certificates. No numerical
dimension-profile match is used as a categorification certificate.

`verify_models.py` independently checked every coefficient in all 133 distinct
stored model receipts, including the full source hashes and basis bijections.
It also replayed all 27 C2 zest recipes, all eight SU(2)_4 central-extension
recipes, six cyclic TY equivariantization recipes, and the Ising-square
subextension. `selected_models.json` retains one preferred description per
input instead of an accumulation of redundant alternatives.

The Liptrap verifier was rerun: all 11 affirmative feudal systems satisfy
the defining identities exactly, and all 88 nontrivial recoupling blocks are
unitary. The HI(C5) model was also independently rematched in all 1000
coefficients. These checks reproduce the earlier positive evidence; they
do not imply novelty of the categories.

Standard constructions (pointed and representation categories, ordinary TY,
SU(2) and PSU(2), odd metaplectic categories, Deligne products) rely on their
established existence theorems, not on a fresh pentagon solve. Legacy labels
LPR-12 and LPR-24 refer to the unitary dimension-12 and dimension-24 rank-five
models in Liu--Palcoux--Ren, LMP112 (2022), 54. These names should be expanded
in a final report; the repository's generic reference `DP5 Theorem 1.1` alone
is not an adequate primary citation.

## C2 zesting is coherent

Let C be a unitary braided fusion category with a C2 grading d and let h be
an invertible object of order two in the neutral component. The recorded
fusion rule is

    X star Y = X tensor Y tensor h^(d(X)d(Y)).

The braiding supplies a central lift of h, so lambda(a,b)=h^(ab) is an
invertible-object 2-cocycle in the neutral center. The scalar obstruction to
associative zesting lies in H^4(C2,U(1))=0. Consequently the construction has
a coherent unitary associator. This is the associative-zesting theorem of
Delaney--Galindo--Plavnik--Rowell--Zhang; it does not assert that the new
category is braided.

For the bosonic/fermionic involutions used here, one can take the pointed
associator on <h> trivial. The sole potentially nontrivial obstruction value
is c(h,h)=+1 or -1 at (1,1,1,1). Taking the normalized scalar cochain with
nu(1,1,1)=1 or i, respectively, cancels it. All phases have modulus one.
The tensor verifier checks neutral degree, centrality at ring level,
order two, and the grading and multiplication formula. The central lift and
scalar coherence come from the braided base categories and this argument.

Every braided base used by the script is legitimate: elementary-abelian-2
TY categories admit braided unitary realizations; the script excludes
TY(C4) and the two LPR exceptions from this source list. The other bases are
standard braided quantum-group, representation, pointed, product, or
permutation-equivariantization categories. Redundant zest descriptions can
be dropped whenever a direct standard model is recorded.

References:

- Delaney et al., *Braided zesting and its applications*,
  https://arxiv.org/abs/2005.05544 , CMP386 (2021), 1--55,
  doi:10.1007/s00220-021-04002-4, associative zesting and its H4 obstruction.
- Delaney et al., *G-crossed braided zesting*,
  https://arxiv.org/abs/2212.05336 , JLMS109 (2024), e12816,
  doi:10.1112/jlms.12816, discussion following (3.17)--(3.19):
  cyclic grading has vanishing H4 obstruction.

## SU(2)_4 central-extension quotients are coherent

Write C=SU(2)_4, d(i)=i mod 2, h=4. Its invertible h is a boson. Let E be
the explicitly recorded central extension of C2 x C2 with normal forms
z^c u^a v^e and multiplication

    (c,a,e)(d,b,f)=(c+d+pab+qef+reb, a+b, e+f).

All coordinates are mod two, and z=(1,0,0) is a central involution. In
C Deligne-product Vec(E), restrict to the full fusion subcategory S of
pairs (X,z^c u^a v^e) with d(X)=a. The object b=(h,z) has a central lift:
use the braiding of h in C and the trivial half-braiding of z in Vec(E).
Its self-braiding is 1. Thus 1+b is a central commutative separable algebra,
and the category of its modules (de-equivariantization) is a unitary fusion
category.

Tensoring by b acts freely on all simple labels because z is nontrivial.
Choose the orbit representative with c=0. This leaves labels (X,e), ten in
total. Multiplying representatives yields the cocycle exponent
p d(X)d(Y)+qef+re d(Y), which is absorbed by multiplying X tensor Y by h.
This is exactly the recorded fusion formula. No obstruction is inferred
merely from the associativity of the candidate fusion ring.

## Cyclic TY actions and the Ising subextension

For TY(C_n,chi,tau), take chi(a,b)=exp(2pi i ab/n), tau=1/sqrt(n).
An automorphism s with s(a)s(b)=ab mod n preserves the displayed TY
associator, so it induces a canonical unitary tensor action on its skeleton.
For a cyclic acting group C_m, one may change the multiplication coherence
by the tensor parity character epsilon raised to floor((i+j)/m). This is
an actual normalized 2-cocycle with values in tensor automorphisms of the
identity. In an equivariant object, its generator obeys U^m=epsilon(X).
The recorded cyclic-equivariantization formula is the exact character
projection for these actions. The verifier checks orthogonality of s and
reconstructs each tensor with exact root-of-unity arithmetic.

The R9_1_102 model is a full fusion subcategory of
(Ising Deligne-product Ising) crossed C2, for the canonical swap action.
The full crossed product is graded by (C2 x C2) semidirect C2; the selected
labels correspond to its cyclic order-four subgroup. The verifier checks
the swap, all selected labels, fusion closure, and all restricted products.

## Group-theoretical models and reporting cautions

The recorded C(G,omega,H,psi) constructions use actual finite groups and
subgroup algebras in pointed unitary categories. Untwisted character-based
formulas and the twisted C2 phase construction therefore define categories
before any comparison with the census. The group-theoretical tensor
receipts match the input exactly. The twisted S4 model and half-even
metaplectic descriptions are redundant for the current baseline and need
not be used in the final preferred list.

The audit validates existence at the level appropriate to a classification
by Grothendieck rings: a known or proved categorical construction plus an
exact full-table isomorphism. It does not claim a new independent pentagon
verification of every cited standard category, nor an exhaustive inventory
of all categorifications of each ring.
