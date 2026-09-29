# Fourth continuation: exact quartic frontier profiles

No whole-ring exclusion or categorification is claimed in this directory.
Both smallest frontier tensors remain unresolved. Their finite necessary
center-induction domains are now exhaustively controlled.

| Tensor | Gram + Galois profiles in the surviving low frame | After degree-three multiplicities and restriction products | After words through six | After exact twist refinements | Possible center ranks |
|---|---:|---:|---:|---:|---|
| R6_4_22 | 93 | 3 | 2 | 2 | 30, 36 |
| R6_4_91 | 524 | 6 | 6 | 2 | 36, 42 |

The counts apply to each of the two low-character labellings. All other low
frames and indicator choices are covered by the canonical records. For
R6_4_91 this includes replay of 14 inherited exact modular-trace rays; the
four new profile rejections per labelling have exact congruence certificates
modulo 2. For R6_4_22 one profile has fourth-word multiplicity 9/2 and is
removed. Its rank-30 profile is retained without a feasibility claim:
a numerical integer-infeasibility report and a bounded 80-node branch
search do not constitute an exact rejection.

The rank-36 R6_4_22 profile and both R6_4_91 profiles have exact nonnegative
solutions to the specified necessary equations, with the required integral
multiplicities. They are not full center fusion rings or modular data.

The profiles force one central lift of the nontrivial invertible object in
both inputs, and one central lift of the Ising object in R6_4_91. The latter
lifts generate an Ising fusion subcategory of its center. This does not
assert a Deligne decomposition of the original fusion category.

## Canonical exact records

- `R6_4_22_frontier_certificate.json`
- `R6_4_91_frontier_certificate.json`
- Normal replay: corresponding `*_frontier_replay.json`.
- Optimized replay: corresponding `*_frontier_replay_optimized.json`.

Each certificate embeds the unrestricted signed-quotient reduction proving
sphericality and a pseudo-unitary Galois conjugate. The verifier reconstructs
the entire low-frame domain, enumerates all bounded affine integer solutions,
and checks every word multiplicity, inherited ray, new congruence, and
retained primal witness. It calls no numerical optimizer.

From the release root:

```bash
python -O research/round4/quartic_front/replay_frontier.py R6_4_22
python -O research/round4/quartic_front/replay_frontier.py R6_4_91
python -O research/round4/quartic_front/algorithm_controls.py
```

`algorithm_controls.json` compares the exact affine enumerator with independent
full-box enumeration on 48 finite systems, including fractional pivot
coordinates and inconsistent systems. `applicability.json` records all ten
frozen frontier inputs and all 54 positive controls. Six are eligible for
this implementation and 58 are ineligible; eligibility does not claim that
an execution succeeded. The eligible known positive input R6_4_322 was run
through all word tests to degree six and retains 24 profiles per labelling
on its surviving low frame (`R6_4_322_control.json`). The independent R6_4_629
profile campaign is in the sibling directory. The eligible higher inputs
R6_8_311 and R6_8_1660 were screened here for applicability only.

## Additional exploratory evidence

The `*_galois_norm_probe.json` files check the stronger joint Galois
signature consisting of the low eigenvalues and the normalized dimension
square. The retained profiles survive. The product-Gram and full low-action
probes impose additional simultaneous center constraints. On the rank-42
R6_4_91 profile, there are exact integral low-action relaxations satisfying
the known Ising A3 action and its parity grading. The resulting low matrices
do not mutually commute, so these are explicitly not fusion data. All such
files remain exploratory and do not determine classification allocations.

Every discovery process had an explicit external limit below 15 minutes.
The failed 80-node branch search and continuous-elimination congruence probe
for the rank-30 R6_4_22 profile leave that profile undecided. They are not used
as exact exclusions by the canonical verifier.
