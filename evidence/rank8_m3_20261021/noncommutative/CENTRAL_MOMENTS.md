# A unified central twist moment relaxation

This necessary condition has pseudo-unitary scope. It unifies central induction
multiplicities and the first two indicator identities through a positive
Toeplitz moment matrix. A completed search with no obstruction gives no model
and no conclusion about general categorifiability.

In a pseudo-unitary category let D be the global dimension and X_i a nonunit
simple object of FP dimension d_i. The twist spectrum on I(X_i), with central
simple dimensions multiplied by their restriction multiplicities as weights,
is a positive measure on the unit circle. Its first three moments are
T=D d_i, zero, and D nu_2(X_i). Here the second indicator is0 for a nonselfdual
simple and lies in {+1,-1} for a selfdual simple. These are the central-induction
indicator identities of Ng–Schauenburg.

The distinguished constituents A_E of I(1) all have trivial twist. Their
dimensions are D/f_E, their multiplicities in I(1) are dim(E), and their
restriction columns start with dim(E). On I(X_i) they supply mass
L_i=sum_E c_E(i) D/f_E. The remaining positive measure therefore has moments

    m0=T-L_i, m1=-L_i, m2=nu_2(X_i) D-L_i.

Its 3 by3 Toeplitz matrix, indexed by1,z,z^2, must be positive semidefinite.
For nu=nu_2(X_i), its distinct principal minors are

    T-L,
    T^2-2TL,
    T^2-(nu D)^2-2L(T-nu D),
    (T-nu D) * (T(T+nu D)-L(3T+nu D)).

These formulas follow by direct determinant expansion. All comparisons are
made in the exact positive embedding of the FP field.

The code enumerates every possible restriction column for each E separately,
using the full induction Gram matrix. The positive dimension equation bounds
every tail coordinate by floor((D/f_E-dim(E))/d_i); this floor is computed
by exact embedding comparisons before the complete inherited enumeration.
In rational dimension fields, exact bounded-knapsack dynamic programming
counts every column and computes its coordinatewise minima without storing
the Cartesian enumeration. Each state records the partial dimension sum,
number of realizations, and minima; combining states adds counts and takes
coordinatewise minima. This is a finite exact recurrence for the same set.
Since D/f_E is positive, the sum of
coordinatewise minimum column contributions gives a lower bound ell_i<=L_i.
The Toeplitz matrix at ell_i is the actual matrix plus
(L_i-ell_i) times the all-ones matrix, which is positive semidefinite. Thus
failure at ell_i rules out the actual spectrum, regardless of whether the
independently minimal columns can occur simultaneously. Passing this relaxed
test does not assert that such simultaneous columns exist.

For each simple the code retains both possible selfdual indicators. It reports
a pseudo-unitary obstruction only if all choices fail for at least one simple,
or a required central constituent has no restriction column. It does not infer
a general exclusion. It records exact field coordinates of every minor and
its sign, source tensor hashes, and the complete column-set cardinalities.
All fourteen known models are positive controls. The replay is read-only by
default, and uses explicit checks that remain active under Python -O.

For the additional integral frontier controls R8_3_731 and R8_3_3344,
the separately verified integer FP dimensions660 and360 imply that any
complex categorification is pseudo-unitary (Etingof–Nikshych–Ostrik,
*On fusion categories*, Proposition8.24). Thus this scoped test also gives a
necessary condition for their general complex categorification. Both pass
the relaxation; neither general existence nor feasibility of stronger
induction/rotation constraints follows.
