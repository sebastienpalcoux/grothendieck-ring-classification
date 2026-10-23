# Recovered rank-eight nonintegral results

These six positive constructions are actual unitary categories. The two negative arguments concern arbitrary complex fusion categories; no pivotal structure is assumed. `verify_nonintegral.py` reconstructs every positive multiplication tensor without reading the census, compares all 512 coefficients, validates all 4096 associativity identities, and checks the structural hypotheses of the exclusions. Frozen source checks run under both ordinary Python and `python3 -O`.

## R8_2_557 and R8_2_313: diagonal central quotients

Write the rank-four basis as 1,g,x,gx. In the ordinary PSU(2)_6 category, g is a central fermion with trivial pointed associator. In each of the two frozen unitary pseudo-PSU(2)_6 categories, its central lift has self-braiding respectively +i and -i, and the associator on g,g,g is -1. The latter assertions are checked from the actual symbolic associators: each source has 224 F-symbols, 136 invertible associator blocks, 2688 pentagon equations and 24 scalar half-braiding equations. The sources and checker were already published in the rank-eight supplement.

In the ordinary Deligne square, g⊠g has self-braiding (-1)^2=1 and trivial pointed associator. In the product of the two pseudo categories, its self-braiding is i(-i)=1 and its pointed associator is (-1)^2=1. Its central square is the unit: the kernel of Inv Z(D)→Inv D is Aut_tensor(Id_D), which is trivial for these adjoint-generated rank-four rings. Thus in either case it generates a genuine central Rep(C2). The category of modules over 1⊕(g⊠g) is a unitary fusion category. All 16 simple objects have free diagonal orbits, yielding eight simples.

Represent each orbit by (0,j) or (2,j), j=0,1,2,3. If a and b are such representatives, the coefficient at representative c is the sum of the ordinary product coefficients at c and at (g⊠g)c. This gives exactly the constructor `quotient`. The basis maps are [0,1,2,7,3,6,5,4] for R557 and [0,7,1,2,3,4,6,5] for R313.

The mixed ordinary/pseudo product does not provide R317: its diagonal pointed associator is nontrivial. No claim about that ring follows from these two constructions.

## R8_2_855: D14 local modules

The invertible V24 of the unitary SU(2)_24 modular category is a boson. Its algebra 1⊕V24 has a unitary category of local modules. In the even-label part the free labels are f0,f2,...,f10 and the fixed label V12 splits into P,Q. Both resolved objects are self-dual. Standard D14 fusion gives

P²=P+f0+f4+f8, Q²=Q+f0+f4+f8, PQ=f2+f6+f10,

and P f_(2j)=Σ_(k=6-j)^5 f_(2k)+P for even j, or with Q for odd j. The Q rule exchanges P,Q. Bulk fusion is SU(2)_24 fusion folded under t↔12-t, with f12=P+Q. The complete basis map is [0,1,7,4,5,6,2,3]. This is the usual D_(2n) construction; Morrison–Peters–Snyder, arXiv:0808.0764, Theorem 4.14, and arXiv:1003.0022, Theorem 2.2 and Proposition 2.4, provide the categorical realization and fusion description.

## R8_2_239: an S3 extension and Morita dual

Let A=C7. The Brauer–Picard group of Vec_A is O(A⊕A-hat) for the hyperbolic quadratic form. The matrices r=diag(2,4) and s=swap preserve that form and satisfy r³=s²=1, srs=r^(-1). They define a homomorphism S3→BrPic(Vec_A).

The group π2=Inv Z(Vec_A) is 7-primary. Positive-degree S3 cohomology with these coefficients vanishes by averaging, since 6 and 7 are coprime. Hence O3 vanishes. The remaining obstruction lies in H4(S3,C*)=0. One can obtain this equality from the Lyndon–Hochschild–Serre sequence for C3 normal in S3: the odd-primary positive quotient cohomology vanishes, H4(C3,C*)=0, and H4(C2,C*)=0. Thus ENO's extension theorem gives an actual S3 extension E of Vec_C7.

The restriction to C3 is pointed, because r is an automorphism bimodule. Its group of invertibles is F21=C7⋊C3, with action multiplication by 2. The associator class on this subgroup is inflated from C3: the C3 invariants in H3(C7,C*) vanish, since multiplication by 2 acts there by multiplication by 4. Restriction H3(S3,C*)→H3(C3,C*) is surjective. Indeed the order-two quotient acts trivially on H3(C3,C*), and all positive quotient cohomology on a 3-primary module vanishes. Twist the extension by an S3 3-cocycle so that its pointed C3 restriction is Vec_F21 with trivial associator.

The object B=⊕_(h in C3) h is therefore an associative separable algebra. Its B-bimodule category D is the actual Morita dual. Its neutral part is (Vec_C7)^C3≃Rep(F21), with simples alpha0,alpha1,alpha2,X,Y. The reflection bimodules in the original extension are the rank-one Fourier bimodules. Passing to B-bimodules gives three odd simples m0,m1,m2 of dimension sqrt(7). Fourier transport inverts the C3 character, so alpha_i m_j=m_(i+j) and m_j alpha_i=m_(j-i). The two nontrivial C7 orbits give X m_j=Y m_j=Σm_k on both sides.

Duality must be m_j*=m_(j+c), by the two alpha actions. Involutivity gives 2c=0 in C3, so c=0. Reciprocity now forces m_jm_k=alpha_(j-k)+X+Y. The remaining neutral products are X²=X+2Y, Y²=2X+Y and XY=Σalpha+X+Y. These are constructed directly in the verifier. The complete map is [0,1,2,3,4,5,7,6]. An extension of a pointed category is weakly group-theoretical, as is its Morita dual, so Galindo–Hong–Rowell Theorem 5.20 makes D unitarizable.

Primary sources: ENO, *Fusion categories and homotopy theory*, arXiv:0909.3140, Corollary 1.2 and Theorem 1.3; Galindo–Hong–Rowell, *Generalized and quasi-localizations of braid group representations*, arXiv:1105.5048, Theorem 5.20.

## R8_2_290: charge-conjugation defects of PSU(3)_4

The adjoint category B=PSU(3)_4 is unitary modular, since the C3 pointed subcategory of SU(3)_4 is nondegenerate. Its neutral basis is (0,0),(3,0),(1,1),(0,3),(2,2), and Inv(B)=1. The Dynkin diagram automorphism induces unitary charge conjugation, restricting to this adjoint category. The order-two symmetry exchanges X=(3,0) and X*=(0,3), and fixes the other three labels. The G-crossed obstruction groups give O3=0 because Inv(B)=1, and O4=0 because H4(C2,U1)=0. The unitary gauging theorem therefore supplies a faithful unitary C2-crossed extension. This is the category of defects before equivariantization, not its gauging. Bischoff's rank formula gives three odd simple objects.

The neutral fusion tensor is independently computed by SU(3)_4 fundamental alcove adjacency and the Jacobi–Trudi formula. It does not use the census or a fitted character table. The regular matrix of X has characteristic polynomial (t²+t+2)(t³-2t²-t+1). Its Frobenius–Perron dimension lambda has degree three, so the odd action A has the cubic characteristic polynomial t³-2t²-t+1. The odd module is indecomposable. The neutral algebra is generated by X, so its A action is irreducible. Since the neutral ring is commutative and the dual action is transpose, A is normal. All three cubic roots are real, forcing A to be symmetric. Its trace is 2 and trace of A² is 6.

An exact enumeration of the resulting nonnegative symmetric 3×3 matrices gives precisely six basis permutations of

[[0,0,1],[0,1,1],[1,1,1]].

The neutral actions in the displayed basis are I,A,A²-I,A,A²-A. A positive eigenvector has coordinates 1,lambda/(lambda-1),lambda. These are pairwise distinct, so the odd simples are all self-dual. Crossed braiding identifies right action by X with left action by X*, and Frobenius reciprocity determines all odd products. The verifier constructs every coefficient and checks all module and fusion relations. The complete map is [0,1,6,2,7,3,4,5].

Primary sources: Edie–Michell, arXiv:2002.03220, Corollary 2.7 (and its adjoint restriction discussed in Section 3); Cui–Galindo–Plavnik–Wang, arXiv:1510.03475, Sections 3.2–3.4 (formulated in the unitary setting); Bischoff, arXiv:1807.06131, Proposition 1.1.

## R8_2_868

The detailed proof `R868_HI7_DUAL_PROOF.md` identifies the actual unitary C7 Haagerup–Izumi Q-dual, proves the canonical algebra has the required object decomposition, and invokes the precise Evans–Gannon fusion theorem. Its constructor is replayed in this verifier; the map is [0,3,1,2,4,5,7,6]. This assertion uses the established unitary order-seven subfactor, not a uniform claim at arbitrary odd order.

## R8_2_784: Hopf dual rank obstruction in dimension44

The tensor has a faithful C2 grading with neutral indices [0,1,2,3,4,6,7], dimensions 1,1,2,2,2,2,2, and a single odd object of dimension sqrt(22). A rank-one module category over the neutral category gives a fiber functor, so the latter is Rep(H) for a semisimple Hopf algebra H of dimension22. Etingof–Gelaki's dimension-pq classification makes H a group algebra or its dual. The rank-seven nonpointed neutral tensor forces H=C[D22]; all other possibilities are pointed. The dual category of the fiber-functor module is then Rep(H*)=Vec_D22, of rank22. But a homogeneous component of a faithful fusion grading is an invertible bimodule, so its left-module dual must be equivalent to the neutral category, of rank7. This is impossible. All steps concern general complex categories.

Primary source: Etingof–Gelaki, *Semisimple Hopf algebras of dimension pq are trivial*, arXiv:math/9801129, Theorem 6; EGNO, Example 7.12.26, for the fiber-functor dual.

## R8_2_181: central descent to an impossible TY(C7) action

The commutative tensor has C2-neutral indices [0,3,4,5,6] of type 1³,3² and three odd sqrt(7) objects [1,2,7]. Its neutral category D has dimension21 and D_ad=D. Solvability in dimension3·7 forces an equivariantization by C3, since a nontrivial prime grading would contradict D_ad=D. The dimension-seven category underneath is Vec_C7^omega. The nontrivial C3 action is multiplication by 2 or 4. Its action on H3(C7,C*) is multiplication by 4 or 2, so invariance forces omega=0. Coprime coherence is unique. Consequently D≃Rep(F21).

The invertibles alpha form its canonical central Rep(C3). Their lifts are unique because U(D)=1. The odd invertible D-bimodule induces the relative-center C2 action. Left and right alpha actions agree and are free on the odd basis, so this action preserves the underlying alpha; uniqueness preserves their central lifts pointwise. Each such invariant central simple has an equivariant structure since H2(C2,C*)=0. Their equivariant lifts form a central group of order6, with kernel C2 and quotient C3. Its unique order-three subgroup lifts the original Rep(C3). Its self-braiding is inherited from that symmetric subcategory, so it is Tannakian. The forgetful functor to C is faithful on this subgroup. This argument does not assume C is braided or pivotal.

De-equivariantization by this central Rep(C3) produces a fusion category of dimension14 whose rules are TY(C7); the recovered C3 action on its invertibles is multiplication by 2 or 4. A tensor auto-equivalence of a Tambara–Yamagami category must preserve its nondegenerate symmetric bicharacter. Every such bicharacter of C7 is chi(a,b)=exp(2pi i kab/7), k≠0. Preservation by multiplication by q requires q²=1 modulo7. Neither q=2 nor q=4 satisfies this. Contradiction.

This is a general exclusion. No assertion that a central fermion is transparent in C is used. Primary dependencies are ENO solvability at p^a q^b, the standard relative-center equivariantization of a faithful grading (Gelaki–Naidu–Nikshych, arXiv:0905.3117), and Tambara–Yamagami's classification theorem.
