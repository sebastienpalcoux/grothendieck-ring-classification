# Classification software

> **AI-generated research — independent verification pending.** The results, proofs, code and data have not yet been independently verified by human experts or formalized in Lean. Read the [prepublication review and dated corrections](../docs/PREPUBLICATION_REVIEW.md) alongside these materials.

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
| 6 | [`rank6/software/`](rank6/software/) and [`verify.py`](rank6/verify.py) | Complete release; 25,362 excluded, 57 realized, 2 unresolved; complete through 3 and exact bands 1, 2, 3, 5, 6, 7, 9 |
| 7 | [`rank7/`](rank7/) | Complete census through 4; 4,172 generally excluded, 29 realized, 0 generally unresolved |
| 8 | [`rank8/`](rank8/) | Complete census through 2; 895 generally excluded, 77 realized, 1 generally unresolved |

The public [fusion-ring-census](https://github.com/sebastienpalcoux/fusion-ring-census)
continues to own the raw tensor census and enumeration code. See the
[verification guide](../docs/VERIFY.md) for the crosswalk and local checks.
Any copied licensed census code retains its license and notice in the
rank-specific software directory.


For the rank-six update, start with its [README](rank6/README.md),
[models](rank6/data/model_catalog.csv) and [current frontier](rank6/research/frontier/README.md).
The authoritative ledger is `rank6/data/decisions.json`. The archive is
`Rank6_Categorification_M9_Frontier_2026-10-01.zip`. Source-bound certificates retain their internal paths.

The [17 October prepublication correction](../evidence/review_20261017/README.md) reopens **R8_2_24** because its categorical-to-linear bridge is unproved. The latest 38-case continuation retains **35 accepted decisions**: 28 proposed general exclusions and 7 unitary constructions. Three general questions remain open: R6_4_155, R6_8_1660 and R8_2_24. Together with earlier residual stages, 139 decisions remain accepted (119 exclusions and 20 constructions), subject to independent review. The [frozen 36-decision snapshot](../evidence/unified_20261016/README.md) and manuscripts remain available with dated errata and exact historical replay; their R8_2_24 exclusion is superseded. From the repository root, run `python3 tools/verify_review_20261017.py --historical` and its optimized-Python counterpart. The [current review and errata](../docs/PREPUBLICATION_REVIEW.md) distinguish these stage replays from full base-release checks; older bundled READMEs describe their frozen historical stages.
