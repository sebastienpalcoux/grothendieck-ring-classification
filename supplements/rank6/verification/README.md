# Rank-six verification

The [complete replay guide](../../../docs/VERIFY.md#complete-rank-six-route)
describes the public route and exact environment requirements. The executed
campaign covers all 25,362 exclusions through 25,355 initial passes plus seven
complete Python-backend retries and two separately replayed post-loop checks.
The initial full process failed; this is a combined campaign, not a successful
single full run. The portable orchestrator has not itself been executed end to
end. Its identity and rejection controls were tested.

`current/conformal_models.json` records the three exact conformal-model tensor
checks. `current/release_consistency_optimized.json` checks the ledger, tables
and residual tensors. `release_summary.json` records its stated partition and
evidence scope. The source-bound certificate directories record exact inputs
and program results. Only `data/decisions.json` determines classification.

Receipt audits verify hashes and completion predicates; they do not execute
the mathematical proof. Use normal Python for checks implemented by `assert`.
A timeout proves no exclusion. All results are AI-generated, not independently
human-verified and not Lean-formalized; use them with caution.
