# Applicability of the two-prime integral-center theorem to all seven NC cases

This table addresses the seven noncommutative rings in the original frontier.
It does not introduce a categorification or exclusion decision. The general
criterion is proved in `INTEGRAL_CENTER_SUBCATEGORY.md` and its TeX companion.
Here D denotes the source global Frobenius--Perron dimension; the center has
dimension D^2. In each row Q(D^2)=Q(D), checked by an irreducible characteristic
polynomial, so the prime support of Norm(D^2) is the same as that of Norm(D).

| Ring | Norm(D) | Proven center-invertible information | Criterion applies? |
|---|---:|---|---|
| R8_3_439 | 576 = 2^6 3^2 | trivial | yes; integral subcategory dimension divides 576 |
| R8_3_455 | 468 = 2^2 3^2 13 | order 2, from the universal C2 grading | no: both hypotheses fail |
| R8_3_567 | 576 = 2^6 3^2 | trivial | yes; dimension divides 576 |
| R8_3_721 | 1088 = 2^6 17 | trivial | yes; dimension divides 1088 |
| R8_3_928 | 147456 = 2^14 3^2 | order 1 or 2; not determined here | not established |
| R8_3_941 | 147456 = 2^14 3^2 | order 1 or 2; not determined here | not established |
| R8_3_1154 | 3600 = 2^4 3^2 5^2 | trivial | no: three-prime norm |

The verifier computes source invertibles, those commuting with every source
basis object, the adjoint subring, and every adjoint component directly from
the full tensor. It does not infer trivial center invertibles merely from
the ring center. The forgetful homomorphism on invertibles has kernel
Aut_tensor(Id), the character group of the universal grading group. For six
rows the adjoint subring is the entire ring. R455 instead has a faithful
universal C2 grading, checked on all tensor coefficients; its only ring-central
invertible is the unit, so its center has exactly the two kernel invertibles.
For R928/R941 the universal grading is trivial, but a second ring-central
invertible remains. Whether it admits a half-braiding is not decided by this
calculation, and the theorem is not asserted for those rows.

Fusion closure of the integral central objects is also checked explicitly for
every row. The verifier records an exact rational linear functional on the
nonconstant coordinates of the FP character field. It vanishes on rational
source dimensions and is strictly positive on every other simple source
dimension. Therefore a nonnegative sum of source dimensions is rational only
when every summand is integral. The integral source labels are independently
checked to be closed under tensor product and duality. Thus the integral
central objects form the preimage of that source fusion subcategory.

For R721 this gives a genuine additional application of the unified theorem.
Its only integral source simple is the tensor unit. Any high restriction
column already has zero unit coordinate, so the theorem adds no new high
column deletion to its existing induction enumeration. It does rule out
nonunit integral central simples categorically.

The exact all-seven replay is `integral_center_applicability.py` with no
arguments, and also runs with `python -O`. It reconstructs the scalar FP
characters and both dimension polynomials from the source tensors, verifies
all rational functional witnesses without a numerical solver, and checks the
saved receipt. Its only direct scalar-character dependency is the frozen
baseline exact implementation, which verifies all character multiplication
identities and the unique positive embedding.
