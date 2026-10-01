# Rank-six categorification through multiplicity nine

**25,421 rings: 25,362 excluded, 57 realized, 2 unresolved.**

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
| 9 | 8,809 | 8,809 | 0 | 0 |
| **Total** | **25,421** | **25,362** | **57** | **2** |

The models comprise 56 unitary realizations and one spherical realization whose ring has no pseudo-unitary categorification. Every allocated exclusion applies to general complex fusion categories. The completed exact-multiplicity bands are 1, 2, 3, 5, 6, 7, 9.

All 8,809 rings of exact multiplicity nine are excluded for general complex fusion categories. The [completion proofs](research/exclusions/m9_completion/README.md) resolve the final eleven cases with standalone exact verifiers and frozen tensor inputs. All 16,612 earlier representatives, identifiers and decisions are preserved. The [new campaign](verification/m9/) records the actual criterion order, discovery budgets and independent exact certificate replays. Timeouts and surviving necessary systems establish neither exclusion nor existence.

## Remaining rings

- `R6_4_155`: The unique rank-26 semion-centralizer modular candidate is completely reconstructed, with nonnegative integral Verlinde coefficients (maximum 9), ten self-dual objects, and all stated finite Vafa and indicator checks passing. The rank-52 center would have twenty self-dual objects. No categorification is known.
- `R6_8_1660`: One relative-center based ring and 1669 labelled center profiles remain, in branches 163, 753, 753. Every indecomposable module category has six simples; exact Morita and indicator reductions leave three possible dual based rings. No categorification is known.

The [frontier index](research/frontier/README.md) gives the current evidence and distinguishes it from frozen historical stages. The [model catalogue](data/model_catalog.csv) identifies actual categorical constructions and all 216 tensor coefficients, including the three conformal-embedding models.

## Verification

```bash
python -m pip install -r requirements.txt
python check_manifest.py
python -O software/replay_m9.py --jobs 2
python -O software/replay_m9_structure.py
python -O software/replay_m9_completion.py
python -O software/m9_completion_controls.py
python -O software/conformal_models.py --verify
python -O software/release_consistency.py
python -O software/frontier_replay.py --check-receipts
python research/frontier/new_research/replay.py
```

The new certificate replay disables numerical optimizers. Historical proofs retain their original exact verification evidence; a receipt audit checks source hashes and predicates and does not rerun the mathematics. For a fresh full-ledger check, use `python -O verify.py --jobs 2 --out verification/current/full_recheck.jsonl`. The verification guide distinguishes these scopes and gives the remaining replay commands.

`data/decisions.json` is authoritative. Regenerate exports with `python software/release.py`, `python software/model_catalog.py`, `python software/build_paper_tables.py`, `python software/build_readme.py` and `python build_papers.py`. Release generation replays historical continuation certificates by default; `--retain-historical-replay` instead checks their frozen source-bound receipt.

The census is pinned to [Fusion Ring Census revision 2a340871242879665fa7ba2b01fa15b8bdeaada3](https://github.com/sebastienpalcoux/fusion-ring-census/tree/2a340871242879665fa7ba2b01fa15b8bdeaada3). Enumeration completeness comes from that source; the import independently checks tensor validity, distinctness and exact correspondence. The [OEIS proposal](oeis/proposal.txt) counts all fusion rings, independently of categorifiability.
