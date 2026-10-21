# R8_3_1154: reviewed Galois follow-up

A new exact Galois signed-permutation obstruction excludes **11 of the 36**
remaining pair-product histograms. It retains **25 histograms across the same
three central-restriction patterns**, 6971, 8766, and 8772. R8_3_1154 remains
unresolved. The pseudo-unitary-center proof scope is explicit in [PROOF.md](PROOF.md).

This is a follow-up to the frozen `rank8_next_20261021` package; no files in that
package were modified. Its manuscript's three-pattern statement remains valid.

- `galois_pair_probe.py` and `.json`: complete labelled-source / grouped-target
  enumeration and deterministic exact result, including source-file hashes.
- `review.py`, `review.json`, and `INDEPENDENT_REVIEW.md`: independent transportation-table
  verification, including direct signed-permutation witness reconstruction.
- `verification.json`: normal/optimized replay and file-hash receipt.

From the repository root:

```sh
python evidence/rank8_postpublication_20261021/r1154_galois_review/galois_pair_probe.py
python evidence/rank8_postpublication_20261021/r1154_galois_review/review.py
```

The scripts use the repository's existing Python/SymPy exact arithmetic code.
No numerical solver status is used as an exclusion certificate. A retained
histogram satisfies these necessary equations only; it does not certify a
model or establish exoticity.
