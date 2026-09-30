# Unresolved rank-six rings

The current tensors and status are in `data/unresolved_tensors.json` and
`data/frontier_summary.json`. Surviving necessary data do not establish existence.

| Ring | Structural description | Exact retained reduction |
|---|---|---|
| [R6_4_155](R6_4_155/) | Generalized near-group R′(4) | One center profile of rank 52 |
| [R6_8_1660](R6_8_1660/) | Free rank-two module over Ising | One relative-center ring; 1670 center profiles |

Run `python -O software/frontier_replay.py --list` from the package root for
retained finite-profile replays. Each command has a 15-minute deadline.
The source-bound certificates retain their internal paths to preserve their
exact provenance. `--check-receipts` checks hashes and completion predicates;
it does not rerun the mathematics.

The [indicator audit](indicator_audit.md) records the tested scopes and remaining
gaps. The short structural and spin checks are:

```bash
python -O research/frontier/R6_8_1660/relative_center/verify_relative_reduction.py
python -O research/frontier/R6_8_1660/relative_center/verify_structural_cuts.py
python -O research/frontier/R6_4_155/verify_low_checks.py
python -O research/frontier/R6_8_1660/spin_profiles/verify_spin_profiles.py
```
