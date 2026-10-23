# Independent audit of the complete dimension-48 exclusion

**Verdict: accepted.** The argument in
`work/resolve_rank9_integral/D48_EXCLUSIONS.tex` excludes `R9_1_62` and
`R9_1_87` as fusion-category Grothendieck rings over the complex numbers.
The positive cases `R9_1_12` and `R9_1_108` remain categorified.

The final quotient step is now census-independent. The complete direct
nonnegative-integer tensor enumeration in
`work/resolve_rank9_neargroup/direct_quotient.py` replaces the earlier
seven-candidate census search. The independent audit and separately written
replay are `DIRECT_QUOTIENT_AUDIT.md` and
`verify_direct_quotient_audit.py`; their complete receipt is
`direct_quotient_audit.json`. Every source has exactly four associative
quotient tensors, all isomorphic to R117. No upstream census-completeness
premise is needed for this exclusion.

The following categorical steps were checked independently.

1. Trivial universal grading and solvability force the final construction
   step to be an equivariantization, by ENO's extension/equivariantization
   characterization of solvability (Proposition 4.4). The order-four
   invertible group forces its prime group to be C2. Cyclic stabilizers
   have trivial complex Schur multiplier, so the three sign-orbit
   dimension profiles are exhaustive.
2. In the `(1^4,2^5)` quotient branch, the fixed dimension-two object m is
   self-dual and has m squared equal to the sum of all four invertibles.
   The four source products cited in the theorem were separately checked
   against the original tensors. For nonfixed quotient outputs, a unique
   source restriction bounds the coefficient by one. Rigidity and
   Frobenius reciprocity handle the fixed outputs. This establishes
   multiplicity-freeness before the census is used.
3. The direct quotient enumeration considers every duality and every
   nonnegative integer coefficient tensor with the canonical restriction
   matrix. Its positive linear equations force binary coefficients before
   enumeration; full associativity leaves only R117. This independently
   replaces the census step and also proves the needed multiplicity bound.
   The exhaustive triality-action theorem covers every neutral TY form,
   both multiplication classes, all scalar C3 associator twists, and all
   crossed-product sections. Its only fusion outcomes are R12 and R108.
4. The near-group branch includes every complex category: unitarizability
   permits Izumi's complete six-category classification, and the explicit
   tensorator normalization covers every tensor autoequivalence. The
   separate audit `NG24_ACTION_AUDIT.md` verifies this point and the
   unique square coherences. Again the only outcomes are R12 and R108.
5. In the rank-six branch, the first involution reduces to profile
   `(1^4,2^2)` in dimension twelve. A transitive action of its invertibles
   on the two noninvertibles would force equal squares with a unique
   noninvertible summand, contradicting the swapping involution. Thus
   the invertibles fix both objects and the category has the stated
   C3 grading. The rank-one module forces a trivial neutral associator.
   The C4 neutral group is excluded by its exact orthogonal group; the
   V4 case gives the six order-three matrices tested in the verifier.
6. For the S3 crossed product, a central invertible has neutral degree.
   Its neutral restriction is fixed by triality, and its twist is
   `(-1)^q`. The exact fixed spaces contain no nonzero isotropic vector.
   Therefore the only central bosons are the two grading characters.
   Morita equivalence preserves the canonical positive twist, giving a
   characteristic nontrivial boson in the rank-six category. The next
   action preserves its Tannakian subcategory. Equivariantizing it gives
   central Rep(V4) in the target; a symmetric fiber functor is obtained
   by forgetting to Rep(C2) and then to Vec. Every target sign is now
   available, including the one with the already resolved near-group
   quotient. The separate `RANK6_BOSON_AUDIT.md` records the detailed
   center and Morita argument.

The structural finite replay passed:

`python work/resolve_rank9_integral/verify_d48_exclusions.py`

It checks all four source trichotomies, all seven dimension-compatible
rank-nine candidates, every necessary involution and restriction matrix,
the C4 orthogonal obstruction, and all six V4 matrices. There are exactly
eight successful restriction maps, two per target, all to R117. Its
receipt is `work/resolve_rank9_integral/d48_exclusions_receipt.json`.
The decisive census-independent replay
`python work/resolve_integral/verify_direct_quotient_audit.py` also passed,
with eight/eight/four/four duality branches and four associative completions
per source. The near-group and triality finite verifiers passed separately.

No assumption of unitary categorifiability, multiplicity-free quotients,
strict group actions, real scalar associators, or a lift of an invariant
fermion is left implicit. The result is a general-complex exclusion.
