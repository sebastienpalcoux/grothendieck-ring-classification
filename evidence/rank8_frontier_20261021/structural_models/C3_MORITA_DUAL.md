# Exact C3-condensation closure of R439 and R567

This is a conditional categorical reduction: **if** either ring is
categorifiable over C, its dual along the canonical C3 subgroup algebra has
the **same based ring**. We neither construct an associator nor assert that
the resulting categories are tensor equivalent. The argument rules out the
suggested possibility that this particular Morita operation reveals the
known C3+6 near-group subcategory or a different rank-eight known model.

## Module category forced by the exact C3 test

Write H=C3 for the source invertibles `[0,1,2]`. The other three invertibles
are the odd coset in S3. Write X,Y for the two noninvertibles, with
`d=3+2 sqrt(3)`, `gX=Xg=X`, `hX=Xh=Y`. In R439 both are self-dual;
in R567 they are dual to one another. A fixed simple trivializes the
pointed associator on H. Since `H²(H,C*)=0`, the algebra
`A=1+g+g²` exists uniquely up to algebra isomorphism in the pointed
subcategory.

The right-A module category has two simples `f0=A,f1=hA` from free pointed
orbits, and triples `X0,X1,X2` and `Y0,Y1,Y2` from the fixed objects. The
complete exact Fourier analysis in
`quadratic/CUBIC_SPLIT_MODULE.md` proves that, up to cyclic relabeling and
complex conjugation, left g shifts the X triple forward and the Y triple
backward, left h swaps corresponding X/Y labels, and the noninvertible
actions have zero blocks on both nontrivial deck-character eigenspaces.
All their 3-by-3 fixed-object blocks are consequently the all-ones matrix.
There are no other nonnegative module actions in the proved finite domain.

The verifier reconstructs the resulting eight integer left-action matrices,
checks all 64 fusion relations and all dualities against the original tensor,
and checks source hashes. Free-to-fixed coefficients are one, by the free
module adjunction; fixed-to-free coefficients follow by duality.

## All simples of the dual

An A-bimodule is an H-equivariant object in the right-A module category, for
the left H action. Each of f0 and f1 is fixed by H and has three equivariant
structures, because cyclic projective representations are one-dimensional.
These give six invertible A-bimodules: their underlying source objects have
dimension 3, and dividing by `FPdim(A)=3` gives bimodule dimension one.
Each triple Xi or Yi is a free H orbit, giving exactly one further simple
A-bimodule, called B_X or B_Y, with underlying source object 3X or 3Y and
bimodule dimension d. This exhausts the dual: its FP dimension is
`6+2d²`, the same as the original category.

The three bimodules over f0 are the character twists of A; their right
action T is simultaneous cyclic shift of the X and Y triples and fixes
f0,f1. A bimodule over f1 has a permutation action U interchanging f0,f1.
Commutation with left X forces it to interchange the X and Y triples.
Commutation with left g then forces
`U(X_i)=Y_(-i+c)` and `U(Y_i)=X_(-i+c')`, while commutation with left h
forces c=c'. A common cyclic relabeling of both triples normalizes c=0
(2 is invertible modulo 3). Hence `U²=1` and `UTU=T^-1`. These six
invertibles form S3. This derivation does not assume that the full pointed
associator on S3 is trivial.

## Uniqueness of the two remaining actions

Tensoring B_X on either side by a character bimodule cannot change its
underlying source support X. There is only one simple bimodule on this
support, so `T B_X=B_X=B_X T`. Its right action matrix B commutes with
every left fusion action and satisfies

`T B=B=B T`, and `B f0=X0+X1+X2`.

These are linear equations in 64 unknown entries. The exact coefficient
matrix for their homogeneous differences has rank 64 in both source
tensors. The left action matrix of X satisfies these constraints, so it is
the unique right action of B_X. The right action of B_Y is its odd translate,
and equals the left action of Y on the deck-invariant subspace; both vanish
on the other deck eigenspaces. The code checks the full integer matrices,
not just their eigenvalues or FP dimensions.

It follows that all dual structure constants agree with the source based
ring. Because right tensor actions compose in reverse order, the verifier
checks the **opposite** multiplication table explicitly. The source labels
for the generator of the character subgroup are chosen by the inverse deck
shift, and the odd coset is ordered accordingly. All 512 coefficients,
the eight duality identities, all left/right commutators, and linear
independence of the eight dual action matrices are checked. In particular,
for the self-dual case the tempting alternative

`rho²=(sum of the three elements of H) + p rho + q (h rho)`, with p+q=6,

does not lead to a different dual ring: the exact matrices force the original
coefficients 3 and 3. The non-self-dual case is likewise
the original R567 tensor.

## Consequence and limits

The complete subgroup-algebra Morita move stays within R439 or R567,
respectively. It does not turn them into a crossed extension with a C3+6
near-group neutral subcategory, and it cannot identify either with the
known C6-invertible equivariantization merely from equal global dimension.
The possible associators on the original and dual rings remain unknown;
based-ring closure is weaker than a Brauer--Picard self-equivalence.
Other algebra objects and chains of Morita moves are not exhausted.

The categorical inputs are standard module categories and dual categories
over a separable algebra, and equivariantization orbit/stabilizer theory:
EGNO, *Tensor Categories*, Chapter 7; Burciu--Natale,
[Fusion rules of equivariantizations](https://arxiv.org/pdf/1206.6625),
Corollary 2.13. No unitary or pivotal assumption is used.

```
python evidence/rank8_frontier_20261021/quadratic/cubic_split_module.py
python evidence/rank8_frontier_20261021/structural_models/c3_morita_dual.py
python -O evidence/rank8_frontier_20261021/structural_models/c3_morita_dual.py
```

The first command independently exhausts the Fourier module domain used as
input. The two Morita commands are read-only by default and verify the
reconstructed matrices and uniqueness equations against saved evidence.
