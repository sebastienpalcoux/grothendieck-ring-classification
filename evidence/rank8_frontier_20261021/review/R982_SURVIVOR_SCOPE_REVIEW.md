# Independent review of the final R982 arithmetic and selected-phase scope

The final evidence leaves R8_3_982 unresolved. It contains exact survival
witnesses for specified arithmetic relaxations and exact phase contradictions
for two specified integer restriction patterns. These do not exclude all
integer patterns in either frame, and do not exclude the source ring.

`verify_r982_survivor_scope.py` reconstructs the complete four labeled-frame
domains from the frozen source and the reviewed shared integer equations.
It checks saved witnesses by direct rational accumulation against every
original row and every original finite bound. It does not accept a numerical
optimizer status and does not use compressed-system satisfaction as a
substitute for the original equations.

For frames 0 and 1, the source-unit strengthened systems have 8,216 equations
and 1,091 variables. Their saved rational points satisfy all equations and
bounds exactly. The review claims continuous feasibility only: these
points do not certify integer feasibility, a center, or a category.

For frames 2 and 3, the saved integer points satisfy all 12,378 original
equations and bounds on 1,544 variables. The review separately reconstructs
the simultaneous seven-matrix eigenvalue tuples and checks their exact
multisets under all eight automorphisms of Q(zeta_24), keeping the object
labels fixed. It also directly checks all 28 source-unit product identities
from the source tensor and saved distinguished fusion coefficients.

The same two integer points are then specialized in the complete height-four
phase cone. The reviewer independently aligns every positive restriction
duality orbit by its full vector, retains every trace type for each such
orbit, and retains every rotation auxiliary column. The fixed low frame is
moved to the RHS. Each selected domain has 885 columns. For every one of
the eight indicator choices in each pattern, it checks the exact separator
against every column and its own exact RHS. All sixteen negative certificates
pass. Thus those particular integer points cannot extend to the required
phase data. No exhaustion of other integer solutions is asserted.

Canonical no-argument replay is `verify_r982_survivor_scope.py`; the
source-bound receipt is `r982_survivor_scope_review.json`. Normal and
optimized Python replay check identical data and mathematical scope.
This target review complements the independent shared integer-theorem and
actual-center controls; it does not replace the producer's signed-lattice
or domain-enumeration certificates.
