# An independent general obstruction from two quadratic fields

The four rings R8_2_35, R8_2_38, R8_2_346 and R8_2_406 have no
complex fusion-category categorification. This argument does not assume
pivotality, sphericality or a pseudo-unitary Galois representative.

Their regular Casimir polynomials are all

    (x-8)^4 (x^2-160x+640) (x^2-32x+128).

The two quadratic factors generate distinct fields Q(sqrt(10)) and
Q(sqrt(2)). In any sphericalization, the positive-sign sector has twice
these Casimir eigenvalues. A Casimir eigenvalue is dim(E)*f_E; all formal
codegrees f_E lie in its spherical dimension field K. Therefore K contains
the compositum Q(sqrt(10),sqrt(2)). In particular

    e = [K:Q(sqrt(10))] >= 2.

The quadratic Casimir quantity for the first factor is

    Q_10 = 40*(160^2-4*640)/640^2 = 9/4.

Applying full-I(1) compression to the sphericalization and retaining only
these two known positive-sector constituents gives

    e*Q_10/4 <= 1.

The factor 1/4 is the square of the reciprocal scaling caused by doubling
the positive-sector formal codegrees. The lower bound on e instead gives

    e*Q_10/4 >= 2*(9/4)/4 = 9/8 > 1,

a contradiction. This is valid for noncommutative rings as well: regular
Casimir multiplicities include the square of each representation degree,
which precisely accounts for its Fourier-norm contribution.

The exact factorization and input hashes are verified in
`verify_higher_field_compression.py`; the output is
`higher_field_compression_certificate.json`. The categorical estimate is
proved in `full_I1_compression.tex` from Schopieray's local modular
compression theorem. This is an independent proof of the four exclusions,
in addition to their earlier generalized-near-group reduction.
