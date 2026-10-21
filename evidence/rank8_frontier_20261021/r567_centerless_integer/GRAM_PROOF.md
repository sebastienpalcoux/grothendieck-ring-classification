# Complete central integer Gram enumeration for R567

The complete source-bound low-frame, full-character symmetry and
partial-S spectral-integrality calculation is in `source.py`. It retains
one low frame,45 candidate high restriction vectors, and two symmetric
character assignments. The independent integral-center theorem removes
indices0,34, while the complete complex-character eigenvalue test removes
indices9,13,16,24,27,30,32,33,42. The remaining34-vector domain is stable
under duality.

This calculation concerns a hypothetical center of a categorification of
R567. It is not a construction. The general scope depends on the separately
proved Galois-pseudo-unitary reduction and integral-center theorem.

Every full seven-coordinate high vector is uniquely

    (u,u,p,q,w,w,w).

Use reduced coordinates `(u,w,p,q)`. The full seven-by-seven Gram identity
is equivalent to the reduced identity with matrix

    [4 0  4  4]
    [0 4  6  6]
    [4 6 42 31]
    [4 6 31 42].

The source verifier checks both the vector lift and every matrix entry.
Two different complete integer enumerations solve the remaining equation

    sum_v m_v v v^T = Q,     m_v in nonnegative integers.

The first enumeration uses the small first two diagonals. Since u*w=0,
the u-positive and w-positive columns are disjoint. Each positive u or w
is1 or2, so diagonal4 forces either four columns with coordinate1 or a
single column with coordinate2. There are331 u-multisets; the entire u-row
leaves4. There are1821 w-multisets for each such choice; the first two rows
leave56 pairs of multisets. Their residual two-by-two matrices have34
distinct targets. For each target the search exhausts all bounded
multiplicities of columns with both p,q positive, followed by all
partitions of each remaining diagonal into squares1,4,16 from the
pure-axis columns.

The second enumeration does not use this decomposition. It groups the
columns by their first nonzero coordinate and recursively assigns each
column every multiplicity from zero to

    min floor(Q_ij/(v_i*v_j)), over positive v_i*v_j.

The residual remains entrywise nonnegative, and a group can finish only
when its leading residual row is zero. Every nonzero vector has a
positive diagonal square, so all ranges are finite. No valid solution is
discarded by these necessary partial-sum bounds. Fixed column order makes
both searches duplicate-free.

Both complete enumerations return exactly1071 integer Gram solutions,
with identical sorted multiplicity lists. Central duality additionally
requires equality of multiplicities of dual restriction columns. Exactly
155 patterns satisfy that condition. The receipt stores all155, the hash
of the complete1071-pattern list, source and proof dependency hashes, and
the exact duality permutation. All49 entries of the original Gram matrix
are checked for every one of the1071 patterns before the duality filter.

All arithmetic in `gram.py` is arbitrary-precision integer arithmetic.
Normal and optimized Python perform the same explicit checks. Default
invocation is read-only; `--write` explicitly replaces the receipt:

    python evidence/rank8_frontier_20261021/r567_centerless_integer/gram.py
    python -O evidence/rank8_frontier_20261021/r567_centerless_integer/gram.py

Further central constraints may exclude these155 necessary patterns.
The Gram enumeration by itself asserts no categorification outcome.
