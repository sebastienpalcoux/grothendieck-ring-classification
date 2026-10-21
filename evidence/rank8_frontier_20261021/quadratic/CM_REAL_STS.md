# A modular STS strengthening for quadratic CM character fields

The new `AtomicCMRealSTS` class is isolated in `atomic_cm_real_sts.py`.
It retains every full-field S-symmetry row of the reviewed atomic
spectrum cone. It adds a necessary STS system without enlarging the
relative twist-trace field when the full character field is
`L=Q(sqrt(q),sqrt(-r))` and the FP field is its conjugation-fixed field
`E=Q(sqrt(q))`. In the R65 application, `(q,r)=(5,1)`.

For distinguished central simples, the modular identity gives

\[
 \sum_Z \theta_Z\chi_A(v_Z)\chi_B(v_Z)
   = f_B\chi_A(v_B).
\]

Let `pi=(1+conjugation)/2:L->E`. Apply the normalized relative trace to
E from a common field containing L and the twists. Distinguished
simples have twist 1, so their contributions become
`pi(chi_A(v)chi_B(v))`. On a complete dual pair of high simples, the
characters satisfy `chi_A(v*)=conjugate(chi_A(v))` and the two twists
are equal. The summed character product is therefore fixed by complex
conjugation and belongs to E. This coefficient factors out of the
relative trace of the twist. The normalized trace of a twist is exactly
the existing FP-field trace type, by the tower property. Thus no
additional phase field or phase types are silently assumed.

For the low choice `(v,G)`, the added coefficient is

\[
 \pi\bigl(\chi_A(v)\chi_B(v)
       -\delta_{G,B}f_B\chi_A(v)\bigr).
\]

The right-hand side is `pi(delta(B,FP) f_B - 1)`: the fixed central unit
is included exactly once. The high coefficient on a complete duality
orbit is its unprojected character-product sum, verified exactly to be
conjugation-fixed, multiplied by the ordinary joint FP twist trace.
All coefficients are reconstructed exactly in `[1,sqrt(q)]` before
scaling. The class checks every reconstruction; merely discarding
nonreal coordinates would not be valid.

This is still a necessary atomic relaxation with independent low-choice
mixtures, not a classification of joint frames or modular categories.
An exact feasible certificate means survival of this stronger test.
A negative result needs the complete general signed lift before it can
be used outside pseudo-unitary scope.

`review_cm_real_sts.py` uses the genuinely nonreal known model
`Fib tensor Vec(C4)`. It checks an exact feasible primal, all 12 actual
central restriction types, all added low/high/right-hand-side entries
by direct field arithmetic, three complete oracle score vectors, and
all packed discovery columns against the original exact column builder.
It additionally records the two fast-column controls for
`Fib tensor Vec(C2 times C2)`: all 419 atomic-real columns and all 988
complete-labeled-frame columns. Numerical discovery of the positive
primal requires `--rediscover --write`; ordinary replay is exact-only.
The packed phase-I adapter is only a proposal mechanism. Its output is
accepted exclusively by the original exact primal or full-domain
separator verifier.

For R3472 the full real character field is strictly larger than the FP
field. The above CM projection does not apply. Its current full-field
S test must not be described as an STS test; an enlarged relative phase
field would be a separate research domain.
