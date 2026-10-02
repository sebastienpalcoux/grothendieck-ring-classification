# Rank-six local computations, 2 October 2026

**R6_4_155 and R6_8_1660 remain unresolved**, including in the unitary class.

- [R155 braid computation](r155_braid_scott/): an exact, interruptible Python program for 226 additional braid blocks of dimensions 6–308. It combines generalized Frobenius–Schur indicators with necessary conditions on all possible irreducible constituents. The README gives a two-hour command and explains the JSON results to return. Python 3.9 or later is sufficient; no extra package or network access is needed.
- [R1660 restriction-product computation](r1660_pair_lifting/): an exact, resumable integer search for low–high and high–high products across all 1,136 surviving profiles, represented by 628 distinct ungraded restriction multisets. It retains repeated-object multiplicities and does not select a charge assignment. Python's standard library is sufficient.
- [All-exponent Minkowski proof](all_p_minkowski/): completed exact certificates proving every Lim Corollary 3.4 inequality on the two given six-element fusion bases, for all real exponents p >= 1 and all nonnegative vectors. This family cannot supply a new exclusion of either original tensor.

The braid program is a new necessary-condition search, not a categorification algorithm. A passing partition constructs no braid representation or category. A timeout is `UNKNOWN`; a candidate obstruction must be independently replayed and audited before any classification decision changes.

Download the complete portable packages: [R155 ZIP](r155_braid_scott_laptop.zip) and [R1660 ZIP](r1660_pair_lifting_laptop.zip). Keep each package's files together. The full searches have not been run; only controls and bounded pilot computations were performed. Return `r155_braid_results.json` and `r1660_results.json` for interpretation. Passing the second computation establishes only separate necessary product decompositions, not a consistent center fusion rule or category.

The [research addendum](../residual_20261002/rank6/research_addendum.pdf) records the proved reductions. The 533-profile reduction for R6_8_1660 leaves 1,136 profiles; it does not construct a center or exclude categorification.
