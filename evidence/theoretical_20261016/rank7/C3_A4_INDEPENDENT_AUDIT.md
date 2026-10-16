# Independent categorical audit of the C3–A4 reduction

**Categorical argument, based-ring classification, and source bindings: PASS in general-complex scope.**
The verified exclusions are `R7_2_236`, `R7_4_2167`, and `R7_4_2716`.
The fourth input, `R7_3_1022`, reaches k=4 and is not excluded by this argument.

An independent fresh execution of `verify_C3_A4_reduction.py`, including
all nine A4 ring checks and the original rank-seven census inputs, returned
PASS and reproduced `C3_A4_reduction_replay.json` byte for byte. Its SHA-256
is `1276f01124e769663a3d613a6240de2d8609a0ef71ed74545f8b92b046e743e4`.
All four source-tensor digests were independently recomputed from the current
rank-seven ledger and agree with that receipt. The condensed manuscript
`manuscripts/rank7/papers/c3_a4_morita.tex` preserves the audited categorical
hypotheses, normalization, and scope, including the unresolved k=4 case.

## First Morita transformation

The dimension-three fixed simple trivializes the pointed C3 associator.
The left and right regular-C3 algebra actions on its tensor square
preserve the isotypic component consisting of two copies of that simple.
A nontrivial projective C3×C3 class has irreducible degree three, so this
two-dimensional multiplicity space forces the trivial class. The resulting
nine invertible bimodules, together with the three from the pointed orbit,
give twelve invertibles in the dual category. The remaining orbit has
cyclic stabilizer and gives exactly three simples of dimension d.

The module dimensions are 1,1,1,1,d. The pointed dual fixes the unique
d-dimensional module, which trivializes its full associator. Its group K
acts transitively on the four dimension-one modules, with stabilizer L of
order three. If L were normal, the dual of Vec_K on this module would have
twelve simples, contrary to the original rank-four integral subcategory.
The only group of order twelve with nonnormal Sylow-three subgroup is A4.
Comparing rational and irrational terms of d²=4+md shows that the left
and right stabilizers of each noninvertible are its unique V4 subgroup H.

## Second Morita transformation

Among three noninvertibles one is selfdual. Duality exchanges the two H
actions and inverts their projective commutator. Since H has exponent two,
the alternating form is swap invariant, without a pivotal assumption.
In matched bases it is `[bJ,C;C,bJ]`, where C is symmetric. Changing the
H algebra by its nontrivial 2-cocycle adds `diag(J,J)`; the inverse twist
on the right has the same commutator in characteristic two.

The exact rank pairs, indexed by `(C00,C01,C11)`, are:

| Triple | Ranks for b=0,1 |
|---|---|
| 000 | 0,4 |
| 001 | 2,4 |
| 010 | 4,2 |
| 011 | 4,2 |
| 100 | 2,4 |
| 101 | 4,2 |
| 110 | 4,2 |
| 111 | 2,4 |

The zero-rank alternative would produce a simple with FP dimension d/4.
For m=6,8,12 its monic minimum polynomial has constant term −1/4, so
this is not an algebraic integer. Hence one algebra choice has rank two,
producing four degree-two projective representations over each of the
three noninvertibles, and therefore twelve simples of dimension t=d/2.
Transport by A4 preserves the H-cocycle class, so the block degree is
uniform across these three objects.

For either H algebra, the pointed dual has group A4. For the untwisted
algebra this is the Fourier dual of V4⋊C3. The other H-cocycle extends to
A4 via the binary tetrahedral central extension; its identity-on-objects
tensor autoequivalence of Vec_A4 identifies the two pointed duals. This
uses an autoequivalence of the pointed subcategory only and does not
assume that it extends to the full ambient category.

The free-orbit conclusion needs an explicit argument: rank-two blocks
alone would not suffice. For any new noninvertible Y, the equation
`FPdim(YY*)=t²=1+kt` forces exactly one invertible summand. Rigidity then
gives a trivial stabilizer. Thus the twelve invertibles act freely and
transitively on the twelve noninvertibles. This dimension argument repairs
the potential ambiguity from a rank-one cross block C.

## Normalizing the final quadratic ring

No initial self-duality assumption on the final twelve objects is needed.
Choose rho and write `rho g=theta(g)rho`. Freeness makes theta an
automorphism. The rational coefficient in `FPdim(rho²)=1+kt` gives a unique
invertible summand a, of multiplicity one. Comparing invertible terms in
`(rho²)g=rho(rho g)` proves `theta²=Ad_a`.

Write theta=Ad_sigma with sigma in S4=Aut(A4). Then a=sigma², because
both elements lie in A4 and its center is trivial. Replacing rho by b rho
changes sigma to b sigma and a to (b sigma)². Choose b=sigma^{-1} when
sigma is even, or b=tau sigma^{-1} when sigma is odd and tau is a
transposition. In both cases b lies in A4, and the new a is the unit.
The new rho is therefore selfdual. The only normalized actions are the
identity and conjugation by a transposition.

## Formal-codegree field obstruction

For the identity action, selfadjoint central N has coefficients a on the
unit, b on the three involutions, and c on all eight three-cycles. Thus
`k=a+3b+8c`. For k≤6, c=0. The cases b=0 contain the forbidden rank-two
fusion subcategory `rho²=1+k rho`. In the other k=3 case the degree-three
representations have irrational formal codegrees in Q(sqrt(5)), whereas
the FP dimension field is Q(sqrt(13)). In the other k=6 cases their formal
codegrees are `16±8sqrt(2)`, whereas the FP field is Q(sqrt(10)).

For the transposition action, twisted centrality identifies N with
A4-conjugacy-invariant coefficients on the odd coset of S4. Its two
classes have size six, so k=3,4 are impossible. For k=6 there are two
choices; their degree-three formal codegrees are again `16±8sqrt(2)`.

The required field containment is valid for **all complex
categorifications**, not only those supplied with a pivotal structure.
The precise scope bridge is Andrew Schopieray, *Categorification of
integral group rings extended by one dimension*, Journal of the London
Mathematical Society 108 (2023), 1617–1641, **page 1628, Lemma 3.1**, DOI
https://doi.org/10.1112/jlms.12789 . Its hypotheses require only that all
basis FP dimensions lie in {1,t}, with t>1. Its conclusion is that any
categorification is **Galois conjugate** to a pseudo-unitary category.
The original arXiv v1 has an incorrect stronger wording and is not the
version used here.

In that pseudo-unitary conjugate, the center constituent A_E associated
to a ring representation E satisfies `dim(A_E)=D/f_E`. This is Ostrik's
Theorem 2.13, restated immediately before Lemma 3.1 on the same published
page. Forgetting A_E expresses its dimension as an integer combination
of 1 and t. Hence every f_E lies in Q(t). The incompatible quadratic
fields above are therefore contradictions. This excludes k=3 and k=6.
The k=4 case remains outside the exclusion.
