# Rank-8 Grothendieck rings through multiplicity 3

The rank-eight multiplicity-three continuation addresses all 3,527 supplied exact-multiplicity-three rings: 3,479 general exclusions, 14 models and 34 unresolved cases. Every recorded model admits a unitary realization. The remaining rings retain unresolved status for general complex categorification.

The rank-seven multiplicity-five continuation addresses all 5,805 supplied exact-multiplicity-five rings: 5,804 general exclusions, 1 realization and 0 unresolved cases. The classification of the supplied census is complete through multiplicity 5. The new realization R7_5_5678 is Rep(AGL(1,7)).

> **AI-generated research · independent verification pending.** Treat these
> results, proofs, code and data with caution. They have not yet been
> independently verified by human experts or formalized in Lean. Automated
> checks establish only their stated computational scope.

The authoritative decision ledger is `output/m3/ledger.json`, restored by `python3 tools/restore_data.py`. Classification is complete through multiplicity 2. Multiplicity 3 has unresolved classification records.

| Exact multiplicity | Rings | General exclusions | Unitary models | Open |
|---:|---:|---:|---:|---:|
| 1 | 96 | 48 | 48 | 0 |
| 2 | 877 | 848 | 29 | 0 |
| 3 | 3,527 | 3,479 | 14 | 34 |
| **Total** | **4,500** | **4,375** | **91** | **34** |

[Manuscript source](../../manuscripts/rank8/paper/rank8.tex) · [PDF](../../manuscripts/rank8/paper/rank8.pdf) · [Research status](../../docs/RESEARCH_STATUS.md)

From the repository root:

```bash
python3 tools/restore_data.py
python3 tools/verify_current_publication.py --historical
python3 -O tools/verify_current_publication.py --historical
```

The history option checks source-bound dependencies in isolated compatible
snapshots. These continuation checks do not replace the complete base-certificate
loops in the [full replay guide](../../evidence/prepublication_20261017/FULL_REPLAY.md).
Use normal Python for assertion-based checkers. Positive counts in an incomplete
band are lower bounds; a timeout or surviving necessary system proves no exclusion.
See [verification scope](../../docs/PREPUBLICATION_REVIEW.md).

## Multiplicity-three continuation

Run the complete current source-bound replay with Python 3.12 and a C++17 compiler:

```bash
python3 -m pip install -r supplements/rank7/requirements-m5.txt
python3 supplements/rank8/software/verify_m3_continuation.py
python3 -O supplements/rank8/software/verify_m3_continuation.py
```

Both full receipts bind all accepted decisions and explicit models to the preserved source files and proof implementation. `--metadata-only` checks those bindings without replaying mathematics. The M3 archive preserves the repository-relative dependency tree. Historical rank-eight data and decisions remain immutable; they are separate inputs to this continuation. Scoped unitary obstructions and unsuccessful searches do not establish general nonexistence.
