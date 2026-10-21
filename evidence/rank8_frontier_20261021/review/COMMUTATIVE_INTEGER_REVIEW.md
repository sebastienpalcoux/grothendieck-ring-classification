# Independent review of the commutative integer center system

The theorem in `commutative_integer/PROOF.md` and
`integer_central_cubic.tex` is valid as a pseudo-unitary necessary condition.
A negative target result still needs its separate complete signed-sector
and dimension-character gate for general-complex scope. The review does
not turn any lattice membership, rational primal, or integer witness into
a construction of a fusion category.

## Variables, normalization and finite bounds

The source is commutative, so all its irreducible representations are
one-dimensional. Each distinguished central simple occurs once in I(1).
Its character is located by exact equality with the positive dimension
character, rather than assuming an index convention. This matters for
quadratic targets whose FP row is not first.

A low variable is a genuine one-hot choice of restriction for a specific
character. A high variable counts the number of central simples with each
member restriction in a complete source-duality orbit. A two-element orbit
contributes two outer products and two spectral/cubic contributions, with
one integer multiplicity shared by duality. No integrality assumption is
made on earlier averaged phase weights.

The partial S normalization beta_E=D/f_E and the output dual G* in the
Verlinde formula are correct. The product formula is linear in these
actual counts. The full power-basis coordinates of a proposed coefficient
must be (N,0,...,0) with integer N>=0; this assertion is independent of
whether the power basis is an integral basis. All196 non-FP triples
(E<=F,G) are present, with a symmetric cache that retains the dualized
output index. Omitting triples involving the unit cannot create a false
obstruction: these are a stated necessary subset.

Diagonal Gram equations give valid finite multiplicity bounds. With an
atomic low domain the residual used for these bounds subtracts only the
fixed tensor unit, enlarging the high domain safely. For a fully fixed
frame, the additional exact range and rank-one norm test is valid:
H=sum vv^T implies v in range(H) and v^T H^+ v<=1. On any nonsingular
principal rank block I, this norm equals v_I^T H_II^{-1} v_I. No floating
positive-semidefinite decision is used.

The initial cubic upper bound is a bound on the linear constant coordinate,
using each positive coefficient times its variable upper bound. The sharper
bound floor(beta_E beta_F/beta_G) follows directly from positivity in
FPdim(A_E A_F)=sum_Z N_EF^Z FPdim(Z). The implementation reconstructs beta
in the ordered FP field from the allowed restrictions, checks agreement
with the full character field, and takes an exact floor. Both bounds are
necessary, and their minimum is safe.

## Galois balance and support deletion

For each fixed distinguished A_E, the numbers
beta_E chi_E(v)/dim(v), one per actual central simple, are the spectrum of
an integer fusion matrix. Its rational characteristic polynomial has
constant multiplicity on every complete algebraic conjugacy orbit. The
adapter verifies that its field is Galois by finding all roots of its
irreducible defining polynomial in the field and checking the resulting
maps. It enumerates the whole orbit, including conjugates absent from the
candidate list; it does not balance merely the conjugates that happened
to be enumerated as restrictions.

If a candidate eigenvalue has a missing conjugate, its multiplicity must
be zero. All contributing variables are nonnegative, so every candidate
column carrying it has zero multiplicity. The iterative support deletion
is valid by induction: no actual central constituent can be the first
removed one. A missing conjugate of a fixed constituent is an immediate
domain contradiction. Atomic low choices are removed individually, and
an empty character-choice domain is reported as a contradiction. The
filtered API is deliberately not represented as an old phase cone.

## Integer arithmetic and conclusion scope

The reviewed interval updates solve each equality for one variable using
exact floor/ceiling divisions, including negative coefficients. The gcd
test moves fixed variables to the right side. Shifting all free variables
by their propagated lower bounds and reducing their upper bounds preserves
the solution set exactly.

Equation-content division includes the right side and is therefore exact
over integers; proportional-row merging retains the signed scales. The
lifted annihilator is checked on every original column. Hermite discovery
works on the column lattice and returns either directly verified rational
or modular separation, or signed lattice membership. Membership alone does
not certify nonnegative bounded feasibility. Numerical MILP status alone
is never a negative certificate.

## Independent actual-model control

`verify_commutative_integer_control.py` reconstructs the actual center
Z(Fib tensor Vec(C4)). Its64 simples are labeled (a,b,g,h), with a,b
Fibonacci labels and g,h in C4. Forgetful restriction gives4 copies of
e_g,8 of e_(g+4), and4 of e_g+e_(g+4) for every g. This reproduces the
claimed actual multiplicity vector.

The reviewer identifies each distinguished object as (e,e,0,j) directly
from its dimension and character value on the C4 generator. It computes
all196 target coefficients from the actual center fusion tensor, and
compares them to the integer-system auxiliary variables. It also builds
eight actual64-by64 integer fusion matrices from the tensor product model
and compares their characteristic polynomials with the independently
computed full modular eigenvalue products. Thus the positive control
checks actual fusion coefficients and integer matrix spectra, rather than
only their integrality.

The same actual witness passes all Galois equations, sharper FP bounds,
and missing-conjugate support cuts. The reviewer also replays600 complete
finite-field systems,80 incremental-versus-one-shot Hermite calculations,
300 complete bounded integer systems, and100 exact row-compression tests.
All arithmetic assertions remain active under Python optimization.

The source-bound canonical review is:

```
python evidence/rank8_frontier_20261021/review/verify_commutative_integer_control.py
python -O evidence/rank8_frontier_20261021/review/verify_commutative_integer_control.py
```

The receipt `commutative_integer_control_review.json` binds the reviewed
core and proof sources. Target-specific witnesses and exclusions remain
separate and are not asserted by this positive-control theorem review.
