# Independent review: R8_3_439 is excluded over the complex numbers

Outcome: **PASS**, with the full scope chain below. This is an independent AI
mathematical/computational review, not a human or proof-assistant certification.

## Categorical scope

The unrestricted signed-sector gate for R439 gives a pseudo-unitary Galois
conjugate of any hypothetical complex categorification. The previously reviewed
complete central/rotation test forces its three transposition indicators to be
+1. Its C3 subgroup fixes a noninvertible simple, killing the restricted
associator on C3. The transposition indicators kill restriction to C2.
Restriction/corestriction gives both 2[omega]=0 and 3[omega]=0, so the full
pointed S3 associator is trivial. Hence the full S3 subgroup algebra exists.

The separately verified full-S3 module calculation gives five possible based
rank-five Morita dual rings. Four have frozen general-complex exclusions; the
remaining tensor is R5_3_40, with dimensions 1,1,2,d,d and d=3+2 sqrt(3).
This is a statement about the based ring, without identifying its associator
with that of a known model. Morita invariance of global dimension (ENO,
*On fusion categories*, Theorem 2.15) and FP dimension (Corollary 8.14)
makes this dual pseudo-unitary. Proposition 8.23 gives its canonical positive
spherical structure.

The source R439 has only the unit among ring-central invertibles and has
C_ad=C. Thus its center has no nontrivial invertibles. Center equivalence
preserves that conclusion for the rank-five dual. The newly proved
`INTEGRAL_CENTER_SUBCATEGORY.md` applies: every nonunit integral-dimensional
central simple is forbidden. This does not assert the same center property
for arbitrary categorifications of the R5_3_40 based ring.

## Completeness of the independent finite calculation

`verify_r439_verlinde.py` imports none of the producer's field, low-column,
Gram-enumeration or Verlinde code. It reads the pinned full rank-five tensor
from the based-isomorphism receipt and computes with rational pairs in
Q(sqrt(3)). The 125 tensor coefficients have the frozen source SHA
84487a759f44be4a988082680fa8c3b28bcd0d159d639f38409825e19c5761e6.

It reconstructs the induction Gram matrix by summing the squares of the five
left regular matrices. It explicitly checks all five character homomorphisms
and their full orthogonality. The codegrees are D,D',3,4,4, with
D=48+24 sqrt(3) and D'=48-24 sqrt(3).

Since the ring is commutative, all five constituents of I(1) occur once.
Independent full integer boxes give low-column counts 3,5,8,8. The unit-row
identity leaves 24 frames after quotienting only the exchange of the two
equal-codegree columns. Exact principal-minor PSD tests leave five frames.
Complete equal-codegree labeling and S symmetry leave one frame and two
labelings. No twist or indicator assumption enters this enumeration.

The remaining four-coordinate Gram matrix is

    [4 2  4  4]
    [2 6  7  7]
    [4 7 34 31]
    [4 7 31 34].

Independent exhaustive coordinate boxes and all principal-minor PSD tests
give 85 possible nonzero high columns. The necessary D/d_Z integrality and
d-number tests leave 38. ENO Proposition 3.3 supplies the first test for the
modular center of global dimension D^2. Ostrik, *On formal codegrees of fusion
categories*, Theorem 1.8 supplies the second: in this pseudo-unitary center
the squared norm is d_Z^2, and the d-number property passes from a square to
its algebraic-integer square root. In Q(sqrt(3)) the used necessary test is
Tr(d_Z)^2/Norm(d_Z) integral.

The no-integral-center theorem removes indices 9,17,19,27. The eigenvalue
S_(A_E,Z)/d_Z of an integer fusion matrix is an algebraic integer; this removes
index 37. The remaining 33 columns are the complete necessary domain.

A third independent memoized generating-series coefficient extraction
enumerates all nonnegative integer multiplicities satisfying the ten Gram
entries. Every multiplicity has a finite diagonal bound, and a residual entry
is pruned only if negative or if no remaining column can contribute to it.
This recovers exactly the same 58 full multiplicity vectors as the producer's
two separately structured exhaustive algorithms.

## The single cubic contradiction

Let A be the distinguished simple for the conjugate-FP character chi and
formal codegree f=D'. It is self-dual: duality preserves I(1), and its dimension
D/f is unique among those five constituents. The distinguished row identity
(Deshpande, *On centers of bimodule categories and induction-restriction
functors*, equation (39), inverted using character orthogonality) is

    S_(A,Z)=(D/f) chi(FZ).

The unnormalized center S-matrix has global dimension D^2 and S_(1,Z)=d_Z.
Thus the ordinary Verlinde formula gives

    N_(A,A)^A = (1/D^2) sum_Z S_(A,Z)^3/d_Z
              = (D/f^3) sum_Z chi(FZ)^3/d_Z.

The sum includes the five distinguished objects once and every high column
with its integer multiplicity. The independent checker evaluates both
normalizations and checks the full S-row norm is D^2 on each of the 58 patterns.
The coefficient histogram in the basis 1,sqrt(3) is:

| Coefficient | Number of complete patterns |
|---|---:|
| 7/6-sqrt(3)/6 | 16 |
| 1/3 | 16 |
| 19/12-5 sqrt(3)/12 | 16 |
| 2-sqrt(3)/3 | 6 |
| 1/3+2 sqrt(3)/3 | 4 |

All values are nonintegral. Therefore the specified rank-five dual cannot
exist, and neither can a complex categorification of R8_3_439.

## Controls and fresh replays

The producer checks the actual Fibonacci center. The independent checker
instead uses all eight simples of Z(Rep(S3)), expressed through conjugacy-class
centralizer induction. It checks all 27 distinguished triple Verlinde
coefficients are nonnegative integers, including every unit fusion identity
and a nontrivial cubic coefficient equal to 1. This tests the normalization
on a different known center, with nontrivial integral central simples allowed.

Fresh read-only runs passed:

    python evidence/rank8_frontier_20261021/rank5_integer_gram/verify.py
    python -O evidence/rank8_frontier_20261021/r439_centerless_rank5/verlinde_exclusion.py
    python evidence/rank8_frontier_20261021/review/verify_r439_verlinde.py
    python -O evidence/rank8_frontier_20261021/review/verify_r439_verlinde.py

The source-bound independent receipt is `r439_verlinde_direct.json`.

Primary sources rechecked for this review: ENO math/0203060 Theorem 2.15,
Proposition 3.3, Corollary 8.14 and Proposition 8.23; Ostrik 0810.3242
Theorem 1.8; Deshpande 1611.04486 equation (39). Earlier independent scope
reviews remain necessary inputs to the general-complex conclusion.
