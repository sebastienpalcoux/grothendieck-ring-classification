# Rank-six categorification through multiplicity nine

**25,421 rings: 25,351 excluded, 57 realized, 13 unresolved.**

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
| 9 | 8,809 | 8,798 | 0 | 11 |
| **Total** | **25,421** | **25,351** | **57** | **13** |

The models comprise 56 unitary realizations and one spherical realization whose ring has no pseudo-unitary categorification. Every allocated exclusion applies to general complex fusion categories. The completed exact-multiplicity bands are 1, 2, 3, 5, 6, 7.

The extension adds 8,809 rings of exact multiplicity nine, with 8,798 exact exclusions and 11 unresolved cases. All 16,612 earlier representatives, identifiers and decisions are preserved. The [new campaign](verification/m9/) records the actual criterion order, discovery budgets and independent exact certificate replays. Timeouts and surviving necessary systems establish neither exclusion nor existence.

## Remaining rings

- `R6_4_155`: One rank-52 center profile remains, with forced twists of exponent 24 and four duality choices. This is not yet complete modular data or a model.
- `R6_8_1660`: One relative-center based ring and 1670 labelled center profiles remain. A tensor involution and Vafa/indicator constraints remove 57 more profiles.
- `R6_9_529`, `R6_9_1060`, `R6_9_2455`, `R6_9_8785`: Recorded multiplicity-nine searches leave this ring unresolved. No additional structural frontier reduction is asserted.
- `R6_9_3748`: Braided categorifications are ruled out by the rank-three subcategory and centralizer obstruction. General, pivotal, spherical, pseudo-unitary and unitary existence remain unknown.
- `R6_9_7018`, `R6_9_7741`, `R6_9_7742`, `R6_9_8099`, `R6_9_8101`, `R6_9_8200`: Pivotal, spherical, pseudo-unitary and unitary categorifications are ruled out by a retained exact certificate. General existence remains unknown.

The [frontier index](research/frontier/README.md) gives the current evidence. The [model catalogue](data/model_catalog.csv) identifies actual categorical constructions and all 216 tensor coefficients, including the three conformal-embedding models.

## Verification

```bash
python -m pip install -r requirements.txt
python check_manifest.py
python -O software/replay_m9.py --jobs 2
python -O software/replay_m9_structure.py
python -O software/conformal_models.py --verify
python -O software/release_consistency.py
python -O software/frontier_replay.py --check-receipts
```

The new certificate replay disables numerical optimizers. Historical proofs retain their original exact verification evidence; a receipt audit checks source hashes and predicates and does not rerun the mathematics. For a fresh full-ledger check, use `python -O verify.py --jobs 2 --out verification/current/full_recheck.jsonl`. The verification guide distinguishes these scopes and gives the remaining replay commands.

`data/decisions.json` is authoritative. Regenerate exports with `python software/release.py`, `python software/model_catalog.py`, `python software/build_paper_tables.py`, `python software/build_readme.py` and `python build_papers.py`. Release generation replays historical continuation certificates by default; `--retain-historical-replay` instead checks their frozen source-bound receipt.

The census is pinned to [Fusion Ring Census revision 2a340871242879665fa7ba2b01fa15b8bdeaada3](https://github.com/sebastienpalcoux/fusion-ring-census/tree/2a340871242879665fa7ba2b01fa15b8bdeaada3). Enumeration completeness comes from that source; the import independently checks tensor validity, distinctness and exact correspondence. The [OEIS proposal](oeis/proposal.txt) counts all fusion rings, independently of categorifiability.
