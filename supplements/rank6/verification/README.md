# Verification evidence

`classification/` records the executed ordered sieve, its finite search budgets,
per-ring outcomes, stage counts and exact-checked certificates. A stopped search
is not an exclusion. The source census is trusted at the pinned revision; only
its byte integrity and representative correspondence are checked here.

`continuation/` contains the historical first continuation: its frozen 47
inputs, bounded discovery outcomes, seven accepted exclusions and replay
reports tied to that revision.

`round2/` contains the second continuation. Its manifest freezes all 40
inputs, including all 39 higher-multiplicity residuals, before the ledger
shrinks. `software/round2_release.py` verifies the supported general proof
sources, alternative proofs and both continuations, freezes
`certificates/continuation_round2.jsonl`, and rebuilds the ledger. Its
`release_replay.json` receipt records the exact accepted file and ledger hashes.
`software/continuation_controls.py` independently checks every certificate in
both continuation files with numerical optimizers disabled; use an explicit
`--out verification/round2/replay_optimized.json` to preserve the historical
first-continuation reports.

`current/` contains regression and consistency checks; each retained report
refers to the input and scope recorded when it ran. Normal and
optimized Python modes test explicit error handling, scope guards, mathematical
controls and deliberate corruptions. Each process record states what actually
ran; no earlier smaller census report is relabelled as a multiplicity-eight run.

`release_summary.json` identifies the final ledger, scope and supporting reports.
`document_build_logs/` contains the final LaTeX build logs. Document layout and
cross-reference checks are recorded separately from mathematical evidence.

The commands in the verification guide reproduce classification checks, source
matching, model reconstruction and exact certificate verification. They do not
perform independent census enumeration.

The original release summary is preserved as `original_release_summary.json`.
The revised summary distinguishes inherited exact evidence from checks repeated
on the continuations. The current exclusion count is read from
`data/classification_counts.json`, rather than from a historical report.
A full current-ledger replay is available through `verify.py`; incremental
continuation checking does not claim to have repeated that full run.

The original sixteen-stage campaign and first continuation remain unchanged.
The second accepted JSONL is a disjoint extension, not a rewritten historical
campaign. Complete all-census scans of the new biquadratic and trace-ideal
criteria are retained in `research/round2_external/`; their overlapping
exclusion totals are criterion coverage, not additional ledger allocations.
The higher stabilizer campaign records explicit eligibility and budget
outcomes for the frozen input domain. A failed hypothesis, surviving
relaxation or unfinished search is never an exclusion.
