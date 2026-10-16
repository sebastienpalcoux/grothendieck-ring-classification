# R6_4_446: backend ordering diagnosis and completed replay

This append-only packet preserves the initial failure and documents a successful replay of the **complete, unchanged general certificate**. It does not change a classification decision or weaken a proof condition. This is AI-generated computational review, not independent human verification or Lean formalization.

## Completed result

The original `supplements/rank6/software/check.py:verify` returned normally on the complete R6_4_446 tensor and its original `oriented_signed` certificate with `SYMPY_GROUND_TYPES=python`, SymPy 1.14.0 and Python 3.12.14. It checked all **128 signed-spherical Farkas cases and the subsequent oriented-signed conditions**, taking **97.053 seconds**. The diagnostic wrapper counted calls while always invoking the original exact inequality checker; it bypassed no condition.

- `full_replay_receipt.json` gives the completed full-ring scope and commitments.
- `full_python_replay.log` is the unmodified raw successful output.
- `original_audit_entrypoint.py.txt` preserves the exact original diagnostic entry point, including its audit-only local paths. It is provenance, not the portable public command.
- `commitments.json` binds the exact full census and decision-ledger files, selected tensor and certificate, and 139 unchanged original source files. The audited snapshot and canonical repository were compared byte for byte before packaging. These bindings were appended to the completed run; no new full run is implied by packaging.
- `initial_full_replay_failure.json`, `initial_flint_diagnostic.log` and `initial_failure_detail.json` retain the failure.

Canonical JSON object hashes use UTF-8, sorted keys, compact separators and **no trailing newline**. The tensor hash is `9057b532ce8fb147c79d4e9f75600be72f0ce87d94c2beea0c183aa5b2f54b48`; the full certificate hash is `9ef3acefe6f08c224b576623266a20bf9812ce7cc540df767894cc74881db34c`.

## Why the initial check failed

`Spectrum.balance` in `spectral_induction.py` sorts tuples of algebraic numbers by their string representations. SymPy's Python rational backend renders coefficients as `MPQ(...)`, whereas its flint backend renders rational literals. That changes the order of the Galois-balance equations. The historical Farkas vector stores row coordinates without stable equation identifiers, so reusing it with the other backend combines different rows.

The first failure is branch 85, case 16 (zero-based), labelling `[5,2,0,1,3,4]`, indicators `[1,-1,-1,-1,-1]`. The integer system is 419 by 1,237. With the untransported stored vector, the flint reconstruction has two negative coefficients, at columns 945 and 987, both `-36864`. The right side is `-941616`, as stored.

The direct system agrees with the cached indicator system. An independent reference Gram enumeration gives the same failed system as the native enumeration. Thus neither indicator interpolation nor a stale native Gram binary causes this failure.

## Exact equivalence proof

`system_python.json.gz` and `system_flint.json.gz` contain the independently reconstructed full integer systems, right sides, original vector and column inventories. `row_equivalence.json` gives a complete row bijection. It moves 210 rows and changes no signs. Every row, including its right side, is checked exactly. High-column inventories and spectrum metadata are identical.

The original vector passes in the Python ordering: `min(A^T y)=0`, `b^T y=-941616`. Transporting this same vector through the proved permutation makes the flint system pass with those identical values. No newly discovered inequality is needed.

From the repository root, the following small standard-library check verifies the compressed inputs, complete permutation and both integer inequalities:

```bash
python evidence/prepublication_20261017/rank6/r446_backend/compare_systems.py
```

This comparison is deliberately scoped to the first failing system. The separately retained full replay receipt covers the complete ring certificate.

## Portable optional replay

The full completed replay can be repeated without changing any frozen source or ledger:

```bash
python evidence/prepublication_20261017/rank6/r446_backend/replay_r446.py \
  --output /tmp/r446_fresh_receipt.json
```

The wrapper explicitly sets `SYMPY_GROUND_TYPES=python` **before any SymPy import**, verifies all input/source commitments, calls the original complete general verifier and checks the 128-case count. Its new receipt is distinct from the retained historical audit receipt. It does not edit a decision.

To regenerate the two diagnostic systems rather than trust the compressed copies:

```bash
SYMPY_GROUND_TYPES=python python \
  evidence/prepublication_20261017/rank6/r446_backend/reconstruct_first_system.py \
  --output /tmp/r446_python.json.gz
SYMPY_GROUND_TYPES=flint python \
  evidence/prepublication_20261017/rank6/r446_backend/reconstruct_first_system.py \
  --output /tmp/r446_flint.json.gz
```

These use the original pinned rank-six dependencies. Both public reconstruction/replay programs accept `--repo PATH` and otherwise infer the repository root from their installed location.

## Interpretation

Pinning the historical rational backend restores reproducible row serialization while leaving all exact checks intact. A future certificate format should use canonical coordinate ordering or stable equation identifiers; such a format change needs deliberate certificate regeneration or verified coordinate transport, not a silent frozen-source edit.

The initial failed run remains a failed run. This packet explains and independently repairs its reproducibility for R6_4_446. Aggregate rank-six verification must bind this full receipt together with every other required successful check. Exact replay tests the implemented necessary conditions; it does not itself prove the categorical theorems behind them.
