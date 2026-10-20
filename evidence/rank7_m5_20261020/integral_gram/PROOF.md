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

The current stronger examples are
`R7_5_3895_full_field_verlinde_branch0_fp5_words.json` and
`R7_5_5039_full_field_verlinde_chi8_{0,2}_fp5.json`. Their proposed center
ranks are 44, 39, and 55 respectively. The first has fourth/fifth unit
multiplicities 44 and 2839. `verify_full_field_witnesses.py` reconstructs
the exact phase inventory, the spectrally integral orbit inventory, all
Gram/moment/STS and primary-order equations, and all 56 low Verlinde
coefficients. It recomputes the optional word coefficients directly from
the character table. It invokes no optimizer and labels every success
`PASS_necessary_data_only`.
