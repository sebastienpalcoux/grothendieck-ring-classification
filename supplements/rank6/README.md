# Rank-six categorification through multiplicity eight

**16,612 rings: 16,553 excluded, 57 realized, 2 unresolved.**

[Manuscript](papers/manuscript.pdf) · [Verification guide](papers/verification_guide.pdf) · [Decision ledger](data/decisions.csv) · [Models](data/model_catalog.csv)

| Exact multiplicity | Rings | Excluded | Models | Unresolved |
|---:|---:|---:|---:|---:|
| 1 | 39 | 18 | 21 | 0 |
| 2 | 154 | 132 | 22 | 0 |
| 3 | 384 | 381 | 3 | 0 |
| 4 | 872 | 866 | 5 | 1 |
| 5 | 1,582 | 1,581 | 1 | 0 |
| 6 | 2,768 | 2,765 | 3 | 0 |
| 7 | 3,814 | 3,812 | 2 | 0 |
| 8 | 6,999 | 6,998 | 0 | 1 |
| **Total** | **16,612** | **16,553** | **57** | **2** |

The models comprise 56 unitary realizations and one spherical realization whose ring has no pseudo-unitary categorification. Every exclusion applies to general complex fusion categories. Classification is complete through multiplicity three and at the exact multiplicities 5, 6 and 7.

## Conformal-embedding models

| Ring | Construction: neutral module category |
|---|---|
| `R6_4_22` | `(B2)_7 ⊂ (D7)_1` |
| `R6_4_91` | `(C3)_4 ⊂ (B10)_1` |
| `R6_4_629` | `(B2)_12 ⊂ (E8)_1` |

Actual unitary conformal-embedding module categories supply associators. The [source and exact arithmetic](research/structural_models/) identify all 216 coefficients of each fusion tensor. These constructors are integrated into the classification pipeline.

## Remaining rings

The [current frontier](research/frontier/README.md) consists of `R6_4_155` and `R6_8_1660`. The generalized near-group ring `R6_4_155` has no braided Morita representative. The ring `R6_8_1660`, free of rank two over its Ising fusion subring, has one possible relative-center based ring. Neither result decides existence.

`R6_5_1204` is excluded by [center rotation integrality](research/exclusions/R6_5_1204/structural_note.md): 72 structural contradictions and 99 exact integer-bound certificates cover every possible induction profile.

## Verification

```bash
python -m pip install -r requirements.txt
python check_manifest.py
python -O software/conformal_models.py --verify
python -O software/release_consistency.py
python -O research/exclusions/R6_5_1204/verify_exclusion.py
python -O software/frontier_replay.py --check-receipts
python -O software/frontier_replay.py --list
python build_papers.py
```

The conformal-model command freshly reconstructs the three tensors. The frontier receipt audit checks frozen hashes and completion predicates; select a ring to replay its mathematical reduction, for example `python -O software/frontier_replay.py --select R6_4_155`. Each command has a 15-minute deadline.

For all exclusion certificates, run `python -O verify.py --jobs 2 --out verification/current/full_recheck.jsonl`. The stored original negative verification is retained; this release freshly verifies the new exclusion and retains the earlier complete evidence.

`data/decisions.json` is authoritative. Counts, tables, the model catalogue and unresolved tensors are derived from the registered constructions and allocated certificates. Rebuild them with `python software/release.py`, `python software/model_catalog.py` and `python software/build_paper_tables.py`. The first command replays all continuation certificates.

The census is imported from the pinned [Fusion Ring Census](https://github.com/sebastienpalcoux/fusion-ring-census/tree/b86eb6dc6eeeafe5fc5f6906d7b074e0322e9726); source data and exact certificates are bundled.
