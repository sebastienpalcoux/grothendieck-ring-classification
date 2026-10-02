# Independent audit: R7_2_252 and R7_2_315

**Decision: approve the general noncategorification proof.** Scope is all fusion categories over C. No pivotal, braided, pseudo-unitary, or unitary hypothesis is used. The audit was completed on 2026-10-02 independently of the rank-seven agent's narrative and source certificate.

I independently read the original tensor inventory and confirmed both dimensions (1,3,3,6,6,1,2), FPdim96, unique nontrivial invertible at label5, its permutation [5,2,1,3,4,0,6], and full adjoint subring. The source hashes are:

- R7_2_252: c9f5eb30410c18cb4064a11512a3d6db35eadc254e11e1fb7b1eca5610c100ee
- R7_2_315: a0436a52c8844c3389145d0d18441ae63e76b9bc7fb49d8d39f8d8ebc7fffa25

Solvability plus trivial universal grading forces a last C2-equivariantization. The exact invertible permutation gives quotient type (1³,3⁵), FPdim48, rank8. A nontrivial universal grading has order dividing48, hence a prime quotient C2 or C3. The C2 neutral component would have dimension24 and all three invertibles, impossible as24≠3 mod9. A C3 neutral component of dimension16 would contain either one or three invertibles, also impossible modulo9. Thus this quotient again has trivial universal grading.

Its forced last C3-equivariantization has dimension16 below. The five dimension-three simples upstairs consist of either five free orbits, or two free orbits and one triplet of fixed-simple lifts. The former gives a pointed category of dimension16; the latter gives type(1⁷,3), impossible because7 does not divide16. This proves that the lower category is Vec_H^ω, |H|=16. Its C3 action has only the identity fixed, because the three invertibles upstairs already arise from the unit.

The unique central Rep(C3) is preserved by the outer C2 action: trivial universal grading makes Inv(Z(D))→Inv(D) injective, and this central subcategory accounts for every invertible of D. Its equivariantization embeds fully faithfully and centrally into the original category as Rep(G), where |G|=6. The cyclic group would supply six invertibles, contrary to the source ring's two. Hence G=S3, and sequential de-equivariantization gives C=(Vec_H^ω)^S3.

The unit orbit gives exactly the source dimensions1,1,2. Since C3 acts freely outside the identity, all other S3 orbits have size3 or6. Each length-three orbit has cyclic stabilizer C2 and supplies two dimension-three simples; each length-six orbit supplies one dimension-six simple. Thus the source dimensions force orbit sizes(1,3,6,6).

The accompanying ORDER16_ORBIT_LEMMA.md proves this impossible without enumeration. Its center argument covers nonabelian H, and its characteristic-subgroup argument includes4H to eliminate C8×C2. For the two possible abelian groups, every involution fixes at least four elements, whereas the required S3 orbits imply exactly two. The independent exhaustive verifier corroborates all cases and passes unchanged under Python optimization.

The primary categorical sources are ENO arXiv:0809.3031 Theorem1.6 and Proposition4.4; ENO *On fusion categories*, Proposition8.15 (subcategory divisibility) and Proposition8.20 (equal grading-component dimensions); DGNO arXiv:0906.0620 Theorem4.18(i), Proposition4.19, and Proposition4.26 with its equivariant-simple dimension formula. These are the same precise tensor-category statements checked for the independently audited dimension52 exclusion.
