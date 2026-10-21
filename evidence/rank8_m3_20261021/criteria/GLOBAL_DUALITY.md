# Duality balance in global central induction

This is an isolated refinement of the global convex central-induction
relaxation in `GLOBAL_CONVEX_INDUCTION.md`. It uses the same complete low
columns, full-Gram high columns, phase traces, moments and rotation equations.
It does not modify previously accepted global certificates.

Work first in a pseudo-unitary category with its canonical spherical
structure. Its Drinfeld center is ribbon. For every central simple object
`Z`, duality preserves its dimension and twist: `theta_(Z*)=theta_Z`. The
dual of a scalar morphism is the same scalar, not its complex conjugate.
Forgetting to the original category commutes with duality. Thus if the
restriction vector of `Z` is `v`, that of `Z*` is the vector `v*` obtained
by permuting the coordinates with the source ring's duality. Their complete
relative phase-trace tuple is identical. Consequently the number of high
central simples of type `(v,tau)` equals that of type `(v*,tau)`.

Partition the high variable labels into these involution orbits. Replace
the two variables in a two-element orbit by one common nonnegative variable;
equivalently replace their two coefficient columns by their sum. Keep
self-dual high labels, all low variables, and all auxiliary rotation
variables unchanged. Every genuine central induction decomposition still
satisfies the resulting system. An exact row functional with nonnegative
coefficients and negative right side is therefore an obstruction. Equality
between the low variables of dual constituents could give further
conditions, but is not used here.

The implementation checks that source duality is an involution, the
complete high-column set is closed under it, paired dimensions agree, the
pairing is involutive, and every original variable belongs to exactly one
contracted class. The exact replay reconstructs the contracted matrix and
checks the full Farkas functional. An accepted general-complex conclusion
additionally requires the unchanged complete sphericalization/oriented
signed lift, as for the base global criterion.

The separate kind is `global_duality_induction_lift`, and its replay runs
in an isolated process, including any parameterized biquadratic field.
`verify_global_duality.py` checks every contracted coefficient against the
original matrix, five complete exact substitution vectors, and the full
partition on three source-bound examples. Known models R334 and R475
survive. The existing exact rays for R1453 still separate the contracted
system and are rechecked; this is a validation control, not a new exclusion.
No timeout, memory limit, or failed numerical reconstruction is an
obstruction.

The completed application R8_3_986 has 197 equations and 52,718 variables,
down from 97,768 variables before contraction. Its 2,863 high columns form
1,538 duality orbits, each paired with all 34 relative trace types. Both
second-indicator branches have exact separators, and the complete
oriented-sphericalization certificate closes all 16 signed branches. The
saved result is `advanced/global_family/R8_3_986.json`. A separate isolated
targeted replay under `python -O` checked the full general certificate.
The related R8_3_65 completed its bounded contracted attempt with no
conclusion; no model is inferred from that outcome.

For numerical discovery, the phase-I formulation
`A x + s_plus - s_minus = b`, with all variables nonnegative and objective
`sum(s_plus+s_minus)`, uses the small number of equality rows. A positive
optimum has dual multipliers satisfying `A^T y <= 0`, `b^T y > 0`;
negating them gives the convention used by the exact checker. Rational
reconstruction may use the proposed tight face, including rational choices
for its free parameters. Every resulting coefficient and the strict
negative right side are checked as integers. The solver is used only to
propose certificates. `verify_global_phase_one.py` replays the saved exact
negative control and binds the positive control to its verified model
without importing SciPy; `--rediscover` optionally reruns numerical search.
