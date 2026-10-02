# A general exclusion for R8_2_68

The ring has dimensions [1,1,1,6,4,4,6,1], global dimension108, Inv=C4 and full adjoint subring. Its unique order-two invertible is index7, and it fixes all four noninvertible objects. These are exact source-bound facts checked by `verify_r68.py`. The following argument concerns arbitrary complex fusion categories.

## A dimension54 descent

Suppose C categorifies the ring. Dimension108=2²·3³ gives solvability. Since C_ad=C, the last prime cyclic step is an equivariantization. The canonical prime group must be C2, since its representation subcategory embeds into Inv(C)=C4. Thus C=D^C2, FPdim(D)=54. The canonical sign is the unique order-two invertible. It fixes both dimension4 and both dimension6 C-objects, so the equivariantization orbit formula gives D of type1²,2⁴,3⁴. Its outer involution tau swaps the four dimension2 simples in two pairs and the four dimension3 simples in two pairs, and fixes both invertibles.

The adjoint subcategory D_ad is tau-stable. If it has a invertibles, b dimension2 and c dimension3 simples, then a∈{1,2}, b,c∈{0,2,4}, and a+4b+9c divides54. Complete enumeration gives dimensions1,2,9,18,27 or54, with types respectively1,1²,1·2²,1²·2⁴,1·2²·3² and the full type. Pointed dimensions1 and2 cannot account for X X* of a dimension3 object, since each invertible occurs at most once. These adjoint subcategories are solvable, hence have the strong Frobenius property. Their integral simple dimensions divide their global dimension, so a dimension2 object in dimension9 or27 is impossible. Thus D_ad has dimension18 or equals D.

## A central Rep(C2) in D in both cases

If D_ad=D, solvability forces D=F^C2. The canonical group cannot have order3 because Inv(D) has order2. FPdim(F)=27, and F is integral. The strong Frobenius property makes every simple dimension divide27, so only dimensions1 and3 can occur. Since D has exactly two invertibles, F has one involution-fixed invertible and four free invertible orbits. These give nine invertibles in F and the four dimension2 D-objects. The four dimension3 D-objects come from two fixed dimension3 F-objects. Hence F has type1^9,3². This already supplies a central Tannakian Rep(C2) in D, on its nontrivial invertible g. Its central lift is unique because U(D)=1.

Now suppose D_ad=E has dimension18 and type1²,2⁴. Its adjoint is itself: a proper grading has order2,3,6,9 or18. For order2, each dimension-nine component must have type1,2²; in particular its neutral solvable subcategory would have dimension9 and a dimension2 simple, contradicting the strong Frobenius property. For order3, each dimension-six component requires both invertibles and one dimension2 simple, which cannot fill three components from only two invertibles. Higher grading orders have components of dimension at most3 and cannot contain a dimension2 simple, whose squared dimension already contributes4. Hence no proper categorical grading is possible.

Solvability therefore gives E=(Vec_A^omega)^C2, where A is a group of order9. Indeed the equivariantizing group is C2, and the dimension-nine category is integral and solvable, hence its simple dimensions divide9; a dimension3 simple would already contribute9 beyond the unit, so it is pointed. A is C9 or C3². Exactly one invertible label is fixed by the involution, so its group automorphism is inversion. The category E has U(E)=1. Its nontrivial invertible g has the canonical central Tannakian lift; since Inv(E)=C2 and the kernel Inv Z(E)→Inv(E) is Aut_tensor(Id_E)=1, one has Inv Z(E)=C2.

The faithful universal grading of D has group C3 and neutral category E. Gelaki–Naidu–Nikshych, Theorem3.3 and Remark3.4, give its canonical braided C3 action on Z(E), and Theorem3.5 gives Z(D)≃Z_E(D)^C3. This action fixes the only nontrivial invertible central object g. Since H²(C3,C*)=0, g has equivariant lifts, as does the unit. These six central invertibles form an abelian group of order6 (invertibles in a braided category commute). Its unique order-two element is a lift of g. Its self-braiding agrees, on restriction, with the self-braiding1 of g in Z(E), so this order-two subgroup is Tannakian and its image in D is the original nontrivial invertible g.

De-equivariantize D by this central Rep(C2), obtaining F of dimension27. The C3 grading descends because the algebra1⊕g lies in E. Its neutral component is Vec_A^omega. A dimension3 D-object cannot be fixed by tensoring with the canonical sign g: that would split into two simple objects of rational dimension3/2 in F, impossible because simple Frobenius–Perron dimensions are algebraic integers. Thus the two dimension3 objects in each nonneutral D-component are exchanged by g and become the two equivariant structures on one dimension3 F-object. Consequently F again has type1^9,3², with a C3 grading of ranks9,1,1.

In this second case U(D)=C3. The kernel Inv Z(D)→Inv(D) is therefore C3. The central lift of g of order2 is unique: its inverse image has order6 and is an abelian group, so has a unique order-two subgroup. In the first case uniqueness was already established from U(D)=1. Thus in both cases D=(F)^C2, of type1^9,3², and the canonical central Rep(C2) is uniquely determined as an order-two subgroup.

## Combine the two actions

Every tensor auto-equivalence of D preserves this unique central order-two lift of g. In particular the outer tau of C=D^C2 preserves its central Rep(C2), with its braiding. Restricting the outer action to that Rep(C2) and then equivariantizing gives a symmetric Tannakian subcategory Rep(H) of C of dimension4. The group H is an extension of C2 by C2. All its simples are invertible and exhaust the four invertibles of C. Their group is C4, so H=C4 (the alternative H=V4 has V4 characters).

The standard equivariantization/de-equivariantization tower gives C=F^C4. Let beta be its generator. Its square sigma is the inner C2 action with D=F^C2. On A=Inv(F), sigma is inversion, as only the unit among the nine invertibles is fixed. Both dimension3 F-objects are sigma-fixed, because they give the four dimension3 objects of D.

In either branch, A=Inv(F) has order9. Its permutation action on the two dimension3 simples is trivial, since an odd-order group cannot act nontrivially on a two-element set. For either such simple X, Frobenius reciprocity therefore puts every a∈A in X X* with multiplicity1. These nine invertibles exhaust FPdim(X X*)=9. Consequently F_ad=Vec_A^omega, U(F)=C3, and its two nonneutral components each have rank1. This establishes the grading also in the first branch D_ad=D.

These rank-one nonneutral components force the associator class omega to vanish: a rank-one module supplies a nonzero2-cochain trivializing omega. Hence F is C3-graded over Vec_A with ranks9,1,1.

The action of beta on this grading must be inversion. If beta acted trivially, equivariantization F^C4 would inherit a faithful C3 grading, contrary to C_ad=C. Therefore beta exchanges the two rank-one components F1 and F2.

## The order-four action cannot exchange those modules

On A one has beta²=-I. For A=C9 no automorphism squares to inversion: Aut(C9) has order6. For A=C3² an automorphism matrix B with B²=-I has minimal polynomial t²+1, which is irreducible over F3, and therefore determinant1. This is also checked over all81 matrices; there are six such matrices, all with determinant1.

A tensor auto-equivalence of Vec_A consists of its group automorphism B and a class eta∈H²(A,C*)≃C3. The latter is the alternating2-cocycle class. B acts on this cohomology group by determinant, hence trivially. Since beta is a coherent order-four action, its fourth tensor power is tensor-isomorphic to the identity. This forces4eta=0, and thus eta=0 in C3. One may equivalently use beta²=sigma: inversion sigma acts trivially on H²(A,C*) and has order2, forcing its class0 and then2eta=0.

Rank-one left module categories over Vec_A are classified by H²(A,C*). A tensor auto-equivalence with determinant1 and tensorator class0 fixes every such module class. Yet F1 and F2 have distinct left-module classes. To prove the distinction, if they were equivalent as left modules, tensoring that equivalence with the invertible bimodule F1^(-1) would equate F0=F1^(-1)⊠_Vec_A F1 (rank9) and F1^(-1)⊠_Vec_A F2=F1 (rank1) as left modules. This is impossible. Therefore beta cannot exchange F1 and F2. The contradiction excludes R8_2_68 generally.

## Cited categorical inputs and audit status

ENO, *Weakly group-theoretical and solvable fusion categories*, arXiv:0809.3031, supplies the p^a q^b solvability theorem, closure properties and prime cyclic construction. ENO's strong Frobenius theorem for weakly group-theoretical categories forces every integral simple dimension to divide the global dimension; solvable subcategories satisfy this hypothesis. Burciu–Natale, arXiv:1206.6625, supplies equivariantization orbit/stabilizer dimensions. Gelaki–Naidu–Nikshych, *Centers of graded fusion categories*, arXiv:0905.3117, Theorem3.3, Remark3.4 and Theorem3.5, apply to the faithful C3 grading of D over E and supply the canonical braided action and Z(D)≃Z_E(D)^C3; their hypotheses impose no pivotal or unitary condition. Classification of Vec_A module categories and tensor auto-equivalences is standard group cohomology as in EGNO, Chapters7–8.

This decision was accepted after independent audits approved the relative-center lift and the combined C4 action. `verify_r68.py` checks exact source hypotheses, every integer partition and finite matrix/cohomology calculation, but the categorical argument requires the cited theorems and mathematical audit.
