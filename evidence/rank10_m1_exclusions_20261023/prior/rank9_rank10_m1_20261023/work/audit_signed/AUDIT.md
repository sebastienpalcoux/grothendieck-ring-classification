# Independent audit of the sphericalization bridge

Audit date: 23 October 2026. Scope: the exact signed-associativity and
dimension-character arguments in `work/general_signed` and
`work/rank9_bridge`. This audit does not certify model constructions or
obstructions stored elsewhere.

## Verdict

The mathematical bridge is valid for the recorded inputs. The complete replay
checks 69 non-self-dual sign problems, 22 alternative signed character
inventories, 77 original character inventories, 40 self-dual saturation
receipts, and three additional self-dual branch exclusions. The bridge proves
sphericality for every hypothetical categorification of the 109 distinct
recorded rings. Combined with the recorded original-character obstructions,
it proves general complex non-categorifiability for the 15 rings listed in
`audit_result.json`. No status downgrade is required by this audit.

The resulting statement is about existence of a spherical structure on an
arbitrary hypothetical categorification. It does not assert existence of a
categorification, and the positive-dimension reductions do not assert
unitarity.

## Mathematical checks

Let R have basis b_i, duality i -> i*, and multiplicity-one coefficients N.
For a hypothetical complex categorification C, its sphericalization has a
central invertible sign object epsilon and two lifts of every simple. Choose
the unit lift and dual-compatible lifts X_i. Such a choice always exists:
choose one lift for a non-self-dual pair and define the other by duality;
both lifts of a self-dual simple are self-dual. Equivalently, the latter fact
follows because the two lifts have nonzero opposite spherical dimensions,
whereas duality preserves spherical dimension.

In the quotient by epsilon = -1, the basis b_i has coefficients T_ij^k in
{+N_ij^k,-N_ij^k}, with unit coefficients T_ij^0 = delta(j,i*). Associativity
and rigidity yield cyclic symmetry of the trace triple (i,j,k*) and dual
reversal (a,b,c) -> (c*,b*,a*). These are precisely the six possible ordered
triples used by the oriented verifier. It does not assume that a signed
quotient of a commutative ring is commutative. In the self-dual situation,
cyclic symmetry and reversal do give all permutations, so the unordered
triple representation used there is justified.

A different dual-compatible lift choice acts by
T_ij^k -> s_i s_j s_k T_ij^k, where s_0 = 1 and s_i = s_i*. The recorded
gauge-coordinate rank proves that every orbit reaches the normalization
used in the finite enumeration; no unsupported Frobenius-Schur normalization
is imposed.

Writing each nonzero sign as (-1)^x converts associativity into exact integer
sign polynomials. Whenever one coefficient has absolute value equal to the
sum of the others, equality in the triangle inequality forces the corresponding
signed monomials to align. Because the all-positive assignment solves each
polynomial, the inferred linear equations over F_2 are homogeneous. The
verifiers reconstruct the original equation, each reduction, every rank
claim, and every remaining finite-domain assignment. Thus the reduction is
necessary, and the eventual enumeration is exhaustive.

The signed quotient is a finite-dimensional semisimple complex algebra.
Indeed, duality is an anti-involution, the unit-coefficient trace makes the
basis orthonormal, and regular multiplication is closed under Hermitian
adjoint. Hence its regular image is a finite-dimensional *-algebra. The
common kernel of the regular commutators consists exactly of the
one-dimensional Wedderburn components: a matrix block of size at least two
has no nonzero vector annihilated by every commutator. This justifies the
scalar-character count even for noncommutative signed tables.

For each proposed scalar character the independent checker verifies every
multiplication identity and the separating-generator identity. Distinct
irreducible factors supply distinct characters, and their total degrees
equal the commutator-kernel dimension. Consequently the inventory is
complete, rather than a numerical selection of possible characters.

A categorical dimension character is nonzero on every simple and equal on
dual pairs. Put delta = sum_i d_i d_i*. The sphericalization has dimension
2 delta, while its formal codegrees are the doubled codegrees from the
original and signed summands. Therefore all these codegrees belong to
Q(d_i), and delta divided by each codegree must be an algebraic integer.
These are the exact hypotheses of the field and norm obstructions used.

The regular Casimir eigenvalue on a simple algebra representation E is
dim(E) f_E. This scaling matters for divisibility. The original-character
checker removes the scalar components, determines the remaining matrix
sizes from the rank deficit (4, 8, or 9), and divides the eigenvalues by 2
or 3 accordingly before applying norm tests. The alternate signed-branch
checker applies only field tests to its Casimir eigenvalues; multiplication
by a nonzero rational integer does not change field containment.

The norm test is necessary even when the two numbers generate different
fields: extend to a common number field and take its norm. The normalized
prime valuation of the numerator norm must be at least that of the
denominator norm. The field-degree test uses the tower law. The finite-prime
test chooses a prime where the monic defining polynomial of the candidate
dimension field splits squarefreely. Such a prime splits completely in
that field. An algebraic integer lying in that field has a minimal polynomial
that splits modulo the prime, possibly with repetitions; an irreducible
factor of degree greater than one therefore contradicts containment.

If only the gauge-original signed table remains categorically admissible,
choose those lifts. Every product then decomposes into the chosen lifts,
which form a fusion subcategory of the sphericalization. Forgetting lifts
is a tensor equivalence with C, so its spherical structure transports to C.

Finally, when the inventory gives a real Galois embedding and signs s_i
with s_i d_i positive and s_i s_j = s_k whenever N_ij^k is nonzero, those
signs define a monoidal natural automorphism of the identity. Twisting the
spherical structure by it preserves sphericality and gives a positive
dimension function. Uniqueness of the positive normalized dimension
function identifies it with FPdim. Extending the embedding to algebraic
structure constants gives the asserted Galois-conjugate pseudo-unitary
category. This is a valid conditional reduction for subsequent exclusions.

## References checked

1. V. Ostrik, *Pivotal fusion categories of rank 3*, arXiv:1309.4822,
   Remark 2.11, Theorem 2.13, Corollaries 2.14-2.15, and Section 5.1(a)-(c).
   These supply the Casimir scaling, dimension-field/divisibility facts, and
   the sphericalization section criterion. The cited statements are not
   restricted to rank three.
   <https://arxiv.org/pdf/1309.4822>
2. P. Etingof, D. Nikshych, V. Ostrik, *On fusion categories*,
   arXiv:math/0203060, Theorem 2.3, Proposition 2.9, Corollary 2.10,
   Remark 3.1, Proposition 5.14, and the observation after Theorem 2.30.
   These provide positivity of squared norms, sphericalization, nonzero
   real spherical dimensions, and algebraic number-field realizability.
   <https://arxiv.org/pdf/math/0203060>

## Replay and implementation qualification

From the package/workspace root, run:

```
python work/audit_signed/replay.py
```

The runner loads tensors directly from both supplied gzipped table files,
checks their binding to receipts, replays all sign/character certificates,
checks coverage of the sphericality bridge for every original inventory,
and writes checksums and explicit case lists to `audit_result.json`.
Two deliberately corrupted receipts must be rejected.

Some older self-dual verifiers use Python `assert`. Therefore this combined
runner explicitly rejects optimized Python execution (`python -O`), which
would disable those assertions. The newer oriented and character verifiers
use explicit checks and were also successfully run under `-O` separately.
No discovery file was modified in this audit.
