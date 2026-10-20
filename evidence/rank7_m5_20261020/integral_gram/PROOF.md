# Integral center data and finite active-row branches

This directory records necessary conditions and exploratory integer solutions
for `R7_5_3895` and `R7_5_5039`. A feasible solution is **not** a fusion category,
a modular datum, or a categorification certificate. An optimizer's infeasibility
status is also not accepted as an exclusion certificate.

## Integer phase multiplicities

Under the pseudo-unitary reduction established separately, a central simple
object has a nonnegative integral restriction row. The conductor-five Galois
transport and categorical duality act on these rows. Their joint row orbits have
equal multiplicity for each normalized relative trace pair
`(Tr(theta), Tr(theta^2))` in the ten-value Cauchy-restricted set. Consequently the
corresponding orbit/phase variables are nonnegative **integers**.

There is an additional parity restriction. Choose a cyclotomic automorphism
nontrivial on `Q(sqrt(5))` and fixing the other source character fields. Its
action on twists is `theta -> theta^(u^2)`, where `u^2 = -1 (mod 5)`. Every
nonrational trace type has fifth-primary order exactly five. If the transported
row equals the original row, or its dual, compose the action with categorical
duality when necessary. The resulting permutation preserves that restriction
row, while every odd iterate changes the fifth-primary part of its twist.
Every cycle therefore has even length. The six nonrational phase types occur
with even multiplicity on such row orbits. The code enforces this by doubling
their columns.

## Low-block Verlinde integrality

Let `A_E` denote the simple summand of `I(1)` associated with a source character
`chi_E`, let `f_E` be its formal codegree, and let `v_Y` and `z_Y` be the
restriction row and positive dimension of a central simple `Y`. The normalized
central S-matrix has

`s[A_E,Y] = chi_E(v_Y)/f_E`, and `s[1,Y] = z_Y/D`.

The multiplicity of the tensor unit in `A_E A_F A_G` is therefore

`D/(f_E f_F f_G) * sum_Y chi_E(v_Y) chi_F(v_Y) chi_G(v_Y)/z_Y`.

This is a nonnegative integer. No complex conjugation is needed in this
symmetric triple-product formulation; it is the usual coefficient
`N[E,F,G*]`. There are 56 unordered triples of the six non-unit induced-unit
simples. The whole dual orbit makes each coefficient real. In these examples
it lies in `Q(sqrt(5))`, so its irrational coefficient vanishes and its rational
coefficient is a nonnegative integer. `verlinde.py` appends these equations with
56 nonnegative integer slack variables.

## Exhaustion of the saturated conductor-five coordinates

For `R7_5_3895`, all high rows with unequal coordinates 4 and 5 have the unique
primitive-fifth-root trace type prescribed by the saturated conductor-five
compression. The residual Gram matrix gives the exact identity

`sum_Y (v_Y[4]-v_Y[5])^2 = 8`.

After source spectral-integrality filtering, each of the two surviving low
frames has 58 possible active row orbits: 25 of weight 2, 27 of weight 8, and
6 of weight 4. The weight-4 orbits are transport-fixed, so parity doubles their
minimum contribution to 8. Thus there are exactly
`binomial(28,4)+27+6 = 20,508` nonnegative integral active allocations.

`enumerate_active.py` enumerates all of them. The remaining rows have equal
coordinates 4 and 5, so their residual Gram matrix must annihilate the
corresponding difference vector, have nonnegative entries, and be positive
semidefinite. These exact tests leave 126 allocations in low frame 6 and 166
in low frame 8. The enumeration does not invoke an optimizer.

The companion `computation/inactive_lattice.py` artifacts provide exact
congruence tests for the remaining inactive columns. Their validity is checked
by containment of every inactive column in the recorded lattice, without
trusting the algorithm that discovered the lattice. These tests leave 32
allocations per frame. Exact Farkas covectors in
`R7_5_3895_branch_farkas_{6,8}.json` eliminate 28 of these 32 allocations for
each of the four positive-indicator character labellings.

The four remaining allocations in low frame 6 are excluded by finite integer
split trees, for each of the four character labellings. The 16 trees have 775
leaves in total. Every split covers all possible integers, and every leaf is
an exact integer Farkas inequality, including its path's integer bounds.
The negative-indicator branches are excluded by one further exact covector.

`verify_frame6.py` is the complete replay entry point. It regenerates all 15
low frames, all 163,766 high rows, both surviving row-orbit inventories, all
eight positive-indicator integer systems, and all active allocations directly
from the canonical source. It then replays the negative-indicator covector,
lattice containment tests, rational separators, branch-specific Gram pruning,
and all 775 integer leaves. Both normal and optimized Python runs pass without
an optimizer. Its conclusion is exactly the exclusion of the distinct-row
low frame 6. Low frame 8 has exact feasible integer witnesses, so this is not a
ring-level exclusion of `R7_5_3895`.

## Feasible necessary-data witnesses

`export_witnesses.py` reconstructs all equations directly from the canonical
source tensor and the exact character table, and checks every reported integer
solution. It checks restriction Gram matrices, both indicator moment systems,
all induced-unit STS equations, Galois and dual row orbits, parity, integral
central fusion eigenvalues, and all 56 low-block Verlinde coefficients.
For `R7_5_5039`, it additionally checks the independently proved
conductor-eight phase budgets 2, 2, and 4.

The exports include the full restriction-row multiset, phase multiplicities,
character labelling, source hash, and a canonical witness hash. They explicitly
carry the status `feasible_necessary_data_only`. Their purpose is to make the
remaining obstruction or construction problem concrete and reproducible.

## Full source field and primary-order refinements

`full_field_verlinde.py` uses the 37 exact two-moment phase types over
`Q(sqrt(5),sqrt(2),i)` from `models/sqrt5/full_source_phases.py`.
Orders 16 and 80 have even fixed-row multiplicity. The genuine zero type
has multiplicity in `4N+5N`, reflecting source-fixed square Galois cycles.
The underlying builder `criteria/q5_full_field.py` also implements the
separately audited conductor-eight branches `c=0` and `c=2` for `R7_5_5039`.
These use sign-normalized row transport. The retracted unsigned-transport
claims that every active orbit has weight at least four, or that every
conductor-eight-active row has zero phase, are not used.

The further fifth-primary refinement comes from
`modules/PRIME_PROJECTION_FP_WEIGHTS.md`. Put

* `u(v)=(2,1,1,2,-2,-2,0).v` for `R7_5_3895`;
* `u(v)=(2,1,1,-2,-2,2,0).v` for `R7_5_5039`.

The total `u^2` weight is 160, and the seven known induced-unit objects
contribute eight at fifth-primary order one. The total weights at exact
fifth-primary orders one and five are `c` and `4c`, with integer
`8<=c<=32`. A genuine-zero multiplicity unit four is split into classes
with fifth-primary part one or five; a unit five belongs to the hidden
class with fifth-primary order at least 25. Mixed large primary orders
are conservatively included in the last class. If `H0,H1` are the first
two high-row weights after splitting, the added equations are

`H1-4H0=32`, `H0+slack=24`, with nonnegative integer variables.

This is a necessary relaxation of the primary-order inventory. It does
not assert realization of an arbitrary split.

For any word `E1,...,Ek` in induced-unit simples, the unit multiplicity is

`D^(k-2)/(f_E1 ... f_Ek) * sum_Y product_j chi_Ej(v_Y)/z_Y^(k-2)`.

It must be a nonnegative integer. The optional `--word-file` interface
accepts source- and domain-bound exact coefficient vectors from
`computation/word_coefficients.py`. In particular, the fourth and fifth
powers of the first formal-codegree-16 character eliminate several older
`R7_5_3895` witnesses, but they do not eliminate its remaining frame.

Historical stronger examples are
`R7_5_3895_full_field_verlinde_branch0_fp5_words.json` and
`R7_5_5039_full_field_verlinde_chi8_{0,2}_fp5.json`. Their proposed center
ranks are 44, 39, and 55 respectively. The first has fourth/fifth unit
multiplicities 44 and 2839. `verify_full_field_witnesses.py` reconstructs
the exact phase inventory, the spectrally integral orbit inventory, all
Gram/moment/STS and primary-order equations, and all 56 low Verlinde
coefficients. It recomputes the optional word coefficients directly from
the character table. It invokes no optimizer and labels every success
`PASS_necessary_data_only`.

Subsequent coupled phase transport strengthens the fixed/dual-row order-80
unit to four and the hidden fifth-primary zero unit to ten, while retaining
the genuine-zero unit four. This rejects the historical conductor-eight-zero
witness's phase assignment. A new assignment with order-16 phases is in
`R7_5_5039_full_field_verlinde_chi8_0_fp5_norm_allwords.json`.
That replacement is historical necessary data: the cyclic fourth-indicator
test below subsequently rejects it.

## Finite all-word integrality and integer norm cuts

`modules/ALL_WORD_UNIT_FUNCTIONAL.md` proves that all low-word unit
multiplicities can be checked by a finite family of linear congruences.
The exact generated spectral order stabilizes modulo the trace denominator.
The present domains give 75 congruences for `R7_5_3895` and 31 for
`R7_5_5039`. The optional `--all-words` interface checks source/domain
hashes and imposes every congruence. Its coefficients and constant are
reduced to nonnegative residues; thus the modular quotient can safely be
represented by a nonnegative integer slack. This differs from imposing
nonnegativity on arbitrary signed order-basis traces, which is invalid.

`integer_norm_cuts.py` gives another family of exact linear constraints.
For a positive low product `P=A_E A_F`, let `n_Y` be its nonnegative
integer coefficient at each center simple. Then
`q=tau(PP*)=sum_Y n_Y^2`. For any rational source vector `x`, put

`g*(t)=max_{k>=0 integer}(t*k-k^2)`.

The monoidal forgetful functor gives `sum n_Y v_Y=F(P)`. For arbitrary
fixed integers `a_l` at the seven known low simples, integer squares give

`q >= x.F(P) + sum_low (2a_l+1-x.v_l)n_l`
`     - sum_low a_l(a_l+1) - sum_high g*(x.v_Y)`.

Every term is linear in the unknown row multiplicities: `q` is a quartic
word coefficient and the known low `n_l` are triple coefficients.
The cut generator reconstructs these coefficients from the canonical
character table and records its rational multiplier and chord centers.
No assumed packet equality is used. The independently derived cut
`models/sqrt5/R5039_c2_fp5_integral_norm_cut.json` rejects the historical
rank-55 witness by an exact gap four. A new rank-53 necessary-data witness
survives the cut; this is not a ring-level exclusion.

## Cyclic fourth and eighth rotation constraints

The grouping identity for pivotal rotation identifies the square of the
rotation on `Hom(1,X^4)` with the order-two rotation for `X^2`.
Consequently, if `m=dim Hom(1,X^4)` and
`t=nu_2(X^2)=sum_i N_XX^i nu_2(X_i)`, its four character multiplicities are

`(m+t+2 Re nu_4(X))/4`, `(m+t-2 Re nu_4(X))/4`,
`(m-t+2 Im nu_4(X))/4`, `(m-t-2 Im nu_4(X))/4`.

Every value must be a nonnegative integer. This uses the full cyclic
character, and does not assume that the indicator of a self-dual object
is real. `fourth_cyclic_constraints` implements the equivalent four
nonnegative integer variables and the complete eight field coordinates.
`fourth_indicator_audit.py` independently rejects the earlier visible-phase
ghosts: the R3895 first nonunit object gives multiplicities
`(13/2,5/2,1,1)`, and the R5039 conductor-eight-zero ghost gives
`(2,2,-1/2,1/2)`.

The complete all-order moment domain is finite after taking relative field
traces: 49 records retain the first, second and fourth moments; 61 retain
the eighth moment as well. Genuine zero records retain their separate
source-fixed packet divisibilities. In particular, a vanishing first pair
of moments is not treated as a vanishing fourth or eighth moment.
The proofs and independent controls are in `modules/` and
`models/sqrt5/full_source_phases.py`.

For C8, the square and fourth power of rotation have traces
`nu_4(X^2)` and `nu_2(X^4)`. The former is computed from the existing C4
variables by additivity. `modules/cyclic_eight_constraints.py` appends
eight nonnegative integer eigenvalue multiplicities per source object.
`criteria/q5_cyclic_eight_search.py` exports all six inequivalent surviving
label/primary-branch systems. A numerical infeasibility report by that
search remains only a discovery result until an exact certificate is
replayed against the source-bound system.

An auxiliary finite branching for R5039 is implemented by
`enumerate_chi8_active.py`. The total squared difference of the first two
nonunit restriction coordinates is 16. With the valid packet
divisibilities, residual Gram positivity leaves seven aggregate row
allocations in primary branch zero and eighteen in primary branch two.
The enumeration uses actual positive signed transport and does not use
the retracted claim that every active orbit has size at least four.
`chi8_branch_system.py` fixes these aggregate counts while retaining all
phase choices. Its partial covector replay checks only recorded leaves;
it does not claim a full exclusion when any allocation remains open.

## Exact final conductor-eight branches for R7_5_5039

The C8 continuation closes both sign-safe primary branches for the
remaining equal-row low frame. In primary branch two, the independent
computation supplies the same sparse congruence functional for both
inequivalent character labellings: every column has value zero modulo
256, while the target has value 128. The source-bound domain replay is
`modules/verify_r5039_c2_domain.py`.

For primary branch zero, the exact seven aggregate allocations expand
to 615 complete active phase assignments in each labelling. A containing
integer lattice for the inactive columns eliminates 611 assignments.
The four survivors each consist of a single order-64 packet of eight
objects at each row of orbit 24. `chi8_phase_lattice.py` checks every
inactive generator against the recorded lattice and regenerates the
complete finite packet enumeration. It does not trust the normal-form
algorithm used to discover that lattice.

After source Gram pruning, the source-object-one C4 character is forced
to have multiplicities `(3,1,0,0)`. The independent exact fourth-character
splits and Farkas covectors are in `criteria/`. The phi-difference budget
has 1004 raw allocations, of which exactly 50 fit the residual Gram.
Exact Farkas tests retain phi indices `2,14,46,49` for labelling zero,
and `46,49` for labelling one.

The irrational part of the eighth indicator gives an additional finite
reduction. Among the remaining rows only orbits 45 and 50 can contribute
to the two sqrt(10) coordinates. Their exact PSD capacities are 17 and
34 actual row copies. The order-320 packet at orbit 45 has size 16 and
cannot cancel its independent restriction vector, so its count is zero.
Cancellation at orbit 50 forces exactly one size-16 order-320 packet,
with two possible phases for each of the four active order-64 phases.
Other phases on orbit 50 remain available. This reduction is proved and
independently replayed in
`models/sqrt5/verify_c0_forced_eighth_packet.py`.

The remaining 48 branches are all excluded by finite integer-split
trees, with exactly two rational Farkas leaves per branch. Each tree
splits the same original variable: the multiplicity of eigenvalue
`-i` in the C4 rotation character of source object five, at the integer
threshold 18. The proofs retain all possibilities on both sides of that
threshold. No numerical infeasibility result is used as a certificate.

`verify_c0_conditional_trees.py` independently reconstructs the canonical
source induction Gram, every packet deletion, and all integral orbit
capacities. Its capacity computation exhausts the possible integer
counts, independently of the discovery binary search. It checks each
leaf inequality directly against the original columns and path bounds,
without calling the discovery augmented-matrix routine. Optimizer
imports are blocked. Both ordinary Python and `python -O` replay all
48 branches and all 96 leaves; receipts are
`c0_conditional_trees_normal.json` and
`c0_conditional_trees_optimized.json`. The low-frame, label and phase
completeness proofs must accompany these final conditional certificates.
