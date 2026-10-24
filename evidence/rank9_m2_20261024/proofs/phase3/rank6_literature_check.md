# Applicability check for arXiv:2609.23559

Checked 23 October 2026. Source: Kai Wang, Jingcheng Dong and Libin Li,
*The Grothendieck Ring of Strictly Weakly Integral Fusion Categories of
Rank 6*, [arXiv:2609.23559v1](https://arxiv.org/pdf/2609.23559),
20 September 2026.

**Result: no change to the classification.** None of the nine remaining
strictly weakly integral rank-nine rings contains a strictly weakly integral
rank-six fusion subring. The paper's rank-six classification therefore has no
direct application to these residuals.

## Scope and exact applicability

The paper works over the complex numbers without a braiding assumption.
Theorem 4.4 claims eight possible Grothendieck rings for strictly weakly integral
rank-six fusion categories. The exclusions in Theorems 4.1 and 4.3 concern four
specific rank-six candidates; their induction, twist and Gram arguments do not
give an additional general criterion beyond those already considered here.

The accompanying script independently tests every unit-containing six-element
basis subset of each residual tensor: 504 subsets in total. It checks full
fusion closure, dual closure and exact simple/global FP dimensions, then
cross-checks the proper-subring lists. Basis indices are zero-based.

| Rank-nine ID | All rank-six subring bases | Simple FP dimensions | Global FP dimension |
|---|---|---|---|
| R9_2_585 | 0, 1, 3, 4, 7, 8 | 1, 1, 5, 5, 2, 2 | 60 |
| R9_2_746 | 0, 1, 4, 5, 6, 8 | 1, 1, 2, 2, 2, 2 | 18 |
| R9_2_1025 | None | — | — |
| R9_2_1209 | 0, 3, 4, 5, 7, 8 | 1, 2, 2, 2, 1, 2 | 18 |
| R9_2_1254 | None | — | — |
| R9_2_1303 | 0, 4, 5, 6, 7, 8 | 1, 1, 2, 2, 5, 5 | 60 |
| R9_2_1709 | None | — | — |
| R9_2_1759 | None | — | — |
| R9_2_1988 | None | — | — |

All four existing rank-six subrings are integral and thus outside the stated
strictly weakly integral classification. None of the ambient rings has rank
six either. This check establishes nonapplicability as a direct subcategory
criterion; it does not exclude a future indirect application after an
additional, independently proved categorical reduction.

## Caution concerning Lemma 2.2

The paper's Lemma 2.2 asserts that a faithful C2 extension of Rep(G) with one
odd simple forces G to be abelian. Its proof identifies every rank-one module
with the usual forgetful module, and hence its dual with Vec_G. That
identification is not valid for arbitrary fiber functors. We do not import
this lemma as an exclusion criterion. This observation alone does not settle
the paper's final rank-six theorem.

There is an explicit counterexample to the lemma as stated among this
project's independently audited positive constructions. Take the unitary
category TY(C5, chi, tau) and let C2 x C2 act by inversion through its first
factor. Modify action composition on the odd simple by the cocycle
beta((a,b),(c,d)) = (-1)^(bc), leaving the pointed sector unchanged. The
equivariantization has neutral component Rep(D10 x C2), where D10 has order
ten: the pointed sector is untwisted, and its action is the ordinary
inversion action. The twisted group algebra of the odd stabilizer is M2(C),
so there is exactly one odd simple. This gives a faithful C2 extension of
Rep(D10 x C2) with one odd simple, although D10 x C2 is nonabelian. Its fusion
ring is R9_2_21. The construction and full tensor match were established
independently of the new paper; see
`phase2/weak_integral/projective_ty.md`, `projective_ty.py`, `models.json`, and
`phase2/models/additional_model_audit.md`.

No new negative or positive classification record is produced by this
literature check. Reproduce its exact subset calculation with:

```sh
python phase3/rank6_literature_check.py
```

The machine-readable output is `phase3/rank6_literature_check.json`.
