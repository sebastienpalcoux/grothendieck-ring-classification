# Rank-7 Grothendieck rings through multiplicity 5

The rank-eight multiplicity-three continuation addresses all 3,527 supplied exact-multiplicity-three rings: 3,506 general exclusions, 15 models and 6 unresolved cases. Every recorded model admits a unitary realization. The remaining rings retain unresolved status for general complex categorification.

The rank-seven multiplicity-five continuation addresses all 5,805 supplied exact-multiplicity-five rings: 5,804 general exclusions, 1 realization and 0 unresolved cases. The classification of the supplied census is complete through multiplicity 5. The new realization R7_5_5678 is Rep(AGL(1,7)).

> **AI-generated research · independent verification pending.** Treat these
> results, proofs, code and data with caution. They have not yet been
> independently verified by human experts or formalized in Lean. Automated
> checks establish only their stated computational scope.

The authoritative decision ledger is `output/rank7_ledger.json`, restored by `python3 tools/restore_data.py`. Classification is complete through multiplicity 5.

| Exact multiplicity | Rings | General exclusions | Unitary models | Open |
|---:|---:|---:|---:|---:|
| 1 | 43 | 30 | 13 | 0 |
| 2 | 319 | 309 | 10 | 0 |
| 3 | 1,059 | 1,057 | 2 | 0 |
| 4 | 2,780 | 2,776 | 4 | 0 |
| 5 | 5,805 | 5,804 | 1 | 0 |
| **Total** | **10,006** | **9,976** | **30** | **0** |

[Manuscript source](../../manuscripts/rank7/papers/manuscript.tex) · [PDF](../../manuscripts/rank7/papers/manuscript.pdf) · [Research status](../../docs/RESEARCH_STATUS.md)

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

## Multiplicity-five continuation

The current continuation is replayed with Python 3.12 and a C++17 compiler:

```bash
python3 -m pip install -r supplements/rank7/requirements-m5.txt
python3 supplements/rank7/software/verify_m5.py
python3 -O supplements/rank7/software/verify_m5.py
```

Use `--metadata-only` only for source and partition checks; it does not replay mathematical certificates.
The older top-level `analyze.py` and `verify.py` retain their M4 source commitments; run them in the preserved M4 archive, not against the extended source file.
The M5 release archive uses repository-relative directories and includes the frozen M4 archive. NetworkX is required by the complete Morita-dual enumeration, and python-flint by the exact all-word integer-order checks; SciPy is optional for discovery. The assertion-based R4982 components run in an isolated unoptimized child in both aggregate modes, preserving all their checks.
