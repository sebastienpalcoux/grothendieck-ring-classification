# Classification software

These directories expose the exact exclusion engines and verification entry
points accompanying the rank-four, rank-five and rank-six manuscripts. The
rank-specific files here are browsable source; run them from their **complete
research release** after extracting its census data, model catalogs and
certificate ledgers. Copying just `software/` and `verify.py` does not create a
self-contained verification run.

| Rank | Source | Required full input |
|---:|---|---|
| 4 | [`rank4/software/`](rank4/software/) and [`verify.py`](rank4/verify.py) | Rank-four source release, including 75.8 MB compressed classification ledger |
| 5 | [`rank5/software/`](rank5/software/) and [`verify.py`](rank5/verify.py) | Rank-five source release, including its decisions and exclusion certificates |
| 6 | [`rank6/software/`](rank6/software/) and [`verify.py`](rank6/verify.py) | Rank-six source release, including decisions, model data and certificates |

The public [fusion-ring-census](https://github.com/sebastienpalcoux/fusion-ring-census)
continues to own the raw tensor census and enumeration code. See the
[verification guide](../docs/VERIFY.md) for the crosswalk and local checks.
Any copied licensed census code retains its license and notice in the
rank-specific software directory.
