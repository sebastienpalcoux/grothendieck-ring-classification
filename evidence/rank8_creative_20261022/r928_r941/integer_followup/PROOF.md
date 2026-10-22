# Exact integer phase refinement

The normalized trace atoms and the670 phase variables are those of the complete
oriented R928 cone in the parent directory. Each variable counts the orbits of
the central semion whose unique positive-charge representative has that trace
atom. This count is an integer: normalized relative Galois averaging changes
the value of an orbit's phase contribution but retains its coefficient1. The
integer-count argument, including the two unrestricted types and the all-order
zero trace tail, is expanded in `README.md`.

Only these phase variables are required to be integral. The rotation auxiliaries
and the two endpoint-mixture parameters are allowed to be arbitrary nonnegative
real numbers. Consequently a contradiction in this mixed domain is a necessary
obstruction, while a solution still supplies only partial center information.

The exact negative certificates use two elementary deductions.

1. In an equation with right side zero and nonnegative variables, if all nonzero
   coefficients have the same sign, every variable in its support is zero.
   Each such deduction records the original row and its newly forced zeros.
2. For an integer variable x and integer k, either x≤k or x≥k+1. The first branch
   is encoded by x+s=k and the second by x−s=k+1, with a nonnegative real slack s.
   At each leaf an exact rational Farkas certificate proves infeasibility of the
   resulting real linear equations with nonnegative variables.

Induction up a complete binary tree therefore excludes its original integer
domain. The proof does not depend on trusting the numerical mixed-integer
solver or on a claimed exhaustive solver status. That solver was used only to
suggest which patterns to investigate. Nor is an integer-lattice consistency
test enough: the exploratory `lattice.json` shows that negative-count lattice
solutions survive, so nonnegativity is essential.

For the positive patterns, `search.json` gives explicit nonnegative integer
phase counts. After fixing them, an exact rational auxiliary witness satisfies
every original equation. These do not construct the unknown S-rows, the complete
center fusion rules, or any associator.

`verify.py` reconstructs all ten original complex cones, checks their matrix
bindings, replays each zero deduction, checks every Farkas leaf independently,
and replays every positive auxiliary certificate. For exclusions it may retain
only selected original equations; this is harmless because infeasibility of a
subsystem already excludes the full system. No independence assertion about
the selected rows is needed for soundness.

Run, from the repository root:

```sh
python3 evidence/rank8_creative_20261022/r928_r941/integer_followup/verify.py
python3 -O evidence/rank8_creative_20261022/r928_r941/integer_followup/verify.py
```

The exact exclusions are patterns44,58,196,243,245,248. Their binary trees have
13,13,11,13,31,11 nodes respectively, comprising49 exact Farkas leaves in total.
The surviving patterns40,49,186,191 each have an exact integer-phase witness.
Thus the complete ten-pattern domain is reduced to four. The refinement does
not exclude the fusion ring R928 itself.
