# No soft tensor autoequivalences for either rank-four ring

**Theorem.** Let C be any complex fusion category whose based ring is either ordinary PSU(2)₆ or pseudo-PSU(2)₆. Every tensor autoequivalence inducing the identity permutation of simple objects is tensor-isomorphic to the identity functor. No pivotality, unitarity, or classification of associators is assumed.

Use the basis (1,f,x,fx), where f²=1 and f exchanges x and fx. In the ordinary ring x²=1+x+fx, while in the pseudo ring x²=f+x+fx. This distinction specifies both rings completely.

A tensor autoequivalence acting trivially on simple isomorphism classes is naturally isomorphic, as a linear functor, to Id. After normalizing its unit constraints, its tensorator is a nonzero scalar j_ab^c on each nonunit admissible trivalent vertex. There are 17 such vertices. Tensor-functor coherence at a nonzero associator entry F^{abc}_d[e,f] is the monomial equation

j_ab^e j_ec^d = j_bc^f j_af^d.

The associator scalar cancels: only whether it is zero matters. Object rescalings (λ_f,λ_x,λ_fx) act by j_ab^c=λ_a λ_b/λ_c. This gauge image is a connected three-dimensional algebraic torus. Its dimension is three because its kernel is Aut⊗(Id_C)=Hom(U(C),C×), which is trivial for both rings (the fusion supports force all three scalars to be one).

First retain only associator blocks with exactly one admissible left channel and one admissible right channel. Their entries must be nonzero by invertibility. The resulting integer exponent lattice has rank 12, is saturated, and therefore cuts out a connected five-dimensional subtorus of (C×)¹⁷. This is a tensor-independent statement about the two finite fusion tables.

The residual exponent classes of **every possible** associator entry have the following small form modulo this rank-12 lattice:

- Ordinary ring: six nonzero classes ±p, ±q, ±(q−p).
- Pseudo ring: four nonzero classes ±p, ±q.

Every two rationally independent classes in the appropriate list extend the initial lattice to a saturated lattice of rank 14. Equivalently, the Smith normal form has fourteen nonzero entries, all equal to 1. The accompanying `soft_aut_universal.py` generates every admissible channel from the fusion tensor, verifies the initial rank/saturation, lists all residual classes, and checks every independent pair. Thus **no actual F-symbol zero pattern is assumed**.

By Etingof–Nikshych–Ostrik, *On fusion categories*, Theorem 2.31, a fixed source and target fusion category have only finitely many tensor functors up to tensor isomorphism. Consequently the actual tensorator solution group, modulo the three-dimensional gauge torus, is finite. Its defining exponent lattice must have rank 14: smaller rank would give a positive-dimensional family of inequivalent tensor functors, and larger rank is impossible because the three-dimensional gauge torus is always contained in the solution group.

Therefore the actual nonzero F-support supplies two independent residual exponent classes. Any such pair already cuts out a connected three-dimensional torus. It contains the full three-dimensional gauge image, hence equals that image. Further actual coherence constraints cannot cut down the gauge image. The entire tensorator solution group is therefore the gauge image, proving the theorem.

Primary rigidity reference: https://annals.math.princeton.edu/wp-content/uploads/annals-v162-n2-p01.pdf, Theorem 2.31, p. 592; also https://arxiv.org/abs/math/0203060. The theorem states both undeformability and finiteness of tensor functors up to equivalence.

## Verification scope

`soft_aut_support.py` writes the two finite fusion tables and vertex lists. Its exploratory unit-intermediate rows are **not used** by `soft_aut_universal.py`; the theorem uses only its rows labelled `singleton`. The latter verifier independently generates all other admissible associator entries. This avoids any premise about nonvanishing of a unit row or a special gauge.

The lattice certificates are `P_soft_aut_universal.json` and `Q_soft_aut_universal.json`. Their independent-pair counts are respectively 12 and 4, with no nonprimitive pair.
