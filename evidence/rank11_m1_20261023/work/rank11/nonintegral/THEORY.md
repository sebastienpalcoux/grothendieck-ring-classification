# Rank-eleven nonintegral exclusions

Research calculation, 23 October 2026. All identifiers retain the physical line
number and tensor basis in the supplied rank-eleven multiplicity-one census.
This note gives uniform applications and refinements of the project's center
restriction methods. It does not claim that the underlying induction theorem
or the idea of a dimension lattice is new to the literature.

## Categorical scope and the exact bridge

For the 59 nonintegral inputs surviving the first arithmetic and cyclic tests,
`verify_reduction.py` independently replays every oriented sign deduction,
every residual sign assignment, and every scalar-character inventory. It uses
the previously developed, independently written verifiers in
`work/general_signed/verify.py` and `verify_characters.py`. The sign deductions
are independently reconstructed. The legacy sign checker also recomputes the
12 small alternative character calculations; a separate direct homomorphism
and completeness replay then verifies their results without trusting that
discovery calculation.

Every categorically admissible signed quotient of a sphericalization is gauge
original for these 59 rings. The normalized chosen lifts therefore span a
fusion subcategory mapping tensor equivalently to the original category. Thus
any categorification of any of these rings is spherical. This is a statement
about that category, not an assumed general pivotality conjecture.

The remaining original dimension characters are completely enumerated and
checked by exact homomorphism identities and scalar-character dimension. Their
zero-dimensional, unequal-dual, norm and dimension-field obstructions are
checked individually. Except for six inputs described below, each surviving
spherical character admits a Galois embedding and tensor sign character making
all simple dimensions positive. In those cases a Galois conjugate of a
hypothetical categorification is pseudo-unitary. The original category itself
need not be pseudo-unitary.

The full replay checks 59 sign records, 12 alternate signed character records,
and 59 original character records. The four inputs R11_1_2, R11_1_51,
R11_1_124, and R11_1_147 already have no surviving spherical dimension
character. All subsequent claims have this replay as an explicit dependency.

## A dimension lattice for every spherical character

Let C be spherical, let d_i be its simple categorical dimensions, and put
δ = sum_i d_i d_(i*). For every irreducible based-ring representation E,
Ostrik's induction theorem supplies a simple A_E in Z(C) with

    dim(A_E) = δ/f_E,       [F(A_E):1] = dim(E).

Consequently δ/f_E belongs to the additive group L_d = sum_i Z d_i. This
condition holds even when some d_i are negative and even when δ is rational.
It is stronger than algebraic integrality of δ/f_E. In particular it is not
restricted to the FP dimension character.

A certificate consists of a rational linear functional ℓ on the exact
character field for which ℓ(d_i) is integral for every i but ℓ(δ/f_E) is not.
No object can have the required dimension. The certificate checker verifies
every value directly; it does not trust a Hermite-normal-form computation or
run a lattice search. Each irreducible character-field factor represents its
whole Galois orbit: the obstruction is preserved by applying the corresponding
embedding, and the multiset of formal codegrees is Galois invariant.

The 34 excluded inputs fall into four dimension families. The table describes
the FP branch; the saved certificates also cover every other admissible
spherical branch.

| FP dimension multiset | Inputs | Missing central-object dimension |
|---|---|---|
| 1^4, 2^3, (1+sqrt(5))^4 | 2,31,51,59,69,83,107,108,122,124,147,151 | (3+sqrt(5))/2 is outside Z+Z sqrt(5) |
| 1^4, 2^3, (2+2sqrt(2))^4 | 32,62,88,110,137,138,152,154 | D/32 = 2+sqrt(2) is outside Z+2Z sqrt(2) |
| 1^4, 2, a^2, b^2, c^2 | 34,70,89,96,115,123,139,167 | D/24 = 2+(a+b)/2 is outside Z+Z a+Z b |
| 1^4, 2, (1+sqrt(5))^4, (3+sqrt(5))^2 | 36,86,95,135,136,170 | D/40 = (3+sqrt(5))/2 is outside Z+Z sqrt(5) |

Every listed index has prefix R11_1_. In the cubic row, a is the largest real
root of a^3-12a-8=0, b=a^2/2-2, and c=a+2. The numbers 1,a,b are rationally
independent, the simple dimensions generate Z+Za+Zb, and D=48+12a+12b.
For the first row D=40+8sqrt(5), and the formal codegree 40-8sqrt(5) gives the
stated missing dimension. For four of those inputs the scalar inventory
already rejects every spherical branch, independently of this description.

The last six inputs require particular care. Besides the FP/Galois branch
there is a mixed spherical character of global dimension 40. It cannot be
silently replaced by the FP character. Its simple dimensions still span
Z+Z sqrt(5), while the actual formal codegrees 60±20sqrt(5) force central
dimensions (3∓sqrt(5))/2, again outside that lattice. Thus both types of
spherical character are excluded, and no pseudo-unitary assumption is used.

`verify_spherical_lattice.py` checks 44 separating functionals across all
remaining branches of these 34 inputs. Four inputs are already excluded by
the complete scalar inventory; the other 30 use at least one lattice witness.

## A uniform two-character restriction obstruction

The remaining four rings R11_1_3, R11_1_52, R11_1_142 and R11_1_149 have
FP dimensions 1^4, 2^3, x^4 with x=2+2sqrt(2) and D=64+32sqrt(2).
The signed/Galois audit reduces their categorification problem to the
pseudo-unitary case.

Let χ be the Galois conjugate of the FP character. It has values 1 on the
invertibles, 2 on the two-dimensional simples, and x'=2-2sqrt(2) on the four
x-dimensional simples. Its formal codegree is 64-32sqrt(2), so its associated
central simple has dimension

    βχ = 3+2sqrt(2) = 1+x.

A second explicitly verified scalar character φ has formal codegree 16 and
is ±sqrt(2) on every x-dimensional simple. Its associated central simple has

    βφ = 4+2sqrt(2) = 2+x.

Both representations have dimension one, so both restrictions contain the
unit exactly once. Positivity and rational independence of 1,sqrt(2) force

    F(Aχ) = 1+X,          F(Aφ) = 1+g+Y,

where X,Y have dimension x and g is a nontrivial invertible. The coefficient
of sqrt(2) forces exactly one x-dimensional summand; the remaining rational
weight is respectively zero or one after accounting for the unit.

The modular character correspondence and symmetry of the center S-matrix
imply

    βχ χ(F(Aφ)) = βφ φ(F(Aχ)).

But χ(F(Aφ))=4-2sqrt(2), and βχ(4-2sqrt(2))=βφ. Hence the equation forces
φ(X)=0, contradicting φ(X)=±sqrt(2). This one argument excludes all four
rings and uses only two characters, no enumeration of induction matrices.

`verify_two_character.py` is a standard-library-only verifier using rational
pairs in Q(sqrt(2)). It checks the two characters against every tensor product,
the formal codegrees, the central dimensions, and all 4×12 possible pairs of
forced restrictions. The exploratory nine-character searches are not needed
for the proof.

## Primary reference and reproducibility

The categorical input is Victor Ostrik, *Pivotal fusion categories of rank 3*,
Moscow Mathematical Journal 15 (2015), 373–396,
https://arxiv.org/abs/1309.4822 : Example 2.9, the character identification
immediately preceding Theorem 2.13, Theorem 2.13, and Corollary 2.15. The
primary PDF was checked directly on 23 October 2026, pages 5–7 of the preprint
(numbered pages; PDF indices 4–6). Sphericity is supplied here by the project's
exact oriented sphericalization argument, not by the theorem's hypotheses
being assumed.

From the workspace root, run all three checks:

    python -O work/rank11/nonintegral/verify_reduction.py
    python -O work/rank11/nonintegral/verify_spherical_lattice.py
    python -O work/rank11/nonintegral/verify_two_character.py

The latter two checks are not standalone general-complex classification
verifiers without the first. Their proof obligations include the signed and
scalar-character replays, whose receipts are bound to full input tensor hashes.
All 38 exclusions are exact; there are no timeout, numerical, or unsuccessful
search claims among them. Overlap with independently obtained structural
exclusions is retained rather than counted twice.
