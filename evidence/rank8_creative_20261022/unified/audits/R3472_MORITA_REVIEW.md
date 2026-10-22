# Independent review of the R3472 conditional Morita restrictions

**Mathematical verdict: accepted with the stated conditional scope.** Neither
rank-two based module is proved to lift to a module category. Excluding some
possible dual spectra therefore does not exclude the original fusion ring.
The reviewer is a separate automated mathematical agent.

Reviewed `../../r3472/PROOF.md`, `product_equations.py`, `exact_integer.py`,
and `verify.py`.

The Galois Gram bound is valid for fusion rings, independently of
categorification. FP dimension is a real one-dimensional character, its
conjugates are distinct characters, and canonical based-ring orthogonality
gives their diagonal Gram matrix. Total reality follows because conjugates
of d_i squared are eigenvalues of the symmetric positive semidefinite
matrix N_i N_i^t. Integer-dimensional terms contribute the same number to
every matrix entry. Subtracting them and evaluating on the reciprocal
global-dimension vector proves the bound and equality statement.

The two integral commutants are full. For the first, commutation forces
the off-diagonal coefficient to be divisible by seven and the diagonal
difference to be twice that quotient. For the second it forces the
diagonal difference to be twice the off-diagonal entry. Hence no parity
coset or half-integral parametrization is missing. Nonnegative action
matrices have nonnegative radical coefficients. Their integral objects
therefore form a subcategory, and the categorical divisibility condition
legitimately restricts its dimension to 1,2,5,7. The small integral
subcategory arguments correctly force it to be pointed.

For both branches the non-FP eigenline is distinct from the common
positive eigenline. Thus the regular FP element has eigenvalue zero there.
This justifies the three square-sum equations for each dimension spectrum,
including for a possibly noncommutative dual ring. No faithfulness of the
rank-two action is needed.

The product-equation builder is a relaxation of based-ring multiplication:
the coefficient of the unit in a triple is invariant under cyclic
rotation and reversed duality, while unit and dimension equations impose
the stated integer system. It imposes no unproved commutativity. In the
three excluded profiles the two duality choices exhaust all possibilities
up to relabeling the sole repeated dimension pair.

The integer solver has no time or node cutoff. Its coefficients are
nonnegative, and every variable has a finite bound from a positive
dimension coefficient. Interval and gcd pruning are necessary conditions.
Using row bounds computed before updates only weakens later bounds within
that pass; it does not remove a feasible assignment. The recursion visits
every remaining integer in the selected interval. Thus its empty complete
searches certify the three additional spectrum exclusions without relying
on numerical MILP infeasibility.

For the second branch, the equality case at g=7 forces (s,t)=(7k,5k).
The two resulting profiles come from the complete square partitions of
seven. In the profile with only three objects of dimension 7+5sqrt(2),
the dimension of XX* forces its invertible stabilizer to be trivial, so
an order-seven group would act freely on three objects. This is a valid
contradiction. It does not eliminate the remaining generalized-near-group
profile, and the proof correctly states that no associator is supplied.

The discussion of a generalized-Haagerup C14 parent retains the distinction
between the signs of known examples and a universal theorem. No general
model-family exclusion follows from the former alone.
