# Global convex central induction

Let R be a commutative fusion ring. Work conditionally in a pseudo-unitary
categorification and let d_i and D be its positive dimensions. Each character
E labels one distinct twist-one simple constituent A_E of I(1), with dimension
beta_E=D/f_E and restriction column c_E whose unit entry is1. The central unit
is fixed separately as e_0. Enumerate every integral column with that required
dimension and necessary Gram bounds, and replace a single choice by
nonnegative variables y_(E,c) whose sum for each E is1.

Let B be the induction Gram matrix. Actual low and high restriction columns
satisfy sum y cc^T + sum x vv^T = B-e_0e_0^T. Every high column has unit entry0
and is admitted by the full nonunit Gram block. Its dimension z is a central
simple dimension, hence a d-number; D/z is an algebraic integer. These
necessary conditions are used only as filters. Their exact quadratic or
biquadratic arithmetic is independently reproducible from field operations.

Pair each high column with every joint normalized relative trace tau_k of
possible twists. Complete tables include unbounded root orders via the
conductor/prime-support compression proved in the inherited trace engines.
For each nonunit i, the first moment is0 and the second moment is nu_2(i)D:

    sum y c_i beta_E + sum x v_i z tau_k = (k==2) nu_2(i) D.

All admissible second indicators are enumerated. Low twists are1. For an
object X, order n, and proper divisor r|n, let a_i=[X^r:i]. Rotation on
Hom(1,X^n) has order dividing n. Introduce nonnegative multiplicities m_t for
every complete joint trace tuple t_r, with sum m_t=[X^n:1], and impose

    D sum m_t t_r - sum y (sum_i a_i c_i) beta_E
      - sum x (sum_(i>0) a_i v_i) z tau_(n/r) = a_0.

The right side is the contribution of the fixed central unit, which has
dimension1 and twist1. Equate all field coordinates. Exact rational row
normalization gives an integer system A x=b, x≥0. A hypothetical category
supplies a one-hot low solution and nonnegative high/rotation multiplicities;
the relaxation therefore cannot exclude an actual category. A proposed
integer ray u is accepted only after checking every entry of u^T A is
nonnegative and u^T b<0 with unbounded integer arithmetic. Numerical solver
limits or failed reconstruction mean no conclusion.

This is initially a pseudo-unitary obstruction. The outer certificate must
also replay the complete spherical-character reduction and every oriented
signed sphericalization table, using the inherited exact lifting machinery.
The general claim is made only after that full lifting succeeds. No arbitrary
pivotality, sphericality, or unitarizability is assumed.

The restored implementation caches complete data by the full tensor, records
partial indicator separators before lifting, and limits each numerical LP
search. It accepts no remembered certificate from the lost workspace: all
separators and validation receipts must be freshly regenerated.
