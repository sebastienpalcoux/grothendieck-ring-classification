# Independent review of R8_3_3258

**Decision: accept the general-complex exclusion.** The complete-domain
certificate, indicator coverage and general sphericalization reduction are
sound. The canonical optimized exact replay passes. The independent direct
operator audit passes in both normal and optimized Python modes and records its complete arithmetic result in
`review_r3258_atomic.json`. This is a separate AI review, not human verification
or formal proof-assistant verification.

The atomic modular theorem was separately reviewed in
`../review/ATOMIC_MODULAR_REVIEW.md`. Here every character lies in the real
FP field Q(sqrt(5)). For each non-FP character E there is a separate simplex
containing every allowed low restriction of dimension D/f_E. An actual
distinguished induced-unit frame supplies one choice in each simplex.
No complete joint-frame enumeration is claimed or needed: the independent
simplex construction contains every actual frame, including every labeling
of equal-dimensional distinguished simples.

The center formula S(A_E,Z) = (D/f_E) chi_E(FZ) follows from
[Deshpande, arXiv:1611.04486, equation (39) and Corollary 4.5](https://arxiv.org/html/1611.04486v1).
Its symmetry gives the partial-S algebraic-integer test. The already reviewed
center relation STS = D T^{-1} S T^{-1} gives the atomic row

    chi_E(c) chi_F(c) - delta(G,F) f_F chi_E(c)

on a choice c in simplex G, and right hand side delta(F,FP) f_F - 1.
This accounts for the fixed tensor unit exactly once. All coefficients are
in the field fixed by the relative trace; dual high constituents are retained
with equal twists and full multiplicity. The identities with the FP character
in S-symmetry hold automatically from the prescribed dimensions.

The independent audit imports the reviewed complete original restriction and
phase domains, and the producer's character reconstruction. It then uses its
own rational-pair arithmetic in Q(sqrt(5)). It checks all multiplication and
orthogonality identities for eight distinct characters, so the characters
exhaust the eight-dimensional commutative fusion algebra. For every candidate
restriction, it independently tests integrality of each central eigenvalue
using its quadratic trace and norm. It retains all low columns and rejects
exactly 479 of the original 1,950 high vectors, leaving 1,471.

For each of the seven non-FP characters, the audit independently takes every
low vector of the required dimension from the full original domain. It
recovers the seven simplex sizes 2359,84,155,84,84,84,24, a total of 2,874
distinct labeled choices. The fixed tensor unit is separate. The complete
height-four domain has ten joint phase-trace types and 35 rotation auxiliary
columns, giving 17,619 columns in total. The trace-compression representative
bound 45 is not asserted to be a categorical exponent bound.

The audit recomputes the Casimir Gram matrix and every tensor power directly
from the source tensor. It reconstructs all coefficients of all 17,619
columns and all 241 right-hand-side coordinates from the mathematical row
formulas. It does not call the producer's column or factorized-oracle routines
to obtain those coefficients; it compares with the producer's column only
after its own reconstruction. Every coefficient agrees. Direct integer
pairings with the saved ray are nonnegative on the entire domain, with
minimum zero and a strictly negative right-hand-side pairing. No numerical
optimization status enters this acceptance.

All seven nonunit simples are self-dual. For objects 1 and 2 the witness
j=2 has odd N[j,j*,i]; for objects 3 through 7 the witness j=1 does.
Thus their second indicators are all +1 by the pivotal
[Fuchs--Runkel--Schweigert theorem, as restated in Liu--Palcoux--Ren--Vercleyen,
arXiv:2203.06522v5, Theorem 3.9](https://arxiv.org/pdf/2203.06522).
This is applied in the pseudo-unitary stage, where pivotality is available.
The sole saved indicator branch is therefore complete.

For general complex scope, the canonical verifier regenerates the complete
normalized oriented signed enumeration. It has a single branch, equal to the
original tensor, with trivial gauge. The normalization is the established
positive-indicator sphericalization normalization; ordered associativity and
all oriented trace symmetries are retained. Consequently a hypothetical
categorification has a closed set of chosen lifts in its sphericalization:
the negative lift multiplicities vanish when the signed tensor equals the
original tensor. Forgetting the lifts gives a tensor equivalence and hence
the spherical structure needed for the subsequent character test. All six
rational character alternatives have a zero object
dimension. The remaining irreducible quadratic factor is exactly the FP
Galois orbit. Galois transport then yields a pseudo-unitary categorification,
contradicting the exact atomic separator. This does not assume pivotality or
unitarity of the original hypothetical category.

Canonical read-only commands:

```sh
python evidence/rank8_frontier_20261021/global_induction/verify_accepted_atomic_sts.py
python -O evidence/rank8_frontier_20261021/global_induction/verify_accepted_atomic_sts.py
python evidence/rank8_frontier_20261021/central_integrality/review_r3258_atomic.py
python -O evidence/rank8_frontier_20261021/central_integrality/review_r3258_atomic.py
```

The shared original restriction enumeration, phase compression and inherited
signed-lift framework remain explicit prerequisites. This audit independently
implements the newly introduced arithmetic, complete labeling, full operator
and ray calculation; it is not described as an independent implementation of
every prerequisite.
