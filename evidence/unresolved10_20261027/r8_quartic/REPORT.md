# Individual theoretical retry: R8_3_928 and R8_3_941

Research date: 27 October 2026 (Asia/Shanghai).
Source revision: `6a426acf6465dd674351be92dcca41b72f371521`.

**Outcome:** neither ring is categorified or excluded by this retry. No change
to either unresolved status is justified. The useful additional result below
is a short, enumeration-free reduction of the integral-center argument and
its uniform obstruction to group-based constructions throughout the Morita
class. This is not advertised as a new theorem in the literature.

## 1. Exact individual inputs and surviving gaps

Put

\[
a=2+\sqrt2+\sqrt3+\sqrt6,\quad
b=2+2\sqrt2+\sqrt3+\sqrt6,\quad
c=3+2\sqrt2+2\sqrt3+\sqrt6.
\]

Both rings have global FP dimension

\[
D=2(1+a^2+b^2+c^2)
 =144+96\sqrt2+80\sqrt3+56\sqrt6.
\]

For **R8_3_928**, the dimension vector in the supplied basis is
`(1,a,a,b,b,c,c,1)`. Its nontrivial invertible is `g=X7`, acting freely as
`(0 7)(1 2)(3 4)(5 6)`. The already established central lift is a semion or
antisemion. The pointed associator is nontrivial. The complete conditional
module theorem says that every indecomposable module category is regular;
all Morita partners are therefore tensor equivalent to the original category.
Its four surviving necessary center phase patterns are 40, 49, 186, 191.
None is an actual modular category or a categorical construction.

For **R8_3_941**, the dimension vector is `(1,b,b,1,a,a,c,c)`. Here `g=X3`,
acting freely as `(0 3)(1 2)(4 5)(6 7)`. Its unique central lift is a fermion.
The pointed associator is trivial, so `1+g` is a genuine separable algebra.
Its four-simple right-module category is not an ordinary rank-four tensor
quotient: fermion condensation supplies a superfusion category. The fourteen
surviving center allocations are 8, 19, 21, 31, 34, 43, 45, 56, 60, 72, 73,
77, 79, 85. The conditional nonpointed Morita route from R6_8_1660 to this
ring still requires an algebra whose existence has not been established.
The guaranteed `1+g` algebra gives a different rank-eight dual and does not
provide that route.

For both rings every nonpointed simple generates the entire fusion ring;
the only proper nontrivial based fusion subring is `{1,g}`. Their adjoint
closures are the full rings. The accompanying short exact verifier checks
these statements directly, together with all dimension-character identities.

## 2. A short integral-center lemma

**Lemma.** Let C be a fusion category with the following properties:

1. C_ad=C.
2. Its integral objects have underlying objects supported on `1,g`, where
   g is an invertible involution acting freely on every simple of C.
3. The object g has an invertible central lift G in Z(C).

Then the only integral simple objects of Z(C) are `1,G`.

**Proof.** The forgetful tensor functor F:Z(C)->C preserves FP dimensions.
Thus an integral central simple Z has F(Z)=a·1+b·g. For each simple X, the
two summands of F(Z) tensor X have supports X and gX, which are distinct.
The half-braiding of Z with X consequently preserves those two summands:
there are no cross-block morphisms. The same applies to arbitrary objects
by additivity. The projections onto a·1 and b·g are therefore morphisms in
the center. Simplicity forces one of a,b to vanish.

It remains to understand central objects with underlying object n·1.
Identify their half-braiding with a simple X with an invertible matrix T_X
on the multiplicity space. Naturality and the half-braiding hexagon imply
T_Y=T_X T_W whenever Y is a constituent of X tensor W, with a consistent
choice of product order. In particular T_{X*}=T_X^{-1}, and every constituent
of X tensor X* has matrix identity. Since C_ad=C, every simple has identity
matrix. Hence the central object is a direct sum of n copies of the central
unit. If F(Z)=n·g instead, apply this argument to Z tensor G^{-1}. Simplicity
then gives n=1. This also proves uniqueness of the lift of g. QED.

The free-action hypothesis in this proof is essential: it is what makes the
underlying pointed-isotypic projections central. No unproved assertion about
arbitrary integral tensor functors or arbitrary pointed supports is used.

For the present pair, condition 2 is immediate without any center enumeration:
all three numbers a,b,c have strictly positive coefficients of sqrt(2),
sqrt(3),sqrt(6). A nonnegative integral sum involving any of them cannot be
rational, because `1,sqrt(2),sqrt(3),sqrt(6)` are Q-linearly independent.
Conditions 1 and freeness follow directly from the source tensor. Condition 3
and its semionic/fermionic braiding type are the explicit inherited center
theorems, not conclusions of the present small calculation.

Consequently the entire integral part of the center is the semion category
for R928, and sVec for R941. The previously enumerated dimension-two central
column is ruled out conceptually by the trivial-kernel argument above.

## 3. Consequence throughout the Morita class

**Proposition.** No category Morita equivalent to a categorification of either
ring can be a nontrivial finite-group extension or equivariantization.

**Proof.** Any Tannakian subcategory Rep(H) of the center is integral. It
would have to lie in the integral subcategory identified above. A semion
category has no nontrivial symmetric subcategory; sVec has no nontrivial
Tannakian subcategory. Thus no nontrivial Rep(H) occurs.

A faithfully H-graded fusion category has a canonical braided embedding
Rep(H) into its center: a representation V has underlying object V tensor 1,
and its half-braiding with an object of degree h acts through V(h). Faithfulness
of the grading makes this central functor fully faithful. An H-equivariantization
also has its canonical central Rep(H), consisting of equivariant structures
on sums of the unit. Thus either construction with H nontrivial contradicts
the absence of a Tannakian subcategory. Braided equivalence of centers under
Morita equivalence transports this obstruction to every Morita representative.
QED.

This rules out the *last nontrivial step* in any proposed construction composed
only of finite-group extensions, equivariantizations, and Morita equivalences.
It does not rule out taking proper fusion subcategories, arbitrary connected
algebras in larger categories, or genuinely new associators. In particular it
is not a general categorification obstruction.

For arbitrary complex categorifications, apply the already established
spherical/Galois gate first. A Tannakian embedding transports through field
automorphisms; semionic self-monodromy stays -1 and a fermion stays fermionic.
Thus the argument is not restricted to unitary categorifications.

## 4. Other new routes examined and why they do not yet decide the cases

* **R928, quaternionic block and second indicators.** The g=-1 quotient is
  quaternionic. It is tempting to turn this into a forbidden negative second
  indicator of a distinguished central summand. But the relevant summand is
  in the negative monodromy sector. Every product X tensor X* has positive
  monodromy, so the usual odd-multiplicity parity obstruction is automatically
  vacuous on that sector. Moreover identifying the ring's involution type with
  a categorical indicator needs an additional categorical justification; it
  is not used here as a proved fact.
* **R941, signed quaternion quotient.** The split-quaternion quotient at g=-1
  has no scalar character. This does not prohibit a fermionic pivotal quotient.
  Inamura's precise convention has qdim(Pi X)=qdim(X), not its negative
  (equation (2.7)); the physically relevant dimension character uses g=+1.
  Thus imposing a g=-1 dimension character would create a false exclusion.
* **Both, ordinary zesting or associator twisting.** Their full adjoint closure
  leaves no nontrivial universal grading. Ordinary twisting along a group
  grading therefore cannot alter a known ring into either target. This does
  not address general super or para-associator constructions.
* **Both, the known E21 construction.** Its rank-eight neutral component is
  R8_3_982. Its established all-ranks Morita rigidity prevents direct Morita
  transfer to these two distinct rings. The common global dimension and common
  rank-four orbit quotient are insufficient to construct a tensor category.
* **R941, the R6_8_1660 link.** The 512-coefficient identification is genuine,
  but constructing or forcing the nonpointed algebra is still necessary.
  No existence equivalence follows from the identified possible dual ring.

## 5. Provenance and references

Inherited categorical inputs and full prior domains:

* `evidence/rank8_frontier_20261021/noncommutative_followup/README.md`
  (general sphericality and Galois-to-pseudo-unitary scope).
* `evidence/rank8_frontier_20261021/quartic_integer_center/source.json`
  (exact dimensions, distinguished characters, complete central domains).
* `evidence/rank8_research_20261022/r928_r941/PROOF.md`
  (unique central lift, semion/fermion type, no braided Morita representative).
* `evidence/unresolved_retry_20261024/proofs/unresolved11_20261024/rank8_quartic_pair/R928_MORITA_RIGIDITY.md`.
* `evidence/unresolved_retry_20261024/proofs/unresolved11_20261024/rank6_pair/RANK6_REPORT.md`.
* `evidence/unresolved_retry_20261024/proofs/unresolved11_retry_20261024/quartic/THEORETICAL_RETRY.md`.

Primary literature checked during this retry:

* R. Usher, *Fermionic 6j-symbols in superfusion categories*, Journal of Algebra
  503 (2018), 453–473, https://arxiv.org/abs/1606.03466 . Explains why forgetting
  parity does not turn the super pentagon into an ordinary pentagon.
* K. Inamura, *Fermionization of fusion category symmetries in 1+1 dimensions*,
  JHEP 10 (2023), 101, https://doi.org/10.1007/JHEP10(2023)101 , equation (2.7).
* D. Aasen, E. Lake, K. Walker, *Fermion condensation and super pivotal
  categories*, https://arxiv.org/abs/1709.01941 , Sections 4.1.3 and 6.1.
* C. Jones, S. Morrison, D. Penneys, J. Plavnik, *Extension Theory for
  Braided-Enriched Fusion Categories*, IMRN 2022, 15632–15683,
  https://doi.org/10.1093/imrn/rnab133 , Section 7.2, canonical Rep(G) in the
  center of a graded category. The categorical constructions needed above
  are also described directly in the proof.

No long enumeration, numerical pentagon search, or update to published
classification claims was performed in this retry.
