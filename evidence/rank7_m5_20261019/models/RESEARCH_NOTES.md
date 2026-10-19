# Model search and unresolved leads

This note separates exact model evidence from exploratory comparisons. It is
not an additional categorification certificate. The authoritative final
classification is the rank-seven M5 ledger, which incorporates exclusions
obtained after some of these comparisons were made.

## Exact positive model

`R7_5_5678` is the representation ring of `C7 semidirect C6`, with the
faithful action of C6 on C7, equivalently `AGL(1,7)`. The independent checker
`verify_frobenius42.py` constructs all seven irreducible characters, checks
their 49 inner products, reconstructs all 343 fusion coefficients exactly,
and compares the full tensor with the pinned original source. The
model-to-census permutation is `(0,1,4,6,3,2,5)`.

The dimensions are six copies of 1 and one copy of 6. This is the maximal
near-group ring `NG(C6,5)`. It has a unitary complex representation category;
all weaker existence columns consequently have affirmative certificates.
No further exact model identification was established by this search.

## Near-group center comparison over Q(sqrt(15))

Put `s = sqrt(15)` and `d = 3+s`. The rank-seven tensors
`R7_5_443`, `R7_5_1214`, and `R7_5_5131` have the dimension multiset

`1, 1, 4+s, 4+s, 5+s, 5+s, 2d`.

Their global dimension is `240+60s`. A near-group category `NG(C6,6)`
has global dimension `30+6s`; hence

`(30+6s)^2 / 6 = 240+60s`.

This arithmetic coincidence points toward the centers studied by
E. C. Rowell, H. Solomon, and Q. Zhang, *On near-group centers and
super-modular categories*, [arXiv:2305.09108](https://arxiv.org/abs/2305.09108).
That paper constructs, from the C6 near-group center, a rank-ten
super-modular category with dimension multiset

`1, 1, 4+s, 4+s, 5+s, 5+s, d, d, d, d`.

It has the same global dimension as the three rank-seven tensors, but its
rank and simple dimensions differ. Thus it is **not** an exact tensor
identification. Its fermion acts freely on the simple objects, whereas the
nontrivial invertible of `R7_5_443` fixes the dimension-`2d` object.
An algebra or other categorical construction realizing one of the
rank-seven tensors was not established. Equal dimension and equal number
field do not provide such a construction.

`R7_5_5131` was subsequently excluded by the pipeline's complete
character-aware induction test. The comparison above records the research
lead, not a surviving status for that ring. The other two cases remain
subject to the final ledger.

## Other searches and scope

The integral profiles were checked exactly against all dimension
equations. Six are excluded by `integral_codegrees.py`, and the noncyclic
maximal near-group tensor `R7_5_4812` is excluded by
Nikshych--Ostrik, Appendix Theorem A.14(ii) in
[arXiv:1309.4822](https://arxiv.org/abs/1309.4822). The latter theorem has
the required general group scope; Siehler's abelian near-group result is
not the justification for this noncommutative example.

No general theorem allowing one to infer solvability merely from simple
dimensions in `{1,4}` was found applicable to the proposed Morita-dual
profile `(1^12,4^27)` of `R7_5_4982`. Such a dimension profile by itself is
not a model, and no categorification is claimed here.

For `R7_5_4653`, writing `d=13+sqrt(165)` gives dimensions
`1,d-1,d,d,d,d,d`. The five induced-unit columns with codegree 11 must
have unit coefficient 1, coefficient 3 on the dimension-`d-1` object,
and coefficients summing to 11 on the other five objects. These necessary
conditions alone do not contradict the induction Gram matrix: one may
take those five coefficient vectors to be `2*(1,1,1,1,1)+e_i` and the
remaining nontrivial induced-unit column to be
`(1,14,14,14,14,14,14)`. The residual Gram matrix is positive semidefinite.
This is a failed obstruction attempt, not a realizable induction functor.

`survivor_numerical_profiles.json` records exploratory numerical profiles
of an early survivor set. It is not an exact proof or final status list.
The dimension-220 files record an unused longer alternative argument;
the accepted exclusion of `R7_5_4757` uses the shorter cyclic-isotypic
obstruction in the main classification evidence.
