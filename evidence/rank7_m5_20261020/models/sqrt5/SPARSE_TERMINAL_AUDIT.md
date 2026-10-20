# Exact fixed-variable elimination and Farkas lifting

The helper `computation/r3895_sparse_terminal.py` is sound as a discovery
preconditioner. A final certificate is still checked in the original complete
integer system; no claim depends on a numerical infeasibility status.

Write the original equations as `Ax=b`, with nonnegative variables and bounds
`l_j <= x_j <= h_j` where an upper bound can be absent. Substitute
`x_j=l_j+z_j`. Fixed variables have `z_j=0` and are removed; a nonfixed finite
upper bound becomes `z_j+s_j=h_j-l_j`, with `s_j>=0`. This is an exact affine
equivalence over both the reals and integers.

For a reduced Farkas covector, write `y` for the original equation weights,
`w_j=(A^T y)_j`, and `u_j` for a reduced upper-bound equation weight (zero
when absent). Its column conditions are `u_j>=0` and `w_j+u_j>=0` for each
nonfixed variable. The original bound rows are
`x_j-s_j=l_j` and `x_j+s_j=h_j`.

For a nonfixed variable with positive lower bound, give its original lower
row weight `-(w_j+u_j)` and its upper row weight `u_j`. The original variable
score is then zero, both slack scores are nonnegative, and the target
contribution beyond `y.b` is

`-l_j*w_j + u_j*(h_j-l_j)`.

When the lower bound is zero its row is omitted, leaving the already
nonnegative score `w_j+u_j`. The target formula is unchanged. For a fixed
variable with positive fixed value `l_j=h_j`, split `-w_j` into lower weight
`min(0,-w_j)` and upper weight `max(0,-w_j)`. Their sum is `-w_j` and their
target contribution is `-l_j*w_j`. For a variable fixed at zero there is no
lower row: upper weight `max(0,-w_j)` leaves score `max(w_j,0)` and contributes
zero to the target. These are exactly the helper's cases.

Consequently the lifted covector has nonnegative coefficients on every
original variable and bound slack, and its target equals the reduced target
exactly. A strictly negative reduced target therefore gives a valid original
Farkas contradiction. The helper additionally checks these conclusions with
the original full-system verifier before exporting a candidate.

Independent `audit_sparse_terminal.py` controls reconstruct the original
bound rows without the producer's `bound_system` function. Normal and
optimized Python both pass 1,800 deterministic systems, 22,985 nonnegative
reduced covectors and 9,491 strictly negative targets. The controls include
9,896 cases with a variable fixed at zero and 5,600 covectors with every
variable fixed. These are arithmetic controls; the all-input justification
is the algebraic calculation above.
