# Exclusion of R10_1_152, R10_1_153 and R10_1_179

**Conclusion.** These three based rings admit no fusion categorification over the complex numbers. The argument combines a new theoretical Morita/relative-factorization reduction with a specific published finite superpentagon exclusion. It does not use unitarity, a unitary classification, or the conjectural unrestricted classification of rank-two superfusion categories.

## 1. Categorical reduction supplied by the forced dual

Assume one of the three rank-ten rings has a fusion categorification. The involution algebra A=1+h, constructed in `../quadratic_obstructions`, produces a rank-sixteen Morita dual D. The exact forced tensors and their categorical derivation are recorded there. The independent verifier `verify_subcategories.py` checks the following statements directly in each tensor.

The adjoint subcategory B=D_ad contains two rank-four fusion subcategories C and E. Their intersection is the pointed category on 1,f. Both have the non-self-dual pseudo-PSU(2)_6 based ring, with simples 1,f,x,y and products

    f²=1,  fx=xf=y,  fy=yf=x,
    x²=y²=f+x+y,  xy=yx=1+x+y.

In particular x*=y. Each cross product of a simple C-object with a simple E-object is simple, and tensoring by a fixed simple in either factor maps the other factor's four simples to distinct simples. Conjugation by the canonical sign bimodule tau exchanges C and E, fixing their common f.

The proof in `RELATIVE_FACTORIZATION.md` shows that C and E coherently commute: E lifts to the relative center Z_C(B). The central lift of f in either rank-four category is unique because its universal grading is trivial. If q_C,q_E are the scalar self-braidings of these lifts, cross-commutation gives q_E=q_C^{-1}. The tensor equivalence induced by conjugation by tau gives q_E=q_C. Thus q_C²=1.

The unique central lift of f has order two as an object of Z(C). Indeed its square lies over the tensor unit, and central lifts of the unit are tensor automorphisms of Id_C; these are trivial because U(C)=1. Therefore q_C=1 would make this central pointed subcategory Rep(C2), while q_C=-1 would make it sVec.

## 2. The bosonic alternative is impossible

If q_C=1, the central algebra 1+f is connected, commutative and separable. Its right modules form a fusion category. The action of f on the simples of C is free, with orbits {1,f} and {x,y}, so this module category has two simples. Under the free module tensor functor, x and y have the same image W, and

    W²=1+2W.

This is the rank-two based ring K_2, excluded over the complex numbers by Ostrik's classification of rank-two fusion categories. Hence q_C=-1: C is a fusion category over sVec.

## 3. The fermionic alternative gives an excluded rank-two super fusion rule

Use the standard associated-superfusion construction for a fusion category over sVec (Usher, Definition 4.9, following Brundan--Ellis). If the central fermion is f, the associated Pi-complete superfusion category has the same objects, with super morphism spaces

    Hom_hatC(U,V)_even = Hom_C(U,V),
    Hom_hatC(U,V)_odd  = Hom_C(U,f tensor V).

Composition and tensor product use the central structure of f and a central isomorphism f² -> 1. The self-braiding -1 supplies precisely the Koszul sign in the super interchange law. This construction assumes only a complex fusion category over sVec; it requires no pivotal or unitary structure.

In this supercategory, 1 and f are oddly isomorphic, as are x and y. Up to homogeneous isomorphism there are two simple representatives I=1 and W=x. They are both m-type: their endomorphism superalgebras are C in even degree, since neither 1 nor x is fixed by f. The superdimensions of the fusion spaces follow directly from the displayed rank-four products:

| Fusion space | Even dimension | Odd dimension |
|---|---:|---:|
| Hom(W²,I) | 0 | 1 |
| Hom(W²,W) | 1 | 1 |
| Hom(IW,W), Hom(WI,W) | 1 | 0 |

Consequently this is the odd-evaluation rank-two m-type rule

    W² = Pi I + (1+Pi)W,

or, in Chang--Chen--Xu's notation, the family C-hat_m^(1,1), equation (3.2).

Chang--Chen--Xu, *Topological Defect Lines in Two Dimensional Fermionic CFTs*, Section 3, manuscript page 25, explicitly report solving the superpentagon systems for a finite list of pairs (n_b,n_f) including (1,1). Their list of surviving odd-evaluation families contains only (0,0). Thus the particular odd family (1,1) has no solution.

This is a stated finite polynomial-system exclusion, not their subsequent conjecture about all unbounded rank-two super fusion rules. Their calculation uses general complex gauge transformations and includes nonunitary solutions. Section 3.2.4 explicitly retains the odd (0,0) superpentagon solutions despite their failure of a proposed physical locality condition; that condition is therefore not used to discard the odd families. The required (1,1) case is excluded by the superpentagon equations themselves.

This contradicts the associated-superfusion construction. The assumed categorification does not exist. The identical argument applies to all three original rings. QED.

## Evidence and scope of verification

- `../quadratic_obstructions/R10_1_{152,153,179}_dual_tensor.json`: complete forced rank-sixteen fusion tensors, whose derivation requires the categorical module-action argument in that directory.
- `verify_subcategories.py` and `subcategories_receipt.json`: exact integer verification of the rank-four factors, free invertible actions, simple cross products, full faithfulness on simple bases, complementary bimodule, and swapping by tau.
- `RELATIVE_FACTORIZATION.md`: categorical proof of coherent cross-commutation without assuming disjoint factors.
- The final finite superpentagon nonexistence result is imported from the published literature. We have checked the exact family and stated scope in the primary paper; we have not independently rerun the authors' Mathematica/Magma calculation.

## Primary references

1. V. Ostrik, *Fusion categories of rank 2*, Math. Res. Lett. 10 (2003), 177--183; https://arxiv.org/abs/math/0203255 .
2. R. Usher, *Fermionic 6j-symbols in superfusion categories*, J. Algebra 503 (2018), 453--473; Definition 4.2 and Definition 4.9; https://arxiv.org/html/1606.03466v1 . Definition 4.9 gives exactly the even/odd Hom formula above, and Section 4 states its equivalence with the underlying-category construction.
3. C.-M. Chang, J. Chen, F. Xu, *Topological Defect Lines in Two Dimensional Fermionic CFTs*, SciPost Phys. 15 (2023), 216; Section 3, equation (3.2), manuscript page 25; https://arxiv.org/abs/2208.02757 and https://scipost.org/SciPostPhys.15.5.216 .
4. P. Etingof, D. Nikshych, V. Ostrik, *Twisted Deligne products of semisimple tensor categories*, https://arxiv.org/html/2607.19560v1 ; Sections 2.2 and 3.1 explain the twisted-center method adapted in our relative-factorization lemma.
