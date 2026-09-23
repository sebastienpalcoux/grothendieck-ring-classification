# Rank-four classification: revised publication bundle

This bundle contains the revised 28-page bounded classification, the 25-page unrestricted companion, the 7-page verification guide, all their LaTeX sources, the exact rank-four census snapshot through multiplicity 128, and the relevant verifier source. It does **not** duplicate the 75,825,461-byte compressed certificate stream in the original `FusionFrontier.tar.xz` attachment.

## Results and provenance

The finite paper classifies the 889,530 rank-four based fusion rings with maximum structure constant at most 128: exactly fifteen admit a complex fusion categorification, and every positive ring has a unitary model. Its input is the rank-four dataset in [`fusion-ring-census`](https://github.com/sebastienpalcoux/fusion-ring-census), pinned to commit `7f1b36e74df53a8a1cf8597db45d261e408d61b2`. The exact 128 count terms in `results/rank4/counts.csv` at that commit sum to 889,530; `data/census_128_manifest.json` records the matching count and digest. Its completeness argument is in that repository. The classification and census have distinct proofs and data paths.

The exclusion table reproduces the **archived** verified certificate allocation, ordered by the revised dispatcher. The last newly used mathematical criterion family appears at multiplicity 18; multiplicities 19 through 128 use the existing families. This is a statement about this certificate allocation, not a minimality theorem. A signed cyclotomic check first succeeds at multiplicity 95 using the cyclotomicity theorem that was already applied at multiplicity 9. The legacy certificate tag `involution_propagation_42` is checked by the general residual-involution criterion, with no exact-tensor exception in generation or verification.

## Rebuild the PDFs

From this directory, run:

```bash
python3 render_report.py
python3 build_pdfs.py
```

These commands use the included small certificate summaries and LaTeX source. They do not need the large certificate stream. The resulting PDFs are in `papers/`. The PDF build performs three passes and fails on unresolved references or overfull boxes.

## Restore and replay the archived certificate

The large stream is retained in the user-supplied original archive. Restore it under `certificates/` without substituting an incomplete extraction:

```bash
mkdir -p certificates
TAR_PATH=/path/to/FusionFrontier.tar.xz
tar -xOJf "$TAR_PATH" 'Rank4/Rank4_Dong_Palcoux_Through128/Rank4_Through128/certificates/classification.jsonl.gz' > certificates/classification.jsonl.gz
gzip -t certificates/classification.jsonl.gz
sha256sum certificates/classification.jsonl.gz
python3 -m pip install -r requirements.txt
python3 verify.py --workers 4
```

The expected SHA-256 of the compressed certificate is `969a2a5a84b794a3da1d9cd3978f92324d631760f503f5d208011923a723920f`. Reject a stream that does not match this value. Full verification was carried out for the archived source before this editorial and dispatcher revision; this bundle was rebuilt and the general residual-involution recognizer was tested on all 24 basis permutations of four affected application models, with eight corrupted witnesses rejected. A new complete 889,530-record verifier replay has **not** been carried out in this revision environment, which lacks `python-flint`. The PDF sources compile independently of that dependency.

## Contents

- `papers/finite.tex`, `papers/companion.tex`, and `papers/verification_guide.tex`, their included sections and PDFs.
- `data/`: pinned tensor parameters, model tensors, signed-cover data and manifests. The compressed parameter file matches the manifest SHA-256 `0c3ab657ebfa9c78719e909a7d5857769e0bf791564a67971350237e752aaf6d`.
- `software/`, `companion_software/`, and the root Python scripts: classification and verification code, including full-tensor integrity and uniqueness checks against the pinned source.
- `verification/`: small archived reports needed to regenerate the displayed tables; `verification/ledger.csv.gz` and the large certificate stream are available in the original archive.
- `CHANGES.md`: detailed revision rationale and verification record.

This package omits the stale nested ZIP, historical authors file, old acknowledgments, and duplicate large verification files.
