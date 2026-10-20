# Independent mathematical and structural review

This review checks the stated categorical deductions and independently
recomputes selected exact identities. It is an AI review, not independent
human verification or a formal proof.

## Quadratic compression

The full induced-unit refinement follows from Schopieray,
[*The dimension block of a spherical fusion category*](https://arxiv.org/html/2609.35287),
Lemma 2.1, Lemma 3.1, and the operator-norm statement of Lemma 4.1.
Retaining all distinct induced-unit coordinates in the squared norm is
valid. No extra representation-degree factor belongs in that coordinate
sum; the regular Casimir multiplicity supplies its square when translating
to the characteristic polynomial. In sphericalization, the original
fusion-algebra sector has Casimir twice the original, so its contribution
to the quadratic invariant is divided by four. The general bound is
therefore `Q <= 4`, without a pivotality assumption.

An independent calculation used multiplication by the central element
`sum_i X_i X_i*`, rather than the certificate's sum of matrix products:

| Ring | Casimir polynomial | Field discriminant | Q |
| --- | --- | ---: | ---: |
| R4653 | `(t-11)^5 (t^2-3960t+7260)` | 165 | 49 |
| R5029 | `(t-24)^2 (t-6)^2 (t-3) (t^2-1584t+6336)` | 88 | 49/9 |
| R5040 | `(t-12)^2 (t-8)^2 (t-3) (t^2-1584t+6336)` | 88 | 49/9 |
| R4569 | `(t-14) (t-7)^3 (t-3) (t^2-2940t+17640)` | 60 | 81/49 |

The first three are general exclusions. The last requires the separate
complete signed-quotient reduction. That reduction is valid: if the signed
quotient is gauge-equivalent to the original tensor, switching the chosen
lifts makes every opposite-lift product multiplicity zero. The selected
lifts form a spherical tensor subcategory equivalent to the original
category. Thus the spherical bound `Q <= 1` excludes R4569 once its complete
enumeration has been replayed.

## Conductor 60

The nine-vertex joint relative-trace hull in
`../criteria/Q60_CENTER_TRACE_PROOF.md` covers all root orders. For orders
`60m` with squarefree `m` coprime to 30, the Gauss-sum pair is a scaled
primitive-60 vertex plus a rational vertical correction contained in the
five rational vertices. Orders `120m` give the primitive-120 segment;
the remaining pairs are rational.

The replacement for equal individual twists is correct. Modular Galois
transport raises a twist to a square power. Every square automorphism fixes
the quadratic field, so normalized relative traces of both the twist and
its square are unchanged. Therefore paired row types have equal counts at
each joint trace pair, which is precisely what the moment columns require.
The local compression equality argument and its Chinese-remainder
combination apply at conductor 60. The trace certificate has pseudo-unitary
scope until combined with the independently verified signed/Galois
reduction in `../sqrt15_reduction/`.

## R4982 Morita descent

Independent full replay passed: 639 first-two-moment Fourier matrices
reduce to 18; all 18 reconstructed module graphs are isomorphic; each of
the three exact 2,048,000-point right-action boxes has one survivor; the
53 possible subgroup images reduce to two; all 729 noninvertible products
in each frame are forced; and both rank-39 based rings have the same
rank-13 closed subset of type `(1^4,4^9)` with invertibles `V4`.

The normalization is justified by the full Morita Gram identity. Its first
column block is `3I`, forcing unit first columns. Its cross block is
`diag(J3,J3,J3)`, forcing the first-row and first-column anchors to be in
the same triple, and exactly one action for each such ordered pair.
The modular-coordinate enumeration is exhaustive because its solved
coordinates are bounded by four, strictly below denominator 31.

[Jordan--Larson, Theorem 1.1](https://arxiv.org/pdf/0812.1603), with
`p=37` and `q=2`, makes any integral category of dimension 148
group-theoretical. The subgroup/double-coset argument in
`../modules/r4982_morita_descent.tex` covers every divisor of 148 for the
subgroup order. If dimensions are `(1^4,4^9)`, the four invertibles must be
cyclic; neither a `V4` complement nor a nonfaithful cyclic complement can
produce a dimension-four double-coset simple. This contradicts both forced
subrings. The argument permits arbitrary associator and subgroup cochains.

The assertion-based R4982 components must run with optimization disabled.
The ledger integration launches them in an isolated tree with this mode
explicitly enforced, including when the outer verifier runs under `-O`.

## Exact structural grouping

`exact_frontier.py` regenerates `exact_frontier.json` from the frozen initial
fifteen tensors. It uses exact positive-character root isolation, checks all
proper basis subsets and all 720 unit-fixing permutations, and records
dimension minimal polynomials, formal codegrees, subgroup actions, subrings,
and automorphisms. No numerical approximation changes a status.

The equal-global-dimension clusters are `{443,1214}`,
`{1964,5343,5623,5778}`, `{3895,5039}`, `{4530,4531}`, and
`{5029,5040}`; singleton clusters are 4569, 4653, and 4982.
Equality of this necessary Morita invariant does not establish a Morita
equivalence or a categorical model.

## Inherited finite proof trees

The three additional members R5343, R5623 and R5778 of the
5,025-induction-frame family were replayed independently, sequentially,
with the historical exact checker in both normal and optimized Python.
All six runs passed. Their receipts under `../computation/` bind the
current candidate bytes and record that numerical optimization was
disabled. The categorical scope review of their complete signed covers
is recorded in `../criteria/INDEPENDENT_SCOPE_AUDIT.md`.
