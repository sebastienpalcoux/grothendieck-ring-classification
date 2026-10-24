# Independent audit: R9_2_1965 general exclusion

**Verdict: PASS.** The argument in
`phase5/integral168/GENERAL_EXCLUSION.md` establishes that R9_2_1965 has
no complex fusion categorification, using the already independently
audited phase-four group-theoretical exclusion. No mathematical gap was
found. The new proof applies to arbitrary complex fusion categories,
including nonunitary categories; it does not assume that the original
category is braided.

The author's files were not modified. The original verifier was replayed
from a copy with only two path changes: inputs still come from the author's
directory, while the replay certificate is written here. Its replay passed.
A separate verifier, `independent_replay.py`, uses only the Python standard
library, reconstructs the quotient tensor from the displayed rules, and
reads the rank-nine tensor directly from the original compressed census.

## Categorical audit

1. **Positive spherical structure and central characters.** The source is
   integral, so EGNO Proposition 9.6.5 and Corollary 9.6.6 supply its
   canonical positive spherical structure. Ostrik Theorem 2.13 was checked
   directly: the distinguished object has dimension `dim(C)/f_E` and
   multiplicity `dim E`; there is no missing factor of `dim E` in its
   dimension formula. These statements apply to noncommutative fusion
   rings. For a scalar character, the pullback through the forgetful
   homomorphism is exactly the S-matrix character of Ostrik Example 2.9.
   Consequently equation (1) is valid in the required scope.

2. **Forced dimension-three restrictions.** The two displayed scalar
   characters have formal codegree 56. Their distinguished objects are
   distinct, have dimension three, and contain the tensor unit exactly
   once after forgetting. The only possibilities are `1+2g` and `1+u`.
   The correctly ordered noncommutative induction formula gives
   `B[0,5]=1`, excluding `1+2g`. Thus both restrictions are `1+u`.

3. **Centralization without unitarity.** The S entries equal nine.
   Balancing expresses them as sums of roots of unity weighted by
   positive dimensions, with total weight nine. Equality forces every
   constituent twist to be one, so the double braiding itself is the
   identity. This is stronger than a numerical trace observation: the
   balancing identity identifies monodromy with the scalar twist on each
   simple summand, including multiplicity spaces. Pairwise centralization
   is preserved under tensor products, summands, and duals; therefore the
   generated subcategory is symmetric. Its twist is identically one.
   Deligne's classification with the canonical positive spherical
   structure makes it Tannakian. A super-Tannakian loophole is absent.

4. **Central Rep(C2) and the quotient.** Trivial universal grading makes
   the forgetful map on central invertibles injective. Any nontrivial
   invertible in the Tannakian subcategory would generate Rep(C2) and
   forget to g. Its restriction to the original category is fully
   faithful, so EGNO Theorem 8.23.3 applies. Free-module adjunction gives
   `Hom(Q(X),Q(Y)) = Hom(X,Y tensor (1+g))`, up to the harmless left/right
   convention since g is central. Different g-orbits therefore give
   disjoint simple images. The fixed dimension-two object has a
   two-dimensional semisimple endomorphism algebra and splits into two
   distinct simples. Their dimensions add to two, so each is invertible.
   Neither is the unit, by the same adjunction. This proves the complete
   six-simple list, not merely a list of candidate objects. The three
   invertibles form C3, which acts trivially on the singleton of
   dimension-three objects and the pair of dimension-six objects under
   both left and right tensor multiplication. The quotient rules follow.

5. **Dimension-84 contradiction.** The quotient is commutative, so its
   six formal-codegree constituents in I(1) are all multiplicity one.
   The dimension-one constituent is the central unit because the tensor
   unit occurs in I(1). The coordinate budgets, the modulo-three step,
   and both positive-semidefinite obstructions are correct. The completed
   square is exactly
   `-(11*t-40)^2/22-36/11`, strictly negative for every real t.
   Thus the contradiction does not depend on a search bound or on the
   prior lower-rank exclusion of R6_4_38.

6. **Perfect Tannaka group and order.** Since central Rep(C2) is
   impossible and central invertibles inject into `{1,g}`, the Tannaka
   group has trivial abelianization. It is nontrivial because the
   subcategory contains a three-dimensional simple. De-equivariantizing
   its centralizer gives rational algebraic-integer dimension
   `168^2/|G|^2`. This implies `|G|` divides 168. Every proper-divisor
   order is solvable: the two three-prime possibilities, 42 and 84, have
   normal Sylow-seven subgroups and solvable quotients; all other
   possibilities have at most two prime factors. Hence the perfect
   group has order 168. The Tannakian subcategory is Lagrangian, and
   EGNO Corollary 9.13.6 makes the hypothetical original category
   group-theoretical. This contradicts the phase-four theorem within
   exactly its audited scope.

## Independent finite replay

`independent_replay_receipt.json` records the following checks:

- Exact original compressed-census identification and canonical tensor hash.
- All fusion axioms and 6,561 source associativity equations.
- Exact adjoint closure and complete central-involution orbit structure.
- Both scalar characters over Q(sqrt(-7)): all 162 multiplicativity
  equations and formal codegree 56.
- Quotient tensor reconstructed from the displayed rules, all its fusion
  axioms and 1,296 associativity equations, and all 486 quotient-map
  coefficient equations.
- Quotient induction Gram matrix recomputed both by ordered induction and
  Casimir multiplication, with matching results.
- Formal-codegree multiplicities established by exact rational eigenspace
  ranks, independently of the author's SymPy characteristic polynomial.
- All **595** nonnegative distinguished restriction-vector assignments
  with the required dimensions and total restriction. Of these, **510**
  have residual quadratic form **-2** on the a-minus-a-squared vector;
  the remaining **85** have negative two-by-two minors between **-130**
  and **-10**.
- All proper divisors of 168 and the unique possible Sylow-seven counts
  for 42 and 84.
- The accepted phase-four GT exclusion, its independent PASS verdict,
  and all source hashes recorded by that independent audit.

The author's optional R6_4_38 identification also passes the copied
verifier. The independent mathematical contradiction does not use that
identification.

Replay commands:

```
python phase5/audit_integral168/author_verifier_replay.py
python -S phase5/audit_integral168/independent_replay.py
```

The first retains the author's SymPy dependency; the second needs only
standard Python. Neither writes to the original author's directory.

## Sources checked directly

- Ostrik, *Pivotal fusion categories of rank 3*, arXiv:1309.4822,
  Proposition 2.4, Theorem 2.5, Example 2.9, and Theorem 2.13:
  https://arxiv.org/pdf/1309.4822
- Etingof--Gelaki--Nikshych--Ostrik, *Tensor Categories*, Proposition
  9.6.5, Corollary 9.6.6, Theorem 8.23.3, symmetric-category
  classification in Section 9.9, and Corollary 9.13.6:
  https://math.mit.edu/~etingof/egnobookfinal.pdf
- The Deshpande paper cited by the author was opened as a consistency
  check; the central scalar-character identity already follows directly
  from the quoted Ostrik construction:
  https://arxiv.org/pdf/1611.04486

The audit does not claim to replace the established external categorical
theorems with computation. It verifies their exact hypotheses and the
intermediate mathematical deductions, while the replay verifies all
finite premises used here.
