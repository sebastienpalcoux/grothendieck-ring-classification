# Seven general exclusions from three-fixed module Gram matrices

The excluded rings are `R7_2_11`, `R7_2_205`, `R7_2_275`, `R7_2_287`,
`R7_3_387`, `R7_4_2473`, and `R7_3_1055`. The argument applies to arbitrary
complex fusion categories. It uses neither pivotality nor unitarity.

## Categorical construction

Let an invertible involution g fix a simple object. Its pointed
subcategory has trivial associator: that fixed simple is a rank-one
module category over Vec(C2,omega), and the module pentagon trivializes
omega. Therefore A=1+g is a connected separable algebra. Put M=C_A and
D=_A C_A, the right-module category and the Morita dual fusion category.

Each simple fixed by g has two right A-module structures, exchanged by
the nontrivial character of C2. Each free orbit gives one right module.
Twisting the A-action commutes with the C-action. If there are three
fixed simples x_a, the three differences of their two module structures
span an invariant space with integer matrices T_i satisfying

    |T_i[a,b]| <= N_i[x_a,x_b],
    T_i[a,b] = N_i[x_a,x_b] mod 2,
    T_(i*) = transpose(T_i),
    T_i T_j = sum_k N_ij^k T_k.

These necessary equations are exhaustive over the finite entry domains.
The source rings are commutative, so all T_i are normal. The public
verifier reconstructs every representation up to changing signs of the
three difference basis vectors. It then reconstructs the full module
matrices M_i. There are respectively 1,1,1,1,4,7,1 gauge orbits for the
seven rings listed above.

For the forgetful functor D -> M, induction followed by restriction has
matrix I+M_g. Thus the restriction columns of the simple objects of D
have Gram matrix I+M_g. Since M_g is an involutive permutation matrix,
its nonnegative integral Gram decomposition is unique: at a fixed point
there are two singleton columns; at a transposition there is one column
supported on its two entries. This determines all dual FP dimensions.
Normalize module dimensions by dividing underlying C-dimensions by two.

For a right-module simple m, evaluation D -> M, Z -> m tensor_A Z,
has Gram matrix

    G_m = sum_i M_i[m,m] M_i.

Indeed its induction/restriction endofunctor is left multiplication by
the internal end m tensor_A m*, whose simple multiplicities are
M_i[m,m]. The dual unit contributes the column e_m. Every other column
v is a nonzero nonnegative integer vector with weighted dimension
dim_D(Z) dim_M(m). Consequently Q_m=G_m-e_m e_m^t must be the sum of the
rank-one matrices vv^t over exactly the remaining dual simples.
These identities are independent of the number of fixed objects.

## Four sqrt2 cases

For each of `R7_2_11`, `R7_2_205`, `R7_2_275`, and `R7_2_287`, the
anti-module equations have one sign-gauge orbit. Their small domains
also admit a direct spectral reduction: a noninvertible generator has
squared Frobenius norm at most20, whereas its conjugate eigenvalue pair
2+/-2sqrt2 contributes24. The remaining pair +/-sqrt2, or +/-i sqrt2,
forces all even entries to vanish and all four unit couplings to have
absolute value one. The remaining fusion relations determine the
matrices up to sign gauge.

Write delta=1+sqrt2. The module dimensions are 1^4,delta^4 and the dual
dimensions are 1^8,delta^8. For a recorded delta-dimensional module m,
the restriction of its full internal-end Gram matrix to the four
delta coordinates has diagonal4 and every off-diagonal entry2.

For a symmetric matrix Q on these four coordinates define

    S(Q)=trace(Q)-2 sum_(a<b) Q[a,b].

A column from a dual invertible has delta-coordinate sum1, so its
contribution to S is1. A delta-dimensional dual simple has column
dimension delta^2=1+2delta. Its delta-coordinate sum is2, and its
contribution to S is either0 or4. All contributions are nonnegative.
But the displayed source Gram matrix has S=16-24=-8. This excludes all
four rings.

## The integral case R7_3_387

All four anti-module branches have module dimensions
(1,9,1,1,3,3,3,3), dual dimensions1^6,6^2,9^2, and the same relevant
Gram entries at the recorded dimension-three module. Rows0,2,3 of the
full Gram matrix are identical with diagonal1. Hence exactly one column
has their three coordinates nonzero, and that column is

    v=(1,1,1,1,1,1,0,0),

of dimension18. It corresponds to one of the two dimension-six dual
simples. Subtract vv^t. Every remaining column vanishes in positions
0,2,3. The six invertible columns have dimension3 and exactly one unit
entry among the final four positions, so their position1 is zero.
The three remaining noninvertible columns have squared position1 entries
summing to12, with each entry at most3. The only possibility is(2,2,2).

The remaining dimension-six column therefore has all final four entries
zero. Each of the two dimension-nine columns w,z has final-four entry
sum3. The cross terms with position1 give w+z=(1,1,2,2) on these four
positions. The off-diagonal entry between positions4 and5 is1, forcing
w4=w5 in{0,1}. The off-diagonal entries(4,6) and(4,7) are both1,
forcing w6=w7=1. Thus the sum of those entries of w is2w4+2, either2 or4,
contradicting the required sum3. All four branches are excluded.

## Exact certificates for R7_4_2473 and R7_3_1055

The anti-module domains have respectively seven and one gauge orbits.
For each orbit, a recorded module simple supplies an impossible Gram
system. For every allowed dual dimension, the verifier enumerates all
nonnegative integer columns v with

    v[a]^2 <= Q_m[a,a],
    v[a]v[b] <= Q_m[a,b],
    sum_a v[a] dim_M(a) = dim_D(Z) dim_M(m).

This is a finite superset of every possible restriction column. The
linear system Ax=b records the upper-triangular entries of Q_m and the
number of columns of each dual dimension. Every frozen integer vector y
is checked directly to satisfy y^T A >=0 and y^T b <0. Therefore even a
nonnegative real solution is impossible, and no categorification exists.
These two conclusions have general complex scope, just like the five
short arguments above.

## Reproduction and independent audit

Run `python verify_three_fixed_gram.py --repo REPOSITORY_ROOT` in this
directory, or invoke it by absolute path. It reopens the full rank-seven
census, checks tensor digests and the based-ring axioms, rebuilds every
anti-module orbit, and regenerates all finite Gram column domains.
It verifies all seven cases, including independent finite certificates
for the five cases having short proofs. The replay uses exact arithmetic
and never invokes an optimizer. All support files are vendored under
`gram_support/` and bound by its SHA-256 manifest. Optimized Python is
supported because validity checks do not use assertions.

An independent generating-word algorithm, distinct from the propagating
enumerator in this verifier, reproduced every orbit and all16 branch
inequalities and matched each tensor to both the census and ledger.
The categorical identities were independently reviewed by two other
agents. Passing any other case through a relaxation has not been treated
as an existence result.
