# Revision notes — unified criteria and finite frontier

The current ledger records **16,552 general exclusions, 54 realized rings
and 6 unresolved rings** among 16,612 census tensors. Multiplicity at most
three and the exact bands 1, 2, 3, 6 and 7 are completely classified. This
revision makes substantial exact reductions within the six unresolved
cases; it adds no general exclusion or categorical realization to the ledger.

## One system for restrictions, products and twists

The manuscript combines restriction Gram equations, spectral moments and
low-word coefficients in a single joint Gram factorization. Every candidate
column lies in an exact rational image and satisfies a rank-one quadratic
bound. These conditions give finite coefficient domains, including singular
Gram matrices. The twist variables and word coefficients are then assigned
to the same proposed central simples, so ribbon balancing couples the
previously separate systems. Duality is explicit for complex characters.

The generic implementation is
[`software/round5_unified.py`](software/round5_unified.py), with
[exhaustive small-domain controls](research/round5/unification/domain_controls.json).
An [independent domain crosscheck](research/round5/unification/native_1204_domain_crosscheck.json)
compares the generic rational construction with the native implementation
used for `R6_5_1204`. Budget exits are incomplete outcomes, never proofs.
The [pointed-center controls](research/round5/unification/pointed_center_control.json)
check complex duality and the ribbon convention; the
[`Rep(S3)` center control](research/round5/unification/s3_center_control.json)
checks nonzero high-word coefficients and genuinely coupled balancing equations.
All are exact categorical controls, rather than an asserted scan of every model.

The dimension-block criterion is checked through its complete finite Fourier
form on all six inputs. Saturation forces actual twist-order restrictions and
exact moment identities from a finite modular representation. The
[shared support implementation](software/dimension_block_support.py),
[representation identities](research/round5/unification/equality_modrep.py)
and [Fibonacci control](research/round5/unification/conductor_support_control.json)
make this equality case reproducible, including exact forbidden-root tests.
The [large-prime indicator congruence](software/prime_indicator_congruence.py)
adds exact indicator constraints for all four cases with a proved full twist
exponent; its categorical controls and deliberate false-exponent control pass.

The subcategory criterion retains the whole nonnegative integral projection
matrix and both modular intertwining identities. It bounds each individual
central-simple contribution. When its columns are proved disjoint, the
subcategory representation can be subtracted before testing the finite
representation spectrum. The
[finite-group controls](research/round5/unification/subcategory_intertwiner_control.json)
check both full-rank and rank-deficient projections, so this subtraction is
used only under its stated hypothesis.
The [saturated Bruhat helper](software/saturated_bruhat.py) also projects
finite-representation vector identities onto every known low row. Its exact
categorical control passes; the bounded scan of all 171 R1204 profiles found
no additional exact obstruction.

## Exact progress on the six remaining rings

| Ring | Certified progress | Primary evidence |
|---|---|---|
| `R6_4_22` | Rank-30 profiles are excluded for both character labellings. The remaining rank-36 center has one necessary fusion/modular datum up to relabelling and complex conjugation. | [Current coverage](research/round5/coverage.json), [balancing certificate](research/round5/fermion/R6_4_22_certificate.json) |
| `R6_4_91` | Exhaustive fusion completion excludes center rank 36. At rank 42 the forced Ising factor has a rank-14 centralizer with eight labelled associative fusion tensors in one based-ring orbit and two compatible conjugate modular data. | [Reconstruction certificate](research/round5/quartic_pair/R6_4_91_center_reconstruction.json), [source-bound replay](research/round5/quartic_pair/replay_O.json) |
| `R6_4_155` | The complete profile, joint Gram and common twist reductions leave six induction profiles, each with one forced pair of low fusion matrices in its semion centralizer. | [Complete frontier certificate](research/round5/m4_155/frontier_certificate.json), [packet reconstruction](research/round5/m4_155/packet_frontier.json) |
| `R6_4_629` | Exact integer enumeration excludes rank 30; modular closure forces a nonintegral Verlinde coefficient at rank 38. Exhaustive rank-35 completion leaves one fusion/modular datum up to conjugation and identical-column relabelling. | [Complete certificate](research/round5/m4_629/modular_reduction_certificate.json), [source-bound replay](research/round5/m4_629/modular_chain_replay_O.json) |
| `R6_5_1204` | All 39 low frames and all character labellings are covered. Exact bounds yield 39,800 profiles, low-word tests leave 1,833, and joint Gram, twist and congruence certificates leave 171. A signed-gauge reduction covers general categorifications. | [Complete certificate](research/round5/m5_1204/profile_certificate.json), [optimized replay](research/round5/m5_1204/exact_replay_optimized.json), [retained profiles](research/round5/m5_1204/remaining_profiles.json) |
| `R6_8_1660` | Actual-root induction and congruence cuts leave three branches with 168, 798 and 798 necessary profiles; the center twist exponent divides 48. | [Complete actual-root certificate](research/round5/m8_actual48/certificate.json), [source-bound replay](research/round5/m8_actual48/replay_O.json) |

These are necessary alternatives. An exact integral witness is not a
categorification; an associative fusion tensor with compatible modular data
still requires a categorical construction. A profile exclusion only removes
that profile. General nonexistence would require exhaustion of every allowed
branch and any needed reduction from general to pseudo-unitary categories.

## Manuscript and evidence organization

The manuscript presents shared criteria once and places the case-specific
finite reductions together. Current documentation follows mathematical
scope rather than campaign chronology. Redundant exploratory material is
separated from the canonical proof dependencies; accepted historical proof
sources and their original receipts remain intact.

Exact replay reconstructs the finite domains and equations from the census
tensors and verifies stored integral witnesses, congruences or separating
rays. Optimized Python runs disable assertions and numerical optimization.
Discovery solver outcomes, feasible relaxations, partial enumerations and
model comparisons do not create ledger decisions.

The [coverage manifest](research/round5/coverage.json) freezes the current scope
and distinguishes intrinsic verifier hashes from later file inventories.
`software/round5_replay.py` lists or reconstructs selected exact frontiers; its
`--check-receipts` mode only audits existing evidence and never claims a fresh
mathematical replay. Fresh replay logs and refreshed receipts are captured in
the requested output directory while retained receipts are preserved.

The [verification guide](verification/README.md) identifies the current
receipts and the retained catalogue evidence. Ledger consistency, document
compilation and archive integrity are separate checks. The original negative
catalogue is inherited with its exact evidence; this revision does not claim
to have rerun it in full. Earlier revision notes remain in `provenance/`.
