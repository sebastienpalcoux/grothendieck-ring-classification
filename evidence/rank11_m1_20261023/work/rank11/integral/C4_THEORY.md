# A restriction criterion for graded extensions, excluding R11_1_153

**Conclusion.** The physical census tensor R11_1_153 has no categorification over the complex numbers. Its cyclic degree-two component has a dual pair, while every categorification compatible with its neutral category and universal grading must have the self-dual degree-two component of the explicit R11_1_104 model.

This is a general extension-cohomology exclusion. It does not assume a braiding, a pivotal structure, unitarity, group-theoreticality of a hypothetical category, or exhaustiveness of a finite model search.

## 1. A general restriction lemma

Let D be a fusion category, G a finite group, K a subgroup, and c:G→BrPic(D) a fixed homomorphism. Write A=Inv Z(D), with the G-action induced by c. Suppose at least one G-extension C⁰ realizing c exists, and

res: H²(G,A) → H²(K,A)

is zero. Then the K-subextensions of all G-extensions realizing c have isomorphic based fusion rings, preserving their K-gradings and neutral subcategories up to the chosen identifications.

Indeed, choose representatives for the homogeneous D-bimodule categories. The ENO classification of their multiplication functors is an H²(G,A)-torsor. Relative to C⁰, another system of products differs by an A-valued 2-cocycle L. Restricting the actual multiplication functors to K restricts L. If its class is zero, this difference is removed by bimodule equivalences of the K-components. The restricted product functors therefore agree up to natural isomorphism and change of simple labels. Their fusion coefficients agree. Once product functors are fixed, the remaining freedom consists of scalar 3-cocycles changing associators; it does not change those coefficients. In a fusion ring duality is determined by the coefficient of the tensor unit, so it also agrees.

This is a consequence of Etingof–Nikshych–Ostrik, *Fusion categories and homotopy theory*, Theorems 8.5 and 8.9, or Theorem 1.3 together with its algebraic construction. The restriction assertion follows directly by restricting the cocycle-indexed product functors in the proof of Theorem 8.5. No vanishing of H³ or H⁴ is needed for this lemma: it compares existing extensions against an existing reference.

## 2. The neutral category is forced

Exact tensor checks give the same structural profile for R11_1_104 and R11_1_153: global dimension 32, dimensions (1⁴,2⁷), universal grading C4, and homogeneous ranks (5,2,2,2). The neutral ring is the Tambara–Yamagami ring on V4. Let m denote its unique noninvertible simple.

For a simple X in a generating homogeneous component, the tables give

XX* = 1+h_L+m,    X*X = 1+h_R+m,

where h_L and h_R are distinct nonidentity elements of V4. Both products have their canonical internal-end algebra structures. In either algebra 1+h+m, the multiplication maps h⊗m→m and m⊗h→m are nonzero because the h-summand corresponds to an invertible stabilizing action on X. Associativity on h⊗m⊗h forces χ(h,h)=1 for the TY bicharacter χ. Thus χ has two distinct nonzero isotropic elements. A nondegenerate nonalternating symmetric form on F2² has exactly one such element; χ is therefore alternating.

The two TY categories with alternating χ are Rep(D8) and Rep(Q8), where the groups have order 8. Nikshych–Riepel, Remark 9.4, gives BrPic(Rep(Q8))≃S3. Any homomorphism from C4 to S3 kills the degree-two element. That homogeneous bimodule would be regular of rank 5, contrary to its rank 2. Therefore the quaternion alternative is impossible and D≃Rep(D8).

This argument considers all TY associators and both TY signs. It is also the neutral-category argument already used for the project's lower-rank triality classification. An independent derivation is in `../structural/C4_NEUTRAL_MODULE_AUDIT.md`.

## 3. There is one relevant Brauer–Picard homomorphism

For D=Rep(D8), BrPic(D)≃S4. Tensor autoequivalences include the six isometries of the alternating form on V4, realized by reindexing the TY category. Their map into BrPic is injective: its kernel consists of inner tensor autoequivalences, which are tensor isomorphic to the identity because D is braided. This S3 is precisely the stabilizer of the regular left-module class p in the four-point S4 action. The three other left-module classes are nonregular.

The homogeneous component of each nonidentity C4 degree has rank 2, so the first, second, and third powers of the image of a generator must all move p. Its order therefore cannot be 1 or 2. In S4 it must be a 4-cycle. The S3 fixing p acts transitively by conjugation on all six 4-cycles: its stabilizer of a 4-cycle is the intersection with that cycle's centralizer, which is trivial. Thus every possible homomorphism c is aligned with that of the reference model by an actual tensor autoequivalence of D.

The group calculation BrPic(D)≃S4 is Nikshych–Riepel, Section 9.1. The regular-point description also follows from the above S3 embedding: forgetting the right action identifies the regular class stabilizer with the image of tensor autoequivalences, and its index is four.

## 4. The coefficient module and zero restriction

The coefficient group is A=Inv Z(Rep(D8))≃C2³. As an S4-module it is

A ≃ F2⁴ / ⟨(1,1,1,1)⟩.

Here is an intrinsic identification, using only the explicit reference model. The nontrivial central-group element z defines the central invertible with underlying tensor unit, acting as +1 on the four invertibles of D and −1 on m. Every tensor autoequivalence fixes z, so its S4 orbit has size one or four. It cannot have size one. If all of S4 fixed z, the C4 action of the explicit R11_1_104 extension would fix z. Relative-center equivariantization would lift it to a central invertible with underlying unit, since the projective linearization obstruction belongs to H²(C4,C*)=0. But tensor automorphisms of the identity of that category are characters of its universal grading C4, and therefore restrict trivially to its adjoint category D. This contradicts the nontrivial restriction z.

The four orbit elements are nonzero and distinct. Their span is all of A: a two-dimensional F2-space has only three nonzero elements. Their single relation is invariant under S4, so is their sum zero. This proves the asserted quotient permutation module. The independent structural audit supplies this identification and a normalized-cochain replay of the cohomology calculation below.

Choose a 4-cycle t and put N=t−1 on A. Then N³=0, rank N=2, rank N²=1, and ker N=im N². Its C4 norm 1+t+t²+t³ is N³=0. Hence

H²(C4,A) = ker N,
H²(⟨t²⟩,A) = ker N² / im N².

Even-degree restriction for cyclic groups sends an invariant representative to itself. Since ker N=im N², the restriction is zero. In coordinates w₀,w₁,w₂ with w₃=w₀+w₁+w₂, the action columns are [2,4,7] in binary encoding; the finite verifier obtains

ker N = im N² = {0,5},
ker N² = {0,3,5,6}.

Thus the general lemma applies to the unique order-two subgroup of C4. The additional odd-degree restriction calculation in the earlier research note is unnecessary for this exclusion.

## 5. Exact reference and contradiction

The reference is the explicit group-theoretical category C(G,ω,H,1) constructed in `../known_models/jordan_gt_model.json`. The group G has order 32 and is the nonsplit extension of V8 by C4 with Jordan action and t⁴ the fixed nonzero vector. The file supplies its entire multiplication table, a normalized μ8-valued 3-cocycle, the V4 subgroup H on which ω is trivial, simple labels, full model tensor, and an exact unit-preserving basis map to R11_1_104. The construction checks all 32⁴ cocycle identities and every fusion coefficient. The independent implementation in `../nonintegral/audit104/verify.py` reconstructs all 1331 coefficients from free algebra bimodules, balanced tensor quotients, and graded intertwiner systems without importing the projective-character convolution. It passes and is executed by the exclusion verifier. These finite categorical input data provide the reference extension needed in Section 1.

For R11_1_104 the universal degree-two component has source labels [9,10]; both are self-dual. All simples in its degree-zero-plus-degree-two subring are self-dual. For R11_1_153 the universal degree-two component has source labels [1,2]; these are dual to one another and neither is self-dual. Its neutral simples are self-dual, so these seven-simple subrings have respectively 7 and 5 self-dual simples and cannot be isomorphic as based fusion rings.

If R11_1_153 admitted any categorification, Sections 2–3 would force the same neutral category and, up to equivalence, the same C4 Brauer–Picard homomorphism as the R11_1_104 model. Section 4 and the general restriction lemma would force its even subring to be isomorphic to the reference even subring. The unequal self-duality counts contradict this. Therefore R11_1_153 is excluded.

## Exact data and audit boundaries

- `verify_c4_reduction.py`, `c4_reduction.json`: independently derives the universal components, dimensions, stabilizers, and degree-two duality from the original census; computes the cyclic-module kernels and images.
- `../structural/C4_NEUTRAL_MODULE_AUDIT.md`: independent categorical audit and normalized bar-cochain H² restriction replay.
- `../criteria_audit/verify_c4_torsor.py`, `../criteria_audit/c4_torsor_independent.json`: independent normalized-bar replay of all 128 C4 2-cocycles, their restriction trivializers, and the six 4-cycle conjugacies.
- `../known_models/jordan_gt_model.json`: explicit reference model, not a search-completeness assumption.
- `verify_c4_exclusion.py`, `c4_exclusion.json`: source-bound finite replay and receipt; this verifier executes the independent balanced-bimodule reference-model audit before accepting the exclusion.

The prior unsuccessful cocycle ansätze in this directory have no role in the proof. Positivity passes in `UNITARY_PASS.md` also have no role in the exclusion; they document that those known families had been exhausted before this new restriction criterion.

Primary references:

1. D. Nikshych and B. Riepel, *Categorical Lagrangian Grassmannians and Brauer–Picard groups of pointed fusion categories*, Section 9.1 and Remark 9.4, https://arxiv.org/html/1309.5026v2 .
2. P. Etingof, D. Nikshych and V. Ostrik, *Fusion categories and homotopy theory*, Theorems 8.5 and 8.9, https://arxiv.org/html/0909.3140v2 .
3. S. Gelaki, D. Naidu and D. Nikshych, *Centers of graded fusion categories*, relative-center equivariantization, https://arxiv.org/abs/0905.3117 .
