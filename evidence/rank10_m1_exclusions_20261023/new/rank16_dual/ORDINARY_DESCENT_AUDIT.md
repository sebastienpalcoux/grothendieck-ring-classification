# Independent audit of the ordinary-factor descent

I independently reviewed `../quadratic_models/ORDINARY_FACTOR_EXCLUSION_DRAFT.md` after completing the relative-factorization proof. The descent step is valid with the inputs stated in that draft.

## Inputs used

1. The established Galois reduction makes a hypothetical original category pivotal, without changing its based ring. This is needed for Etingof--Ostrik Theorem A.3; it is not replaced by an assumption of unitarity.
2. The forced Morita dual is a split C2 extension of B with canonical odd invertible tau of order two and trivial pointed associator. The inverse Morita algebra is 1+tau. Thus the original category is the equivariantization of B by conjugation with tau.
3. Etingof--Ostrik classifies the two pivotal rank-four factors as quantum PSU(2)_6 categories. The tau action identifies their monoidal structures.
4. Our relative-factorization lemma gives a dominant tensor functor F:P1 boxtimes P2 -> B, and the induced central algebra is A=1+(f,f). The Bruguières--Natale monadic result identifies B with A-modules.

## Audit of the possible swapping actions

Let T be a coherent order-two action on B exchanging the two marked factors. Identify the second factor with the first using T restricted to the first. With this identification, the two restrictions of T are ordinary interchange: the restriction in the reverse direction is its inverse by the order-two coherence. Any possible rank-four automorphism exchanging its two noninvertible simples is absorbed in this choice of identification; it is not an omitted extra action.

Applying T to the coherent cross-commutation gives a cross-commutation for the exchanged factors. For each simple cross pair it is unique, because the ratio between two choices is a character of the trivial universal grading of P. This proves that the evident isomorphism T F ~= F L, where L is factor interchange, is a **tensor** natural isomorphism.

Under the monadic description B=(P boxtimes P)_A, a functor with this compatibility is reconstructed from its induced central algebra isomorphism L(A) -> A. This is not merely a statement about the underlying objects: the tensor compatibility transports the algebra multiplication and central structure. Conversely each such algebra isomorphism gives the corresponding descended tensor functor. The unit summand of A is fixed, and the other summand h=(f,f) is simple and satisfies h²=1. Therefore its scalar is necessarily +1 or -1. These exhaust the algebra isomorphisms.

There is no further coherence choice for a fixed descended order-two functor. Two coherences differ by a tensor natural automorphism of Id_B, and this group is Hom(U(B),C^times)=1. The adjoint-generated rank-eight ring has U(B)=1. Likewise U(P boxtimes P)=1 removes any ambiguity from tensor natural automorphisms of F: a tensor automorphism acts by scalars on its simple cross-product values, and these scalars must be constant on the universal-grading relations.

Hence at most the two signs occur. Commutation of equivariantization with condensation expresses them as condensation of 1+(f,f)_epsilon in (P boxtimes P)^swap.

## Audit of the resulting based rings

For the positive sign, in the permutation equivariantization the square of d_x^+ contains both d_x^+ and d_y^+ once. The condensate identifies these two simples because d_f^+ tensor d_x^+=d_y^+. The induced image b is simple (the two equivariant simples form a free orbit under the condensate's invertible summand), so b² contains b twice. This excludes this outcome from a multiplicity-one census.

For the negative sign, the established explicit balanced-module calculation produces R10_1_21. Its invertible group is C2 x C2 and all its simples are self-dual, whereas both targets 114 and 115 have C4 invertibles and nonselfdual simples. Galois conjugating the factor categories and this algebra construction preserves the fusion coefficients and duality permutation. Therefore the other quantum parameter choices cannot produce either target.

Subject to the four explicitly identified inputs, the two target rings are excluded. The argument does not infer a tensor-category classification from equality of the rank-sixteen based rings.
