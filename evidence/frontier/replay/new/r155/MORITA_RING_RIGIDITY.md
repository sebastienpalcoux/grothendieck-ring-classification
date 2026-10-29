# R6_4_155: complete connected-algebra reduction and Morita ring rigidity

Date: 29 October 2026. **Status: unresolved; no exclusion and no model.**

This note proves a stronger conditional structural result: every fusion category
Morita equivalent to a pseudo-unitary categorification of R6_4_155 has the same
based ring R6_4_155. Thus passing to a different Morita representative cannot
turn this case into a categorification of a different, already known ring.
This is rigidity of the based ring, not uniqueness of categorification or of
module-category structures.

## Premises and notation

The existing audited center reduction supplies the unique central lifts of all
four invertibles of a hypothetical pseudo-unitary category C. Write the simples
as 1,h,g,hg,X,Y, with g,h of order two, hX=X, gX=Y, X*=Y and

    XY=1+h+4(X+Y),     X²=Y²=g+hg+4(X+Y).

Put d=4+3√2 and D=FPdim(C)=72+48√2. The central lifts have twists
1,-1,i,-i after conjugation. In particular h is a central fermion, while
<g> and <hg> have nontrivial pointed associator. These are inherited categorical
premises, not consequences of a matrix calculation in this note.

Any indecomposable module category can be represented by a connected separable
algebra A: choose a simple generator and take its internal end. In the positive
pivotal normalization such algebras have nondegenerate Frobenius pairings, so
A≅A*. For a simple right A-module m one has

    FPdim(End_C(m)) = FPdim_C(m)² / FPdim_C(A).

The left side is an algebraic integer. These standard module dimension facts
are also used in the previous accepted A_k reduction.

## 1. Every connected algebra has one of six underlying objects

For an invertible a, free-module adjunction gives

    [A:a]=dim Hom_A(a⊗A,A).

Both free modules are simple, so this is zero or one. Their stabilizer is a
subgroup H of V4 on which the pointed associator must be trivial. Since g and
hg have the nontrivial C2 associator, H is either {1} or {1,h}. Selfduality
therefore puts every A in one of the families

    A_k=1+k(X+Y),       B_k=1+h+k(X+Y),        k≥0.

For A_k the preceding accepted Gram calculation leaves residual module vectors
(a_j,b_j) satisfying

    Σa_j²=Σb_j²=1+8k−4k²,       Σa_j b_j=8k−4k².

It forces k≤2. For k=1, the only viable residual modules have underlying
objects 2X+Y and X+2Y. For k=2 they are X and Y, whose internal ends have
underlying object 1+h. The algebra structure on 1+h is unique up to
isomorphism: the pointed associator is trivial there, and H²(C2,C*)=0
(equivalently, rescale the nonzero h²→1 multiplication). Thus A_2 has
the same module category as B_0. A_0 is the regular algebra.

Here is the complete complementary B_k calculation. The two distinct pointed
free modules have underlying objects B_k and gB_k. Every other simple module
has underlying object a_jX+b_jY. Subtracting the two free modules from the
induction Gram matrix gives

    q=2+8k−2k²,
    Σa_j²=Σb_j²=q,       Σa_j b_j=q−2.

Hence k≤4. For k=1 and k=3, q=8. Put c_j=a_j+b_j>0. Its internal-end dimension
is respectively

    c_j²(13+9√2)/7,       c_j²(5+3√2)/7.

Since the ring of integers of Q(√2) is Z[√2], integrality forces 7|c_j.
But c_j≤2√8<6, a contradiction. Therefore B_1 and B_3 are impossible.

For k=2, q=10 and the internal-end dimension is c_j²(1+2√2/3), so 3|c_j.
Furthermore Σc_j²=36 and c_j≤2√10<7. A single c_j=6 would force a_j=b_j=3
and contribute 9 to an inner product whose total is only 8; this is impossible.
There are therefore four residual modules, each with c_j=3. Since their total
Σ(a_j²+b_j²)=20, each has coefficients (1,2) or (2,1), twice each. Its internal
end has dimension 9+6√2=1+2d and hence underlying object 1+X+Y. Thus every
B_2-module category is represented by an algebra of underlying object A_1.
Conversely the accepted A_1 action gives internal ends B_2 at its two residual
simples, so this is exactly the same possible family of module categories.

For k=4, q=2 and the residual supports are disjoint. They are two copies each
of underlying X and underlying Y. Every such simple has internal-end dimension

    d²/(2+8d)=1.

It therefore gives the regular C-module category. Finally B_0=1+h is the
existing pointed-algebra category.

The complete underlying-object list is consequently

    1, 1+h, 1+X+Y, 1+2X+2Y,
    1+h+2X+2Y, 1+h+4X+4Y.

Of these, the only module-category type not already forced to be regular or
the 1+h module is A_1=1+X+Y. This statement does not assert existence or
uniqueness of algebra structures on A_1.

## 2. A central fermion gives a Morita self-equivalence without braiding C

Let f be a central fermion in any fusion category C, and let A=1⊕f be its
group algebra. The central half-braiding of A defines alpha induction

    α:C → {}_A C_A,       α(V)=V⊗A,

with the free right action and left action obtained by moving A past V via
its half-braiding. This is a strong tensor functor.

For completeness, its full faithfulness does not require a braiding on all
of C. A right-linear morphism α(V)→α(W) is determined on V⊗1 by

    t_0:V→W,       t_1:V→W⊗f.

Left f-linearity imposes no additional condition on t_0, by naturality of the
half-braiding. For t_1, use naturality with t_1 followed by the half-braiding
hexagon on W⊗f. The same comparison acquires precisely the scalar
c_{f,f}=−id_{f⊗f}. More explicitly, suppress associators and write m for
the multiplication f⊗f→1. The two left-linearity composites on f⊗V are

    (id_W⊗m)(t_1⊗id_f)c_{f,V},
    (id_W⊗m)(c_{f,W}⊗id_f)(id_f⊗t_1).

Naturality replaces (t_1⊗id_f)c_{f,V} by
c_{f,W⊗f}(id_f⊗t_1). The hexagon replaces c_{f,W⊗f} by
(id_W⊗c_{f,f})(c_{f,W}⊗id_f), which is the negative of the
second composite. Since m and the half-braidings are isomorphisms on these
summands, left linearity therefore forces t_1=0 in characteristic zero. Hence

    Hom_{A-A}(α(V),α(W)) = Hom_C(V,W).

Both fusion categories have dimension FPdim(C), so α is an equivalence.
This is the central version of the Clifford-algebra Azumaya argument. It uses
the fermionic self-braiding explicitly; it is not an inference from a
commutative Grothendieck ring. Taking f=h shows that the dual of C_{1+h}
is tensor equivalent to C.

## 3. Any A_1 algebra has dual based ring R6_4_155

Suppose A_1 exists. In the accepted module basis

    A_1,hA_1,gA_1,hgA_1,M,N,
    F(M)=2X+Y, F(N)=X+2Y,

the positive dimension vector is v=(1,1,1,1,√2,√2). The X action is

    [1 1 1 1 1 2]
    [1 1 1 1 1 2]
    [1 1 1 1 2 1]
    [1 1 1 1 2 1]
    [2 2 1 1 2 2]
    [1 1 2 2 2 2].

The four pointed actions are regular on the first four positions; h fixes M,N
and g exchanges them. Let D'=Fun_C(C_{A_1},C_{A_1}) (with the conventional
opposite if needed). Each simple dual object acts by a nonnegative integral
matrix commuting with these five matrices. Solving these elementary linear
equalities/equalities shows that every such matrix is uniquely

    [a b c e u v]
    [b a e c u v]
    [c e a b v u]
    [e c b a v u]
    [v v u u a+b c+e]
    [u u v v c+e a+b],

where all six parameters a,b,c,e,u,v are nonnegative integers. Put
p=a+b+c+e and q=u+v. Its eigenvalue on the positive module vector is
λ=p+q√2=FPdim(dual simple).

The regular-object action is

    Σ λ_j M_j = (D/(vᵀv)) vvᵀ = (D/8)vvᵀ.

Comparing the first four entries and the last two entries of the first row
separately, and then the rational and irrational coefficients, gives

    Σp_j²=36,       Σp_j q_j=24,       Σq_j²=18.

The inherited four central invertible lifts act as the four different pointed
permutations. Thus D' has at least these four simples with (p,q)=(1,0).
Remove them. Cauchy–Schwarz is then an equality:

    (Σp_j²)(Σq_j²) = 32·18 = 24² = (Σp_jq_j)².

Every remaining (p_j,q_j) is therefore t_j(4,3), with a positive integer t_j.
Since Σq_j²=18, Σt_j²=2: there are exactly two remaining simples, each of
dimension d. In particular no extra kernel invertibles or other integer-
dimension simples have been silently omitted.

Transpose swaps u and v and fixes a,b,c,e. Since u+v=3 is odd, neither of the
two large simples can be selfdual. They are dual to one another. The regular
matrix identity then gives a=b=c=e=1 for both; their (u,v) pairs add to (3,3).
The h action fixes each, and g exchanges them.

Call them Z,Z*. Frobenius reciprocity and their dimension force

    ZZ*=1+h+4(Z+Z*).

Indeed the pointed stabilizer is {1,h}, and selfduality of ZZ* makes the two
large coefficients equal; d²=2+8d then makes each coefficient four. Comparing
this identity in the action matrices gives uv=2. Together with u+v=3, this
forces (u,v)=(1,2) or (2,1); the possibilities (0,3),(3,0) fail.
The square identity is consequently

    Z²=g+hg+4(Z+Z*).

These are exactly the R6_4_155 rules. No faithfulness of the action on arbitrary
dual Grothendieck rings was assumed; the dimension argument first limits its
simples, and the resulting six matrices are linearly independent.

## Consequence and exact remaining gap

Sections 1–3 exhaust all connected-algebra types, so every Morita dual of a
pseudo-unitary categorification has based ring R6_4_155. This rules out a model
obtained by Morita equivalence from a category with a different based ring.
It does not exclude this ring, produce associators, force A_1, or prove that
the dual categorification is tensor equivalent to the original one in the A_1
case. The previous general-complex existence reduction supplies a
pseudo-unitary representative if a complex categorification exists; this note
does not claim that every original complex category is already pseudo-unitary.

The companion standard-library checker verifies the complete elementary Gram
reductions, the commutant equations, the six generating matrices, the
Cauchy coefficient identities, and the final two dual tensors. These finite
checks support the displayed arithmetic. The central-lift, module trace,
internal-end and alpha-induction categorical premises are explicitly separate.

Primary background: Davydov–Nikshych, *The Picard crossed module of a braided
tensor category*, arXiv:1202.0061, §3.2, for the braided Azumaya formulation;
the elementary half-braiding argument in §2 is its central special case.
