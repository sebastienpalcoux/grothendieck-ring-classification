# R928: complete fixed-pattern semion-orbit and correlated-pair tests

## Prerequisites and scope

The unrestricted signed-sector gate in `noncommutative_followup/` proves
that a hypothetical complex categorification has a pseudo-unitary Galois
conjugate. All following equations are imposed in that conjugate with its
canonical positive spherical structure. They therefore give necessary
conditions for general complex categorifiability, without assuming unitarity.

The complete source, full distinguished S-row integrality, integer Gram,
and distinguished Verlinde calculation in `quartic_integer_center/` leaves
343 integer restriction-multiplicity patterns. The independently verified
`review/verify_quartic_central_orbits.py` proves that every pattern forces a
unique central involution G over the nontrivial source invertible g. The
forgetful kernel is Vec. The earlier complete indicator domain forces
nu_2(g)=-1; the pointed order-two hexagon and balancing then give theta_G^2=-1.
The canonical positive pointed pivotal structure is essential here.

Tensoring with G has no fixed simple: the monodromy charge is +/-1,
whereas theta_G=+/-i, so balancing cannot preserve a simple twist. The
restriction vectors with canonical indices 0,...,39 are fixed by g and
therefore have even multiplicity. Exactly 15 of the 343 patterns satisfy
this condition. Each of the five distinguished low objects translates to
high index 40,41,42,43,57, respectively, with multiplicity one. Their
relative twist moments through height six are (0,-1,0,1,0,-1).

The forced semion is a structural necessity, not a tensor-factorization
claim about the original fusion category.

## First complete coupled test

`verify.py` reconstructs the complete height-six rotation system and the
full distinguished STS equations, including the normalized matrix character
D/(f_E dim E). It fixes all65 high multiplicities to one of the15 integer
patterns. For the fixed restriction types it imposes zero second and sixth
moments; it fixes all six moments of the five translated low objects.
The previously excluded positive-indicator branch is replayed exactly.
The double-semion center Z(Vec(C2)^omega) supplies an actual known-model
STS and semionic-moment control.

All15 systems receive exact certificates. The indices 2,6,61,64,199 are
infeasible by integer Farkas separators. The other ten indices
40,44,49,58,186,191,196,243,245,248 have nonnegative rational primals checked
against every original equation. No numerical status is used as a proof.

## Correlated pair strengthening

The independent `review/semion_pair_traces.py` enumerates exactly30 complete
joint relative trace types

    Tr_K(theta^k + (i theta)^k),  k=1,...,6,

where Tr_K is the normalized relative trace to K=Q(sqrt2,sqrt3). Both signs
of the ratio are covered by interchanging the pair. The finite order bound
is288. This is the same prime-power bound used for the individual linked
traces: primes are2 and3, and valuations beyond the bound make every one
of the six relative traces zero. Multiplication by i cannot cancel such
an excessive valuation. The all-zero tail type is included.

The checker independently averages all288 exponents in Q[zeta_288] over
the24-element subgroup fixing K. Its actual pair1,i is a positive control.
The complete proof and bound are the biquadratic relative trace theorem
already used in the rank-eight manuscript, applied to both roots jointly.

`pair_rotation.py` finds an exact decomposition of each correlated pair
type as a sum of two old linked types. It replaces each of the40 fixed
restriction blocks by the30 sums of the entire old columns. Thus all Gram,
multiplicity, rotation, STS, and additional moment rows are preserved;
pair variables contribute mass two. The25 other high blocks and every
auxiliary rotation block remain exactly once. Equality of all six
field-coordinate moments proves that the chosen decomposition cannot
change any equation. This yields873 rows and2227 variables per pattern.

All ten remaining patterns have exact nonnegative rational primals in this
stronger system. These are feasible necessary data only: they do not specify
integer root multiplicities, modular fusion data, associators, or a fusion
category. R928 remains unresolved.

## Joint integral-matrix spectrum

`joint_spectrum.py` checks all343 integer patterns for each of R928 and
R941. For each low or high central restriction Z it constructs the whole
five-component eigenvalue tuple

    (D chi_E(FZ)/(f_E dim(E) dim(Z)))_E.

All five low central simples are counted once, including the one whose
induction multiplicity is two. The five center fusion matrices commute
and have integer entries. Applying a field automorphism to their common
eigenvector equations gives a semilinear isomorphism of the corresponding
joint eigenspaces. Their joint eigenvalue multiplicities must therefore
be Galois invariant, with the matrix labels E held fixed. This remains
valid for a noncommutative source ring because these are fusion matrices
in its braided center.

All four automorphisms of Q(sqrt2,sqrt3) are checked exactly. Each ring
retains255 of343 patterns. All15 semion-parity R928 patterns pass, so this
is an independent finite strengthening of the earlier common domain,
with no further reduction of the final R928 candidates. An actual Z(Fib)
control verifies the integral fusion matrix, its S eigenvectors, and the
nontrivial joint Galois multiplicities.

The additive `charged_joint_spectrum.py` also checks the93 corrected R941
monodromy-charge allocations from `quartic_integer_center/r941_charges.json`.
Adding the rational eigenvalue of N_G keeps all93 allocations across68
patterns. This auxiliary result binds the corrected receipt hash and
makes no assertion of R941 categorifiability.

## Integer pair-type and rotation-eigenvalue counts

For each actual central G-orbit, taking normalized relative trace changes
its tuple values, not the number of such orbits. Consequently every pair
type count is an integer. The unchanged high variables similarly count
central simples, and the auxiliary variables count actual tensor-rotation
eigenvalues: their builder has coefficient-one mass rows equal to
`dim Hom(1,X^n)`. All are necessary nonnegative integer counts.

`integer_counts.py` first tests the exact integer equations modulo
2,3,5,7,11,13. Each variable has a finite upper bound obtained directly
from a nonnegative equation. The subsequent numerical integer search is
bounded by30seconds and20000nodes per pattern. A purported solution is
accepted only after rounding and exact verification of every one of the
873 original integer equations. It yields four exact integer witnesses,
at patterns40,49,186,191. They are necessary data, not fusion categories.

For patterns44,58,196,243,245,248, the numerical solver reports
infeasibility but supplies no accepted proof. Their integer feasibility
is explicitly unresolved. `integer_support_lattice.py` independently
reconstructs the nonnegative-row bounds, removes every variable forced
zero, and repeats all six modular tests on this restricted support. These
also pass. No numerical infeasibility is promoted to an exclusion, and
no unresolved integer search is counted as a completed exclusion test.
The four exact integer witnesses are a stronger positive necessary-data
result than the rational relaxations.

## Read-only replay

```
python evidence/rank8_frontier_20261021/r928_semion_rotation/verify_all.py
python -O evidence/rank8_frontier_20261021/r928_semion_rotation/verify_all.py
```

The entry point checks the complete finite campaigns, joint spectrum, and integer research receipts and their source-bound
receipts. The independent central-orbit and pair-domain checkers are also
registered separately in the global research verifier.
