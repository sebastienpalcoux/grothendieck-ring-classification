# Rank-four finite certification audit

**AI-generated research · independent verification pending.** This is a source and exact-arithmetic audit, not a Lean formalization or independent human verification of the categorical arguments.

## Scope and conclusion

I reviewed the finite necessary conditions (Section 13), the exhaustive certification argument (Section 14), the ordinary census appendix, and the implementations that link the census to the certificate bank. No gap was found in the finite enumeration coverage, basis transport, arithmetic rejection logic, or model identification within that scope. The unrestricted classification additionally depends on the earlier theoretical dimension bound and categorical necessity lemmas. Those dependencies are audited separately and are not proved by these finite checks.

The attachment's release-integrity checker passed before any regeneration. The attachment was left unchanged. The complete replay was executed in an isolated work copy and in the adapted standalone computational package. The latter has independently checked source/data hashes and byte-identical generated tables in the adapted paper.

The exact finite results are:

| Scope | Inputs | Exclusions | Models |
|---|---:|---:|---:|
| Ordinary rings with FPdim < 1000, multiplicity ≤31 | 1,692 | 1,677 | 15 |
| Positive orbits in the arithmetic-filtered signed cover, multiplicity ≤31 | 1,182 | 1,173 | 9 self-dual |

The ordinary census consists of 1,642 self-dual rings and 50 rings with one dual pair. The complete signed search has 92,795 orbits: 90,510 fail the d-number criterion, 68 more fail the cyclotomicity criterion, and 2,217 remain. The ordinary and signed counts describe different sets and must not be combined as one census.

## Coverage argument

1. **Complete presentations.** Rank four permits identity duality or one transposition on the three nonunit basis elements. Reciprocity gives ten parameters in the self-dual case and six in the dual-pair case. An independent symbolic construction recovered exactly the six and four stated nonzero commutator equations, including signs. Commuting multiplication matrices with the prescribed unit row give associativity: the zero row of the regular multiplication defect propagates to every row by commutation.

2. **Self-dual elimination.** The six mixed coefficients form one permutation orbit, so placing a minimum at `b` loses no based-ring isomorphism class. For `b>0`, the first, second, and fourth equations determine `h,g,j`; the third is the displayed exact two-variable linear Diophantine equation. I independently checked that its numerator is precisely `C*a+A*i+B0`. The implementation retains all gcd progressions and all zero-coefficient branches. Its interval pruning is necessary, not heuristic, and every output is retested against all six equations.

3. **Zero branches.** The cases `b=0<c`, `b=c=0<e`, and `b=c=e=0` cover all remaining possibilities. Every division has an explicit nonzero-denominator hypothesis. The ordinary `e=0,b=0<c` branch forces positive `d,h`; the signed version also retains negative `h`, the exceptional `d=0` branch, and the `f=-1` terminal branch. These signed branches are important and are present in both text and code.

4. **Dual-pair branch.** The final equation fixes a nonnegative square root `f`, which is tested exactly. The subsequent equations determine `b` and `a` only when their denominators are nonzero; all bounded free variables are retained otherwise. Exchanging the dual pair leaves the parameter tuple unchanged.

5. **Isomorphism and signs.** The ordinary generator compares every relevant nonunit permutation. The signed generator compares all 48 signed permutations within its preferred representative set. The preferred sign conditions are achievable because `b,c,d` have independently adjustable signs; when `b=c=0`, a remaining gauge fixes the sign of `e`. A signed orbit contains at most one nonnegative permutation orbit: a sign change preserving nonnegativity fixes every nonzero coefficient.

6. **Exact dimension acceptance.** The Casimir matrix is real symmetric and nonnegative, and its strictly positive FP vector has eigenvalue `D`; hence `D` is its largest eigenvalue. The strict condition `D<1000` is equivalent to positive definiteness of `1000*I-B`. Integer leading principal minors implement Sylvester's criterion without numerical rounding. C++ uses 128-bit fraction-free determinant arithmetic within the explicitly bounded range; Python recomputes with arbitrary-precision integers. Removing both dimension-pruning steps gives 16,065 classes; independent direct determinant expansion retains exactly the same 1,692 tuples. The literal multiplicity-two box tests all 59,778 assignments and gives the same 27 classes.

## Certificate logic

The full ledger compares each input's identity, canonical digest, tag, multiplicity, stage, and status against a deterministic pipeline. Every later self-dual witness carries a checked explicit based-ring isomorphism. A status flag, source index, or digest is not used as the mathematical exclusion itself.

The ordinary table of any categorifiable ring passes the common arithmetic conditions, so its signed orbit lies in the retained signed cover. Separately, every compatible sphericalization quotient is recovered by expanding all signed permutations and testing coefficient bounds, parity, adjoint parity, and determinant divisibility. The verifier regenerates the global cover, compares the exact retained set, and replays all required signed tables and character factors.

The arithmetic statements reviewed are correctly one-way necessary conditions. Normalized norm valuations follow by taking norms in a compositum. The split-prime field test uses an unramified prime and tests the necessary splitting implication; the cyclotomic rejection uses unequal Frobenius cycle lengths in a transitive abelian action. Failure to find one of these witnesses is not treated as acceptance of a field assertion.

The low-induction search retains codegree multiplicities, the central-unit column, all bounded integral restriction columns, and all admissible combinations. It checks residual Gram nonnegativity and the indicated moment inequalities. No uniqueness is assumed. Positivity-dependent inequalities are used only after a stated pseudo-unitary reduction. General signed branches use the squared-dimension positive measure, retaining ordinary/signed codegree provenance and the same indicator assignment at every real embedding.

The two-moment polynomial identity, the diagonal involution inequalities, the non-self-dual quadratic-family contradiction, and the root-length conductor-40 boundary have the asserted signs and numerical constants. For the quadratic family, Gram saturation forces exactly two exceptional columns; their twist ratio is an integral rational number in the stated interval, and the modulo-nine argument excludes the endpoint. The equality statement in the conductor-40 root bound distinguishes the two copies of `-1` and gives the contradiction after squaring. These arguments use the earlier categorical induction/indicator inputs.

The rank-two subring obstruction is justified by the cited unrestricted rank-two classification. The adapted manuscript states that dependency directly.

## Models and reproducibility

All fifteen model names and canonical multiplication tensors exactly equal the fifteen model tensors in the current repository. Independent constructions from group, product, adjoint, near-group, and exceptional fusion rules passed. Exact positive dimension characters, 240 character product identities, global dimensions, and table polynomials were checked. These identify fusion rules; the cited existence papers remain the source for categorical realizations.

The package uses explicit checks throughout the main verifier and its regression/table-generation scripts, so optimization does not remove verification gates. Polynomial comparisons normalize coefficient containers before comparison, supporting both SymPy and FLINT. Delivered receipts record normal and optimized full deep replays, exact source/data hashes, and manuscript table equality.

The canonical target is `supplements/rank4/unrestricted/`. It runs independently with `python supplementary/check.py --deep`; `--manuscript-root` additionally checks the generated tables in an accompanying paper. `verify_package.py` checks immutable source, deterministic data, generated tables, and delivered receipts. Timing reports are allowed to change during a fresh replay and remain linked to the exact census and ledger hashes.
