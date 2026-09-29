# Classification software

These directories expose the exact exclusion engines and verification entry
points accompanying the rank-specific manuscripts. Restore the compressed
repository datasets with `python3 tools/restore_data.py` before running the
checks. Rank six includes the complete revised research release, including
its census data, model catalogs, all three continuations, exact proof sources and
verification records. Other rank directories describe any full source-release
inputs needed by their verifiers. Copying just `software/` and `verify.py`
does not create a self-contained verification run.

| Rank | Source | Required full input |
|---:|---|---|
| 4 | [`rank4/software/`](rank4/software/) and [`verify.py`](rank4/verify.py) | Rank-four source release, including 75.8 MB compressed classification ledger |
| 5 | [`rank5/software/`](rank5/software/) and [`verify.py`](rank5/verify.py) | Rank-five source release, including its decisions and exclusion certificates |
| 6 | [`rank6/software/`](rank6/software/) and [`verify.py`](rank6/verify.py) | Complete revised release included here; 16,548 excluded, 54 realized, 10 unresolved; general classification complete through multiplicity 3 and separately at exact multiplicity 7 |

The public [fusion-ring-census](https://github.com/sebastienpalcoux/fusion-ring-census)
continues to own the raw tensor census and enumeration code. See the
[verification guide](../docs/VERIFY.md) for the crosswalk and local checks.
Any copied licensed census code retains its license and notice in the
rank-specific software directory.


For the rank-six update, start with its [README](rank6/README.md),
[revision notes](rank6/REVISION_NOTES.md), and
[current release summary](rank6/verification/release_summary.json).
The original campaign and all three continuations are kept separately;
current decisions come from `rank6/data/decisions.json`. The new
`certificates/continuation_round3.jsonl` contains 12 general exclusions,
reducing the previous v2 release's 22 residuals to 10. Its exact replay is
`verification/round3/release_replay.json`. The first two continuation files
(7 and 18 records) and their previous verification evidence are unchanged.
The current archive is `Rank6_Categorification_M8_Revised_2026-09-29_v3.zip`.
