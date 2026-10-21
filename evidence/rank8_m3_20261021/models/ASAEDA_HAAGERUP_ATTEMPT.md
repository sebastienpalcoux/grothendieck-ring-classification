# Asaeda--Haagerup Morita-family check

`R8_3_721` has **exactly the Asaeda--Haagerup global FP dimension**
`136+32*sqrt(17)`. Its resemblance to that family cannot be dismissed by
a dimension-field or global-dimension mismatch. Nevertheless it is not
any of the six known categories in the complete AH Morita class.
This is a negative result for a specified model family, not a general
categorification obstruction.

## Published family and exact comparison

Grossman--Snyder, *The Brauer--Picard group of the Asaeda--Haagerup fusion
categories*, [arXiv:1202.4396v2](https://arxiv.org/pdf/1202.4396v2), Section
4.3, Tables 1--3 (printed p.27), gives ranks `6,9,9` and invertible counts
`1,2,2` for AH1, AH2, AH3, respectively. Grossman--Izumi--Snyder,
*The Asaeda--Haagerup fusion categories*,
[arXiv:1501.07324v1](https://arxiv.org/pdf/1501.07324v1), Lemma 3.4
(p.14), gives four invertibles and four objects of dimension
`d=4+sqrt(17)` for each of AH4, AH5 and AH6. Theorem 4.21 (p.37)
completes this Morita class with exactly six categories.

The rank-eight based rings are even more restrictive. Lemmas 3.7 and
3.15 identify AH4 and AH6 with the same `C4` ring, and AH5 with the `V4`
ring, with

\[
\alpha_g\alpha_h=\alpha_{g+h},\quad
\rho\alpha_g=\alpha_{-g}\rho,\quad
\rho^2=1+2\sum_{g\in G}\alpha_g\rho.
\]

Both have maximum multiplicity two. The accompanying executable
reconstructs all their coefficients independently and checks full
512-coefficient identifications with the existing positive controls
`R8_2_39` (AH4/AH6) and `R8_2_484` (AH5). Thus none of the exact-M3
source rings is a known AH Morita model. In particular, `R8_3_721` has
only one invertible, which independently distinguishes it from all
rank-eight members of the family.

## Source arithmetic and full baseline scan

The exact source dimensions of `R8_3_721`, in census order, are

\[
\left(1,\frac{3+\sqrt{17}}2,\frac{3+\sqrt{17}}2,
4+\sqrt{17},\frac{5+\sqrt{17}}2,3+\sqrt{17},
\frac{5+\sqrt{17}}2,5+\sqrt{17}\right).
\]

All 64 positive dimension-character identities are checked in
`Q(sqrt(17))`, and the sum of squares is `136+32*sqrt(17)`.
Its duality interchanges the two smallest nontrivial objects. Hence the
self-square hypothesis of Grossman--Snyder Lemma 4.5 is absent; that
unitary uniqueness lemma cannot be used as a general exclusion here.

For every one of the 277 baseline tensors, the verifier constructs the
integer Casimir matrix and divides its characteristic polynomial by
`x^2-272*x+1088`. Exactly fourteen sources contain this factor. For
each of those fourteen it also verifies a strictly positive exact
dimension character with the stated global dimension. The other 263
therefore have a different global dimension. The fourteen matches are
listed explicitly in the receipt; the thirteen besides `R8_3_721` are
already addressed by the independent general exclusion ledger. Equal
dimension is never treated as a positive model identification.

For `R8_3_721`, a faithful nontrivial finite-group extension or a
finite-group equivariantization of an AH category, and every Morita
dual of either, has global dimension `|G|` times the AH dimension and
so also cannot provide its model. This observation does not classify
arbitrary de-equivariantizations or new constructions outside these
specified families.

## Replay

`python evidence/rank8_m3_20261021/models/asaeda_haagerup_attempt.py`
and the same command under `python -O` are read-only exact replays.
Only `--write` regenerates `asaeda_haagerup_attempt.json`. No source
classification status or positive-model manifest is changed.
