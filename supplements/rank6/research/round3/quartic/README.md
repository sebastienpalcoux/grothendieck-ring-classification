# Third continuation: quartic fields and commutative signed sectors

## Exact commutative-sector exclusions

The release implementation is `software/round3_commutative_sector.py`.
It does **not** assert that a noncommutative source ring has only commutative
signed quotients. It exhausts precisely the commutative sector, for use as
one component of the separate noncommutative signed-spectrum argument.

Starting from `oriented_signed.problem(R, normalized=False)`, impose
`T[i,j,k] = T[j,i,k]` on all coefficient variables. Each resulting variable
class receives the intersection of the original full signed domains;
a class identified with a zero coefficient receives the singleton zero
when parity permits it. Representatives are selected before their other
class members in the native search order. The original exact associativity
polynomials remain unchanged. Thus this is an exhaustive sector enumeration,
without fixing any second-indicator signs.

| Input | Oriented variables | Commutative variables | Complete tables | Sign orbits | Character rejections |
|---|---:|---:|---:|---:|---:|
| R6_7_200 | 30 | 24 | 176 | 11 | 27 |
| R6_8_491 | 30 | 24 | 208 | 13 | 53 |

The original formal codegrees are the two roots of
`x^2 - 1560*x + 1872` and the two-dimensional block's formal codegree `12`.
The regular Casimir eigenvalue of that block is `24`, so directly treating
that eigenvalue as a formal codegree would be incorrect. The implementation
reconstructs the normalization with `oriented_extension.linear_data`.

For every commutative signed table, all one-dimensional character components
are reconstructed. A dimension character must be nonzero on every simple,
equal on dual pairs, and satisfy the global-dimension/formal-codegree norm
integrality conditions. The first input has 11 zero-dimension, 5 duality,
and 11 norm rejections. The second has 27 zero-dimension, 13 duality,
and 13 norm rejections. The norm obstructions occur at primes 3 or 13.
No character-field obstruction is needed for these two applications.

The two `*_comm_certificate.json` files are complete exact certificates.
The `*_comm_values.txt` and `*_comm.cpp` files preserve the exploratory native
outputs. Their source and output digests are in `*_comm.json`.
`nc_comm_replay.json` records optimized-Python replay with numerical optimizer
entry points disabled, and mutation controls removing a table, removing a
sign orbit, and substituting 24 for the formal codegree 12. All controls pass.

A successful commutative-sector certificate is **not** a general exclusion
by itself. The root release combines it with the independently proved
noncommutative signed-spectrum and saturated-sign arguments.

## Quartic frontier relaxations

The surviving multiplicity-four cases R6_4_22 and R6_4_91 were tested against
stronger necessary systems:

1. Coupled Galois multiplicities, transforming center joint spectra by
   `sigma` and relative twist-trace types by `sigma^2`.
2. Nonnegative low-center Verlinde coefficients and compatibility of every
   low-center product with its restriction to the original ring.
3. Integer multiplicities for high restriction/twist types, low-center
   fusion coefficients, and aggregate high-product coefficients.
4. For R6_4_91, the Ising subcategory's support constraint: a central simple
   whose restriction contains the Ising object must have twist satisfying
   `theta^8 = -1`.

The Ising constraint follows from `nu_8(sigma)=-sqrt(2)` and positivity in
the central indicator formula: a positive weighted average of unit-modulus
numbers equals -1 only when every term equals -1. The Ising indicator is
obtained from the Tambara--Yamagami formula, e.g. Shimizu,
*Frobenius--Schur indicators in Tambara--Yamagami categories*,
https://arxiv.org/abs/1005.4500, and the central-indicator formula is in
Ng--Schauenburg, *Frobenius--Schur indicators and exponents of spherical
categories*, https://arxiv.org/abs/math/0601012.

Both low-character labellings of each ring survive these strengthened
height-three systems. The four `*_witness_2.json` / `*_witness_3.json` files
contain rational vectors whose exact substitution into every constructed
integer equation was checked. Their high multiplicities give formal full
induction Gram decompositions of ranks 36 and 42, respectively. They are
**feasible necessary relaxations**, not complete center fusion rings,
modular data, or categorifications. R6_4_22 also survives the height-six
cyclic-rotation refinement (`R6_4_22_h6.json`).

The smallest-case agent subsequently checks the R6_4_91 witnesses against
additional exact third-indicator equalities; see
`research/round3/smallest/R6_4_91_previous_witness_indicators.json` and the
subsequent replay reports there. Their third indicators on objects 1, 2,
and 5 are all exactly 1.

## Higher ambient field

R6_6_1035 has FP field `Q(sqrt(3),sqrt(5))`, requiring ambient conductor 60
in this approach. The exact initial low-stage audit in
`audit_1035_lows.json` reconstructs all 12 low frames; exactly two admit
character labellings. The larger higher-moment probes use a 890-second
external limit and remain exploratory. A log without a completed branch
record supplies no exclusion or feasibility conclusion. The half-E6
subcategory motivates a twelfth-root support constraint; its exponent is
12 in Hong--Rowell--Wang, *On exotic modular tensor categories*,
https://web.math.ucsb.edu/~zhenghwa/data/research/pub/exotic-08.pdf.
