# Exact integer refinement of the R7_5_3895 low-center systems

This is a conditional refinement of necessary center data. It is not a
whole-ring nonexistence certificate. The source derivation, character labels,
and enumeration of active counts are owned by `../integral_gram/`.

For a fixed active count vector, subtract its columns from the right side of
the exact integer system. All remaining phase multiplicities and low
Verlinde coefficients must be nonnegative integers.

**Lattice test.** A recorded echelon integer lattice contains every remaining
column. Exact replay checks this containment column by column. The residual
right side must therefore lie in that lattice. Discovery computes a Hermite
basis, but correctness does not require trusting that computation or even
proving equality with the generated lattice: containing every column is
sufficient. Rational echelon coordinates give explicit congruence and
linear-equality tests. This reduces each of the two recorded low frames to
32 active branches per retained label case.

**Residual Gram test.** A positive integer value of a variable consumes at
least one copy of its entire Gram column, including any required parity
factor. The remaining Gram matrix must have nonnegative entries and be
positive semidefinite. A column can therefore be removed if subtraction
violates an entry bound or has an explicitly recorded integer vector `u`
with `u^T Q u < 0`. Replay checks that displayed inequality directly. It does
not trust the discovery algorithm that found the vector.

**Integer splits.** At a tree node, an integer variable `x_j` is split into
`x_j <= k` and `x_j >= k+1`. These alternatives cover its entire current
integer domain. Upper and lower bounds are represented as
`x_j+s=k` and `x_j-s=k`, respectively, with `s>=0`. Every terminal node has
an integer ray whose dot product with the right side is negative and whose
dot product with every variable column is nonnegative. This is a direct
contradiction for nonnegative solutions. The independent replay evaluates
these column inequalities without constructing the discovery matrix and
without importing an optimizer.

For low frame 6, active branches 0, 14, 122, and 125 and label cases 0, 2, 4,
and 6 have sixteen complete trees with **775 exact leaves**. Both normal and
optimized Python pass independent replay; sixteen corrupted leaf rays are
rejected. The earlier active enumeration, lattice and linear-separation
certificates cover the other active branches. Their source/completeness
checks must accompany these trees to conclude that the entire frame is
impossible. Low frame 8 has exact feasible necessary data, so this refinement
does not exclude R7_5_3895 itself.

From the repository root:

```sh
python evidence/rank7_m5_20261020/computation/check_inactive_branches.py
python -O evidence/rank7_m5_20261020/computation/check_inactive_branches.py
python evidence/rank7_m5_20261020/computation/verify_branch_lattice.py
python -O evidence/rank7_m5_20261020/computation/verify_branch_lattice.py
python evidence/rank7_m5_20261020/computation/verify_integer_trees.py --frame 6
python -O evidence/rank7_m5_20261020/computation/verify_integer_trees.py --frame 6
```

Receipts bind the exact source systems, active branches, lattice records,
pruning inventories, and tree files. Incomplete low-frame-8 tree attempts
remain research logs and supply no additional exclusion.
