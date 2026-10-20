# Fusion coefficients on source-fixed Galois packets

This is a necessary condition for a pseudo-unitary categorification and its
modular Drinfeld center. It does not assert a categorification of either
remaining rank-seven ring.

Let `M[Y,i]` be the multiplicity of the source simple `i` in the forgetful
image of the central simple `Y`. Write `z_Y = sum_i M[Y,i] d_i` and let `D`
be the global dimension of the source, so the normalized central modular
matrix has `s[0,Y] = z_Y/D`. Let `L` contain all source character values,
formal codegrees, and Frobenius--Perron dimensions. For the two rings here
one may use `L = Q(sqrt(5),sqrt(-2))`, enlarging the real source field for
R3895 harmlessly.

For a Galois automorphism `sigma` fixing `L`, the values `z_Y/D` are fixed
and positive. The signed Galois symmetry of the central modular matrix
therefore has positive signs on every central label. Denote its permutation
by `g`. The unit row is fixed pointwise, whence `g(0)=0`. For every constituent
`A_E` of the induced unit, its modular row is

`s[A_E,Y] = chi_E(F(Y))/f_E`.

This row also lies pointwise in `L`, so `g(A_E)=A_E`. Applying `sigma` to
Verlinde, using `g(0)=0`, gives

`N[g(A),g(B)]^{g(C)} = N[A,B]^C`.

Thus `g` is a based-ring automorphism, and for any two induced-unit
constituents `A,B`, the vector of coefficients `N[A,B]^Y` is constant on
each orbit of every subgroup of source-field-fixed Galois automorphisms.
The same holds simultaneously for the entire column
`x_Y = (N[A,B]^Y)_(A,B)`.

The source-fixed square-twist orbit argument in
`FULL_SOURCE_PHASES_PROOF.md` preserves the restriction row and the relative
first and second phase moments in the multiquadratic field `F8`. It gives:

* For order16 or80, each packet has even size. It is valid to relax every
  such orbit as a union of size-two packets with identical columns.
* For the true zero phase, the multiplicity of each identical column is in
  `4 N + 5 N`. It is valid to use size-four and size-five packets and to
  allow every such partition of the displayed multiplicity.
* Other phase types receive no extra packet restriction here. In particular,
  a discovery variable's multiplicity unit may encode a different Galois
  argument; it must not automatically be imposed on each fusion column.

Consequently the residual quartic Gram matrix must admit a packet-weighted
factorization

`G_(AB),(CD) = sum_packets w x_(AB) x_(CD)`,

with integral nonnegative packet columns, each of its prescribed restriction
row and phase. Its restriction equations are

`R_(AB),i = sum_packets w x_(AB) M[Y,i]`.

Here `G` is the full low-product Gram after subtracting the contributions of
the seven already known induced-unit labels. A single diagonal equation is
already a stronger test than requiring just an integral tensor-product
decomposition: its summands must have the permitted packet weights.

The argument uses only source-field-fixing automorphisms. It does not use the
false assertion that a general normalized row transport `T(v)` is positive;
the actual general transport can be `-T(v)`.

Independent review: root and survivor_theory checked the positive-sign,
unit-fixing, based-ring automorphism, and packet-partition steps on20Oct2026.
