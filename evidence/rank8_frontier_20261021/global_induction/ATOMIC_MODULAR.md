# Character-labeled atomic modular relaxation

This is a necessary pseudo-unitary central-induction system. It is deliberately
weaker than the complete labeled-frame hull: its low constituents can be mixed
independently. Exact feasibility therefore asserts survival of this relaxation,
not a joint integral low frame or a category. A negative result is promoted to
general complex scope only after the complete oriented signed lift.

Assume the commutative rank-eight ring has all eight characters in its totally
real quadratic or biquadratic FP field. Let E0 be the FP character, fE the formal
codegree and betaE=D/fE. The tensor unit in the center is A_E0. For every E != E0
create a separate simplex over all allowed integral low restriction columns c
of dimension betaE, after the exact partial-S algebraic-integrality filter.
An actual category chooses one such column vE for each distinguished simple.

Use the ordinary Gram, first/second twist moments and proper-divisor rotation
constraints. Add the linear symmetry identities, for E,F != E0,

    betaE chiE(vF) - betaF chiF(vE) = 0.

Identities with E0 are automatic because chiE0 is the dimension character and
dim(vE)=betaE. The low coefficient of the (E,F) STS row on a choice (c,G) is

    chiE(c) chiF(c) - delta(G,F) fF chiE(c).

The high coefficient is the sum of chiE(v)chiF(v) on the complete duality orbit,
multiplied by the joint relative trace of the twist. Its right hand side is

    delta(F,E0) fF - 1.

Indeed the fixed tensor unit contributes 1 on the left, and v_E0=1 makes the
right side fF when F=E0; for all other F the right side is linear in the choice
of vF and is moved into that simplex's column. This is precisely the already
reviewed center relation sum_Z thetaZ chiE(vZ)chiF(vZ)=fF chiE(vF).
All characters and coefficients here are in the relative-trace field, so the
trace multiplication is valid. Complete dual pairs have equal twists and are
retained with their full Gram contributions. No complex phase is discarded.

Every complete actual labeled frame maps to one-hot choices in these simplices,
so all actual categories satisfy this system. The full finite-domain oracle is
checked over integers. Numerical LPs propose rational primal solutions or integer
separating rays; neither is accepted until every equation or every complete-domain
column is checked exactly.

`verify_atomic.py` compares every labeled complete low frame in the known model
Fib tensor Vec(V4) against the atomic S-symmetry and STS defect, including the
fixed tensor-unit term; compares the complete oracle against direct columns;
checks all twelve actual central restriction types; and replays an exact rational
positive-control primal. Numerical rediscovery requires `--rediscover --write`.
The previously used model R334 is inapplicable to this narrower real-FP adapter:
its full character table does not split in its FP field. That preflight failure
is recorded and is not a categorical obstruction.
