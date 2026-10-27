# The conditional R1660–R941 construction

**Status: both rings remain unresolved.** The statement concerns a hypothetical
pseudo-unitary categorification, as supplied by the project's existence reduction.

Put \(d=3+2\sqrt2+2\sqrt3+\sqrt6\). The rings R6_8_1660, R8_3_928
and R8_3_941 all have global FP dimension
\(4(1+d^2)=144+96\sqrt2+80\sqrt3+56\sqrt6\).
Equality alone does not imply categorical Morita equivalence. The complete
module-rigidity theorem for R928 rules out a rank-six Morita partner.

**Proposition.** Let C be a pseudo-unitary categorification of R6_8_1660,
with simples \(1,g,X,gX,\sigma,T=\sigma X\). If a connected separable
algebra A has underlying object \(1\oplus X\), then the fusion category
of A-bimodules has based ring R8_3_941. The same holds for \(1\oplus gX\).

**Proof.** Connectedness makes the distinguished free right module A simple.
Its internal end is A, so the diagonal action coefficients at this module
are one for 1 and X and zero for the other source simples. In particular
the sigma coefficient is zero, making it a leaf in a regular Ising block.
The complete module classification in
`manuscripts/rank6/papers/chapters/frontier_1660_morita.tex` has exactly two
regular Ising blocks and four possible rows I–IV. Row I is regular and
cannot give this internal end. Rows II and IV have nonzero T coefficient
at each leaf. Thus the row is III; after fixing the X label, its first
diagonal sign is positive and the second is either positive or negative.

The mixed-sign row is excluded by the pivotal-Frobenius pairing argument
in `evidence/unresolved7_20261027/r6_1660/MORITA_PAIRING_FILTER.md`.
The equal-sign row has precisely two necessary dual tensors. The earlier
weighted-second-indicator argument excludes one. The remaining tensor is
R941: the permutation (0,3,6,7,4,5,2,1) identifies all 512 coefficients,
as checked in the archived `rank6_pair/r941_morita_identification_certificate.json`.
There is therefore no further based-ring choice once the algebra exists.
Relabelling X and gX gives the second assertion. QED.

In the surviving linking data the dual action diagonal at the chosen leaf is
(1,0,1,0,0,0,0,0). Thus the inverse internal-end algebra in this Morita context
also has underlying object \(1\oplus Y\), with Y selfdual of dimension d
(census index 6 under the displayed permutation). This is a statement about
that Morita context; it does not force an algebra or rank-six partner in
every hypothetical categorification of R941.

The construction target is C together with A. With the unit fixed, the
multiplication on \(X\otimes X\) has one component in
\(\operatorname{Hom}(X^2,1)\) and three in
\(\operatorname{Hom}(X^2,X)\), since
\(X^2=1+3X+3gX+4T\). These four coefficients are counted before
normalization and gauge. Their associativity equations depend on the unknown
ambient associator. This is not a four-variable solution of categorification.
Neither C nor A has been constructed. The exact left and right actions supply
a concrete six-simple connecting module target, not associators.

The proof uses the complete, previously audited module and dual-action domain;
the new parity argument strengthens the earlier conditional identification by
removing the mixed-sign alternative. The general-complex existence reduction
does not assert pseudo-unitarity of an arbitrary original category.
