# What the complete conjugation-parity test can and cannot decide

This note gives two finite, theoretical restrictions on the six-case frontier. It establishes no new categorification and no general exclusion of one of the six rings.

## 1. Saturation of palindromic self-duality tests

Let C be a semisimple rigid C-linear pivotal category. Write S for its self-dual simple objects, with their pivotal second indicators epsilon(S) in {+1,-1}. The previously proved conjugation lemma says that an object V carrying a nondegenerate epsilon-symmetric self-duality gives an epsilon-symmetric self-duality on X tensor V tensor X* for every X. Hence a simple S of opposite indicator has even multiplicity in this object.

Define an undirected graph on the self-dual simple labels. Join Y and S whenever some **simple** X has an odd coefficient [X Y X*:S]. The conjugation lemma requires the second indicator to be constant on each connected component, and equal to +1 on the unit component.

**Proposition (finite saturation).** For any proposed simple-object second-indicator assignment, the graph condition implies every further multiplicity-parity constraint obtained from:

1. an arbitrary object X in place of a simple conjugator;
2. an arbitrary V whose simple multiplicities permit an epsilon-symmetric self-duality;
3. any repeated or nested use of the conjugation operation.

This proposition only concerns this family of parity constraints. It does not imply that an assignment passing the graph comes from a pivotal category.

**Proof.** Decompose X as a direct sum of n_i copies of X_i. In X V X*, the diagonal contribution is the direct sum of n_i squared copies of X_i V X_i*. For i different from j, the two off-diagonal objects X_i V X_j* and X_j V X_i* are dual to each other, using V isomorphic to V* and pivotality. Thus a self-dual simple has the same multiplicity in the two off-diagonal objects, and their joint contribution is even. Equivalently, these summands form a hyperbolic pair. Modulo 2, it suffices to test simple X_i.

Decompose a possible epsilon-symmetric V into self-dual isotypic summands and pairs Z plus Z*. A self-dual simple of opposite indicator has even multiplicity in V; its contribution remains even after any additive conjugation. A non-self-dual pair is hyperbolic, and its conjugate is again a pair of dual objects, so every self-dual multiplicity it contributes is even. Only self-dual Y of indicator epsilon with odd multiplicity matter. For these, the graph condition gives exactly the required vanishing modulo 2 in the opposite-sign S rows. This proves (1) and (2). Repetition follows inductively, proving (3). QED.

In particular, enlarging a search from simple X to tensor words of arbitrary length cannot strengthen this test. A new argument would have to use additional structure, for example a rotation, a specified half-braiding, compatibility of multiple forms, or associativity of a proposed algebra.

## 2. Exact six-case application

Labels are those of `current_remaining_cases.py`, with unit 0. The source tensors and all their associativity identities were independently checked. The graph components are:

| Case | Self-dual parity components | Assignments allowed by the graph with unit sign fixed |
|---|---|---:|
| R6_4_155 | {0,3}; {4,5} | 2 |
| R6_8_1660 | {0,1,2,3}; {4}; {5} | 4 |
| R8_3_928 | {0}; {7} | 2 |
| R8_3_941 | {0,3,4,5,6,7} | 1 |
| R8_3_1154 | {0,5,6,7}; {3}; {4} | 4 |
| R9_2_137 | {0,1,2,7}; {3,6}; {4,5}; {8} | 8 |

All inherited indicator assignments pass. The exact verifier additionally checks 13,297 cross-term duality identities used in the proof. The counts in the third column are **not** counts of categories or categorifications, and other inherited conditions restrict them further.

The implementation is `verify_saturation.py`; the result is `saturation_receipt.json`. The copied old receipt is merely the input for comparison, not a new proof of the inherited indicator values.

## 3. A tempting dimension-doubling construction is impossible

Put d=4+3 sqrt(2). R6_4_155 has four invertibles and two noninvertibles X,Y of dimension d, with X* = Y and X not isomorphic to Y. Its global FP dimension is 4+2d squared. R9_2_137 has four invertibles, one self-dual simple of dimension 2, and four self-dual simples of dimension d. Its global FP dimension is 8+4d squared, exactly twice the former.

**Proposition.** A categorification of R9_2_137 cannot be a one-step finite-group equivariantization of a categorification of R6_4_155. It also cannot be a nontrivial faithful finite-group extension of one.

**Equivariantization proof.** The dimension ratio forces the group to have order two. Equivariant simple objects are parametrized by a group orbit of source simples and an irreducible projective representation of its stabilizer. For a group of order two over C, all such projective irreducible representations are one-dimensional. A two-element orbit {X,Y} would produce a simple of dimension 2d, which the target ring does not have. Therefore X and Y would both have to be fixed. The four resulting equivariant simples have underlying objects X,X,Y,Y. The forgetful tensor functor preserves duals. Consequently none of them can be self-dual: its dual lies over the other source simple. This contradicts the target ring, in which all four d-dimensional simples are self-dual. QED.

**Extension proof.** In R9_2_137 the adjoint based subring is the whole ring: the union of the supports of X_i X_i* is {0,1,2,3,4,5,6,7}, and multiplication generates label 8 as well. Thus its universal grading group is trivial. It cannot be faithfully graded by the required group of order two. QED.

These two proofs use only the tensor structure and FP dimensions. No pivotal, spherical, pseudo-unitary or unitary hypothesis is needed. They rule out these two specific construction mechanisms, **not** arbitrary categorical relationships or categorification of either ring. For the same elementary adjoint-subring reason, none of the six frontier rings can itself be a nontrivial faithful group extension of any smaller fusion category. This latter observation is a repeated structural check, not claimed as new to the project.

## Sources and scope

- The earlier elementary conjugation lemma is in the project's current `manuscripts/frontier/Fusion_Ring_Frontier.tex`, section 1.
- S.-H. Ng and P. Schauenburg, *Higher Frobenius--Schur indicators for pivotal categories*, https://arxiv.org/abs/math/0503167, supplies the pivotal-indicator setting.
- S. Burciu and S. Natale, *Fusion rules of equivariantizations of fusion categories*, https://arxiv.org/abs/1206.6625, supplies the orbit/stabilizer description of equivariant simples.
- P. Etingof, D. Nikshych and V. Ostrik, *Fusion categories and homotopy theory*, https://arxiv.org/abs/0909.3140, gives the extension framework.

The saturation theorem is conditional on a pivotal structure. Applying it to general complex categorification requires a separate valid existence reduction. The route obstruction in section 3 does not require such a reduction. Neither argument turns a surviving numerical system into a model.
