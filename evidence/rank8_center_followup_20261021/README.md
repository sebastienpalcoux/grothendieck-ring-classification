# Separately verified necessary-condition addendum

This package strengthens necessary central data for two unresolved rank-eight
rings. It does not change the frozen inventory of 25 further exclusions and
nine residual rings, and it supplies no categorical model.

| Case | Exact new outcome |
|---|---|
| R8_3_721 | Two of four central Gram patterns are excluded. The rank-16 pattern has one necessary low-action tuple; the rank-22 pattern has 46 labelled tuples, three up to equal-type permutations. |
| R8_3_1154 | Of 1,238 cubic-surviving patterns, 892 fail coordinate norm bounds and 54 more fail exact coordinate propagation. The remaining 292 are not certified feasible. The old eight height-six exclusions lie among the 892, so 938 pattern exclusions are new relative to that test. |

The proof notes and TeX sections distinguish exact pattern exclusions,
necessary-data witnesses, and unresolved categorical constructions. All
mathematical scripts are read-only unless a reviewer is explicitly given
`--write`; the aggregate never passes that option.

Replay from the repository root:

```sh
python evidence/rank8_center_followup_20261021/verify.py --root . --output evidence/rank8_center_followup_20261021/publication/replay_normal.json
python -O evidence/rank8_center_followup_20261021/verify.py --root . --output evidence/rank8_center_followup_20261021/publication/replay_optimized.json
python evidence/rank8_center_followup_20261021/verify.py --root . --metadata-only
```

Full replay invokes every listed checker sequentially, using the same Python
optimization mode. Metadata verification requires both complete full receipts
under this package's `publication/` directory and the exact current manifest.
The verifier writes only a path explicitly supplied with `--output`. It rejects
source-file overwrites, metadata writes over canonical full receipts, and a
canonical receipt path for the wrong optimization lane.

`source_manifest.json` uses schema 1:

- `package_files`: package-relative file paths and SHA-256 hashes, including
  the dispatcher, all final scripts, primary receipts, and proof notes.
- `baseline_files`: all 1,445 frozen main-manifest inputs and the main manifest
  itself, with repository-relative paths and SHA-256 hashes.
- `baseline_source_manifest`: the repository-relative frozen main manifest;
  that path must also occur in `baseline_files`.
- `checks`: an ordered list of objects with `script`, `kind`, and, when
  applicable, `receipt`. Kinds are `json_receipt` (recomputed JSON must equal
  its primary receipt), `internal_replay` (independent verifier checks its
  own saved receipt), and `quartic_summary` (the small common control).

Full reports bind the manifest, the frozen baseline manifest, each child
stdout hash, and each stored primary receipt hash. They contain no external
absolute paths. Full receipts and the manifest itself are excluded from the
manifest's `package_files` to avoid hash cycles. Probe scripts and duplicate
optimized primary receipts are intentionally omitted.
