# Phase compatibility of fixed integer restriction patterns

This is a specialization of the already verified full central induction,
rotation and distinguished-STS necessary cone, not a new assumption about
integer trace weights.

Fix a complete labeled low frame, or fix one allowed low column for each
distinguished character in an atomic cone. Give each chosen low column
coefficient one. For every high restriction-duality orbit O with a positive
integer multiplicity n_O, retain all relative-phase columns belonging to O
and append the equation `sum_tau x_(O,tau)=n_O`. Set all other high columns
to zero. Retain all proper-divisor rotation columns. Subtract the fixed low
contribution from the original right-hand side. The source indicator cases
remain the original complete finite list.

The variables x are nonnegative rationals in this relaxation. They encode
compressed relative phase traces and are not required to be integers.
Every categorical center with this exact integer restriction pattern gives
a feasible point, because each actual central simple contributes one unit
to its restriction-orbit count. A feasible exact primal is additionally
expanded back to the complete frozen source cone and checked there.
An exact separator is checked against every specialized column and its
indicator right-hand side; repeated separators may share their already
verified, unchanged column inequalities.

If all indicators are separated, only this selected integer pattern has
been ruled out. Other integer patterns may exist. In particular rejection
of both sampled R982 witnesses would not exclude R982. Conversely an exact
phase-compatible integer pattern is still only a necessary-system witness:
it is neither a full modular datum nor a categorification.

`phase_mass.py` is the reusable atomic or complete-frame specialization.
`r982_phases.py` is the independent fixed-frame implementation for the two
source-bound R982 integer witnesses. Numerical phase-I optimization is used
only with explicit discovery; default replay checks saved exact primal or
dual certificates and does not import SciPy.
