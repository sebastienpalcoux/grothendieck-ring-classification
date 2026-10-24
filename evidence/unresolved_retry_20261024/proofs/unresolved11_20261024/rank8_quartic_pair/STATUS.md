# Rank-eight quartic pair: October24 theoretical follow-up

**Status: no new exclusion or categorical model. Both R8_3_928 and R8_3_941
remain unresolved.**

The new result is a complete, rank-unbounded categorical module and Morita
classification for any hypothetical R928 categorification. See
`R928_MORITA_RIGIDITY.md`, its exact verifier `r928_module_rigidity.py`, and
receipt `r928_module_rigidity.json`. Every indecomposable module is regular;
every categorical Morita partner is the original category; the four
connected separable algebras are the internal matrix algebras of simple
objects; every tensor functor is fully faithful onto its fusion image.
These conclusions close construction routes but do not turn the ring into
an excluded case.

The current R928 phase patterns remain40,49,186,191. The current R941
center allocations remain8,19,21,31,34,43,45,56,60,72,73,77,79,85.

## The known E21 model does not transfer by Morita equivalence

The known categorification of R8_3_982 and both targets have the same FP
global dimension

    144 + 96 sqrt(2) + 80 sqrt(3) + 56 sqrt(6).

The published R982 Morita restrictions apply to partners of **every rank
and multiplicity**, not merely the census range. The audited chain is:

1. `evidence/rank8_research_20261022/r982/MODULE_TYPES.md` proves every
   module has rank8 from a complete internal-end list and determinant-one
   or diag(1,2,2) paired Gram lattices. No module-rank cutoff is assumed.
   The rank12 lattice possibility is excluded by parity and a norm bound.
2. `evidence/rank8_creative_20261022/r982/MORITA_OBJECT.md` uses the three
   complete module types, all rationally regular, and module-character
   reciprocity to force the same canonical Lagrangian object and hence a
   commutative rank8 dual fusion ring. The categorical reciprocity inputs
   are explicitly Schaumann1206.5716v3 Prop5.8/Thm4.5 and
   Shimizu1801.02493v2 Thm5.4, Lem5.9, Thm5.11, Cor5.13, Thm3.13–3.14.
3. `evidence/rank8_creative_20261022/r982/MORITA_RING.md` forces the full
   same based ring through a linking-Gram orthogonal transformation and
   the odd-unimodular index2-overlattice classification of D8.

All three verifiers passed independently in this follow-up, read-only. This
review checked the complete rank argument and followed the recorded
categorical dependencies, rather than independently reproving every
upstream pivotality or character-reciprocity theorem.

## R941 and the fermionic quotient

The unique central invertible lift of g is a fermion. The source has a
trivial pointed associator, so the ordinary algebra1+g does exist. Its
right-module category has rank4. This does not make the quotient an
ordinary rank4 fusion category: fermion condensation is a superfusion
construction. The central-fermion construction without a braiding on the
source is described in Aasen--Lake--Walker, *Fermion condensation and super
pivotal categories*, Section4.1.3:
https://arxiv.org/html/1709.01941v2#S4.SS1.SSS3

Free g action means its four quotient simples have scalar endomorphism
algebras, but it does not eliminate odd fusion channels. The same paper,
Section6.1, explicitly gives SO(3)_6/psi with no q-type simples and a mixed
even/odd fusion channel. Thus ordinary rank4 bounds cannot be imported
through an alleged absence of q-type objects. No such exclusion is used.

The signed quotient of the R941 fusion algebra at g=-1 is the split
quaternion algebra: on representatives1,b,a,d,

    b^2=-1, a^2=d^2=1,
    ba=-d, ab=d, bd=a, db=-a, ad=b, da=-b.

For R928 the analogous quotient is the Hamilton quaternion algebra, with
all three generators squaring to-1. These elementary identities describe
decategorified algebras; neither one supplies an associator or obstruction.

The rank-six investigator identified the surviving rank-eight alternative
in the R6_8_1660 Morita reduction with R941 coefficientwise, using
permutation (0,3,6,7,4,5,2,1); all 512 coefficients agree. The receipt is
`rank6_pair/morita_r941_identification.json`. This is a necessary possible
dual, not an equivalence of existence: the required nonpointed algebra
has not been constructed or forced.

## Integral-center criterion cross-check

The new solvability/Tannakian criterion proposed by the rank9 agent cannot
reduce these two current center domains. Exact FP dimensions show that,
among all65 canonical high columns, the only integral ones are index40
(dimension1) and index45 (dimension2). The complete343-pattern
`quartic_integer_center/gram_cubic.json` already has multiplicity40=1 and
multiplicity45=0 in every pattern. Hence every current pattern already has
only the two invertible integral center simples1 andG. This is a direct
check of the old complete domain, not a new exclusion.

## Independent rank-nine audit

The separate requested audit is recorded in `AUDIT_RANK9.md`. It confirms
the arbitrary-complex categorical scope of the central-quotient,
normalizer, and integral-center arguments. Independent full equation
reconstruction verifies the positive-TY-sign exclusions for R1607, R1976,
and R1975, while preserving their unresolved full-ring status.
