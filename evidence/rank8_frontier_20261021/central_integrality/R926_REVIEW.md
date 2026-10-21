# Independent review of R8_3_926

**Decision: accept the general-complex exclusion.** The new partial-modular
filter and the complete label/frame coverage are sound. Fresh normal and
optimized producer replays both pass. The additional independent arithmetic
audit passes and records its exact checks in `review_r926_partial_s.json`.

For a commutative Grothendieck ring every irreducible character E has dimension
one. The distinguished central simple A_E has dimension D/f_E, and
Deshpande, [arXiv:1611.04486, equation (39)](https://arxiv.org/html/1611.04486v1),
combined with character orthogonality gives

\[
S_{A_E,Z}=\frac{D}{f_E}\chi_E(FZ).
\]

By symmetry of S, division by dim(Z) is a fusion-matrix eigenvalue. It must be
an algebraic integer. Here every term is in Q(zeta_24), whose ring of integers
is Z[zeta_24]; integrality of all reduced power-basis coefficients is therefore
an exact necessary condition. No claim of unitarity is needed for this
spherical modular identity. The producer uses FP dimensions only in the
pseudo-unitary stage and separately verifies the complete general lift.

The eight reconstructed characters are distinct, satisfy every multiplication
identity and exact orthogonality, and include the FP character. The audit
recalculates all proposed high-column eigenvalues without calling the
producer's integrality predicate. It independently removes exactly 140 of
2,863 high columns, retaining 2,723, and finds no low-column rejection.

An actual induced-unit frame assigns its eight distinguished simples
bijectively to the eight characters with matching D/f_E. Equal formal
codegrees do not identify their characters. The producer's backtracking
retains all assignments consistent with dimensions and symmetry; the audit
instead enumerates all 24 dimension-compatible permutations for each of the
6,891 complete frames. Both methods retain the same 11 frames and exactly the
same character-label assignments. Ordering interchangeable equal-column-set
groups does not remove any case because all equal-dimension character labels
are subsequently considered.

Every actual low frame is a vertex of the complete frame hull. Its high
columns occur in dual pairs with equal twists, so the dual-orbit compression
is necessary. The audit scans all 49,618 actual cone columns separately for
each of the two second-indicator branches. It uses `column()` and direct
integer dot products, independently of the factorized separation oracle.
Both rays pair nonnegatively with every column and strictly negatively with
the corresponding right hand side. Discovery LP status is not used.

The general certificate explicitly checks all three spherical character
factors. Two fail duality; the remaining factor is the FP Galois orbit and
is excluded by the pseudo-unitary obstruction. The oriented signed quotient
enumeration regenerates all 16 branches without assuming commutativity. Eight
are gauge-equivalent to the original tensor, while the other eight have all
their character factors excluded by duality or exact norm divisibility. This
uses the established sphericalization framework and its positive-indicator
normalization. The parity input is the pivotal Fuchs-Runkel-Schweigert theorem
restated in Liu-Palcoux-Ren-Vercleyen,
[arXiv:2203.06522v5, Theorem 3.9](https://arxiv.org/pdf/2203.06522), which applies
to odd multiplicity in X* tensor X without requiring X simple. Thus the
general conclusion does not assume that the original category is pivotal.

Canonical commands, from the repository root:

```sh
python evidence/rank8_frontier_20261021/global_induction/spectral_generation.py --verify evidence/rank8_frontier_20261021/global_induction/spectral_results/R8_3_926_h4.json
python -O evidence/rank8_frontier_20261021/global_induction/spectral_generation.py --verify evidence/rank8_frontier_20261021/global_induction/spectral_results/R8_3_926_h4.json
python evidence/rank8_frontier_20261021/central_integrality/review_r926_partial_s.py
python -O evidence/rank8_frontier_20261021/central_integrality/review_r926_partial_s.py
```

The independent audit shares the producer's complete domain construction and
exact character reconstruction; it independently checks the newly introduced
filter, permutation coverage and full-column ray evaluations. It is not
represented as an independent implementation of the entire inherited
sphericalization framework.
