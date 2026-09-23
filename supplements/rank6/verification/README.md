# Verification evidence

`classification/` records the executed ordered sieve, its finite search budgets,
per-ring outcomes, stage counts and exact-checked certificates. A stopped search
is not an exclusion. The source census is trusted at the pinned revision; only
its byte integrity and representative correspondence are checked here.

`current/` contains current regression and consistency checks. Normal and
optimized Python modes test explicit error handling, scope guards, mathematical
controls and deliberate corruptions. Each process record states what actually
ran; no earlier smaller census report is relabelled as a multiplicity-eight run.

`release_summary.json` identifies the final ledger, scope and supporting reports.
`document_build_logs/` contains the final LaTeX build logs. Document layout and
cross-reference checks are recorded separately from mathematical evidence.

The commands in the verification guide reproduce classification checks, source
matching, model reconstruction and exact certificate verification. They do not
perform independent census enumeration.
