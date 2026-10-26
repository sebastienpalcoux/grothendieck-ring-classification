# Paired stabilizers and isotypic integrality

**Proposition.** Let C be an arbitrary complex fusion category, and let X,Z be simple objects. Suppose a finite subgroup H of invertible objects fixes X on the left and Z on both sides. If m=[X tensor X*:Z]>0, then m*FPdim(Z)/|H| is an algebraic integer.

**Proof.** Choose nonzero isomorphisms rho_h:h tensor X -> X. Their compositions supply multiplication constants on A=direct-sum_(h in H) h for which the direct sum of the rho_h is a left A-action on X. Associativity follows from the module pentagon, or by comparing its two sides after acting on X. Thus A is the twisted subgroup algebra belonging to this actual object's stabilizer cochain. It is connected and separable in characteristic zero. There is no assumption that a preselected trivial cochain works.

Transpose the left action across the evaluation X* tensor X -> 1 to make X* a right A-module. The tensor product X tensor X* is an A--A bimodule with commuting outer actions. Its entire Z-isotypic block mZ is stable: multiplication by each h sends Z to an isomorphic Z on the relevant side, so the actions cannot map that block into another simple isotypic block. Therefore mZ is itself an A-bimodule.

For a connected separable algebra, the A-bimodule category is fusion and its object dimensions satisfy FPdim_(A-bimod)(M)=FPdim_C(M)/FPdim_C(A). This is the normalization in EGNO, Exercise 7.16.9(i), with the Morita-dual identification in Section 7.12. Here FPdim_C(A)=|H|. The dimension of the object mZ in a fusion category is an algebraic integer, proving the assertion. No pivotal, spherical, pseudo-unitary or unitary assumption was made.

This direct proof uses the pairing X,X*: for two unrelated objects fixed by a noncyclic group, their stabilizer two-cochain classes need not agree. For cyclic H, H2(H,C*)=0 removes that issue and recovers the earlier proof. The following stronger square argument avoids matching the cochain classes altogether.

**Stronger proposition (two stabilizer algebras).** Suppose H fixes X on the left, Y on the right, and Z on both sides, with m=[X tensor Y:Z]>0. Then m*FPdim(Z)/|H| is an algebraic integer, for arbitrary finite H.

**Proof.** The actual fixed objects supply two possibly different connected separable algebras A and B, both with underlying object the sum of H. The Z-isotypic block M=mZ is an A--B bimodule. Its rigid dual is a B--A bimodule, so P=M tensor_B M* is an A-bimodule. Put n=|H| and d=FPdim_C(M). The relative-product formula gives FPdim_C(P)=d*d/n. Dividing once more by FPdim(A)=n gives FPdim_(A-bimod)(P)=(d/n)^2. This is an algebraic integer. Therefore d/n is integral over the ring of algebraic integers, being a root of t^2-(d/n)^2; transitivity of integrality makes d/n an algebraic integer. The relative-product formula holds for indecomposable separable algebras; the connected subgroup algebras here meet that hypothesis. An explicit primary reference is Sanford, *Fusion Categories over Non-Algebraically Closed Fields*, arXiv:2401.02354v3, Proposition 3.34, with its bimodule normalization in Corollary 3.32. Over C no endomorphism-field adjustment is needed.

The full arbitrary-X,Y scan is `stabilizer_general.py` / `stabilizer_general.json`. On all 632 input rings it finds 208 already-excluded rings and the same sixteen new cubic_C7 exclusions, with no modeled-ring conflict. Thus the stronger theorem unifies the mechanism but does not add another status change in this input.

For exact testing, put q=|H|/gcd(|H|,m). Since FPdim(Z) is already an algebraic integer, Bezout's identity shows that m*FPdim(Z)/|H| is integral if and only if FPdim(Z)/q is integral. The scaled monic minimal polynomial is tested exactly. The maximal usable H is Stab_L(X) intersect Stab_L(Z) intersect Stab_R(Z), directly computable from the based tensor.

In all sixteen new cubic_C7 cases, one can take X=Z, m=1 and |H|=4. FPdim(X) has irreducible polynomial t^3-4t^2-4t+8. Consequently FPdim(X)/4 has monic polynomial t^3-t^2-t/4+1/8 and cannot be an algebraic integer. The exact original-basis H and X are stored per case in `stabilizer_square.json`.
