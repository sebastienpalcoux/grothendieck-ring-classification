# General exclusion of R901 by complete octic low-S symmetry

Use the distinguished-central-simple symmetry formula established in
`ATOMIC_SPECTRUM_REVIEW.md` and the complete character field established
in `OCTIC_CHARACTER_ADAPTER.md`. For R901 the seven raw low-column domain
sizes are 6, 9, 4, 4, 12, 12, 20. The complete induction Gram bounds leave 2024
raw low frames. No high restrictions, partial-S integrality filter,
twist assumptions beyond the standard distinguished-simple theorem,
or linear programming is needed.

For each frame, the distinguished-simple dimensions permit exactly four
bijections with the eight characters. All 8096 full bijections violate
S symmetry. The primary recursive assignment search and an independent
unpruned enumeration of complete dimension-compatible permutations agree.
The latter evaluates S symmetry only after the whole bijection has been
formed, so it does not reuse the primary recursion or its pruning. The
known complex model `Fib tensor Vec(C4)` has 576 such permutations for
its supplied actual low frame, and all 576 pass the same independent test.

The general signed lift is complete. The ordinary character polynomial
has two quartic factors: the FP Galois orbit is excluded by the low-S
obstruction, and the other orbit violates duality of dimensions. There
are 32 oriented signed branches. Sixteen are gauge equivalent to the
original ring; each of the other 16 has one character orbit violating
duality and one ruled out by the formal-codegree norm condition at 3.
The latter orbit has global-dimension polynomial

\[
 t^4-240t^3+4560t^2-28800t+57600.
\]

Every branch is reconstructed and checked by the existing exact signed
verifier. Thus R8_3_901 has no complex fusion-category categorification,
without a pivotality or unitarity hypothesis.

The three no-argument read-only replays are:

- `octic_low_s_symmetry.py`: complete 2024-frame primary witness;
- `octic_low_s_general.py`: complete general signed certificate;
- `review_octic_low_s.py`: independent 8096-bijection enumeration,
  complex positive control, and general certificate replay.

Their corresponding `_results.json` receipts bind the original source
tensor, the frozen native complete-frame enumerator, the octic adapter,
and the general certificate. The native executable is compiled in a
temporary directory; frozen evidence is not modified.
