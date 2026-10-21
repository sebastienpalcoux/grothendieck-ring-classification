# Independent review of the R1055 complex-character exclusion

The necessary full-character-field atomic S system is derived in
`ATOMIC_SPECTRUM_REVIEW.md`. Here the full character field is
`Q(sqrt(37),sqrt(-3))`, with primitive element
`u=sqrt(37)+sqrt(-3)` and polynomial `u^4-68u^2+1600`.
S symmetry uses all four rational coordinates and no complex
conjugation. High twist moments remain in the real FP field.

The complete height-four system has211 rows and16695 columns:
5748 character-labeled low choices,352 complete duality orbits of566
high restriction vectors times31 trace types, and35 rotation columns.
The partial-S algebraic-integrality filter removes4949 low choices
(counting original domain occurrences) and553 high restriction vectors.
The two complete second-indicator assignments are
`[0,0,1,1,1,-1,1]` and `[0,0,1,1,1,1,1]`. Both have a saved integer
separating functional.

`review_atomic_complex_1055.py` independently checks every added
full-field S coefficient and every omitted FP equation, and compares
three factored-oracle score vectors against direct dot products of every
column. For each of the two separators it independently checks all16695
inequalities and the strictly negative pairing with the right-hand side.
It also replays the complete general signed lift. There are six spherical
character factors: four linear factors and a nonreal quadratic factor
force a zero simple-object dimension; the remaining quadratic factor is
the FP Galois orbit. All four oriented signed branches are gauge
equivalent to the original ring. Thus the final conclusion excludes
arbitrary complex fusion-category categorifications, with no pivotality
or unitarity assumption.

A genuinely complex-character positive control is included, rather than
relying only on a real field embedded into a complex field. The ring
`Fib tensor Vec(C4)` has nonreal characters and all12 known center
restriction types pass. An exact32-column rational feasible certificate
satisfies the complete atomic cone, with second indicators
`[0,1,0,1,0,1,0]`. Numerical discovery of that control is optional and
explicit (`--rediscover-control --write`); the ordinary replay uses
exact arithmetic only.

The no-argument replay is `python review_atomic_complex_1055.py`, and
the source-bound receipt is `review_atomic_complex_1055_results.json`.
The feasible control proves only that this necessary relaxation retains
a known model. The negative conclusion for R1055 uses the complete
separator and signed lift, not numerical LP status. No claim of a
complete joint-frame hull or an STS test is made.
