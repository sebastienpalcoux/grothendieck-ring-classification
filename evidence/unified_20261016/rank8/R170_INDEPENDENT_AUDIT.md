# Independent audit of the R8_2_170 inverse-Morita exclusion

Result: the categorical reduction and the cyclic terminal replay pass. The conclusion concerns all fusion categorifications over C, without a pivotal, spherical, or unitary hypothesis.

The source tensor is `78c260875e85e75fa8689dba58a9c5225942228315e25da354ad3da8b4bbf06d`. Its neutral C2 component has labels 0,5,6,7; choose u=3, g=5, and r=6. Both u and g are involutions and uru=gr. Left and right multiplication by u give different partners of r. The H×H orbits for H={1,u} are {0,3}, {4,5}, and {1,2,6,7}, with stabilizer sizes 2,2,1. The noninvertible dimension d satisfies d²=1+4d, hence d=2+sqrt(5).

## Coherence and algebra object

The faithful C2 grading restricts to an isomorphism on H. The pointed restriction has an associator class in H³(H,C*)=C2. Inflating the inverse class along the grading and multiplying the full associator by its normalized 3-cocycle preserves the pentagon and all fusion coefficients. Thus existence of any source category implies existence of another category with the same tensor whose restriction to H has trivial associator class. A choice of trivializing 2-cochain then transports the regular group algebra to a connected separable algebra A=1+u. This argument does not assert that A exists in every original associator before twisting.

## The full list of simple bimodules

For the free A-bimodule F(Y)=A tensor Y tensor A, adjunction gives End(F(Y))=Hom(Y,A tensor Y tensor A) as vector spaces. For either pointed orbit this endomorphism algebra is semisimple of dimension two, hence C×C: F(Y) has two distinct simple summands, once each. An underlying summand's support and multiplicities are invariant under multiplication by u on either side, because these action maps are isomorphisms on each group summand. Since the underlying free object contains each member of its two-element orbit twice, each simple bimodule contains both orbit objects once. Its normalized dimension is 2/FPdim(A)=1. This also handles any possible projective stabilizer cocycle directly; no unproved triviality of a four-element stabilizer is used.

For the noninvertible orbit the free endomorphism algebra is one-dimensional, so F(r) is simple. Its underlying object contains each of the four noninvertibles once, and its normalized dimension is 4d/2=2d. Every simple bimodule is a summand of a free one by the free-forgetful adjunction and semisimplicity. The three orbits therefore give exactly four invertibles and one noninvertible Z. The invertibles form C4 or V4. The unique noninvertible is fixed by them and self-dual, so reciprocity and dimensions force Z²=sum(h)+8Z. This is the complete near-group tensor, not a dimension-only recognition.

## Terminal exclusions and provenance

The V4 alternative uses the general near-group obstruction in Schopieray's Theorem 1.1, as cited and source-checked in the surrounding R170 proof.

The C4 alternative is independently replayed in `rank5_cyclic/verify.py`. Its five Python source modules and four TeX source files are byte-identical extracts from the earlier Rank5_Unified_Frontier.zip, SHA256 `057aff6c4f910136a4486eeb65b0fa69020560d40d2ab9a6a1257de8a4cb54cb`. This provenance is distinct from the later complete-through-20 archive. The extracted source tensor has hash `200f68cbc260cb74439c319df1cfb634e87a3dd3927d2c4d504e43e5d3aa6b95`; the wrapper independently constructs K(C4,8), checks a complete based isomorphism, and validates all based-ring axioms.

I compared the archived cyclic-support proof and finite-trace proof with Theorem 6.3 and the k=2 summary of the current rank-five PDF. They give the same six branches at height six. The four exact separators have A-transpose-y nonnegative and b-transpose-y equal to -800,-220,-320,-80. The other two branches force the fusion coefficient 1/2. Both normal Python and optimized Python replays pass with identical receipts. No optimizer is called.

The general-complex scope is justified by Thornton, *On braided near-group categories*, arXiv:1102.4640, Theorem 1.3. I directly checked the primary PDF: that theorem explicitly applies to near-group categories without a braiding and gives a spherical structure that becomes positive under a field automorphism. Hence a pseudo-unitary Galois conjugate exists. The central-support and finite-indicator argument applies to this conjugate; the original category need not have been given a pivotal structure. Source: https://arxiv.org/pdf/1102.4640, page 2 (Theorem 1.3) and page 5 (its proof).

No missing associator choice or projective block remains in the reduction. The terminal C4 proof is a theoretical finite central-support argument with exact integer certificates, not a bounded search for associators or twist orders.
