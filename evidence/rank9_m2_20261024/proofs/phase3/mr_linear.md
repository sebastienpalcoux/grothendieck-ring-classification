# Bounded mixed Moore--Read action check

The former Z3 timeout for `(p,r,v)=(2,15,1)` was replaced by exact sparse
linear elimination over Z/2^k. The equations are exactly those in
`phase2/weak_integral/mr_mixed_action.py`: every tensor-functor associator
entry, C2 square coherence, central-boson transport, and algebra equivariance.
The system has664 variables and19,169 equations.

The algorithm pivots on an odd coefficient, whose inverse exists modulo2^k.
It substitutes that variable in the other equations. When every remaining
coefficient is even, an odd right side is a contradiction; otherwise the
system divides by2, reducing the modulus. Zero rows and duplicate rows are
checked for contradictory right sides. These operations preserve solvability.
Any positive result would be replayed against every original equation.

The tested16th-root and32nd-root phase systems are both inconsistent:

|Phase group|Output|Elapsed seconds|
|---|---|---|
|Z/16|mr_linear_2_15_1_4.json|29.8|
|Z/32|mr_linear_2_15_1_5.json|26.7|

This is a completed negative test of these two finite-phase ansatzes. It
does not rule out higher-root or arbitrary complex tensorators, and does
not exclude any of the remaining rank9 fusion rings. No categorical model
or based tensor was inferred from this failed action search. Further mixed
actions and all neutral categories remain unclassified.
