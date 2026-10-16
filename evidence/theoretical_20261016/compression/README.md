# Compression over all constituents of I(1)

This package records a strengthening of the modular-representation argument
in Andrew Schopieray, *The dimension block of a spherical fusion category*,
arXiv:2609.35287v1, Lemma 4.1 and the proof of Theorem 5.1:
https://arxiv.org/html/2609.35287v1

For a spherical categorification with simple-dimension field K and Galois
group G, all formal codegrees belong to K. For every character chi of G,

    sum_E |sum_sigma chi(sigma) sigma(1/f_E)|^2 <= |G|/conductor(chi).

Each simple constituent of I(1) supplies one coordinate, regardless of its
multiplicity. The complete proof is in `full_I1_compression.tex`.

For the regular Casimir B=sum_i N_i N_i^T, group its irreducible quadratic
factors x^2-t_j x+n_j, with multiplicities m_j, by their real quadratic
field L. If q is the fundamental discriminant of L, define

    Q_L = q sum_j m_j (t_j^2-4n_j)/n_j^2.

A spherical categorification requires Q_L<=1. This works for noncommutative
rings: the Casimir eigenvalue is dim(E)*f_E and its regular multiplicity
is dim(E)^2, which is precisely the weight needed by the Fourier norm.

An arbitrary categorification requires Q_L<=4 by applying the argument
to its sphericalization. At the boundary Q_L=4, the sphericalization's
dimension field is exactly L and every formal codegree of its negative
epsilon sector is rational. This boundary conclusion is used in the
separate general exclusion of R7_3_695. It does not assert a nontrivial
grading: categorical and Frobenius--Perron dimension fields must not be
conflated in the non-pseudounitary setting.

## Exact coverage and scope

`source_tensors.json` contains the 85 unresolved source tensors at the start
of this revision: two rank-six, 39 rank-seven and 44 rank-eight tensors.
Every tensor carries its SHA-256 of compact JSON and source path. The input
revision is `1592905dc573227ad03659a6370a9459d40db26c`. Rank-seven tensors
were compared entrywise with the source ledger; rank-eight scoped cases
were compared with the ledger's canonical tensor hashes.

`verify_full_I1_scan.py` scans every quadratic factor of every Casimir.
It performs 82 nonempty quadratic-field checks on all 85 tensors. The nine
violations are:

| Cases | Q_L | Consequence of this test alone |
|---|---:|---|
| R8_2_35, R8_2_38, R8_2_346, R8_2_406 | 9/4 | No spherical categorification; separate general reductions are supplied elsewhere |
| R8_2_318, R8_2_735 | 5/4 | No spherical categorification |
| R7_3_695, R7_3_783, R7_3_1015 | 4 | No spherical categorification; sphericalization boundary constraint |

This is a complete scan of quadratic factors, not a test of all higher
degree fields or a completion of categorifiability for the remaining rings.

For R8_2_318 and R8_2_735, `verify_rank8_full_I1.py` also verifies all eight
characters exactly and shows that the only characters nonzero on every
basis element are the real Frobenius--Perron character and its conjugate.
Both are duality invariant. Hence any pivotal categorification would be
spherical: the two rings have no pivotal categorification either.
These compression arguments alone do not address arbitrary nonpivotal categorifications. The independent [anti-invariant module proof](../rank8/ANTI_MODULE_EIGHT_GENERAL_PROOF.md) now gives a general complex exclusion for both rings.

## Reproduction

Run with Python 3 and SymPy:

    python verify_full_I1_scan.py
    python verify_rank8_full_I1.py

The scripts write the two adjacent JSON certificates. They verify tensor
hashes before performing exact arithmetic and do not alter decision ledgers.
The theorem's normalization and sphericalization boundary argument received
two independent mathematical audits during this revision. The categorical
input remains the cited modular compression theorem, rather than a claim
that numerical verification alone establishes categorifiability.

## Higher-degree fields and a new general exclusion

The targeted higher-degree check is recorded in
`higher_field_compression_certificate.json`. Among all 85 original residual
tensors, only R8_2_190, R8_2_489, R8_2_857 and R6_8_1660 have Casimir
factors of degree greater than two. Every character of their corresponding
fields is checked exactly by `verify_higher_field_compression.py`.

For R8_2_190 and R8_2_489 the cyclic quartic field has conductor 20.
The primitive-character bounds are equalities; the other ratios are 1/2.
These inequalities provide no exclusion. For R6_8_1660, the two relevant
biquadratic characters attain equality, as used in its twist-one analysis.

For R8_2_857, primitive characters of conductor 32 have ratio four.
The sphericalization boundary forces a dimension field of degree eight;
three exact signed Jacobi-matrix branches then give a **general complex
categorification exclusion**. See `R857_GENERAL_PROOF.md`, its independent
audit, and `verify_R857_general.py`. This conclusion changes its general
classification and is stronger than a spherical obstruction alone.

The higher-field verifier also confirms that the four cases
R8_2_35, R8_2_38, R8_2_346 and R8_2_406 force two independent quadratic
fields in any sphericalization. Their minimal field index strengthens the
ratio to 9/8 above the allowed bound. `MIXED_FIELD_FOUR_PROOF.md` gives
this second general proof, independent of a pseudo-unitary reduction.

Additional reproduction commands:

    python verify_R857_general.py
    python verify_higher_field_compression.py
