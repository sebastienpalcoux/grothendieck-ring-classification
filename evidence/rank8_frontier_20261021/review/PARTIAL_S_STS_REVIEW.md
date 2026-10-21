# Review of partial modular spectrum and real STS constraints

The mathematical refinement is accepted as a necessary condition for
pseudo-unitary categorification, with the exact field-membership gates
implemented in `global_induction/sts_frame.py`. This review does not by
itself add any ring to the excluded list. A general-complex exclusion
still requires complete source-bound rays for all indicator choices and
the complete sphericalization lift, or a separately proved general gate.
This is review by a separate AI agent, not human or proof-assistant review.

## Normalization

For a commutative source algebra, Deshpande's Lemma 4.3 and Corollary 4.5
identify the central character with restriction and give

    S(A_E,Z) = beta_E chi_E(FZ),   beta_E = D/f_E.

This is the unnormalized S matrix, with object dimensions in its unit
row. There is no missing factor, duality operation or complex conjugation.
Verlinde therefore makes S(A_E,Z)/dim(Z) an algebraic integer. The exact
power-basis denominator test is justified by the full integer ring of the
cyclotomic field, not merely the integer ring of a suborder.

Mueger's center theorem gives both Gauss sums equal to D. The modular
twist equation gives STS = D T^(-1) S T^(-1). Since every distinguished
constituent of I(1) has twist one, dividing the (E,F) entry by beta_E beta_F
gives precisely

    sum_Z theta_Z chi_E(FZ) chi_F(FZ) = f_F chi_E(F(A_F)).

The distinguished S symmetry already imposed on each character labeling
makes the equations symmetric in E and F. Using the 36 pairs E <= F
therefore loses no necessary equation in this real projection.

## Duality and relative trace

The ribbon dual has the same scalar twist. The exact source character
tables satisfy chi_E(v*) = conjugate(chi_E(v)). Consequently, two distinct
dual restriction vectors have conjugate product coefficients, and their
sum is real before multiplication by their common twist. A duality-fixed
restriction vector already gives real values for each character. The
code keeps a two-vector orbit as the sum of two features, and a fixed
vector as one feature, with the correct multiplicity convention.

For each retained coefficient, its membership in the actual real field K
used by the relative trace is checked by exact reconstruction in the
cyclotomic algebra. This matters also when K is smaller than the maximal
real subfield of Q(zeta_24). Once the paired coefficient c belongs to K,
normalized relative trace satisfies Tr_K(c theta) = c Tr_K(theta).
There is no claim that Re(theta c) = theta Re(c) for an arbitrary unpaired
complex coefficient. For the twist-one low terms and right side, complex
conjugation fixes K, so projection first to the real part is valid; the
remaining field-membership check ensures that relative trace fixes that
real part. Thus the implemented low coefficient and right side -1 have
the correct normalization.

## Enumeration and exact implementation

The partial-S table checks all eight distinct characters, every tensor
multiplication identity, exact orthogonality, and duality/conjugation.
Every dimension-compatible bijective labeling of every complete low
frame is searched; only character reuse or exact S asymmetry prunes a
partial assignment. The STS cone then retains a separate variable for
every surviving (frame, labeling), including repeated copies of a frame
with different labels. The positive row denominator scales and exact
bilinear high-column evaluation preserve the displayed equations.

A fresh optimized run of `global_induction/verify_sts.py` passed. Its
independent direct-S formulas check every low frame/label and selected
high columns; its direct all-column scores check the complete streaming
oracle for three integer test functionals on each of two duality-closed
restricted high domains. The controls are R8_3_334 (16 labeled frames,
459 variables) and R8_3_1739 (108 labeled frames, 959 variables). These
are implementation controls, not a substitute for each accepted
exclusion's full-domain exact ray replay. The saved R334 full-domain
feasible certificate is a useful positive control, not a constructed
category arising from this relaxation.

Primary sources independently consulted:

- https://arxiv.org/pdf/1611.04486, Lemma 4.3 and Corollary 4.5.
- https://arxiv.org/pdf/math/0111205, Theorem 1.2.
- https://arxiv.org/pdf/1310.7050, equations (2.4)-(2.6).
- https://www.jmilne.org/math/CourseNotes/ANT.pdf, Theorem 6.4(b).
