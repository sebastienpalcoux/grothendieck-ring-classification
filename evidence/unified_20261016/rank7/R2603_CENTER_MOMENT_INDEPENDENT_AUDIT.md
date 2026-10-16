# Independent audit: the R7_4_2603 full-character moment obstruction

**Status: PASS for the general complex-category exclusion.**

Auditor: two_dimension, 2026-10-16.

I read the complete `R2603_CENTER_MOMENT_PROOF.md`, the standalone
source-bound verifier, its certificate, and the exact helper routines
imported from `verify_quadratic_center_trace.py`. I independently ran
the standalone verifier under Python `-O`; the receipt is
`R2603_center_moment_independent_optimized.json`.

## Categorical scope and transport

The previously audited dihedral Morita reduction produces a category
with precisely two Frobenius--Perron dimensions. Schopieray's published
Galois pseudo-unitarity theorem applies to that category, and Morita
invariance carries the pseudo-unitarity conclusion to a Galois
conjugate of the hypothetical source. Thus the proof is not limited
to unitary or initially pivotal categorifications.

The seven displayed characters are distinct and satisfy every source
product. The verifier also checks their formal codegrees and the
complete source Gram spectrum. The fields Q(sqrt(5)) and Q(sqrt(-2))
are disjoint, so the required cyclotomic automorphism may flip the
dimension field while fixing the five remaining characters.

The full signed row transport is verified against all seven
characters, not just the dimension character. Its dimension-codegree
ratios are exactly 9+4sqrt(5) and 9-4sqrt(5). The map is an integer
involution. Passing from a signed image to its uniformly positive
version is necessary; excluding mixed-sign images is valid. The
induced-unit support is preserved with positive signs and contains
the forced partner 1+Y+Z.

The new relative-moment pairing is valid without conductor saturation.
For the anomaly-free canonical center, the modular Galois twist rule
is theta_(pi_sigma A)=sigma^2(theta_A). Every square of a Galois
automorphism fixes a quadratic field K. Hence sigma^2 lies in
Gal(L/K), and normalized relative trace is invariant under it:

    t_K(sigma^2(theta^n))=t_K(theta^n).

This holds for every n. It does not assert equality of the individual
twists. Pairing aggregate row multiplicities remains valid when the
permutation on individual center simples has longer cycles, because
the signed row transport has order two and the relative moments are
constant around those cycles.

## The two induced-unit possibilities

The analytic reciprocity derivation is complete. The three
codegree-eight rows have irrational multiplicity sum two and exactly
one additional nonidentity invertible. They cannot contain X by
dimension. The two codegree-four rows must each contain X once,
because these are the only rows that can supply its total unit-row
multiplicity two. Their remaining integral part is a single
nonidentity invertible. The five invertible entries therefore have
multiset {g,g,g,a,b}.

Using f_F chi_E(v_F)=f_E chi_F(v_E), the P/U/V comparisons force
the P-row invertible to be g. Its C comparison forces equal Y,Z
multiplicities. For U or V versus a C row, the two possible real
parts have incompatible nonzero values (16 versus 8); thus both
vanish, and the irrational coefficient vanishes as well. This
forces both C-row invertibles to be g and forces each codegree-four
row to have two Y and two Z. The remaining a,b occur once each.
The C+/C- comparison then gives p_++p_-=2. The two displayed blocks
are exhaustive up to the stated row permutations.

The independent finite replay gives the same result: 50 bounded
Gram/transport-compatible blocks, 48 excluded by all character
assignments, and exactly the two analytically derived survivors.

## Independent derivation of the arbitrary-root moment hull

Let K=Q(sqrt(5)) and u_e=(-1+e sqrt(5))/4. For a primitive root of
order 5^b m with 5 prime to m:

* If b>=2, both relative moments vanish. The rational Ramanujan sum
  and the lifted primitive quadratic-character sum both vanish;
  squaring does not change the 5-adic exponent.
* If b=1, first separate the 2-part of m. For 2-adic exponents
  zero, one, and two, the basic moment pairs are respectively
  (u_e,u_-e), (-u_e,u_-e), and (0,-u_e), allowing either e.
  The odd part multiplies both moments by q=mu(m_odd)/phi(m_odd).
  That scalar lies in [-1/2,1]. The six basic pairs and their
  negative halves therefore contain every such moment pair in
  their convex hull. Higher 2-adic exponent gives zero.
* If b=0, both relative moments are rational. The odd-part
  Ramanujan ratio has the same bound, while 2-adic exponents
  zero, one, and two give (q,q), (-q,q), and (0,-q).
  These are contained in the five rational vertices in the proof;
  higher exponent gives zero.

This proves the seventeen-vertex hull for all possible root orders.
It is not a bounded-order search. The code's coordinate list matches
these pairs, including the signs of the second moment in the
primitive-order-ten and primitive-order-twenty cases.

## Arithmetic and the exact contradiction

The algebraic-integer test uses the full maximal order
Z[(1+sqrt(5))/2]. The two doubled coefficients of D/z are required
to be integral with equal parity, so half-integral possibilities are
retained. The 465 global rows are a necessary superset bounded by
the full source Gram matrix. The principal-inverse and range tests
are exact necessary conditions for subtracting a rank-one positive
semidefinite contribution; the Galois partners must satisfy them
as well. No actual row can be discarded by these tests.

The second-indicator vector is forced. In particular the canonical
palindromic form on Y* X Y has sign nu_2(X), and its unit occurs
once because XY=Y+Z. Thus nu_2(X)=+1 even though Y is not
self-dual. The pointed indicators are positive in the integral TY
subcategory, while Y,Z have indicator zero. The sign helper derives
the same vector by its sandwich and odd-power equations.

The two induction trace identities and the residual Gram identity
have the correct normalizations and signs. Every actual center
contributes a nonnegative combination of the 45-entry columns.
The common moment pair on each Galois row pair is justified above.
The verifier clears all hull denominators by eight and checks every
integer dot product against the one displayed covector.

The independent optimized replay reports:

    tensor SHA-256:
    c54217eea35774c032df716ad15fdda9c4a93a4e2ebebd5893bd57a4aa63a5a2
    residual paired row types: 72 and 76
    moment columns: 1224 and 1292; union size 1292
    minimum column dot product: 12 in both branches
    prescribed target dot products: -1336 and -1240

Thus neither target belongs to the nonnegative column cone. The
contradiction is exact and excludes pseudo-unitary categorification;
the initial Morita/Galois bridge proves the claimed general complex
exclusion. No gap was found.
