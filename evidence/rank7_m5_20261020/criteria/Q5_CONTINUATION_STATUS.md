# Exact necessary data for the two remaining quadratic rings

This directory does **not** contain a general categorification exclusion or a
categorical construction for `R7_5_3895` or `R7_5_5039`. It now contains exact
**braided-only exclusions for both**, described in
`BRAIDED_FRONTIER_EXCLUSION.md` and replayed by `verify_braided_frontier.py`.
The general categorification question remains open. An exact feasible integer list of
restriction rows and relative twist traces is only necessary data. The accepted
general-to-Galois-pseudo-unitary reduction is in `../sqrt5_reduction/`; it does
not itself exclude either ring.

Both have dimension `D=80(9+4 sqrt(5))`. The source dimensions, character tables,
and full normalized Galois transport are recomputed exactly. The latter is bound
to the independently checked construction in `../models/sqrt5/verify_transport.py`.
The source character fields are contained in `Q(sqrt(5),sqrt(-2))`; the nonreal
quadratic factor occurs only for R5039. The center restriction rows are grouped
under the full quadratic Galois transport and categorical duality. A row orbit
has a common relative twist trace because Galois permutation changes the twist
by a square automorphism, and duality preserves the twist.

## Established constraints

The following are necessary under the pseudo-unitary reduction:

* The complete induction Gram identity and the complete character labelling of
  the seven multiplicity-one summands of the induced unit.
* Algebraic integrality of every known central fusion eigenvalue
  `(D/f_E) chi_E(v)/dim(v)`, together with closure of its joint Galois type.
  `spectral_induction.Spectrum` supplies this existing exact criterion.
* The two indicator trace identities and all low-block modular `STS`
  identities. The latter are an extension of the existing implementation in
  `supplements/rank7/software/modular_character_induction.py`, not a newly
  claimed theorem. With normalized center `S`,
  `S(E,Y)=chi_E(v_Y)/f_E`, and therefore
  `sum_Y theta_Y chi_E(v_Y) chi_F(v_Y)=f_F chi_E(v_F)`.
* The categorical Cauchy theorem restricts twist orders to powers of 2 and 5,
  since `D=80` times an algebraic unit. The ten real-quadratic phase pairs in
  `q5_center_trace.phase_vertices()` are consequently exact values, not merely
  vertices of an outer convex hull. Their multiplicities are integers.
* Conductor-five compression is saturated on the difference of the two
  formal-codegree-five summands. Every high row with unequal designated
  coordinates has precisely the primitive fifth-root relative phase determined
  by its low labelling. The complete independent argument and finite check are
  in `../modules/Q5_SATURATION_INDEPENDENT_AUDIT.md` and
  `../modules/verify_q5_saturation.py`.
* For R5039 the independently checked conductor-eight partial projection
  bounds give squared-difference budgets 2, 2, 4 for the nonzero phase buckets
  with exact two-primary orders 1, 2, 4. The corresponding low-frame bound
  excludes low frame 1. The proof is in
  `../modules/CHI_MINUS8_PARTIAL_PROJECTION_AUDIT.md`.

An additional proposed deletion of all nonzero real-quadratic phases on rows
with `v_1 != v_2` was **retracted**. Actual positive row transport may be `-T(v)`;
for example `v=(0,1,0,1,1,1,1)` has `T(v)=-dual(v)`. Its two-row orbit invalidates
the claimed universal four-row budget argument. The current engine does not
apply that deletion, the proposed pointwise product-zero cut, or its dependent
hidden-order argument. The uniform 2, 2, 4 bounds remain in force.

A later, separately audited **sign-safe** replacement extends the actual
two-primary spectral masses to `(c,c,2c,4c)`, with `c=0` or `2`. It uses actual
source-fixing Galois cycles and categorical duality, not the rejected minimum
four-row claim. `q5_full_field.build_system(..., chi8_branch=...)` implements:

* `c=2`: character-active twists have order dividing 40 and exact squared
  difference masses `(2,2,4,8)` at two-primary orders `(1,2,4,8)`.
* `c=0`: character-active visible F8 phases have orders 16 or 80; genuine-zero
  active multiplicity is divisible by four. The four lower masses are zero.

The proof excludes active five-primary orders at least 25 in both cases. The
four mass conditions are equality rows, with no inequality slack columns.
Fresh code controls independently check their exact coefficients, targets,
phase-order provenance, and active-zero divisibility. Both real linear
relaxations remain open for all twelve labellings of the surviving R5039 frame;
neither is an exclusion certificate.

The conductor-five FP-difference projection additionally gives total weight
160 and exact actual five-primary masses `(c,4c)` at orders 1 and 5, with
integer `8<=c<=32`; the known induced-unit summands use weight 8 at order 1.
The weights are the squares of
`(2,1,1,2,-2,-2,0) dot v` for R3895 and
`(2,1,1,-2,-2,2,0) dot v` for R5039. The generic builder therefore includes
the conservative visible high-row bounds 24 and 128, with two additional
inequality slacks. It does not equate visible phase masses to actual masses:
the genuine-zero F8 phase can hide either five-primary part. The proof and
independent local replay are in `../modules/PRIME_PROJECTION_FP_WEIGHTS.md`.
The stronger shared-c allocation of hidden phases is in the separate integer
wrapper. The four control cases pass normal and optimized Python after this
addition.

The ring of integers of `Q(sqrt(5))` is used throughout. If a high dimension is
`z=a+b sqrt(5)`, its necessary `D/z` integrality permits half-integral equal-parity
coordinates: `a^2-5b^2` divides `160a` and `160b`, and the resulting quotients have
the same parity. Replacing these by divisibility of `80a` and `80b` would be an
unjustified strengthening.

## Full multiquadratic relative traces

`q5_full_field.py` implements both `L4=Q(sqrt(5),sqrt(-2))` and the stronger
`F8=Q(sqrt(5),sqrt(2),i)`. The exact phase source is the independent
`../models/sqrt5/full_source_phases.py`. All nonzero first-and-second relative
trace pairs arise from eightieth roots; the higher prime-power orders yield the
genuine zero pair. Every square automorphism fixes either trace field, so the
same phase can be attached to an entire restriction-row orbit.

The F8 basis is
`(1,sqrt(5),sqrt(2),sqrt(10),i,i sqrt(5),i sqrt(2),i sqrt(10))`.
Since full duality orbits make each character-product coefficient real
quadratic, multiplication by an eight-component phase is performed in four
independent copies of the exact quadratic arithmetic. No imaginary component
is discarded. `q5_full_field_controls.py` independently projects every retained
column and the right side back to the established 101-equation real-field
system, including row-multiplicity factors.

The full-phase builder enforces the necessary fixed-row cycle counts supplied
by the phase proof: orders 16 or 80 have even multiplicity, and genuine zero
phase multiplicity belongs to `4 N + 5 N`. The latter is represented by separate
four- and five-unit columns. Conditional fifth-root parity is incorporated by
the least common multiple of the necessary divisibilities; this does not assume
independence of the two possible even-cycle actions.

Every phase-orbit variable is a nonnegative integer. If its smallest allowed
contribution exceeds a nonnegative Gram or conductor-eight budget, it is forced
to be zero and removed before linear relaxation. This preprocessing is exact.
The remaining real linear systems are relaxed necessary conditions. Discovery
uses a numerical optimizer only to propose separating covectors, which are
checked exactly before they are recorded.

## Separate integer and fusion checks

The files under `../integral_gram/` add exact integral phase counts and all 56
nonunit low Verlinde triples. Their generic coefficient is

`dim Hom(1,A_E A_F A_G) = D/(f_E f_F f_G) sum_Y chi_E(v_Y) chi_F(v_Y) chi_G(v_Y)/dim(v_Y)`.

It must be a nonnegative integer. `q5_ghost_checks.py` provides independent
additional checks on feasible necessary data: every low tensor product has
coordinatewise nonnegative forgetful remainder after subtracting its known low
summands, with zero unit coordinate; the first four traces of each known central
fusion matrix are nonnegative integers. Passing these checks is not a model.

Files whose status is `no_exclusion`, solver infeasibility without an exact
certificate, or `feasible_necessary_data_only` must not change the accepted
classification ledger. The accepted thirteen Oct20 exclusions use their
separate exact certificates and independent replays.
