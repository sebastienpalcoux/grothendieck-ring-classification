# A uniform extension theorem for the eight Tambara–Yamagami categories of dimension 8

## Conclusion and exact scope

Let T=TY(A,χ,τ), where |A|=4 and τ=±1/2, over C.

1. If A=C4, every finite-group extension of T is group-theoretical.
2. If A=V4 and χ is alternating, every finite-group extension of T is group-theoretical.
3. If A=V4 and χ is nonalternating, BrPic(T) is a 2-group, for either sign of τ. In particular, a C3 extension has three regular bimodule components and rank15.

Consequently, suppose B is an S3-graded fusion category with neutral component T and its C3 subextension has rank9 and type (1^4,2^5). Then B is group-theoretical. The nonalternating V4 case is impossible by (3), and (1)–(2) cover all remaining cases.

These are general-complex statements. The TY classification itself parameterizes every such category; no assertion that a unitary table exhausts arbitrary spherical categories is used.

## The center formulas needed

We use Gelaki–Naidu–Nikshych, *Centers of graded fusion categories*, arXiv:0905.3117, Proposition4.1 and Section4.3. The center has eight invertible simples X_(a,ε), ε²=χ(a,a)^−1, six two-dimensional simples Y_(a,b) with a≠b unordered, and eight two-dimensional simples Z_(ρ,Δ).

The canonical positive twists and the relevant unnormalized S entries are

    θ_X(a,ε)=χ(a,a)^−1,       θ_Y(a,b)=χ(a,b)^−1,
    S_X(a,ε),X(b,δ)=χ(a,b)^2,
    S_X(a,ε),Y(b,c)=2χ(a,b+c),
    S_X(a,ε),Z(ρ,Δ)=2ερ(a).

In particular e=X_(0,−1) has twist1, centralizes all X and Y, and has S_(e,Z)=−2. Thus e never centralizes a Z simple.

The center is pseudo-unitary, its dimension is64, and every braided autoequivalence preserves its canonical positive spherical structure and twists. A Lagrangian subcategory has dimension8 and consists of bosons. Since the only simple dimensions are1 and2, it has exactly one of the following two forms:

* eight invertible simples;
* four invertible simples and one two-dimensional simple.

There is no other numerical possibility: the tensor unit must be included, and two dimension2 simples already contribute8 before including it.

For completeness, the usual test S_(X,Y)=dim(X)dim(Y) detects centralization here. The monodromy eigenvalues are roots of unity and all categorical dimensions are positive, so equality in the triangle inequality forces every monodromy eigenvalue to be1. Conversely centralization gives this equality. A set of twist1, pairwise-centralizing simples generates a symmetric twist1 category, hence a Tannakian category. Its dimension is at most8 because it embeds in its centralizer in a dimension64 modular category. Therefore a seed already of squared-dimension sum8 is automatically fusion closed and Lagrangian.

## Alternating V4: a characteristic Lagrangian

If χ is alternating, χ(a,a)=1 and χ(a,b)^2=1 for all a,b. Hence all eight center invertibles have twist1 and centralize each other. They form a Lagrangian subcategory of dimension8. This is the entire maximal pointed subcategory of the center, so every braided autoequivalence preserves it.

For any group grading extending T, the induced group action on Z(T) therefore preserves this Lagrangian. GNN Corollary3.10 proves that the extension is group-theoretical. The sign of τ never enters this argument.

## Cyclic C4: the unique Lagrangian

Write A=Z/4 and χ(a,b)=i^(sab), s=1 or3. Precisely four invertible center objects are bosons: X_(0,±1),X_(2,±1). A Lagrangian must contain these four and one dimension2 object; the eight-invertible alternative is unavailable.

Since these four include e, the additional object cannot be a Z. A bosonic Y_(a,b) requires χ(a,b)=1. To centralize X_(2,±1) it also requires χ(2,a+b)=1, so a+b is even. Among distinct a,b in Z/4 these two conditions leave exactly {a,b}={0,2}.

The set

    {X_(0,±1), X_(2,±1), Y_(0,2)}

is pairwise centralizing and of dimension8, so it is Lagrangian. It is the unique one. Hence every braided autoequivalence preserves it, and GNN Corollary3.10 proves that every group extension is group-theoretical, for either s and either τ.

## Nonalternating V4: exactly two Lagrangians and a 2-group BrPic

Choose a,b generating V4 with χ(a,a)=χ(b,b)=−1, χ(a,b)=1, and put h=a+b. The only bosonic invertibles are X_(0,±1),X_(h,±1), so they all belong to any Lagrangian. Again e excludes every Z simple.

The Y twist and centralization formulas leave precisely Y_(0,h) and Y_(a,b). They give the two Lagrangians

    L0={X_(0,±1),X_(h,±1),Y_(0,h)},
    L1={X_(0,±1),X_(h,±1),Y_(a,b)}.

Both are Tannakian representation categories of a nonabelian group of order8, since their simple dimensions are1,1,1,1,2. Both are Rep(D8), rather than Rep(Q8). Here is a direct way to distinguish them that is insensitive to τ.

Under the canonical pivotal forgetful functor Z(T)→T, their dimension2 simple Y_(u,v) becomes u⊕v with u≠v and u²=v²=1 inside the untwisted pointed subcategory Vec_V4. On Hom_T(1,(u⊕v)²), the second-indicator rotation is the identity: the only two summands are Hom(1,u²) and Hom(1,v²), and each order2 invertible in Vec_V4 has second indicator+1. The central Hom space is a rotation-invariant subspace, and is one-dimensional because Y is self-dual and simple in the Lagrangian. Restriction of the identity is the identity, so ν2(Y)=+1. The unique two-dimensional irreducible representation of D8 has indicator+1, whereas that of Q8 has indicator−1. Thus both Lagrangians are Rep(D8).

Each Lagrangian determines a pointed Morita presentation Vec_D8^ω of T. The subgroup of BrPic(T)=Aut_br Z(T) stabilizing this Lagrangian is the image of Aut_⊗(Vec_D8^ω). This is the standard Lagrangian stabilizer/induction theorem (Marshall–Nikshych, Section3; equivalently the canonical regular algebra of Rep(D8) is preserved).

The tensor-auto-equivalence group of Vec_D8^ω is an extension of a subgroup of Aut(D8) by H²(D8,C×). The former is a2-group (indeed |Aut(D8)|=8) and the latter is a2-group by finite-group cohomology (indeed C2). Therefore the stabilizer is a2-group. Its orbit on the two Lagrangians has size1 or2, so the whole BrPic(T) is a2-group. This proves the assertion for both τ signs without computing the full group or invoking a classification limited to the Kac–Paljutkin sign.

Any homomorphism C3→BrPic(T) is consequently trivial. Each homogeneous component of a C3 extension is then the regular T-bimodule class and has five simple objects. The extension has rank15, incompatible with rank9. This last inference uses the bimodule-class homomorphism of extension theory; it does not assert that the whole extension is a strict tensor product or that all its associator classes vanish.

## Independent exact verification

The portable script `verify_TY8_lagrangians.py` uses integer arithmetic in Q(zeta16), checks all four bicharacters and both τ signs, validates all quadratic-refinement equations, and checks exact unitarity of each22×22 S matrix. It then exhausts the two numerical Lagrangian shapes above. Under python−O it returns:

| A and bicharacter | τ=+1/2 | τ=−1/2 |
|---|---:|---:|
| V4, alternating | 7 | 5 |
| V4, nonalternating | 2 | 2 |
| C4, χ(a,b)=i^(ab) | 1 | 1 |
| C4, χ(a,b)=i^(3ab) | 1 | 1 |

Thus, even without the stronger characteristic-Lagrangian and BrPic arguments, every C3 extension of every TY category of dimension8 is group-theoretical: a C3 action on a finite set whose size is not divisible by3 has a fixed point, and GNN Corollary3.10 applies.

The short structural proof above is the main argument. The exact enumeration is a bounded independent check, not a search over associator solutions.

## Sources

* Gelaki–Naidu–Nikshych, https://arxiv.org/pdf/0905.3117, Proposition4.1, Section4.3, Corollary3.10.
* Marshall–Nikshych, https://arxiv.org/pdf/1603.04318, Sections2.3 and3 (tensor autoequivalences, induction and Lagrangian stabilizers); Proposition6.30 independently confirms the positive nonalternating Kac–Paljutkin case.
* Tambara–Yamagami classification as recalled in GNN Section4.1; the symmetric bicharacters on groups of order4 have exactly the four forms treated here.

No online files or existing classification artifacts are changed by this note.
