# Independent categorical audit of the conductor-forty obstruction

Auditor: `rank6_center`, 2026-10-16. Status: **PASS** for the categorical
premises, exact domains, and separating-inequality formulation in
`R671_CENTER_TRACE_PROOF.md`.

I independently read that complete proof, its standard-library verifier,
the conductor-equality lemma, and the quadratic residue-saturation lemma.
The separate general-complex scope gate was fully audited and replayed in
`HI6_PAIR_GALOIS_PU_INDEPENDENT_AUDIT.md`. Thus the present positive
spherical argument applies to a Galois conjugate of every hypothetical
complex categorification; it assumes no unitary associator realization.

## Actual character labels and Galois transport

The center character correspondence uses the actual six ordinary
characters, even where their codegrees coincide. The two irrational
ordinary characters lie in Q(sqrt3), disjoint from Q(sqrt10), so an
automorphism flipping sqrt10 and fixing sqrt3 exists. Exponent59 modulo120
is an explicit compatible choice, extendible to the full cyclotomic
field. The rank-one transport formula preserves every other character
evaluation and has the required conjugate dimension evaluation. Character
orthogonality therefore proves it on the whole forgetful row. Integrality
forces B divisible by three, and its overall Galois sign is correctly
removed by requiring the resulting restriction row to be nonnegative.

The unit's transported row is the stated J row. The integral I(1)
multiplicity vector is S-fixed, which makes the support stable with
positive Galois signs. Consequently the unit/J difference has the
quadratic conductor-forty torus character. Rationality of the other
codegrees gives the exact compression -1/sqrt40; rationality of their
character values is not assumed.

## Saturation and the moment domains

The full twist-one projection of S w is exactly -w/sqrt40. Thus a high
object with nonrational dimension ratio has nonzero coordinate in S w,
has twist order dividing40, and cannot have twist one. The last exclusion
uses the equality of the full projection, not an unsupported assertion
that I(1) exhausts every twist-one object.

The residue-saturation lemma applies to primitive order40 modes. I
checked its local Gauss-sum computation and Chinese-remainder factor;
the primitive residue sign is negative. It imposes no primitive-order
requirement on all high objects. The seven restricted moment pairs in
the proof are exactly the pairs for orders2,4,5,8,10,20 and primitive40
with that sign.

For arbitrary twist order the nine-vertex hull is valid without a global
conductor bound. Rational Ramanujan pairs lie in the five rational
vertices: odd order gives (c,c), twice odd order gives (-c,c), and
multiples of four have first moment zero. A nonzero irrational first
moment comes from the primitive chi40 Gauss sum at order40m, where m is
squarefree and coprime to10, and has value plus or minus
sqrt10/(8*phi(m)); its second moment is zero. Irrational second moments
come similarly from order80m with first moment zero. The origin and all
scaled such pairs are in the stated hull.

Galois partner rows may be assigned common relative moments. Indeed
normalized relative trace to K commutes with cyclotomic Galois
automorphisms, and modular symmetry transports a twist by sigma squared.
Since sigma squared fixes quadratic K, every relative moment is
unchanged. This observation requires neither the actual twists to be
equal nor a twist-order bound. On the restricted level40 rows, the
explicit exponent59 gives equal actual twists as well.

Every source second indicator is positive: in fact each source simple
occurs with odd multiplicity in some X X*. The canonical pivotal
sandwich form has positive transpose sign. In particular nu2(g)=1;
positivity in Tr(theta^2 I(g))=dim I(g) forces theta squared equal to one
on every constituent containing g. Intersecting this with the preceding
high nonrational restriction leaves only twist minus one, as used.

## Exhaustive finite formulation

The low rows all have unit multiplicity one, fixed central dimension
D/f, and fixed total F I(1). Thus the bounded labelled-row enumeration
contains every possibility. Character reciprocity and residual Gram
positivity are necessary conditions, and exact rational Schur
complements implement the latter.

For high rows, coordinate bounds follow from the residual Gram diagonal.
The condition D/z integral follows because the center formal codegree
(D/z)^2 is integral; transitivity of integral dependence implies D/z is
integral. The use of O_K=Z[sqrt10] is correct. Each actual pair of
distinct Galois row types has equal multiplicities and is represented by
one of the retained two-row orbits; a fixed row type is represented by
a singleton. Subtracting one such orbit gives a necessary PSD and
entrywise-nonnegative residual test.

Taking a convex combination of its relative trace vertices preserves
the common Gram column, and the moment columns use the product of the
restriction multiplicity, central dimension, and relative twist trace.
The targets subtract each known twist-one low object once. The second
trace target is D for every nonunit source simple because all second
indicators are positive. No factor of source or central dimension is
missing.

An actual center would therefore give a nonnegative real combination of
these 56-entry columns equal to the stated target. Each exactly checked
integer covector nonnegative on all columns and negative on that target
is a valid Farkas contradiction. No sufficiency of modular data, no
known HI(C6) center classification, and no numerical feasibility result
is used.

An exploratory third-indicator shortcut asserting that self-duality
forces real higher indicators was withdrawn and is not part of this
proof or its verifier. The present argument uses only second indicators
and real normalized relative traces of twists.

The independent optimized replay completed with PASS for all six frames.
It reproduced orbit counts 73,85,73,28,36,28 and moment-column counts
360,398,360,138,168,138. The exact target pairings are -225800939520 for
the first three frames and -960 for the last three; all minimum column
pairings are zero. The receipt is
`r671_center_trace_rank6_independent_optimized.json`.
