# Rank-nine commutative continuation, 24 October 2026

## Classification outcome

No complete source-ring exclusion or categorical model was obtained. R9_2_137, R9_2_1607, and R9_2_1976 remain unresolved. Their necessary categorical structure has nevertheless been narrowed by two new arguments, and a previously missed lower-rank dependency has been corrected.

## New established restrictions

1. **No central free involution.** A hypothetical half-braiding on the unique isotropic free involution would de-equivariantize to R6_4_174 or R6_4_6. Both have existing general-scope exclusions. The quotient-to-target permutation is (0,5,1,2,3,4) in each case. All 216 coefficients per transport and all 486 coefficients of each of six quotient maps are checked exactly. This corrects the old note that treated the V4 quotient only as an open external-literature family.
2. **Integral center is Vec or sVec.** The pointed center can contain at most one anisotropic involution, necessarily a fermion. Norm divisibility and Burnside's theorem prohibit any Tannakian subcategory of the whole center. Applying the categorical Burnside theorem and Natale's integral weakly-anisotropic theorem to the integral central subcategory proves that every integral-dimensional central simple is invertible. The argument is general complex in scope and is independently audited by the root and quartic-pair agents.
3. **A finite TY spectrum.** The dimension-two TY object has indicators (0,epsilon,0,0,0,epsilon,0,2) through order eight. Positive saturation forces its induced central constituents to have eighth-root twists, with explicitly determined weight in every twist fiber. Each primitive-eighth-root fiber has exactly two multiplicity-one constituents, of dimension pair (2+d,2+7d) or (2+4d,2+4d), where d=4+3sqrt(2).
4. **The positive TY sign is impossible for R9_2_1607 and R9_2_1976.** Exact separating vectors for the strengthened height-four necessary systems have b^T y equal to -1,253,376 and -17,466,624 respectively, with minimum entry of A^T y zero. Thus these two rings, if categorifiable, must have tau=-1/2. Rationality of tau and chi makes the sign invariant under the Galois-pseudo-unitarity reduction. Independent semantic reconstruction is recorded separately by the quartic-pair auditor; the arithmetic replays and portable exports have passed.

The main proofs are `NO_CENTRAL_BOSON.md` and `TY_SPECTRUM.md`. None of these conclusions forces a central fermion to exist. A based-central invertible need not have a half-braiding. A fermionic half-braiding in a nonbraided source category also does not supply the transparent-fermion fixed-point obstruction.

## Completed computational attempts

| Source | Integral-center height 3 | TY spectrum height 4, tau=+1/2 | TY spectrum height 4, tau=-1/2 |
|---|---|---|---|
| R9_2_137 | No separator | No separator | 180-second optimizer limit |
| R9_2_1607 | No separator | Exact conditional exclusion | No separator |
| R9_2_1976 | No separator | Exact conditional exclusion | No separator |

“No separator” means that the numerical separator problem reported infeasibility; it is not an exact feasible categorical witness, and is never interpreted as a model or an exclusion. The timeout has no mathematical implication. No further heuristic solve remains running in this branch.

The full order-16 pointed-bimodule stabilizer calculation was pursued independently by the noncommutative agent. It admits an exact fourth-root cochain, so it supplies no exclusion. No duplicate or weakened cyclic calculation is counted as progress here. The same agent also obtained the positive-TY-sign exclusion for R9_2_1975; that case is outside this report's ownership.

## Reproduction and exact records

- `verify_no_central_boson.py`: source hashes, adjoint generation, six quotient maps, two tensor transports; optional `--replay-dependencies` invokes the two complete existing lower-rank verifiers with optimizer entry points disabled. The full lower-rank certificates are retained in `lower_rank_dependencies.json`.
- `verify_ty_spectrum.py`: exact Shimizu indicator sums, Fourier weights, induction Gram columns, and algebraic-integer tests. Its receipt is `ty_spectrum_receipt.json`.
- `screen_integral_center.py`: reconstruction of the strengthened labelled-S necessary systems; `--verify` replays a saved positive-sign ray without invoking the optimizer.
- `R9_2_1607_tau1_exact_system.json.gz` and `R9_2_1976_tau1_exact_system.json.gz`: portable integer matrices, right-hand sides, rays, and hashes. `check_exported_ray.py` checks them using only the Python standard library. Source bindings identify the reconstruction code versions.
- The `_replay.json` and `_replay.log` files preserve fresh optimized-Python exact system checks. The discovery logs preserve every solver outcome, including the single explicit timeout.

The lower-rank dependency replay is intentionally distinguished from the fast transport check in `no_central_boson_receipt.json`. Its `dependency_replay` field is false. The duplicate full R6_4_174 replay was stopped after more than 23 CPU minutes while reconstructing its 128 old height-six systems; it did not complete, and the subsequent full R6_4_6 replay did not start. The existing published categorical proofs are inherited, with the source files hash-bound in `published_dependency_source_binding.json`. No fresh full replay of those old proofs is claimed. The log and `dependency_replay_status.json` record this explicitly. All new exact checks, including the quotient transports and conditional exclusion certificates, completed. No process was left running.

## Remaining mathematical gap

For R9_2_1607 and R9_2_1976 the negative TY sign remains. For R9_2_137 neither sign has been excluded. The two previously surviving uniform D8 Morita based rings remain necessary candidates; no associator, tensor-equivalent construction, or contradiction for their remaining branches has been produced. Matrix feasibility, based-ring isomorphism, and pointed-module cochains do not by themselves categorify those rings.

No repository or website was changed.
