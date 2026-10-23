# Independent audit of the direct dimension-24 quotient completion

**Accepted.** The direct enumeration proves that a central \(C_2\)
de-equivariantization of any of R9_1_12, R9_1_62, R9_1_87, R9_1_108 with
profile \(1^4,2^5\) has based ring R9_1_117. No completeness claim about a
fusion-ring catalogue is used, and multiplicity-freeness of the quotient
is proved by the positive equations before the binary search.

The audited files, in work/resolve_rank9_neargroup, have SHA-256 hashes:

| File | SHA-256 |
|---|---|
| direct_quotient.py | 34d13c2a90456c40f09810a6a428ed2073f7ef122040e45b51f1198994dad6f7 |
| direct_quotient.json | 65ab3e152a8a50eebe23a83dc94b5aae98490078fbe54326310f9165ac1955ac |
| DIRECT_QUOTIENT.tex | a7acf34f82aa7bafa14d3495b9a0dcc08b4524cb7c4622b324fb45a38fa8bfa2 |

These exact versions were independently read and replayed successfully.
The proof audit covers the following completeness points.

1. **Canonical restriction covers every quotient.** The standard
   \(C_2\)-equivariantization classification has two stabilizer characters
   for a fixed quotient simple, and one induced simple for a free orbit.
   Thus the source sign orbits determine the canonical restriction matrix
   after a harmless relabeling of quotient simples. The labels
   \((1,a,b,c,m,x,x',y,y')\) and involution
   \((b\ c)(x\ x')(y\ y')\) leave no additional orbit type unexamined.
   The unique source sign of the required profile has original ID
   \(2,7,3,6\), respectively. Source dimension vectors are checked exactly
   against every source product.

2. **Duality is not guessed.** The code enumerates every
   dimension-preserving involutive permutation fixing the unit,
   commuting with the action, and intertwining source duality through
   the restriction matrix. This yields eight branches for 12 and 62
   and four for 87 and 108. Every actual duality satisfies these
   necessary conditions.

3. **Variable identifications are necessary identities.** The
   disjoint-set unions use exactly Frobenius reciprocity
   \(N_{ij}^k=N_{i^*k}^{j}=N_{kj^*}^{i}\) and simultaneous action of the
   quotient involution. Unit, duality, dimension, and every coefficient
   of the tensor-functor identity are imposed. No target tensor enters
   these constraints.

4. **The binary bound is proved.** After collecting repeated variables,
   each equation has positive integer coefficients and nonnegative
   right-hand side. In any nonnegative integer solution, a variable of
   coefficient \(w\) in a row of right-hand side \(r\) is bounded by
   \(\lfloor r/w\rfloor\). The final addition to the verifier explicitly
   records a row witness giving an upper bound at most one for every
   variable in every duality branch. I inspected this change and
   replayed the resulting version. Thus the search covers all
   nonnegative integer tensors, not an assumed multiplicity-one subset.

5. **Propagation and branching are exhaustive.** The bit-set recurrence
   computes every subset sum of the remaining positive weights.
   A variable value is removed only if the corresponding residual sum
   is impossible. Assignments made during a propagation pass remain
   sound because the tested value was forced even before those
   additional restrictions. If any variables remain, both values
   are visited. Full assignments are checked against all
   \(9^4=6561\) associativity equations.

6. **Identification is subsequent to enumeration.** The R9_1_117 input
   is used only after an associative tensor has been found.
   The final unit-preserving, dimension-preserving based permutation
   is checked against all 729 coefficients. No list of candidate
   quotient rings is consulted.

The independently replayed counts are:

| Source | Duality branches | Search nodes | Linear solutions | Associative solutions |
|---|---:|---:|---:|---:|
| R9_1_12 | 8 | 74 | 36 | 4 |
| R9_1_62 | 8 | 74 | 36 | 4 |
| R9_1_87 | 4 | 8 | 4 | 4 |
| R9_1_108 | 4 | 8 | 4 | 4 |

Every associative solution is based-isomorphic to R9_1_117.
The receipt retains every solution, based map, duality branch, bound
witness, and original source tensor hash. This closes the global
quotient-identification gap.

An additional structural argument forcing the same quotient to be a
\(C_3\) extension of a TY category of dimension eight was independently
derived and checked by the signed-audit agent. It is preserved separately
as an optional appendix; the accepted finite completion above is sufficient
for the main proof and does not depend on that additional argument.
