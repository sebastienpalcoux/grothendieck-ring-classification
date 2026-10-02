# Retained upper-rank research and publication state

This document preserves the pre-failure theoretical results and limitations. It is not a replacement for the complete original signed certificates and proof programs, which remain inaccessible. All38 exact source tensors and all13 model-to-census basis maps are preserved in decisions.json. The first36 decisions had independent mathematical and source-bound audits before interruption; the last2 are additionally reconstructed and verified in this checkpoint.

## Six rank-seven integral exclusion families (12 rings)

**R7_2_70,213; R7_4_358.** Dimensions1^4,2,d², global8p with(p,d)=(5,4) or(17,8); adjoint whole, all nonunits fixed by invertibles. Solvability forces C=D^C2, where D has dimensions1^4,(d/2)^4 and global4p. D has no C2 grading: an involution preserves a nonzero character of a possible grading quotient. A Cp grading is impossible for p17 byrank8<17; for p5 its neutral pointed dimension4 and four rank-one components force trivial associator, but neither BrPic(Vec_C4) nor BrPic(Vec_V4) has an element of order5. Consequently D=E^C2. Strong Frobenius and dimension partitions force E of type1²,2^((p−1)/2) with E_ad=E. E=(Vec_Cp^omega)^C2. Unique central lifts (U(E)=1) preserve this Tannakian C2 under the outer action, hence C=(Vec_Cp^omega)^H with H of order8 and abelianization V4. Its action on Cp has cyclic image at most2. For p17, orbit/projective stabilizer dimensions are at most4, contradicting8. For p5, coprime strictification, H²(Cp,C*)=0 and H²(H,Cp-hat)=0 remove stabilizer multipliers; an invariant mu_p-valued associator is obtained by averaging. Ordinary orbit/stabilizer dimensions are at most2, contradicting4.
Original files: r7_integral/EIGHT_P_GENERAL_PROOF.md, verify_general_families.py, independent EIGHT_P_AUDIT.

**R7_3_386,966.** Dimension112, type1²,2³,7². Adjoint whole and solvability force C2 de-equivariantization of dimension56, type1^7,7. This near-group has adjoint whole and is a C7 equivariantization of Vec_(C2^3), with Singer7 action. Its unique central C7 survives the outer C2, forcing an action of H14; the embedded representation subcategory has type1²,2³, so H=D14. This would require inversion of the Singer7 in GL3(2), whose normalizer is7:3. Contradiction. All168 GL3(2) matrices were independently checked.
Original D112_GENERAL_PROOF.md.

**R7_2_113,273.** Dimension96, type1²,2,3²,6², and the same sign-action premises as previously published R252/R315. The sign fixes the2 and6 objects and swaps the3 pair. Existing general proof yields C=(Vec_K16^omega)^S3 with orbits[1,3,6,6]. Fixed-point-free C3 forces K=C4² or C2^4. The outer involution would have exactly2 fixed points but must have at least4. Reuses supplements/rank7/papers/D96_GENERAL_EXCLUSION_PROOF.md without changing its scope.

**R7_2_50,280.** The other dimension96 sign branch fixes2 and swaps both3 and6 pairs. De-equivariantization has dimension48, type1³,3,6 and adjoint whole, hence is a C3 equivariantization of E16 of type1^4,2³. C3 cycles the nontrivial V4 invertibles and the three2-dimensional objects. E's adjoint is Vec_V4^omega, and universal V4 grading has three rank-one components. A rank-one module forces omega=0. H²(V4,C*)=C2 gives only two rank-one left-module classes, whereas three invertible components must have pairwise inequivalent left modules (tensor with the inverse bimodule proves this). Contradiction.
Original D96_NEW_BRANCH_PROOF.md.

**R7_3_398,478.** Dimension54, type1²,2^4,6. De-equivariantization gives D27 of type1^9,3², with pointed A9 neutral and rank-one C3 components, forcing trivial pointed associator. The outer C2 inverts both A9 and the grading C3. Its restricted tensorator eta is in H²(A9,C*); inversion acts trivially on this odd group, and order2 implies2eta=0, hence eta=0. Its Brauer–Picard restriction −I is central and cannot conjugate the nontrivial order3 component class to its inverse.
Original D54_GENERAL_PROOF.md.

**R7_4_963.** Dimension310=2·5·31, type1²,2²,10³. ENO Theorem9.2 gives group-theoretical. Closed subring dimensions are1,2,10,310. In C(G310,omega,H,psi), H=1 or2 cannot supply degree10; H10 must be D10. Degree10 objects force trivial outside intersections, giving three outside double cosets of size100, hence a Frobenius group with kernelC31 and complementD10. Such a complement cannot act faithfully in cyclic Aut(C31). For H=G, Sylow31 is normal and the quotient D10 splits; its action has cyclic image at most2, so all representation degrees are at most2.
Original D310_GENERAL_PROOF.md.

The12-family inventory was approved_general_decisions.json. Source checker validated all343 tensor coefficients and2401 associativity relations per ring, plus dimensions, duality, adjoint closure, sign action and descent. Complete18-input integral coverage receipt fingerprint retained:
f851de11a9640b02b0c54a35473bf196a47e0850be52821d654bcc738779954e.

## Rank-seven signed general exclusions and modular model

**R7_3_1036,1044; R7_4_2510,2706.** Complete oriented signed sphericalization enumeration had8,24,4,48 tables respectively. Every character branch fails a zero dimension, duality constraint or formal-codegree norm divisibility. This applies generally: sphericalization doubles global dimension and formal codegrees, leaving the necessary quotient unchanged. It does not assume an original pivotal structure. Normal and optimized replay passed, with independent completeness and tampering controls.
Original <ID>_general.json, verify_nonintegral_results.py, SIGNED_GENERAL_AUDIT.md.

**R7_2_240.** Unitary modular D12 even part/local bosonic modularization of PSU(2)_20, basisf0,f2,f4,f6,f8,P,Q. Fold SU(2)_20 labels t→10−t; f10=P+Q. P f_(2j)=sum_(k=5−j)^4 f_(2k)+(P for j even,Q for j odd); Q interchanges P,Q. P²=Q+f2+f6, Q²=P+f2+f6, PQ=f0+f4+f8, P*=Q. All343 coefficients and2401 associativity relations passed. Morrison–Peters–Snyder0808.0764 Theorem4.14 and1003.0022 Theorem2.2/Proposition2.4 supply the actual category. Map is in decisions.json.
Original R240_D12_PROOF.md, verify_d12.py.

## Rank-eight integral models

Four models are strict unitary pointed equivariantizations, checked through full orbit addition:
- R244, (Vec_(C4²))^C3, alpha(x,y)=(-y,x−y) mod4.
- R289, (Vec_(C2^4))^C3, alpha(x,y,z,w)=(y,x+y,w,z+w).
- R143, (Vec_C17)^C4, alpha(x)=4x mod17.
- R179, (Vec_(C2^4))^C5, alpha(x,y,z,w)=(w,x+w,y+w,z+w).
The zero orbit contributes ordinary stabilizer characters; free orbits and exact addition counts give all fusion products.

**R237=Rep(AGammaL(1,8))**, order168. Elements(v,a,t) act on F8 by x→v+a x^(2^t). Character dimensions1³,3²,7³. Exact induced characters in Q(zeta21), orthogonality and all512 coefficients passed. The degree7 characters are
chi_s(v,a,t)=zeta3^(s t) sum_(r nonzero, a r^(2^t−1)=1) (−1)^Tr(v/r).

**R575**, dimension32, is the Davydov–Runkel extension Rep(H_C:sigma1)⊕Vec. The neutral semisimple Hopf algebra has basish(p,q,j), p mod4,q,j mod2. Let zeta=zeta16, omega=zeta², i=zeta^4, and tau(p,q)=(-p+q,q). D8 multiplication is(p,q)(r,s)=(p+(−1)^q r,q+s).
h(p,q,j)h(r,s,k)=delta_((p,q),tau^j(r,s)) omega^(q j k) h(p,q,j+k).
Delta h(g,j)=sum_(ab=g) i^(−a2 b1 j) h(a,j)⊗h(b,j).
epsilon h=delta_(p0)delta_(q0).
S h(p,q,j)=zeta^((4p−2)qj) h(tau^j((p,q)^−1),j).
The symmetric nondegenerate Hopf pairing is
P(h(p,q,j),h(r,s,k))=delta_(s,j)delta_(k,q) i^(−3rp) zeta^(jq)/4.
All8192 pairing identities and all Hopf axioms were exactly checked. Davydov–Runkel's dual convention is H-vee=(H*)^(op,cop), requiring Gamma=S∘P^−1; plain P^−1 would use the wrong convention. The cointegral lambda(h)=delta_(j0)/2 and normalized integral Lambda=(e00+e00t)/2 satisfy Gamma(lambda)=4Lambda and lambda Gamma lambda=1. Gamma is symmetric, S²=1,g=1, so their Theorem2.5 applies; Theorem3.25 gives rigidity. Neutral fusion is Rep(D16), type1^4,2³; the odd M has dimension4, Xi M=dim(Xi) M and M²=sum dim(Xi) Xi. ENO dimension32 solvability makes the fusion category weakly group-theoretical; GHR Theorem5.20 makes it unitarizable.
Original R575_HOPF_PAIRING_PROOF.md, r575_model.py, hopf16_symmetric_pairing.py, R575_INDEPENDENT_AUDIT.md.

## Rank-eight integral general exclusions

**R41,R86,R162**, dimension32: a rank-one component over dimension16 neutral yields a fiber functor and a Hopf algebraH16 whose Rep(H*) is again the same neutral category. Kashina math/0004114 Theorem1.2/Table1 leaves only H_C:sigma1 when both groups of grouplikes have order4. Its neutral Rep(D16) fusion has V4 invertibles and all2-dimensional simples self-dual. R41/R86 have C4 invertibles; R162 has a non-self-dual2-dimensional pair. These exclude general categories, without unitarity.

**R697**, dimension68, type1^4,4^4, adjoint whole and V4 fixing nonunits: solvability gives D34 of type1²,2^8, also adjoint whole, then Vec_C17^omega equivariantized by inversionC2. The unique central Rep(C2) is preserved by the outer involution, giving combined V4 equivariantization. V4→Aut(C17) has image at most2. Nonzero orbits have size2 and cyclic stabilizers, forcing2-dimensional simples, contradicting only4-dimensional nonunits.

**R808**, dimension186, type1²,2,6^5: ENO integralpqr makes group-theoretical; groups of order186 are solvable, hence the category is solvable. A C2 descent yields dimension93 of type1³,3^10 with adjoint whole, hence Vec_C31^omega equivariantized byC3. Unique central C3 survives the outer involution, yielding S3 equivariantization because its representation subcategory has type1²,2. Every S3→Aut(C31) has cyclic image and kills its normalC3, contradicting the nontrivialC3 action.

**R140**, dimension56: neutral indices[0,1,2,3,7] form dimension8 TY(C4), with invertibles[0,1,2,7] and E(index3) of dimension2. Each of indices4,5,6 is a rank-one neutral module: gM=M and EM=2M. Thus the neutral admits a fiber functor, equals Rep(H8), and G(H*)=C4. Kashina's general prime-power Theorem1.1 says cyclic grouplikes would force H*=kC8 with8 grouplikes, contradiction. No assumption that all dimension56 categories are group-theoretical is used.
Original R140_RANK_ONE_MODULE_PROOF.md.

**R694** is proved separately in the fresh recovery proof and checker.

## Rank-eight nonintegral models

**R557:** diagonal central-boson quotient of PSU(2)_6⊠PSU(2)_6. Fermionic g factors give self-braiding(−1)²=+1 and trivial pointed associator; all16 orbits are free and yield8 objects.

**R313:** corresponding quotient of pseudo-PSU(2)_6 classes1 and2. The frozen unitary data have g self-braidings+i and−i and each has F_ggg=−1; their paired object has both trivial self-braiding and trivial associator. This is an actual Tannakian quotient. The superficially similar mixed ordinary/pseudo construction forR317 is invalid: its diagonal associator is nontrivial.

**R855:** unitary modular D14 even part/local modules of SU(2)_24 at its V24 boson, basisf0,f2,...,f10,P,Q with both P,Q self-dual. P²=P+f0+f4+f8;Q²=Q+f0+f4+f8;PQ=f2+f6+f10. P f_(2j)=sum_(k=6−j)^5 f_(2k)+(P for evenj,Q for oddj);Q interchangesP,Q.

**R239:** C3-algebra Morita dual of an S3 extension of Vec_C7. In BrPic(Vec_C7)=O(C7⊕C7-hat), take r=diag(2,4),s=swap, generatingS3. The order6 action has trivial O3 by coprime7-primary cohomology; O4 is in H4(S3,C*)=0. ENO Theorem1.3 gives the extension. The C3 restriction is pointed C7⋊C3; its3-cocycle is inflated fromC3. Surjectivity H3(S3,C*)→H3(C3,C*) allows an outer twist to make this restriction associative-trivial. The algebra sum_(h∈C3)h gives the actual Morita dual. It is weakly group-theoretical and hence unitarizable. Its neutral Rep(F21) objects arealpha_i,X,Y; oddm_j have dimensionssqrt7. Rules:
alpha_i alpha_j=alpha_(i+j);
X²=X+2Y,Y²=2X+Y,XY=sum alpha+X+Y;
alpha_i m_j=m_(i+j),m_j alpha_i=m_(j−i);
X m_j=Y m_j=m_j X=m_j Y=sum m;
m_j m_k=alpha_(j−k)+X+Y.
Allm_j are self-dual. The full tensor was checked against the source.

**R290:** charge-conjugation C2 crossed extension of unitary modular PSU(3)_4. Its rank5 neutral has no nontrivial invertibles, so O3=0; H4(C2,U1)=0 removesO4. Charge conjugation is the actual tensor/braided symmetry (Edie–Michell2002.03220 Corollary2.7); unitary gauging existence is in CGPW1510.03475 Sections3.2–3.4. Bischoff1807.06131 Proposition1.1 gives odd rank3, equal to the fixed neutral rank. Quantum Weyl alternants in Q(zeta21) reconstruct the neutral category in basis(0,0),(3,0),(1,1),(0,3),(2,2). Its non-self-dual generatorX has regular characteristic polynomial
(t²+t+2)(t³−2t²−t+1).
The odd actionA must have characteristic polynomial t³−2t²−t+1. Normality and its real spectrum force A symmetric; traceA=2 and traceA²=6 force
A=[[0,0,1],[0,1,1],[1,1,1]]
up to odd relabelling. Neutral actions areI,A,A²−I,A,A²−A. Distinct odd dimensions force self-duality, and reciprocity determines all odd products. All512 coefficients matched; model fingerprint
9e793f985c4d50d1fe6b3d4b8b624694b334cd6dcf2c1e0458df4333db2a67ed.
Original verify_psu34_defects.py, psu34_defect_model_proof.md, independent R290_R140_INDEPENDENT_AUDIT.md.

**R868** is proved and independently constructed in the fresh recovery files.

## Rank-eight nonintegral general exclusions

**R784**, dimension44: neutral indices[0,1,2,3,4,6,7] have dimension22 and type1²,2^5; index5 is the unique oddsqrt22 simple. A rank-one invertible component forces a fiber functor. Hopf dimensionpq classification (Etingof–Gelaki math/9801129 Theorem6) makes neutral Rep(D22), since all other Hopf22 possibilities give pointed Rep. The dual fiber-functor category Vec_D22 has rank22, whereas invertibility requires dual equivalent to neutral rank7. Contradiction.

**R181**, dimension42, commutative: neutral dimension21 type1³,3² with adjoint whole is uniquely Rep(F21), from C3 equivariantization of Vec_C7. Invariance under×2 kills the H³(C7,C*) class because it acts by×4; coprime coherence is unique. The unique central invertiblesC3 are preserved pointwise by the odd bimodule, since left/rightalpha actions agree and are free. Relative-center equivariantization and H²(C2,C*)=0 give6 central invertible lifts; its unique order3 subgroup is Tannakian and embeds faithfully inC. De-equivariantizing yields a TY(C7) category with a C3 action by×2 or×4. Such a symmetry must preserve its nondegenerate symmetric bicharacter chi(a,b)=zeta7^(kab), impossible because2² and4² are not1 mod7. This is a general proof and does not use a transparent-fermion argument.
Original dimension42_proofs.md, verify_ty7_obstruction.py.

## Scope-only results and rejected shortcuts

The separate scoped_results.json does not change any general exclusion totals.

Rank-seven pivotal impossibility forR1212,1213,1417,1420 follows from the complete ordinary character screen; general oriented search timed out and remains UNKNOWN. Rank-seven integral general-open116,261,160,387,970,601 admit no braided or weakly group-theoretical category, but this leaves a general gap. R160 remains unitary-open; its proposed negative vector was not a joint fusion character and was rejected. All exact joint-character primary tests were nonnegative.

Rank-eight unitary obstructionsR24,152,153,166,495 use the2D2 neutral category and Grossman's Brauer–Picard computation: components cannot have the required module type or order4 automorphism square. R315/R317 have incompatible FS2(g)=+1 and−1 on overlapping ordinary/pseudo-PSU(2)_6 subcategories; this is unitary-only. R312 has a pseudo-unitary obstruction: Larson's pseudo-PSU rules force FS2(g)=−1, while its other fixed simple forces trivial pointed associator. These scopes were independently audited.

The three multiplicity-one rank-eight casesR9,R18,R49 remain generally open. A finite scalar-tensorator gauge calculation plus Ocneanu finiteness forces specified unique central lifts; R49's113×113 relation matrix has determinant−1, and phase supports mod4 were exhaustively checked. This does not force those lifts to be bosons. A central fermion can fix an underlying simple, as happens with Ising, so no general exclusion was inferred.

Fresh literature audit adds that none ofR9,R18,R49 can be braided (Schopieray, Irrational braided generalized near-groups, Theorem3.6). Published JLMS2023 Lemma3.1 in Categorification of integral group rings extended by one dimension says any two-dimension categorification is Galois conjugate to a pseudo-unitary one. Hence general, pivotal, spherical and pseudo-unitary *existence* are equivalent for these three rings. It does not assert every realization is pseudo-unitary. The earlier arXivv1 literal formulation should not be used.

The known order4 Haagerup–Izumi Morita families do not produce these three rings: standardC4 has noncommutative inversion rules, standardV4 is commutative, and the otherC4 Morita categories have nontrivial gradings. Grossman1612.07185 Theorem4.13/Lemma4.7 closes that known family, not all possible categories. arXiv2609.25185 applies its uniform Q-dual classification to odd cyclic orders and does not solve these even cases.

## Inaccessible work and next release steps

The pre-failure source stage was upper_residual_20261002b, copied into classification-repo/evidence/upper_residual_20261002b. Its36 decisions.json and previous_records.json were generated; application to local ledgers passed. tools/apply_upper_residual_20261002b.py and tools/verify_upper_residual_20261002b.py were written, but the verifier's source hash constants remained PENDING and whole-stage execution was unfinished. The historical verifier dispatch was adapted to preserve the old stage through an isolated historical temporary root.

The rank-seven and rank-eight TeX manuscripts and exact manuscript mirrors were revised to the36-decision counts; citations, environments, mirrors and transcription checks passed. Tables and PDFs were not regenerated. The last2 decisions need incorporation into those inaccessible manuscripts.

After recovery: freeze approved38 decisions; recover all full signed certificates and scripts; generate source hash manifest; run whole-stage normal and optimized verification with historical preservation; regenerate tables; compile and inspect both PDFs; rebuild self-contained archives and manifests; update docs/OEIS; publish a synchronized main commit; then build and deploy the owner-private Site at that exact source commit. Site182 models should become195 after all13 new models. No part of this pipeline is marked complete prematurely.
