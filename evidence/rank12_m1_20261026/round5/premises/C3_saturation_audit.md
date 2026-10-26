# Independent final audit: R561 and R628 conductor saturation

Verdict: the exclusion proof in ../c3_structure/saturation_exclusion.md is valid, given the pinned Schopieray preprint arXiv:2609.35287v1 (Lemma4.1 and Theorem5.1). This audit read the source statements/proof and independently checked the equality refinement and categorical application. The exact replay verify_saturation.py passes under Python -O.

The earlier forced-central-C3 proof was independently audited in audit.md, including an explicit relative-center half-braiding diagram. Thus no new central-lift assumption is inserted here.

1. The dimension field and the global-dimension field are both Q(sqrt(10)), so the field-index factor e in Schopieray's theorem is one. The nontrivial character has conductor40. D=120+36sqrt(10) gives the exact squared reciprocal difference1/40. The theorem's dimension-block matrix coefficient therefore reaches its norm bound.

2. For p=3, the local torus character is trivial. Let A_3=P_3 rho(s_3)P_3 and B be the product of all other commuting local compressions. The relevant torus eigenspaces are preserved by A_3. Thus

       |<w, B A_3 w>| <= ||w|| ||B A_3 w||
                         <= ||w|| (1/sqrt(40)) ||A_3 w||
                         <= ||w|| squared /sqrt(40).

   Equality at the endpoints forces ||A_3 w||=||w||. Because w is upper-unipotent fixed and rho(s_3) is unitary, rho(s_3)w is upper-unipotent fixed too. Hence w is fixed by both upper and lower elementary unipotents. They generate SL2(Z/3^a) for every a>=1 (elementary elimination over the local ring, with the Weyl element itself a product of elementary unipotents). There is no overlooked a=1 exception or use of simplicity of the finite group.

3. The conjugate-dimension summand B0 centralizes the forced C3. The central character identity gives unnormalized S_(B0,h)=dim(B0) for each invertible h. In fact positivity is unnecessary for this particular inference: h tensor B0 is simple, so its monodromy is scalar and the nonzero trace equality forces that scalar to be one. Hence the center's genuine ribbon splitting gives B0=1 tensor B1 and w=e_0 tensor(e_1-e_B1), nonzero because dim(B0)=d squared>1.

4. Taking n=N/3^a, the global matrix s t^n s^(-1) is identity at every CRT factor except3. Its action must fix w. Exact S and T tensor factorization inside the Drinfeld center gives the corresponding tensor product of the words in each modular factor. There is no need to normalize the projective representations of the factors separately. In the metric C3 factor, the vacuum column is ((1+2z)/3,(1-z)/3,(1-z)/3) with z a nontrivial cube root. Its nonvacuum coordinates are nonzero, contradicting the pure-tensor form of w.

5. In the Tannakian branch, the actual central regular algebra gives a pseudo-unitary quotient of dimension D/3. Free H-action yields simple dimensions1,1,d,d, so again e=1 and conductor40. Its squared reciprocal difference is9/40, strictly larger than the allowed1/40. This closes the branch without importing a lower-rank classification or an exponent bound.

The proof is uniform for both rings and excludes arbitrary complex categorification after the valid pseudo-unitary Galois reduction. It does not assume a braiding or unitarity on the original category.
