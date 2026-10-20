# Relative twist traces over the full source field and its multiquadratic enlargement

The common arithmetic input is the Cauchy theorem of
Bruillard--Ng--Rowell--Wang, *Rank-finiteness for modular categories*,
arXiv:1310.7050v3, Theorem 3.9. For a hypothetical spherical categorification
with positive dimension `D=720+320 sqrt(5)=80(9+4 sqrt(5))`, the FS exponent
has only the prime factors 2 and 5. The parenthetical factor is an algebraic
unit. The general-to-positive reduction is a separate certificate.

We use two fields:

* `L=Q(sqrt(5),sqrt(-2))`, the complete source character field of R5039;
  it also contains the source character field of R3895.
* `F=Q(sqrt(5),sqrt(2),i)`, the maximal multiquadratic subfield of
  `Q(zeta_40)`. This gives the stronger common phase domain for both rings.

The fields have degrees 4 and 8 respectively. Every square cyclotomic
automorphism fixes F and therefore L. Since a categorical Galois permutation
changes a twist by the square of its cyclotomic automorphism, relative first
and second twist traces over either field agree across the source Galois row
orbits. Dual objects have the same twist, so duality closure also preserves
these traces.

## A finite exact domain

Let a root of unity theta have order `2^a 5^b`. If `b>=2`, the order-five
kernel in the cyclotomic tower fixes F and has zero average on both theta
and theta squared. If `a>=5`, the relevant order-two kernels similarly
give zero trace on theta and on theta squared. More explicitly, the
automorphisms `1+2^(a-1)` and `1+2^(a-2)` negate theta and theta squared,
respectively, while fixing F. The other prime component can be fixed by
the Chinese remainder theorem. Consequently all nonzero two-moment pairs
come from orders dividing 80. The larger orders give the zero pair.

For F there is a short closed form. Put `xi=zeta_8` and take the three pairs

\[
(c_1,c_2)=(1,1),\qquad
\left(\frac{-1+\delta\sqrt5}{4},
      \frac{-1-\delta\sqrt5}{4}\right),\quad\delta=\pm1.
\]

The complete domain consists of:

1. The 24 pairs `(xi^j c1, xi^(2j) c2)` for `0<=j<8` and the three choices
   above.
2. The 12 pairs `(0,xi^j c1)` for `j=1,3,5,7` and the three choices.
3. The zero pair.

The first group has orders dividing 40; the second has orders 16 or 80.
The exact cyclotomic check confirms that these 36 nonzero pairs are
distinct and that no order dividing 80 gives the zero pair.

For L there are 21 distinct nonzero pairs, and again the additional zero
pair. Primitive orders 8 and 40 have nonzero imaginary first relative
trace, and primitive orders 16 and 80 have nonzero imaginary second
relative trace. Projecting further to `Q(sqrt(5))` would lose these entries.

The verifier works in `Q[x]/(Phi_80(x))`, of degree 32. The subgroups fixing
L and F are respectively

\[
H_L=\{1,9,11,19,41,49,51,59\},\qquad
H_F=\{1,9,41,49\}.
\]

It averages each of the 80 roots and its square over the appropriate
subgroup, solves for exact field coordinates, and compares the F result
with the closed form above. Coordinates are integers after scaling by 8.

## Multiplicities for each fixed restriction row

Let sigma be a cyclotomic automorphism fixing L, hence all source
characters, codegrees and dimensions in either ring. The normalized
character transport is then the identity. The restriction multiplicity
row of a center simple is preserved under its categorical Galois
permutation: there is no residual sign, since the global dimension and
all center dimensions are fixed and positive. Equivalently, a putative
negative signed row would contradict its nonzero nonnegative restriction
multiplicities.

On twists this permutation acts by `theta -> theta^(u^2)`. Its orbits on
objects are therefore multiples of the corresponding orbits on roots.
Relative phases over F are unchanged because every square automorphism
fixes F, even though sigma itself need only fix L.

For orders 16 and 80, choose `u=3 mod 8`, fixing the fifth-primary
component as needed. Then `u^2` has order 2 on the primitive sixteenth
roots. Thus the number of objects in **each fixed restriction row and
each such relative phase** is even. The verifier checks the exact square
action on all finite-order phase records using the L-fixing subgroup.

For the genuine zero phase, the order lies outside the divisors of 80.
There are two possibilities:

* If `a>=5`, choose `u=3 mod 8` and fix the fifth-primary component.
  Since `v_2(u^2-1)=3`, the square action has order `2^(a-3)`, a multiple
  of 4, on primitive `2^a`-th roots. These objects occur in multiples of 4
  within each fixed row.
* If `b>=2`, choose `u=6 mod 25` and fix the second-primary component.
  Then `v_5(u^2-1)=1`, so the square action has order `5^(b-1)`, a multiple
  of 5, on primitive `5^b`-th roots. These objects occur in multiples of 5.

The choices exist by the Chinese remainder theorem and fix L. If both
large prime-power factors occur, the independent actions give a multiple
of 20. Partitioning by twist order shows that the genuine zero-phase
multiplicity within each fixed row belongs to

\[
4\mathbb Z_{\ge0}+5\mathbb Z_{\ge0}.
\]

Thus counts 1, 2, 3, 6, 7, and 11 are forbidden. In an integer relaxation
one may parameterize each zero-phase count as `4x+5y`, with nonnegative
integer variables x,y. This is a necessary condition, not a sufficiency
claim or a categorification test by itself.

## Interface and reproduction

`full_source_phases.py` exposes `phase_records(field)` and
`phases_scaled8(field)`, where field is `L4` or `F8`. The default is L4
for compatibility; F8 is the stronger domain intended for both rings.
Each record contains the scaled phase tuple, finite-order provenance,
and a necessary fixed-row multiplicity factor. The zero record is last
and carries `zero_semigroup=[4,5]`.

For L4 the ordered basis is
`(1,sqrt(5),sqrt(-2),sqrt(-10))`; for F8 it is
`(1,sqrt(5),sqrt(2),sqrt(10),i,i*sqrt(5),i*sqrt(2),i*sqrt(10))`.
The first half of each tuple is the first moment, the second half is the
second moment. Both are scaled by 8.

Run the script normally and with `python -O`, using `--field L4` or
`--field F8`. The exact receipts are `full_source_phases_certificate.json`
and `maximal_multiquadratic_phases_certificate.json`.
