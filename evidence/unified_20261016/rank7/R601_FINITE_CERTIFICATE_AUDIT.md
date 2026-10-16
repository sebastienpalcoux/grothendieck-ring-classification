# Independent finite-certificate audit for R7_3_601

## Result

The exact induction-lattice verifier was independently read and replayed successfully against the repository source. Together with the separately checked categorical premises in `R601_CATEGORICAL_PREMISES_AUDIT.md`, it proves a general complex noncategorifiability result for `R7_3_601`.

The audited source tensor has compact-JSON SHA-256

`afbed9441f88f4ba296235d0dd6220f41ecbcf97a7424220125e73f255ff489c`.

Audited file digests:

- `verify_r601_center_lattice.py`: `879a16ad5f5f23d0f256aef8e45fc7fa9d74820023d3aa86128b121a322eb6e8`;
- `r601_center_lattice_certificate.json`: `603d62bad474618c9359380ea6d5650a2286c52447164351f64465eb2d72457f`.

## Coverage checks

1. **Source and characters.** The verifier loads the immutable census line, binds it both by SHA-256 and by the ledger tensor, and verifies associativity, commutativity, self-duality, the seven complete orthogonal characters, their codegrees, positive dimension character, and based-ring simplicity. Consequently the six nonunit summands of induction of the unit have the required dimensions 24, 40, 40, 45, 90, 120 and unit-coordinate 1. The central unit is handled separately by its exact forgetful row.

2. **All induction-of-unit blocks.** Each row is enumerated over a finite box implied by the first row and diagonal of the full induction Gram matrix. The dimension equation is imposed exactly. The row sum is exactly the first column of that Gram matrix after subtracting the unit row. Equal-dimension rows are sorted only to remove a permutation redundancy. Every pruning step is necessary: nonnegative remaining coordinates, entrywise nonnegative Gram remainder, nonnegative principal 2-by-2 minors, and positive semidefiniteness. The resulting 336 blocks are regenerated, rather than trusted from a supplied list.

3. **Exact positive semidefiniteness.** The fraction-free elimination step replaces the lower block by a positive multiple of its Schur complement. Division is only by a positive common divisor. If a diagonal pivot is zero, positive semidefiniteness requires the whole corresponding row to vanish, which is checked. Thus this filter cannot remove an actual nonnegative sum of outer products through a numerical threshold or an invalid pivot rule.

4. **All remaining central rows.** Every remaining simple has zero unit-coordinate. The initial six-coordinate box follows from diagonal entries of the full Gram matrix. Its dimension lies in the categorically justified list of non-prime-power divisors of 360. The initial entrywise outer-product bounds leave 4700 candidates. For each of the 336 blocks, the residual matrix is independently shown positive definite by exact rational elimination; the computed scaled inverse is checked by multiplication. A genuine remaining row must satisfy both the residual entrywise bounds and the rank-one condition `v^t R^{-1} v <= 1`. These conditions are imposed with integer arithmetic after clearing denominators. The fact that only necessary conditions are imposed enlarges the set of candidate rows and cannot create a false obstruction.

5. **Terminal contradiction.** For every block the stored finite-field vector annihilates the outer product of *every* candidate row retained by the preceding exhaustive test, while pairing to 1 with the residual Gram matrix. Since a sum of these outer products, with arbitrary nonnegative integer multiplicities, would have pairing 0, no Gram completion exists. This is a lattice obstruction, so no bound on the number of central simples and no integer-programming assumption is involved.

## Replay outcome

The independent ordinary Python replay returned:

- exact recursion node counts: 1, 8, 78, 212, 398, 336, 336;
- regenerated low blocks: 336;
- global candidate columns: 4700;
- candidate columns per block: 1 through 111;
- congruence certificates: 218 modulo 2 and 118 modulo 3;
- status: `PASS`.

All mathematical checks use explicit exceptions rather than Python `assert` statements. The proof and verifier use no floating-point computation, numerical spectral test, LP solver, MILP solver, or symbolic-algebra package. The normal and optimized replay receipts supplied alongside the certificate agree on these counts.

## Theoretical boundary

The finite part proves that the stipulated integral simple modular center cannot exist. Its application to every hypothetical complex categorification uses the independently audited deductions: integrality implies pseudo-unitarity; the source cannot be braided; the LPR simple-center theorem applies; and the prime-power-dimension theorem excludes all nontrivial prime-power-dimensional central simples. No unitary assumption has been introduced by the finite certificate.
