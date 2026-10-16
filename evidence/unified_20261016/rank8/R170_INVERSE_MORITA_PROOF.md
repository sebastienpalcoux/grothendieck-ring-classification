# A general inverse-Morita obstruction for R8_2_170

**Claim.** R8_2_170 has no fusion-category categorification over C.

This argument does not classify its 2D2 neutral category and imposes no pivotality or unitarity assumption. Its terminal inputs are the general exclusion of the near-group rings R(V4,8) and R(C4,8).

The source tensor has a faithful C2 grading with neutral labels (0,5,6,7). Put g=5, r=6, and u=3. Its four invertibles form V4, with u²=g²=1, ug=gu; all four noninvertibles are the free left orbit of r. Right multiplication satisfies u r u = g r.

Suppose C categorifies this tensor. On the pointed subgroup H={1,u}, the associator has one of the two classes in H³(C2,C*)=C2. The grading restricts to an isomorphism H -> C2. Multiplying the associator of C by the inflation of the appropriate normalized 3-cocycle on the grading group makes its restriction to H trivial. Concretely the only possible nontrivial twist is gamma(a,b,c)=(-1)^{abc}, for degrees a,b,c in {0,1}. This preserves every fusion coefficient and the pentagon. Replace C by this twist. The regular algebra A=1+u is now a connected separable algebra.

Let B be the fusion category of A-A bimodules in C. For a simple Y of C write F(Y)=A tensor Y tensor A for its free bimodule. Adjunction gives

    dim End_B(F(Y)) = dim Hom_C(Y,A tensor Y tensor A)
                    = #{(h,k) in H×H : hYk=Y}.

For an invertible Y this number is two. Its H×H orbit consists of two invertibles, and each occurs twice in the underlying object of F(Y). The two-dimensional semisimple endomorphism algebra of F(Y) is C×C, so F(Y) splits into two distinct simple bimodules, each with multiplicity one. Each summand has H-stable nonzero underlying support, and hence contains both orbit objects. Their total multiplicities are two, so each summand contains each orbit object exactly once. Thus each has FP dimension 2/FPdim(A)=1. The two disjoint pointed orbits yield four invertibles in B.

For a noninvertible r the H×H orbit consists of r, ur, ru, uru=gr. They are all four distinct noninvertibles. Its stabilizer is trivial, so End_B(F(r))=C: F(r) is simple. It is the only noninvertible simple of B, since all simple bimodules occur in free bimodules and the three H×H orbits exhaust the source simples. Its FP dimension is

    (4 FPdim(r))/FPdim(A) = 2(2+sqrt(5)) = 4+2sqrt(5).

Call this simple Z. The four invertibles form a group G' of order four, hence G' is C4 or V4. Since Z is the unique noninvertible, it is fixed by every invertible and is self-dual. Frobenius reciprocity makes every invertible occur once in Z². Taking FP dimensions gives

    Z² = sum_{h in G'} h + 8 Z.

Therefore B categorifies the rank-five near-group ring R(G',8).

If G'=V4, this contradicts Schopieray, *Categorification of integral group rings extended by one dimension*, J. London Math. Soc.108 (2023), Theorem1.1. If G'=C4, it contradicts the rank-five manuscript's Theorem6.3 (cyclic-four central-support criterion), specialized to k=2 and moment height6. That theorem concerns arbitrary complex categorifications: its proof first takes the pseudo-unitary Galois conjugate and then uses exact central-support identities. The k=2 certificate has six branches: two force the nonintegral fusion coefficient k²/8=1/2, while the other four have integer separating vectors y with Aᵀy≥0 and bᵀy respectively −800, −220, −320, −80. Both possibilities are impossible. The complete archived source and its exact, optimizer-free replay are in `rank5_cyclic/`; its `verify.py` independently checks that its tensor is isomorphic to R(C4,8), enumerates all six branches, and checks every separating inequality. This is extracted from the earlier `Rank5_Unified_Frontier` bundle identified in `rank5_cyclic/provenance.json`; no hash identity with a later rank-five archive is asserted.

The grading twist is essential: a tensor alone does not assert that 1+u is already an algebra in the original category. Here the twist is available precisely because u lies in the nontrivial grading component. We only need to show that existence of C would imply existence of the forbidden Morita dual after an allowed associator twist.

## Source binding and replay

The flattened canonical source tensor R8_2_170 has SHA-256
`78c260875e85e75fa8689dba58a9c5225942228315e25da354ad3da8b4bbf06d`.
`verify_r170_morita.py --repo <repository-root>` verifies this immutable digest, the faithful grading, the pointed V4 multiplication, the conjugation relation, the three double-orbits and stabilizers, and the exact dimension equation. It also checks the normalized grading cocycle's pentagon and invokes `rank5_cyclic/verify.py` in an isolated process. The combined receipt reports PASS only after the cyclic terminal replay succeeds. Normal and `python -O` receipts agree.

The Klein-four terminal is the published general-complex theorem, not a unitary classification: A. Schopieray, *Categorification of integral group rings extended by one dimension*, J. London Math. Soc. 108 (2023), Theorem 1.1, DOI [10.1112/jlms.12789](https://doi.org/10.1112/jlms.12789), [arXiv:2208.07319](https://arxiv.org/abs/2208.07319). For G=V4 it leaves precisely near-group multiplicities 0 or 4, so 8 is excluded.

The Morita steps use only standard algebra-object theory in semisimple rigid tensor categories: a trivialized finite pointed subgroup has its separable regular algebra; connected separability makes the bimodule category fusion; every simple is a summand of a free bimodule by adjunction; and its dimension is the underlying object's FP dimension divided by FPdim(A). No spherical trace, C*-structure, or existence theorem for a 2D2 Q-system is used.
