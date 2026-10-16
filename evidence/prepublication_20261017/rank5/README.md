# Rank-five classification: complete replay

This package supplies a fresh, fully replayable check of the rank-five classification through multiplicity **20**.

| Multiplicity | Pinned rings | Unitary model matches | General exclusions |
| --- | ---: | ---: | ---: |
| 1–18 | 28,493 | 17 | 28,476 |
| 19 | 5,640 | 0 | 5,640 |
| 20 | 6,866 | 0 | 6,866 |
| **Total** | **40,999** | **17** | **40,982** |

**Please treat these results and data with caution. The arguments, code, data processing, and audit were generated or revised with AI assistance. They have not been independently verified by a human expert or formalized in Lean. Passing these checks verifies the encoded exact arithmetic and tensor coverage; it does not constitute independent verification of the mathematical theorems.**

The two former multiplicity-18 residuals are checked by composing the existing inert-prime parity criterion with their original spherical-character witnesses. Every other tensor receives an exact model match or an exact general exclusion certificate. No result is asserted beyond multiplicity 20.

## Run the checks

Use Python 3.12, a C++17-capable `g++` compiler, and the versions in the packaged `requirements.txt`: SymPy 1.14.0, NumPy 2.3.5, and SciPy 1.17.0. From the repository root:

```sh
python evidence/prepublication_20261017/rank5/replay.py --check-package
python evidence/prepublication_20261017/rank5/replay.py --jobs 2
python -O evidence/prepublication_20261017/rank5/replay.py --jobs 2
```

The first command checks the archive, every extracted file, and agreement with the repository's published rank-five counts. The next two commands replay all **40,982** exclusion certificates, all **17** model matches, the complete pinned tensor census, and the secondary controls. `-O` is supported because proof conditions use explicit exceptions. Fresh receipts and decision ledgers are written to `rank5-replay-output/`; use `--output-dir PATH` to choose another location.

The [complete package](rank5_current_replay.zip) also works after extraction: enter `rank5_current_replay/` and run `python evidence/prepublication_20261017/rank5/verify_current.py --jobs 2` (and its `python -O` counterpart). All required tensor/certificate inputs are included. Exact replay does not run numerical linear programming; numerical discovery only proposed rational certificates that replay checks exactly.

## Provenance and limits

The pinned census is `fusion-ring-census` commit `b86eb6dc6eeeafe5fc5f6906d7b074e0322e9726`. Its compressed rank-five table has SHA-256 `4542c0871498337ef38ce3903407933289699a5ff06c85ad0f6c2bd57da823fb`.

The old complete release archive and its final `decisions_all.json` were not recovered during this audit. The older ledger digest `9261917451d469ece9929a1756f505924cf84adf34e79a0d2e6f68fed43f55cf` remains a **historical reference**, not a verified identity for the reconstructed ledger. This package reconstructs the complete decisions from recovered, checksummed source archives and the published proof modules; it records the actual digest of the new ledger separately. Every multiplicity-band result is checked against the currently published classification.

The original 28,474 prefix exclusion certificates and two spherical witnesses are preserved. The two inert-parity composites are derived from the full tensors. The 12,506 multiplicity-19/20 certificates are regenerated from the exact pinned tensors. The 25 published software files match their Git blob hashes; the new entry point handles the previously missing inert-parity dispatch without changing those archived modules.

The ZIP contains the complete checker, source modules, tensor/certificate inputs, reconstructed decision ledger, normal and optimized replay receipts, and reconstruction provenance. [package.json](package.json) lists every member's size and SHA-256 digest. The checker's six new negative controls reject corrupted inert-field hypotheses, missing residue characters, and missing spherical-character witnesses. An independent AI audit of the orchestration found no coverage or dispatch gap; no human review is claimed.

## Fresh replay receipts

Both [normal](current_normal.json) and [optimized](current_optimized.json) full replays passed, with byte-identical reconstructed decision ledgers. The fresh ledger SHA-256 is `12886636134e0500a403ae1b635f5b901612d64b203dad1e1fdf94b0da2c31f1`.

The packaged proof sources and input files were rehashed against those receipts before packaging. [Reconstruction provenance](reconstruction.json) records the recovered sources, exact transformations, and the unavailable historical archive/ledger limitation.
