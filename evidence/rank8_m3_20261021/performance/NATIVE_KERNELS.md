# Exact native enumeration through rank eight

These are additive accelerators. The frozen supplement algorithms remain
unchanged. `verify_native.py` performs 86 fresh comparisons against their
Cartesian, all-principal-minor, and exhaustive principal-coordinate methods.
For the reference Gram executable only its input rank guard is enlarged from
five to eight; its enumeration and arithmetic are unchanged.

`low_frames_rank8` enumerates the exact row sum by meet in the middle. Identical
column sets are ordered lexicographically, exactly as in the frozen enumerator.
For Gram pruning, every partial choice leaves a positive semidefinite residual
if it extends to a solution. With m unspecified columns and remaining row sum r,
the Schur complement condition `m Q - r r^T >= 0` is necessary. Its one- and
two-coordinate minors are used only as partial pruning tests. Entrywise
nonnegativity and the exact positive semidefiniteness of the completed residual
are checked before output. Symmetric fraction-free elimination detects PSD:
a negative pivot rejects; a zero diagonal with a nonzero remaining row rejects;
otherwise the positive-pivot Schur complement is tested recursively.

Bareiss entries are minors. For tail size d and input bound b, every numerator
is bounded in absolute value by `2 ((d-1)! b^(d-1))^2`. The Python wrapper
requires this to be below `2^120` before any native PSD calculation. Row sums,
products, and partial 2x2 tests are also within the declared 64/128-bit bounds.
Unsupported arithmetic sizes fail explicitly; they never certify an exclusion.

`gram_vectors_rank8` seeks nonzero nonnegative integer v with both
`Q-vv^T >= 0` and entrywise nonnegative residual. Exact fraction-free elimination
first verifies PSD and finds a nonsingular principal coordinate set I. On its
range, every v is uniquely determined by w=v_I through
`v=Q[:,I] adj(Q[I,I]) w/det(Q[I,I])`. The condition is the ellipsoid
`w^T adj(Q[I,I]) w <= det(Q[I,I])`. Every prefix principal ellipsoid is a
necessary condition, so pruning at prefixes preserves completeness. Integrality,
nonnegativity, diagonal bounds, the full ellipsoid, and all entrywise products
are checked exactly. The wrapper proves explicit 128-bit arithmetic bounds for
each prefix and for the range map.

The `high_columns` adapter retains the frozen rational/quadratic algebraic
integer and d-number tests after complete native Gram enumeration. Its output
is separately compared with the frozen Cartesian implementation. The environment
variable `RANK6_REFERENCE_GRAM` still selects that reference implementation.

Fresh source-derived bottlenecks are replayed by `verify_benchmarks.py`:

| Input | Complete output count |
|---|---:|
| R8_3_65 low frames, Gram-pruned | 168024 |
| R8_3_1453 low frames, Gram-pruned | 168024 |
| R8_3_903 low frames, Gram-pruned | 58398 |
| R8_3_731 Gram vectors in the Casimir tail | 24970 |

The recorded SHA-256 digests cover the complete sorted outputs. Timings are
diagnostic only and are never used as mathematical evidence. Both verification
entry points use explicit exceptions, so `python -O` does not bypass checks.
