# Independent audit of the eight anti-module spectral exclusions

Date: 2026-10-16. **PASS for all eight rings, unrestricted complex scope.**

The proof `ANTI_MODULE_EIGHT_GENERAL_PROOF.md` and its verifier were read
independently. The verifier was rerun and its complete output agrees with
the retained normal receipt. Its source ordering is protected by exact
hash comparison to the rank-eight decision ledger. The same eight tensors
were independently matched to the separately retained compression input
tensors, and their characteristic-polynomial factorizations were checked.

The categorical construction works for any positive fixed count. In
particular, the four-dimensional anti-invariant module exists whenever
one of these eight hypothetical categorifications exists. No pivotal
structure or central lift of the involution is required. The relation
`XX*=X*X` is sufficient for normality of the one matrix used in the
proof; commutativity of the entire ring is unnecessary.

The spectral arithmetic checks as follows. Integrality makes the
characteristic polynomial rational, so each irrational quadratic root
occurs with its conjugate and equal multiplicity. Normality gives the
sum of squared eigenvalue moduli as the squared Frobenius norm, even
for the cases with non-real eigenvalues.

* Bounds A and B give norm squared 12 or 16. The large pair contributes
  34, so is absent. For 319, 320, 370, and 760, all remaining roots have
  modulus one, forcing the contradictory value 4.
* For 318 and 735, the extra pair contributes 6. The only possible norm
  meeting the lower bound is 12 from two copies of this pair. Its trace
  is -4. Norm 12 forces the even diagonal entry to vanish, leaving two
  diagonal entries of absolute value one and hence trace in [-2,2].
* Bound C gives norm squared 12, 16, or 20. The large pair contributes
  38, so is absent. Cases 368 and 758 again have only unit-modulus roots
  left, contradicting the lower bound 12.

Thus the proofs exclude `R8_2_318`, `R8_2_319`, `R8_2_320`, `R8_2_368`,
`R8_2_370`, `R8_2_735`, `R8_2_758`, and `R8_2_760` as Grothendieck rings
of arbitrary complex fusion categories. The arguments are short
theoretical contradictions; the verifier certifies their exact finite
source inputs without enumerating matrices or associators.
