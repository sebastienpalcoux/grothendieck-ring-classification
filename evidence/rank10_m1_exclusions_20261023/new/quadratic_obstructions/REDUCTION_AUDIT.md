# Exact reduction audit

This note audits the necessary Morita dual for R10_1_114,115,152,153,179, with R10_1_21 as a realized control. It does not independently assert that a necessary based ring has a categorification. The subsequent pseudo-branch exclusion is proved in `../rank16_dual/PSEUDO_BRANCH_EXCLUSION.md`.

## Completeness of the finite matrix step

The categorical arguments in `MORITA_REDUCTION.md` first prove, without a pivotal, unitary, or braiding assumption, that the A-bimodule category has exactly sixteen simple objects, two over each of the eight simple right A-modules. They also determine the complete eight-dimensional left C-action. The finite calculation starts only after these facts have been proved.

Let w be its positive dimension vector, normalized to have w_0=1 at A. Its entries belong to {1,δ,δ²}, where δ=1+sqrt(2). Let S be the sum of the ten left action matrices. Module duality makes S symmetric; indecomposability makes S irreducible. Consequently any nonnegative matrix B commuting with the left action satisfies Bw=λw and wᵀB=λwᵀ. If B e_0=e_m, then λ=w_m. Therefore

    0 ≤ B_ij ≤ λ w_i/w_j ≤ δ⁴ = 17+12sqrt(2) < 34.

The last strict inequality is exact: 12sqrt(2)<17 follows from 288<289. Every integer entry is in 0,...,33. No arbitrary numerical cutoff is used.

The exact rational commutant has dimension twelve. Prescribing column zero leaves four free parameters for each of the eight columns. The verifier explicitly finds an entry equal to each parameter; thus the parameters themselves are nonnegative integers in 0,...,33. It applies only necessary linear inequalities to narrow these ranges, then enumerates every remaining parameter tuple and checks all sixty-four entries for nonnegative integrality. Exactly two matrices remain for each unit column. The derived ranges, parameter entry locations, and counts are recorded in `commutant_completeness_receipt.json`.

Let T fix the four free modules and exchange the two pairs of split modules. For each candidate B_j the exact identity B_j T=B_(j xor 1) holds, with the same unit column and with distinct matrices. Categorically, T is tensoring with the sign bimodule ε. The two left equivariant structures on a fixed right module differ by ε⊗_A−, which acts by right multiplication by T on these matrices. Thus the two actual simple bimodules cannot have the same action matrix: both computed candidates must occur. This is the step that converts candidate enumeration into a forced simple basis.

Every nonnegative decomposition of B_i B_j is exhausted by its unit column: for each module m, the sum of the coefficients of the two candidates over m must equal (B_i B_j)_(m,0). The verifier ranges one coefficient over 0,...,(B_i B_j)_(m,0); the other is then forced. This yields one decomposition for 240 of the 256 ordered products and seven decompositions for each of the remaining sixteen products. The latter are exactly the products of δ²-dimensional objects. Each such object has already been identified as a simple product of two δ-dimensional objects, so associativity with the determined δ rows forces every remaining product. No associativity solution is chosen arbitrarily.

The stored fusion tensor uses matrix composition and hence is the opposite of the literal A-bimodule tensor product under its labeling. It is the tensor of End_C(C_A). All exclusions are unchanged by this convention. The canonical sign involution is index 0; the tensor unit is index 1.

## Relative factorization: direct categorical proof

Use the two rank-four subcategories C,E of the forced rank-eight adjoint category B, with common simples 1,f, and their complementary C-bimodule subcategory M. Fix a noninvertible simple Y in E. The functor L:C→M, X↦X⊗Y, is a left C-module equivalence, since it bijects the simple bases. Transport of the right action identifies M with the twisted regular bimodule C_φ for a tensor autoequivalence φ. It fixes every simple class because XY and YX have the same simple class.

Here is the precise twisted-center step. There is a standard identification

    C_φ ⊠_C C_φ ≃ C_(φ²),

under which the representative Y⊠Y corresponds to the tensor unit. Multiplication in B followed by projection to M is a C-bimodule functor C_(φ²)→C_φ. A left-module functor between these regular left modules is tensoring on the right by its value V at the unit. In the present case V=1⊕f, since the M-part of Y² is Y⊕fY. Its right-module constraint gives coherent natural isomorphisms

    φ²(X)⊗V ≃ V⊗φ(X).

Replacing X by φ⁻¹(X) gives the twisted half-braiding φ(X)⊗V≃V⊗X. For simple X, its two source constituents are φ(X) and φ(X)f, and the target constituents are X and fX. Because φ fixes the simple classes and f acts freely, these are two distinct simple classes. Thus the maps are block diagonal with respect to V=1⊕f. This holds naturally for all objects, and the unit projection and inclusion are morphisms of the twisted central object. The unit block gives coherent natural maps φ(X)→X, hence a tensor isomorphism φ≃Id.

This argument does not require projection to M to be a tensor functor: it is used only as a C-bimodule functor. The decomposition B=C⊕M is by C-bimodule subcategories, so its projection is indeed such a functor. Nor does it assume that arbitrary subobjects of twisted central objects inherit half-braidings: inheritance follows here from the verified block diagonal maps.

After φ≃Id, the left module equivalence L can be made a C-bimodule equivalence. Its value Y=L(1) therefore has an ordinary relative half-braiding with C.

For closure under summands, if Z is an E-object equipped with relative half-braiding and Z=⊕Z_i is a multiplicity-free decomposition into E-simples, then for every simple X in C the objects XZ_i are pairwise distinct simples. Hence the relative half-braiding is block diagonal in these summands and each Z_i inherits one. Starting with Y, its square contains both noninvertible E-simples; in the pseudo case it also contains f, while in the ordinary case Y⊗(fY) contains f. Thus tensor powers and their simple summands, together with the unit, produce all of E. Two half-braidings on an E-simple differ by scalars λ_X on simple X in C. Their coherence makes these a character of U(C), which is trivial. Thus each such half-braiding is unique, all E morphisms are central, and the resulting lift E→Z_C(B) is tensor. This establishes coherent cross-commutation without an exact-factorization hypothesis C∩E=Vec.

The central self-braidings of f in the two factors are inverse, while conjugation by the canonical sign object exchanges the factors and makes them equal. Therefore q²=1. The unique-central-lift assertion uses Aut⊗(Id_C)=Hom(U(C),C×)=1; it does not confuse this group with the group of tensor autoequivalences acting trivially on simple classes.

## Independent proof that φ is trivial

`SOFT_AUT_THEOREM.md` proves the stronger statement that any tensor autoequivalence fixing all simple classes in either of these rank-four based rings is tensor-isomorphic to the identity. It does not require the ambient category B. Its finite integer lattice calculation uses only forced nonzero one-by-one associator blocks, all possible remaining blocks, and ENO rigidity of tensor functors; it assumes no F-symbol nonvanishing pattern beyond invertibility of one-by-one blocks. This supplies an independent backup for the direct twisted-center argument above.

## What remains outside this reduction

Determination of a based ring does not classify its associators. The new relative factorization is the extra categorical input needed to constrain those associators. For the pseudo branch, the q=+1 possibility reduces to Ostrik's excluded rank-two K_2 ring, and q=-1 reduces to the finite odd-evaluation rank-two superpentagon exclusion, as detailed and sourced in `../rank16_dual/PSEUDO_BRANCH_EXCLUSION.md`. The ordinary branch requires its own extension/descent argument. No ordinary-branch exclusion follows from these matrix calculations alone.
