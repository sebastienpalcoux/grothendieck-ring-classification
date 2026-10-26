# Independent audit of the forced central lifts

## Outcome

The categorical premises behind the rank-12 C3 and semion reductions survive this audit. No new categorification or exclusion is obtained. In particular, no symmetry/isotropy follows merely from the central lift or from trivial universal grading.

## 1. Inner actions

Conjugation by invertible objects defines a tensor action of their group of isomorphism classes. The multiplication isomorphisms for chosen representatives need not be associative: their scalar associator is cancelled by the inverse scalar on the dual factor of conjugation. The action is also identified categorically with a relative center. A current primary source explicitly states and proves this in Gannon–Schopieray–Yadav, *On Haagerup–Izumi fusion categories*, Proposition 6.1, https://arxiv.org/pdf/2609.25185, pp.20–21. Its proposition is for any fusion category and pointed tensor subcategory; no odd-order or HI hypothesis enters that proposition.

Thus the argument is not assuming a subgroup algebra, a trivial ordinary pointed associator, or a genuine object-level group embedding in the strict category.

## 2. Explicit central embedding and its convention

Let Q be a pointed fusion subcategory of C and E=Z_Q(C). Write the relative half-braiding of Y in E as

    d^Y_V: V tensor Y -> Y tensor V,  V in Q.

The full subcategory of E lying over Q is Z(Q), represented with this left-half-braiding convention. For W in this subcategory define

    beta^W_Y = d^Y_W: W tensor Y -> Y tensor W.

This is an E-morphism, not merely a morphism in C. Indeed its compatibility with relative half-braidings is precisely naturality of d^Y against the morphism d^W_V: V W -> W V in Q:

    (beta^W_Y tensor id_V)(id_W tensor d^Y_V)(d^W_V tensor id_Y)
      = (id_Y tensor d^W_V)(d^Y_V tensor id_W)(id_V tensor beta^W_Y).

The relative hexagon for d^Y gives the displayed equality. The tensor-product rule for relative half-braidings gives the central hexagon for beta. This yields the standard fully faithful central embedding

    Z(Q)^rev -> Z(E).

The reversal is important for conventions but immaterial to the alternatives under consideration: it exchanges the two nondegenerate C3 braidings and the two semion signs. This proof establishes that every equivariant lift of a fixed invertible in Q has a central lift in E; it does not require selecting a preferred equivariant structure.

## 3. Restriction through the adjoint section

The complete finite ring refinements in the preceding packet make E_ad -> C a tensor equivalence. The underlying simple objects of the selected central lifts lie in E_ad, hence their half-braidings restrict to E_ad. For an invertible object, two half-braidings differ by a monoidal natural automorphism of the identity. Such automorphisms are characters of the universal grading group. Since U(E_ad)=1, the half-braiding is unique. Products and powers of the selected objects therefore acquire exactly the selected half-braidings; their group law holds in the center, not only after forgetting.

This validates the order-three central subgroup for R561/R628 and the order-two central subgroup for R623. The previously proved nu_2(z)=-1 in the positive spherical category yields the nontrivial ordinary C2 associator. Consequently the central C2 must be semionic, rather than Tannakian or fermionic.

## 4. Regular C3 algebra and alpha induction

For the C3 subcategory, the ordinary pointed associator is trivial and the regular algebra A exists. In either nondegenerate bicharacter branch, the alpha-induction tensor functor C -> A-bimod(C) is fully faithful. A left-linear map has components f_h: X -> hY; compatibility with right multiplication by k gives

    (b(k,h)-1) f_h = 0.

Nondegeneracy forces h=1. Equal Frobenius–Perron dimensions give a tensor equivalence. This can also be checked directly in the pointed model Vec_H: alpha sends an object x to the character k -> b(k,x)^(-1) of the regular-algebra dual, an isomorphism exactly when b is nondegenerate. Hence the Morita step genuinely returns the original category; its rank-four one-sided module category must not be treated as a fusion category.

## 5. No inferred extra splitting

The central embedding is into Z(C), not a braiding on C. Müger decomposition applies to Z(C). It does not split C into a Deligne product, nor does U(C)=1 force the central pointed subcategory to be symmetric. Any stronger obstruction must use additional data.
