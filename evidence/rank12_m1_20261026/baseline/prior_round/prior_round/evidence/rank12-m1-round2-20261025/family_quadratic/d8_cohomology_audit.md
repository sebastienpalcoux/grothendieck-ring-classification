# Independent coverage audit for the dihedral associator classes

**PASS.** The sixteen recorded relative fourth-root cocycles represent exactly eight complex cohomology classes. All eight admissible complex classes are covered.

`audit_d8_cohomology.py` uses integer Hermite normal form of the lattices [d2 | 4I] and [d2 | 8I], with 343 normalized three-cochain coordinates and 49 normalized two-cochain coordinates. This is independent of the constructing agent's modular kernel/cokernel reduction. Each candidate is normalized, satisfies all 4096 cocycle identities and has trivial restriction to the chosen order-two subgroup. The fourth-root lattice gives sixteen distinct classes. The eighth-root lattice gives the class labels

    0,0,2,2,5,5,7,7,4,4,6,6,1,1,3,3.

Thus each of eight classes appears twice. The exact input hash and lattice data are in `d8_cohomology_audit.json`. This supplementary calculation took about 24 seconds; it was a fixed certificate audit, not a search for associators.

For the complex-coefficient bound, Goff--Mason--Ng, *On the Gauge Equivalence of Twisted Quantum Doubles of Elementary Abelian and Extra-Special 2-Groups*, arXiv:math/0603191v3, Lemma 4.1(b), gives H3(D8,C*)=C4 times C2 times C2. Lemma 4.5 gives surjective restriction to the rotation subgroup C4. Restriction from that C4 to its subgroup C2 is also surjective, since the generator of integral H2 restricts to the generator and its square generates H4. Hence the kernel relevant to the actual subgroup algebra has eight complex classes. The coefficient exact sequence for fourth powers shows that fourth-root cocycles cover H3(D8,C*), since this group has exponent four.

It remains to ensure that distinct eighth-root lattice classes among the fourth-root inputs cannot become equal over C*. Here H2(D8,C*) has exponent at most two. One elementary verification uses projective lifts R,S of r,s, rephased so R^4=S^2=1. Their remaining relation is S R S^-1=zeta R^-1 with zeta^4=1. Rephasing R by a fourth root changes zeta by a sign, so squaring any projective class makes it trivial. If a fourth-root three-cocycle is a complex coboundary d beta, then beta^4 is a two-cocycle and beta^8 is a coboundary. Rephasing beta by the coboundary of a suitable one-cochain makes beta eighth-root valued without changing d beta. Therefore eighth-root coboundaries detect every complex equivalence between the recorded fourth-root cocycles.

The eight distinct lattice classes are consequently eight distinct admissible complex classes, equal to the entire allowed kernel. Together with the separately established categorical Morita converse and the complete dual-tensor replay, this is sufficient coverage for the dimension-forty classification argument. This receipt by itself assigns no ring status and does not replace those categorical premises.
