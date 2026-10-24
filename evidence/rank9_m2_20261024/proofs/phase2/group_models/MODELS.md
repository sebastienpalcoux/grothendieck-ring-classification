# An explicit two-member representation-category family

The two previously unresolved rings

* `R9_2_812`;
* `R9_2_813`

are respectively the representation rings of

\[
 G_A=(C_2\times C_2)\rtimes\operatorname{Dih}(A),
 \qquad A=C_9,\ C_3\times C_3.
\]

Here `Dih(A)=A⋊C2`, with the involution acting by inversion. Fix a
surjection `q:A→C3`. On `V=F2²`, an element `a∈A` acts by `R^{q(a)}` and
the inversion involution acts by `S`, where

\[
 R(x,y)=(y,x+y),\qquad S(x,y)=(x,x+y).
\]

The identities `R³=S²=1` and `SRS=R⁻¹` define the semidirect product.
Thus these are explicit finite groups of order 72, and `Rep(G_A)` are
unitary fusion categories without any associator-existence uncertainty.
They are SmallGroup(72,15) and SmallGroup(72,43), respectively; the second
also has the standard description `C3⋊S4`, where odd permutations invert
`C3`.

## Unified character construction

The action on the characters of `V` has two orbits: the trivial character
and the three nontrivial characters. Clifford theory gives:

1. The irreducible representations inflated from `Dih(A)`: two of degree
   one and four of degree two. The degree-two characters are indexed by
   pairs `{χ,χ⁻¹}` of nontrivial characters of `A`.
2. Choose a nontrivial character of `V`. Its stabilizer in `Dih(A)` is
   `Dih(ker q)≅S3`. It extends over the semidirect product with its
   stabilizer. Inducing its three twists by the irreducible stabilizer
   representations gives two representations of degree three and one
   of degree six.

The complete degree multiset is therefore `(1,1,2,2,2,2,3,3,6)`.
The exact characters, not only these degrees, are used to establish the
models. `dihedral_extension_models.py` implements the inflated and
induced character formulas in `Q(ζ9)`, checks character orthogonality and
`Σ degree²=72`, calculates all 729 tensor-product multiplicities by exact
character inner products, and finds a unit-preserving based isomorphism
to each input ring. It also checks the explicit group law's associativity.
The canonical records are in `canonical_models.json`.

The source-to-model basis maps are:

* `R9_2_812`: `[0,1,6,7,2,5,3,8,4]`;
* `R9_2_813`: `[0,1,6,7,2,4,5,8,3]`.

These constructions are independent of the GAP discovery search.
GAP/SmallGroups also finds the same representation-ring models and
several Morita-equivalent untwisted subgroup-algebra presentations.

## Scope of the finite group-model search

`scan.g` scans all groups of the specified orders and all conjugacy
classes of subgroups. Before computing an untwisted group-theoretical
fusion tensor `C(G,1,H,1)`, it checks the full Frobenius–Perron dimension
multiset using double cosets and stabilizer character degrees. Exact
cyclotomic stabilizer-character convolution then computes every tensor
entry; `match_gap.py` tests full based isomorphisms against the input.

Non-matches do not exclude categorification. The search does **not**
classify categories with nontrivial global 3-cocycles or subgroup
2-cocycles and does not assert that all integral categories of these
dimensions are group theoretical.

Primary construction references: the standard finite-group
representation category and Clifford induction. GAP's official
SmallGroups documentation is
https://gap-packages.github.io/smallgrp/doc/chap1_mj.html .
An independently maintained group description for the second model is
https://www.lmfdb.org/Groups/Abstract/72.43 . Neither external catalogue
is needed for the explicit construction or replay.
