# A proposed complete resolution of the nine D40 rings

**Status: all positive constructions and the complete converse have passed separate mathematical and implementation audits. Independent human verification remains pending.**

The relevant source IDs are R12_1_156,263,309,383,449,467,470,501,514. Their type is `(1^4,2^4,(sqrt5)^4)`, global FP dimension40. R449 is modeled by a C4-equivariantization of TY(C5); R156 and R263 are explicit Morita models below. The other six cannot be complex-categorified by the theoretical exhaustion below.

## 1. The forced Morita precursor

For every source tensor the adjoint subring B has type `(1^2,2^2)` and is the representation ring of D10. Write its nontrivial invertible g. Direct multiplication checks give:

* g is central in the entire based ring;
* the integral subring Cint has type `(1^4,2^4)` and is B plus hB for an invertible h normalizing g;
* g fixes the four dimension-two objects and acts freely on the four sqrt5 objects; its left and right permutations on these objects agree.

If C categorifies the ring, B is an actual fusion subcategory. Since g fixes a simple dimension-two object, the associator class on <g> is trivial, so A=1+g admits its regular separable algebra structure. No pivotal/unitary assumption is needed.

**Dihedral Morita lemma.** For any category B with D10 representation fusion rules, Bimod_B(A) is pointed of dimension10. Here is the short argument, independent of a classification of categorifications of Rep(D10). The A-module simples are M0=A and two lifts Mj+,Mj- of each two-dimensional Tj. All have underlying FPdimension2. Let u be A with its right A-action changed by the character g->-1. On this five-object module category, u fixes M0 and exchanges each +/- pair. The stabilizer algebra for a fixed Tj is a projective algebra of C2xC2, hence either splits into four one-dimensional bimodules, or into one bimodule Qj of normalized dimension2. In the latter case uQj=Qj and Qj M0=Mj++Mj-. Reciprocity forces M0 to appear once in Qj* Mj+. Since uQj*=Qj*, that output is u-invariant. Its total dimension is2, but its sole u-fixed vertex M0 has odd multiplicity1; all other vertices are paired. This is impossible. Thus all A-bimodules in B are invertible (ten total).

Since conjugation by h fixes g, it sends A to an isomorphic algebra: H²(C2,C*)=0 makes the multiplication choice unique. An appropriately identified hA is an invertible A-bimodule, so the second component of Bimod_Cint(A) is also pointed. Thus Dint=Bimod_Cint(A) is pointed, dimension20.

Set D=Bimod_C(A). The two free two-element orbits of g on sqrt5 simples each have diagonal stabilizer C2 in the left/right A-action; H²(C2,C*)=0 gives two one-dimensional stabilizer representations per orbit. Consequently D has exactly20 invertibles and four simples of dimension sqrt5. All products of two noninvertibles are integral, hence pointed: D is a feudal category with common stabilizer H of order5. In particular H is the unique Sylow5 subgroup of S=Inv(D).

**A more general direct Morita criterion.** The pointedness of Dint also follows without using the odd-dihedral subcategory: every integral simple has dimension1 or2, g is central in the based ring, and every noninvertible Y has invertible stabilizer exactly{1,g}. These conditions are checked directly for allnine inputs. Every simple right A-module M has underlying FPdimension2, hence normalized module FPdimension sqrt2. Its internal endomorphism object in Cint has FPdimension2 and contains the unit once; it is therefore1+v for a nontrivial invertible v. Since vM=M, v fixes the underlying object. That underlying object's invertible stabilizer is exactly{1,g}, both for a fixed Y and for a free invertible pair h+hg. Thus v=g and gM=M as right A-modules. The two characters of C2 then give two left A-actions on M; the scalar normalization obstruction is H²(C2,C*)=0. Every resulting simple bimodule has normalized dimension2/2=1, proving pointedness of dimension20. This is a uniform criterion for integral categories with all simple dimensions1 or2 and a common two-element stabilizer, not an assumption that Cint or B has a standard associator.

The inverse Morita algebra A' is the internal endomorphism algebra of the simple A-module A. Module FPdimensions normalize as FPdim_C(M)/sqrt(FPdim(A)), so FPdim_D(A')=2. It is connected, hence A'=1+c for a nontrivial involution c in S. This explicitly tracks the reverse algebra; no arbitrary choice of another module category is being made.

## 2. The pointed group and its associator

The integral part of C is recovered as Bimod_{Vec_S^alpha}(1+c). For Hc=<c>, its invertibles come from the normalizer and there are exactly |N_S(Hc)| of them (two projective characters per normalizer double coset). As the input has four invertibles, |N_S(Hc)|=4.

There are exactlyfive groups of order20. Indeed Sylow5 gives a normal C5, and any Sylow2 subgroup is a complement of order4. Thus S=C5 rt P4 with P4=C4 orV4 and action image of order1,2 or4 in Aut(C5)=C4. The abelian groups and Dic5 have every involution central. The remaining possibilities are F20=C5 rt_2 C4 and D10xC2=C5 rt V4. Their noncentral involutions form a single orbit under group automorphisms, so c may be chosen as the displayed generator in the code.

**Commutativity lemma for the dihedral alternative.** Let S=D10xC2 and let Hc be generated by any noncentral involution. For every group associator alpha for which the subgroup algebra exists, the ring of Bimod_{Vec_S^alpha}(1+c) is commutative. This statement does not assume alpha is a selected finite-order representative. Here is a proof. The normalizer is Hc times the central C2. Every nonnormal Hc-double coset is invariant under inversion and has trivial stabilizer, so it supports a unique simple object of dimension2, and that simple is self-dual. There are four invertibles, forming an abelian group. Their left/right actions on the dimension-two objects agree: their normalizer coset can be represented by the central involution, and each relevant nonnormal double coset supports only one simple. The two invertibles supported on Hc act trivially there, so every invertible has an action of order at most2 on the dimension-two objects. For self-dual dimension-two objects Y,Z, the coefficient of any dimension-two W in YZ equals that in ZY by duality. The coefficient of an invertible v is delta(Z,v^-1 Y), which is symmetric in Y,Z because v acts involutively. Thus all products commute.

All eight noncommutative D40 inputs have a noncommutative integral subring, checked directly from its64 products. Consequently their pointed Morita precursor must have S=F20. This is a theoretical conclusion for arbitrary complex associators, not an inference from an unsuccessful model search.

As an independent supplementary check, H fixes every lord and hence alpha|H is cohomologically trivial. Coprime transfer then reduces alpha to quotientQ4 cocycles. `integral_part_scan.py` constructs the six possible C(S,alpha,Hc,1) integral tensors: cyclic classes0,2 for F20, and four V4 trilinear classes for D10xC2. `integral_part_results.json` records their full tensors. Exact comparison agrees with the commutativity argument: cyclic class0 matches156,309,467,470; class2 matches263,383,501,514. R449 uses the dihedral alternative. This finite check is not required for the preceding commutativity proof.

## 3. A new order-four conjugation obstruction

Let r generate S/H=C4 in F20, with r a r^-1=a² on H=C5. Identify the four lords with m_q=r^q m_0, q in C4. Their right action is m_q r=m_{q+sigma(1)}, where sigma is an involutory automorphism of C4. Their product is the H-coset of r^{q+sigma(t)+p}, where sigma(p)=p.

In any Liptrap uberderivation let t_m in F5* be the nonzero parameter of the symmetric bicharacter on HxH. The biderivation identity with its third group argument in H eliminates upsilon. Comparing (r a,b) and (a² r,b), for a,b in H, gives

    t_{r^-1 m}=2 t_m.

The quasisymmetry identity restricted to HxH has a trivial tau-ratio (H fixes every lord), and gives

    t_{dual(m)}=t_m.

Therefore t_{m_q}=2^{-q}t_{m0}. Since dual(m_q)=m_{-sigma(q+p)}, and2 has order4 in F5*, the equality for all q forces sigma(q)=-q and p=0. The universal grading group is consequently D8, with r order4, m0 order2, and m0 r m0=r^-1. This argument permits arbitrary nonzero complex uberderivation variables and variable tau; it does not restrict phases to fifth roots for a negative conclusion.

**Unified form.** Let H=C_p for an odd prime p and suppose the invertible group is C_p rt_u C_n, where u in F_p* has exact order n. A feudal categorification with this common stabilizer has n lords. The identical calculation gives t_{r^-1m}=u t_m and t_dualm=t_m. Because the cyclic quotient action is faithful, it forces the universal grading group to be the dihedral group D_{2n}: the right quotient action is inversion and the square of a chosen base lord is the neutral coset. This is a necessary condition over C; it does not assert existence for every p,n. It excludes all other cyclic-quotient feudal rules uniformly, rather than by a finite root-of-unity search.

## 4. Exhaustiveness of the D8 twists

The neutral component of the universal grading is Vec_C5: its associator is trivial because C5 fixes a lord. The Brauer-Picard group is O(C5+C5*,q), the split orthogonal group of order8, isomorphic to D8. The r component represents the automorphism a->a², hence an orthogonal element of order4. A lord component is the rank-one module determined by the nondegenerate bicharacter t_m, hence a reflection. These generate all of BrPic(Vec_C5). Changing the chosen lord m0 by r^j m0 cycles t_m through all four nonzero values, so the homomorphism rho:D8->BrPic(Vec_C5) is unique up to an identification of grading groups preserving r and c=r².

ENO's classification of graded extensions first parametrizes product equivalences by H²(D8,Inv Z(Vec_C5)). Here Inv Z(Vec_C5)=C5² with the rho-action. All positive-degree cohomology of the order8 group with these5-primary coefficients vanishes (averaging by1/8). The relevant lower obstruction therefore vanishes and the product system is unique. An explicit category D0 exists, supplied by the accepted Liptrap certificate in `feudal40_models_sparse.json`, parameters F20/sigma=inversion/p=0. ENO's remaining associator choices form an H³(D8,C*) torsor. Thus every possible D above is a grading3-cocycle twist of D0, up to the relabeling already described.

Every class in H³(D8,C*) has exponent dividing4. A short proof avoids relying on a cohomology table: choose an index-two V4 subgroup K. The Kunneth formula gives H³(K,C*)=(C2)^3, of exponent2. Restriction followed by corestriction is multiplication by2, so 4 alpha=cor(2 res alpha)=0 for every alpha. The coefficient sequence mu4->C*--fourth-power->C* therefore shows every class has a mu4-valued representative. On the subgroup <c>=C2 the map H³(C2,mu4)->H³(C2,C*) is an isomorphism (H²(C2,C*)=0). Every class with trivial C* restriction consequently has a normalized mu4 cocycle with omega(c,c,c)=1. The reverse algebra exists exactly in this relative kernel. Any two algebra multiplications differ by H²(C2,C*)=0 and hence are isomorphic.

`grading_cocycles.py` uses exact invertible row/column operations modulo4 on the normalized bar complex:343 3-cochain variables,2401 quadruple equations plus omega(c,c,c)=1, and49 normalized2-cochain generators. It generates the entire cocycle kernel, quotients by all normalized mu4 coboundaries, and retains16 relative mu4 cohomology representatives. These cover all relative C* classes (the mu4 list may have cohomology duplicates after extending coefficients). Every representative is separately checked against all4096 cocycle identities and the subgroup restriction.

## 5. Exact constructive conclusion

`feudal_dual.py` reconstructs all scalar recouplings from Liptrap Lemma5.4, then constructs actual1+c bimodules and their balanced relative tensor products. Only recouplings with at most two lords enter; the three-lord Fourier matrices establish unitarity of D0 but are not needed in the relative tensor multiplication. All module relations, balanced relation consistency and descent of both actions are checked. Exact projective stabilizer traces use Phi10/Phi20/Phi40; no floating-point arithmetic determines a coefficient.

`feudal_twist_scan.py` repeats that construction for all16 relative grading twists. Each result has rank12; exact comparison of all1728 coefficients identifies only R156 or R263. Therefore, by Sections1-4, R309,R383,R467,R470,R501,R514 are excluded from arbitrary complex categorification. R156 and R263 have actual unitary models. R449 is independently realized by the C4-equivariantization of TY(C5) with generator inversion and parity coherence kappa_m=-1 for its fourth power.

Independent audit files `../family_quadratic/audit_graded_models.py` and receipts check the accepted positive models by an independent weighted-balanced-quotient/Hom-space implementation, all480000 relevant scalar pentagons, and64 unitary Fourier blocks. The negative conclusion uses the theoretical exhaustion argument in this document, independently reviewed by the other audit implementations.

## References and a second check of Section3

P. Etingof, D. Nikshych, V. Ostrik, *Fusion categories and homotopy theory*, Quantum Topology1 (2010),209-273, arXiv:0909.3140, Theorems1.1 and1.3: the BrPic identification and the H²/H³ extension classification.

J. Liptrap, *Generalized Tambara-Yamagami categories*, arXiv:1002.3166v2, Definitions4.3-4.4, Theorem4 and Lemma5.4: all original complex feudal categories are parametrized; the positive phase certificates and reconstructed F-data are covered by the theorem.

There is an independent conceptual proof that the universal group U is D8. Its C4 serf quotient maps faithfully to the diagonal order-four subgroup of BrPic(Vec_C5)=O(C5+C5*,q). Every lord component has rank one, so its BrPic element is an off-diagonal reflection. Such a reflection has square1 and inverts the order-four rotation. This forces U=D8 directly and confirms sigma=-id,p=0 without restricting any complex parameters.
