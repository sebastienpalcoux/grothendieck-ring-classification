# Signed support and integer capacities at conductors 12 and 24

For the quartic dimension field of R928, R941 and R982, the two saturated
characters have conductors 12 and 24 and sums `h_f=-1/sqrt(f)`. The preceding
conductor theorem restricts the respective cyclic modular representations
to `SL_2(Z/f)`. Analyzing the sign of the maximal compression eigenvalue
gives additional forbidden twists and exact fibre capacities.

Write `dim(Z)=a+b sqrt(2)+c sqrt(3)+d sqrt(6)` and define the integer masks

    L12(Z)=3c-a-b,           L24(Z)=6d-a-2b.

All four coefficients are integers because the original simple dimensions
have this property and center objects forget to sums of source simples.
The dimension-row Fourier coordinates are `c_f(Z)=L_f(Z)/sqrt(f)`.
Each vector w_f contains four signed dimension-orbit basis vectors, so
`||w_f||^2=4`.

## Statements

1. If `L12(Z)!=0`, then `theta_Z=exp(2 pi i k/12)` with
   `k` in `{0,2,3,4,5,6,7,8,9,10}`. The missing primitive exponents
   `1,11` are the positive quadratic-character class.
2. If `L24(Z)!=0`, then `theta_Z=exp(2 pi i k/24)` with k different
   from `1,5,19,23`. These four missing primitive exponents are likewise
   the positive quadratic-character class.
3. For each of `theta=1,-1`, the fibre satisfies `sum_Z L12(Z)^2=4`.
4. For each of `theta=1,-1,i,-i`, the fibre satisfies
   `sum_Z L24(Z)^2=4`.
5. Every simple satisfies `|L12(Z)|<=4` and `|L24(Z)|<=4`.

The sums count simple objects with their actual multiplicities as distinct
simples, not their multiplicities in I(X). Other fibres have additional
capacities depending linearly on one unknown mixture parameter for each
character. The full two endpoint spectra are recorded in
`composite_verification.json`; any actual spectrum is a convex combination
of the two endpoint spectra multiplied by `||w_f||^2=4`.

## Proof of the spectral endpoints

The primitive real character of conductor 12 is the product of the odd
quadratic characters of conductors 4 and 3. That of conductor 24 is the
product of the odd quadratic characters of conductors 8 and 3. Denote the
2-power conductor by q, where q is 4 or 8. Their local quadratic Gauss sums
are `G_q=i sqrt(q)` and `G_3=i sqrt(3)` in the standard complex embedding.

In the primitive-column permutation model, the local maximal compression
space is spanned by F,H as in the conductor proof. For each of these odd
quadratic characters,

    A F=-H,     A H=F/q.

Its two orthogonal eigenspaces are the lines

    v_(q,epsilon)=F+epsilon G_q H,
    eigenvalue epsilon i/sqrt(q),       epsilon=+1 or -1.

The same formulas hold with q=3. Thus the global compression has maximal
eigenvalue `-1/sqrt(3q)` precisely on the two tensor-product lines with
matching signs. Equality of the dimension-block matrix coefficient forces
`A w_f=-w_f/sqrt(f)`. Decomposing orthogonally into irreducible product
representations, and using equivariant embeddings into the local primitive
column representations, each nonzero component of w_f therefore maps into
the span of these two tensor-product lines. They are orthogonal. In addition,
the two local endpoint vectors have zero **mixed spectral projector pairing**
at every unipotent eigenvalue. This is checked below by the same explicit
finite Fourier calculation as the norms. Thus even a linear combination
of both tensor-product endpoint vectors has no cross term in any spectral
mass. Summing over the orthogonal irreducible components gives the asserted
convex combination, with nonnegative weights adding to one. It is not
necessary to assume the two endpoint lines generate distinct irreducibles.

For clarity, the local profiles can be found without any floating point
calculation. The unipotent generator acts on functions by
`f(x,y)->f(x-y,y)`, and

    (s v_(q,epsilon))(x,y)
       = -chi_q(x)+epsilon G_q chi_q(y)[x=0].

Project this function onto the q-th-root eigenspaces by the finite Fourier
sum on every unipotent orbit. For q=4, the eigenvalues 1 and -1 each have
normalized squared mass 1/4, and one of i,-i has mass 1/2. For q=8, all
four even exponents have mass 1/8 and two of the four odd exponents have
mass 1/4. For q=3, exponent zero has mass 1/3 and one nonzero exponent
has mass 2/3. The sign determines the listed choices.

The full exact profiles, including these signs, are verified directly over
`Q[z]/Phi_q(z)` by `verify_composite_support.py`. Convolving the q-profile
and the 3-profile sends exponents `(u,v)` to `3u+qv mod 3q`.

The vanishing of mixed projector pairings also has a direct description.
On unit-frequency eigenspaces one endpoint is zero. At every remaining
frequency, the big-cell contributions for the two signs have opposite
sign, while the small-cell contributions have equal sign and the same
total size. They cancel. The exact checker enumerates all primitive columns
and all unipotent orbits for q=3,4,8, and verifies zero mixed pairing at
every eigenvalue, so no support or fixed-point assumption is implicit here.

For conductor 12, the endpoint supports are

    {0,2,5,6,8,9},       {0,3,4,6,7,10}.

Both have mass 1/12 at exponents 0 and 6. Their largest mass is 1/3.
For conductor 24, the endpoint supports are

    {0,4,6,7,10,12,13,15,16,18,21,22},
    {0,2,3,6,8,9,11,12,14,17,18,20}.

Both have mass 1/24 at exponents 0,6,12,18. Their largest mass is 1/6.
Multiplying the normalized profiles by 4 gives the squared Fourier masses.
Finally `|c_f(Z)|^2=L_f(Z)^2/f`. The common endpoint masses therefore
give the stated capacity 4, and the largest possible individual squared
mask is `4*12*(1/3)=4*24*(1/6)=16`. QED.

## Scope

This is a uniform necessary-condition theorem for the three quartic cases,
not a categorification or exclusion by itself. Types whose relevant mask
vanishes have zero weight in this spectral calculation, so their twists
must not be removed using that character. The earlier separate twist-one
vanishing outside the dimension orbit remains applicable.
