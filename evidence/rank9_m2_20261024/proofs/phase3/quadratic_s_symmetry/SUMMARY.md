# Completed quadratic continuation

Seven old unresolved rings are now excluded in general complex scope:
114,128,516,1487,1635,1636,1959. The canonical accepted records are in
`exclusions.json`, with independent proof audits, exact replays and signed
Galois-pseudo-unitarity dependencies.

Six are unified by the Galois-unit restriction theorem: modular S symmetry
forces a half-integral restriction vector for one central simple. The short
proof is `GALOIS_UNIT_THEOREM.md`. The seventh,516, forces central Rep(S3),
whose condensation and grading produce an impossible rank-three neutral
subcategory; see `R516_STRUCTURAL.md`. Neither primary argument needs an LP.
The independent audits are in `../audit_quadratic_symmetry/`.

All eleven available commutative models in the theorem's quadratic-field
scope pass the new restriction test. These include the restored half-E6
models; their records are in `galois_unit_positive_controls.json`. An exact
necessary-condition pass is used only as a control, never as a new model.

The full labelled-S sweep was completed at height3, and with central duality
at height6, on all ten old commutative quadratic cases. It supplied initial
certificates which were subsequently replaced by the short proofs above.

## Precise remaining scope

137,1607,1976 remain unresolved. Their determined Galois-unit restriction
vectors are nonnegative integral, and the standalone self-dual-character
restriction domains are nonempty. The bounded LP outcomes were:

| Ring | Height3 labelled S | Height6 labelled S plus duality | 25-second forced-central-invertible screen |
|---|---|---|---|
| 137 | No separator returned | Time limit, no certified ray | Time limit, no certified ray |
| 1607 | No separator returned | Time limit, no certified ray | Time limit, no certified ray |
| 1976 | Time limit, no certified ray | Time limit, no certified ray | No separator returned |

The LPs search for separating functionals. In their logs an infeasible
**separator** LP is not an infeasible categorical feasibility system. These
outcomes are all recorded as no conclusion. No feasible numerical relaxation
is treated as a categorical realization, and no timeout is treated as an
exclusion.

The final central-invertible screen omitted all candidate central invertibles
forgetting to nontrivial source invertibles. It sought a contradiction to that
hypothesis at height3, with 25 seconds allotted to the separator optimizer per
ring. It certified no forcing statement and changes no classification. This
was the final bounded attempt; no open search remains running in this branch.

Noncommutative1848 and1975 were outside the commutative sweep and handled by
the other research branches. Independent extension of the self-dual-character
criterion to the fifteen weak/integral residuals also yielded no exclusions;
that separate audit is `../audit_signed_so3/REAL_CHARACTER_AUDIT.md`.

The earlier adversarial audit of nineteen center and two Morita exclusions
is complete and passed, in `../audit_center_morita/AUDIT.md` and `audit.json`.
