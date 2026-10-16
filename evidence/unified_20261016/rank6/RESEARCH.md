# Rank-six follow-up: Morita constraints, higher indicators, and one witness obstruction

Date: 16 October 2026. Verdict: both categorification questions remain open.
The historical rank-37 modular witness is now excluded by a half-integral
Verlinde coefficient; the earlier weaker necessary system still passes.

## A new uniform necessary identity

Let B be a braided fusion category containing a fermion f, and let A=1+f be the regular algebra of its underlying Vec(C2). Let M=B_A and write M_i for the matrices of the simple objects of B acting on the simple right A-modules. Then

\[
\sum_i M_i[a,b]M_i[c,d]
 = \sum_i M_i[c,a]M_i[d,b]
\tag{1}
\]

for all module labels a,b,c,d.

Here there is a categorical reason to prescribe the entire dual category, stronger than merely searching for an arbitrary dual Gram factorization. The algebra 1+f is the one-generator Clifford algebra in sVec. Its Azumaya morphism A tensor A^op -> End(A) is an isomorphism. This can be checked inside sVec, and a braided embedding sVec -> B preserves that isomorphism. Therefore both alpha-induction functors B -> A-bimodules(B) are tensor equivalences. Their actions on M have precisely the matrices M_i. The usual linking-category associativity/Frobenius-reciprocity identity now gives (1), since both sides of the Morita context have the same prescribed simple action matrices.

Primary reference for the Azumaya criterion and its equivalence with alpha-induction being equivalences: Davydov–Nikshych, *The Picard crossed module of a braided tensor category*, Section 3.2, Definition 3.5 and the paragraph immediately following it:
https://arxiv.org/html/1202.0061v1#S3.SS2

This argument applies to braided B. Merely knowing that a nonbraided category has a commutative Grothendieck ring does not identify the two module actions. That replacement would be invalid.

## Exact application to R6_4_155

The forced rank-26 modular candidate B has fermion label 0 and unit label 1. Its A-module candidate has rank 22. I reconstructed the complete 26 matrices directly from the published six-dimensional anti-invariant witness and tested (1) on all 22^4=234,256 ordered quadruples. Every identity holds exactly.

The new identity therefore gives no exclusion. It does strengthen the exact scope of the passing witness: the numerical linking data are compatible with the specifically required Azumaya self-Morita dual, not just with an unspecified abstract dual ring. It still supplies no associativity constraints or actual module category.

Replay:

    python work/unified/rank6_center/verify_fermion_crossing.py --repo repo

The replay uses only Python's standard library and binds the published modular data and anti-invariant witness by their fixed SHA256 hashes. Both `--repo` and automatic repository-root discovery are supported. The receipts are `fermion_crossing_receipt.json` and `fermion_crossing_receipt_optimized.json`. The frozen prior inputs are unchanged. The dated manuscript supplement gives the full index convention and linking-category derivation.

## A forced third indicator for R6_8_1660

The entire twist-one sector has already been identified categorically. Its
saturated quadratic torus lines therefore belong to unique multiplicity-one
irreducible summands of the finite modular representation. Exact character
averages give their matrix coefficients and hence weighted higher indicators.
Exhausting all 532 finite-group irreducible pairs leaves four possible pairings
of the two saturated sectors. Third rotation on the three-dimensional space
Hom(1,X^3) excludes the two mixed pairings.

Consequently nu_3(T)=2 and nu_3(X)=nu_3(gX) is either 2+omega or 2+omega^2,
where omega is a primitive cube root. The same argument gives nu_5(X)=nu_5(T)=2,
nu_7(X)=3 and nu_7(T)=4. These statements use the canonical positive spherical
structure on the established positive Galois representative. They do not assume
that higher indicators of self-dual objects are real.

The two surviving choices are conjugate. The historical rank-37 necessary-system
witness uses one of them and passes these indicator constraints. The separate
Verlinde calculation below excludes that particular witness. Neither result
constructs a category or excludes every remaining profile.

The full proof, independent audit, source-bound standard-library replay and
identical normal/optimized receipts are in `higher_indicators/`. Run

    python evidence/unified_20261016/rank6/higher_indicators/verify_r1660_higher_indicators.py --repo .

from the repository root, and repeat with `python -O`. The verifier regenerates
the torus, compression and matrix-coefficient traces directly from the frozen,
previously certified local character tables, and checks the complete source
tensor's invariant-space dimensions. No previous inputs are modified.

## Other unified routes inspected and their limits

1. **Two-orbit Morita descent.** R6_4_155 already has an exact Morita analysis. The proposed descent to a near-group category of order 8 and level 16 requires a coherent symmetry exchanging its two noninvertible objects. Equality of their dimensions and the ring involution do not construct that symmetry. The canonical intermediate condensation instead gives C tensor Rep(C2), as the existing proof establishes. Schopieray's elementary-abelian near-group classification cannot be applied before such a descent and the pointed group are proved.

2. **An Ising complement as an invertible bimodule.** For R6_8_1660, the complement of the Ising subcategory is regular as a left Ising module. Its relative-center analysis has already determined the surviving quadratic ring, including the nontrivial t-dual and the coefficient object 2(sigma,1)+2(sigma,g)+3(sigma,sigma). This is not an ordinary rank-two fusion category: the coefficient is an object of Z(Ising), so applying Ostrik's scalar rank-two classification would be invalid. The remaining pentagon is genuinely enriched over Ising.

3. **Small module dimensions.** The complete rank-six Morita list already includes the rank-six Ad(E6) alternative and one noncommutative rank-eight alternative. Its small Ad(E6) subcategory is itself categorifiable, so restricting to it yields no contradiction. Treating the complement as a faithful group-graded component would contradict its actual fusion rules and the established trivial universal grading.

4. **Integral finite modular representations.** The historical rank-37 SL2(Z/48) witness still passes its original 1,536 linear equations. The new exact Verlinde argument excludes that specific restriction/twist/representation witness by a half-integral coefficient. It does not exclude other refinements of the retained profiles.

5. **Known general constructions.** The published no-Tannakian-center theorem already blocks nontrivial finite-group extensions and equivariantizations as the final operation in either Morita class. Recent near-group and odd-order Haagerup–Izumi construction papers do not apply to either of these forced rings merely from a quadratic field or a matching global dimension.

## Result

The new indicator refinement establishes no general, pivotal, spherical, pseudo-unitary, or unitary existence or nonexistence theorem. In particular, neither rank-six ledger entry should change. The unresolved issue is coherent categorical realization of the surviving center/relative-center data, not an omitted rank-six involution or an untested linear equality from the existing witness system.

## Exact rejection of the historical rank-37 witness

The standalone replay in `verlinde_obstruction/verify_r1660_witness_verlinde.py` first rechecks the historical 1,536 equations and 1,447 bounds, all of which still pass. It then combines the saturated rank-one modular summand with the exact finite-group character table to obtain the impossible center fusion coefficient N(A,B;B)=1/2. The visible symmetric doublet contributes 2 and its one-dimensional hidden difference contributes -1. The proof and independent audit identify the two lines and verify that the mixed term vanishes.

Only this specific restriction, twist, and modular representation witness is rejected. Both source categorification questions and the other R6_8_1660 profiles remain unresolved. Run the checker with `--repo .`, also with `python -O`; its normal and optimized receipts agree. Frozen earlier inputs and historical PASS receipts are unchanged.
