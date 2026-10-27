# Audit and continuation: seven unresolved fusion rings

**Published continuation.** These notes retain the offline research checkpoint and its original source bindings. In the current repository, use `python3 tools/replay_frontier_20261027.py`; the direct commands below apply inside the frozen downloaded proof archive, whose ten-case input is intentionally preserved. See [current decisions and seven-case status](../frontier_20261027/README.md).

Start with `RESEARCH_REPORT.md`. The three prior general-complex exclusions
R9_2_1607, R9_2_1975, and R9_2_1976 are retained after fresh audit.
No additional census ring is excluded or modelized in this continuation.

The remaining seven are R6_4_155, R6_8_1660, R8_3_928, R8_3_941,
R8_3_1154, R8_3_1768, and R9_2_137.

Important new results include the pairing-parity obstruction for Morita
forgetful functors, exclusion of every GH(C6,2) Morita realization of R1768,
two excluded R1660 module realizations, simple centralizer restrictions
for R928/R941, and identity of all six R1154 trivalent rotations. These
statements have the exact scope and inherited dependencies stated in the
case proofs. They are not exclusions of those census rings.

## Short exact replays

Run from the root containing `data/` and `evidence/`, using Python 3 and
SymPy. Numerical optimizers are not needed for these saved-certificate replays.

```
python evidence/unresolved7_20261027/audit_fs2/verify_r155_algebra_reduction.py
python evidence/unresolved7_20261027/audit_fs2/verify_r1660_bimodule_parity.py
python evidence/unresolved7_20261027/r6_1660/verify_spin_constraints.py
python evidence/unresolved7_20261027/r8_928_941/verify.py
python evidence/unresolved7_20261027/r8_1154/verify_odd_rotation.py
python evidence/unresolved7_20261027/r8_1154/verify_integral_center.py
python evidence/unresolved7_20261027/r8_1768/verify_morita_parity.py
python evidence/unresolved7_20261027/r8_928_941/audit_r1768_profiles.py
python evidence/unresolved7_20261027/audit_parity/verify_r137_positive_fs2.py
```

The same new verifiers support `python -O`. The R137 witnesses satisfy
necessary relaxations; they are not models. The R1154 certificate files
whose names contain `probe` are final exact certificates and are retained;
exploratory `probe_*.py` scripts are omitted from the deliverable archive.

## Archived evidence and scope

The accompanying archive also retains the previous ten-case evidence bundle
and the direct data dependencies of the new replays. Older reports describe
their own dated checkpoint; the present report controls the current research
status. The previous bundle's `BUNDLE_MANIFEST.json`, where present, describes
that earlier snapshot only. `CONTINUATION_MANIFEST.json` describes this archive.

The mathematical premises of older complete domain/gate proofs remain
explicit dependencies at frozen public repository commit
`6a426acf6465dd674351be92dcca41b72f371521`. Short checks verify finite claims
and certificates; they do not independently prove every inherited theorem.

No online updates have been made. This folder is research evidence, not a
replacement for the public classification ledger or source manuscripts.
