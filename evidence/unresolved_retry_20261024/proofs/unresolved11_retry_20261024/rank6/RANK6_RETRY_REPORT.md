# Fresh theoretical retry: R6_4_155 and R6_8_1660

Neither rank-six case was resolved in this retry. The work produced a new all-even-order necessary character criterion for R6_4_155. The proposed regular Ising bimodule approach to R6_8_1660 was found already covered in the existing manuscript and is not counted as a new reduction.

## R6_4_155

The prior project had tested odd cyclic Clifford constraints. The present retry derives the even-cycle analogue: four insertion-algebra blocks, two fixed by rotation and one exchanged pair, with three explicit spin-character spectra. See `EVEN_CLIFFORD.md`.

All 1,144 new finite tests pass: orders4,6,...,24, both large simple objects, and all52 central targets. `even_clifford_receipt.json` gives nonnegative integer decompositions. `verify_even_clifford.py` verifies every coefficient with standard-library integer arithmetic and rejects a mutated witness. It passed both ordinary and optimized Python.

This is not a rerun of the prior odd test or of ordinary cyclic-integrality tests. It asks whether each cyclic representation extends to the even-cycle stabilizer algebra. Passing it is still only a necessary condition.

## R6_8_1660

The complement of the Ising subcategory is equivalent to the regular Ising bimodule category. The tensor-auto-equivalence input was checked directly in DGNO, RemarkB.6(i). A full reread located this exact argument already in the existing `prop:1660-relative-center`; the prior work also determines its relative-center coefficient object. The audit and its precise limit are in `R1660_REGULAR_BIMODULE.md`.

This makes relative half-braidings available, but extending them over the multiplication channels remains unproved. A central Ising lift, a tensor product decomposition, and a nonpointed algebra must not be inferred from the relative statement.

## Cross-case audit

The rank-nine agent's new forced anticommutator was checked against the existing stabilizer-rotation proof. A two-dimensional cubic invariant space forces the set {-1,-zeta3,-zeta3²}; it does not force -1 when prime3 occurs in the Frobenius–Schur exponent. The weighted Morita total-indicator transfer and the stronger direct-source module-functor argument were independently reviewed. The rank-nine agent owns their complete proofs and any exclusion certificates.

No online files or repository classification statuses were changed by this agent.
