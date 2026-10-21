# Independent review of the complete R8_3_982 module restriction

**Accepted scope.** If R8_3_982 has a complex fusion categorification, every
indecomposable semisimple module category has eight simples. Its based module
is among the three recorded types, and its simple internal ends are among the
eight surviving candidate objects. Every nonregular module type includes
`1+X5`. These are necessary conditions; the two nonregular based modules are
not claimed to admit module associators, and no algebra multiplication on
`1+X5` has been constructed.

This review examined `../r982/MODULE_TYPES.md`, `module_types.py`, its receipt,
and the preceding complete algebra-object filter. It also checked the
pointed-module theorem in the primary source. The result is a separate
mathematical/computational review, not human peer review or formal proof
verification.

## Why the involution must act freely on every module category

The frozen pseudo-unitary center/indicator result forces the source order-two
invertible to generate the nontrivially twisted pointed category
`Vec_(C2)^omega`. The new sphericalization gate, reviewed separately in
`PIVOTALITY_REVIEW.md`, applies to arbitrary complex categorifications.
The nontrivial C2 associator class is fixed under Galois conjugation, so the
pointed-category conclusion also applies to every original categorification.

If a simple module object were fixed by `g`, the full abelian subcategory of
its finite direct sums would be a rank-one module category for the pointed
subcategory. Its scalar module associators would provide a 2-cochain whose
coboundary is `omega`, impossible for this nontrivial class. This agrees with
Ostrik, *Module categories over the Drinfeld double of a finite group*,
[arXiv:math/0202130](https://arxiv.org/abs/math/0202130), Example 2.1: a stabilizer
subgroup must trivialize the restricted 3-cocycle.

Restriction to the pointed subcategory may decompose a module category, but
that does not weaken the argument: a fixed simple by itself supplies the
forbidden rank-one summand. No braiding or positive module trace is being
assumed. Consequently every simple internal end has zero coefficient at `g`,
removing twenty of the thirty-one previously bounded candidate objects.

## Why the module rank is exhausted, rather than bounded by choice

For a fixed simple module object `m`, the induction matrix `B` contains every
module simple among its columns: otherwise the objects occurring in the
`X_i m` would form a proper module summand. Hence no column is zero.
The distinguished columns `m, gm` are exactly `a, ga`, and the remaining
columns have zero entries at source rows 0 and 6 and form free pairs.

Module adjunction gives the stated Gram formula. The source action of `g`
swaps the remaining rows in three pairs. Splitting paired columns into their
row sums `u` and differences `d` gives exactly `P=UU^t`, `M=DD^t`, with
`u>=0`, `|d|<=u`, and `u=d mod 2`. Each `u` column is nonzero, because the
original columns are nonnegative and nonzero. These conditions recover the
original pair by `(u+d)/2` and `(u-d)/2`; there is no lost normalization factor.

For determinant-one `P`, Cauchy–Binet gives a sum of squares of integral
maximal minors equal to one. Choose the unique nonzero minor. Every maximal
minor replacing one of its three columns by any extra column vanishes, so
the extra column has zero coefficient along each selected basis column.
It is zero. Thus there are exactly three nonzero column pairs.

For determinant-four `P`, the checked unimodular transformation changes it
to `diag(1,2,2)`. The norm-one row occupies one coordinate. Orthogonality
forces the other rows to vanish there. Each norm-two row has exactly two
entries `+1` or `-1`; their supports cannot meet in exactly one coordinate.
If the supports coincide, orthogonality gives the three-column form. If
they are disjoint, it gives the five-column form. Signed coordinate
permutations account for all possibilities, including signs of the norm-two
rows. Therefore there are no intermediate or larger nonzero-column cases.

The program transforms both forms back to the original coordinates before
checking positivity and parity. This ordering is essential: an arbitrary
unimodular row change would not preserve coordinatewise positivity or the
relevant parity bound. In all four five-column cases, the original second
row has five odd entries but the corresponding row of `D` has squared norm
one. Since each odd entry forces a nonzero difference coordinate, this is
impossible. Only three paired columns remain, and the two distinguished
columns give module rank eight.

## Finite factor and based-module accounting

After the rank proof, the three-column Gram-factor searches are genuinely
finite: each row is bounded by its exact squared norm. Sorting the first
positive row removes only column permutations; all later rows and all signed
difference factors are enumerated. Every compatibility condition and the
reconstructed full Gram are checked. Exchanging pair members and permuting
pairs is done after this coverage.

The resulting `B` is square and is checked invertible. In the row convention
of the source tensor, `N_i B = B M_i`, so the unique action is
`M_i=B^(-1) N_i B`. This uses the correct ordered convention. Three candidates
are removed: two force an exact action entry -1, and one has no paired
integral factor. The eight remaining candidate indices are
`0,2,5,9,12,16,19,23`.

Every surviving action satisfies all source products and dual-transpose
relations and is connected. The simultaneous-permutation test exhausts the
possible permutations by their internal-end labels; it gives one regular
and two distinct nonregular based-module types. The latter are exchanged
by source duality. Each has `1+X5` as an internal end at two vertices.
For the regular type, a vertex with internal end 1 identifies the actual
module category with the regular category. No uniqueness of associator
structures on the two nonregular types is inferred from their matrices.

## Replays and independent arithmetic

The full producer replay passed under optimization:

```sh
python -O evidence/rank8_research_20261022/r982/module_types.py
```

Its output is `r982_modules_optimized_replay.log`. The additional checker
`review_r982_modules.py` uses only Python integer/Fraction matrices and
imports no producer or SymPy code. It reconstructs every retained induction
Gram and every `B^(-1) N_i B`, verifies each failed action entry and each
class-identifying permutation, checks all source products for all three
actions, and independently checks the five-column obstruction in the
original coordinates. It also verifies the `1+X5` internal ends. This passed
and is recorded in `r982_modules_independent_review.json`.

```sh
python evidence/rank8_research_20261022/r928_r941/review_r982_modules.py
```

The separate checker does not claim to replace the lattice completeness
argument or re-enumerate the original thirty-one algebra candidates. Those
are explicit proof dependencies. Together with the exact producer replay,
the categorical and lattice arguments justify the stated complete
necessary module restrictions.
