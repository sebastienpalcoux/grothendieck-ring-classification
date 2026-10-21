# R8_3_982: complete module-rank and internal-end restriction

Every complex categorification of R8_3_982 has the following necessary
properties:

1. Every indecomposable semisimple module category has exactly eight simple
   objects.
2. Its based module is either the regular based module or one of two
   explicitly recorded, mutually dual, nonregular based modules.
3. The complete list of possible underlying objects of connected separable
   algebras shrinks from 31 to eight.
4. Every nonregular module category contains a simple object whose internal
   end is `1+X5`. Thus any nontrivial categorical Morita construction must
   first realize this particular possible algebra, of dimension
   `3+sqrt(2)+sqrt(3)+sqrt(6)`.

These are necessary structural restrictions, not a categorification or
an exclusion of the fusion ring. In particular, the two new integral
based modules do not supply module associators. Whether `1+X5` admits a
connected separable algebra structure remains unresolved.

## Categorical inputs and scope

The canonical tensor has SHA256
`f4a9fb77b3a78e9dcd8370ca9fa822ea331f1b71e3fad7990efdd386445fcd1c`.
Its unique nonidentity invertible is `g=X6`, acting freely on the source
simples by `(0 6)(1 2)(3 4)(5 7)`.

The complete preceding center/indicator audit in
`../../rank8_next_20261021/r982/SEMION_ACTION.md` forces the source pointed
subcategory to have the nontrivial associator class in
`H^3(C2,C*)`: its positive pivotal second indicator is `nu2(g)=-1`.
This initially holds for pseudo-unitary categorifications. The independent
signed-sphericalization proof in `../pivotality/` upgrades general
categorification to a spherical category with a pseudo-unitary Galois
conjugate. The two C2 associator classes have representatives with values
`+1,-1`, so being nontrivial is Galois invariant. Consequently this
pointed-associator conclusion applies to every complex categorification.

If `g*m` were isomorphic to a simple module object `m`, the one-object
orbit would be a rank-one module category for the pointed subcategory.
Its module pentagon would trivialize the associator on C2, a contradiction.
Equivalently, pointed module categories are parameterized by a subgroup
on which the associator restricts trivially, together with a trivializing
2-cochain; see Ostrik, *Module categories over the Drinfeld double of a
finite group*, Example 2.1, [arXiv:math/0202130](https://arxiv.org/abs/math/0202130).
Thus `g` acts freely on every module category. This argument does not
require a source braiding, a module trace, or a tensor product splitting.

For a simple module object `m`, let `A=internalEnd(m)`. The coefficient
of `g` in `A` is `dim Hom(g*m,m)=0`. The previous complete finite algebra
filter, whose categorical proof uses only adjunction and FP dimensions,
is in
`../../rank8_frontier_20261021/structural_models/ALGEBRA_CANDIDATES.md`.
Exactly 20 of its 31 candidate objects have a nonzero g coefficient;
they are now excluded.

## Complete paired induction Gram calculation

Fix one of the remaining eleven candidates `A=sum_i a_i X_i`, and write

`B_(i,n) = dim Hom(X_i*m,n)`.

Module adjunction gives the exact Gram matrix

`(B B^t)_(i,j) = sum_k a_k N_(j,k)^i`.

Every module simple appears in some `X_i*m`: the full submodule generated
by `m` is the whole indecomposable module category. Therefore every
column of B is nonzero. The columns belonging to `m` and `g*m` are `a`
and its g translate. All other columns have zero coordinates at source
indices 0 and 6 and come in pairs `(v,g*v)`. Remove the distinguished
pair and order the remaining six source rows as

`(1,2; 3,4; 5,7)`.

For each remaining paired column, let `u` be the three sums within its
row pairs and `d` the three differences. The residual Gram matrix H
then yields two 3-by-3 matrices

`P_(i,j)=H_(2i,2j)+H_(2i,2j+1) = sum_columns u_i u_j`,

`M_(i,j)=H_(2i,2j)-H_(2i,2j+1) = sum_columns d_i d_j`.

Each column obeys `u>=0`, `|d_i|<=u_i` and `u_i=d_i mod 2`. Its u
column is nonzero. Conversely these conditions reconstruct both
nonnegative original columns as `(u+d)/2,(u-d)/2`.

Seven candidates have `det P=1`. By Cauchy--Binet, the sum of squares of
all 3-by-3 minors of an integral factor U is one. Exactly one such minor
is nonzero. Choose its three columns as an integral basis. Replacing any
of them by any further column produces zero determinant, forcing every
further column to be zero. Nonzero-column exhaustivity therefore leaves
exactly three residual column pairs: the module rank is eight.

The other four candidates have `det P=4`. The receipt provides a checked
integral unimodular isometry of each P to `diag(1,2,2)`. Every integral
embedding of this lattice has, up to signed coordinate permutation, one
of two forms. The norm-one row occupies one coordinate. Each of the two
orthogonal norm-two rows has two entries of absolute value one outside
that coordinate. Their supports either coincide, with cancelling inner
products, or are disjoint. These give respectively three or five nonzero
columns; no other support pattern is possible. The script transforms
both representatives back and checks the unique possible nonnegative
column signs.

For all four five-column factors, the second row of U has five odd
entries while `M_(1,1)=1` (zero-based indices). The parity condition would
force the corresponding row of d to have at least five nonzero integer
entries, contradicting its squared norm one. Hence the rank-twelve
alternative is impossible. Again the module rank is eight.

## Exact source action and survivors

For rank eight, each retained induction matrix B is square and invertible.
The source action is uniquely forced by

`M_i = B^(-1) N_i B`.

The script exhausts every integral three-column factor of P and M inside
their exact squared-norm bounds. Column permutations and exchanging the
two members of a g pair are removed only after the complete enumeration.
No LP, floating-point infeasibility decision, or arbitrary module-rank
bound is used.

| Prior algebra index | Underlying object coefficients | Result |
| --- | --- | --- |
| 0 | `[1,0,0,0,0,0,0,0]` | Regular type |
| 2 | `[1,0,0,0,0,1,0,0]` | Two nonregular types |
| 5 | `[1,0,0,1,1,1,0,0]` | Two nonregular types |
| 9 | `[1,1,1,1,1,1,0,0]` | Two nonregular types |
| 10 | `[1,1,1,1,1,1,0,1]` | Unique factor forces an action entry -1 |
| 12 | `[1,1,1,1,1,2,0,0]` | Regular type |
| 14 | `[1,1,1,2,2,1,0,1]` | Unique factor forces an action entry -1 |
| 16 | `[1,1,1,2,2,2,0,0]` | Regular type |
| 19 | `[1,2,2,3,3,2,0,2]` | Regular type |
| 21 | `[1,2,2,3,3,3,0,1]` | No compatible paired integral factor |
| 23 | `[1,3,3,4,4,3,0,2]` | Two nonregular types |

All surviving actions are independently checked for every source
multiplication, dual-transpose compatibility, connectivity, and free
g action. Exact simultaneous-permutation checks yield three based-module
types. The first is independently matched to the regular module. The
second and third are distinct, and source duality interchanges them;
the intertwining permutation is recorded.

The regular type has a simple object with internal end 1, so any actual
module category of that type is equivalent to the regular category.
Both nonregular types have exactly the four internal-end vectors at
indices 2,5,9,23, each occurring twice. In particular they both contain
`1+X5`. This proves the stated reduction of every nonregular Morita route
to that algebra, without asserting its existence or uniqueness.

## Replay

`module_types.py` binds the canonical tensor, the complete preceding
31-object receipt, the frozen semion/indicator audit, and the independent
general sphericalization gate by SHA256. Default execution is read-only:

```sh
python evidence/rank8_research_20261022/r982/module_types.py
python -O evidence/rank8_research_20261022/r982/module_types.py
```

Both compare the complete exact result with `module_types.json`. The
receipt contains every relevant Gram matrix, integral isometry, possible
paired factor, failed action entry, surviving NIM-representation, and
permutation identifying the three types. Passing this verifier certifies
only the necessary module restrictions stated above.
