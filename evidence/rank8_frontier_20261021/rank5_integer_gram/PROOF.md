# Complete integer Gram domain for the forced rank-five dual of R439

This is a finite necessary-condition calculation, not a construction or a
noncategorification result. The tensor is the pinned rank-five source
`R5_3_40`, with basis `1,s,V,P,Q`, dimensions `1,1,2,d,d`, and
`d=3+2 sqrt(3)`. The full-S3 Morita reduction and its scope are established
in the structural-model evidence. The present calculation applies only to
that specified hypothetical Morita dual, not to arbitrary categorifications
of the positive rank-five based ring.

The complete low-frame and symmetric-character assignment computation in
`../r439_centerless_rank5/verify.py` leaves low frame12. Its remaining central
restriction Gram matrix, in coordinates `s,V,P,Q`, is

    [4 2  4  4]
    [2 6  7  7]
    [4 7 34 31]
    [4 7 31 34].

The complete high-column domain has38 vectors. The spectrum of a low
central fusion matrix rejects index37: its proposed eigenvalue is -3/2,
which is not an algebraic integer. The general integral-center criterion
in `../review/INTEGRAL_CENTER_SUBCATEGORY.md` rejects every nonunit
integral-dimensional central simple. In this basis these are precisely
high columns with both P and Q coordinates zero: indices9,17,19,27.
The original tensor unit remains among the distinguished low simples.

For the33 retained vectors v, an actual central restriction matrix would
give nonnegative integer multiplicities m_v satisfying

    sum_v m_v v v^T = Q.

The verifier exhausts this finite domain by two independent integer
algorithms, using arbitrary-precision Python integers throughout.

1. Every retained vector with nonzero s coordinate has s=1 and V either0
   or1. The first Gram row forces exactly four such vectors, precisely
   two of each V value. There are1260 unordered multiset choices before
   enforcing the other entries of the first row;22 remain. Their removal
   leaves second diagonal4. V-positive vectors with s=0 therefore occur
   either as four V=1 vectors or one V=2 vector. After the complete second
   row is imposed there are114 partial choices. The residual two-by-two
   Gram matrices have83 distinct values. Each is exhausted by bounded
   multiplicities of the five vectors with both P and Q positive, followed
   by the complete partitions of each remaining diagonal into squares1
   and4 for the pure-axis columns.
2. A separate recursion groups all retained vectors by their first
   nonzero coordinate. It assigns each multiplicity in the complete range
   `0 <= m <= min(Q_ij/(v_i v_j))`, over positive denominators, then removes
   its outer product. A group can finish only when its entire first
   residual row is zero. At the fourth group the residual is required to
   vanish. This algorithm does not use the first algorithm's forced
   four-object/two-object decomposition or its two-dimensional partition
   formula.

Every multiplicity in either search is bounded by a positive diagonal
entry because every high vector is nonzero. Entrywise nonnegativity is
necessary at every partial subtraction, so neither algorithm discards a
valid completion. The first-nonzero-coordinate partition and fixed vector
ordering count each multiset exactly once. Both algorithms produce the
same58 complete multiplicity vectors; all ten Gram entries and all five
forbidden multiplicities are independently checked for every vector.

The receipt stores every solution, the exact source hash, full high-vector
domain, and source-bound categorical dependencies. These58 patterns are
inputs to further necessary central constraints. Their survival does not
provide central fusion rules, twists, associators, or a realization.

Canonical read-only replay:

    python evidence/rank8_frontier_20261021/rank5_integer_gram/verify.py
    python -O evidence/rank8_frontier_20261021/rank5_integer_gram/verify.py

Both invocations reconstruct the complete domain and compare the two
enumerations with the saved receipt. Explicit `--write` is required to
replace that receipt.
