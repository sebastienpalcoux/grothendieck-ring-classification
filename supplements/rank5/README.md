# Rank-five Grothendieck rings through multiplicity twenty: two general residuals at eighteen

The paper classifies complex-categorifiable rank-five fusion rings through multiplicity 17. Of the 23,413 rings in the pinned [fusion-ring census](https://github.com/sebastienpalcoux/fusion-ring-census/tree/b86eb6dc6eeeafe5fc5f6906d7b074e0322e9726), exactly 17 are categorifiable, each with a unitary model. Of the 5,080 rings at multiplicity 18, exactly two still lack a general exclusion by the criteria in this release; both are excluded pivotally and spherically. A failed or timed-out search is never counted as an exclusion.

At exact multiplicities 19 and 20, all 5,640 and 6,866 census rings, respectively, have verified general noncategorifiability certificates. Thus the 40,999 rings through 20 split into 17 unitary models, 40,980 general exclusions and two general residuals at multiplicity 18. Pivotal, spherical, pseudo-unitary and unitary existence is fully classified through 20. The pinned census tensors through 18 and this release's archival tensors agree **up to based-ring isomorphism**, verified for all 28,493 classes by all 24 unit-fixing permutations. Their labels do not generally agree: identify a ring by its full tensor and a basis permutation, rather than importing a numeric label from one release into another. The later 12,506 certificates address the pinned tensors directly in their recorded order.

## Contents

- `papers/manuscript.tex` and `.pdf`: research manuscript; `papers/verification_guide.tex` and `.pdf`: reproducibility guide.
- `data/decisions_all.json`, `.csv`: all 40,999 five-status decisions, including repository indices where the pinned records are addressed directly. `data/decisions.json`, `.csv` retain the archived labels through 18.
- `certificates/exclusions.json`: exact general exclusion certificates, addressed by the **labeled tensor's** SHA-256 fingerprint, not by an isomorphism-invariant hash.
- `data/frontier.json`: complete data on the two general residuals at multiplicity 18.
- `data/extension19_20/full.jsonl`: complete pinned m19/20 tensors and 12,506 exactly checked general exclusion certificates.
- `software/`: tensor criteria, proof checkers and positive constructions.
- `verification/`: recorded full verification results and regression controls.

The authoritative count source is the pinned census commit above. Copies of `results/rank5/counts.csv` and `results/rank5/tables.txt.gz` are bundled under `data/pinned_repository/rank5/`; `data/classification_tensors.json` retains the labeled basis choices needed to check the classification witnesses. `verify.py` checks the full isomorphism-class crosswalk before any exclusion certificate. There is no second census computation.

The [Grothendieck-ring classification repository](https://github.com/sebastienpalcoux/grothendieck-ring-classification) hosts the manuscript and its checked classification certificates. It is currently private.

## Reproduce the finite classifications

Use Python 3.11 or later, the packages in `requirements.txt`, and a C++17 compiler with OpenMP and `__int128`. From this directory:

```sh
python -m pip install -r requirements.txt
python verify.py --jobs 2
python software/verify_extension.py --jobs 2
python -O verify.py --jobs 2
python -O software/verify_extension.py --jobs 2
python software/export_tables.py
python build_pdfs.py
```

The first checker matches the pinned census tensors through 18, reconstructs all 28,474 general exclusions, verifies 17 exact tensor matches to constructed unitary models, and checks both spherical frontier certificates. The extension checker checks every pinned tensor and all 12,506 general exclusions at exact multiplicities 19 and 20. They reject incomplete branches, timeouts, inexact floating-point rays and unsupported cases. The `-O` run checks that no proof condition relies on a removable Python `assert`.

To investigate a residual or another tensor without consulting the decision ledger:

```sh
python software/discover.py --multiplicity 18 --index 5073 --height 6 --seconds 120 --output verification/retry.jsonl
python software/discover.py --tensor new_tensor.json --height 6 --seconds 120 --output verification/new.jsonl
```

The first index is the **local archival ordinal**, stored under `local_index`; for cross-repository work use the complete tensor instead. The discovery process proposes witnesses; the exact verifier accepts or rejects them.

`papers/allocation_table.tex` and `papers/stage_table.tex` are regenerated from the verified 40,999-ring ledger. Their certificate order follows the executable decision order. The last genuinely new theoretical criterion family first used in this bounded record occurs at multiplicity 8; the last new combined certificate type first occurs at 12. No new type is needed through multiplicity 20, although two general residuals remain at 18; these bounded observations do not claim an unbounded classification.
