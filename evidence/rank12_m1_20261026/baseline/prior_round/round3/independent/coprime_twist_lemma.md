# Coprime-primary associator twists preserve the group-theoretical fusion rules

**Lemma.** Let H be a subgroup of a finite group G, let (omega,psi) define a group-theoretical category C(G,omega,H,psi), and let theta be a normalized 3-cocycle with values in mu_N, where gcd(N,|H|)=1. Then multiplying omega by theta, with a compatible modification of psi, does not change the based Grothendieck ring.

This does not claim tensor equivalence. It is the fusion multiplicities, not associators, that are invariant.

**Proof.** All positive-degree cohomology groups H^j(K,mu_N) vanish for K<=H: transfer annihilates them by |K|, and multiplication by |K| is an automorphism of mu_N. First trivialize theta|H by a mu_N-valued 2-cochain, and extend that cochain to G. Replacing theta by the corresponding cohomologous cocycle makes theta|H identically one. This change gives an equivalent group-theoretical category and permits the original subgroup cochain psi to be used.

A simple subgroup bimodule is indexed by a double coset HgH and an irreducible projective representation of K_g=H intersect gHg^-1. Its multiplier alpha_g is the standard transgression of (omega,psi). Under omega -> omega theta this multiplier becomes alpha_g times alpha_g^theta, with alpha_g^theta a normalized mu_N-valued 2-cocycle. There is a mu_N-valued 1-cochain beta_g with d beta_g=alpha_g^theta. This beta_g is unique: the ratio of two choices is a character K_g->mu_N, and every such character is trivial. Consequently multiplying a projective representation by beta_g identifies the sets of simple objects before and after the twist, preserving their dimensions and supports.

It remains to prove compatibility with tensor multiplicities; triviality of the stabilizer Schur classes alone would not suffice. Use the usual double-coset Mackey decomposition of the balanced tensor product. Each multiplicity is a sum of dimensions of intertwiner spaces over subgroups L<=H. On such a summand the projective representations contributed by the input and output stabilizers are restricted and conjugated to L, and the associator supplies a scalar correction gamma. Write gamma_theta for the ratio of these corrections after multiplying omega by theta. It is a mu_N-valued 1-cochain on L.

Associativity of the actual balanced bimodule action gives the multiplier identity

    d(gamma_theta) = alpha_out^theta / (alpha_left^theta alpha_right^theta)

on L, with the same restrictions and conjugations used in that Mackey summand. This identity can equivalently be obtained by applying the representation multiplication law to the input tensor product and the output; their scalar multipliers must agree. It is a consequence of the 3-cocycle equation, not an assumption that the representations are ordinary.

After the canonical beta changes of projective representations, the remaining scalar correction is

    eta = gamma_theta * beta_left * beta_right / beta_out.

The displayed multiplier identity and d(beta)=alpha^theta imply d(eta)=1. Thus eta is a mu_N-valued character of L. Since gcd(N,|L|)=1, eta is identically one. All Mackey intertwiner spaces are therefore unchanged. Their sums give precisely the same fusion coefficients under the simple-object correspondence. QED.

This argument also explains conjugation/restriction compatibility: any mismatch between the canonical beta choices is again a mu_N-valued character and therefore vanishes.

## Application

For G=A5 x C2 and H the graph of reflection sign on D10, |H|=10. Therefore every 3-primary associator twist preserves fusion rules. Once the relative kernel has been proved to be C3 x C2^2, it suffices for fusion-rule classification to construct the four relative 2-primary classes. No inference that a 3-primary twist is tensor-trivial is made.

The Mackey decomposition invoked here is the standard tensor-product formula for group-theoretical categories; alternatively it follows directly by separating graded H--H bimodules into double cosets and their balanced products into intersection-group orbits. The cocycle comparison above is independent of the precise convention for gamma: reversing the convention replaces eta by its inverse and gives the same conclusion.
