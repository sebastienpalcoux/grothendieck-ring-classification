# What a central lift of the free involution would imply

This is a conditional reduction, not an assertion that such a lift exists.

Let C categorify one of R9_2_137, R9_2_1607, R9_2_1976. The unconditional TY-module argument in `ty_module_subtask/THEOREM.md` determines its integral subcategory D as TY(V4,χ,τ) with χ nonalternating. Write its anisotropic involutions as h1,h2 and its unique nonidentity isotropic involution as g=h1h2. The latter acts freely on all four dimension-d simples, where d=4+3√2.

Suppose, additionally, that g admits a half-braiding on C. Then C is a C2-equivariantization of a rank-six fusion category E with four invertibles and two self-dual noninvertibles X,Y. The group of invertibles of E is either V4 or C4. In either case there is an involution h and an element u outside {1,h} such that

hX=X, hY=Y, uX=Y, uY=X,

X²=Y²=1+h+4X+4Y,

XY=u+hu+4X+4Y.

The two possibilities for u² are 1 and h.

## Why the hypothetical lift is Tannakian

The universal grading of C is trivial. A half-braiding on the tensor unit is a tensor automorphism of the identity, so forgetting from Inv(Z(C)) to Inv(C) is injective. Any lift of g therefore has order two.

Restrict its half-braiding to D. The invertible central objects of a Tambara–Yamagami category have half-braiding on pointed objects given by χ(a,b); see Gelaki–Naidu–Nikshych, Proposition 4.1. In particular the self-braiding on g is χ(g,g)=1. Thus its generated rank-two symmetric category is Rep(C2). Its forgetful image is the full subcategory on 1,g, so central de-equivariantization applies to C and gives E with C≃E^{C2}.

This argument does not apply to h1 or h2: their self-braidings, if they lift, are −1. A fermionic central lift in a nonbraided category is not the same as a transparent fermion in a braided category. The latter's fixed-point exclusion cannot be used here.

## Exact quotient calculation

Condense the regular algebra 1+g. The invertibles of C form two free g-orbits, giving two invertibles of E. The dimension-two simple of D is g-fixed and splits into two further invertibles u,hu. Its square forces u²∈{1,h}. Therefore Inv(E) has order four and is either V4 or C4.

Each free orbit among the four large simples gives one simple of E of dimension d; there are two such orbits. In all three source tensors, duality preserves each free g-orbit. Thus both quotient simples are self-dual. Exact source multiplication then gives the displayed fusion rules, including the coefficient four of each of X,Y. The integral dimension is four and FPdim(E)=4+2d²=72+48√2.

`verify_central_lift_reduction.py` constructs both rank-six tensors, verifies all associativity and Frobenius-reciprocity identities, and checks all six source-to-quotient ring maps coefficient by coefficient. The matrix entry F[i,j] records the multiplicity of quotient basis element j in the image of source basis element i. These exact ring maps do not assert that a tensor functor exists without the central-lift premise.

## The precise literature boundary

For Inv(E)=V4 this is the self-dual rank-six ring R(4,4) in Meng–Yu, arXiv:2608.06064v1. Their Theorem 1.1 retains it, and the discussion preceding Conjecture 5.9 states that the remaining rings R(2,2), R(4,4), R′(4) are not categorified there. Thus even forcing this central lift would presently reduce the problem to a stated open rank-six case, not provide an exclusion. Their remark about a future C4-quadratic classification is not an available classification theorem.

In particular, {1,h,X} is not a fusion subring: X² contains Y with multiplicity four. It is invalid to replace this rank-six quotient with the excluded near-group ring C2+8 merely because d²=2+8d.

## Sources

- Gelaki–Naidu–Nikshych, *Centers of graded fusion categories*, Proposition 4.1: https://arxiv.org/pdf/0905.3117; published version https://msp.org/ant/2009/3-8/ant-v3-n8-p05-s.pdf.
- Drinfeld–Gelaki–Nikshych–Ostrik, *On braided fusion categories I*, Proposition 2.3, Theorem 4.18, Proposition 4.19: https://arxiv.org/pdf/0906.0620.
- Meng–Yu, *Classification of some Z/2Z×Z/2Z-quadratic fusion categories of rank 6*, Theorem 1.1 and the discussion before Conjecture 5.9: https://arxiv.org/pdf/2608.06064.
