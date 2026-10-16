# A second inversion-descent realization: R7_4_35

**Theorem.** The census ring R7_4_35 has a unitary categorification.
Together with R7_4_2665, this is obtained by one construction applied to
two established near-group inputs. The pointed cyclic associator and
the duality shift distinguish the two outputs.

We use the central base-change and monodromy lemmas proved in Sections
3--4 of `R2665_INVERSION_CONSTRUCTION.md`. The additional point needed
for the noncyclic parent group is supplied explicitly below.

## 1. The regular near-group Morita square for noncyclic groups

Let C=NG(G,|G|) be a unitary near-group category in Izumi's normalization,
with G abelian. Theorem 11.3 identifies its regular-G Morita dual with C
using the original labels. Let Mcal denote this self-Morita bimodule.
For its distinguished simple kappa, the left regular-G internal-end
algebra is untwisted. We claim the right internal-end algebra is also
untwisted, without requiring H²(G,C*)=0.

The right generators are alpha'_g=Ad U(-g)|_(M^alpha), and

    u_g=U(g): kappa alpha'_g -> kappa.

Izumi's U is an honest unitary representation of G, not a projective
one (the construction immediately preceding Theorem 4.1, and the
fixed-point calculation in Theorem 11.3). In the composition defining
the right-module cocycle, right whiskering of u_g by alpha'_h
precomposes the homomorphism and leaves its implementing intertwiner
U(g) unchanged. Thus the two-step composition is

    u_h composed with (u_g whiskered by alpha'_h)
       = U(h)U(g) = U(g+h) = u_(g+h).

In particular, one must not replace right whiskering by alpha'_h(U(g));
U(g) need not belong to M^alpha. The multiplication class is zero.
Taking the opposite module preserves the untwisted algebra. Hence
Mcal and its inverse are equivalent as left C-modules: both arise from
the same untwisted regular-G algebra. Their square is therefore the
regular bimodule with a tensor autoequivalence G0 on the right.

The center-label calculation in Section 2 of the R2665 proof applies
for arbitrary abelian G. Left and right actions on the free orbit of
|G| simples are opposite, so the center permutation is g -> -g.
The square fixes all central-invertible labels. Izumi Corollary 13.5
is faithful on those labels and forces G0=Id. Consequently Mcal² is
the regular bimodule. This removes the cyclic-group restriction from
the parent-square argument used for R2665.

## 2. The diagonal cyclic orbifold of the Yu--Zhang category

Use the established category of Yu--Zhang, Proposition 3.1:

    G=C4×C4,
    chi((x,y),(u,v))=i^(xu-yv),
    a(x,y)=exp(2*pi*i*3(x²-y²)/8), c=1.

Take the cyclic subgroup H=<(1,1)> of order four. Directly,

    H=H-perp, chi|_(H×H)=1, a|_H=1,
    G/H=C4, with generator r represented by (1,0).

Its central regular algebra A is commutative and separable. Izumi
Theorem 12.5 gives the unitary orbifold D=C_A with

    r⁴=1, rho r=r^(-1)rho,
    rho²=1+(1+r+r²+r³)rho.

There are four dimension-one simples and four dimension-t simples,
where t=2+sqrt(5). These are the self-dual C4 Haagerup--Izumi based
rules. This statement does not assume that D is one of the previously
classified subfactor categories with an algebra 1+rho.

In the crossed-product realization of this orbifold, alpha_(1,0)
extends to the crossed product by H with fourth power exactly the
identity: on the implementing lambda_(j,j) its action is multiplication
by i^j. Thus the four pointed objects have the strictly associative
C4 group law, and the restricted class in H³(C4,C*) is zero.

## 3. Descended inversion and coherence

The near-group Morita bimodule preserves A because its center action
is inversion. Descend it along A. The fixed simple of dimension four
splits into four dimension-one module simples, since H is cyclic and
the restricted internal-end algebra is untwisted. The sixteen free
orbit simples give four dimension-t module simples. As in Section 3
of the R2665 proof, action on these two sets proves that the descended
left module is regular. It therefore gives an actual tensor
autoequivalence F of D.

The left A-character shift is chi(h,(1,0)), whereas right transport
through U((1,0)) gives its inverse. Consequently F(r)=r^(-1).
Changing the algebra identification by a character of H composes F
with the canonical dual action T. Choose

    F(r)=r^(-1), F(rho)=r^(-1)rho.

The parent-square result of Section 1 and central base change give
F²=Inn(r^ell)T^j for some ell,j modulo four. The monodromy of the
central lift of (1,0) with H is chi((1,0),(k,k))²=(-1)^k, so

    T²=Inn(r).

The lift of (2,0) has trivial monodromy and makes r² central in D.
Since F² fixes all simple labels, 2ell+j=0 modulo four. Therefore
F²=Inn(r^(ell+j/2))=Id. The universal grading of D is trivial by its
rho² decomposition, so Aut_tensor(Id_D)=1 and the involution is
coherent. This is a genuine unitary C2 action.

## 4. Reflection dual and its integral group

The crossed product E=D semidirect_F C2 has

    r⁴=s²=1, srs=r^(-1), rho r=r^(-1)rho, rho s=rs rho,
    rho²=1+(1+r+r²+r³)rho.

Let B=1+s, an actual regular algebra supplied by the coherent C2
crossed product. Its Morita dual K has four invertibles, one simple
X of dimension two, and two simples Y,Z of dimension 2t, by the same
double-coset analysis as in the R2665 construction. Here rho*=rho,
and both irrational double orbits are self-dual, so Y*=Y and Z*=Z.

The integral subcategory is C(D8,<s>,Omega,psi), a Tambara--Yamagami
category on a group of order four. The restriction of Omega to the
rotation C4 is trivial, by Section 2. Every cyclic subgroup of D8 is
either contained in that C4 or has order two. For the latter, the
restriction of any 3-cocycle has order at most two. The formula of
Ng--Schauenburg, Theorem 9.2, therefore gives

    FSexp(K_int) divides 4.

This excludes a cyclic group of four invertibles. In fact, Shimizu
Theorem 3.4 and its immediately following specialization give, for
every TY(C4,chi,tau),

    nu_4(X) = (1/2) sum_(x in C4) chi(x,x)^(-1) = 1+i or 1-i,

because nondegeneracy forces chi(1,1)=i or -i. The answer is independent
of the sign of tau and is not FPdim(X)=2. But FS exponent dividing four
would force nu_4(X)=2. Thus the integral invertibles form V4.

Write them as {1,g,h,gh}, where {1,h} are supported on L={1,s}.
Then h fixes Y,Z and g,gh interchange them. This is the self-dual
V4 case R7_4_35.

## 5. Complete tensor and source binding

In basis (1,g,h,gh,X,Y,Z), the tensor is

    g²=h²=1, gh=hg, gX=hX=X,
    gY=Z, gZ=Y, hY=Y, hZ=Z,
    X²=1+g+h+gh, XY=YX=XZ=ZX=Y+Z,
    Y²=Z²=1+h+X+4Y+4Z,
    YZ=ZY=g+gh+X+4Y+4Z.

For the nonintegral and mixed products use the actual free bimodules
X=B r B, Y=B rho B, Z=B r²rho B and the relative-tensor isomorphism
(B u B) tensor_B (B v B)=B u B v B. Expansion gives all eight mixed
and irrational products. The TY integral rules and Frobenius
reciprocity distinguish the two invertibles sharing an underlying
pointed support, as in the R2665 proof.

The constructor in `verify_R35_inversion_model.py` is independent of
the census. It checks the finite-group hypotheses, all fusion axioms
in ranks seven and sixteen, the eight induction identities, the
two exact Shimizu indicators, and all 343 source coefficients, with

    model -> census: [0,1,5,2,6,3,4].

It imports only elementary tensor helpers from
`verify_R2665_inversion_model.py`, whose default construction is
unchanged. Receipts bind the tensors and original compressed source
by SHA-256. Categorical existence is supplied by Sections 1--4, not
by the finite associativity check.

## Sources and scope

The sources common to both constructions are listed in
`R2665_INVERSION_CONSTRUCTION.md`. Additional primary inputs are:

1. Zhiqiang Yu and Qing Zhang, *Realizing modular data from centers of
   near-group categories*, arXiv:2412.20763v2, Proposition 3.1 and
   Equation (13). https://arxiv.org/abs/2412.20763
2. Kenichi Shimizu, *Frobenius--Schur indicators in Tambara--Yamagami
   categories*, Journal of Algebra 332 (2011), 543--564,
   arXiv:1005.4500, Theorem 3.4 and the displayed nu_4 formula on the
   following page. https://arxiv.org/abs/1005.4500

This proves a unitary realization of R7_4_35. It does not prove a
realization or exclusion of R7_4_2053, R7_4_2603, or R7_4_2591.
