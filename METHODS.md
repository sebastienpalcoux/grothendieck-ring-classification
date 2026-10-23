# Case-specific reductions and exact certification

The campaign aims at new exclusions. All systems are necessary conditions
under the spherical, center and Galois reductions cited in the pinned
source notes. A model contradiction is not silently promoted to a census
status update. A feasible model does not establish categorifiability.

## R928 and R941: actual twist orbits and rotations

The inherited restriction-column domain is complete. Its character vectors
are injective over Q(sqrt(2),sqrt(3)). Squared modular Galois action therefore
fixes each relevant type under the subgroup fixing Q(zeta_24).
The saturated dimension norm is 147456 = 2^14 * 3^2, so only primes 2 and 3
can divide the conductor. For a root order 2^a*3^b its squared-subgroup
orbit has size 2^max(a-4,0)*3^max(b-1,0). A type has at most eight objects,
forcing a root order dividing 1152. Actual roots are partitioned into these
finite orbits; a phase variable counts multiplicity **per root**, integrally.
Semion and fermion translations preserve the appropriate charge rules.

Orbit power sums lie in Q(zeta_48). For a rotation order n, the full Fourier
equations are evaluated in Q(zeta_lcm(48,n)); the order-nine test genuinely
uses Q(zeta_144). Rotation multiplicities are nonnegative integers bounded
by the exact Hom-space dimension. Subtracting its quotient by n from each
multiplicity controls coefficient magnitudes without changing the system.
The two surviving spectral endpoint mixtures are rational continuous
parameters. Full STS, source spectral-fibre and indicator-field equations
remain coupled to the same actual-root counts.

All 4 R928 and all 14 R941 inherited branches are included. Default
rotation orders are 3,4,6,8,9,12,16. Higher orders may strengthen a model;
this choice does not restrict the allowed twists. Detailed proofs,
including source assertions, are in cases/R928_R941_THEORY.md.

## R1154: completing the distinguished fusion matrix

All 25 accepted pair histograms are retained. For each, the unknown
distinguished matrix N1 is symmetric and nonnegative integral, with finite
entry bounds imposed by nonnegativity of N3=N1+K3 and N4=K4-N1. Each free
entry uses a complete one-hot finite domain. Known packet matrices,
N2,K3,K4 and the forgetful intertwiner impose linear necessary equations.
A fixed combination of all forced commuting matrices yields necessary
joint commutant equations. Exact source characters determine the low and
packet spectral columns, trace and squared trace.

Pair-word vacuum vectors are fixed by the accepted histogram. Their
degree-five compressed moments are linear in N1 and add equations absent
from the previous relaxation. Every integer assignment then undergoes
exact tests of all available degree-six vacuum moments and the full
mandatory characteristic polynomial.

Only a complete assignment rejected by such an exact invariant may be
blocked. If one variable was selected in each one-hot group, their sum
is at most the number of groups minus one for all other assignments.
The rejection receipt, full assignment and cut are archived. Before a
final contradiction is accepted, every receipt is regenerated against
the original equality model, every cut is regenerated and checked, and
the exact strengthened model is reconstructed in order. This also
verifies that every rejected assignment satisfied the earlier cuts.
The resulting contradiction is then checked against that final model.

## R1768: coupling the integer center and the rational phase cone

The prior finite-fibre arithmetic has 40 branches: 39 exact rejections
and one surviving sector. The package replays all those certificates and
the known rational phase witness as controls. The surviving phase cone is
combined with the existing integer Gram/S/cubic and joint-Galois center
system, rather than treating those separately feasible tests as a new
exclusion search.

The 72*z and 18*(2*z) alternatives are both retained. Coupling uses the full
eight-coordinate restriction vector and exact source-character data.
Uniqueness of the alpha restriction and rational mass 52 are preserved.
Relative spectral phase masses are rational trace parameters, not counts
of simple objects; they remain continuous. Actual center multiplicities
remain integral.

All fixed variables are substituted using exact integer arithmetic.
The original models, free-variable maps, fixed assignments and retained
source-row maps are shipped. Deduplication occurs only after complete
equality of the normalized numerical systems; both original branch
records remain available. A projected witness lifts through the saved map.

## Numerical search and exact proofs

HiGHS supplies numerical MIP candidates and LP separation directions.
No floating-point status certifies infeasibility. Exact rational checks
accept witnesses, propagate integer bounds, generate verified cuts and
branch only on integer variables. Continuous variables are never rounded
to manufacture an integer obstruction.

For an equality model Ax=b and box l<=x<=u, a rational covector y proves
infeasibility only when y*b exceeds the exact box support of y*A.
A bound cut for a variable uses the full residual c-y*A and its exact box
support. Finite integer branching partitions the current integer interval
into exhaustive children; both must close exactly. All accepted cuts and
branch nodes are retained in a resumable journal and exported proof tree.

Inequalities are exported with continuous slack variables to a canonical
equality model. A separately implemented standard-library checker
recomputes rational support, cut validity and every branch. Its exported
model is compared to the standardized current search model. Exact
assignment-cut replay is additionally required for R1154.

Build validation includes positive rational mixed-variable witnesses,
LP and integer infeasibility controls, inequality/slack controls,
branching controls, candidate rejection and tampering controls,
case-specific source/coverage checks, complete model compilation and
short real-system solver runs. These validate implementation and finite
arithmetic. The analytic categorical reductions remain mathematical
prerequisites and must be reviewed along with any newly obtained closure.
