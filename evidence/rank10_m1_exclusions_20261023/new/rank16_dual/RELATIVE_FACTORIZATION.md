# A relative factorization lemma for the forced rank-eight categories

This is a categorical deduction conditional only on existence of a complex fusion categorification of the reconstructed rank-sixteen tensor. It does not assume a braiding, pivotal structure, pseudo-unitarity, or unitarity.

## Hypotheses supplied by the exact tensors

Let B be the adjoint subcategory of the forced rank-sixteen category. There are two rank-four fusion subcategories C,E with the following properties, independently checked by `verify_subcategories.py`.

1. Their intersection has simples 1,f, where f has order two and acts freely on all simples of C and E.
2. Every cross product XY, with X simple in C and Y simple in E, is simple. For fixed X or fixed Y, the resulting four simples are distinct. The two subcategories generate B.
3. If Y is either noninvertible simple of E, the four simples XY, X in C, form the complement M of C in B. This complement is a C-bimodule subcategory.
4. The M-part of Y squared is Y plus fY, each with multiplicity one. This holds for both the ordinary and pseudo PSU(2)_6 fusion rules.
5. C and E are multiplicity-free and have trivial universal grading. Indeed each noninvertible X has XX*=1+X+fX; these constituents generate the whole rank-four category.

For R10_1_114 and R10_1_115, both rank-four subcategories have the ordinary PSU(2)_6 based ring. For R10_1_152, R10_1_153 and R10_1_179, both have the non-self-dual pseudo-PSU(2)_6 based ring. The same ordinary case occurs in the known control R10_1_21.

## Lemma: the two factors admit coherent cross-commutation

Under these hypotheses, the inclusion E -> B lifts to the relative center Z_C(B). Equivalently, multiplication extends to a dominant tensor functor C tensor E -> B, where tensor denotes the Deligne product.

**Proof.** The functor L:C -> M, X |-> XY, is an equivalence of left C-module categories: it is fully faithful on simple objects and essentially surjective. Transport the right C-action on M along L. It is determined by a tensor autoequivalence phi of C. At the level of objects phi fixes every simple, because XY and YX are isomorphic. Thus M is the regular C-bimodule with one action twisted by phi.

Tensor product in B, followed by projection to the C-bimodule summand M, gives a C-bimodule functor

    M tensor_C M -> M.

Under the regular-module identifications its underlying object is 1+f: evaluating on Y tensor_C Y and projecting to M gives Y+fY. The usual description of functors between twisted regular bimodule categories therefore makes 1+f an object of a phi-twisted center (with phi possibly replaced by its inverse, which is immaterial).

The twisted half-braiding with a simple X is a map between direct sums whose two simple constituents are X and fX, with phi(X) isomorphic to X. These constituents are distinct. Hence every such map is block diagonal for the decomposition 1+f. Naturality and the half-braiding axiom restrict to the unit summand. A twisted central structure on the tensor unit is exactly a tensor isomorphism phi -> Id_C. Consequently phi is tensor isomorphic to the identity, and Y admits an ordinary relative half-braiding with C. The f summand of the same argument also provides a central lift of f inside C.

Any relative half-braiding on a fixed simple object Z in E is unique: two choices differ on each simple X in C by a scalar lambda_X, since XZ is simple. The half-braiding axiom, and full faithfulness of - tensor Z on C, give lambda_W=lambda_X lambda_X' whenever W is a constituent of XX'. Such scalars are characters of U(C), which is trivial.

It remains to check closure under tensor product and summands. Products of two lifted simple E-objects lift to the relative center. Such a product is multiplicity-free. For each simple X in C, the functor X tensor - is fully faithful on E: it maps its four simples to distinct simples. Therefore the relative half-braiding of this product preserves each of its simple E-summands, and each inherits a relative half-braiding. Starting with 1,f,Y and repeatedly taking these products produces every E-simple (in particular fY). For arbitrary direct sums take the corresponding direct sums of these simple lifts. Uniqueness of the simple lifts makes all E morphisms central and identifies tensor products of the chosen lifts with the chosen lift of each product. This is the required tensor lift and proves the lemma. QED.

This argument is closely related to the twisted-center method in Etingof--Nikshych--Ostrik, *Twisted Deligne products of semisimple tensor categories*, arXiv:2607.19560, Sections 2.2 and 3.1. Their ordinary exact-factorization theorem does not apply directly because C intersects E in a nontrivial pointed subcategory. Here the direct-sum decomposition B=C+M and the free action of f provide the missing argument.

## Corollary: the central self-braidings are inverse

The central lift of f in each rank-four factor is unique, since U(C)=U(E)=1. Write q_C and q_E for its scalar self-braiding. Let c_{Z,X}:ZX -> XZ denote the coherent cross-commutation, for Z in E and X in C.

For Z=f this is the unique central lift of f in C, so c_{f,f}=q_C. For X=f, the inverses c_{Z,f}^{-1}:fZ -> Zf form a central lift of f in E, so q_E=q_C^{-1}.

In the forced rank-sixteen category, conjugation by the canonical sign bimodule tau exchanges C and E. This is a tensor equivalence carrying f to f; uniqueness of its central lift implies q_C=q_E. Therefore any categorification of any of the five candidate rings necessarily satisfies

    q_C^2 = 1.

The shared invertible f is NOT tau: this distinction is checked in the receipt and is essential.

## Applying the lemma to exclusions

The known pseudo-PSU(2)_6 categories have q=+i or q=-i, so the preceding argument rules out all constructions using those categories as the two rank-four factors. More strongly, `PSEUDO_BRANCH_EXCLUSION.md` now rules out q²=1 for **every** complex categorification of the pseudo based ring: q=+1 gives the forbidden rank-two ring K_2, while q=-1 gives the odd-evaluation rank-two super fusion rule C-hat_m^(1,1), excluded by a specific finite superpentagon calculation in Chang--Chen--Xu. Therefore R10_1_152, R10_1_153 and R10_1_179 are excluded without a rank-four categorical classification or a unitarity assumption.

One possibility, q=+1, can already be excluded intrinsically in both rank-four based rings: a central boson f gives the connected separable central algebra 1+f. Its module category is a fusion category with two simples, because f acts freely. The nontrivial simple has dimension 1+sqrt(2) and square 1+2X, which is the noncategorifiable rank-two ring K_2 by Ostrik. Thus the forced symmetric alternative is q=-1.

For the ordinary PSU branch, the relative factorization lemma gives a precise central-product reduction but does not by itself classify the two rank-four categories or the order-two extension and its associator. No exclusion of R10_1_114 or R10_1_115 follows from this note alone.

Primary references:

- Etingof--Nikshych--Ostrik, https://arxiv.org/html/2607.19560v1 .
- Ostrik, *Fusion categories of rank 2*, https://arxiv.org/abs/math/0203255 .
