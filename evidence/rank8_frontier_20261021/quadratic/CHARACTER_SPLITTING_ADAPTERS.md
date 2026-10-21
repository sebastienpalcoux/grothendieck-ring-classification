# Complete small splitting fields for the quadratic frontier

The earlier exact `character_field_coverage.py` establishes which
characters lie in the FP quadratic field. This addendum covers the four
remaining cases with small, explicit extension fields. It does not make
a categorification claim.

| Source | Full splitting field | Degree | Defining polynomial |
| --- | --- | ---: | --- |
| 65 | `Q(√5,i)` | 4 | `u⁴−8u²+36` |
| 1055 | `Q(√37,√−3)` | 4 | `u⁴−68u²+1600` |
| 3413 | `Q(√5, real ζ9)` | 6 | `u⁶−21u⁴+2u³+84u²+24u−19` |
| 3472 | `Q(√2, real ζ7)` | 6 | `u⁶+2u⁵−9u⁴−14u³+10u²+8u+1` |

For the quartic cases `u=√q+√−r`, with `(q,r)=(5,1)` or `(37,3)`.
Inside the exact quotient field,
`rad=(u²+q+r)/(2u)` squares to `q`, and `eta=u−rad` squares to `−r`.
The explicit complex-conjugation map sends `u` to `rad−eta`; it is checked
to fix `rad`, negate `eta`, be multiplicative, and square to the identity.
The physical embedding takes `rad` to the positive square root and
`eta` to `i√r`.

For the sextic cases `u=√q+theta`, where theta has polynomial
`t³−3t+1` for q=5 or `t³+t²−2t−1` for q=2. The defining polynomials are
the products `p_theta(u−√q)p_theta(u+√q)`. The implementations check
irreducibility, all six roots real, the radical and cubic identities,
and positivity of all FP dimensions in an exact real embedding.

For all four tensors the full separating source characteristic polynomial
splits into eight distinct verified roots in the displayed field. Every
character row is then checked against all fusion products, duality, and
orthogonality. Thus this is complete splitting, not selection of only
real or dimension-field characters.

For an element lambda of any number field L, multiplication by lambda is
a rational linear operator. Its characteristic polynomial is monic and
integral exactly when lambda is an algebraic integer. If lambda is
integral the characteristic polynomial is a power of its integral minimal
polynomial; conversely that characteristic polynomial annihilates lambda.
The implementations use this equivalence for full integral closure and
do **not** test mere integrality of primitive power-basis coordinates.

`sextic_character_table.SexticTable(R,a)` and
`quartic_complex_character_table.QuarticComplexTable(R,a)` match the
partial-S table API: field K, degree, all characters, dimensions, global
dimension, codegrees, beta values, coordinates, conjugation, metadata,
`failure(v)`, and inherited `prepare/assignments`. Rational multiplication
operators are cached by exact field value. The output coordinates belong
to the full field; induction/rotation coordinates may still use the
smaller FP field.

Controls include all 64 source character values per tensor, 74 independent
direct multiplication-operator comparisons per tensor, integral primitive
generators and nonintegral rational one-half, and all twelve distinct known
center restriction columns of Fibonacci tensor Vec(C2 times C2). The known
columns remain feasible in both larger-field adapters. Normal and optimized
read-only replays pass:

```sh
python evidence/rank8_frontier_20261021/quadratic/sextic_character_table.py
python -O evidence/rank8_frontier_20261021/quadratic/sextic_character_table.py
python evidence/rank8_frontier_20261021/quadratic/quartic_complex_character_table.py
python -O evidence/rank8_frontier_20261021/quadratic/quartic_complex_character_table.py
```

The separate `review_real_partial_s.py` independently checks the previous
quadratic adapter on every low/high candidate for 1768,1795,3258. It
reconstructs all character rows from a different separating element and
compares radical trace/norm integrality with direct defining-power-basis
multiplication operators. Its receipt records 3,625, 20,823, and 4,824
candidate checks, respectively, plus the same known center control.
