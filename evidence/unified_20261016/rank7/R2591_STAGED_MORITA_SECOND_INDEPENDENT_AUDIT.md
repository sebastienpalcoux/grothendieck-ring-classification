# Independent audit of the staged Morita exclusion of R7_4_2591

Status: **PASS for the general complex categorical argument**.

I read the complete `R2591_STAGED_MORITA_EXCLUSION.md`, after previously
independently auditing its twisted-V4 Morita input. The new argument closes
that reduction without a pivotality, unitarity, or associator-classification
assumption. The finite source/group replay is a separate verification.

The character-twist argument forcing phi(L)=L is valid even for a twisted
regular algebra Q. Its four character-twist bimodules have underlying
support L, are distinct invertibles, and account for all four original
invertibles. If phi(L) differs from L, the two index-two normal subgroups
generate K; the noninvertible support is a single orbit of size eight.
The order-two stabilizer has injective projections into L. Its projective
representations are the two ordinary one-dimensional characters after a
coboundary normalization. Restricting characters of V4 onto that order-two
subgroup is surjective. Tensoring with a character twist therefore
interchanges those two simples, contradicting their individual fixedness.
No trivialization of the associator outside L is used.

Once phi(L)=L, the two irrational support orbits are the two L cosets,
and there is exactly one original irrational simple on each. Their
mutual duality forces a outside L. For K=D8, conjugation by any such a
acts on the three nonidentity elements of L as a transposition, whereas
(phi|L)^2 cannot be a transposition in S3. Thus K is abelian and phi
has order at most two. Its restriction to V4 fixes a nontrivial delta.

The algebra A=1+delta is an actual subalgebra of Q. It is not inferred
from a based-ring subgroup alone. Its regular order-two multiplication
can be normalized and is separable. Centrality of delta and phi(delta)=delta
give four size-two pointed orbits and four size-two irrational orbits,
each with order-two stabilizer. Since such projective stabilizers split,
the A-bimodule dual again has eight invertibles and eight dimension-t
simples. Comparing the rational coefficients in t^2=1+4t verifies that
the invertibles still act freely on the irrational simples.

The staged inverse algebra is likewise actual: Q as an A-bimodule has
relative dimension two, multiplication Q tensor_A Q -> Q, and unit A.
An A-bimodule map A->Q is determined by its unit component, in the
one-dimensional Hom(1,Q), so it is connected. It must be 1+h because
every noninvertible has dimension t>2. Separability forces the regular
order-two algebra. The equivalence of its bimodules with Q-bimodules
in the original category follows directly by restricting and extending
the two Q actions, with compatible relative tensor products.

Finally, the integral TY sector forces h to be nonnormal in the new
order-eight invertible group: a normal order-two subgroup would have
four size-two double cosets, each splitting into two invertibles. Hence
the new group is D8 and h a reflection. If its image under the free-orbit
right-action automorphism lay in the same reflection class, a size-two
irrational orbit would produce a forbidden dimension-t original simple.
It must lie in the other class. With H=<s> and psi(H)=<rs>, the two
irrational double orbits have rotation supports {1,r^-1} and {r,r^2}.
Multiplication by central r^2 exchanges them. Either invertible bimodule
on the pointed coset H r^2 therefore interchanges the two original
irrational simples, contradicting the source fixedness rules.

All support arguments are unaffected by projective normalization or
the pointed associator. The proof uses an actual chain of separable
algebras, so no formal Morita inverse or unsupported coherent action is
being substituted for a categorical construction. No gap was found.

The independent optimized replay of `verify_R2591_staged_morita.py`
also passed. It rechecks the source tensor and the prior twisted-V4
reduction, enumerates all five groups of order eight, and verifies all
16 opposite-reflection configurations. The source-compatible inverse
group systems comprise eight for C4 x C2 and 112 for C2^3, with none
for C8, D8, or Q8. The receipt is
`R2591_staged_morita_independent_O.json`.
