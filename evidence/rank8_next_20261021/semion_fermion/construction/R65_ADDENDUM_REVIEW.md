# Independent review of the R65 pointed-associator refinement

The categorical argument in `../../quadratic/POINTED_COCYCLE.md` is valid,
conditional on its explicitly stated existing general-complex exclusions and
the direct two-Frobenius–Perron-value Galois/pseudo-unitary reduction. It does
not exclude R65 itself.

Assuming the pointed C4 associator is trivial, the subgroup algebra for
H=<g²> exists. Its four simple right modules arise from the four free right
H-orbits. Left H fixes each isomorphism class; the potential projective
multiplier is trivializable because H²(C2,C*)=0. There are therefore two left
linearizations per right module. Inside untwisted Vec(C4), the invertible
bimodule group is H-hat times C4/H, namely V4; this statement does not assert
triviality of its associator. Character twisting swaps the two linearizations,
and the nontrivial coset swaps the two noninvertible right-module orbits.
Consequently the four noninvertibles form a free V4 orbit.

The odd total multiplicity 11 forces the right-action automorphism on that
orbit to be the identity. The duality symmetry then permits a self-dual orbit
representative. Thus the 27 unordered coefficient partitions considered by
`pointed_dual.py` exhaust the possible V4 dual fusion rings. The same argument
gives its 21 self-dual C4 possibilities for comparison.

For each group character parameter m, the formal codegrees have norm
16(m²+4), while the pseudo-unitary dimension has norm 2000. The norm of D/f
in the quadratic compositum is 125/(m²+4), or its square. If D/f is an
algebraic integer, this rational number must be an integer. This remains true
when the two quadratic fields differ; no unjustified identification of their
norm maps is made. The resulting condition |m|=1 or 11 is correct. The three
V4 survivors are excluded by the stated rank-two theorem, rank-four bound,
and the exact R1453 tensor identification with its accepted exclusion.

Hence the pointed associator class of any categorification of R65 is nonzero.
A rank-two module action fixes every module simple under all of C4, and its
scalar module associators would trivialize that class. Both rank-two actions
are therefore impossible. The consequent arithmetic totals 144 possible algebra
objects, 178 induction factors and 30 full-action classes follow from the
previously complete rooted-factor list.

The optional class refinement is also sound. Restriction of H³(C4,C*) to
H³(C2,C*) reduces the class k modulo 2. The rank-four actions have stabilizer
C2, so a realization forces k=2 after the zero class is excluded. Conversely,
if k=2 in a categorification, A=1+g² exists. Its subgroup dual has a free orbit
over an order-four invertible group. The complete C4/V4 reduction forces its
fusion ring to be R65; its rank-four Morita module forces its pointed class
to be 2 as well. Classes 1 and3 allow only the remaining rank-eight necessary
actions. None of these conditional statements supplies an associator.

The source hashes in `pointed_dual.json` were checked against the current
files. The finite coefficient domains, formal-codegree formulas, subring and
tensor-map checks were inspected independently. The producer's normal and
`-O` runs provide the complete finite replay. The earlier arithmetic closure
was independently rerun here against the updated action records; its refreshed
receipt is `quadratic_arithmetic_review_refresh.json`. The previously finalized
nineteen-file semion/fermion package remains unchanged.
