# Independent audit of the census-independent quotient reconstructions

I read the final local versions of `../d48/quotient_reconstruct.py`,
`rank9_reconstruct.py`, and `ring_utils.py`, including their frozen input
format, and replayed both reconstructions under Python `-O`. Both pass.
The exact tensor utilities verify all coefficients of every final based
isomorphism; no identification is based on dimension profiles alone.

## Binding and complete finite domains

The source routine verifies each frozen tensor hash, fusion axioms, exact
dimension character, multiplicity one, and full adjoint closure. It enumerates
every nontrivial based central involution and recomputes its orbit tensor.
The orbit quotient's well-definedness is checked for every pair of source
representatives. Every identified orbit tensor is matched by a full based
map, preserving its dimensions. The types of the actual hypothetical
de-equivariantizations follow from the usual cyclic-stabilizer equivariant
simple-object formula; their orbit-sum image is this recomputed tensor.

For rank twelve, all five groups of order eight are included. All involutive
group automorphisms with four fixed invertibles are enumerated. Every action
on the four noninvertibles is generated from all assignments of permutations
to a group generating set, with the entire Cayley relations checked. Left
and right actions are independently included, with inversion converting a
right action to a homomorphism. Commutation of the actions and compatibility
with the specified quotient involution are imposed. Source invariant-ring
commutativity is checked before the same action-candidate filter is used on
both sides, and the final two-sided orbit constraints are checked directly.

All possible duality involutions are included. Reciprocity fixes all output-
invertible coefficients. The remaining coefficient identifications use only
reciprocity, duality, equivariance and associativity with an invertible
factor. Every identification is a necessary equality in a true based ring.
The source orbit coefficients explicitly bound every remaining coefficient
by one; after these equalities there are at most three binary variables.
Every assignment is tested against dimension, every orbit equation and full
associativity. Thus the search is an exhaustive small finite proof, not an
assumption about completeness of a previous census.

The four invariant source classes produce, respectively:

| First source | Distinct reconstructed rings |
|---|---|
| R12_1_130 | R12_1_351 |
| R12_1_175 | R12_1_513 |
| R12_1_216 | R12_1_351 |
| R12_1_319 | R12_1_513 |

## Rank-nine reconstruction and its bounded linear solver

Here all groups of order four, all actions on five noninvertibles, all
commuting left/right pairs, and all compatible dualities are included. The
outer action fixes the four invertibles and one dimension-two object and
exchanges the other four in two pairs, exactly as required by the source
equivariantization pattern. There is no assumption of multiplicity one or
of a C3 grading for the reconstructed rank-nine ring.

After the same necessary coefficient equalities, all unknown coefficients
are bounded nonnegative integers. Their equations have nonnegative integer
entries: they are orbit-sum equations and dimension equations. The bound
for each variable is the minimum of floor(rhs/coefficient) over its rows.
The recursion rejects only a residual outside the possible interval, fixes
all variables in a row only when the residual is an endpoint, or solves a
single remaining variable by exact divisibility. It otherwise branches over
every integer from zero to its bound. These propagation rules are complete
and cannot discard a feasible nonnegative solution. The full orbit tensor
and all associativity identities are checked after each solution.

The four rank-nine invariant source classes have respectively one, zero,
one, zero based-ring lifts:

| First source | Linear solutions | Associative labelled tables | Isomorphism classes |
|---|---:|---:|---:|
| R12_1_175 | 36 | 24 | 1, invertibles V4 |
| R12_1_216 | 12 | 0 | 0 |
| R12_1_244 | 12 | 8 | 1, invertibles C4 |
| R12_1_410 | 4 | 0 | 0 |

There are twelve actual source/involution bindings. Both surviving rings
have full adjoint closure, exactly one nontrivial based central involution
h, and h fixes all five noninvertible simples. Both have **no** exhibited
C3 grading; that absence is preserved honestly. The final argument below
does not use the false implication that dimension type 1^4,2^5 alone forces
a C3 extension of a TY8 category.

Deduplicating by based-ring isomorphism is harmless for the properties used:
full adjoint closure, unique based central involution and its action on
simples are ring-isomorphism invariants. Since the involution is unique,
every outer tensor action must preserve it. Here the actual outer action
even fixes all four invertibles individually.

## General-complex categorical conclusion for the rank-nine survivors

An integral dimension-twenty-four fusion category D is solvable by the ENO
prime-power-dimension theorem. Take the last nontrivial step of a solvability
presentation. Since U(D)=1, this step cannot be a faithful extension. If it
were equivariantization by C3, its canonical Rep(C3) would give three
invertibles, impossible in the group of order four. Hence

    D = E^(C2),  FPdim(E)=12.

Its canonical nontrivial representation h must be the unique based central
involution already found. A simple of D fixed by tensoring h comes from a
free two-element orbit in E. Conversely a fixed simple of E has two
one-dimensional equivariant lifts exchanged by h; H2(C2,C*)=0 rules out
additional projective cases. The four invertibles of D therefore descend
to two fixed invertibles of E. The five h-fixed dimension-two simples each
descend to two invertibles. All twelve simples of E are invertible, so E
is pointed.

The original outer C2 action on D fixes h. A central structure on a given
underlying invertible is unique when U(D)=1: the ratio of any two such
half-braidings is a tensor automorphism of the identity, hence a character
of U(D). Consequently the outer action preserves the actual central
Tannakian Rep(C2), not merely its based-ring span.

Equivariantizing this preserved central symmetric subcategory gives a
central Tannakian category of dimension four in the original C48. It is
Rep(P) for a group P of order four, including either possible action
coherence. The composite tensor functor C48 -> D24 -> E12 kills this
subcategory, and transitivity of de-equivariantization identifies its
Rep(P) quotient with E12. Equivalently the induced quotient functor is
dominant and both categories have dimension twelve, so it is an
equivalence. Thus C48 is E12^P with E12 pointed. It is group-theoretical,
being Morita equivalent to the pointed crossed product E12 crossed P.

Result: PASS for the finite reconstruction/exhaustion and this categorical
closure. No unitary classification, incomplete lower-rank census, or
unsupported C3 grading is used.
