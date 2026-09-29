# Fourth continuation: R6_4_629

The ring remains unresolved. This directory supplies a complete, substantially smaller domain of necessary induction data, with scope recorded at every stage.

## General reduction

`general_reduction.json` and `general_reduction_replay_O.json` prove that every categorification is spherical and has a pseudo-unitary Galois conjugate. The unrestricted signed search has 32 tables in one sign-gauge orbit. The optimized replay disables numerical optimizers.

## Exhaustive induction profiles

`R6_4_629_exact_profiles.json` is the unified `round4_quartic_profiles` certificate. All seven low frames are reconstructed. Six fail the spectrum test; the remaining frame has two low-character labellings. Its 85 admissible high columns have exactly 784 integral Gram/Galois multiplicity profiles. The native affine enumerator (`profiles.cpp`) visits 22,641,594 nodes; an independent Python reconstruction under `-O`, with numerical optimizers disabled, yields exactly the same 784 profiles.

For each labelling, exact low-word multiplicities through degree six and nonnegative restricted low-product remainders reduce the domain to five profiles, with ranks 24, 30, 32, 35, and 38. `filtered_profiles.json` is the exploratory version of this reduction; the unified certificate is authoritative. Its profile indices use sorted profiles, while the exploratory files use native traversal order; identify profiles by their full 85-entry count vectors when crossing these files.

## Odd relative twist orbits

`software/round4_629_orbits.py` proves and implements the additional count restriction from odd relative cyclotomic Galois orbits. The modular action is via squares on twists; the square map is surjective only because the relevant relative Galois groups have odd order. The code does not impose this rule on even prime support. The manuscript proof is `papers/chapters/round4_629_orbits.tex`.

`scan_orbit_scope.json` covers the frozen ten-ring frontier and all 54 realized controls: 61 are outside the supported scope, and the three eligible inputs are R6_4_629, Fib times Vec(C3), and the Izumi C5+5 near-group category. Both positive controls have exact necessary-system witnesses and optimizer-free replays. The independent root-orbit arithmetic audit checks 1,482 identities by summing the square action explicitly; normal and optimized receipts are included.

## Fixed profiles and twist refinement

`fixed_twist_h6.json` treats the first low-character labelling; `fixed_twist_h6_lab1.json` treats the second. All five profiles for the second labelling have exact Farkas obstructions. For the first labelling, ranks 24 and 32 also have exact Farkas obstructions, while ranks 35 and 38 have exact integral necessary-system witnesses. The rank-30 branch has a numerical integer infeasibility result, which by itself is not an exclusion. Its subsequent exact bounded affine enumeration reached the external 840-second limit; `rank30_exact.json` records exit status 124 and retains the profile. No congruence obstruction was found at primes 2, 3, 5, or 7. The exact replay file reconstructs every branch without numerical optimizers and marks the unproved branch explicitly.

Thus the currently proved retained profile ranks are **30, 35, and 38**, with one character labelling. `R6_4_629_orbit_h6_strong_primal_replay_O.json` additionally validates an exact rank-35 witness for the stronger height-six system including low Verlinde coefficients and restriction products (5,948 equations, 5,699 variables). A primal witness is not modular data and not a category.

The earlier dense-dual attempt `probe_orbits_h6_strong.json` records a resource interruption, not an exclusion. It was replaced by a successful sparse primal computation. `galois_norm_profiles.json` confirms the existing augmented spectrum normalization on all five profiles; that test is not claimed as a new criterion.

All status changes require exact certificates. Numerical MILP failure, search exhaustion under a resource budget, and a surviving necessary-system witness have no categorification implication by themselves.
