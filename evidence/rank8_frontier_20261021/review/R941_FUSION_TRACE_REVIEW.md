# Permutation and mixed fusion traces for the forced R941 fermion

This is an additive necessary test. It does not modify the frozen earlier
phase or integer-witness receipts.

In the established pseudo-unitary Galois conjugate, the forced central
fermion G has G²=1 and twist −1. Its fusion matrix N_G is an involutive
permutation matrix. Modular diagonalization gives its eigenvalue at a
central simple Z as the monodromy charge M_G,Z in {+1,−1}. Therefore

    number of G-fixed central simples = Tr(N_G) = P−N,

where P and N count the positive- and negative-charge simples. Balancing
shows that a G-fixed simple must have negative charge. The ten known
distinguished objects and their translates form five nonfixed pairs.
For a fixed high restriction type j, its q_j negative-charge objects
form an involution with a fixed count f_j satisfying

    0 <= f_j <= q_j,       f_j = q_j mod 2.

Thus a necessary and sufficient combinatorial condition for the required
number of fixed points within these separate type sets is

    sum_j(q_j mod 2) <= P−N <= sum_j q_j,
    P−N = sum_j q_j mod 2.

Here P=8+2 sum p_j and N=2+sum q_j, with p_j the already enumerated
positive-charge pair counts. This gate retains 71 of all 93 complete
charge allocations. Of the sixteen exact paired-phase survivors, it
removes precisely allocation 4 (pattern40), whose required fixed count
is −2, and allocation86 (pattern236), which requires13 fixed simples
among only7 eligible negative-charge high objects.

More generally, a product of fusion matrices is a nonnegative integer
matrix. Hence for each e in {0,1} and every monomial in the four nonunit
distinguished fusion matrices,

    Tr(N_G^e N_A1^a1 ... N_A4^a4)

is a nonnegative integer. These matrices commute in the braided center.
The script reconstructs all simultaneous eigenvalues directly from the
source tensor's characters, dimensions, and formal codegrees, using the
noncommutative S scale D/(f_E dim E). It then checks all 420 such traces
with sum a_i<=6 for every one of the 93 charge allocations. These tests
remove no additional allocation beyond the fixed-point gate. This is a
finite degree-six test, not a claim about all monomial degrees.

The actual nine-simple center Z(Ising) is an independent positive control:
the script constructs its integer fusion matrices, verifies the three
actual fermion-fixed simples, and compares 56 mixed traces with their
modular eigenvalue formulas. No numerical optimization enters this test.

After intersection with the frozen paired and integer campaigns, fourteen
exact rational solutions and eleven exact nonnegative integer witnesses
remain. Three further integer-feasibility questions are unresolved. These
witnesses satisfy the stated finite constraints and are not categories.

Canonical replay is `verify_r941_fusion_traces.py`, with exact source-bound
receipt `r941_fusion_traces.json`; both normal and optimized Python replay
are required. The mechanism is ordinary permutation-matrix and fusion-matrix
trace positivity; no new classification theorem or novelty is claimed.
