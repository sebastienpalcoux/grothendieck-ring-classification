# Round-four model and structural scope report

No new positive model is allocated by this workstream. The frozen ten inputs
are used throughout; later exclusions do not alter the scope of this audit.

## Registered models and relative centers

`model_dimension_scan.py` reconstructs the positive dimension character
directly from the regular fusion matrices, including noncommutative inputs.
It enumerates every fusion subcategory of all 61 registered constructions,
representing 54 known rank-six rings. It compares the minimal polynomials
of FPdim(C)*FPdim(D) for all D, including Vec and C, with those of the ten
residuals. All 293 comparisons fail to match. Taking D=Vec also rules out
a residual being Morita equivalent to any currently registered rank-six
model. The output includes exact tensor and source-file hashes, all proper
fusion subsets of the inputs, and all compared polynomials.

This is a finite model-scope check. It does not cover arbitrary constructions
from models of other ranks and supplies no negative classification label.

## Specific dimension-matched Morita candidates

For a commutative pseudo-unitary fusion category of global dimension D,
a formal codegree f gives a simple summand of I(1) of dimension D/f.
This supplies a sharper model comparison than global dimension alone.
Morita equivalence preserves the braided center and hence its positive
simple-object dimensions.

The exact checks in `modular_morita_scope.py` rule out these three families:

* R6_4_629 has formal codegree 5. Its global dimension matches the modular
  category Ad(D16), but D/5 is absent from all 81 products of its nine
  simple-object dimensions. Thus the ring cannot belong to this Morita
  class, including the natural rank-eight relative-product model built
  from Ad(E8). The Ad(D16) dimensions are [1],[3],...,[13],[15]/2,[15]/2
  at q=exp(pi*i/30). The center decomposition
  Z(Ad(E8))=Ad(D16) times Fib^rev is established by Edie-Michell,
  https://arxiv.org/pdf/1709.04721, Lemma 3.3.
* R6_5_1204 has formal codegree 8. Its dimension 336+192*sqrt(3) matches
  B=C(sl3,9)^0_Rep(C3), but D/8=42+24*sqrt(3) is not a product of two
  entries in {1,3+2*sqrt(3),7+4*sqrt(3),8+4*sqrt(3)}. This rules out B
  and its entire Morita class, including the natural rank-eight relative
  product of the C3+6 near-group category. The dimensions and the center
  identification for that near-group category are in Edie-Michell,
  https://arxiv.org/pdf/2102.09065, Section 5 and Theorem 5.2.
* R6_4_91 has formal codegree 4 and global dimension equal to PSU(2)_14.
  The latter center is the diagonal-fermion quotient of same-parity pairs
  of SU(2)_14 simples. There are (8²+7²-1)/2=56 free pairs and the fixed
  pair (7,7) splits into two simples, giving rank 58. Its fixed-point
  dimensions are [8]²/2, while the required D/4 equals [8]². None of the
  other simple dimensions equals D/4 either. The exact comparison uses
  Q(zeta_32) and excludes this whole Morita class.

These statements reject proposed known models, not arbitrary hypothetical
centers of the residual rings. Galois conjugation of the known models does
not change their positive Frobenius--Perron dimension data.

## F4 parameter check

The odd-root F4 category at ell=15 has rank four, so it cannot realize a
rank-six tensor. In Rowell's root-order convention q² has order ell.
The highest-short-root alcove has fundamental-weight coefficients
(2,2,3,4), and the rank is the coefficient of x³ in
1/((1-x)(1-x²)²(1-x³)(1-x⁴)), namely four. See
https://arxiv.org/pdf/math/0503226, Section 4.7, Table 2 and Theorem 4.10.
The previously registered non-pseudo-unitary rank-six conductor-nine model
is type B2 at ell=9 restricted to integer weights, not F4; it is described
in Section 5.2 of the same source and in Schopieray,
https://arxiv.org/pdf/2010.02958, Example 1.

## Structural caution

A decomposition of the Grothendieck ring into regular modules over a
Fibonacci or Ising subcategory does not by itself imply a Deligne product
or a central lift of the subcategory. Graded-extension classification
requires invertible components and applicable multiplication equivalences.
It cannot be applied just from regular based modules when products contain
several such components. The projection theorem used in this round avoids
this extra hypothesis and only restricts objects already in the ambient
center.
