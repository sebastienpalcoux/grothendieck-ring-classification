# Prepublication correction · 17 October 2026

**R8_2_24 is reopened.** Its proposed general exclusion is withdrawn from the
current classification. The original argument uses unsupported decorated-phase
cancellation. Its proposed paired-diagram repair still lacks an established
oriented g-cap/crossing sign in the categorical-to-linear bridge. The conditional
8-slot calculation does not repair that missing argument.

Read the [proof-gate audit](../prepublication_20261017/r24/R24_BRIDGE_PREPUBLICATION_AUDIT.md)
and [dated manuscript errata](../../docs/PREPUBLICATION_REVIEW.md).

All results, proofs, code and data are AI-generated, not independently
human-verified and not Lean-formalized. Automated replay establishes only
its stated computational scope. Current accepted decisions remain provisional.

| Current scope | Excluded | Realized | Unresolved |
|---|---:|---:|---:|
| Rank 7 through multiplicity 4 | 4,172 | 29 | 0 |
| Rank 8 through multiplicity 2 | 895 | 77 | 1 |
| Latest 38-case continuation | 28 | 7 | 3 |

Rank eight is complete through multiplicity **1**. Its multiplicity-two
band has 847 exclusions, 29 models and one open ring; its realized count
is a lower bound **≥29**. The three general open cases are `R6_4_155`,
`R6_8_1660`, and `R8_2_24`.

## Current record and frozen history

- [35 currently accepted decisions](decisions.json) retain their original
  proof references relative to `evidence/unified_20261016/`.
- [All 38 original cases](ALL38_COVERAGE.md), [remaining IDs](remaining_ids.json),
  and [current totals](expected_totals.json) describe the corrected state.
- [Review transition](review.json) records the exact old and new R8_2_24
  records and complete-ledger preservation hashes.
- The [frozen 36-decision unified stage](../unified_20261016/README.md)
  remains unchanged as a **superseded historical snapshot**. Its historical
  claim about R8_2_24 is not a currently accepted exclusion.
- `parent_files.json` and `parent_files.zip` preserve every pre-review file
  replaced by this correction. The new verifier checks their byte identities
  before restoring an isolated historical replay copy.

## Replay

```bash
python3 tools/verify_review_20261017.py --metadata-only
python3 tools/verify_review_20261017.py --historical
python3 -O tools/verify_review_20261017.py --historical
```

The first command checks the correction, unchanged records and frozen sources.
The latter two restore the exact parent snapshot and run the **unchanged**
unified verifier and its earlier history. A historical PASS is not acceptance
of the withdrawn categorical argument. Full base checks remain separate:
[complete replay instructions](../prepublication_20261017/FULL_REPLAY.md).
The normal run is required because some historical checkers use assertions.
