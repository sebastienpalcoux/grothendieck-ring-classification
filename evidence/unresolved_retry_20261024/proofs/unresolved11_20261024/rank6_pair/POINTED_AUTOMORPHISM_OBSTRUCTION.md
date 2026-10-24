# Central twist separation and pointed extensions of R6_4_155

## General criterion

Let C be a spherical fusion category whose pivotal structure is unique. Suppose every invertible simple a of C has a unique lift a~ to Z(C), and their canonical twists q(a)=theta(a~) are pairwise distinct. Then every complex-linear tensor autoequivalence of C fixes every invertible simple class.

Indeed, transporting the pivotal structure along a tensor autoequivalence F gives another pivotal structure, hence the same one. The induced braided equivalence Z(F) is therefore ribbon. It takes the unique lift of a to the unique lift of F(a), so q(F(a))=q(a). Twist separation gives F(a)=a.

Consequently, if C is a fusion subcategory of D and an invertible object r of D normalizes C, conjugation by r fixes every invertible class of C. In particular the subgroup Inv(C) is centralized by every invertible normalizer in D. This statement does not assert that D is braided or that conjugation by an invertible is the identity on all objects.

## Application to R6_4_155

Use basis 1,h,g,hg,X,Y and relations

    Y=X*, hX=X, gX=Y,
    XY=1+h+4X+4Y,
    X²=g+hg+4X+4Y.

Every tensor automorphism eta of the identity is scalar on simples. The occurrence of 1,X,Y in XY gives eta_X eta_Y=1=eta_X=eta_Y. The relation aX in {X,Y} then gives eta_a=1 for every invertible a. Thus Aut_tensor(Id_C) is trivial. Pivotal structures, when they exist, form a torsor for this group, so the spherical structure established in the published proof is unique.

The same argument proves uniqueness of an invertible's central lift: the ratio of two half-braidings on a fixed invertible is a scalar on each simple; their hexagons make those scalars a tensor automorphism of the identity.

The published center restrictions give central lifts of all four invertibles. In the positive spherical representative their twists, after choosing g, are

    q(1)=1, q(h)=-1, q(g)=i, q(hg)=-i.

These are the semion factor and the fermion in its modular centralizer. The precise project source is `manuscripts/rank6/papers/chapters/frontier_155.tex` (central-induction reduction) and `frontier_155_categorical.tex`, subsection “The canonical intermediate condensation adds no new near-group category”; that subsection already uses the distinct-twist observation. The present note isolates its general extension consequence rather than claiming the underlying observation is new.

The published spherical/Galois reduction covers every complex categorification of the ring. Transporting its center and spherical structure along the inverse field automorphism preserves the existence and uniqueness of the four lifts and pairwise distinctness of their twists. Hence the criterion applies to every original complex categorification, not merely to unitary categories.

## Nonabelian extension obstruction

No fusion category D can have all of the following:

1. a faithful C2 grading whose neutral component C has ring R6_4_155;
2. pointed group Inv(D) isomorphic to the dihedral group D8 of order eight;
3. Inv(C) is the normal Klein-four subgroup of Inv(D).

An invertible r outside C normalizes the neutral component, and conjugation by r swaps two elements of that Klein-four group. This contradicts the criterion. More generally, whenever an invertible-normalized R6_4_155 subcategory occurs, its four invertibles must be central in the invertible normalizer.

This is a genuine categorical obstruction to the stated extension, conditional only on the already published central-induction restrictions. It does not exclude R6_4_155 itself. It also cannot be applied merely because a based ring has the numerical dimensions of such an extension: the full fusion tensor must exhibit the neutral R6_4_155 subring and the stated conjugation action.

## Equivariantization consequence

For any coherent C2 action on a categorification of R6_4_155, all four invertibles are fixed. Since H²(C2,C×)=0, each fixed invertible has two inequivalent equivariant structures, giving eight invertibles in C^{C2}. Thus none of the rank-nine rings with dimension type (1^4,2,(4+3sqrt(2))^4) is obtained by such an equivariantization. This rules out a proposed construction route only; it is not an exclusion without a categorical inverse reduction.

## Primary background

EGNO, *Tensor Categories*, Proposition 9.5.1, gives uniqueness of the positive spherical structure in a pseudo-unitary category: https://math.mit.edu/~etingof/egnobookfinal.pdf . The proof above also uses the elementary torsor description of pivotal structures, functoriality of the Drinfeld center, and the definition of the twist from the braiding and pivotal structure. No classification or unitarization theorem for near-group categories is invoked.
