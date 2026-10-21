# Streaming global induction and the complete low-frame hull

This continuation imports the immutable rank-8 M3 central-induction
identities. It changes neither the underlying spherical identities nor
the all-order relative trace compression. A numerical linear program is
only a proposal mechanism. Accepted negative certificates are integer
row functionals tested on every column of the complete finite domain.
Accepted feasible certificates are nonnegative rational weights whose
exact column sum is the entire right hand side.

## Complete-domain column generation

Let `A x = b`, `x >= 0`, be the complete central-induction relaxation.
For a subset J of columns, solve its phase-I program with artificial
positive and negative slacks. An exact solution on J is also an exact
solution on the full domain. Conversely, a separator for J is accepted
only after checking `y A_j >= 0` for **every** full-domain column and
`y b < 0`. Otherwise violating columns are added and the proposal is
repeated. Numerical infeasibility, failure to reconstruct a rational
ray, or a solver limit never proves exclusion.

The high columns factor into an integral Gram contribution and products
of restriction coordinates with a relative trace of `dim(Z) theta^k`.
For fixed central dimension and phase type those traces are shared.
`streaming.Cone.oracle` evaluates the exact factorization without
materializing the dense full matrix. `verify_streaming.py` compares
the individual coefficients with the published operator and compares
the entire oracle with a direct scan. Coordinate denominator clearing
uses a strictly positive row scale and preserves all inequalities.

## Complete low-frame convex hull

For a commutative fusion ring each irreducible ring character has
dimension one. The distinguished constituents of induction of the unit
therefore give one low restriction column for each formal codegree,
with the central tensor unit fixed separately. A genuine low matrix L
has the prescribed unit row of `L L^t`, and `B-L L^t` is the Gram matrix
of the remaining nonnegative integral restriction columns. In
particular that residual matrix is entrywise nonnegative and positive
semidefinite.

The validated native enumeration retains every choice satisfying these
necessary conditions. It orders columns only when their full allowed
sets agree, hence only quotients permutations of interchangeable low
objects; every actual matrix retains a representative. Let F be the
resulting finite set of complete frames. If `a_c` is the original cone
column for a low constituent c, replace the independent low-choice
variables by columns

`a_F = sum_{c in F} a_c`, with `lambda_F >= 0` and
`sum_F lambda_F = 1`.

The seven original low-choice simplex rows each express the last
equality after this replacement. Every actual category supplies a
one-hot choice of F, so the new system is necessary. It is generally
stronger than choosing seven low columns independently, because every
extreme point already satisfies their joint constraints. High columns
and rotation auxiliary columns remain unchanged. The exact frame
oracle first computes each constituent score and sums its seven scores
for every complete frame; no frame is omitted by sampling. Sampling
is used only for the initial numerical restricted cone.

`verify_frames.py` compares frame columns with sums of the published
operator's constituent columns and compares the entire factorized
oracle with direct exact scores. The known unitary R8_3_334 has an exact
nonnegative rational solution of the strengthened cone, independently
replayed with Python optimization enabled.

## Scope

These cones initially give pseudo-unitary obstructions. A general
complex exclusion additionally requires the existing exhaustive
indicator assignments and the complete oriented signed/sphericalization
lift (or a separately verified general pseudo-unitarity gate). The
discovery driver records and replays that lift explicitly. A feasible
relaxation is evidence that this particular necessary-condition system
does not exclude the ring; it is never a categorification or model.

All discovery, validation, and certificates in this directory are new.
Published rank-8 M3 proof files remain immutable.
