# Classification software

These directories expose the exact exclusion engines and verification entry
points accompanying the rank-specific manuscripts. Restore the compressed
repository datasets with `python3 tools/restore_data.py` before running the
checks. Rank six includes the complete revised research release, including
its census data, model catalogs, accepted exclusion certificates and conformal constructions, exact proof sources and
verification records. Other rank directories describe any full source-release
inputs needed by their verifiers. Copying just `software/` and `verify.py`
does not create a self-contained verification run.

| Rank | Source | Required full input |
|---:|---|---|
| 4 | [`rank4/software/`](rank4/software/) and [`verify.py`](rank4/verify.py) | Rank-four source release, including 75.8 MB compressed classification ledger |
| 5 | [`rank5/software/`](rank5/software/) and [`verify.py`](rank5/verify.py) | Rank-five source release, including its decisions and exclusion certificates |
| 6 | [`rank6/software/`](rank6/software/) and [`verify.py`](rank6/verify.py) | Complete release; 16,553 excluded, 57 realized, 2 unresolved; complete through 3 and exact bands 1, 2, 3, 5, 6, 7 |

The public [fusion-ring-census](https://github.com/sebastienpalcoux/fusion-ring-census)
continues to own the raw tensor census and enumeration code. See the
[verification guide](../docs/VERIFY.md) for the crosswalk and local checks.
Any copied licensed census code retains its license and notice in the
rank-specific software directory.


For the rank-six update, start with its [README](rank6/README.md),
[models](rank6/data/model_catalog.csv) and [current frontier](rank6/research/frontier/README.md).
The authoritative ledger is `rank6/data/decisions.json`. The archive is
`Rank6_Categorification_M8_Revised_2026-09-30_v6.zip`. Source-bound certificates retain their internal paths.
