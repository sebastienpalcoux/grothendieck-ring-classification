# Full upper-rank replay, including the base certificates

The current review verifier checks the reopened record, then restores the exact
frozen unified snapshot in isolation. The unified verifier checks its historical decisions, their
source bindings and exact preservation of earlier stages. Its `--historical`
option replays those earlier finite updates. The original full base checks
are a separate step: the current supplement wrappers delegate to historical
update scripts before reaching the old all-record loops.

The helper in this directory restores the exact pre-stage-b files in a new
isolated directory. It checks the fixed source-manifest identities for all
four reversed stages, every source file in those manifests, all changed and
unchanged records, the complete canonical parent ledgers, and the prior model
files. It does not edit the source repository or change any frozen verifier.
It refuses an existing output directory or an output inside the source tree.
Restoration alone is not mathematical verification.

## Reproduce

Use normal Python for both original full checkers: some of their critical
checks use `assert`, which `python -O` removes. The optimized current-stage
run below is an additional check, not a replacement for normal Python.
The replay environment needs Python 3.12 or later, SymPy 1.14.0, NumPy 2.3.5
and a C++17 compiler available as `g++`. The signed enumeration engines compile
temporary exact integer programs. No network is used by the replay itself.

From the classification repository root:

```bash
python3 tools/restore_data.py
GRC_AUDIT=$(mktemp -d)
python3 evidence/prepublication_20261017/restore_pre_b_snapshot.py \
  --repo . --output "$GRC_AUDIT/base"

(cd "$GRC_AUDIT/base/supplements/rank7" && python3 verify.py --workers 2) \
  > "$GRC_AUDIT/rank7-full-base.log" 2>&1
(cd "$GRC_AUDIT/base/supplements/rank8/software" && python3 verify.py) \
  > "$GRC_AUDIT/rank8-full-base.log" 2>&1

python3 tools/verify_review_20261017.py --historical \
  > "$GRC_AUDIT/unified-history.log"
python3 -O tools/verify_review_20261017.py --historical \
  > "$GRC_AUDIT/unified-history-optimized.log"
```

Check each command's exit status. Do not interpret a timeout or interrupted
run as a pass or an exclusion. The base checks can take substantially longer
than a consistency check. Their generated reports are written in the isolated
copy; the source repository's frozen reports remain unchanged. The restoration
receipt is saved beside that copy as `base_restoration.json`.

## Coverage

| Rank | Full pre-b input | Pre-b exclusions / models / open | Later changes checked by the unified history chain | Current recorded totals |
|---:|---:|---:|---|---:|
| 7 | 4,201 records | 4,116 / 26 / 59 | 56 exclusions and 3 constructions | 4,172 / 29 / 0 |
| 8 | 973 records | 832 / 60 / 81 | Historical 64 exclusions and 17 constructions; R8_2_24 then reopened | 895 / 77 / 1 |

The 140 historical transitions are exactly the 43 + 14 + 47 + 36 decisions in
stages b, c, theoretical and unified. The review withdraws one exclusion, so
139 decisions remain accepted: rank-seven 56 exclusions and 3 constructions;
rank-eight 63 exclusions and 17 constructions, with R8_2_24 reopened.
Exact preservation checks connect the historical transitions
to the base ledgers. The full rank-eight loop also replays 75 imported
rank-eight signed proof trees and four rank-seven subring trees, and checks
six published full-tensor transfers. Census exhaustiveness and the cited
mathematical classification theorems remain explicit input dependencies.

## Rank-six combined replay

**The newly supplied orchestration below has not been executed end to end.**
Its source/input checks and rejection controls have been tested; this is not a
claim that an all-Python full replay passed. See the
[rank-six backend packet](rank6_backend/README.md) for the actual audit records
and their completion status.

The audit combines the original complete run's receipt stream, strict
Python-backend replays of every failed complete certificate, separate execution
of the original post-loop count and positive-registry checks, and an aggregate
coverage audit. The original process's failure status and raw failed records
remain preserved. Its loaded backend and version were not measured at startup.
The global python-flint installation changed from 0.8.0 to 0.9.0 during the run;
existing workers may have retained 0.8.0 while later child processes loaded
0.9.0. The Flint backend is inferred from the default environment and reproduced
failures, and no uniform initial runtime version is established. The new wrapper
records requested and observed backends and package versions per child process.

Use a **fresh restored checkout**, with no pre-existing native binaries beside
the rank-six C++ sources. From that checkout's repository root, install the
frozen requirements in an isolated environment and choose a new output directory:

```bash
python3 tools/restore_data.py
python3 -m pip install -r supplements/rank6/requirements.txt
python3 evidence/prepublication_20261017/rank6_backend/replay_complete.py \
  --repo . --output-dir NEW_DIR --jobs 2
```

Replace `NEW_DIR` with a nonexistent directory outside `supplements/rank6`.
The wrapper refuses existing native caches; it does not delete another run's
binaries. The frozen requirements pin SciPy 1.17.0 and python-flint 0.9.0;
the new orchestration remains untested end to end in that environment.

In fresh normal-Python subprocesses, the wrapper first runs the unchanged full
verifier with the FLINT backend. It requires exactly 25,362 ordered exclusion
outcomes, each with the correct ID, certificate kind and Boolean result.
If failures occur, only the verifier's final negative-certificate failure gate
is accepted as the initial stopping point. Every failed complete certificate
must then pass the unchanged worker under the Python backend; missing, failed
or mismatched retries abort the campaign. The original two post-loop checks
run separately under Python. Source/input identities and certificate/tensor
hashes bind the stages; fresh temporary directories and recorded compiled
binary hashes distinguish the native calculations.

Some frozen algebraic character tuples use backend-dependent string ordering,
which changes the order or orientation of saved balance equations. The selected
Python replays retain the historical certificate convention and check every
exact condition; no failed condition is suppressed. A combined success summary
is written only after complete coverage and all final checks succeed. It does
not relabel an unsuccessful initial run as a successful single run.
The ledger contains 25,421 records and retains `R6_4_155` and `R6_8_1660` as unresolved.

## What a successful replay means

A pass establishes the calculations and input bindings checked by these
programs. It does not prove every categorical reduction or cited theorem,
independently enumerate the upstream census, rerun the published Normaliz
searches used by appendix transfers, or constitute human verification or Lean
formalization. Read the [dated review and errata](../../docs/PREPUBLICATION_REVIEW.md)
and [research-status notice](../../docs/RESEARCH_STATUS.md) alongside the results.
