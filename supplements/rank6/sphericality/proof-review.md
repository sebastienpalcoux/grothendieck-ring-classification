# Review of the proof of sphericality in rank six

The section numbers refer to *Spherical structures on fusion categories of rank six*. The comparison is with the [preceding manuscript](https://github.com/sebastienpalcoux/grothendieck-ring-classification/blob/7a79d637871988cd954770e987c4b61c6a40bb19/manuscripts/rank6/sphericality/Sphericality_in_Rank_Six.pdf).

## Corrections affecting statements or their use

| Section | What needed justification | Repair |
| --- | --- | --- |
| 2 | The cyclic prime-power corollary used an unspecified rank. The two trace normalizations in the sphericalization were implicit. | Define the rank before the degree inequality. Restrict the unit trace to the two sign idempotents to get the factor of two in the formal codegrees. |
| 11–12 | Two intermediate statements concluded sphericality where a subsequent reduction used a pseudo-unitary Galois conjugate. | State the stronger conclusions proved by the primitive-ratio exclusions and the proper-subfield theorem. |
| 13 | The proposition restricting the four moments used the hypothesis that the trace of the dimension ratio exceeds one million. The hypothesis was missing from its statement. | State the hypothesis and invoke the separate bounded-trace result for its complement, including the endpoint. |
| 13 | A reciprocal-mass table and a quartic height bound each require hypotheses that need checking before reuse. | Apply the quadratic pair mass bound first and give the conductor-eight inequality in the setting where it is used. |
| 14 | The ordinary row inequality for arbitrary codegree referred to a lemma stated for codegree four. | Apply the diagonal twist identity directly to the rational row of codegree h. |
| 14 | The vanishing of the ordinary complementary evaluations had been deduced for even n. The valuation-eight argument also needed it for odd n. | Compare the squared lengths modulo 128. Both quartic traces are divisible by 128, and the 2-adic valuation of 1 + n² is one for odd n. This excludes the nonzero evaluation. |

## Shorter arguments

| Sections | Main change |
| --- | --- |
| 2–5 | A single relative-discriminant inequality gives the trace estimates in degrees four and six. Schur's cubic inequality gives the codegree gap at conductors seven and nine. The Gram matrix of the Gaussian periods at conductor twenty-five gives a direct obstruction to total positivity. |
| 6–8 | For conductor twelve, the rational rows of codegrees 3 and 12 reduce to a single Pell recurrence tuple, excluded modulo seven. For codegrees 3 and 8, character orthogonality determines the shape of the Perron row, whose integrality condition would give a square congruent to 12 modulo 16. |
| 9–10 | A common argument for three rational characters of codegree four serves five exclusions. The Morita argument identifies the extra induction labels and computes their Fourier entries. |
| 11–12 | In the cyclic quartic field of conductor fifteen, an integral period basis and two Fourier bounds replace 23,625 lattice tests. |
| 13 | A weighted Cauchy–Schwarz estimate handles distinct quadratic complements at conductors sixteen and twenty-four. At conductor twenty-four it lowers the trace ceiling from 500 to 188. Each of the remaining 247 primitive ratios has a direct exact certificate. When the conductor-eight Fourier bound is attained, the ratio determines every weight at both conductors. This removes 86 stored separating problems from the conductor-sixteen proof. |
| 14 | At valuation eight a marked square equation has no ordinary solution. Hensel's lemma and the perfect trace pairing produce a signed solution. This replaces the finite census at that valuation. |

## Reproducing the finite computations

The [verification instructions](README.md) cover the current manuscript. The optional verbose output reports intermediate counts. The numerical verifiers check the finite parts of the argument. The categorical reductions, bounds that make the searches exhaustive, and the new hand proofs were checked by reading the arguments and their cited hypotheses.
