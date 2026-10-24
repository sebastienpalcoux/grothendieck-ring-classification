# Rank-nine weakly integral continuation: assigned five-case report

Research date:24 October2026. This report changes no online repository or
website. The categorical proof and its exact tensor checks are separate.

| Case | New conclusion from this work | Authority |
|---|---|---|
| R9_2_585 | General exclusion established by the separate unified dimension120 audit | See sibling `weak_b` and root accepted ledger; not an independent claim of this report |
| R9_2_746 | Explicit unitary model | `CYCLIC_TY_MODELS.md`, `cyclic_ty_models.py/json` |
| R9_2_1025 | General exclusion established by the separate cyclic-TY stabilizer argument | See sibling `weak_b` and root accepted ledger |
| R9_2_1209 | Explicit unitary model | `CYCLIC_TY_MODELS.md`, `cyclic_ty_models.py/json` |
| R9_2_1254 | Explicit unitary model | `MR_1254_MODEL.md`, `mr_1254_model.py/json`, independent sibling `audit_models/mr_order4_audit.py/json` |

## Two models, by one uniform construction

An explicit central C3 quotient of
`TY(C3,chi,1/sqrt3) boxtimes Vec(C9,Omega3)` gives a generalized TY category
with invertibles C9 and three sqrt3-dimensional simples. Its coherent
inversion action and the variant with negative odd square coherence give
R9_2_746 and R9_2_1209 respectively. The central lift, central cube,
self-braiding, algebra multiplication, inversion tensorator and algebra
preservation are all given explicitly. No unproved lifting assumption or
vanishing-H4 inference is used.

The constructor checks the pointed3-cocycle, tensor-functor equations,
central half-braiding, central cube, algebra preservation, both complete
fusion tensors, all729 coefficient comparisons, and all ring axioms.
The source-to-model permutations are

-746:[0,1,6,7,2,5,3,8,4].
-1209:[0,6,7,2,5,3,8,1,4].

Section4 extends the construction uniformly to every odd n>1, with
intermediate dimension2n^2 and final dimension4n^2 and rank(n^2+n+6)/2.
There is no assertion of classification or tensor-equivalence novelty.

## R9_2_1254: solved by an order-four lift and coherent descent

This ring has the same integral neutral fusion ring and its action on the
two odd objects as the already realized R9_2_389. The difference is that
the two odd objects are mutually dual in1254, and each is self-dual in389;
their squares and mixed products are interchanged. This observation led to the order-four lift below.

The earlier16th/32nd-root phase failures for a mixed lift to the Ising
and cyclic-charge covering category are now replaced by a short exact
obstruction valid for arbitrary nonzero complex tensorators. Five
necessary equations imply1=-1. The same integer relation works for all
p=2,6,10,14, r=7,15, v=1. `MR_ARBITRARY_PHASE_OBSTRUCTION.md` gives the
four scalar ratios, equations and proof; `verify_mr_five_equations.py`
independently checks the relevant Ising/pointed associator entries without
importing the old generator. This rules out only these covering-category
lifts, not all possible actions on the condensed generalized Moore–Read
category, and not the fusion ring itself.

A direct standard cyclic lift with r=3,5,11,13 changes the chosen central
boson's half-braiding by the odd-parity character, so it does not preserve
that particular central algebra. The mixed r=3,v=1 order-four lift does preserve the central algebra.
The complete tensorator and square-to-central-boson functor isomorphism
were solved and exactly replayed. After condensation its square becomes
the identity, and an explicit universal-grading character adjustment kills
the C2 coherence defect. All729coefficients then match1254.
`MR_1254_MODEL.md` supplies the categorical proof;
`mr_order4_descent_2_3_1_4.json` stores every phase;
`mr_1254_model.json` stores the final tensor and basis map. An independent
audit reconstructed all18432tensor-functor entries and the explicit
C2coherence equations successfully. Thus1254is now realized, not merely
a feasible scalar ansatz. The earlier pure-lift exploration is superseded
by this complete descent certificate.

## Hopf8 route: explicit limit

An exploratory exact computation found four symmetric nondegenerate Hopf
pairings for the standard Kac–Paljutkin Hopf algebra H8, and compatible
involutive Hopf automorphisms. These are recorded in `hopf8_pairing.py`,
`hopf8_pairings.json` and `hopf8_actions.py`. This is not the model certificate
for1254; the successful construction is the separate order-four descent. An equivariantization of a rank-one odd extension of Rep(H8),
with the odd object fixed by C2, necessarily has the canonical sign
invertible interchange its two odd equivariant lifts. In1254 every
invertible fixes each odd simple. Thus this proposed construction cannot
produce1254. No broader nonexistence is inferred.

The preliminary full-HNF attempt was abandoned after the exact
five-equation relation was found; no HNF output is used as evidence.

## Primary literature consulted

- S.Gelaki,D.Naidu,D.Nikshych, Centers of graded fusion categories,
  Algebra&NumberTheory3(2009),959–990, https://arxiv.org/pdf/0905.3117.
  ExplicitTY associators, central invertibles, orthogonal action, central
  de-equivariantization. Our right-half-braiding convention is specified.
- J.Liptrap, Generalized Tambara–Yamagami categories,
  https://arxiv.org/html/1002.3166v2. This supplies a complete algebraic
  parameterization in the generalizedTY setting, but we did not solve its
  full equations for all condensed-category involutions.
- J.Dong,S.Natale,H.Sun, A class of prime fusion categories of dimension2^N,
  NYJM27(2021),141–163, https://nyjm.albany.edu/j/2021/27-5p.pdf.
  The braided structure theorem is not used to classify unbraided actions.
- A.Davydov,I.Runkel, Z/2Z-extensions of Hopf algebra module categories by
  their base categories, https://arxiv.org/abs/1207.3611.
  The Hopf8 exploration remains outside accepted model authority.
