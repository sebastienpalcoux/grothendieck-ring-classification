# Independent audit of the R2053 to R18 categorical reduction

Status: **PASS**. The two-dimension workstream independently read the full
`R2053_R18_MORITA_REDUCTION.md` and every line of its standalone verifier,
then executed a fresh optimized replay. The receipt is
`R2053_R18_independent_optimized.json`.

The starting categorical reduction is the previously audited four-case
dihedral theorem. Its actual inverse algebra is supported on a reflection
H in D8; the two irrational double orbits have trivial stabilizers, hence
each supports exactly one simple bimodule. There is therefore no projective
representation ambiguity in determining their duality. The explicit
dual-support formula a^{-1} phi(g^{-1}) fixes the two supports when a=1
and exchanges them when a=r^2. The source R2053 has both irrational
simples selfdual, so the former case is necessary.

The rotational branch is excluded by the previously proved pivotal
odd-multiplicity argument and TY(C4) eighth indicator. I independently
checked that the present verifier recomputes the odd cubic multiplicities
and the exact two residue sums [8,24,8,24], rather than loading the earlier
receipt. The general-complex scope is preserved by applying the published
two-FP-dimension Galois pseudo-unitarity bridge to the actual Morita dual
and its actual inverse algebra. No unitary or arbitrary-central-lift
assumption enters this step.

In the surviving reflection case, sigma=s rho obeys sigma r=r sigma and
sigma^2=r^3+(1+r+r^2+r^3)sigma. This follows directly from rho r=r^{-1}rho,
rho s=rs rho, and rho^2=1+(s+rs+r^2s+r^3s)rho. The eight indicated simples
are closed under tensor products and duality, so they define an actual
fusion subcategory, not merely a candidate subring realization. Reversing
the rotation generator gives precisely the R18 presentation.

The optimized replay passes both immutable source hashes, the source
projective-block hypotheses, all fusion identities of the constructed
rank-sixteen forms, both inverse-orbit dualities, the rotational indicator
sums, and all 512 endpoint coefficients. The endpoint source permutation
is [0,1,7,2,4,3,6,5]. It uses exact integer arithmetic and no optimizer.

Thus every complex categorification of R7_4_2053 would produce one of
R8_1_18. The completed `R18_STS_MOMENT_PROOF.md` now excludes that endpoint
generally, so their conjunction is a general-complex exclusion of R2053.
