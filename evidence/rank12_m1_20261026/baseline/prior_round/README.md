# Rank-12 multiplicity-1: third offline continuation

Current total: **438 excluded, 148 unitary models, 46 unresolved**, among 632 supplied based rings.
This round resolves 20 of the former 66 unresolved cases: **13 exclusions and 7 models**.
No repository or website was revised. Independent human verification remains pending.

## Contents

- `report.pdf` / `report.tex`: research report and source.
- `ledger.json` / `ledger.csv`: all 632 permanent IDs, statuses and original tensor hashes.
- `new_decisions.json`: 13 exclusion routes and seven complete model tensors with basis bijections.
- `unresolved_tensors.json` / `remaining_cases.csv`: all 46 open cases and their exact family-specific gaps.
- `round3/`: detailed proofs, actual categorical data, exact certificates, independent audits and replay code.
- `prior_round/`: unchanged prior-round snapshot, including earlier evidence and its separate replay.

## Reproduction

Install the small dependencies in `requirements.txt`, then run:

```sh
python verify.py
python -O verify.py
```

These commands reconstruct all accepted new models and exclusion arithmetic, replay the independent audits,
check the 632-record ledger against the frozen baseline, and verify every new source-to-model coefficient.
They require no network, GAP database, optimizer, local repository, or compiled discovery executable.
They also check the structural D144 reduction and the quadratic restrictions without changing unresolved statuses.
To replay the earlier results, first copy `prior_round/` to a separate directory and run its `verify.py` there.
That verifier writes new receipts; keeping the delivered `prior_round/` unchanged preserves the immutable
baseline check in `prior_snapshot_manifest.json`. Its original successful receipts are included.

The main verification logs are in `verification/`. The final delivery was also replayed in an isolated directory
with access to the original workspace denied. `portability.json` records that check.

## Scope of the proofs

The D120 exclusions use a complete categorical converse, the forced order-ten subgroup, exhaustive relative
cohomology, and the coprime-twist lemma. The R350 exclusion uses a published Galois-to-pseudo-unitary gate,
all 30 low frames, and all 32 exact Farkas rays. Numerical failure or a timeout is never an exclusion.
All seven positive decisions use actual unitary categories and separable algebras, not just candidate tables.
The D144 t=0 branch is ruled out, but its four rings remain open in the t=3 branch.

Files whose names contain `probe`, `attempt`, `search`, or `discovery`, and historical notes in `round3/root/`,
document bounded explorations. Some discovery scripts retain original workspace paths and optional tools;
they are not required by `verify.py` and are not proofs of an exhaustive classification.
The frozen positive witnesses and accepted replay entry points are the authoritative computational evidence.

The specific constructions are recorded without asserting novelty up to tensor equivalence.
