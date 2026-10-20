# Three quadratic Casimir exclusions

These are **general complex fusion-category exclusions**, with no pivotal,
spherical, or pseudo-unitary assumption on the proposed categorification.
They apply the existing full induced-unit compression theorem, rather than
introducing a further conjectural obstruction.

## The bound used

See `manuscripts/rank7/papers/full_I1_compression.tex`, specifically
Corollary `cor:quadratic-Casimir` and Corollary `cor:compression-boundary`.
The local modular-representation compression input is Schopieray,
*The dimension block of a spherical fusion category*, arXiv:2609.35287v1,
Lemma 4.1 and the proof of Theorem 5.1. The repository's refinement retains
all the simple constituents of the induced unit. It does not rely on an
identification of a dimensional grading for an arbitrary spherical category.

Let `N_i` be regular fusion matrices and `B = sum_i N_i N_i^T`.
For a real quadratic field L of fundamental discriminant q, collect all
irreducible quadratic factors `(x² - t_j x + n_j)^m_j` of the characteristic
polynomial of B that generate L. Set

`Q_L = q sum_j m_j (t_j² - 4 n_j) / n_j²`.

The spherical bound is `[K:L] Q_L <= 1`, where K is the dimension field.
For an arbitrary categorification, take its canonical sphericalization.
The epsilon=+1 sector of its fusion algebra is the original fusion algebra;
the sphericalized Casimir restricts to `2B`. Replacing every quadratic
root by twice that root divides the displayed Q contribution by four.
All other contributions to the squared-norm inequality are nonnegative.
Consequently `[K:L] Q_L/4 <= 1`, and in particular **Q_L <= 4**.
This argument uses the actual sphericalization of a hypothetical category,
so it does not impose a proposed signed quotient or presume a pivotal
structure on the original category.

## Exact witnesses

| Ring | Quadratic Casimir factor | Fundamental discriminant q | Q_L |
| --- | --- | ---: | ---: |
| R7_5_4653 | x² - 3960x + 7260 | 165 | 49 |
| R7_5_5029 | x² - 1584x + 6336 | 88 | 49/9 |
| R7_5_5040 | x² - 1584x + 6336 | 88 | 49/9 |

All three values exceed four. They therefore exclude every complex fusion
category with the corresponding based ring.

For comparison, R7_5_4569 has factor `x² - 2940x + 17640`, q=60,
and Q=81/49. This excludes a spherical categorification only; this file
does **not** promote that conditional result to a general exclusion.

## Exact replay and controls

`quadratic_compression.py` builds B from each source tensor, factors its
integer characteristic polynomial, computes the fundamental discriminants
and rational Q values exactly, and verifies certificates by recomputation.
The receipt hashes each tensor and records every factor. The proof checks
use explicit exceptions and remain active under Python optimization.

From the repository root:

```
python evidence/rank7_m5_20261020/criteria/quadratic_compression.py
python -O evidence/rank7_m5_20261020/criteria/quadratic_compression.py --replay
```

The 15-ring frontier gives exactly the three general exclusions above.
All 30 rank-seven model controls satisfy even the spherical bound. Three
deliberately corrupted Q certificates are rejected. The spherical-only
R7_5_4569 result is explicitly checked not to produce a general certificate.
The full receipts and controls are in `quadratic_compression_results.json`.
