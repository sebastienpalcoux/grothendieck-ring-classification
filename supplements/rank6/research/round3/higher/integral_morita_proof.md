# Integral refinement of the full Morita Gram obstruction

Let a categorification of the input ring have a forced split involution
algebra A=1⊕g. Enumerate all compatible split-module actions by the existing
exact antiinvariant module procedure. Fix one such module action. The
full Morita Gram construction exhausts a finite list of possible integral
right-action matrices B_1,…,B_t for simple objects of the dual fusion
category. Their vectorized outer products, together with the prescribed
first-column multiplicities, give the exact integer system

    A x = b,  x ∈ Z_{≥0}^t.

Here x_j counts simple dual objects with right-action matrix B_j; distinct
simple objects are permitted to have the same matrix. All entries of A and
b are reconstructed from the full input tensor and the module branch.
The prior rational relaxation used only x≥0 over Q or R.

**Congruence obstruction.** If an integer q>1 and an integral row vector y
satisfy yA≡0 (mod q) and yb≠0 (mod q), this branch cannot occur.

Indeed any integral solution would give yb=yAx≡0 (mod q), a contradiction.
No sign, positivity, sphericality, braiding, unitarity, or restriction on the
field of categorical dimensions is used in this argument. The only
nonnegativity is the ordinary multiplicity of a simple object. Removing
identical or zero equality rows before finding y preserves the solution set.

The implementation `round3_integral_morita.py` reconstructs the full system,
performs deterministic duplicate-row removal, and checks both pairings with
Python integers. All new application witnesses use q=2. The module verifier
never invokes linear or integer optimization. In particular the exploratory
MILP statuses are not mathematical certificates.

## Combination with Clifford rotation

For both R6_5_638 and R6_7_1225, the exhaustive module domain has 16 branches.
Two fail the Morita rank bound and twelve fail this congruence criterion.
The two remaining branches force negative stabilizer signs on objects 4 and
5. Their cubic rotation spaces have dimension 4 and 6 respectively. The
existing Clifford lemma forces their third indicators into {−2,1} and {−3,0},
respectively; in fact the weaker interval bounds already suffice in each
central trace system.

For each tensor there are exactly 91 low induction frames, 31 with a
nonempty character labelling set, and 50 labellings. Their four second-
indicator choices give 200 height-six exact separating systems. All frames,
labellings, signs, and possible restriction columns are exhausted by the
existing public verifier, with no finite cutoff on twist orders. The fields
are Q(√65) and Q(√145), with exponent prime supports {2,5,13} and {2,5,29}.
The low-column counts are (217,225,225,61,61) and (469,481,481,127,127).

The independent unrestricted signed reductions enumerate 11,800 tables in
418 sign orbits for R6_5_638, and 46,856 tables in 1,560 sign orbits for
R6_7_1225. In each case every nonoriginal signed orbit is excluded, and the
single original sign orbit has only the FP Galois orbit as a nonzero
admissible dimension character. Thus the combined exclusion has general
complex-fusion-category scope, rather than assuming a pivotal structure.

The certificate kind is `general_integral_morita_rotation`, with exact
entry point `round3_integral_morita.verify_general(R,certificate)`.
Full verification status is recorded in the adjacent `*_general.json`
files; discovery-only records are explicitly distinguished.

## Primary background source

Ng–Schauenburg, *Frobenius–Schur Indicators and Exponents of Spherical
Categories*, arXiv:math/0601012,
https://arxiv.org/abs/math/0601012, provides the center-twist formula and the
identification of the FS exponent with the twist order of the center.
The new congruence step is the elementary displayed argument above, applied
to the already proved full Morita Gram identity of this package.
