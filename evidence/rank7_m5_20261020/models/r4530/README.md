# R7_5_4530 and R7_5_4531: structural observations

These computations identify a common based-ring construction, not an
associator. No categorical model has been identified.

Let `A=C9` for 4530 and `A=C3 x C3` for 4531. Write the basis of
`Rep(A semidirect C2)`, where C2 acts by inversion, as `1,s,V1,...,V4`.
Adjoin a new basis element `a` and put `U=s+V1+...+V4`. For products
of two nonunit elements in the original dihedral basis, add `3a+4U`
to the original product. The remaining products are

```
a^2 = 1+3a+s+2(V1+V2+V3+V4),
a*s = a+3U,
a*Vi = 2a+3U.
```

The exact embeddings into the census are recorded in the receipt, and
all 343 coefficients of each ring are checked.

For `z=2cos(pi/9)`, satisfying `z^3=3z+1`, put
`a_dim=3z^2+3z=(z^2-1)^3` and `d=3z^2+6z+2=(z+1)^3`.
The positive dimension vector is `(1,a_dim,d-1,d,d,d,d)`.
Writing `P=3(z^2+z+1)=FPdim(PSU(2)_7)`, its global FP dimension is
`D=P^2(z+1)^2`. This numerical identity does not identify a model.
Neither ring can be the Grothendieck ring of a Drinfeld center:
the square roots of `D` are not totally positive. Indeed one satisfies
`t^3-54t^2-81t+243=0`, with a negative conjugate between -3 and -2,
and its negative has a negative conjugate at the original embedding.

The Casimir polynomial is `(t-9)^4(t^3-3078t^2+32805t-59049)`.
The cubic field is the real cubic subfield of the ninth cyclotomic
field. For its nontrivial character, the reciprocal-codegree Fourier
modulus squared is

```
(5/9)^2 - 3*(38/729) = 37/243.
```

The three cubic codegrees therefore contribute `37/81`, exceeding
`3/9` in the full induced-unit compression theorem. This excludes
spherical categorifications. If the dimension field is larger, the
left side gains the square of the relative degree while the upper
bound gains only the relative degree, so the contradiction persists.

For arbitrary categorifications, sphericalization divides this known
sector's contribution by four. Then `37/324 < 1/3`; this calculation
does **not** exclude general categorifications. A separate pivotality
argument or a stronger obstruction would be required for that scope.

Run `python verify_structure.py` and `python -O verify_structure.py`.
The full induced-unit compression theorem is stated and proved in
`manuscripts/rank7/papers/full_I1_compression.tex`; its analytic input is
Schopieray, *The dimension block of a spherical fusion category*,
<https://arxiv.org/abs/2609.35287>.
