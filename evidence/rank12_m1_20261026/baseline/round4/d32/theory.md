# Dimension32 multiplicity-one Morita-source classification

Status: accepted after separate independent reviews of the categorical converse, all142 constructions, both new positive models, and every nonisomorphism test. This resolves all18 input cases: two unitary models and16 exclusions from general complex categorification. The independent audit is recorded in ../audit_models/d32_exhaustion_audit.md.

## 1. A forced algebra in the integral neutral category

Every target has type 1^8,2^2,(sqrt8)^2 and adjoint dimensions32,16,4,1. Thus any complex categorification C is nilpotent, hence unitarizable (Galindo–Hong–Rowell, Theorem5.20). Its integral adjoint category D has invertible group G8, two dimension-two simples X,Y, and common stabilizer H4. Liptrap reconstruction gives nondegenerate bicharacters B_X,B_Y on H, and H is abelian.

Choose g in G outside H, write P=Ad_g on H, and let Y=gX. Since g² belongs to H, P²=1. Restricting Liptrap biderivation and quasisymmetry to H gives

    B_Y(a,b)=B_X(Pa,b),       B_{X*}(a,b)=B_X(b,a).

For the first identity, compare biderivation at (g,a,b,X) with that at (gag^-1,g,b,X); all upsilon ratios cancel because b fixes every noninvertible. The inverse of P equals P.

There is a nonidentity involution h in H fixed by P with B_X(h,h)=B_Y(h,h)=1.

* For H=C4, take its unique involution; bilinearity makes both diagonal values one.
* For H=F2², write bicharacters as nonsingular matrices. If X*=Y, then P is a cosquare. A nonsymmetric2x2 matrix has nonsingular alternating difference B+B^T, whereas an involution P has rank(P−1)≤1. Thus B is symmetric and P=1; a symmetric form in dimension2 has a nonzero isotropic vector.
* If X*=X, both forms are symmetric, so P^T B=BP and P is an orthogonal involution. If P=1 use an isotropic vector. Otherwise its fixed line equals its image(P−1); every vector on that line is isotropic, since B((P−1)v,(P−1)v)=0.

The subgroup <h> has trivial associator class: X is a rank-one module for the pointed category Vec_H^alpha, so its action scalars trivialize alpha|H. Therefore A=1+h is an actual connected separable algebra. No central lift or braiding is being assumed.

The neutral dual _A D_A is pointed of dimension16. The pointed part contributes eight invertibles (h is central in G8). Each of X,Y has stabilizer C2×C2; its projective commutator is B_X(h,h), respectively B_Y(h,h), which equals one. Hence each gives four one-dimensional projective stabilizer representations, and therefore four invertible bimodules. This totals16.

Consequently E=_A C_A is a C2 extension of a pointed category of dimension16. The odd component is an indecomposable module over the pointed neutral part, hence its invertibles act transitively on simples. If H is their common stabilizer, each odd simple has dimension sqrt(|H|). Nonintegrality and total odd dimension16 allow exactly

    16 invertibles + 2 simples of dimension sqrt8,
    16 invertibles + 8 simples of dimension sqrt2.

The inverse Morita algebra B has FP dimension2, is connected, and has the form1+c for an invertible involution c of E. Its associator restricts trivially to <c>. Since all odd simples are nonintegral, B is neutral. Thus C is recovered as _B E_B with the grading preserved. The original integral neutral type1^8,2² forces

    |C_{G(E)}(c)|=8.

Indeed each double coset in the centralizer has size2 and gives two invertible bimodules; other double cosets have size4 and give one dimension-two bimodule.

## 2. Sources with two sqrt8 simples

Here the common stabilizer H is abelian of order8, G(E)/H=C2, and the universal grading group has order4. Let g represent G/H and P=Ad_g|H. The same bicharacter identities hold.

If the universal grading is C4, the two odd simples are dual, so P is the cosquare of a nondegenerate bicharacter of H and P²=1. For every abelian group H of order8, an involutive cosquare is the identity. Thus G is abelian, contradicting |C_G(c)|=8. The finite lemma is checked exhaustively in `finite_bicharacter_lemmas.py`: it includes all4,8,168 nondegenerate bicharacters on C8,C4×C2,C2³, respectively, and all involutions of their automorphism groups. This is a finite proof of the stated elementary lemma, not a search over associators.

Suppose the universal group is C2². Both odd simples are self-dual, B is symmetric, and P is an orthogonal involution.

If c belongs to H, then P(c)≠c because c is noncentral. Both odd simples are fixed by left and right c. To produce a dimension-sqrt8 bimodule, rather than four dimension-sqrt2 bimodules, each requires a nontrivial projective C2² commutator, namely

    B(c,c)=B(Pc,c)=−1.

No such pair occurs for an order-eight H, an orthogonal involution P, and a moved order-two element c. For C8 there is no moved involution. For C4×C2 no orthogonal involution moves an order-two element. For C2³, P−1 has rank1, so the rank-one symmetric form B(P−1,−) has value1 on every moved vector; therefore the two displayed signs are opposite. The same exhaustive elementary lemma replay confirms all cases.

Therefore c is outside H. The subcategory generated by H and one odd simple is an actual TY(H,chi,tau) category. The invertible involution c and its actual subgroup algebra supply a coherent C2 action, so E is its crossed product and _B E_B is its equivariantization. Tensor autoequivalences of a TY category induce precisely orthogonal automorphisms of H (Edie-Michell, Lemma2.16 and Remark2.17). For completeness, the kernel is trivial: for a label-fixing tensor functor, the (a,b,m) coherence makes J_ab the coboundary of J_am; gauge J_ab=J_am=1. The (a,m,m) coherence makes every diagonal J_mm^b constant, and (m,m,a) forces J_ma=1. Rescaling m removes the remaining constant. The (a,m,b) coherence forces every general label permutation to preserve chi. A fixed orthogonal automorphism has a strict skeletal lift, and action-square choices differ by the parity character (Aut_tensor(Id)=C2). The centralizer condition says that the orthogonal involution fixes four elements of H. The resulting fusion rules depend only on H, that involution, and its parity-square choice, not on the particular invariant bicharacter or tau. Exhaustive enumeration of these finite parameters yields exactly R28,R183,R405,R522.

## 3. Sources with eight sqrt2 simples

Let h be the common stabilizer involution. It is central in the invertible group G of order16. The adjoint category is Vec_<h>, with trivial associator (again a rank-one module implies this). The universal grading group U has order16, with index-two subgroup K=G/<h>. Each degree in K contains two invertibles; each degree outside K contains one sqrt2 simple.

The inverse c is outside <h>, because it is noncentral in G. Its left action on odd simples is free. Every odd B-bimodule must have support size4: an orbit of size2 has cyclic stabilizer and would give dimension-sqrt2 simples, whereas an orbit of size4 gives a single dimension-sqrt8 simple. Equivalently, the image cbar in K has no centralizer element outside K in U.

The centralizer C_G(c), of size8, projects onto a subgroup of C_K(cbar) of size4. If cbar were central in K, let d be its conjugate by an odd degree. Then cbar,d are distinct central involutions of K and every odd double orbit is a coset of L=<cbar,d>, of order4. An even dimension-two bimodule has support projecting into one coset of <cbar>; tensoring it with an odd bimodule is supported on a single odd orbit. Dimension comparison forces multiplicity2, contrary to the census. Thus cbar is noncentral in K.

A group of order8 with a noncentral involution is D8. Write K=<r,s>, r⁴=s²=1, srs=r^-1, and take cbar=s. A central extension G by <h> with a lift c of s satisfying c²=1 has a presentation

    R⁴=h^a,  c²=h²=1,  h central,  cRc=R^-1 h^b.

Since C_G(c) must project onto all C_K(s)=<r²,s>, the lift R² commutes with c. Hence R⁴=1 and a=0. There remain exactly two extension classes b=0,1. The second is genuinely nonsplit; discarding it would be an error.

No odd degree centralizes cbar. Therefore odd conjugation swaps the two reflection conjugacy classes of K. The only order16 extensions U of K with this property are D16 and SD16. A direct proof chooses odd t with tst^-1=rs and trt^-1=r^epsilon, epsilon=±1. If epsilon=−1, t² lies in{1,r²}; then ts has order8 and conjugation by s is inversion or the third power. If epsilon=1, t² lies in{r,r³}; then t itself has order8 and the same two presentations result.

## 4. Complete associator classification via ENO and Shapiro

These are U extensions of Vec_C2. Its Brauer–Picard group is C2 (the hyperbolic orthogonal group of C2⊕C2), not S3. The nontrivial element exchanges the two bosons in Z(Vec_C2). The homomorphism U→BrPic(Vec_C2) has kernel K: pointed components are the regular bimodule and the sqrt2 components are the unique rank-one invertible bimodule.

Let M=Inv(Z(Vec_C2))=C2². Odd degrees exchange its two coordinates; even degrees act trivially. Hence

    M = Ind_K^U(C2),   H²(U,M) ≅ H²(K,C2)

by Shapiro's lemma. Under this isomorphism, the ENO multiplication-system class is exactly the central extension1→<h>→G→K→1: restriction to K followed by forgetting the half-braiding projects to one of the two coordinates of M. This is the standard Shapiro projection. Thus the group extension class b=0 or1 fixes the entire H² datum, not merely part of it.

Each of the four possibilities (U=D16/SD16, b=0/1) has an actual reference category. For b=0 it is the earlier Ising–pointed pullback. For b=1 explicit Liptrap categories are certified in `nonsplit_ising_7.json` and `nonsplit_ising_3.json`, with every defining equation and Fourier block rechecked. ENO extension theory then says that every other associator with the same U and H² datum is a U-group3-cocycle twist of that reference. No claim that a single saved associator exhausts categorifications is needed.

## 5. Complete H³ parameters and actual inverse algebras

For U=C8⋊_u C2, the Lyndon–Hochschild–Serre filtration gives order bounds for H³(U,C×). The only possible E2 terms in total degree3 are

    H⁰(C2,H³(C8,C×))=C8,
    H²(C2,H¹(C8,C×)),
    H³(C2,C×)=C2.

The middle term is C2 for u=−1 and zero for u=3. Thus the orders are at most32 and16. Explicit cocycles achieve these bounds.

For D16 they are: the order8 rotation cocycle from round3; the inflated reflection cube (−1)^{b d f}; and the mixed cube (−1)^{(a mod2)d f}. They are independent by restrictions to C8, <s>, and <rs>. For SD16 the recorded rotation cocycle restricts to a generator on C8 and trivially to <s>; together with the reflection cube it supplies16 independent classes. Its order is8: its eighth power is trivial on both subgroups, while the order bound and the independent restrictions force the restriction map to C8⊕C2 to be injective.

The inverse subgroup is generated by a lift of a reflection. Within the D8 even subgroup all reflections in a fixed class are conjugate; choices of the other class are related by the permitted relabeling of U. Each lift has two possible h signs. These are both included. The algebra1+c exists exactly when its associator restricts trivially to <c>; H²(C2,C×)=0 makes its algebra structure unique up to isomorphism. For each reference category, a possible nontrivial restriction is corrected by the reflection cube. Thus the remaining twists are the eight rotation powers and (for D16) the mixed cube. All are enumerated by exact balanced-bimodule products.

For b=0 the outputs are R28,R183,R240,R408. For b=1 the outputs are R405,R522,R419,R530. The original two-sqrt8 source branch adds only R28,R183,R405,R522. Therefore the target profile, including its proved adjoint series32,16,4,1, admits exactly these eight based rings in the supplied census. The remaining16 are excluded from general complex categorification.

## References

* J.Liptrap, *Generalized Tambara–Yamagami categories*, arXiv:1002.3166v2, especially Definition4.3, Theorem4 and Lemma5.4.
* P.Etingof, D.Nikshych, V.Ostrik, *Fusion categories and homotopy theory*, arXiv:0909.3140, extension classification and BrPic(Vec_A)=O(A⊕A*).
* C.Galindo, S.-M.Hong, E.C.Rowell, *Generalized and quasi-localizations of braid group representations*, Theorem5.20 (nilpotent categories are completely unitary).

## Exact finite receipts

`exhaustive_catalog.py` is a fresh portable replay of all96 generalized-Ising source/twist/lift parameters and all46 TY action/square parameters. All142 constructions match exactly one of the eight allowed census tensors, coefficient by coefficient. It includes all eight rotation powers and both inverse-algebra lifts for the split semidihedral source. `structural_binding.py` independently checks the exact positive dimension characters, all neutral/stabilizer hypotheses, adjoint series and complete based nonisomorphism tests for all24 retained census tensors. Exactly16 lie outside the eight-ring catalog. Both replays pass with Python assertions disabled.

Additional primary reference: C.Edie-Michell, *Auto-equivalences of the modular tensor categories of type A, B, C and G*, Adv.Math.(2022), Lemma2.16 and Remark2.17; author manuscript https://par.nsf.gov/servlets/purl/10321271.

## Elementary order-eight form lemmas without reliance on enumeration

For C8 every bicharacter is symmetric, so its cosquare is the identity. For F2³, a nonsymmetric nondegenerate form has alternating difference of rank2. If its cosquare P were an involution, P−1 would have square zero and therefore rank at most1 in dimension3. This is impossible. For C4×C2, choose generators r,s. Every nondegenerate bicharacter has exponent matrix modulo4

    B(r,r)=a (a odd),  B(r,s)=2b,  B(s,r)=2c,  B(s,s)=2.

If b=c it is symmetric. If b≠c, its cosquare satisfies

    P(r)=(1+2c)r+s,   P(s)=2r+s,
    P²(r)=−r,         P²(s)=s.

It is therefore not an involution.

For the fixed-odd inverse-algebra lemma, an automorphism of C8 fixes its unique involution. In C4×C2, a putative orthogonal automorphism moving an involution must send s to2r+s and r to ur+vs with u odd. Preservation of B(r,s) forces v=1, but then B(P(r),P(r))=B(r,r)+2 modulo4, a contradiction. In F2³, a nontrivial orthogonal involution P has rank(P−1)=1. The symmetric bilinear form C(x,y)=B((P−1)x,y) has rank1 and kernel Fix(P), so C(c,c)=1 for a moved vector c. Consequently B(Pc,c) and B(c,c) have opposite signs. These arguments establish both lemmas abstractly; the finite replay is an independent exact safeguard.

The normalized cochain check `shapiro_check.py` provides an additional safeguard for Section4: for each U it computes H²(U,C2²_swap), obtains dimension3, and verifies that restriction followed by projection to the first coordinate maps its eight classes bijectively to the eight central-extension presentation parameters (a,b,c). Thus the abstract Shapiro projection has no hidden kernel in these concrete groups.
