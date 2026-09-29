# Deferred refinement: Galois balance with a phase permutation

This note records a possible strengthening of the quartic necessary systems.
It has **not** been implemented or used in any exclusion in this release.
The certificates and their audited verifiers remain unchanged.

Let `K = Q(zeta_F)` be the ambient field used for dimensions, low-row central
fusion eigenvalues, and normalized relative twist traces. For a central simple
`Z`, write `tau(Z)` for its augmented dimension/eigenvalue type, and write
`phi(Z) = (Tr_K(theta_Z^j))_j` for its normalized relative-trace tuple.

For a cyclotomic Galois automorphism with exponent `ell`, the standard Galois
symmetry of the canonical Drinfeld-center modular representation gives
`theta_(hat_sigma(Z)) = theta_Z^(ell^2)`. The center has trivial multiplicative
central charge, so the canonical twist matrix supplies this normalized
representation. If `h` is the restriction of the automorphism to `K`,
commutation of relative trace with the abelian cyclotomic Galois action gives

`phi(hat_sigma(Z)) = h^2(phi(Z))`.

Meanwhile its augmented type transforms by `h`, including the usual positive
normalization of the dimension by the global dimension. Thus an actual center
has equal multiplicities of the joint states

`(tau, phi)` and `(h(tau), h^2(phi))`.

For a quadratic ambient field, `h^2` is trivial and this recovers the existing
balance at each fixed relative-trace type. For the quartic real fields inside
conductors 16 and 20, squares can act nontrivially, so keeping the phase fixed
would be unjustified. The correct prospective refinement permutes phase
tuples by `zeta_F -> zeta_F^(ell^2 mod F)`. The finite phase domain is closed
under this action, including its all-zero tuple for outside-box orders.
Low summands of the canonical induction have phase tuple `(1,1,...)` and stay
in that phase class.

A future implementation should reconstruct these joint-state maps exactly,
verify their closure and all forced low counts, and check the resulting
linear balance equations. No discovery on the remaining quartic inputs was
started using this proposal during the present release.
