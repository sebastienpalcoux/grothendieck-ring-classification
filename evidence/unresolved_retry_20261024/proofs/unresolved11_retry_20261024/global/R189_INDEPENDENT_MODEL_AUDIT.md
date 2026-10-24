# Independent categorical audit: an actual model for R10_1_189

**Verdict: the direct conformal-embedding construction is a unitary categorification.**
The argument below uses an existing category and an existing algebra. It does not infer a category from the rank-fourteen modular-data candidates.

Let C be the unitary WZW category SU(4) at level 6. The conformal embedding

    SU(4)_6 ⊂ SU(10)_1

coming from the ten-dimensional symmetric-square representation gives a connected commutative separable algebra B in C. In Dynkin-label notation its underlying object is

    B = 000 ⊕ 060 ⊕ 202 ⊕ 222.

This is the vacuum branching rule of an actual conformal embedding, not an assumed algebra on a candidate object. Let D=C_B, with its relative tensor product, and let F:C→D be free induction. Then F is a central tensor functor (DMNO, §§3.3–3.4). In particular each F(v) commutes with every object of D. The local module subcategory is SU(10)_1, hence pointed with simples τ_j, j∈Z/10, satisfying τ_j τ_l=τ_{j+l}.

The required published branching rules, in one orientation of the generator, are:

| j | Underlying object R(τ_j) in C |
|---|---|
| 0 | 000 + 060 + 202 + 222 |
| 1 | 200 + 212 + 042 |
| 2 | 012 + 230 + 303 |
| 3 | 030 + 103 + 321 |
| 4 | 400 + 121 + 024 |
| 5 | 600 + 006 + 220 + 022 |
| 6 | 004 + 121 + 420 |
| 7 | 030 + 301 + 123 |
| 8 | 210 + 032 + 303 |
| 9 | 002 + 212 + 240 |

The opposite orientation exchanges j with −j and changes none of the conclusions.

Put v=010 and β=F(v). The ordinary SU(4) exterior-Pieri rule gives

    v² = 000 + 101 + 020,
    v³ = 3·010 + 2·111 + 030 + 200 + 002.

No affine truncation occurs: all relevant dominant highest weights lie strictly inside the level-six alcove. The quantum Weyl formula gives dim(v)=d=2+√5, so d²=1+4d.

Free-induction adjunction and v*=v imply

    dim Hom_D(β, τ_j β) = dim Hom_C(v², R(τ_j)).

The displayed branching table makes this one when j=0 and zero otherwise. In particular β is simple. Tensoring by τ_j shows that the ten objects τ_jβ are pairwise nonisomorphic simples.

Similarly,

    dim Hom_D(β², τ_j β) = dim Hom_C(v³, R(τ_j)).

This equals one precisely for j∈{1,3,7,9}, and zero for the other values of j. Since β is self-dual, β² also contains the unit with multiplicity one. These known constituents already have dimension 1+4d=d². Positivity of FP dimensions proves that they exhaust the product:

    β² = 1 + τ_1β + τ_3β + τ_7β + τ_9β.

Now set g=τ_2 and x=τ_5β. The object g has order five, x is self-dual, and gx=xg because β is central and the τ_j form a cyclic group. Since τ_5²=1,

    x² = 1 + (g+g²+g³+g⁴)x.

The ten pairwise distinct simples

    1,g,g²,g³,g⁴,x,gx,g²x,g³x,g⁴x

are closed under tensor products and duals. Their full additive subcategory is therefore an actual unitary fusion subcategory of D, with exactly the defining based ring of R10_1_189. This establishes existence without any completion or uniqueness premise about modular data.

## The initially proposed intermediate algebra is also legitimate

The alternative semion-centralizer description uses L=1+060⊂B. This is a genuine algebra inclusion, not merely a direct summand assertion. In any connected separable algebra B, its regular right module is simple. If an invertible g occurs in B, multiplication g⊗B→B is a nonzero right-B-module map between simple modules, hence an isomorphism. Its g⊗g→1 component is nonzero when g has order two and the unit multiplicity is one. Thus multiplication restricts to 1+g. Commutativity is inherited from B. This confirms that the proposed L inclusion has no missing categorical premise, although it is unnecessary for the direct rank-ten proof.

## Primary sources and scope

1. R. Coquereaux and G. Schieber, *Quantum symmetries for exceptional SU(4) modular invariants associated with conformal embeddings*, SIGMA 5 (2009), 044, §1.4.3 and §1.4.5. The former gives all ten branching blocks; the latter identifies the vacuum object and its dimension 20+8√5. https://arxiv.org/html/0805.4678v4 ; https://sigma-journal.com/2009/044/.
2. J. Böckenhauer and D. E. Evans, *Modular invariants from subfactors*, the SU(4)_6⊂SU(10)_1 example. This supplies the conformal-net/subfactor realization, including the unitary setting. https://arxiv.org/abs/math/0006114.
3. Y.-Z. Huang, A. Kirillov Jr. and J. Lepowsky, *Braided tensor categories and extensions of vertex operator algebras*, Comm. Math. Phys. 337 (2015), 1143–1159. This identifies suitable VOA extensions with commutative algebra objects and local modules with extension modules. https://doi.org/10.1007/s00220-015-2292-1 ; https://arxiv.org/abs/1406.3420.
4. A. Davydov, M. Müger, D. Nikshych and V. Ostrik, *The Witt group of non-degenerate braided fusion categories*, §3.3 (C_B is fusion and F is tensor), §3.4 and equation (17) (F lifts to Z(C_B)), and Corollary 3.30 (center decomposition). The proof only needs the explicitly constructed central lift of F; no stronger assertion about local modules is necessary. https://arxiv.org/pdf/1009.2117 (version 2).

The use of unitarity here is an existence statement: we construct a unitary category. No theorem about arbitrary original spherical categories or their unitarizability is used.
