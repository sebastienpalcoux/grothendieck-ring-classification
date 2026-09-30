# Verification

`current/conformal_models.json` records the fresh exact source/tensor checks
for the three conformal models. `current/release_consistency_optimized.json`
checks the current ledger, five existence columns, tables and residual tensors.
`release_summary.json` states the current partition and exact evidence scope.

The unchanged negative allocation is stored in `certificates/`. Its original
executed sieve and accepted continuation receipts are retained under
`classification/`, `continuation/` and the numbered certificate directories.
Their original dates, input domains and source hashes are evidence for those
proofs; only `data/decisions.json` determines the current classification.

Use `python -O verify.py --jobs 2 --out verification/current/full_recheck.jsonl`
for the complete exclusion replay. Use `python -O software/frontier_replay.py
--list` for the three necessary-profile reductions. Receipt audits do not run
mathematical proofs. A timeout cannot establish an exclusion.
