# The regular-algebra dual has the same based ring

This is a further necessary condition on a hypothetical categorification of R10_1_189. It does not prove equivalence of fusion categories or exclude the ring.

Work with a pseudo-unitary categorification C, put `d=2+sqrt5` and `D=5(1+d²)`, and use `POINTED_ASSOCIATOR.md` to take `C_pt=Vec_C5` with trivial associator. The connected separable algebra `A=sum_i g^i` exists.

## The dual's simple dimensions

The two simple right A-modules are `M0=A` and `M1=xA`. Indeed, the right C5-action on each of the two orbits of C-simples is free, and Frobenius reciprocity gives `End_A(xA)=Hom_C(x,xA)=C`. These two modules exhaust the category C_A. Their underlying C-dimensions are5 and5d.

Left tensoring by g preserves both right-module isomorphism classes: `gA` is isomorphic to A, and `gxA` is isomorphic to xA because `gx` is isomorphic to `xg` and `gA` is isomorphic to A. An A-bimodule is an equivariant object for this genuine left C5-action on C_A. Since `H²(C5,C×)=0`, each invariant simple right module has exactly five inequivalent equivariant structures, each of projective-representation dimension1. Therefore the dual fusion category `Dcat=_A C_A` has five simple objects of FP dimension1 and five of FP dimensiond. Here bimodule FP dimension is underlying C-dimension divided by FPdim(A)=5.

The five invertibles form C5. They act freely, hence transitively, on the five noninvertibles: a nontrivial stabilizer would be all C5, forcing all five invertibles into `YY*`, although its rational dimension coefficient is1 in `d²=1+4d`.

## All possible based rings with this dimension profile

Choose a noninvertible x. Because left and right C5-actions are free and transitive, there is an automorphism tau of C5 with `xg=g^tau x`. Write `x*=g^a x`. Applying duality twice gives `a=tau*a`; the unique invertible summand of x² is then `g^(-a)`. Associativity of x² with g implies `tau²=1`. If tau=-1, then a=0; if tau=1, replacing x by `g^(a/2)x` makes x self-dual. Thus a self-dual representative always exists.

For tau=-1, write `x²=1+sum_i m_i g^i x`. Comparing `(x²)g` and `x(xg)` gives `m_i=m_(i+2)` for all i. This would make all five multiplicities equal, contradicting `sum_i m_i=4`. Therefore tau=1, and the ring is commutative.

Self-duality gives `m_i=m_(-i)`, so

    x² = 1 + [m0+m1(g+g^-1)+m2(g²+g^-2)]x,
    m0+2m1+2m2=4.

Up to automorphisms of C5, the four possible triples are

    (4,0,0), (2,1,0), (0,2,0), (0,1,1).

The first contains the rank2 based subring `x²=1+4x`, which would give an actual rank2 fusion subcategory and is excluded by Ostrik's rank2 classification. This use of the rank2 theorem concerns a fusion subcategory of the dual; it does not apply that theorem to the rank2 module category C_A.

## The quadratic center field excludes the middle two rings

For a nontrivial fifth-root character value `g=zeta5`, let `t=m0+m1(zeta5+zeta5^-1)+m2(zeta5²+zeta5^-2)`. The scalar character sends x to a root w of `w²=1+t*w`. Its formal codegree is `f=5(1+w²)`. Consequently `y=f/5` satisfies

    y²-(t²+4)y+(t²+4)=0.

For the two middle triples, taking the norm from Q(sqrt5) gives:

| Triple | t | Polynomial for f/5 |
|---|---|---|
| (2,1,0) | (3+sqrt5)/2 | y⁴−15y³+60y²−90y+45 |
| (0,2,0) | −1+sqrt5 | y⁴−20y³+100y²−160y+80 |

Both polynomials are Eisenstein at5, so their roots, and hence these formal codegrees, have degree4 over Q.

The centers of Morita equivalent fusion categories are braided equivalent. In the pseudo-unitary structures this preserves FP dimensions. Every central simple of the original C restricts to a C-object, so its dimension is in Q(sqrt5). Thus every central simple of Dcat must also have dimension in Q(sqrt5).

On the other hand, the usual induction/formal-codegree theorem for the commutative Grothendieck ring of Dcat supplies a simple summand of `I_Dcat(1)` of dimension `D/f` for every scalar character. Since D lies in Q(sqrt5), a quartic formal codegree f makes `D/f` lie outside Q(sqrt5), a contradiction.

Only the fourth triple remains, which is exactly R10_1_189. Hence the regular-algebra Morita dual has the same based ring.

## Scope and remaining gap

This proves equality of based-ring isomorphism types, not that C and its dual are tensor equivalent. It does not produce a monoidal autoequivalence, a central lift of g, a braiding on C, or a tensor structure on C_A. None of those extra structures follows just from equality of fusion rules. The existence of a nonbraided categorification with trivial pointed associator remains unresolved.

References: Ostrik, *Fusion categories of rank2*, https://arxiv.org/abs/math/0203255; Schopieray, *Categorification of integral group rings extended by one dimension*, DOI10.1112/jlms.12789, for the scalar formal-codegree induction framework; the standard equivalence between Morita equivalence and braided equivalence of centers is also stated in Mignard–Schauenburg, §1, https://arxiv.org/html/1708.06538v1.
