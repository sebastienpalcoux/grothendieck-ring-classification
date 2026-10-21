# Unitary realization of R8_3_448

The initial certificate used only Ostrik's Appendix A.5–A.6 in
Calegari–Morrison–Snyder, *Cyclotomic integers, fusion categories, and
subfactors*. That appendix explicitly establishes pseudo-unitarity.
The certificate therefore initially asserted only pseudo-unitarity.
The following additional primary sources justify upgrading the existence
scope to unitary; the fusion tensor and its census identification are unchanged.

Morrison–Penneys, *Constructing spoke subfactors using the jellyfish
algorithm*, [arXiv:1208.3637v2](https://arxiv.org/pdf/1208.3637), §5.1,
pp.25–26, constructs a symmetric self-duality for the 2221 subfactor
planar algebra (Theorem5.5). The preceding discussion explicitly states
that removing the shading gives an unshaded spherical positive C*-planar
algebra, whose projection category is a Z2-graded unitary fusion category
with fusion graph2221. Its neutral category is the Izumi–Xu category,
and its odd component is the module category M3 for 1+g+g².

Grossman–Jordan–Snyder, *Cyclic extensions of fusion categories via the
Brauer-Picard groupoid*, [arXiv:1211.6414v2](https://arxiv.org/pdf/1211.6414),
Theorem4.9 and Remarks4.10–4.11, classify extensions of either known IX
category by this bimodule. There are exactly two, and their distinction
is the H3 associator choice; the underlying bimodule multiplication and
integer fusion coefficients are unchanged. The paper explicitly identifies
Ostrik's and Morrison–Penneys's constructions as the earlier constructions
recovered by this theorem. The two choices of complex-conjugate IX category
also have identical integer fusion coefficients. Consequently the unitary
2221 construction has precisely the ring of Ostrik's Appendix A.6.1.

`izumi_xu_extension.py` reconstructs the entire tensor from those published
rules, including the essential noncommutative relation Vg=g²V. The
recorded source-to-model permutation checks all512 constants against
R8_3_448. Thus the unitary assertion is bound to a complete based-ring
identification, not only the principal graph or Frobenius–Perron dimensions.

This argument also explains why the commutative tensor R8_3_347 is not
obtained by choosing the other associator: an H3 twist does not alter
integer fusion coefficients.
