# Fresh exclusion audit, rank 12 and multiplicity one

The 425 exclusions assigned to this audit remain supported over arbitrary
complex fusion categories. I found no false exclusion among them. This is
a fresh review of the categorical arguments and executable domains, followed
by exact replays; the previous PASS receipts were not used as evidence of
correctness. The parent independently reviews the other 13 assigned routes:
12 dimension-120 exclusions and R350. The 24 inherited lower-rank transfers
were subsequently assigned here and are detailed in `lower_transfers.md`.

The frozen baseline has 632 rings and 438 exclusions. Fresh code checks every
original physical input line against its permanent ID, complete tensor and
ledger digest, all fusion axioms, and all 4,012 saved subring embeddings.
No input, old artifact, repository or website was changed. Original checker
receipt writes were redirected under this new audit folder, and bytecode
writes were disabled.

## Route inventory and risk assessment

| Route | Assigned count | Main risk checked | Fresh conclusion |
| --- | ---: | --- | --- |
| Arithmetic / near-group | 234 | Casimir versus formal codegree; correct near-group hypotheses | Retain |
| Cyclic isotypic integrality | 113 | Actual compatible algebra actions, arbitrary original associator | Retain |
| Center field / dimension order | 12 | Genuine general-to-spherical bridge; exact positive dimensions | Retain |
| Primary-3 | 6 | Unitarizability of every hypothetical original category | Retain |
| Liptrap monomial obstruction | 4 | All complex parameters, rather than finite phase failure | Retain |
| Paired stabilizers | 16 | Actual stabilizer algebra and stable isotypic bimodule | Retain |
| Rep(S3)-rule Morita enlargement | 4 | No unproved classification of the original subcategory | Retain |
| Mod-four signed descent | 4 | Complete signed domain and actual spherical descent | Retain |
| Dimension-40 exhaustion | 6 | Every precursor, extension and relative cocycle class covered | Retain |
| Pointed bimodule stabilizers | 2 | Arbitrary pointed associators | Retain |
| Inherited lower-rank transfers | 24 | Complete source proofs and every embedded coefficient | Retain |
| **Total reviewed here** | **425** | | **No status correction** |

The 438-row `route_inventory.json` also identifies the 13 parent-reviewed
records. The distinction is audit ownership, not an additional classification.

## 1. Arithmetic: no mistaken use of commutativity

The regular central element is `sum_i b_i b_i*`. On an irreducible block of
degree `e`, its scalar is `e*f`, with regular multiplicity `e^2` and formal
codegree `f`. Its eigenvalues are d-numbers for any fusion category; Ostrik's
rank-three paper, Proposition 2.2, states this preliminary result without
restricting rank or imposing pivotality. Thus the Casimir test applies to the
noncommutative inputs as well.

The replay rebuilds this element from the tensor and uses prime valuations
of minimal-polynomial coefficients. There are 228 direct d-number witnesses.
The fresh supplemental checker confirms that every stored factor used in
this arithmetic step is genuinely monic and integral: 234 factors, including
the six integral-center witnesses. This removes any ambiguity from conversion
of polynomial coefficients to Python integers.

There are 15 irrational two-orbit divisibility witnesses. Transitivity of
the invertible action forces the same nonintegral dimension `d` on all
noninvertibles. Their square relation is `d^2=h+r*d`, with `h` the actual
stabilizer size. The checked nonsquare discriminant and `h` not dividing `r`
are precisely the hypotheses of published Schopieray Proposition 3.3.
The one small-multiplicity near-group witness has a commutative full tensor,
so the commutativity condition in Proposition 3.2 is met.

For integral input, weak integrality supplies pseudounitarity. Each
distinguished central simple forgets to a sum of integral-dimensional
objects. Therefore `e*D/lambda` must be an integer. A nonrational Casimir
root cannot satisfy this. For a rational root, the noncommutative test
exhausts all allowed degrees `e<=sqrt(m)` and every partition of the regular
multiplicity `m` into their squares. It does not silently replace every
irreducible degree by one. Four commutative and two noncommutative
integral-center witnesses pass.

## 2. Cyclic and paired stabilizers: the algebra really exists

If an invertible subgroup fixes a simple object, its action on the
one-object semisimple subcategory supplies a stabilizer two-cochain. The
module associativity equation says exactly that this cochain trivializes
the restricted ambient associator and defines a connected separable
twisted subgroup algebra. This is stronger than merely knowing that the
underlying direct sum is fusion closed.

For the cyclic test, the objects fixed on the left and right may initially
supply different cochains. Their ratio is a two-cocycle, and
`H^2(C_n,C*)=0` identifies their subgroup algebras. The tested `Z`-isotypic
block of `X tensor Y` is stable under both actions because every group
element fixes `Z` on the appropriate side. Its dimension in the actual
bimodule fusion category is `m*FPdim(Z)/n`, hence an algebraic integer.
The argument requires no spherical or unitary structure. All 208 saved
cyclic witnesses, including overlaps, were replayed; 113 are first routes.
Perron factors are isolated by exact rational intervals.

For the 16 new paired-stabilizer cases the right action is obtained by
dualizing the left action on `X`; thus `X tensor X*` uses the same algebra
without requiring the stabilizer group to be cyclic. Its entire
`Z`-isotypic block is again a bimodule. Every new case has a verified
order-four stabilizer, multiplicity one, and quotient minimal polynomial
`t^3-t^2-t/4+1/8`. Its nonintegral constant coefficient proves the required
contradiction. The fresh whole-input scan finds these same 16 new cases,
206 previously excluded cases, and no positive or currently unresolved case.

The stronger two-algebra square argument in the old notes is not needed
for any of these 16 decisions. Their paired formulation suffices, so the
decisions do not rely on matching unrelated noncyclic stabilizer cochains.

## 3. Center-field and order obstructions

All 12 first-round center-field/order records have exactly two positive FP
values. The relevant published Schopieray Lemma 3.1 gives a pseudounitary
**Galois conjugate**, without assumptions about rank, commutativity or an
original pivotal structure. The older preprint's wording that the original
category is pseudounitary must not be substituted for this result.

The new `exact_field_gates.py` independently verifies the complete dimension
characters as polynomial congruences, with strict positivity certified by
rational isolating intervals. It uses no `evalf` decision or original HNF
routine. Ten required Casimir factors generate a different quadratic field:
their discriminant ratio is not a rational square. The other two are
commutative and their distinguished center dimensions have nonintegral
coordinates in the actual lattice `Z+Z*d`. Both mechanisms pass exactly.

The field implication is valid even in the noncommutative case: Ostrik's
central induction theorem gives an object of dimension `D/f`; forgetting it
is an integral sum of source dimensions, so `f`, and then `e*f`, belongs
to the dimension field. An integer degree multiplier does not remove the
field obstruction.

## 4. The six primary obstructions have the necessary unitarity bridge

All six exact positive dimension vectors are integral and have total
dimension `216=2^3*3^3`. ENO Theorem 1.6 makes every categorification of
this dimension solvable. GHR Theorem 5.20 makes weakly group-theoretical
categories unitarizable. Both primary statements were checked directly;
the argument does not infer unitarity from pseudounitarity alone.

The primary matrix is `sum_i N_i tensor N_i tensor N_i / d_i`.
Independent integer contractions, with an explicit int64 overflow bound,
give the following exact negative quadratic values:

| ID suffix | Value |
| ---: | ---: |
| 91 | `-400108643/3` |
| 92 | `-400064978/3` |
| 197 | `-133398621` |
| 198 | `-399993005/3` |
| 220 | `-400019516/3` |
| 221 | `-133320942` |

No numerical eigenvalue or square-root approximation is needed to accept
these six witnesses.

## 5. Liptrap exclusions and overlapping controls

Liptrap Theorem 4 parametrizes fusion systems over the original field; its
statement does not assume unitarity. The checked tensors are genuinely
feudal, with the required common abelian stabilizer. Every stabilizer
character and every nondegenerate symmetric bicharacter is enumerated.
Every assignment to every noninvertible object is included.

The obstruction is an integer Laurent-monomial identity: all powers of
the arbitrary nonzero complex `chi`, `upsilon` and normalized `tau`
variables cancel, while a nontrivial stabilizer root of unity remains.
The normalization `sqrt(|H|)*tau` makes its dual-product relation one
without restricting its complex phase or magnitude. Thus no failed finite
root-of-unity search is being used as an arbitrary-complex exclusion.
The four direct and three transferred Liptrap source proofs replay exactly.

There are additionally ten accepted zero-spectrum witnesses, all overlapping
other routes. `overlap_controls.py` checks the direct Hom-space sums printed
in the theorem, rather than only the Frobenius-transformed formulas of the
old checker. They all pass. Six small involution-module control systems
also exhaust their full domains of 16–64 assignments. Their anti-invariant
module matrices retain every integer entry allowed by the multiplicity
and parity bounds; the right-regular matrix convention is used consistently.
The finite generator images reconstruct the entire algebra and every
multiplication identity is tested. Search limits do not truncate any
accepted negative domain.

One maintenance issue was found: the unused convenience entry point
`adapted_module.verify()` expects a noncommutative-specific certificate
kind, while the stored general wrapper uses `involution_module`.
The integrated original replay correctly calls `solve()` directly. The
new overlap checker verifies the stored wrapper, every returned metadata
field, and full exhaustion explicitly. This naming mismatch causes no
classification error; no old file was edited.

## 6. Four signed-sphericalization exclusions

For R63, R64, R215 and R365 the proof supplies actual spherical descent,
not just an associative signed table. In sphericalization, duality cannot
exchange the opposite-dimensional lifts of a self-dual original simple.
Tensoring by the sign object reverses its second indicator, so a positive
indicator lift can be selected. The canonical symmetric self-duality of
`Y tensor Y*` forces even multiplicity for negative-indicator self-dual
simples. Consequently the signed coefficient satisfies `N-T=0 mod 4`.
This argument is pivotal inside sphericalization and imposes no pivotality
on the original category.

Multiplicities are one, so each nonzero signed coefficient is a sign.
Associativity modulo four gives necessary linear equations over F2. The
independent code constructs all trace and duality orbits, the entire linear
system, and every kernel vector. There are respectively 2,2,4,16 candidates;
full integer associativity leaves 2,2,4,8. Each survivor is a verified
dual-compatible basis-sign gauge of the original nonnegative tensor.
Changing lifts by this gauge makes the selected simples closed under tensor
products, yielding a genuine spherical subcategory equivalent to the
original category.

The spherical character audit uses the full commutator-ideal quotient,
then an exact separating element. It includes every one-dimensional
character, even for the two noncommutative inputs. Zero or dual-incompatible
characters cannot be dimensions. Rational or cubic fields cannot contain
the necessary quadratic Casimir factor. The remaining quadratic orbit has
dimension lattice `Z+Z*d`, `d^2=8d+2`. The Casimir root 36 has regular
multiplicity one, so it is an actual degree-one formal codegree. Its
required center dimension is `2/3+(7/3)*d`, outside that lattice for both
embeddings. No character orbit is omitted.

## 7. The four C9 Morita exclusions

The original rank-three subcategory is used only through its rules
`gT=Tg=T`, `T^2=1+g+T`. The proof does not assume an equivalence with
a preferred realization of Rep(S3). For its actual algebra `A=1+g`, the
three simple module objects have equal dimensions. The sign-twist
invertible fixes the free module and exchanges the other two. If the
Morita dual contained a dimension-two simple, its module action would
have a row with total multiplicity two consisting of one fixed vertex
plus equal multiplicities on the exchanged pair: `1+2n=2`, impossible.
Thus that dual is pointed of dimension six.

The checked outside invertible normalizes the subgroup algebra and doubles
the pointed part to dimension twelve. Each free nonintegral C2 orbit has
two compatible bimodule characters, giving dual type `1^12,x^4,y^2`.
The exact dimension basis satisfies `y^2=6+2x+2y`, so any y-dimensional
simple has left and right stabilizers of order six. Their intersection
contains C3 and fixes both y-dimensional simples. One such simple appears
in `Y Y*` with multiplicity one or two. Paired-stabilizer integrality would
make `m*y/3` integral, whereas its norm is `-8*m^3/9`. Both possible
multiplicities fail. Every original-ring premise and both norms replay.

## 8. The dimension-40 converse is complete

This was the highest-risk inherited exhaustion argument. Its reduction
uses actual subgroup algebras, not a presumed known associator for the
integral subcategory. Every simple right `1+g` module in the integral part
has underlying dimension two. Its internal End has dimension two and
contains the unit; its other invertible must be g by the checked exact
underlying stabilizer. The right module itself is therefore fixed by g,
and `H^2(C2,C*)=0` gives the compatible left actions. The dual integral
subcategory is pointed of order twenty.

The reverse algebra has dimension two and lies in that pointed part.
The source invertible count forces its involution normalizer to have
order four. The elementary order-twenty group classification leaves
F20 or D10×C2. In the latter, each nonnormal double coset is inverse-stable
with trivial stabilizer; its unique simple is self-dual. Left/right
invertible actions agree and are involutions. Dual reversal then makes
every fusion product commute, for every allowable associator. The actual
eight relevant integral subrings are noncommutative, leaving F20.

The neutral adjoint category is Vec(C5), since a fixed noninvertible
trivializes its associator. Its Brauer-Picard group is the split orthogonal
group D8. The F20 quotient rotation acts with order four and a rank-one
component is a reflection. The grading group has order eight, so this
homomorphism is an isomorphism. This forces the D8 precursor grading
without any scalar-search completeness assumption. All inverse-algebra
involutions in F20 are conjugate, so their choice adds no omitted orbit.

The coprime extension theorem, ENO Theorem 9.5, makes the remaining
extensions an H3(D8,C*) torsor. Equivalently, all positive cohomology with
the C5² lower coefficient module vanishes. An actual base extension is
provided by the checked Liptrap data. Restriction/corestriction from an
index-two V4 proves that H3(D8,C*) has exponent dividing four. Every
class therefore lifts to fourth-root cocycles. The degree-three map on
the reverse C2 subgroup is injective because H2(C2,C*) vanishes; hence
requiring pointwise trivial restriction loses no admissible class.

The fresh exact cohomology replay gives relative cocycle kernel size
`2^87` and coboundary image size `2^83`: exactly 16 classes. All 16
representatives and all 120 pairwise inequivalences are checked. The
independent balanced-bimodule calculation reconstructs all 16 dual tensors;
they match only R156 or R263, with every coefficient tested. Thus all six
negative inputs are excluded by a complete converse. No bounded cocycle
scan is being mistaken for coverage of arbitrary complex associators.

## 9. The two D24 stabilizer exclusions

The source tensors have exact faithful C3 gradings with pointed neutral
part. ENO Theorem 6.1 makes each component an invertible bimodule category.
Galindo–Plavnik Corollary 7.11 applies to arbitrary pointed 3-cocycles and
requires its left and right stabilizers to be isomorphic. For R445 and
R493 their full multiplication tables give V4 and C4, respectively.
Their element-order lists differ. The gradings, transitivity, stabilizers
and element orders all replay; no untwisted pointed premise is inserted.

## Files, fresh replays, and reference boundary

- `inventory.py` and `route_inventory.json`: all input and embedding bindings.
- `exact_field_gates.py` and its receipt: fully exact replacement for the
  older floating positivity check and monic-factor validation.
- `overlap_controls.py` and its receipt: extra spectrum/module witnesses.
- `replay_readonly.py`: original independent replay routines, freshly read
  and run with `python -O`, with every receipt redirected to `replayed/`.
- `results.json`: the 425 retained decisions and the 13 delegated routes.

The reviewed original routines are `audit_all_exclusions`,
`stabilizer_square`, `audit_quadratic_signed`, `audit_c9_morita`,
`audit_d40_sources`, `audit_d8_cohomology`, `audit_d40_duals`, and
`audit_pointed_stabilizers`. They use explicit checks that remain enabled
under optimized Python. Reusing reviewed implementations is distinguished
from the new binding and field-gate implementations; this is not a claim
of proof-assistant formalization or independent human verification.

Primary theorem statements checked during this audit include:

- Ostrik, Proposition 2.2 and Theorem 2.13:
  <https://arxiv.org/abs/1309.4822>.
- Schopieray, published Lemma 3.1 and Propositions 3.2–3.3:
  <https://doi.org/10.1112/jlms.12789>.
- ENO, solvability Theorem 1.6:
  <https://arxiv.org/abs/0809.3031>.
- Galindo–Hong–Rowell, unitarizability Theorem 5.20:
  <https://people.tamu.edu/~rowell/GHRarx1.pdf>.
- Liptrap, Definition 4.3 and Theorem 4:
  <https://arxiv.org/html/1002.3166v2>.
- ENO, Corollary 1.2 and Theorems 1.3, 6.1, 9.5:
  <https://arxiv.org/html/0909.3140v2>.
- Galindo–Plavnik, Corollary 7.11:
  <https://arxiv.org/html/1407.2783v4>.
- Huang–Liu–Palcoux–Wu, primary criteria:
  <https://arxiv.org/abs/2210.00792>.

The remaining categorical constructions in the argument are proved above
or in the specified frozen notes and were checked with their actual
hypotheses. No unproved Isaacs or generalized unitarity conjecture is used.
