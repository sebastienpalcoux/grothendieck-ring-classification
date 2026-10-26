# Rank 12, multiplicity 1: completion

The final ledger contains **480 excluded, 152 modeled, and 0 unresolved** rings.
Only the previous three unresolved entries change. The other 629 record objects
are retained exactly. Of the modeled rings, 151 have previously established
unitary realizations; the new R12_1_623 realization is complex/pseudo-unitary,
with unitarity unproved. No online revision was performed.

Read `report.pdf` for the six-page proof synthesis and references. The two
commutative rings R12_1_561 and R12_1_628 share a new equality-case refinement
of the dimension-block conductor bound, combined with the previously proved
central C3 lift. R12_1_623 is the cyclic near-group isotropic quotient described
in `round5/models/R623_NEAR_GROUP_MODEL.md`. Its construction extends to every
k congruent to 2 modulo 4. The full mixed-associator convention audit is in
`round5/premises/R623_model_audit.md`.

The final `ledger.json`, `ledger.csv`, `summary.json`, `new_decisions.json`, and
`resolved_tensors.json` are authoritative for this continuation. Status
`pseudo_unitarily_realized` counts as modeled and does not claim unitarity.
All tensor maps are unit-preserving maps in the documented direction.

## Verification

Run `python3 -O verify.py` with Python 3 and SymPy. It checks the complete
632-record ledger and its three-entry delta, the frozen baseline, the new
tensor bindings, the forced-central-C3 section exhaustion, and all four new
exact replays. Replays run in an isolated temporary copy. Receipts are written
to `verification/`; the immutable evidence and baseline are not modified.
Run `python3 -O verify.py --baseline` to repeat the preceding full 32-check
audit as well. This optional longer replay is not needed to verify the delta;
the preserved baseline contains its earlier successful receipts.

`baseline/` is a byte-for-byte copy of the complete preceding proof packet,
including its historical ledgers, sources, and validation receipts. References
in unchanged legacy records retain their preceding packet's path convention;
resolve them using that packet's README and evidence tree. Their historical
counts are not current counts. `baseline_snapshot_manifest.json` binds every
file in that snapshot. `MANIFEST.sha256` binds this package except regenerable
top-level verification receipts.

The arithmetic programs are application and tensor checks, not machine proofs
of the categorical theorems. Existence uses the pinned algebraic near-group
preprint; no unitarity conjecture or completeness of a unitary classification
is assumed. Proof reviews were conducted by separate assistant agents;
independent human verification remains pending.

Supplementary notes on center profiles, semion nonsplitting and the Morita
route are retained as exploratory safeguards. They are not used to classify
an input unless cited explicitly in `new_decisions.json`.
