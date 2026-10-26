# Fresh audit of the 24 inherited rank-12 exclusions

All 24 decisions are retained. `verify_lower_transfers.py`, freshly run
under optimized Python, verifies the six source proofs below and binds
every inherited decision to an exact dual- and product-closed based
subring of its original rank-12 tensor. The concrete receipt is
`lower_transfers.json`. No old artifact was changed.

| Excluded source | Rank-12 input suffixes |
|---|---|
| R10_1_118 | 281, 283, 291, 293, 455, 456, 460, 461 |
| R10_1_122 | 298, 300, 462, 464 |
| R10_1_180 | 533, 535, 605, 606 |
| R6_1_12 | 589 |
| R6_1_13 | 349, 590 |
| R8_1_17 | 450, 546, 547, 548, 613 |

## Arbitrary complex scope of the Liptrap sources

Liptrap, *Generalized Tambara–Yamagami categories*, Theorem 4, is an
equivalence between all fusion systems on the feudal fusion rule and
the displayed überderivation data over the original field. This is a
complete parametrization over C; it is not a classification restricted
to unitary associators, nor merely a construction of some solutions.
The exact feudal parity, common abelian stabilizer, and the entire
source multiplication are checked again.

For R10_1_118, R10_1_122 and R10_1_180 respectively, there are 4, 2 and 2
nondegenerate symmetric stabilizer bicharacters, hence 16, 4 and 4
assignments to the two lords. Every assignment has a checked integer
combination of the necessary multiplicative identities in which all
formal Laurent exponents cancel and a nontrivial root of unity remains.
All chi, upsilon and normalized tau variables are arbitrary nonzero
complex numbers. The identity for normalized tau follows by rescaling
the defining tau by sqrt(|H|); it restricts neither its absolute value
nor its phase. The conclusions do not depend on failure of a finite
phase search. Fresh replay reuses the previously independently written
and now reread Laurent verifier, not the discovery solver.

Primary source: <https://arxiv.org/html/1002.3166v2>, Definition 4.3 and
Theorem 4.

## The two rank-six field and order obstructions

The full positive dimension character is independently verified using
polynomial quotients and strict rational isolating intervals. There
are exactly two FP values in each source. The applicable general-scope
bridge is published Schopieray Lemma 3.1: such a fusion category has a
pseudo-unitary Galois conjugate. We apply the center obstruction to that
conjugate, which has the same integer based ring. We do not assume the
original category to be pseudo-unitary or unitary.

For R6_1_12 the dimension field is defined by t²−12t+18, whereas an
actual Casimir factor is t²−15t+45. Their discriminant ratio 5/8 is not
a rational square. In a pseudo-unitary categorification each formal
codegree is D/dim(A_E), and hence belongs to the dimension field because
forgetting A_E is an integer sum of the original simples. Multiplying
a formal codegree by its integer representation degree does not change
that containment. Thus the exhibited Casimir eigenvalue is impossible.

For R6_1_13 the ring is commutative, so each representation degree is
one. With its actual nontrivial FP value d, the global dimension is
6+9d. The actual codegree 6 requires a forgotten center object of
dimension 1+(3/2)d, outside Z+Zd. The exact obstruction is independently
recomputed in the basis (1,d); it does not depend on the coordinate
basis used by the earlier Hermite-normal-form certificate.

Primary sources: Schopieray, published Lemma 3.1,
<https://doi.org/10.1112/jlms.12789>; Ostrik, Theorem 2.13,
<https://arxiv.org/html/1309.4822v1>.

## R8_1_17: all oriented signs and all spherical dimensions

For an arbitrary complex category take its canonical sphericalization.
Each simple has two lifts of opposite nonzero dimensions. Choose lifts
compatible with duality: this is possible for nonselfdual pairs, and a
selfdual simple cannot have its chosen lift dual to the other lift,
since dual objects in a spherical category have equal dimensions.
The signed quotient by the negative lift of the unit consequently has
unit coefficients and dual pairings equal to +1. Oriented cyclic
reciprocity and reversal with duals impose precisely the six-element
orbits used by the verifier. No unoriented symmetry or commutativity
of lifts is assumed.

Every nonzero original structure coefficient is one; the corresponding
signed coefficient is therefore +1 or −1. The independent enumeration
checks all 2^13 = 8192 assignments, without the positive-indicator
restriction of an earlier implementation. Exactly 16 are associative.
Every one equals s_i s_j s_k N_ij^k for a dual-compatible basis sign
choice s. Changing the actual lifts by these signs makes every
nonzero coefficient positive. The chosen lifts then form a full tensor
subcategory of the sphericalization, equivalent under forgetting to
the original category. This proves actual spherical descent, not just
an isomorphism of signed rings.

For the resulting spherical category, dimensions are nonzero,
dual-compatible one-dimensional characters. A square-free separating
regular multiplication matrix has degree eight, and every multiplication
matrix is verified as a polynomial in it. Consequently its irreducible
factors give all character orbits, without omitted branches. The
quadratic orbit t²−124t+4244 and quartic orbit
t^4+180t³+10520t²+235944t+2869828 violate equality of dual dimensions.
The remaining quadratic orbit t²−256t+9184 gives global-dimension
norm 128. An actual formal-codegree factor is t²−24t+96, whose norm is
96. Divisibility of global dimension by every formal codegree would
force an algebraic integer with rational norm 128²/96² = 16/9 in a
common extension. Equivalently the prime-three valuation inequality
checked by the code is impossible. This excludes every spherical
dimension character and therefore the original arbitrary category.

The sphericalization and center statements used here are reviewed in
Ostrik, Sections 5.1 and 2.3 of the preceding primary source.

## Transfer and conclusion

For each of the 24 original tensors the receipt records the actual
subset of simples and complete unit-preserving basis permutation to
its source class. Product closure, dual closure and every structure
coefficient are checked anew. A hypothetical categorification would
therefore contain the corresponding full fusion subcategory, contrary
to its general-complex exclusion above. None of these transfers relies
on identifying an associator from its fusion ring or on a unitary-only
classification.
