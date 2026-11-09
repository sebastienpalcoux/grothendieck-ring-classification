# Positive and adversarial regressions

The principal runner executes all 54 checks in `regression.py` normally and
under Python `-O`. The reports give the exact rejection messages. Tests accept
valid certificates and reject deliberate corruptions without changing the
release ledger. A negative test requires the verifier's explicit mathematical
rejection, rather than an incidental exception.

The checks cover omitted character or low-part branches, duplicated branches,
incorrect induction rows, missing positive-dimension proofs, null witnesses,
incomplete formal-codegree roots, false strict signs, invalid arithmetic data
and false model identifications. The retained false Rep(A4) exclusion must be
rejected because it supplies no violated local condition. Witness selection
for the d-number test is also checked under reversed factor-discovery order.

The seven checks in `stages_regression.py` accept the fifteen-model endpoint and reject a missing
model, an extra nonmodel, missing or duplicated records, incorrect stage counts
and misassigned criteria. Failed runs must replace any old PASS report with a
failed status. The five exclusion stages end at `central`; `models` additionally
replays the model certificates.

## Cyclotomicity

Positive controls include cyclic cubic, cyclic quartic and biquadratic fields,
a product of quadratic factors, and repeated quadratic factors. Nonabelian
cubic, dihedral quartic and symmetric quartic examples must be excluded.
The tests reject unrelated or malformed polynomial factors, false nonabelian
claims for abelian fields, and a false exclusion of Rep(A4). The independent
checker also validates the actual codegree witness and rejects a false one
using its separate root-field splitting calculation.

## Fourth-indicator witnesses

R2 is a positive control for the fourth-indicator corollary in Section 3.
Its four low-part branches have floor 16 and positive gaps 108, 76, 44 and 44.
The verifier checks both exact inequalities defining the floor. Tests supply
false floors 15 and 17 with matching recomputed gaps; these must still be
rejected. Further mutations use a boolean, float, string, missing floor or
zero gap. Pointed controls test self-dual and non-self-dual objects, including
an integer boundary and rational offsets of size `10^-40` on either side.
The independent central verifier separately checks valid and corrupted
fourth-indicator witnesses.

## Generic row reduction

`linear_box_regression.py` compiles `linear_box_regression.cpp` and compares
the exact row-reduction solver with exhaustive five-variable integer boxes.
Cases include zero rows, inconsistent systems, negative pivots, rank drops
and signed interval endpoints. The normal regeneration runner and deep replay
include this check; compiler-free replay omits it.
