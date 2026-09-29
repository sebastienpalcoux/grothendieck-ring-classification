# Independent audit of the higher stabilizer sieve

The tensor-parametric engine `software/stabilizer_rotation_higher.py` was
reviewed independently of its discovery run. The categorical input is the
Clifford proposition in `papers/chapters/stabilizer_rotation.tex`, whose
universal algebra identities are replayed by `clifford_rotation.py`.

For a fixed simple object Y the cubic multiplicity is
`N[Y][Y][dual(Y)]`. Self-duality of Y is unnecessary. A diagonal -1 in the
anti-invariant action of the involution records the exchange of its two
right-module structures, exactly the hypothesis of the categorical
proposition. Positive odd cubic multiplicity is immediately impossible.

For even cubic multiplicity n, the normalized relative Galois average of
the third indicator over a real field belongs to

`{n/4 - 3a/2 : 0 <= a <= n/2}`.

When the Cauchy prime support omits 3, its smaller rational value set is
`{-n/2 + 3b : 0 <= b <= floor(n/4)}`. The engine uses these complete value
sets, with exact rational arithmetic.

The initial interval relaxation introduces two nonnegative rational
variables z,w. The added indicator row is

`high third-twist sum + Delta*z = (n/4)*Delta - low contribution`,

and `4z+4w=3n`. Consequently the averaged indicator equals `n/4-z` and
lies in `[-n/2,n/4]`. The same rational variable z occurs with coefficient
Delta in every coordinate of the number field. This is essential: the
implementation does not accidentally impose unrelated coordinate bounds.

All high-column variables are mapped back to their original labels before
the third-power trace is read. The character-refinement keep-map matches
the filtering in `modular_character_induction.equation_system`; existing slack
variables contribute zero. When the full character field exceeds the FP
field, the engine retains the full base rotation system and omits that
character refinement. It does not substitute traces over an incompatible
field.

Failure to find an interval ray never counts as exclusion: the discovery
engine then requests an exact ray for every tuple of allowed discrete
indicator values. If any tuple survives, that conditional obstruction
fails. Every ray is checked using integer inequalities after reconstructing
the system.

The verifier reconstructs all involution-module representations and checks
their ordered list. Each is rejected either by an odd Clifford dimension,
a complete conditional trace certificate, or the independent full Morita
rank/Gram obstruction. Conditional certificates reconstruct every low
frame, every character labeling when applicable, and every second-indicator
assignment. Their object sets, cubic dimensions, field, prime support,
trace height, matrix metadata, and conditional references are checked.
Unused conditional certificates are rejected.

The general-scope wrapper additionally verifies the unrestricted signed
sphericalization/Galois pseudo-unitarity reduction. A pseudo-unitary
certificate alone is not promoted to general scope.

For R6_4_416 the complete certificate has two involution-module branches,
both using the fixed objects 4 and 5 of cubic multiplicity four. Its field
is Q(sqrt(2)), its Cauchy prime support is {2,5}, and its individual rational
indicator domains are {-2,1}. The 895 low frames yield 32 required central
systems; all are excluded already by the interval relaxation.

The complete R6_4_416 pseudo-unitary certificate was independently replayed
successfully with `python -O software/stabilizer_rotation_higher.py
R6_4_416 --output research/round2_theory/R6_4_416_higher.json --verify`.
The separate general wrapper also has a successful optimizer-disabled
optimized replay, recorded in
`research/round2_center/general_replay_416_report.json`: it checks 2,376
signed quotient tables in 83 sign orbits before the complete higher sieve.
