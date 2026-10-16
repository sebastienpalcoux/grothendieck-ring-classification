# Four general exclusions from positive-semidefinite Gram subtraction

The four rings are `R7_4_776`, `R7_4_927`, `R7_4_2126`, and `R7_3_909`.
The categorical input is the general-complex module construction and
the two evaluation Gram identities proved in `THREE_FIXED_GRAM_PROOF.md`.
No pivotal, spherical, pseudo-unitary, or unitary hypothesis is imposed.

For an anti-module representation T and a simple right module m, write

    Q = sum_i M_i[m,m] M_i - e_m e_m^t.

Every hypothetical categorification supplies a decomposition Q=sum vv^t,
one nonnegative integral column for each nonunit simple of the Morita
dual. Each column has its prescribed positive FP dimension. The previous
finite Gram condition used entrywise bounds on v. We additionally use
the necessary condition

    Q-vv^t is positive semidefinite.

This follows because it is the sum of the other rank-one Gram matrices.

## Exact finite filter

If Q is not positive semidefinite, no Gram decomposition exists. Otherwise
choose a maximal independent set I of columns and put P=Q[I,I]. Unless
Q=0, P is positive definite and Q=Q[:,I] P^{-1} Q[I,:]. For any column v,

    Q-vv^t >= 0

is equivalent to both

    v = Q[:,I] P^{-1} v[I],
    v[I]^t P^{-1} v[I] <= 1.

The first equality says that v lies in the range of Q. After factoring Q
through the positive definite matrix P, the second is the usual rank-one
Schur-complement criterion I-ww^t >=0. These statements remain valid when
Q is singular. For Q=0, no nonzero column can occur.

The implementation chooses I by rational row reduction, verifies positive
definiteness through exact leading principal minors, verifies the displayed
reconstruction of Q, and clears denominators in both tests. Thus all final
range and quadratic-form checks use Python integers. It uses no numerical
eigenvalues or tolerances.

## Exhaustive exclusions

The public source-bound verifier regenerates all anti-module matrices from
their entry bounds, parity, transpose-duality, source annihilators, and
complete fusion relations. Sign-gauge orbits number:

| Ring | Complete anti-module orbits |
|---|---:|
| R7_4_776 | 55 |
| R7_4_927 | 20 |
| R7_4_2126 | 12 |
| R7_3_909 | 27 |

For each of all 114 orbits, the certificate specifies a module simple m.
The verifier regenerates every finite nonnegative integral column with
the correct FP dimension and entry bounds, then applies the exact filter
above. It builds Ax=b from the upper-triangular Gram entries and the
required counts of each dual dimension. A recorded integral vector y is
checked to satisfy

    y^t A >= 0,        y^t b < 0.

Hence even a nonnegative real solution to that branch is impossible.
Every possible anti-module branch is covered, so the four source rings
have no complex fusion categorification.

Run `python verify_psd_gram.py --repo REPOSITORY_ROOT`. The replay reopens
the original compressed rank-seven census, checks all source tensor
digests and based-ring axioms, regenerates all finite domains, and verifies
all 114 separating vectors. It never calls an optimizer. The existing
vendored helpers retain their original SHA manifest; the new exact filter
is separately bound by SHA-256 in `psd_gram_certificate.json`.

The earlier seven Gram exclusions do not depend on this stronger filter.
Surviving relaxations in other rings are not being claimed as monoidal
models or as categorifications.
