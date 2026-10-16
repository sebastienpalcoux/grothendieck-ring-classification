# Rank-six checks skipped after the negative-certificate failure gate

**PASS for the two isolated post-loop checks. This is not a full-replay PASS.**

The unchanged `supplements/rank6/verify.py` stops at line 122 when any negative
certificate fails. Its next two checks, at lines 123–125, were run separately
in normal Python with `SYMPY_GROUND_TYPES=python`. The harness extracts and
executes the four original AST statements directly, rather than rewriting
their mathematical conditions or invoking the full verifier.

| Check | Expected | Observed |
| --- | --- | --- |
| Multiplicity-one records | 39 | 39 |
| Multiplicity-one exclusions | 18 | 18 |
| Multiplicity-one unitary realizations | 21 | 21 |
| Positive registry coverage | Exact equality with the ledger's positive IDs | Equal: 57 IDs in each set; no extra or missing IDs |

The positive ledger contains 56 unitary records and one spherical,
non-pseudo-unitary record. The original `positive_registry()` also validates
the registry existence metadata and checks consistency when a ring has more
than one registered model. No model constructors or negative certificates
were rerun here.

After these two checks the verifier only assembles the success statistics,
writes its summary JSON, prints it, and returns zero. There are no additional
post-loop verification conditions. Those summary-producing statements were
not executed, so this check does not manufacture a success summary for the
failed original full replay.

## Command and environment

From `/workspace/scratch/b038cfaffb82`:

```sh
SYMPY_GROUND_TYPES=python PYTHONDONTWRITEBYTECODE=1 python3 \
  work/prepublic_audit/rank6_postloop/check_postloop.py \
  --repo work/prepublic_audit/replay_repo \
  --inventory work/prepublic_audit/remote_inventory.json \
  --output-dir work/prepublic_audit/rank6_postloop \
  > work/prepublic_audit/rank6_postloop/run.log 2>&1
```

Exit status: **0**. Python **3.12.14**, SymPy **1.14.0**, normal mode;
SymPy's observed ground-type backend was **python**. Runtime: approximately
**1.20 seconds**.

## Source and input identity

The audit's original remote reference is commit
`e6a36a6f247b2db05f5468ffd4be1752ff42f157`, tree
`037b0822e5086c706ca221bcb416a28dd1c760be`.

All **15 directly tracked files** used for this check matched their original
Git blob SHA-1 and byte length in `remote_inventory.json`: the verifier,
`software/exact.py`, `software/existence.py`, all eleven registry JSON inputs,
and `data/large_files_manifest.json`. Every SHA-256, Git blob hash, and byte
length is recorded in `receipt.json`.

The sixteenth file, the restored `data/decisions.json`, is represented in Git
by compressed payloads. Its **25,584,731 bytes** have SHA-256
`abb36cb0e7f9196e0a231cb85a601c82a1c8fd398996f77a8961487a7ca692e5`,
exactly the commitment in the original Git-bound large-file manifest.
The materialized local checkouts omit the compressed payload chunks; this run
therefore checks the restored ledger against that manifest, without claiming
a fresh payload reconstruction. Two preliminary harness attempts stopped on
missing payload paths before any post-loop check; their logs are preserved as
`attempt1_missing_payload.log` and `attempt2_missing_payload.log`.

All sixteen source and input files had identical hashes before and after the
successful run. No frozen sources, ledgers, registries, or original replay
receipts were edited.

## Files

- `check_postloop.py`: complete isolated harness, including identity checks.
- `executed_original_statements.py`: exact original statements executed.
- `unexecuted_summary_statements.py`: original remaining summary-only code.
- `receipt.json`: expected/observed results, all 57 positive IDs, complete
  source/input identities, environment and command.
- `run.log`: successful process output.

This was an AI-performed audit; it does not constitute independent human
verification or Lean formalization.
