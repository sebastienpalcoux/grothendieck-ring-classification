# Verification coverage audit — 16 October 2026

> **Historical coverage snapshot, superseded in part on 17 October 2026.**
> This audit describes the October 16 ledger, including its then-accepted R8_2_24 exclusion.
> The subsequent review withdraws that decision: current rank eight is 895 / 77 / 1,
> and 139 of the 140 historical transitions remain accepted. Use
> `tools/verify_review_20261017.py --historical` for the current record and exact
> restored history. See [the dated review](../../../docs/PREPUBLICATION_REVIEW.md).

This is an AI source-code review of verification coverage, not independent human
mathematical verification or Lean formalization. No frozen proof, ledger or
verifier was changed. The publication edits are separate from this audit.

## Main finding

`tools/verify_unified_20261016.py --historical` freshly checks the latest
continuation and its finite predecessor updates, with exact preservation of
all earlier records. It is **not**, by itself, a fresh replay of every base
certificate in the 25,421 / 4,201 / 973 rank-six / rank-seven / rank-eight censuses.
The full base checkers must also run. A manifest hash establishes identity,
not mathematical validity.

The current supplement entrypoints for ranks seven and eight advertise full
replay in their docstrings but delegate before those full loops. They prefer a
bundled `verification-repository` containing stage-c history and run
`tools/verify_upper_residual_20261002c.py`. This can succeed while neither
rechecking all base certificates nor checking the latest unified release.

## What the unified command recomputes

The command uses explicit `need(...)` failures, rather than removable asserts,
to check:

- The fixed SHA-256 of the 610-file source manifest and every listed file.
- Current transition records, census/tensor identity, unchanged-record hashes,
  exact restored parent ledgers, remaining IDs and current totals.
- All 38 originally open-case IDs and their statuses.
- Complete model-catalogue coverage and the full coefficient-by-coefficient
  basis matches for newly recorded constructions.
- Fresh subprocess results for all 39 entries in `replay_manifest.json`.
  Every decision's declared verifier is among those entries. Several entries
  check scoped necessary conditions or independent arithmetic cross-checks;
  a `PASS` does not convert them into new categorification decisions.

The generated reports come from the fresh subprocess output. They are not
accepted solely because a stored receipt says `PASS`. Certificate files are
sometimes inputs, but the checkers verify the proposed identities,
separators, finite branch coverage, or polynomial combinations. For example,
the 2D2 replay regenerates cap/rotation and square equations and checks exact
ideal-membership identities; it does not merely trust a Groebner success flag.
The categorical bridge from those equations to a general existence decision
remains a mathematical proof dependency.

With `--historical`, it reconstructs the exact preceding ledgers and prior
files in a temporary directory, then freshly runs this chain:

| Stage | Recorded transitions | Fresh checks and retained limitation |
|---|---:|---|
| Unified 16 October | 36: 29 exclusions, 7 constructions | 39 listed replays, source and model binding. |
| Earlier theoretical 16 October | 47 exclusions | Each decision verifier plus the specified compression and frontier checks. Its optional `--spectral` backup is not requested by the unified chain. |
| October 2 stage c | 14 exclusions | Ten finite premise replays and restoration of stage b. |
| October 2 stage b | 43: 30 exclusions, 13 constructions | Nine premise/model scripts, recovery check, original residual update, and AnyonWiki replay. |
| Original residual update | 46 decisions | Rank-seven/rank-eight update scripts and scoped portable obstructions, tied to original tensors. |
| AnyonWiki import | 8 additional models | All 139 multiplicity-one tensor crosswalks, model permutations and three exact rank-seven associator replays. Rank-eight existence and unitary gauges retain cited construction dependencies. |

No stage in that chain calls the original all-record rank-seven or rank-eight
base `main()` loop. Rank-six ledger preservation is checked, but its full
25,362 negative-certificate replay is also a separate command.

## Full base replays needed to close that coverage gap

| Rank | Exact input coverage | Practical fresh entrypoint |
|---:|---|---|
| 6 | All 25,421 records; 25,362 exclusions, 56 unitary models, one other spherical model, two unresolved | From `supplements/rank6`, normal Python `verify.py --jobs 2 --out /absolute/audit/receipts.jsonl`. It checks source hashes/coverage, constructors, scoped structures, frontier evidence, and each accepted negative certificate. Census exhaustiveness and uniqueness are inherited from the pinned source census. |
| 7 | All 4,201 records at the exact pre-stage-b boundary: 4,116 exclusions, 26 models, 59 unresolved | Restore the pre-b files and ledger in scratch, then run the original `supplements/rank7/verify.py --workers 2` in **normal Python**. Combine with current unified `--historical` for all later decisions. |
| 8 | All 973 records at the exact pre-stage-b boundary: 832 exclusions, 60 models, 81 unresolved | Restore the pre-b files and ledger in scratch, then run the original `supplements/rank8/software/verify.py` in **normal Python**. It additionally replays 75 imported rank-eight signed proof trees and four rank-seven subring trees, and checks six published full-tensor transfers. Combine with current unified `--historical` for all later decisions. |

The scratch helper `restore_pre_b_snapshot.py` reverses the unified,
theoretical, c and b transitions. At each step it checks current changed
records, unchanged records and the complete canonical parent digest. It
restores the unified parent-file archive against its inventory and checksums,
and the stage-c / stage-b baseline files. The final eleven stage-b files are
checked byte-for-byte. It does not change the source repository.

The pre-b complete-ledger canonical SHA-256 values are:

- Rank seven: `2a6c64f4d8d41a9b13b75ce7e8181e7823db64cc9a3fb80dd5e7ef876616b543`.
- Rank eight: `6717588bf6d1c2c9ece32e52eca2dd46fd81257b44f31d9bf3c75b854ebc415c`.

The historical full loops rely on exact lower-rank classification theorems and
positive catalogues for subring transfer. Their own census enumeration is
not rerun. Root audit work separately addresses the lower-rank replay paths.
The original rank-seven checker compares every source tensor with its ledger,
reconstructs all model matches and checks all negative certificates, including
246 exhaustive oriented signed certificates. It does not independently redo
the upstream census's isomorphism-class enumeration.

The arithmetic of the coverage bridge is exact: at rank seven, the 59 pre-b
open records become 56 additional exclusions and three models, giving
4,172 / 29 / 0. At rank eight, the 81 pre-b open records become 64 additional
exclusions and 17 models, giving 896 / 77 / 0. Those 140 changes are precisely
the 43 + 14 + 47 + 36 transitions in stages b, c, theoretical and unified.
Thus a successful full pre-b replay plus successful preservation and replay
of those stages covers all current decisions without needing to change the
frozen baseline checker to understand later certificate kinds.

## Optimization and assertion scope

All 49 Python files in `evidence/unified_20261016` were parsed for `ast.Assert`:
none contains an assert statement. The unified dispatcher and major historical
stage dispatchers use explicit exceptions. Thus the important checks in that
new source are not erased by `python -O`.

That observation must not be generalized to the entire repository. The
original rank-eight full checker uses removable asserts for fusion axioms,
source matches, certificate equality, model basis maps and totals. Its
`experimental_signed/verify_imported.py` and `verify_signed.py` also use
asserts for input binding. Some older rank-seven constructor/source checks use
asserts as well. Run the full base replay in normal Python. A successful
optimized run is supplementary evidence, not a substitute for the normal run.
The rank-eight full checker launches the imported-proof subprocess without
`-O`, but this does not restore assertions removed from its own parent process.

## Explicitly retained dependencies and non-recomputed inputs

- The mathematical lemmas connecting finite calculations to categorical
  conclusions are still prose proofs. They have not been mechanically proved
  by these Python scripts, nor independently human-verified or formalized in
  Lean.
- Lower-rank subring transfers depend on the cited classification ranges and
  correct positive catalogues; they do not reproduce those classification
  proofs inside every upper-rank check.
- Rank-eight published appendix transfers check exact source matches and
  stated hypotheses; they do not rerun the cited Normaliz induction search.
- The historical `rank6/r1660_modular_witness/replay.py` freshly checks its
  integer witness, all stored equations, reconstructed new constraints and
  CRT products. It explicitly treats the older actual48 rows and finite-group
  character data as source-bound inputs, not regenerated outputs. That
  witness has necessary-condition scope only and is now rejected by a later
  Verlinde check; no general rank-six decision follows from it.
- Proof-source hashes, stored reports and frozen manuscript hashes establish
  provenance, not independent validation of the contents.

## Documentation and reading corrections

1. `docs/VERIFY.md` says historical constructor replays run automatically, but
   the nearby advertised unified commands omit `--historical`. Without that
   option the report explicitly says history was not requested. The CI
   workflow correctly includes the option.
2. Frozen `supplements/rank7/README.md` reports 4,164 exclusions / 27 models /
   10 unresolved, and rank-eight's README reports 875 / 72 / 26. These are the
   earlier theoretical boundary, not current 4,172 / 29 / 0 and 896 / 77 / 0.
   Their direct theoretical-stage commands also expect that earlier boundary.
   Redirect readers through a current guide or dated errata while preserving
   frozen sources.
3. The current rank-seven and rank-eight `verify.py` dispatch behavior must be
   described accurately. A reader should not infer an all-record base replay
   from the old docstring or a later-stage `PASS`.
4. “Complete”, “certified”, “verified” and “independent audit” need the public
   caution context: recorded research coverage or computational scope, not
   human verification. Independent audit documents in this AI-generated
   research record are additional AI review passes.

The locally revised README and site README now make those distinctions
prominent, link the planned dated prepublication review, and retain the two
unresolved rank-six IDs.

## Fresh-run outcome

**PASS: the original full rank-seven checker exited 0 in normal Python with
two workers.** It freshly checked all 4,201 pre-b records: 4,116 exclusions,
26 model matches and 59 then-unresolved records. The log is
`rank7_full_base_replay.log`; the structured result is
`rank7_full_base_report.json`. The original full-loop verifier SHA-256 is
`6ffa5bece7290ec206027000d8750bf2aec73bb5efe83c17aea1424d4d953c73`.

The portable public helper at
`evidence/prepublication_20261017/restore_pre_b_snapshot.py` was also run
successfully. It checked the fixed manifests for 610, 268, 281 and 201 files
at the four reversed stages. Its output was compared byte-for-byte with the
successful full-replay input: both complete upper-rank ledgers and all eleven
terminal baseline files match. `FULL_REPLAY.md` documents the normal base
commands and required current unified history commands.

The root audit owns the rank-six full run and unified normal/optimized history
runs; the rank-eight auditor owns its corresponding full base replay. Those
outcomes are recorded in their own receipts rather than inferred here.
