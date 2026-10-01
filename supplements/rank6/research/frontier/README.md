# Unresolved rank-six rings

**Both rings remain unresolved.** The current audited research summaries are in
[`data/frontier_research_progress.json`](../../data/frontier_research_progress.json).
The classification remains 25,421 rings: 25,362 generally excluded, 57 realized,
and two unresolved; all 8,809 exact-multiplicity-nine rings are excluded.

| Ring | Current necessary reduction |
|---|---|
| [R6_4_155](R6_4_155/CURRENT_STATUS.md) | Complete unique rank-26 modular candidate; ten self-dual objects (twenty in the full rank-52 center); all stated finite checks pass |
| [R6_8_1660](R6_8_1660/CURRENT_STATUS.md) | One relative-center ring; 1669 center profiles; every indecomposable module has rank six, and three possible Morita-dual based rings remain |

The [new research](new_research/README.md) contains exact replays and independent
audits. Complete necessary modular data, based modules and algebra supports do
not supply categorical constructions or associators.

## Replay and historical evidence

Run from the package root:

```bash
python research/frontier/new_research/replay.py
python -O software/frontier_replay.py --check-receipts
```

The first command replays the new research. The second audits retained historical
source hashes and completion predicates; it does not rerun the old mathematics.
Use `python -O software/frontier_replay.py --list` to list the historical finite
replays and their 15-minute deadlines.

[`data/frontier_summary.json`](../../data/frontier_summary.json), `coverage.json`,
and the original per-ring `README.md` files are **frozen historical-stage evidence**.
Their earlier-stage counts and partial-data descriptions are preserved byte for
byte because the retained receipts bind their hashes. They are superseded as
current summaries by the status pages above. This also applies to R155's dated
`MODELS_IDENTIFICATION.md`: the new order-32 near-group constructions and their
condensation obstruction are described in the new research.

The [indicator audit](indicator_audit.md) states every finite scope and remaining
gap. The [source-binding adapter](m9_adapter/README.md) explains preservation of
the historical evidence; the separate `m9/inputs.json` and `m9/coverage.json` have
empty case lists, matching the final ledger.
