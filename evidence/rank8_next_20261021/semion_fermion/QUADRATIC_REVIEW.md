# Independent review of quadratic algebra and Morita closure

Reviewed by the semion/fermion workstream on 2026-10-21. The producer is the
separate `../quadratic` workstream. No producer file is changed by this review.

**Theoretical conclusion: the new closures are valid necessary conditions for
arbitrary complex fusion categories.** No pivotal, spherical, or unitary
assumption is needed.

The primary reference was checked directly: Etingof–Nikshych–Ostrik,
[Fusion categories and homotopy theory](https://ems.press/content/serial-article-files/36746),
§2.5, equation(1), Proposition2.2, and Remark2.3. These give the canonical
positive module dimension function, the internal-Hom product formula, and its
normalization by the sum of squares. Applying the formula to the root regular
module A and a simple module M yields

    FPdim(internalEnd(M)) = (B_M · d)^2 / FPdim(A).

Thus the entire multiset of these squared canonical module dimensions is
unchanged when another simple module is chosen as the root. Every such root
gives a connected separable internal-end algebra in the same original fusion
category. Iterative removal of impossible dimensions is sound; profile closure
is sound as well. The profile test removes whole profile classes, so its single
pass already gives a fixed point at that stage.

The matrix entry bound is also valid without unitarity. The common positive
module dimension vector is an eigenvector of M_i M_i^t with eigenvalue d_i².
This nonnegative symmetric matrix has spectral radius d_i². Each row square
norm of M_i is therefore at most d_i², so every entry is at most floor(d_i).

The induction and action conventions were checked. With
B[r,j]=[X_j A:M_r] and M_i[r,s]=[X_i M_s:M_r], one has
M_i B=B R_i^t and M_i[r,0]=B[r,i]. The underlying object of a connected
separable algebra is self-dual, so the transpose convention in B^t B=N_A is
harmless. Indeed the nonzero counit pairing gives a nonzero module map from
the simple regular module A to its dual; equal Frobenius–Perron dimensions
make this map an isomorphism.

When B has full row rank, its right inverse forces all M_i. The producer checks
all fusion products, duality, integrality and nonnegativity. Since every
indecomposable module category admits a simple root and its connected
internal-end algebra, exhaustive rooted factors give an exhaustive list of
possible based actions whenever every surviving factor has full row rank.
This applies to R65. It does not assert that the listed based actions lift to
module associators.

`review_quadratic.py` independently reconstructs every internal-end dimension
and profile from the saved integral factors, reproduces the complete iterative
dimension and profile closures, verifies all75 full-rank actions directly,
recomputes their32 permutation classes, and checks all32 canonical algebras
X X* survive. It imports no quadratic producer and writes no quadratic file.
The resulting counts are148 possible algebra objects and182 induction factors.
For R65, the twelve factors give exactly six possible based actions of ranks
2,2,4,4,8,8. All results agree with the producer.

The review also inspected the complete pivot-box Gram enumeration and its
integer branch bounds, the rejected action-row certificates, and the exact
character trace test. The expensive full Gram/row replay is separately
provided by the quadratic campaign's normal and `-O` verifiers. This independent
review does not claim to duplicate that replay.

Reproduce the independent closure/action checks with:

```sh
python evidence/rank8_next_20261021/semion_fermion/review_quadratic.py
python -O evidence/rank8_next_20261021/semion_fermion/review_quadratic.py
```

`quadratic_review.json` binds the reviewed producer receipts and README by
SHA256. These statements refine necessary algebra and module data. They give
no new ring exclusion, algebra multiplication, associator, or category.
