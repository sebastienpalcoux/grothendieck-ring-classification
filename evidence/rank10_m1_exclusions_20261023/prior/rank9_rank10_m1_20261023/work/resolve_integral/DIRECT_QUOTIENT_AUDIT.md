# Independent audit of direct quotient completion

**Verdict: accepted, with no census-completeness premise.** Every dimension-24
quotient of profile `(1^4,2^5)` arising from any of the four source rings
R9_1_12, R9_1_62, R9_1_87 and R9_1_108 has based ring R9_1_117.
The construction in `work/resolve_rank9_neargroup/direct_quotient.py` is
exhaustive among all nonnegative integer quotient tensors. Its canonical
restriction matrix and binary search do not omit possible categorical
quotients.

The independent replay is
`work/resolve_integral/verify_direct_quotient_audit.py`, with receipt
`direct_quotient_audit.json`. It imports none of the author's code. It uses
only the original input tensors, the verified dimension values (checking
all dimension equations itself), and the proposed output receipt for
comparison after its own enumeration. It passes both ordinary Python and
`python -O`.

## Canonical restriction matrix is complete up to relabeling

For a C2 equivariantization, a fixed quotient simple has two lifts differing
by the sign, and a free quotient orbit has one induced simple. The cyclic
stabilizers have no nontrivial projective dimensions. Conversely these
possibilities are recovered from the sign's action on source simples.
For the desired profile there is exactly one possible sign in each source.
Its source orbits comprise two pairs of invertibles, one fixed dimension-2
object, one pair of dimension-2 objects, and two fixed dimension-4 objects.

Label the quotient images of the invertible pairs by 1 and a, with the pair
containing the source unit mapped to 1. Label the two constituents of the
fixed dimension-2 source object b,c. Label the common image of the paired
dimension-2 source objects m. Finally label the constituents of the two
fixed dimension-4 source objects x,x' and y,y'. These choices give exactly
the stated F and the involution `(b c)(x x')(y y')`.

Any actual quotient admits these labels. Choosing their order is only a
change of quotient basis; it does not impose any product, pointed-group
structure, duality or nonneutral pairing. Arbitrary central structures on
the same underlying sign do not invalidate this orbit description. The
independent checker reconstructs F from the source orbits without importing
the canonical-restriction function and obtains precisely the proposed F.

## All dualities and integer coefficients are considered

The checker independently enumerates every dimension-preserving permutation
of the quotient basis, then retains exactly the involutions fixing the
unit, commuting with alpha, and satisfying the dual-compatibility equation
for F. The counts are eight branches for 12 and 62, and four for 87 and 108.
They agree with the author's enumeration; there is no prescribed duality.

The only tensor-variable identifications are the two noncommutative
Frobenius reciprocity identities and equivariance under alpha. No
commutativity, invertible group, adjoint grading or target quotient ring is
assumed. The independent checker computes these equality classes by
breadth-first orbits, whereas the original uses union-find.

Unit, duality, positive dimension and restriction equations are necessary
for every categorical quotient. Their coefficients are nonnegative.
For every variable, the minimum of `floor(rhs/weight)` over equations
containing it is at most one. The independent regeneration verifies this
before any binary search. In the eight-branch cases there are 60 zero-bound
and 32 one-bound variables; in the four-branch cases there are 52 and 31.
Thus nonnegative integer coefficients outside {0,1} are rigorously excluded
by the equations themselves. A separate multiplicity-free theorem is not
required.

## Exhaustive search and independent result

The author's subset-sum propagation is sound: a binary value is rejected
only if the other positive weights cannot attain the remaining target.
Otherwise both values are eventually branched on. Updating several forced
values within one pass does not create an invalid rejection, because each
forcing is already necessary under the preceding partial assignment.
No leaf is accepted before every variable is assigned and all associativity
equations are checked.

The independent checker deliberately uses a different, weaker propagation:
only residual lower/upper interval bounds and one-variable interval tests.
It branches on the smallest remaining variable, not the author's heuristic.
It then checks all associativity equations. These differing searches obtain
identical complete solution sets, compared by hashes of all 729 coefficients.

| Source | Duality branches | Linear tensors | Associative tensors |
| --- | ---: | ---: | ---: |
| R9_1_12 | 8 | 36 | 4 |
| R9_1_62 | 8 | 36 | 4 |
| R9_1_87 | 4 | 4 | 4 |
| R9_1_108 | 4 | 4 | 4 |

Every associative tensor matches R117 under the supplied explicit based
permutation; the independent checker verifies all 729 coefficients of each
map. The R117 tensor is consulted only after the quotient enumeration has
finished, for identification. No list of possible quotient rings is used
as an enumeration filter.

This replaces the earlier seven-candidate census step in the dimension-48
exclusion theorem. Together with the independently accepted exhaustive
triality and near-group action theorems and the rank-six central-boson
reduction, it establishes the exclusions of R9_1_62 and R9_1_87 over C
without an upstream census-completeness assumption.
