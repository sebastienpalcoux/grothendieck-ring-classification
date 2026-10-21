# Independent review: R8_3_567 is excluded over the complex numbers

Outcome: **PASS**, after the unrestricted Galois-pseudo-unitary scope gate.
This is a separate AI mathematical/computational review, not a human or
proof-assistant certification. No Morita reduction or forced-indicator
argument is needed for this exclusion.

## General scope and integral-center restriction

The previously reviewed all-parity signed-sector gate proves that any complex
categorification of R567 has a pseudo-unitary Galois conjugate with the same
based ring. The full source tensor has only the unit among ring-central
invertibles, and its adjoint subring is the entire ring. The center therefore
has no nontrivial invertibles, including none in the forgetful kernel.

The source dimensions are six copies of 1 and two copies of 3+2 sqrt(3).
The integral-center theorem applies with D=48+24 sqrt(3) and
Norm(D)=576: a nontrivial integral central subcategory would have dimension
dividing 576, hence be solvable and possess a nontrivial invertible. Thus every
nonunit integral-dimensional central simple is forbidden. This theorem uses
FP dimensions and does not add a pivotal restriction to the scope.

## Independent complete domain

The replay `verify_r567_verlinde.py` uses the previously independently reviewed
full-box low/high enumeration routines, and the frozen exact scalar-algebra
primitives. It imports none of the new R567 producer source, Gram, or cubic
code. New calculations are independently implemented for partial-S eigenvalue
integrality, the complete integer Gram enumeration, duality, and the final
cubic coefficient. The source tensor and every mathematical dependency are
hash-bound in the review receipt.

The complete scalar algebra is C^4 plus M2. All scalar multiplication
identities and all five character orthogonality identities are checked. The
matrix character is independently reconstructed from the regular trace:

    trace(N_i) = sum of the four scalar characters at i + 2 trace_E(i).

Its character degree is 2, so the distinguished-row identity is

    S_(A_E,Z) = D/(f_E dim(E)) trace_E(FZ).

This factor of 2 is retained in every partial-S test. There are five distinct
distinguished central simples: the M2 object occurs once in a sum over central
simples, while its restriction has unit-coordinate 2. No multiplicity of 2 is
incorrectly inserted into the Verlinde sum.

Complete low boxes give column counts 3,2,2,3 and five low frames. Exact full
S symmetry in Q(sqrt(3),i) leaves one frame, with the two permitted
equal-codegree character labelings. The earlier raw high-domain enumeration
gives all 45 columns. The new checker independently computes the degree-four
regular multiplication characteristic polynomial of every proposed
distinguished S eigenvalue. It removes precisely the nine indices
9,13,16,24,27,30,32,33,42. The integral-center theorem removes indices 0,34.
It verifies that i is integral and (1+i)/2 is not as exact nonreal arithmetic
controls. Thus 34 high columns remain.

Every high vector has the form (u,u,p,q,w,w,w). The full seven-coordinate
Gram system is checked equivalent, entry by entry, to the four-coordinate one
in the order (u,w,p,q):

    [4 0  4  4]
    [0 4  6  6]
    [4 6 42 31]
    [4 6 31 42].

A third independent memoized generating-series coefficient extraction
enumerates all 1071 nonnegative integer Gram patterns, matching the producer's
two exhaustive algorithms before duality. The dual action on high columns is
reconstructed from the original source tensor. Its exact multiplicity-equality
filter leaves precisely 155 patterns. The resulting full multiplicity vectors
agree individually with the producer receipt, not merely in number.

## Cubic obstruction and normalization

The final obstruction uses only the real scalar conjugate-FP character chi,
with f=D'=48-24 sqrt(3). Its distinguished central object A is self-dual.
The row is real, or equivalently A is the unique distinguished object with
its dimension D/f. The unnormalized Verlinde formula is

    N_(A,A)^A = (1/D^2) sum_Z S_(A,Z)^3/d_Z,
    S_(A,Z)=(D/f) chi(FZ).

The independent checker evaluates this formula directly in Q(sqrt(3)), with
the five low objects once each and the full integer high multiplicities. It
also checks the row norm sum_Z S_(A,Z)^2=D^2 on every pattern. The result is

| Cubic coefficient | Complete dual-compatible patterns |
|---|---:|
| 1/3 | 84 |
| 4/3 | 71 |

Neither value is an integer. Thus no pseudo-unitary category with this ring
exists; the independently established Galois gate excludes every complex
categorification.

Although the producer supplies all 40 nonunit distinguished triple formulas
with complex dual character map (0,1,3,2,4), this conclusion needs only the
real scalar triple (1,1,1). There is no real-part projection, twist averaging,
or phase assumption in this last obstruction.

## Known control and replays

The independent known-model control is the actual center of Vec(S3). Its
distinguished sector is Rep(S3), with character degrees 1,1,2 and codegrees
6,6,3. The restriction columns of the distinguished objects are e,e,2e;
these are three objects counted once each. The remaining five center objects
come from the nonidentity conjugacy classes. All 27 distinguished Verlinde
coefficients are checked against the full Rep(S3) tensor. This checks both
the matrix-character normalization and the low-object multiplicities on an
actual noncommutative source. The producer additionally supplies a Fibonacci
center control.

Canonical independent read-only replay:

    python evidence/rank8_frontier_20261021/review/verify_r567_verlinde.py
    python -O evidence/rank8_frontier_20261021/review/verify_r567_verlinde.py

The producer's optimized `r567_centerless_integer/verlinde_exclusion.py`
was also independently replayed. All runs passed.

The primary-source normalization is Deshpande 1611.04486, equation (39),
inverted with character orthogonality, followed by the ordinary modular
Verlinde formula. High-column D/d_Z integrality uses ENO math/0203060,
Proposition 3.3; the pseudo-unitary central d-number condition follows from
Ostrik 0810.3242, Theorem 1.8. The no-integral-center proof cites ENO
Proposition 8.15 and ENO 0809.3031, Theorem 1.6 and Proposition 4.5(iv).
