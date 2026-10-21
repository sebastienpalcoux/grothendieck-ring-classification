# The inversion action required by R8_3_436

## Exact source identification

The census tensor SHA256 is
`0f6d68de67a7287db7dd32a786237f7af9f35ec7c26b3ada2ba50012ff5455c7`.
Its basis subset `[0,1,2,5]` is the near-group ring
`NG(C3,3)`, with `g=1`, `g^2=2`, `X=5` and

\[
g^3=1,\qquad gX=Xg=X,\qquad X^2=1+g+g^2+3X.
\]

The odd invertible `t=3` has `t^2=1` and conjugates `g` to `g^2`.
The companion executable constructs the abstract crossed based ring for
the order-two permutation `(1,g,g^2,X) -> (1,g^2,g,X)` independently.
In the ordered basis `(1,t,g,gt,g^2,g^2t,X,Xt)`, its model-to-census map is
`[0,3,1,7,2,6,5,4]`. Every one of its 512 coefficients agrees with the
source tensor. This identification by itself constructs a ring, not a
tensor category or a coherent categorical action.

## Unitary obstruction

Suppose a unitary fusion category had this tensor. Its full neutral
subcategory on `[0,1,2,5]` would be a unitary `NG(C3,3)` category.
Conjugation by the invertible object `t` is a unitary tensor
autoequivalence of that subcategory, sending the two nontrivial
invertibles to each other.

Izumi, *A Cuntz algebra approach to the classification of near-group
categories*, [arXiv:1512.04288v2](https://arxiv.org/pdf/1512.04288v2),
Theorem 9.1 (printed p.71), classifies the relevant **C\*** categories.
Example 9.4 (p.72) gives the unique `C3+3` solution up to relabelling and
complex conjugation. Example 13.7 (p.123), together with the automorphism
description in Section 13.3 (p.128), states that these Section 9
solutions have trivial tensor automorphism group. In the explicit
parameters, inversion fails because `b(1)-b(2)=zeta_3*i*sqrt(d/3)` is
nonzero for `d=(3+sqrt(21))/2`. Thus the required conjugation action is
impossible. **R8_3_436 has no unitary categorification.**

There is also a direct source for the failure of the proposed known-model
construction: Grossman--Jordan--Snyder, *Cyclic extensions of fusion
categories via the Brauer--Picard groupoid*,
[arXiv:1211.6414v2](https://arxiv.org/pdf/1211.6414v2), Section 4.2 after
Remark 4.10 and Remark 4.11 (printed p.10), establishes that each known
Izumi--Xu category has no outer tensor automorphisms. Inner conjugations
act trivially on its commutative based ring, so no tensor
autoequivalence of either known category can invert `g`. Their
nontrivial bimodule extensions in Theorem 4.9 are a different
construction; their existence does not furnish the inversion action.

## Scope of the general categorification problem

This proof does **not** exclude all complex fusion categories with
the source tensor. Izumi's classification is a C* classification;
Remark 9.2 (pp.71--72) describes the proposed extension of its equations
to nonunitary categories as a conjectural step. The two primary sources
used here do not prove that every complex `NG(C3,3)` categorification
is one of the known Izumi--Xu categories or their Galois conjugates.
Consequently a hypothetical nonunitary neutral category with an
inversion automorphism remains outside this argument. No general
classification status is promoted by this construction attempt.

## Reproducibility

`python models/r436_inversion_attempt.py` (from the evidence directory)
recomputes the exact source hypotheses and compares the deterministic
receipt without writing. The same command under `python -O` performs
the same checks. Only `--write` regenerates the receipt. The categorical
automorphism theorem is a stated, source-bound mathematical input;
the executable does not purport to prove that published theorem.
