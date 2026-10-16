# Independent audit of the complete quadratic center obstruction

Auditor: rank7_structural, 2026-10-16.

Status: **PASS**, including a complete independent optimized replay.

I independently read the complete 268-line standard-library verifier,
the proof, and the four integer covectors. I also developed the separate
45-equation moment builder used during discovery and independently
checked every earlier exact separator against that builder. This audit
concerns the final source-derived verifier, whose enumeration does not
read those exploratory domains or branch assignments.

The source identification by multiplicity and ordinal, followed by the
three immutable tensor hashes, binds every calculation to the original
compressed census. The positive dimension character is checked against
all products. The induction Gram matrix is reconstructed directly from
the tensor, and its characteristic polynomial verifies the entire
formal-codegree multiset.

The separating-matrix characteristic polynomials justify the needed
Galois automorphism. Their roots are distinct. I independently checked
that the quadratic discriminants are respectively
3*10352^2 and 2*592^2; 3*11296^2 and -2*16^2; and 6*5812^2.
Each one-dimensional simultaneous eigenspace of the commuting rational
fusion matrices is defined over the corresponding eigenvalue field.
Thus an automorphism can flip the dimension field while fixing all
other character values. Rational codegrees alone would not justify
this step; the final argument does not make that inference.
Character orthogonality then makes the irrational dimension-coefficient
vector vanish on every other character, and evaluation on the two
dimension characters gives exactly the displayed rank-one transport.

The low-row recursion is exhaustive. Every nonunit constituent of I(1)
has unit coefficient one; its dimension and the sum of all six rows
are fixed. Its remaining coefficients are bounded by both the unit
Gram row and the diagonal Gram entries. The forced Galois image of
the unit is inserted at its unique dimension. Sorting only removes
permutations of equal-dimension rows. Every partial PSD and entrywise
test is necessary because the unchosen rows still form a sum of
nonnegative rank-one Gram matrices. The final transport-stability
check is an assertion on the enumerated blocks, not a hidden filter.

For the residual rows, the norm-divisibility test is exactly the
condition that 48/z be integral in Z[sqrt(r)]; the norm sign is handled
correctly by integer remainder. The global integer bounds cover every
possible row. For a singular residual R, the selected principal block
P is invertible on the range. With H=h*P^{-1}, the tests
R[:,I] H v_I=h*v and v_I^t H v_I<=h are precisely the range condition
and v^t R^+ v<=1. Thus they test R-vv^t positive semidefinite without
discarding admissible rows in a null direction. All arithmetic is
Fraction or arbitrary-precision integer arithmetic.

Full-row Galois partners are retained together, with an overall sign
only when all coordinates have that sign. Mixed-sign and absent
partners cannot occur in a genuine center. Aggregate multiplicities
agree along each paired row type even if the permutation of individual
center simples has order greater than two. Finite-field span failure
is therefore a valid obstruction to the integral paired Gram sum.

The moment columns agree with the independent builder. The first 21
entries are the paired rank-one Gram entries. The next twelve and
last twelve are the first and second twist-trace coefficients in the
basis 1,sqrt(r). Every entry and every target is multiplied by four.
The first trace target subtracts the twist-one low constituents from
zero; the second subtracts the same contribution from D*nu_2(X_i).
The center unit contributes zero to these six nonunit coordinates.

The rational-ratio test is the exact cross-product condition z/D in Q,
not a weaker dimension-pair fixedness test. Such rows are fixed under
the full transport and receive the unrestricted nine-vertex hull.
Every other row receives the six-vertex saturated hull. The shared
moment choice on paired rows is justified by conductor 12 or 24 and
the identity k^2=1 modulo that conductor. The finite hull and the
conductor/residue refinements have separate theoretical audits.

The union-find indicator computation uses only the proved odd
isotypic form constraints, assigns indicator zero to nonselfdual
simples, and enumerates both signs on every unconstrained component.
It reproduces two branches for R106, one for R2155, and two for R146.

Finally, the verifier reconstructs every allowed column and tests its
dot product with the fixed integer covector individually. It requires
a strictly negative target dot product for every indicator branch.
Neither floating-point feasibility nor a numerical tolerance occurs
in this proof. Its final count equality checks that every low block
was excluded by a finite-field span contradiction or an exact moment
inequality. No gap was found in the finite coverage or arithmetic.

The previously apparent coverage discrepancies have also been
resolved: the final R2155 certificate covers all 173 blocks (151 was
an intermediate checkpoint), and R146 has 1088 blocks for each sign
although only 1072 different right-hand sides occur. All 1088 are
reconstructed and checked, including repeated targets.

The general-complex scope follows from the separately audited
three-case Galois pseudo-unitarity reduction. The final center argument
uses the canonical pseudo-unitary spherical structure and does not
assume a unitary fusion category.

The independent `python -O` replay completed successfully for all three
cases. It reconstructed 194, 194, and 1323 low blocks; excluded 21,
21, and 235 by modular span; and checked all 346, 173, and 2176
remaining trace systems with the four covectors. Its receipt is
`quadratic_center_trace_independent_O.json`. No optimization library
was imported or called.
