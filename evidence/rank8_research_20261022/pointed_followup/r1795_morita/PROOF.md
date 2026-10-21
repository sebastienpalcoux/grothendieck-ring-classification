# R1795: the forced order-two subgroup dual has the same fusion ring

This is a conditional structural theorem, not a new ring exclusion, model,
or categorical self-equivalence. It belongs to the exploratory followup,
outside the frozen accepted publication inventory.

**Theorem.** Suppose a complex fusion category C has fusion ring R8_3_1795.
Assume the independently recorded complete pointed-associator obstruction
in `../R1795_pointed_associator_obstruction.json`. Then the actual separable
algebra A=1+g exists, where g=X1. Its Morita dual B=A-bimod(C) has fusion
ring R8_3_1795. Both pointed subcategories have trivial associator class.
This does not identify B with C as tensor categories.

The cited pointed-associator proof rules out the nontrivial C2 class using
all eight exact indicator branches, and the accepted general-to-PU-Galois
gate transfers the conclusion to arbitrary complex categorifications.
Accordingly A is the ordinary subgroup algebra in Vec_C2. For the
dimension/codegree exclusions below we may apply that Galois automorphism
to the entire Morita context. B is then pseudo-unitary by Morita invariance
of global dimension and FP dimension. All based-ring arguments below need
neither this reduction nor a pivotal structure.

## The eight bimodules and their common quotient

The source g acts freely, with orbits

    (0,1), (2,7), (3,6), (4,5).

Choose representatives 0,2,3,4. The four simple right A-modules are Xi A,
one per orbit: their endomorphism spaces are one-dimensional, and every
simple module is a constituent of an induced object. Left tensoring by g
fixes each of these module isomorphism classes because the source ring is
commutative. An A-bimodule structure is a left C2-linearization. Its scalar
projective multiplier can be trivialized since H^2(C2,C*)=0, leaving exactly
two linearizations, differing by the nontrivial character. Thus B has eight
simples. Each forgets to the right module Xi A and has FP dimension

    FPdim_C(Xi A) / FPdim_C(A) = FPdim_C(Xi).

Write h for the character bimodule over A. It is an order-two invertible.
It acts freely on each pair of linearizations. Its left and right actions
on bimodule isomorphism classes coincide: the underlying object of each
pair is Xi + gXi, with two distinct simple summands. The left and right g
actions both exchange these summands. Conjugating both actions by the
diagonal automorphism (+1,-1) changes both signs. Consequently changing
only the left sign is isomorphic to changing only the right sign. This
proves centrality of h in the fusion ring, without asserting a half-braiding.

The action of either bimodule over Xi A on the right-module category is the
same matrix Q_i, since

    (Xj A) tensor_A Y_i = Xj tensor Y_i = Xj Xi A

as right A-modules. The four Q_i are linearly independent (their unit
columns form the standard basis), so the quotient of K0(B) by h=1 has
exactly the source pair-quotient tensor Q. Apart from the unit products,
its products on a,b,c are

    a² = 1 + 4a + 4b + 4c,
    ab = 4a + 5b + 4c,      ac = 4a + 4b + 5c,
    b² = 1 + 5a + 4b + 5c,
    bc = 4a + 5b + 5c,
    c² = 1 + 5a + 5b + 4c.

Their FP dimensions are 6+3sqrt(5), 7+3sqrt(5), 7+3sqrt(5).

## All possible duality branches are selfdual

Each pair is preserved by duality because its underlying source orbit is
selfdual. In the signed quotient h=-1 write a_i* = e_i a_i, e_i in {+1,-1}.
Let tau be the coefficient-of-unit trace in this quotient. It is cyclic
and invariant under the anti-involution. Hence, without assuming
commutativity,

    tau(a_j² a_i) = tau((a_j² a_i)*)
                  = e_i e_j² tau(a_i a_j²)
                  = e_i tau(a_j² a_i).

If e_i=-1, this trace and thus the coefficient T[j,j,i] vanish. But T[j,j,i]
has the parity of Q[j,j,i]. The three odd values

    Q[2,2,1] = Q[3,3,2] = Q[2,2,3] = 5

force e_1=e_2=e_3=+1. All eight bimodule simples are therefore selfdual.
The fusion anti-involution fixes every basis element, so the dual ring is
commutative. In particular it cannot be the noncommutative R8_3_1154.

## Complete finite cover enumeration

The signed tensor T has unit and coefficient-of-unit entries delta_ij,
and its remaining entries are symmetric in all three indices by
commutativity and Frobenius reciprocity. There are exactly ten variables,
one for each unordered triple from {1,2,3}. Each variable ranges over

    -Q[i,j,k], -Q[i,j,k]+2, ..., Q[i,j,k].

Changing the chosen lift in one pair changes the corresponding basis sign.
The odd variables T122,T223,T233 transform respectively by the independent
signs of bases 1,3,2. Requiring these three to be positive retains exactly
one representative of each sign-gauge orbit. The complete box contains
2,531,250 choices. All ordered associativity identities yield six distinct
nonzero polynomial equations; exact enumeration returns 45 tensors.

Every returned tensor is expanded to the full eight-dimensional fusion
tensor by

    N[(i,e),(j,f),(k,u)] = (Q[i,j,k] + (-1)^(e+f+u) T[i,j,k])/2.

The verifier checks nonnegativity and every ordered associativity identity
again, using direct Python integer arithmetic. No cutoff or numerical
infeasibility report is involved.

The signed-sector formal codegrees in the full ring are the eigenvalues
of twice the signed Casimir. The global dimension is
D=540+240sqrt(5), with minimal polynomial x²-1080x+3600. For a codegree
with monic minimal polynomial p of degree a, integrality of D/f requires

    a v_l(3600) >= 2 v_l(|p(0)|)

for every rational prime l. Taking norms in a common number field proves
this necessary condition. It excludes 41 of the 45 covers.

Two of the four remaining covers have codegree 60+24sqrt(5). Central
induction would give a simple of dimension

    D / (60+24sqrt(5)) = 5+2sqrt(5).

Every object forgotten to B has radical coefficient divisible by three,
since all eight source dimensions have this property. Thus this required
central dimension is impossible. This excludes both covers exactly,
without an integer search or approximate comparison.

A third remaining cover has T=Q. The even-labeled simples form a closed
rank-four subring with tensor Q and global FP dimension
270+120sqrt(5). A corresponding fusion subcategory contradicts the accepted
general rank-four bound 24+12sqrt(3), specifically Corollary
`finite:cor:sharp-bounds` in
`manuscripts/rank4/papers/companion_sections/14_finite_certification.tex`.
This earlier theorem is an explicit dependency; it is not re-proved here.

The last cover is checked by all 512 coefficients to be R8_3_1795, with
the exact based permutation recorded in `covers.json`. This proves the
conditional Grothendieck-ring self-duality. The dual pointed associator is
also trivial, either by applying the same pointed-associator obstruction
to B, or because h fixes each of the four simple objects in the Morita
module category and a fixed simple trivializes its restriction cocycle.

## Reproduction and limitations

Run `python enumerate_covers.py` from any working directory. It regenerates
and compiles the small native enumeration, then independently checks each
returned tensor and all obstruction witnesses. `covers.json` binds the
canonical input tensor, the pointed and spherical-gate receipts, and the
earlier rank-four theorem source by SHA-256.

This proves a complete necessary ring result for this particular forced
algebra. It does not classify all module categories, solve associators,
prove existence of R1795, or give a tensor equivalence between its Morita
partners. A same-ring subgroup dual can exist without the source category
being braided; therefore the accepted no-braided-Morita theorem does not
exclude the remaining cover.

## Standard categorical references

The module-category and subgroup-algebra construction is the usual
internal-algebra description in EGNO, *Tensor Categories*, Chapter 7.
The bimodule FP-dimension normalization is Exercise 7.16.9(i); preservation
of FP dimension under Morita equivalence is Corollary 7.16.7:
<https://math.mit.edu/~etingof/egnobookfinal.pdf>.
The induced-unit formal-codegree theorem used in the norm and dimension
lattice obstructions is Ostrik, *Pivotal fusion categories of rank 3*,
Theorem 2.13: <https://arxiv.org/abs/1309.4822>.
The simultaneous general-to-PU-Galois reduction and the exact odd-class
obstruction are the explicit source-bound repository inputs named above.
