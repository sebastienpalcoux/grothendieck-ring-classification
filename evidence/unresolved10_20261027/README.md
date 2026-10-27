# Final research checkpoint: ten fusion rings

**Published continuation.** These notes retain the offline research checkpoint and its original source bindings. In the current repository, use `python3 tools/replay_frontier_20261027.py`; the direct commands below apply inside the frozen downloaded proof archive, whose ten-case input is intentionally preserved. See [current decisions and seven-case status](../frontier_20261027/README.md).

Final outcome: **3 excluded over C, 0 new census models, 7 unresolved**.

Excluded: R9_2_1607, R9_2_1975, R9_2_1976.
Unresolved: R6_4_155, R6_8_1660, R8_3_928, R8_3_941, R8_3_1154,
R8_3_1768, R9_2_137.

No online changes were made. The source snapshot is classification commit
6a426acf6465dd674351be92dcca41b72f371521. The report distinguishes new
proofs from inherited results, negative attempts and unresolved gaps.

## Read first

- RESEARCH_REPORT.md: consolidated account of all ten cases.
- r9_noncommutative/GALOIS_PARITY_EXCLUSION.md: R1975 exclusion.
- r9_commutative/GALOIS_FS2_EXCLUSION.md: R1607 and R1976 exclusions.
- r6_155/GALOIS_FROBENIUS_FS2_AUDIT.md and R1975_INDEPENDENT_AUDIT.md:
  independent categorical audits.
- r6_1660/R1975_GALOIS_AUDIT.md and RANK9_SIGNED_GATES_AUDIT.md:
  source bindings and fresh general-scope certificate replays.
- r8_quadratic/REPORT.md and R1768_DUAL_OBSTRUCTION.md: the algebra is
  constructed, but every translated 1+sigma algebra in this precursor
  has the wrong pointed dual and does not model R1768.
- r8_quartic/R1154_NOTES.md: the new rank-ten necessary Morita normal form.
- Each remaining case's REPORT.md records its individual investigation.

Older discovery discussions may describe intermediate branches as surviving.
They are retained to explain failed approaches; the final theorem files
above and STATUS.json control the conclusions. Exploratory probe scripts
are not part of the final verification suite.

## Short exact checks

From the extracted bundle's root (the directory containing data/, evidence/
and supplements/), run the commands below with Python 3. The scripts use
SymPy; the archived signed-gate replays also use NumPy and z3-solver.
The zero-spectrum replay compiles a small C++ program with g++.

    python evidence/unresolved10_20261027/r9_noncommutative/verify_duality_obstruction.py
    python evidence/unresolved10_20261027/r9_noncommutative/verify_galois_parity.py
    python evidence/unresolved10_20261027/r9_commutative/verify_galois_fs2.py
    python evidence/unresolved10_20261027/r6_1660/replay_r1975_gate.py
    python evidence/unresolved10_20261027/r6_1660/replay_rank9_signed_gates.py
    python evidence/unresolved10_20261027/root/verify_diagonal_phase.py
    python evidence/unresolved10_20261027/r6_1660/audit_r1768_phase.py
    python evidence/unresolved10_20261027/r6_1660/verify.py
    python evidence/unresolved10_20261027/r6_155/replay_zero_spectrum.py
    python evidence/unresolved10_20261027/r8_quartic/verify.py
    python evidence/unresolved10_20261027/r8_quartic/r1154_rank10.py
    python evidence/unresolved10_20261027/r8_quartic/r1154_character_check.py
    python evidence/unresolved10_20261027/r8_quartic/distinguished_parity.py
    python evidence/unresolved10_20261027/r9_commutative/verify_source_checks.py

Use normal Python, not -O, for the full suite: some inherited finite checks
use assertions. The exclusion-specific new checkers also work with -O;
the inherited replay wrappers explicitly refuse it.

Checks establish exact arithmetic and completeness of the stated finite
domains. The categorical steps and arbitrary-complex-cochain invariance
are proved in the accompanying text. A passing necessary test never
constitutes a model.

The bundle supplies the direct data dependencies of this suite and the
earlier unresolved-case evidence. Other historical manuscript dependencies
are identified by path and frozen repository commit in the reports; they
are not all duplicated here. BUNDLE_MANIFEST.json records every included
file's SHA-256. The original large replay archive is not duplicated;
its verified minimal signed-gate extraction and provenance are included.
