# Integral-center deletion in the original R439 and R567 systems

This exact additional necessary-condition test does not exclude either ring.
Each system has one exact rational feasible witness after all nonunit
integral-dimensional central restriction types are deleted. Feasibility of
these relaxations supplies neither a fusion category nor a complete center.

The categorical input is the independently reviewed proposition in
`../review/INTEGRAL_CENTER_SUBCATEGORY.md`, bound computationally by
`../review/integral_center_subcategory.py`. Its conclusion is general-complex:
the tensor unit is the only integral-dimensional simple in either center.
The source-specific Galois-to-pseudo-unitary reductions, full-S low-frame
enumeration, and joint rotation equations are the earlier prerequisites in
`../noncommutative_followup/`. The receipt keeps its conditional scope explicit
so that the arithmetic replay does not purport to prove these categorical
inputs itself.

The complete full-S low-frame domain leaves frame 2 for each ring. Its four
nonunit distinguished columns all have nonintegral dimensions. Among the 45
high restriction types, exactly two have integral dimension:

| Ring | Zero-based type indices | Dimensions |
|---|---|---|
| R8_3_439 | 13, 34 | 3, 2 |
| R8_3_567 | 0, 34 | 3, 2 |

For each forbidden type, its 19 nonnegative joint-phase weights have sum zero.
These equations are added to the frozen height-six Gram, indicator, and tensor
rotation system. The original-ring systems used here do not include STS
equations. All eight indicator branches are reconstructed for each ring. Seven
retain exact Farkas obstructions; the remaining branches have exact nonnegative
rational solutions:

* R8_3_439: `(0,0,1,1,1,1,1)`;
* R8_3_567: `(0,0,0,0,-1,-1,-1)`.

The receipts bind the ordered high types, full-S domain, entire augmented
matrices and right-hand sides, all indicator branches, and the exact witnesses.
The read-only verifier uses explicit checks in both Python modes:

```sh
python evidence/rank8_frontier_20261021/integral_center_filter/verify_original.py
python -O evidence/rank8_frontier_20261021/integral_center_filter/verify_original.py
```

Both commands passed on 2026-10-21. The `--write` option is discovery mode and
is not needed for replay. Height six is the complete finite moment domain of
this test, not a proven bound on the exponent of a hypothetical category.
