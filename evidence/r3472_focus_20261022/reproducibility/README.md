# R3472 creative-stage reproducibility repair

At repository revision `ebaeb62`, the command

```sh
python evidence/rank8_creative_20261022/r3472/verify.py
```

failed at its seventh line with `ModuleNotFoundError: No module named
'second_branch_count'`. The imported helper was absent from the repository,
the creative acceptance file, and the creative source manifest. Thus the
published replay receipts did not suffice to make this particular check
reproducible from the published source inventory.

The missing helper has been reconstructed from the finite arithmetic domain
proved in the existing `r3472/PROOF.md`. It counts multisets of integral pairs
`u >= 0`, `t >= 1` satisfying

```
sum u^2 = 35-h,   sum u*t = 70,   sum t^2 = 175.
```

For positive `u`, the equations give `u <= floor(sqrt(35-h))`, `t <= 13`,
and a finite upper bound on every multiplicity. A memoized recursion visits
every multiplicity of every allowed type exactly once. Cauchy's inequality
discards only impossible residual states. For `u=0`, the remaining choices
are partitions of the unused `t^2` sum into positive squares. Their exact
generating-function coefficients are computed by an integer coin recurrence.
There is no numerical optimization, floating-point arithmetic, or search
cutoff.

The reconstruction is not presented as the unavailable original source.
Its cache traversal differs, so its honest diagnostic state counts differ:

| h | Spectrum count, both algorithms | Historical cache states | Reconstructed cache states |
|---|---:|---:|---:|
| 1 | 272,348 | 158,885 | 1,078,029 |
| 2 | 124,228 | 121,756 | 840,138 |
| 5 | 3,900 | 37,967 | 232,981 |
| 7 | 2 | 832 | 681 |

The spectrum total is unchanged: **400,478**. These are conditional necessary
dimension spectra, not categorifications.

The original `verify.py`, `product_equations.py`, and `exact_integer.py` are
unchanged. The original verifier's `--write` mode regenerated `verification.json`
with the new diagnostics; its full equality comparison was retained. Exactly
four fields changed, all `second_branch_arithmetic_counts[i].states`. In
particular, all six product-exclusion searches, their node counts, the input
tensor positive control, input hashes, mathematical counts, and unresolved
classification status remain unchanged.

The historical files are preserved byte-for-byte here:

- `original_verification.json`: original mathematical receipt;
- `original_accepted.json`: original acceptance/source binding;
- `original_source_manifest.json`: original publication source inventory.

The archived manifest binds the original acceptance file and receipt by
SHA256. The repair audit verifies these identities, and also verifies that the
original three mathematical scripts retain their accepted hashes. The active
acceptance file now binds both the reconstructed helper and the regenerated
receipt. Publication manifests and aggregate replays must be regenerated as
part of the enclosing publication update; the archived receipts are retained
as history, rather than represented as verification of the repaired sources.

## Independent audit

`verify_repair.py` computes the same four counts independently by multiplying
finite geometric-series factors in descending type order, using an iterative
sparse coefficient table. It completes the `u=0` sector by a separate
largest-square recursion. This algorithm neither imports nor calls the
reconstructed helper. It then runs the unchanged original verifier in normal
and optimized Python and checks both outputs against the regenerated receipt.

```sh
python evidence/r3472_focus_20261022/reproducibility/verify_repair.py
```

The checked result is `repair_verification.json`; both original-verifier
stdout logs are retained alongside it. The repair makes no new exclusion and
constructs no category. **R8_3_3472 remains unresolved.**
