# A general scope gate for the two noncommutative residual rings

**Proposition.** Every complex fusion categorification of R8_3_721 or
R8_3_1154 admits a spherical structure and has a pseudo-unitary Galois
conjugate. Consequently a pseudo-unitary noncategorification obstruction for
either fusion ring excludes every complex categorification of that ring.
The proposition neither constructs a category nor asserts unitarity.

The source-bound finite certificate is `general_galois_pu_gate.json`, replayed
by `general_galois_pu_gate.py`. Its primary path incorporates the independent
unrestricted enumerator `../review/verify_nc_gate_unrestricted.py`. It uses
the existing canonical sphericalization framework, with a new complete
calculation for these two noncommutative tensors. Neither commutativity nor
positive-second-indicator normalization is imposed in the primary proof.

## Complete character and codegree accounting

For each source tensor the complexified fusion algebra is C^4 plus M_2(C).
The common kernel of every commutator in the regular representation consists
exactly of the four scalar summands. Indeed all commutators vanish there;
on the standard M_2 module their common kernel is zero. The verifier checks
invariance of this kernel, its dimension four, the simultaneous polynomial
coordinates of all eight multiplication operators, and the character
multiplication identities. A separating element has a square-free degree-four
polynomial, so its four roots give all one-dimensional algebra maps.

A spherical dimension function is a one-dimensional algebra map even when
the fusion ring is noncommutative. The matrix block therefore cannot provide
an unexamined dimension character. It must nevertheless be included in
formal-codegree obstructions. In the regular Casimir spectrum the matrix
block contributes eigenvalue 2 f with multiplicity four; the implementation
checks this complete factor and uses f, not 2 f, as its formal codegree.

For R8_3_721 the two rational scalar characters have a zero simple dimension.
For R8_3_1154 one rational character has a zero simple dimension and the other
violates the formal-codegree norm divisibility condition. In both cases the
only ordinary spherical-character orbit left is exactly the quadratic FP
orbit, as checked against the unique everywhere positive character.

## Complete sphericalization branches

Let C be an arbitrary hypothetical categorification. Its canonical
sphericalization has the sign object epsilon of dimension -1 and two lifts
of each simple. Choose dual-compatible lifts. A lift of a self-dual simple stays
self-dual: its dual has the same nonzero spherical dimension, whereas its
opposite lift has the negative dimension. Passing to epsilon=-1 gives a
signed tensor T on the eight original labels.

Its coefficients satisfy |T_ij^k| <= N_ij^k and T_ij^k congruent to N_ij^k
modulo 2. Cyclic trace symmetry and dual reversal hold; ordered associativity
holds without requiring T_ij^k=T_ji^k. The primary calculation uses every
integer in the full parity interval; it does not use any modulo-four
restriction or Frobenius-Schur indicator normalization.

The exact ordered enumeration gives:

| Ring | Variables | Search nodes | Complete signed tensors | Gauge-original tensors | Other tensors |
|---|---:|---:|---:|---:|---:|
| R8_3_721 | 51 | 6871 | 64 | 64 | 0 |
| R8_3_1154 | 53 | 7340655 | 288 | 64 | 224 |

The 224 nongauge tensors for 1154 form five sign-gauge orbits, of sizes
64,64,32,32,32. Changing dual-compatible basis signs is a trace-preserving
star-algebra isomorphism; it preserves formal codegrees, squared-dimension
sums and zero/duality obstructions. Thus it is enough to check one
representative of each fully enumerated orbit. Every such representative
has exactly four scalar characters and one two-dimensional block. Each of
its scalar-character factors is excluded by
a zero dimension or a formal-codegree norm obstruction. The codegrees of
both R and T are tested, including their matrix blocks. This is necessary:
the sphericalization has dimension 2 delta, and its two sign sectors have
formal codegrees 2 f_E(R) and 2 f_E(T). The induced-unit theorem therefore
requires delta/f to be an algebraic integer for every such f. The displayed
norm witnesses are exact necessary consequences of that integrality. They
do not assume the hypothetical category is pseudo-unitary.

All possible signed quotients are thus gauge-original. The certificate gives
dual-compatible signs s_i, s_0=1, and checks all 512 identities
T_ij^k=s_i s_j s_k N_ij^k. Switch the chosen lifts by these signs. The new signed
tensor is exactly N. Since its positive and negative lift multiplicities
sum to N and differ by N, every negative lift multiplicity is zero. Hence
the chosen eight lifts form a spherical fusion subcategory. Forgetting lifts
is a tensor equivalence of that subcategory with C: it is bijective on
simple objects and is fully faithful on their Hom spaces. This proves the
existence of a spherical structure on C.

Its dimension character must now lie in the sole surviving FP Galois orbit.
Fusion categories and their spherical structure can be defined over an
algebraic number field. Choose a Galois automorphism sending that character
to the positive FP character. The resulting spherical category has all
simple dimensions equal to FP dimensions and is pseudo-unitary. The fusion
tensor is unchanged by this conjugation. This proves the proposition.

## Replay and limitation

```sh
python evidence/rank8_frontier_20261021/central_integrality/general_galois_pu_gate.py
python -O evidence/rank8_frontier_20261021/central_integrality/general_galois_pu_gate.py
```

The checker exhausts the unrestricted signed domain anew, with all ordered associativity
equations and explicit overflow checks in the generated finite enumerator.
It does not infer general scope from a failed bounded search, an unproved
pivotality assumption, or a putative equality of integral and unitary
categorification. At present this is a conditional scope reduction for the
remaining necessary-condition searches, not an exclusion of either ring.

For comparison, the separate positive-indicator normalization yields four
signed tensors for 721 and sixteen for 1154, with the same conclusion. This
smaller calculation is replayed as a cross-check but is not needed for the
unrestricted proof.
