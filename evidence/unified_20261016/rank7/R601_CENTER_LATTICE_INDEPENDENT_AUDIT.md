# Independent exact-code audit of the R7_3_601 center-lattice exclusion

Status: **PASS for general complex noncategorifiability**.

I read the complete final proof and the portable standard-library verifier
in `evidence/unified_20261016/rank7`, independently reviewed the categorical
premises audit, and ran the published verifier in normal and optimized
Python. Both runs passed; receipts are
`r601_center_lattice_independent.json` and
`r601_center_lattice_independent_O.json` in this directory.

The source tensor is bound to SHA-256
`afbed9441f88f4ba296235d0dd6220f41ecbcf97a7424220125e73f255ff489c`.
The verifier checks its actual census row and current ledger identity,
all associativity identities, self-duality, commutativity, all seven
orthogonal character rows, the positive dimension character, and that
every nonunit simple generates the full ring. The negative weighted
character expression is used only to exclude an ordinary representation
ring and hence the symmetric possibility. No unitary-only positivity
criterion is applied to an arbitrary pseudo-unitary category.

The main new categorical restriction is that the Drinfeld center is
simple: the source is nonpointed and simple, and neither modular nor
symmetric, hence cannot be braided. The cited simple-center theorem
then applies. Integrality and modular dimension divisibility force every
central-simple dimension to divide 360. The prime-power-dimension theorem
and simplicity remove nontrivial prime powers; simplicity separately
removes nonidentity invertibles. These facts are exactly the extra
conditions absent from the earlier unrestricted induction relaxation.

I checked the finite coverage carefully:

1. The induction Gram matrix is regenerated as sum_a N_a N_a^t.
   The complete character table determines the seven multiplicity-one
   I(1) constituents and their dimensions. The unit's forgetful column
   is exactly e0, so the six other columns have first coordinate one
   and must sum to B e0-e0. The coordinate and dimension bounds in the
   recursive enumeration therefore cover every possibility.
2. The two dimension-40 columns are merely ordered lexicographically;
   this removes duplicates without deleting any unordered block.
   Every pruning condition is necessary: coordinatewise residual
   nonnegativity, two-by-two Gram minors, and exact positive
   semidefiniteness. The integer Schur-elimination routine rescales
   only by a positive gcd, and a zero diagonal correctly requires
   the entire corresponding row to vanish.
3. The resulting 336 blocks are regenerated, not trusted from the
   certificate. Each certificate's actual low rows are compared to
   the regenerated block in order. The dimensions have row-domain
   counts 14,44,66,542,1101 and recursion counts
   1,8,78,212,398,336,336, agreeing in both independent runs.
4. Every remaining central column has first coordinate zero. Its
   last six coordinates lie in the exhaustive diagonal-bound box.
   The allowed dimension list and initial entrywise tests leave
   exactly 4700 possible outer products. Nonnegative coordinates
   ensure no sign ambiguity is lost by storing outer products.
5. For each block, rational Gauss--Jordan elimination checks positive
   pivots and constructs integer h>0 and H with RH=hI. Thus the
   filter v^t H v<=h is precisely the necessary rank-one PSD bound.
   Together with vv^t<=R, it leaves every possible residual column.
   There is no floating-point or numerical spectral comparison.
6. Every surviving outer product is tested against its supplied
   finite-field annihilator. The residual vector has value one while
   all possible summands have value zero. Repeated columns and
   arbitrary nonnegative integer multiplicities remain impossible.
   All 336 branches are covered: 218 modulo two and 118 modulo three.

The earlier exact 25-object Gram witness in this directory does not
contradict this result: its proposed center contains dimensions 5,8,9,
which are now excluded by the simple-center prime-power theorem. It was
explicitly recorded as a necessary relaxation, not a category. This
serves as a useful control on the scope of the new argument.

No mathematical or coverage gap was found. The final exclusion uses the
categorical prime-power restriction and exact integer Gram congruences;
it is not based on optimizer infeasibility or on a unitarity assumption.
