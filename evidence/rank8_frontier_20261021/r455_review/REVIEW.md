# Independent R455 integer-domain and separator review

The complete finite arithmetic obstruction is accepted by this review.
Both normal and optimized Python replay passed on 2026-10-21. The categorical
scope and the new Q(sqrt(3),sqrt(13)) joint-trace domain have a separate
review; their hypotheses remain explicit dependencies of the final general
noncategorification conclusion.

The source is R8_3_455, tensor SHA256
`358b5323c54c66e80684b34dbe39d7bff44c5fe227bb8fb188794a0a9a722d88`.
The established source/character/restriction constructors are shared and
recomputed. They leave one low frame, two equivalent S labelings, and thirteen
high restriction vectors. The present review supplies an independent
enumeration of all integer multiplicities on that complete domain.

The residual Gram has two disjoint rank-two blocks, with matrices
`[[4,4],[4,16]]` and `[[12,18],[18,66]]`. Every high vector is in exactly one
block. A separate dynamic program extracts the coefficient of each target
Gram from its finite outer-product generating function. For each vector, its
multiplicity ranges from zero through the exact diagonal bound; every partial
sum is retained unless it exceeds a target entry. Thus no possible
nonnegative solution is discarded. The two target coefficients contain 14
and 58 solutions. Their 812 Cartesian products are distinct and each passes
all 49 original residual Gram equalities. Conversely, every full solution
restricts to one solution of each block, proving completeness.

The FP character is explicitly identified by equality with the source FP
dimensions and moved to the unit position. Both characters exchanged in this
step have formal codegree D and multiplicity one, so no normalization changes.
This is the corrected producer ordering; the earlier uncorrected exploratory
R455 replay is not used.

For every possible restriction column, the reviewer constructs the actual
distinguished S entries directly as

    S[E,Z] = D * chi_E(FZ) / (f_E * dim(E)).

The unit row is checked to equal all central FP dimensions, and the unit
column is checked to have entries D/f_E. The twenty symmetric nonunit low
fusion coefficients are then computed directly from

    N[E,F,G] = (1/D^2) * sum_Z S[E,Z] S[F,Z] S[G,Z] / dim(Z).

All five distinguished objects are self-dual, and all five are counted once
in this sum; the two-dimensional algebra representation is normalized by
its factor dim(E)=2. Exactly 24 of the 812 patterns have nonnegative integer
values for all twenty coefficients.

Precisely two distinguished columns equal the source unit vector. Hence the
invertible kernel of central forgetting has order two. Its nontrivial object
G has FG=1 and twist one, since it is a constituent of I(1). Tensoring by G
preserves every restriction vector. On a negative-monodromy object the twist
changes sign, so such an object cannot be fixed by G. Therefore each
negative-monodromy restriction type has even multiplicity. The direct S row
identifies exactly seven such high types; this leaves twelve patterns.
Galois spectral and low-pair tensor tests remove no additional pattern and
are not needed for the independent proof chain reviewed here.

There are exactly four allowed second-indicator tuples. The reviewer rebuilds
every one of the twelve-by-four complete height-six systems. All 48 have the
same 381-by-792 integer matrix and the same integer separating covector; their
right-hand sides are checked individually. Every one of the 792 explicit
column pairings is nonnegative, with minimum zero. Every one of the 48
right-hand-side pairings is strictly negative. This check uses neither the
producer's LP verifier nor a numerical optimization result.

The full source-bound score sequences and branch checks are recorded in
`direct.json`. The read-only commands are:

```sh
python evidence/rank8_frontier_20261021/r455_review/verify_direct.py
python -O evidence/rank8_frontier_20261021/r455_review/verify_direct.py
```

This is a separate AI review, not human refereeing or proof-assistant
formalization. Its independent components are the complete integer-pattern
enumeration, direct modular cubic normalization, parity domain, and explicit
full-column separation. The earlier restriction enumeration and the joint
operator constructor remain shared, with the latter's new field and trace
formulas reviewed separately.
