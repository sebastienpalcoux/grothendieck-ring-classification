# A spherical and Galois-pseudounitary reduction for the two sqrt(5) cases

Every categorification of `R7_5_3895` or `R7_5_5039` admits a spherical
structure and is Galois conjugate to a pseudo-unitary category. This is
a necessary structural reduction, not an existence or exclusion claim.

Choose the canonical lifts used in the oriented sphericalization enumeration.
The complete enumeration gives two signed quotients for `R7_5_3895`, both
gauge equivalent to its unsigned tensor. It gives four for `R7_5_5039`,
two of which are gauge equivalent to its unsigned tensor.

For either remaining signed quotient of `R7_5_5039`, the unsigned and signed
Casimirs have respectively the factors

    x^2 - 1440x + 6400,       x^2 - 616x + 1760.

Their splitting fields are Q(sqrt(5)) and Q(sqrt(11)). All formal codegrees
of a spherical fusion category belong to its dimension field, because the
corresponding simple summand of the induced unit has dimension D/f.
The two sectors of the sphericalization have twice these Casimir roots
(the algebras here are commutative). Consequently its dimension field must
contain their degree-four compositum. But every character component of
either signed quotient has degree at most two. Its spherical dimension
character belongs to the negative sector, so its dimension field has
degree at most two, a contradiction.

Thus in both cases the actual signed quotient must be gauge equivalent to
the unsigned tensor. Switching the chosen lifts by this gauge makes every
opposite-lift multiplicity zero. The selected lifts form a tensor subcategory
of the sphericalization, tensor equivalent to the original category. The
spherical structure restricts to this subcategory.

Finally, the exact character calculation shows that every character outside
the Frobenius–Perron Galois orbit either vanishes on a simple object or takes
different values on dual objects. Neither is a spherical dimension character.
Applying the appropriate number-field automorphism therefore makes all
dimensions Frobenius–Perron dimensions, giving a pseudo-unitary category.

`verify_reduction.py` re-enumerates every signed quotient, verifies its tensor,
checks the gauges and both quadratic fields, proves the compositum degree,
and checks every original character. It uses the repository's existing
oriented sphericalization framework and the induced-unit formal-codegree
theorem cited in `manuscripts/rank7/papers/full_I1_compression.tex`.
