# Three commutative rank-nine cases: theoretical continuation

Date: 27 October 2026. Source: public classification commit
`6a426acf6465dd674351be92dcca41b72f371521`.

This file records an individual investigation of `R9_2_137`, `R9_2_1607`
and `R9_2_1976`. The final result is **two new general-complex exclusions**:
`R9_2_1607` and `R9_2_1976`. `R9_2_137` remains unresolved, with every
large second indicator forced to $+1$ in its positive representative.

The complete new proof is `GALOIS_FS2_EXCLUSION.md`. It uses the
symmetric pairing on a multiplicity-one Galois summand of the canonical
central algebra, followed by the Morita-invariant weighted second
indicator. This is a global categorical argument that supplies the
missing restriction left open by the pointed cochain probes below.
The earlier quadratic-refinement conjecture remains unproved and is
not used. No online ledger or website files were changed.

## 1. Exact common structure and distinct cases

Put `d=4+3sqrt(2)` and `D=144+96sqrt(2)=16+32d`.
Each ring has dimension type `(1^4,2,d^4)`. Its integral subcategory in any
categorification is the nonalternating Tambara–Yamagami category on `V4`.
The existing theorem reduces arbitrary complex categorifiability to a
pseudo-unitary Galois representative, without changing the rational TY
parameter `tau=epsilon/2`.

| Case | Dimension-two object | Large objects | Self-dual large objects | Existing surviving TY signs |
|---|---:|---|---|---|
| R9_2_137 | 8 | 3,4,5,6 | all four | + and − |
| R9_2_1607 | 3 | 1,2,7,8 | 7,8 | − |
| R9_2_1976 | 5 | 1,2,3,4 | none | − |

Indices are zero-based. All large cubic invariant spaces have dimension
two. Existing source-local Clifford arguments give
`nu_3(X) in {-1,-zeta_3,-zeta_3^2}`. The positive-sign R137 branch and the
negative-sign R1976 branch have only the projected value `1/2` remaining
for every large object. This means an actual value in
`{-zeta_3,-zeta_3^2}`, not the number `1/2` itself.

The short verifier checks all dimension-character identities, exact source
hashes, dualities and cubic multiplicities. It performs no optimizer search.

## 2. A small arithmetic restriction on the necessary ninth-root sector

Work in the positive spherical representative. Let `Z` be a simple object
of the Drinfeld center whose twist has order divisible by nine.

Every invertible of the source lies in its untwisted pointed V4 subcategory
and has second indicator one. Positive saturation of the central-induction
formula therefore forces the twists of constituents of each `I(g)` to
satisfy `theta^2=1`. The TY object's eighth indicator is its dimension,
two, so constituents of `I(Y)` satisfy `theta^8=1`. Consequently `Z`
cannot restrict to an invertible or to `Y`. Its dimension is therefore
`B*d`, where `B` is the sum of its four nonnegative integral large-object
restriction multiplicities.

Modular formal-codegree integrality now gives

`D^2/(B*d)^2 = 1152/B^2` in the algebraic integers.

This is a rational number, so it is an integer. Thus

`B in {1,2,3,4,6,8,12,24}`.

For completeness, these are all possibilities: `1152=2^7*3^2`, so the
prime factorization of `B` has 2-adic valuation at most three and 3-adic
valuation at most one, and no other prime factors.

Square-Galois symmetry supplies at least three distinct central objects
of the same dimension in the orbit of `Z`: choose a Galois element fixing
the quadratic dimension field and the 2-primary roots while acting
nontrivially by a square on its primitive ninth-root part. The center's
normalization has anomaly one. Such an orbit contributes at least
`3*B^2*d^2` to `D^2`. Since the center also contains its unit, this yields
`3*B^2<1152`, eliminating `B=24` from this sector.

This restriction is insufficient to exclude any case. It is unsafe to
replace equal dimensions within the Galois orbit by equality of the full
restriction columns without a separate argument about the induction
labels. The present investigation does not make that replacement.

Primary inputs: Ng–Schauenburg, *Frobenius–Schur indicators and exponents
of spherical categories*, https://arxiv.org/abs/math/0601012;
Gannon–Morrison, *Modular data for the extended Haagerup subfactor*,
Section 3 and Lemma 3.1, https://arxiv.org/abs/1606.07165; Ostrik,
*Pivotal fusion categories of rank 3*, modular formal-codegree discussion,
https://arxiv.org/abs/1309.4822.

## 3. Historical exploration: duality coherence and second indicators

The following exploratory discussion is superseded for the final statuses by
`GALOIS_FS2_EXCLUSION.md`; its rejected shortcuts are retained to explain
why the global pairing argument was needed.

The parallel D8 investigation studies the genuinely additional requirement
that the pointed bimodule support the **specified duality permutation**.
This is stronger than checking only its left/right associativity cochain.
Its report and checker, once audited, are the authority for any removed
duality branch. This file does not duplicate a provisional proof.

The categorical opposite-bimodule formula used in that investigation is
confirmed directly by Vainerman–Vallin, *On Z/2Z-extensions of pointed
fusion categories*, https://arxiv.org/abs/1210.1732, Section 2.2.2 and
Section 3.1.1. In their `(s,t^op)` coordinates, the opposite uses
`(s,t^op) -> (t^-1,(s^-1)^op)` and inverts the cochain. In the present
`(g,k)` coordinates, acting by `g X k^-1`, this is precisely factor swap
and inverse cochain. Only this bimodule fact is used; these nonintegral
categories are not asserted to be faithfully Z2-graded.

Suppose the remaining D8 Morita dual has duality shift zero, so all four
of its large objects `X_q`, indexed by `Q=D8/Z(D8)=V4`, are self-dual.
There is then a useful exact target for a further proof. In the canonical
positive pivotal structures, Morita invariance of the weighted total
second indicator gives

`sum_q nu_2(X_q) = sum_{large X in the source} nu_2(X)`.

Indeed, the integral contribution on the source side is `4+2*epsilon`:
four invertibles with indicator one, plus the TY object of dimension two
with indicator `epsilon`. The pointed D8 dual has the same contribution:
the four objects in its even V4 subgroup contribute one each; the two odd
reflections contribute `epsilon`; the two order-four rotations have
second indicator zero. Each large object has dimension `d` on both sides,
so cancellation proves the displayed formula.

Consequently the remaining dual sign sums must lie in:

| Source | Required sum of four dual signs |
|---|---|
| R9_2_137 | `{-4,-2,0,2,4}` |
| R9_2_1607 | `{-2,0,2}` |
| R9_2_1976 | `{0}` |

The zero for R1976 is particularly rigid: its four large source objects
are all non-self-dual, hence each has second indicator zero. A proof that
the D8 signs form a nondegenerate quadratic refinement on Q would instead
give a Gauss sum of plus or minus two, and would finish this case. However,
the pointed 3-cocycle and the pivotal coherence must be included in such
a proof. The commutator pairing of D8 and the forced left/right central
anticommutator alone do not establish that refinement. At this checkpoint
the refinement is a proposed route, **not an accepted theorem**.

A complementary version considers the inverse Morita algebra on an even
reflection subgroup. The four large A-bimodules lie over two free orbits.
The opposite-bimodule cochain determines whether the two projective
character choices over each orbit are self-dual or paired. Relating these
two signs could determine which of the three source duality types actually
occurs. Character freedoms and pivotal coherence must be checked; a based
Morita completion is not sufficient.

The parallel exact pointed-module calculation has now tested this
complementary idea. Its induced module cochain and opposite equivalence
allow all three possibilities: zero, two, or four self-dual large inverse
Morita objects. Thus pointed associativity and opposite equivalence alone
do **not** rule out any of the three source duality patterns. This prevents
using the proposed sign argument as an exclusion without additional
pivotal or noninvertible coherence. The calculation is recorded by the D8
investigation in `../r9_noncommutative/probe_full_module.py`.

## 4. Construction attempts and limits

The SU(3)_5 global dimension matches D, but this route was already
rigorously excluded: its center has at least nine invertibles, while the
source center's invertibles inject into V4 and in fact form at most sVec.
No new progress is claimed from this dimensional coincidence.

The R6_4_155 fermionic product with Ising has the right global dimension,
but its surviving central semion is incompatible with the established
Vec-or-sVec pointed center. The rank-six investigation owns the detailed
scope of that construction obstruction.

An order-32 abelian near-group precursor and an isotropic order-four
quotient do not automatically realize the forced D8 pointed part. The
existing pointed-center obstruction and the rank bound for the algebra
`1+sum X_q` remain applicable. No unproved algebra existence is promoted
to a categorical model here.

Current outcome of this investigation: no complete case decision;
the source-specific second-indicator constraints and the independent
duality-coherence audit identify a smaller and more concrete target.
