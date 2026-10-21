# Independent review of the R1615 general-complex exclusion

The mathematical conclusion reviewed here is that R8_3_1615 has no
categorification by a complex fusion category. This is a separate AI review,
not human refereeing or proof-assistant formalization.

The complete-domain framework is the previously reviewed central induction
frame hull with partial modular eigenvalue integrality and distinguished
center STS equations. Its exact cyclotomic character table has eight distinct
characters and satisfies multiplication, duality, and orthogonality. The
relative trace field is Q(sqrt(2),sqrt(3)), inside Q(zeta_24).

The complete low-frame enumeration has 61,688 frames before distinguished-S
symmetry. Exactly two frames remain, with two character assignments each.
These four labeled choices are separate low columns in the cone. No low
restriction vector is discarded by eigenvalue integrality; 1,551 high
restriction vectors are discarded, leaving 3,003. Every retained high type is
fixed by duality. All 34 joint height-four trace types and the proper-divisor
rotation variables are included. The resulting cone has 341 equations and
102,141 columns. The eight indicator tuples are exactly
`(a,b,1,1,1,1,c)` with `a,b,c` independently equal to +1 or -1.

The reviewer independently reconstructed the 144 low STS features from the
unnormalized S-matrix equation. All 108,108 high character-pair coefficients
were independently evaluated in Q(zeta_24), checked real before any trace,
and compared with their relative-field coordinates. Thus no incorrect
replacement of Re(theta c) by theta Re(c) for an unpaired nonreal coefficient
is used. The normalization and categorical hypotheses are those recorded in
`../review/PARTIAL_S_STS_REVIEW.md`.

The direct verifier then builds every actual operator column and pairs it
with each of the eight saved integer rays. This additional separator check
does not use the producer's factored Farkas oracle. All column pairings are
nonnegative, and each right-side pairing equals the recorded strictly
negative integer. Five distinct rays suffice for all eight indicator tuples.
The complete score sequences are hash-bound in `r1615_direct.json`.

The first direct run used the producer's explicit column method, independently
of its oracle. The final read-only verifier additionally reconstructs the
high STS part by integer multiplication in the checked basis
`(1,sqrt(2),sqrt(3),sqrt(6))`. It requires the same complete score hashes.
The review shares the previously audited domain constructor, native complete
low-frame enumeration, and non-STS column primitives. It does not claim a
second independent implementation of those established components.

For general complex scope, the complete oriented signed enumeration has
eight branches and every branch is gauge-original. The ordinary spherical
dimension alternatives consist of two quadratic character components,
excluded by exact norm obstructions, and the quartic FP Galois orbit. Thus
the pseudo-unitary center obstruction applies after the certified Galois
reduction. The canonical general verifier checks the complete signed domain,
every gauge, every spherical character alternative, and the pseudo-unitary
certificate. Neither pivotality nor unitarity is imposed on the final
noncategorification conclusion.

The review receipt binds the source tensor and the complete producer
certificate. Its canonical read-only commands are:

```sh
python evidence/rank8_frontier_20261021/r1615_review/verify_direct.py
python -O evidence/rank8_frontier_20261021/r1615_review/verify_direct.py
```

Both stable-source commands passed on 2026-10-21. The general-complex
exclusion is accepted by this review.

The producer certificate is
`../global_induction/complete_results/R8_3_1615_sts_frame_h4.json`.
The release-wide canonical producer replay is
`../global_induction/verify_accepted_complete.py`.
