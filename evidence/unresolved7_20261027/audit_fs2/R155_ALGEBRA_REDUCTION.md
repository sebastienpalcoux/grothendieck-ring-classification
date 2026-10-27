# R6_4_155: a new small-algebra reduction, with exact scope

Date: 27 October 2026. **The ring remains unresolved.**
No complete exclusion or categorical model has been found in this pass.

Write the basis as 1,h,g,hg,X,Y with h fixing X,Y, g exchanging them,
X*=Y and

    XY=1+h+4(X+Y),       X²=Y²=g+hg+4(X+Y).

Put d=4+3sqrt(2), D=72+48sqrt(2). The preceding reduction permits a
pseudo-unitary representative whenever any complex categorification exists.

## A new family of necessary algebra constraints

Consider a connected separable algebra with underlying object

    A_k = 1 + kX + kY,     k >= 1.

Then **k is either 1 or 2**. For k=1 there is exactly one possible based
right-module structure, of rank six. For k=2 there is likewise exactly
one possible based right-module structure, of rank six. The k=1 conclusion is only necessary. The canonical-center argument below
additionally proves conditional existence of A_2 whenever C exists.

Indeed, each of the four free modules aA_k, a in {1,h,g,hg}, is simple:
its endomorphism dimension is [A_k:1]=1. They are pairwise distinct because
their underlying objects have different unique invertible summands. Every
other simple right module has underlying object a_j X+b_j Y, with
nonnegative integers a_j,b_j: if its underlying object contained an
invertible a, free-module adjunction would identify it with aA_k.

Subtracting the four known simple contributions from the free-module Gram
matrix gives

    sum a_j² = sum b_j² = 1+8k-4k²,
    sum a_j b_j = 8k-4k².

For k>=3 the first expression is negative, a contradiction.

For k=2 the two residual vectors have disjoint support and squared norm
one. Thus the only additional right modules have underlying objects X
and Y, respectively. Tensoring by the four invertibles and reciprocity
then determine all six action matrices.

For k=1 the residual squared norms are five, and the inner product is four.
Consequently sum(a_j-b_j)²=2. After interchanging two labels,
a-b=e_p-e_q; equality of the squared norms gives b_q=b_p+1.
Writing b_p=t, the contribution of these two coordinates is
`t²+(t+1)²<=5`, so t is 0 or 1.

If t=0, there is a simple right A_1-module whose underlying object is X
(and another whose underlying object is Y). Its internal endomorphism
object in C has FP dimension

    d²/FPdim(A_1) = d²/(1+2d) = 2+4sqrt(2)/3.

This is not an algebraic integer (minimal polynomial
`9t²-36t+4`), whereas the FP dimension of every object of a fusion category
is an algebraic integer. Hence this branch is impossible. This is a
relative internal-end dimension, not the generally false claim that
FPdim(C)/FPdim(A) must always be an algebraic integer for an arbitrary
noncentral algebra.

If t=1, these two coordinates already exhaust the squared norm five.
Thus the two remaining modules have underlying objects 2X+Y and X+2Y.
Their dimensions relative to the four free modules have ratio
`3d/(1+2d)=sqrt(2)`. This proves the asserted unique rank-six module.

## Explicit surviving action

Order the k=1 modules by A,hA,gA,hgA,M,N, where M=2X+Y and N=X+2Y.
The invertibles act regularly on the first four; h fixes M,N and g
exchanges them. With columns as inputs, multiplication by X is

    [[1,1,1,1,1,2],
     [1,1,1,1,1,2],
     [1,1,1,1,2,1],
     [1,1,1,1,2,1],
     [2,2,1,1,2,2],
     [1,1,2,2,2,2]],

and multiplication by Y is its transpose. The k=2 action is recorded in
the companion exact checker. Both obey the original fusion relations.
The module calculation requires no pentagon search or numerical solve.

An initial apparent trace contradiction was explicitly rejected: the
four free-module diagonal entries must be counted. For k=1 the full trace
of N_X is 8, not 4, and is compatible with its character spectrum.

## The k=2 algebra is actually forced, but returns to the known module

This further observation was suggested by the root investigator and checked
independently. The formal codegrees of this commutative rank-six ring are
D,D',8,8,4,4. Thus I(1) has six multiplicity-one constituents, with dimensions

    1, 1+4d, 1+2d, 1+2d, 2+4d, 2+4d.

The pointed subcategory of dimension four corresponds, under the canonical
subalgebra/fusion-subcategory correspondence, to a connected etale subalgebra
L of I(1) of dimension D/4=2+4d. A unit-containing subobject of I(1) with
that dimension must be L=1+B, where B has dimension 1+4d. To check uniqueness,
compare the constant and d coefficients of
`1+m(1+4d)+n(1+2d)+p(2+4d)=2+4d`: nonnegative multiplicities force
m=1,n=p=0.

The constituent B is selfdual by uniqueness of its dimension, and F(B)
contains the unit once. Its dimension and selfduality then force
`F(B)=1+2X+2Y`. The canonical algebra counit F(I(1))->1 is an algebra map,
so it restricts to an augmentation F(L)->1. Separability splits off this
unit algebra as a two-sided direct-product block. The complementary block
is a connected separable algebra with underlying object A_2=1+2X+2Y.
This uses the algebra counit and separability, not the false assertion that
an arbitrary simple summand of I(1) is itself an algebra.

For the unique k=2 module described above, the simple whose underlying object
is X has internal endomorphism algebra with underlying object 1+h: this is
read from its diagonal action multiplicities. The algebra structure on
1+h is unique up to isomorphism because H²(C2,C*)=0 and the pointed
associator restricts trivially there. Consequently C_{A_2} is equivalent,
as a C-module category, to C_{1+h}. Thus this forced noninvertible algebra
recovers the already available fermion module; it does not provide a
categorical construction of C or reduce it to a known new Morita model.

The canonical subalgebra correspondence is DMNO, arXiv:1009.2117,
Theorem 4.10; its canonical-algebra and separability prerequisites are
standard results in Section 3 of that paper. The dimensions and
multiplicities use Ostrik, arXiv:1309.4822, Theorem 2.13.

## Why this is not yet a resolution

The k=1 module passes the ring-action and short full-Gram consistency
checks. A based module is not a coherent module category, and the argument
does not force existence of A_1. Nor does the algebraic-integer obstruction
on the other Gram branch exclude the surviving branch. The new result
narrows a noninvertible-algebra construction route without changing the
classification status of R6_4_155.

The preceding symmetric Galois-pairing theorem also does not exclude this
ring: X and Y are nonselfdual, and the forced negative-indicator
invertibles g,hg are absent from the relevant restrictions of selfdual
multiplicity-one constituents of I(1).

A fresh literature check included the 18 October 2026 Anyon Atlas,
https://arxiv.org/html/2610.25439v1. Its numerical modular-data enumeration
is not an exhaustive categorical classification, and its explicit new
pentagon/hexagon constructions are stated for particular ranks 11 and 12.
No matching categorical construction for the required rank26 factor,
its rank16 supermodular centralizer, and the necessary algebra was obtained
from that paper. This source is a comparison resource, not an exclusion
or a model of R155.
