# Independent audit of the four PSD-Gram exclusions

Result: **PASS, general complex categorifications**, for `R7_4_776`,
`R7_4_927`, `R7_4_2126`, and `R7_3_909`.

This audit does not require a pivotal, spherical, pseudo-unitary, or unitary
structure. The earlier categorical audit of the split-involution module
construction and the two evaluation Gram identities applies without a
restriction on the number of fixed simples.

For any hypothetical category, evaluation at a simple right module gives
an actual matrix whose columns are nonnegative integral multiplicities of
the simple objects of the Morita dual. Removing its unit column gives
`Q = sum(v v^t)` over the nonunit dual simples. Thus every actual column
satisfies `Q - v v^t >= 0`. The positivity here is ordinary positivity of
Gram matrices, unrelated to a categorical pivotal dimension. Frobenius–
Perron dimensions give the positive prescribed dimension of each column.

The exact filter is valid also for singular Q. If I indexes a full-rank
positive definite principal block P, then
`Q = Q[:,I] P^{-1} Q[I,:]`. A rank-one subtraction is positive semidefinite
precisely when v is in this column space and
`v[I]^t P^{-1} v[I] <= 1`. A nonpositive principal block contradicts
positive semidefiniteness; Q=0 allows no nonzero column. The published
integer filter implements these conditions by exact denominator clearing.

An independent replay used a different anti-module enumeration: choose
generating words spanning the full source algebra, enumerate the generator
matrices, recover the remaining matrices by rational linear algebra, and
check every fusion relation and transpose-duality relation. It did not use
the certificate generator's propagation algorithm. Every resulting sign-
gauge orbit coincides with exactly one recorded branch.

| Source ring | Complete gauge orbits | Independent generators | Generator tuples |
|---|---:|---|---:|
| `R7_4_776` | 55 | 1, 2, 5 | 512 |
| `R7_4_927` | 20 | 2, 4 | 40 |
| `R7_4_2126` | 12 | 1, 5 | 16 |
| `R7_3_909` | 27 | 1, 3, 4 | 64 |

All four tensors were independently reopened from the compressed census
and compared with both the discovery frontier and current ledger; their
SHA-256 digests match the public certificates. The finite dimension and
entry-bound column enumerator was reviewed for completeness. The replay
then replaced the published PSD filter with a rational implementation,
selecting a nonsingular principal block by exhaustive combinations rather
than the published row-reduction pivots. All 114 rebuilt systems match the
recorded metadata. Every recorded separating vector satisfies `y^t A >= 0`
and `y^t b < 0` by exact rational arithmetic; no optimizer is called.

The complete per-case digests, orbit counts, filtering counts, and all 114
negative pairings are recorded in `psd_gram_independent_audit.json`. The
four exclusions may therefore be promoted to general-complex exclusions.
Passing relaxations for other rings remain undecided.
