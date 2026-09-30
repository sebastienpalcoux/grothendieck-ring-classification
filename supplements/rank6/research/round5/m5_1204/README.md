# Exact reduction of R6_5_1204

The ring remains unresolved. The new argument gives a complete finite list of
171 necessary induction profiles; a surviving profile is not a categorification,
a modular datum, or a fusion ring for the center.

The common criterion combines the restriction Gram matrix with low-word fusion
coefficient Gram matrices. Their mixed entries are the restrictions of the
products. Every central simple gives a nonnegative integral joint column in the
rational image of the joint Gram matrix. Exact Schur bounds enumerate all such
columns, separately for each restriction type. Count, Gram, restriction,
Galois, and twist equations then give exact necessary linear systems.

For this tensor the complete low domain has 39 frames. Two admit character
assignments. Frame 20 is excluded by the two inherited exact full-character
rays. Frame 21 has three identical low columns, so its six character assignments
are equivalent under their permutations. No character branch is omitted.

In frame 21, 165 exact separating-ray steps give integral lower and upper bounds.
Exhaustive affine enumeration has 293,972 nodes and 39,800 profiles. Low-word
integrality through degree six and nonnegative restriction remainders retain
1,833 profiles. These determine 43 joint quadratic-word Gram matrices.
The joint coefficient equations exclude 1,568 profiles by exact rays; the
height-three twist equations exclude 91 more; two further profiles fail an
exact parity equation. A cubic-word joint Gram certificate removes one more profile. Exactly 171 profiles remain in this necessary domain.

The general-to-pseudo-unitary reduction exhausts 512 signed quotient tables in
16 sign orbits. Thus this necessary-profile reduction applies to every complex
categorification of the given based ring, not only to an assumed pseudo-unitary
categorification.

Run from the package root:

```sh
python -O software/round5_1204.py
```

`profile_certificate.json` is the compact certificate. The replay reconstructs
the entire domain and disables numerical linear and integer optimization.
`remaining_profiles.json` supplies the retained induction columns in sparse
form. `joint_domain_certificate.json` is an inspectable copy of the complete
joint-column domains. The C++ search uses exact bounded integers; its rational
image and prefix Schur tests have an independent Python cross-check in
`../unification/native_1204_domain_crosscheck.json`.

Additional explorations distinguish necessary feasibility, numerical timeouts,
and proofs. Height-six rotation/twist ray discovery found no additional exact obstruction
among the 174 profiles before the final parity and cubic cuts. Refined variables coupling each joint coefficient
column to a twist type add the ribbon balancing identities, but the bounded
initial probes still have feasible relaxations. These observations do not alter
the canonical classification status.
