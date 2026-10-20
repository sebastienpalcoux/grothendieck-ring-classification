# Exact cyclic-indicator proof chain for R7_5_5039

This note describes the complete replay obligation. Acceptance in the census is
a separate decision after successful normal and optimized-Python verification
and independent review. A numerical infeasibility report is not an input to the
proof.

The original based fusion tensor is pinned by the canonical compact-JSON SHA256
`8606c63a2f02ea028185db755a4b055382073b94736d5040ee92f3eec07f450c`.
The read-only entry point is
`models/sqrt5/verify_r5039_cyclic_chain.py::verify(rid, tensor)`.
It returns a receipt binding the input tensor, all reconstructed systems,
certificate files, imported repository code, and mathematical proof notes.

## Mathematical reductions

The signed-quotient enumeration and dimension-field argument in
`sqrt5_reduction/verify_reduction.py` cover every possible categorification.
There are four oriented signed quotients. The admissible gauge branches give a
spherical category whose dimension character lies in the Frobenius–Perron
Galois orbit; the remaining signed branches are excluded by the incompatible
quadratic character-field requirements. Thus the center calculations may be
performed after Galois conjugation in a pseudounitary categorification.

The independent domain verifier regenerates four complete induced-unit frames
and all 142,510 possible high restriction rows. Character reciprocity leaves
two eligible frames. One has induced-unit conductor-eight difference-square
weight eight, contradicting the twist-one upper bound two. The other has
twelve label assignments, falling into exactly two classes of identical
character-to-row assignments. The second Frobenius–Schur indicator vector is
uniquely `(1,0,0,1,1,1,1)`.

The sign-safe conductor-eight projection theorem gives two cases, `c=0` and
`c=2`. It uses actual positive restriction rows, not an assumption that the
raw Galois transport matrix preserves the positive cone. The exact
two-primary difference-square masses are `c,c,2c,4c` at orders `1,2,4,8`.
Duality makes `c` even and the local projection bound gives `c≤2`.

The phase and cyclic equations use the trace field
`K=Q(sqrt(5),zeta_8)` and the source-character field
`L=Q(sqrt(5),sqrt(-2))`. The all-order arithmetic proof yields exactly 61
relative moment records for powers `1,2,4,8`, represented by the 320th roots
and a true-zero record. The latter has source-fixed packet monoid generated
by 16 and 5, with the additional conditional packet divisibilities stated in
`POWER_MOMENT_PHASES_PROOF.md`. No finite upper bound on the Frobenius–Schur
exponent is assumed. C4 and C8 eigenspace multiplicities are nonnegative
integers, using the exact block-rotation identities and the integral basis
of `Z[zeta_8]`.

## Exhaustive finite contradiction

For each of the two label classes, the complete `c=2` system has an integral
covector modulo 256 annihilating every column while taking value 128 on the
right-hand side. Each certificate has support 86 and checks all 1,700
columns. These are exact whole-branch contradictions.

For `c=0`, the independently reconstructed aggregate allocations and exact
inactive lattice quotients enumerate 615 phase allocations and leave four.
For each, the C4 rotation space of source object 1 has five possible integer
choices; exact lattice/Farkas replay leaves only `(3,1,0,0)`.

The conductor-five difference-square allocation has 1,004 raw possibilities,
of which exactly 50 satisfy the residual source Gram conditions. Exact
separating covectors exclude 184 of the 200 phase/allocation combinations in
label class 0, and 192 of 200 in label class 1. The remaining 24 combinations
are not discarded by numerical tests.

The eighth-indicator `sqrt(10)` and `i sqrt(10)` equations, together with exact
Gram capacities, force one order-320 packet of multiplicity 16 in orbit 50.
Each of the four active phases allows two choices for that packet. Other
phase contributions in orbit 50 remain allowed. Consequently the remaining
24 combinations yield exactly 48 final branches.

For each branch the replay independently reconstructs packet pruning and
all orbit-capacity inequalities from the raw source induction Gram. Capacity
maxima are checked by direct integer scans and rounded only by the gcd of
the remaining packet units. Every final branch has a complete two-leaf
integer split certificate, for 96 exact Farkas leaves in total.

All 48 final trees split the same original integer variable: the multiplicity
of the eigenvalue `-i` in the C4 rotation space for source object 5. One leaf
excludes values at most 18; the other excludes values at least 19. Together
they exclude every integer value. The certificates do not need or assert
that this variable is exactly `18.5`.

The final Farkas rays use Gram, first/second moment, STS, a prime-budget
equation, the independently reconstructed integer fusion-norm cut, C4, and
capacity/bound rows. Their C8 coefficients vanish: C8 is essential earlier
in restricting the possible phase packets. The final rays also have zero
coefficients on the all-word and low-Verlinde blocks. The full replay still
regenerates those blocks and their bound data, so no unverified stored
constraint is silently introduced.

## Reproducible verification

From the repository root, run the Python interpreter with
`evidence/rank7_m5_20261020/models/sqrt5/verify_r5039_cyclic_chain.py`.
Repeat with `-O`. An optional `--output PATH` writes the resulting receipt;
the `verify` callable itself makes no repository changes. The signed
enumeration compiles its generated C++ search only in a private temporary
directory, which is deleted afterward. Legacy receipt writers are captured;
regenerated inventory writes are compared to the existing source-bound
inventory instead of replacing it. Any missing branch, changed source,
changed constraint, failed covector, or unexpected output write raises an
exception before a complete PASS receipt can be returned.
