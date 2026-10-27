# Exploratory scripts are not exclusion certificates

The accepted proof and exact replay are `REPORT.md`,
`GALOIS_PARITY_EXCLUSION.md`, `verify_duality_obstruction.py`, and
`verify_galois_parity.py`. Only their receipts support the new result.

The three files prefixed `probe_` retain useful intermediate calculations:

* `probe_bimodule_dual.py` originally searches fourth-root coboundaries.
  Its negative answers are not valid tests over C: rotation duality requires
  eighth roots. The accepted checker explicitly supplies that witness.
* `probe_full_module.py` constructs compatible full module cochains, but its
  tentative identification of the duality cochain with a pivotal tensorator
  has not been established. It also selects only one duality trivialization;
  character twists can change apparent second-indicator sign patterns.
* `probe_rotation_square.py` examines a chosen square coherence only. Its
  nonzero entries do not constitute a categorical obstruction, because the
  remaining character and pivotal normalization freedoms are not exhausted.

None of those probes is used in the accepted reflection, projective-parity,
or Galois-unit proofs. In particular no conclusion about R9_2_137 follows
from their tentative second-indicator output.
