# Independent audit of the rank-37 witness obstruction

Auditor: two_d_two. Date: 16 October 2026.

**Scope:** rejection of the specified historical necessary-system witness only.
This is not an exclusion of R6_8_1660, of all 1,136 retained profiles, or of an
unspecified modular representation with the same rank.

I read the complete `R1660_WITNESS_VERLINDE_OBSTRUCTION.md`, the exact research
checker, and the source of its low-character, spectral-projector and finite
character calculations. I independently replayed its exact arithmetic in
optimized Python and obtained the displayed coefficient 1/2. I also computed
the full twist spectra of every active irreducible directly from the two local
character tables.

## Identification of the two lines

The recorded restriction/twist fiber at phase 4 consists of exactly two copies
of `(0,0,1,1,0,2)`. Among all active irreducibles, precisely `(61,5)` and `(0,1)`
have phase 4, and each contributes one dimension. The former occurs once, has
dimension 12, and has simple twist spectrum and a one-dimensional twist-one
space. The latter occurs once and is one-dimensional. Thus there is no
unrecorded freedom to put the second phase-4 line in another irreducible for
this witness.

The projector Q onto the low compression eigenvalue `-sqrt(6)/12` is the
twist-one line of `(61,5)`, by the already audited saturated-sector theorem.
Applying S to that line yields equal, nonzero coordinates at the two repeated
rows. Since its phase-4 image is one-dimensional, it is the symmetric sum of
the two simple-label vectors. Orthogonality gives their antisymmetric
difference as the `(0,1)` line. No arbitrary choice of a basis in a repeated
isotypic component is being used.

## Character probabilities and weighted ratios

Let b be the normalized symmetric sum. For each phase t of W, the operator
`P_4 S P_t S^{-1}` has trace equal to the squared transition amplitude between
the two one-dimensional twist eigenspaces. Expanding the spectral projectors
as finite Fourier sums gives exactly the two-variable character average in
the proof. CRT requires local phase coordinates `(12,1)` for global phase 4,
and global reconstruction `t=3a+16b mod48`; both are implemented correctly.

Write `a_E=|<e_E,S e_W>|^2`, with e_W the normalized twist-one vector of W.
The low-character formula gives `a_E=L_E Q L_E^*`. All L and Q entries are
real in this witness, which the revised checker verifies, so the displayed
unconjugated products are legitimate. More directly, the saturated vector
gives `a_E=L6(v_E)^2/96`; this also supplies the proposed standalone rational
replay. Its total is one.

Since every phase space in W has dimension one, division by the nonzero
phase mass gives the expectation of the Verlinde spectral diagonal on that
line, regardless of other irreducibles having the same phase. The character
probabilities and weighted ratios in the proof therefore determine
`<b,N_A b>` without choosing any unknown S entries. Their exact sum is 2.

## The mixed term and the half-integral coefficient

On the one-dimensional hidden summand, S acts by a scalar. Thus the
antisymmetric difference h is an eigenvector of N_A with eigenvalue -1,
because both simple labels in its support have spectral ratio
`S_{A,B}/S_{0,B}=-1`. In particular the mixed terms with the orthogonal
visible vector vanish. This conclusion can be seen either from this
eigenvector identity or directly after applying S inverse; the equal ratios
at the doublet are essential and are checked.

Consequently each original label vector `(b±h)/sqrt(2)` has diagonal entry
`(2-1)/2=1/2` in N_A. This contradicts integral fusion coefficients. It is
independent of signs or phases in a full modular matrix realization and of
any numerical reconstruction.

**Verdict:** the scoped categorical and exact arithmetic argument passes.
The final publication checker should continue to bind the exact witness,
the two local character tables, and the low-character identification; it
must preserve the stated single-witness scope. The historical witness still
solves its original weaker linear system.

## Final standalone replay

I subsequently read every line of the standard-library checker
`verlinde_obstruction/verify_r1660_witness_verlinde.py`, SHA256
`a05b927f2592ab4f2503bfd177d91df85bd8fa38bc8cac498ca298bf7109b9bd`,
and independently ran it with Python `-O`. The receipt
`verlinde_obstruction/replay_independent_O.json` reports PASS and
`FIXED_WITNESS_EXCLUDED` with exact coefficient `1/2`.

This version checks all six input hashes, all 1,536 old integer equations and
all 1,447 bounds, regenerates the active representation list and phase-4
support, verifies the source FP character, identifies A's Galois character
from its dimension, verifies the four field-coordinate weights, and computes
the two local character averages using exact cyclotomic arithmetic. Its
four-embedding field inverse and the conversion from descending input
character coefficients to ascending internal coefficients are correct.
Its explicitly false `source_ring_excluded` field preserves the proper scope.
