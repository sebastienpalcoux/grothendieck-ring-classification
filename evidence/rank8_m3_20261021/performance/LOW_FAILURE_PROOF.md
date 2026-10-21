# Exact PSD shortcut for low-induction failures

The frozen checker first returns the lexicographically first negative Gram
entry, then the first negative principal minor in increasing size and index
order, then the first failed moment inequality. The additive adapter preserves
that exact output, not only its accept/reject result.

For a symmetric matrix `A`, a negative diagonal is incompatible with positive
semidefiniteness. A zero diagonal in a PSD matrix forces the whole corresponding
row to be zero: otherwise a two-coordinate quadratic form takes negative
values. A positive diagonal `p` reduces PSD equivalently to the Schur complement
`A_tail - v v^T/p`. Fraction-free Bareiss updates represent positive scalar
multiples of these Schur complements. Their division by the preceding positive
pivot is checked exactly. All arithmetic uses unbounded Python integers.
Zero rows can be omitted without changing PSD. If any input assumption or
exact division is not established, the shortcut returns an indeterminate result.

If the tail is certified PSD, every principal minor examined by the frozen
checker is nonnegative. The adapter may therefore skip that enumeration and
execute exactly the same moment formula, object order, algebraic sign query
and output encoding. If the tail is not certified PSD, the frozen checker is
called unchanged, preserving its precise first obstruction. The initial Gram
entry test is copied in the original order. The tail, rather than the full
matrix, is tested because that is exactly the frozen check's domain.

The bounded memoization key is the complete immutable integer tail matrix;
no approximate dimensions, tensor identity, field object identities, or mutable
state enter the PSD decision. Imported aliases are replaced only when they
refer to the exact frozen function. Frozen proof sources are never edited.

Fresh validation compares all principal minors on synthetic positive, singular,
indefinite, zero-pivot and large-integer matrices, and compares full obstruction
objects with the frozen implementation on synthetic and actual rank-eight
frames. See `verify_low_failure.py` and `low_failure_validation.json` for the
precise newly executed scope.
