# General exact reductions

The implementation `negative_subring.py` transfers only frozen general
nonexistence decisions. A dual-closed basis subset is checked for product
closure, then its entire multiplication tensor is matched by a unit-preserving
permutation to a rank-six or rank-seven tensor with a published negative
decision. Both that tensor and the full source decision are hash bound. A
categorification would contain the corresponding full fusion subcategory,
contradicting the source theorem. No absence from a positive-model list is
treated as a new exclusion.

For `quadratic_compression.py`, use the already proved full-I(1) compression
theorem in `evidence/theoretical_20261016/compression/full_I1_compression.tex`.
If quadratic factors of the regular Casimir polynomial in Q(sqrt(d)) are
(x²-t_j x+n_j)^m_j, set

    Q_d = f_d sum_j m_j (t_j²-4n_j)/n_j²,

where f_d is the fundamental discriminant (quadratic character conductor).
The multiplicity m_j is the regular spectral multiplicity; it automatically
accounts for (dim E)² while the Casimir eigenvalue is dim(E)f_E. Thus no
commutativity assumption is needed. A spherical categorification with
dimension field K satisfies [K:Q(sqrt(d))]Q_d ≤ 1. If the quadratic
squareclasses present have F2-rank r, their compositum has degree 2^r and is
contained in K. Hence 2^(r-1)Q_d ≤ 1.

For an arbitrary categorification, sphericalization has the original fusion
algebra as its plus sector and doubles its Casimir eigenvalues. The known
sector's reciprocal-square norm is divided by four, so necessarily
2^(r-1)Q_d ≤ 4. A strict violation is a general exclusion. For a weakly
integral ring or a ring with exactly two distinct Frobenius-Perron dimensions,
the existing general-to-Galois-pseudo-unitary reduction supplies a spherical
categorification whenever any categorification exists; in that case the
stronger bound1 applies. The reconstruction applies the compositum degree
also in this stronger branch. These additional witnesses do not change any
previous positive or unresolved decision.

All spectral factorizations, rational inequalities, F2-ranks, and gate
hypotheses are recomputed from the exact source tensor. Replay uses explicit
checks retained under optimized Python. Counts are output of the scan and
are never proof premises.
