# R7_5_4653: exact structure and compression arithmetic

The ring is an exact uniform deformation of the representation ring of
the dihedral group of order 22. In the representation-ring basis
`1, sign, V1, V2, V3, V4, V5`, add 4 to every structure coefficient
whose three indices are all nonzero. The resulting tensor agrees with
the census after the permutation `[0,1,2,6,3,5,4]` from model indices to
census indices. The verifier compares all 343 entries.

This identity is not a construction of a fusion category. In particular,
it does not transfer the associator of `Rep(D22)` to the deformed ring.

Writing `d=13+sqrt(165)`, the exact positive dimension vector is
`(1,d-1,d,d,d,d,d)` and the global FP dimension is `1980+154*sqrt(165)`.
The Casimir characteristic polynomial is

```
(x-11)^5 (x^2-3960*x+7260).
```

The quadratic field has fundamental discriminant 165. The full
induced-unit compression invariant from
`manuscripts/rank7/papers/full_I1_compression.tex` is exactly

```
Q = 165*(3960^2-4*7260)/7260^2 = 49.
```

The existing theorem requires `Q<=4` for any fusion-category
categorification, not only for a spherical or pseudo-unitary one. Its
sphericalization argument contributes `Q/4=49/4>1` from the known sector
alone. Thus the theorem excludes this ring. This folder independently
checks its numerical and tensor premises; it does not duplicate the
finite `SL2` representation lemma on which the theorem rests.

Near-group comparison: the global dimension of `NG(C11,11)` is
`(165+11*sqrt(165))/2`. Its ratio into the present global dimension is
`13+sqrt(165)`, so these categories cannot be Morita equivalent. Their
common quadratic field is insufficient to identify a model. Primary
reference for the near-group family is Evans and Gannon,
*Near-group fusion categories and their doubles*,
<https://arxiv.org/abs/1208.1500>.

Run `python verify_structure.py` or `python -O verify_structure.py`.
The script uses explicit checks, not Python assertions, and needs SymPy.
