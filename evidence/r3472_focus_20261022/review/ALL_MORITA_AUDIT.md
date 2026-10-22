# Independent review of the R3472 all-Morita restriction

The reviewed statement is the proposition in `../morita/manuscript.tex`:
every Morita partner of every complex categorification of `R8_3_3472` has
either one or seven invertible simples; in the latter case its full dimension
profile is `1^7,(7+5*sqrt(2))^7`. This is a necessary restriction, not an
existence or nonexistence theorem for the source ring.

**Review conclusion:** the expanded proof is valid with the stated scope.
No assumed realization of a rank-two based module, commutativity of the
Morita partner, pivotal structure, pseudo-unitarity, or braiding is used.
The categorical arguments below were checked mathematically; the separate
Python audit checks their finite arithmetic, not the categorical theorems.

## Dimension-field descent

The source tensor has only the unit invertible and has `N_ii^i=2` for all
seven nonunit simples. A central invertible must forget to the unit. Its
half-braiding then gives a tensor automorphism of the identity, with nonzero
scalars satisfying `lambda_i^2=lambda_i`. Every scalar is one. Consequently
the center has no nontrivial invertibles, a property preserved under Morita
equivalence. This direct argument avoids dependence on the separate theorem
about simplicity of the center and on the earlier sphericalization analysis.

For any proposed Morita partner, every conjugate of a squared FP dimension
is an eigenvalue of `N_Y N_Y^T`, hence is nonnegative. Thus the dimension
field is totally real. Every conjugate of `d_Y` is an eigenvalue of `N_Y`,
so its absolute value is at most `d_Y`. An embedding fixing the total
dimension must attain equality in the sum of these squared inequalities,
and hence sends each simple dimension to a sign times itself. Equality in
the product dimension triangle inequalities makes those signs a tensor
automorphism of the identity. Its triviality implies that every embedding
fixing the total dimension is the identity. Characteristic-zero separability
then proves field equality. No assertion that the field extension is Galois
is required.

For total dimension `700+490*sqrt(2)`, all dimensions therefore lie in
`Z[sqrt(2)]`. The spectral-radius inequality for the other embedding forces
both coordinates to be nonnegative. Orthogonality of distinct one-dimensional
dimension characters holds for noncommutative based rings too; it does not
require commutative fusion rules. This proves the three moment identities.

## Primary hypotheses of strong Lagrange

The supplied BIMSA URL currently serves the published paper by Alekseyev,
Bruns, Dong, and Palcoux, *Classifying integral Grothendieck rings up to rank 5
and beyond*, Letters in Mathematical Physics **116** (2026), article 141,
[DOI 10.1007/s11005-026-02164-7](https://doi.org/10.1007/s11005-026-02164-7).
In that version the needed result is **Proposition 5.7**, printed page 33,
and its dimension-type consequence is Corollary 5.8. The earlier numbering
4.12 must not be attached to this version. Source checked:
<https://bimsa.net/doc/publication/14753.pdf>.

Proposition 5.7 applies to an arbitrary complex fusion category, a fusion
subcategory, and an indecomposable component under the subcategory's left
action. It imposes algebraic integrality of the component dimension divided
by the subcategory dimension. A pointed subgroup's simple-object orbits are
exactly the relevant indecomposable components. Thus the use of
`orbit_size*d^2/group_order` has the required hypotheses and normalization.

The integral subcategory is closed because radical coordinates are
nonnegative. Its small possible dimensions and pointedness argument are
complete. The order-two contradiction correctly counts every free orbit
twice and uses even rational coordinate on fixed simples, contradicting
the odd mixed moment 245.

## Exhaustive order-five reduction

The independent audit starts with all fixed and free types together,
before dividing moments by five. Fixed types require both coordinates
divisible by five. The full type list, with minimum multiplicity steps, is

```
(1,1;5), (2,1;5), (3,2;5), (4,3;5),
(5,4;5), (6,4;5), (7,5;5), (15,10;1).
```

Exact enumeration of all multiplicities gives the same four profiles as
the manuscript and no solution containing the fixed type `(15,10)`. This
also independently confirms the manuscript's residual Cauchy exclusion.

The smallest-dimensional product in profile A has exactly one invertible
summand by its trivial stabilizer. Its remaining dimension cannot be
expressed using the available nonintegral dimensions. In B and C, the
unique orbit of dimension `u=1+sqrt(2)` is dual-stable. The right orbit of
the dual of a simple fills this same orbit, so every product of two such
simples has exactly one invertible summand. The remaining dimension `2u`
cannot contain any larger available simple. This proves the claimed
rank-ten fusion subcategory, including multiplication and dual closure.

## Why the six-orbit quotient in profile D is a fusion ring

Right multiplication by the five-element group permutes the left orbits
of each dimension. There are fewer than five, so each left orbit is fixed.
All left actions are free, and duality makes the right actions free too.
For representatives `x,y,z`, define the quotient coefficient by summing
the original coefficients over the left orbit of `z`.

Changing `x` to `g*x` translates the product on the left. Changing `y` to
`g*y` does the same because `x*g=h*x` for an appropriate group element
`h`. Thus the coefficients are independent of representatives. The orbit
relations form a two-sided ideal, so associativity descends. Duality also
descends because right and left orbits agree.

The total coefficient of invertibles in `x*y` counts group elements `h`
with `y=x^*h`. Freeness gives coefficient one exactly for dual orbits and
zero otherwise. In particular the quotient has the required normalized
unit pairing. Frobenius reciprocity can also be checked explicitly:

```
sum_g N_(x,y)^(g z)
  = sum_g N_(y,z^* g^(-1))^(x^*)
  = sum_g N_(y,z^*)^(x^* g).
```

Since `x^*g` runs once through its left orbit, this is precisely the
quotient's cyclic Frobenius identity. The quotient is therefore a based
fusion ring. **No categorical quotient or de-equivariantization is asserted.**

For the two `u`-basis elements `A,B`, a product with a unit coefficient
has residual dimension `2u`; one without such a coefficient is a single
`u^2`-basis element. If `A^*=B`, cyclic reciprocity gives
`[AB:A]=[B^2:B]=0` and `[AB:B]=[A^2:A]=0`, a contradiction. If both
are self-dual, the same reciprocity forces `A^2=1+2A` and `B^2=1+2B`.
Positivity lifts the required orbit closure back to the original ring,
again producing the rank-ten subcategory.

## The rank-ten obstruction and order-seven case

The free orbit allows a self-dual noninvertible representative. Its right
action exponent must square to one modulo five. The negative exponent
forces five equal multiplicities summing to two and is impossible. The
positive exponent leaves either a rank-two subcategory with coefficient
two, or the symmetric pair of nonzero coefficients described in the proof.

Ostrik's rank-two classification excludes the first option for arbitrary
complex fusion categories; no pivotality assumption is needed. Source:
*Fusion categories of rank 2*, main theorem,
<https://arxiv.org/abs/math/0203255>.

For the second option, the character and its formal codegree are correctly
normalized. Independently eliminating the character variables gives

```
f^4 - 55 f^3 + 1000 f^2 - 7250 f + 18125.
```

Its reduction modulo two is irreducible, so it is the minimal polynomial.
The prime 29 divides its constant term but not its trace coefficient.
Equivalently `55^4 mod 18125 = 15625`. This violates the formal-codegree
d-number condition. Ostrik's theorem applies to arbitrary multi-fusion
categories; the relevant statements are Theorem 1.2 and Lemma 2.7(v) in
*On formal codegrees of fusion categories*,
<https://arxiv.org/pdf/0810.3242>.

Finally, equality in the Galois Gram bound for seven invertibles forces
all nonintegral dimensions to be positive integer multiples of `7+5*sqrt(2)`.
The two possible square partitions of seven are complete. The profile
with only three objects of the smaller dimension contradicts the free
seven-element orbit forced by the dimension equation for `XX^*`.

The result is thus a restriction on **all** Morita partners. It leaves
the one-invertible branch and the seven-invertible profile open, and proves
no associator existence for either candidate fusion ring.

## Exact independent check

Run:

```sh
python evidence/r3472_focus_20261022/review/verify_morita_independent.py
```

The receipt records the reviewed manuscript and verifier hashes, the source
tensor hash, the independent all-type order-five enumeration, and the
independent polynomial elimination. It imports no code from the author's
verifier. The final mathematical proof is the expanded manuscript, not the
finite arithmetic receipt alone.
