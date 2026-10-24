# Independent audit of five structural exclusions

**Outcome: all five exclusions are accepted in general complex fusion-category scope.**
The audited IDs are `R9_2_907`, `R9_2_1071`, `R9_2_1724`,
`R9_2_1356`, and `R9_2_1933`. No positive-model registry, absence-from-a-list
argument, numerical infeasibility result, braiding assumption, or unitarity
assumption is used. In particular, these proofs are independent of the
newly discovered omission of the half-E6 category from an earlier registry.

This audit re-derived the categorical arguments, checked the precise primary
statements, and read each tensor afresh from the original compressed input.
It did not accept previous `PASS` records as evidence. The original tensor
checks are in `fresh_tensor_checks.json`; the independent implementation is
`fresh_tensor_audit.py`. Positivity and all 81 dimension-character products
are checked in exact integers or in the pair presentation of Q(sqrt(26)).

## Shared categorical steps

1. **Actual last operation, not merely Morita solvability.** ENO,
   arXiv:0809.3031v2, Proposition 4.4(3) explicitly gives a sequence ending at
   the category itself, each step an extension or equivariantization by a
   cyclic prime group. If the adjoint subcategory is the whole category,
   no nontrivial extension can be the last step. An equivariantization by
   Cp has a canonical fully faithful central Rep(Cp), so its character
   group is a subgroup of the underlying invertibles. This is the needed
   statement; the weaker claim that the category is Morita equivalent to
   a cyclically nilpotent one would not suffice on its own.

2. **Central lift uniqueness.** If U(B)=1, an invertible b has at most one
   isomorphism class of central lift. Given two lifts, their tensor quotient
   has underlying unit and thus corresponds to a monoidal automorphism of
   Id_B. Its scalar on each simple is multiplicative across every nonzero
   fusion coefficient; such scalar systems factor through U(B). Hence it
   is trivial. Transport by a tensor autoequivalence consequently preserves
   a central pointed subcategory which already lifts all invertibles.
   This is about the actual half-braidings, not simply centrality in K0.

3. **Equivariantizing the preserved central subcategory.** The original
   coherent action restricts, including its coherence maps. The
   half-braiding of an equivariant central object with another equivariant
   object is equivariant, so the restricted equivariantization embeds into
   the center of the ambient equivariantization. If the central pointed
   subcategory was Rep(A), its equivariantization is Tannakian: forget
   equivariance and compose with the symmetric fiber functor Rep(A)->Vec.
   No unproved bosonic-lift assertion is being made. Fully faithful
   forgetful image is retained. De-equivariantization by the combined
   Tannakian category recovers the iterated construction in stages.

4. **Cyclic projective stabilizers.** H^2(Cn,C*)=0 over C: the periodic
   cyclic resolution gives C*/(C*)^n in degree two, which vanishes. Thus
   every projective irreducible of a cyclic stabilizer is one-dimensional.
   Consequently tensoring by its character group distinguishes fixed
   downstairs simples from free orbits exactly as the proofs require.

## Dimension 96: 1356 and 1933

The fresh tensors have dimension 96, invertible group C3, and adjoint
closure equal to all nine basis elements. ENO Theorem 1.6 applies because
96=2^5*3. The preceding actual-last-operation argument forces a central
Rep(C3), hence every underlying invertible would commute with every simple.

The independent check stores an explicit unequal left/right product for
**each** of the two nontrivial invertibles in each tensor. Both generators
are noncentral. This is a contradiction before any more elaborate
triality, Tambara-Yamagami, Brauer-Picard, or dimension-32 classification
is needed. Those later structural claims are not dependencies of these
two exclusion certificates and are not silently included in this audit.

## Dimension 222: 907

The tensor has positive dimension character (1,1,2,6,6,6,6,6,6), invertibles
C2, trivial universal grading, and its nontrivial invertible fixes every
noninvertible on both sides. The dimensions establish integrality.

ENO Theorem 9.2 applies to 222=2*3*37 and gives group-theoreticality. All
groups of order 222 are solvable: the number of Sylow-37 subgroups divides
6 and is 1 modulo 37, so the Sylow subgroup is normal, and the quotient
has order six. A pointed category on such a group is solvable, regardless
of its associator, and solvability is Morita invariant (ENO Proposition
4.5(i),(ii)). Thus the category in question is solvable, even though its
three-prime dimension does not fall under Theorem 1.6 directly.

The last operation must be C2 equivariantization, giving E of dimension
111 with three invertibles and twelve dimension-three simples. The outer
involution swaps the two nonunit invertibles. For any three-dimensional
simple X in E, dimension counting in XX* forces the invertible stabilizer
to have size three: 9=|Stab(X)|+3m and the possible sizes are one and three.
The noninvertible contribution is nonempty. Hence E_ad contains every
invertible and at least one three-dimensional object. A proper adjoint
subcategory would have dimension 1, 3, or 37; none has the required form
3+9k with k>=1. Therefore U(E)=1.

A second last-operation argument gives E=(Vec_C37^omega)^C3. The C3
permutation of the nonidentity pointed objects is nontrivial: otherwise
all equivariant simples would be invertible, contrary to the dimension
character. The preserved-central-subcategory argument combines the two
stages into a genuine S3 action on Vec_C37^omega. Its normal C3 would have
the nontrivial object action just obtained. But any object action factors
through a homomorphism S3->Aut(C37), and Aut(C37) is abelian, so its normal
C3 is killed. This is the contradiction. The proof never needs to set
omega=1 and does not exclude twists by an unsupported assumption.

## Dimensions 52 and 104: 1071 and 1724

The fresh tensors have a faithful C2 grading. Their even components have
rank seven, dimension 52, dimensions (1^4,4^3), invertible group C4, and
trivial adjoint quotient. Every neutral invertible fixes every
four-dimensional simple on both sides. The odd component consists of two
objects of dimension sqrt(26). These assertions were checked directly,
including every nonzero coefficient's grading parity.

### Rigidity of the neutral category

The dimension-52 category D is solvable by ENO Theorem 1.6. Its last step
must be a C2 equivariantization. The sign pairs its four invertibles and
fixes its three four-dimensional objects, so the quotient B has dimensions
(1,1,2,2,2,2,2,2) and dimension 26. A nontrivial universal grading of B
would have order dividing 26 and at most its rank eight, hence order two.
Its neutral component would have prime dimension 13 and therefore be
pointed of rank 13, impossible. The prime-dimension assertion is ENO,
*On fusion categories*, Corollary 8.30, not an unproved Hopf-algebra
specialization. Thus U(B)=1, and B=(Vec_C13^omega)^C2 with nontrivial
object inversion.

Its central Rep(C2) lifts all invertibles uniquely, so the outer C2
preserves it. The combined central Tannakian category has four invertible
simples and underlying group of simples C4. Its Tannaka group is therefore
C4, rather than V4. It follows that D=(Vec_C13^omega)^C4. The object action
must have order four: an image of order at most two has only orbits of
size at most two, and its cyclic stabilizers cannot provide projective
representations of larger dimension.

There are two separate coherence issues, both resolved:

* An order-four u in Aut(C13) satisfies u^2=-1. The induced action on
  H^3(C13,C*)=H^4(BC13,Z) multiplies by u^2, because the degree-four
  class is the square of the degree-two generator. The invariant
  associator must therefore satisfy omega=-omega in C13, hence vanish.
* Once omega is trivial, individual tensor-functor structures are unique
  because H^2(C13,C*)=0. Coherent composition structures on the C4 action
  form, when nonempty, a torsor under H^2(C4,C13-hat). This group vanishes
  by coprime averaging. Thus no additional categorical action twist was
  missed. The equivariantization is the ordinary representation category
  of G=C13 semidirect_5 C4, up to the harmless dual action.

The second bullet is essential: merely trivializing the pointed associator
would not by itself identify D as Rep(G).

### Exhaustion of module categories, including cocycles

Ostrik arXiv:math/0111139, Section 3.4, Theorem 2 classifies every
indecomposable Rep(G) module category by a subgroup H and a class in
H^2(H,C*). The theorem is applicable over C without any unitarity
assumption. The subgroup list is complete for elementary reasons:
H intersects the normal C13 either trivially, in which case it embeds into
C4 and is cyclic, or in all of C13, in which case its quotient has order
one, two, or four. The subgroup types and module ranks are:

| H | Number of subgroups | H^2(H,C*) | Number of irreducibles |
|---|---:|---:|---:|
| 1 | 1 | 0 | 1 |
| C2 | 13 | 0 | 2 |
| C4 | 13 | 0 | 4 |
| C13 | 1 | 0 | 13 |
| D26 | 1 | 0 | 8 |
| C13 semidirect C4 | 1 | 0 | 7 |

The multiplier vanishing for the two noncyclic types follows from the
Lyndon-Hochschild-Serre spectral sequence for C13 normal with cyclic
quotient Cd, d=2 or4. Every total-degree-two E2 term vanishes:
H^2(Cd,C*)=0, H^1(Cd,C13-hat)=0 by coprimality, and H^2(C13,C*)=0.
Thus this is an exhaustion of twisted as well as untwisted module
categories. Independently, `group52_independent.g` constructs G as an
affine permutation group on 13 points and asks GAP for **all** subgroup
conjugacy classes, their sizes, character counts and Schur multipliers.
Its output confirms all 30 subgroups and all zero multipliers; it also
identifies G as SmallGroup(52,3). This code does not import the earlier
custom group enumeration.

A rank-two module category is consequently Rep(C2). Its dual has simples
indexed by C2 double cosets and irreducibles of intersection stabilizers.
There are two double cosets of size two, each contributing two simples,
and twelve double cosets of size four, each contributing one. Hence its
dual rank is 16 and its dimensions are (1^4,2^12). The independent GAP
computation verifies the complete double-coset count and normalizer order
four, separately from the earlier Python implementation.

ENO *Fusion categories and homotopy theory*, Theorem 6.1(i) makes the odd
component an invertible D-bimodule category. Its dual as a left module
must therefore be D or its opposite according to convention; both have
rank seven. The rank-16 dual contradicts this. The opposite-category
convention cannot affect the argument.

## Primary sources actually reopened during this audit

* ENO, arXiv:0809.3031v2, Theorem 1.6, Proposition 4.4(3), Proposition
  4.5(i),(ii), Theorem 9.2, Proposition 2.10:
  https://arxiv.org/pdf/0809.3031 .
* ENO, *On fusion categories*, Corollary 8.30:
  https://arxiv.org/pdf/math/0203060 .
* ENO, *Fusion categories and homotopy theory*, Theorem 6.1(i):
  https://arxiv.org/pdf/0909.3140 .
* V. Ostrik, *Module categories, weak Hopf algebras and modular invariants*,
  Section 3.4, Theorem 2: https://arxiv.org/pdf/math/0111139 .

No defect requiring withdrawal or scope reduction was found in these five
arguments. The audit does not certify unrelated baseline subring
exclusions or the entirety of the dimension-96 residual classification.
