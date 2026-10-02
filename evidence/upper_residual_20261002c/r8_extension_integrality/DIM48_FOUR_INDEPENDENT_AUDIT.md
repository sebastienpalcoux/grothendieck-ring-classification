# Independent audit: the four dimension-48 exclusions

**Approved for general complex fusion categorification.** I independently
read the complete argument and its exact verifier. No pivotal, spherical,
braided, or unitary hypothesis is needed. The original full tensors are
bound to the census by the verifier, and fresh ordinary and optimized
Python replays both pass:

- `dim48_four_independent_normal.json`
- `dim48_four_independent_optimized.json`

The dimension-12 classifier tests 100 oriented candidate product tables,
finds six associative tables, and retains exactly two with the required
outer involution. These two are precisely `R_{3,V4}` and `R_{3,C4}`.
Jordan--Larson Theorem 1.4 applies because the group order is four and
excludes the latter. The pointed associator in the former is trivial:
the rank-one homogeneous component is an actual module category and
therefore supplies a fiber functor on the pointed neutral category.

The delicate module step is sound. De-equivariantization gives an actual
E-module of rank one or four. Galindo Proposition 4.1 makes each
homogeneous component act on actual indecomposable neutral summands,
not merely on abstract equivalence classes. The rank-four regular class
and the two rank-one classes constitute a three-cycle. Any nontrivial
class orbit has total rank at least six. Thus the available module is
rank four and has two rank-two summands. A group of order three cannot
permute these two actual summands nontrivially, so either is a coherent
E-module extension. This is the hypothesis needed in Galindo Theorem 1.3.

The resulting induced-module dual is a semidirect product, with a graded
tensor section. Hence no independent C3 associator twist is lost.
The order-three tensor autoequivalence has nontrivial order-three image
in Aut(V4), since its Brauer--Picard class is nontrivial and the kernel
has order two. The vanishing of `H^2(C3,V4-hat)` identifies its coherence
with the strict group action. The resulting pointed category is the
untwisted `Vec_A4`.

Nikshych--Riepel Proposition 7.6 and Section 8.3 identify the three A4
Lagrangians as the orbit of the canonical one, so each has untwisted
pointed dual `Vec_A4`. The outer involution fixes one. Galindo
Proposition 5.3 requires invariance of that module, not a coherent
extension, and gives the required pointed graded Morita realization.
Its group extension is either S4 or A4 times C2. The latter has six
identity-supported central invertibles for every associator. Because
U(D) is trivial, restriction of central invertibles is injective, whereas
D has only four invertibles. The direct product is therefore excluded.

Finally, the arbitrary-twist extension-integrality lemma is applicable
to S4. Gelaki--Naidu Theorem 4.1 identifies the identity block of a
twisted subgroup dual with ordinary Rep(N). Pointedness forces N
normal and abelian; S4 has only such subgroup orders one and four.
The normalized bimodule simple dimensions are therefore one or two.
ENO Corollary 3.13 transports the whole graded extension through Morita
equivalence. Integrality of the transported category implies integrality
of the original one via the common integral center and the induction
dimension formula. This contradicts the two source dimensions
`2sqrt(3)` in all four cases.

Primary sources checked directly:

- https://arxiv.org/pdf/0812.1603
- https://arxiv.org/pdf/1010.5283
- https://arxiv.org/pdf/1309.5026
- https://arxiv.org/pdf/0909.3140
- https://arxiv.org/pdf/0709.4326

The exact finite checks and categorical argument have distinct roles;
passing the checker alone does not certify the cited categorical steps.
