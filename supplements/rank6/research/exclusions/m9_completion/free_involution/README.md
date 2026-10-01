# R6_9_1060: exact general exclusion

This bundle certifies that the frozen rank-six ring `R6_9_1060` has no complex fusion categorification. It assumes no pivotal, spherical, unitary, or braided structure on a hypothetical category.

The proof combines an exact sphericalization dimension reduction with an exhaustive center-induction obstruction. The latter checks four frames and **all 32** second-indicator sign vectors per frame: **128 exact Farkas inequalities**. It does not use a Frobenius–Schur parity shortcut.

## Replay

Requires Python, SymPy, NumPy, and `g++` with C++17 support. SciPy and a numerical optimizer are not needed. Point `--source-root` at the canonical classification package containing `software/`:

```sh
python verify.py --source-root /path/to/Rank6_Categorification_M9 --report audit/normal.json
python -O verify.py --source-root /path/to/Rank6_Categorification_M9 --report audit/optimized.json
python audit_mutated_ray.py --source-root /path/to/Rank6_Categorification_M9
```

Alternatively set `RANK6_SOURCE_ROOT`, or run with the bundle beneath the canonical package root. The default searches ancestors of the bundle and current directory. There are no workspace-specific absolute paths in the bundle.

The verifier imports eight hash-pinned canonical Python files listed in `source_manifest.json`. It never writes to the canonical package. Native integer enumeration is compiled in a temporary directory and removed afterwards. Python bytecode writing is disabled.

## Artifacts

- `PROOF.txt`: the categorical and arithmetic argument, with primary references.
- `tensor.json`: frozen tensor and duality, copied from canonical `data/census.json`; verification does not depend on a residual or unresolved list.
- `certificate.json`: four frames, Galois pruning data, and 128 integer Farkas rays.
- `general_dimension_certificate.json`: exhaustive arithmetic survivors and d-number checks.
- `verify.py`: exact frame enumeration, dimension reduction, and complete ray replay.
- `gram_vectors_general.py` and `.cpp`: exact integer Gram-vector enumeration; the adapter uses temporary build storage.
- `source_manifest.json`: hashes of the canonical implementation dependencies.
- `audit/`: normal, optimized, and corrupted-ray test reports.

## Audit guarantees

Every correctness gate uses an explicit exception-based `require`; none depends on Python's `assert`. The verifier also rejects canonical dependencies containing optimization-sensitive assertion statements. It validates the frozen tensor, all characters, complete frame enumeration, every dimension candidate, all 128 indicator cases, and each exact inequality. Optimizer entry points are replaced with a function that raises if called.

The negative test replaces a complete stored ray by zeros. Both normal and optimized verification must reject it at the exact Farkas check, rather than merely rejecting metadata or a file hash.

## Indicator system reconstruction

The inherited builder's only indicator-dependent terms are the two coefficient rows for each second moment. In rank six these are rows 25–34, using zero-based indexing. The verifier builds the all-positive and all-negative endpoints, requires every other row and right-hand side to agree, and selects the relevant pair of normalized rows for each sign. Primitive row normalization is preserved because each affected row depends on just one indicator. A mixed sign case is also rebuilt directly with the canonical implementation and compared in full for every frame.

The detailed proof is separate from the finite arithmetic checker: the checker verifies its stated finite reductions and certificates, while `PROOF.txt` explains why every hypothetical categorification must satisfy them.
