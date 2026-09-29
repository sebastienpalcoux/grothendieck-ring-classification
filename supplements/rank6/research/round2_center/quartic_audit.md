# Independent audit of the quartic stabilizer-trace proofs

The hardened engine `software/cyclotomic_stabilizer_trace.py` was reviewed
independently of its implementation author. All four general certificates for `R6_4_258`, `R6_4_325`, `R6_8_570`, and
`R6_8_2203` passed complete replay under `python -O`, after the
SciPy optimizer entry points were replaced by functions that raise errors.
Eleven malformed variants per certificate (44 in total) were rejected, covering signed
quotient/module/low-frame completeness, prescribed stabilizer objects,
cyclotomic embedding and trace-domain metadata, indicator branches, high-column
pruning counts, and zero separating vectors. See
`quartic_independent_audit_report.json`,
`quartic_m8_570_independent_audit_report.json`, and
`quartic_m8_2203_independent_audit_report.json`. The final multiplicity-eight
replay took 291 seconds; all its mutation controls also passed.

## Field and finite phase domain

The engine identifies a quartic global-dimension field inside a supported real
cyclotomic field. It verifies the proposed image of global dimension against
its exact polynomial, expresses every dimension in the global-dimension power
basis, checks the resulting multiplication homomorphism, and checks positivity
using real-root isolating intervals. Thus `field_isomorphism` proposes an
embedding but does not itself certify the positive dimension character.
The positive unital character is uniquely the Frobenius–Perron character.

For the reviewed proofs the ambient conductors are 20 and 16, with prime
supports `{2,5}` and `{2}`, respectively. At trace powers 1,2,3 their conductor
boxes are 40 and 32. Put `z = zeta_F`. The entire finite trace domain has the
following independent closed form:

- `(z^a, z^(2a), z^(3a))` for `a mod F`;
- `(0, z^a, 0)` for odd `a mod F`;
- `(0,0,0)`.

Indeed the two relative conjugates of a root of order dividing `2F` but not
`F` are `theta` and `-theta`. Hence odd-power averages vanish and the second
average is `theta^2`. This gives exactly `3F/2+1` types: 31 for `F=20` and
25 for `F=16`. The independently constructed sets agree exactly with the
engine's Galois-kernel enumeration.

This also covers arbitrary exponent orders, rather than assuming a conductor
bound. For `F=16`, every order outside the box has a 2-power exponent at least
6; after raising to any of 1,2,3, a nontrivial cyclotomic layer beyond the
base conductor remains and has zero relative trace. For `F=20`, an outside
order has 2-power exponent at least 4 or 5-power exponent at least 2. The
powers 1,2,3 cannot remove that excess layer. Summing over its Galois fibre
again gives zero, and transitivity of normalized traces proves vanishing
in the full base field. Consequently the extra all-zero type covers every
order outside the finite box. `quartic_phase_check.py` checks the closed
forms and representative first and higher outside layers exactly.

## High-column pruning

Every high restriction column `v` is nonnegative integral and must satisfy
both `G-vv^T >= 0` as a positive-semidefinite matrix and entrywise
nonnegativity of the residual Gram matrix. I independently enumerated the
entire rectangular coordinate box for all five multiplicity-four low frames and tested
positive semidefiniteness by exact rational Schur elimination. These lists
agree exactly with the native range/adjugate enumerator. The full boxes have
at most 2,625 entries and the coordinates at most 6; native integer and
integer-square-root bounds are therefore far from their implementation
limits. See `quartic_pruning_audit_report.json`.

If `z` is the resulting simple central dimension and `D` the global dimension
of the input category, `(D/z)^2` is a formal codegree of its center, hence
an algebraic integer. It follows that `D/z` is also an algebraic integer.
The first divisibility filter is therefore necessary.

Simple dimensions in a modular category are d-numbers. For any conjugate
roots of a d-number, the valuations at a fixed prime are equal. If a monic
integer polynomial of degree `k` has these conjugates, possibly repeated,
its coefficients satisfy `a_j^k / a_k^j` integral. Thus the same divisibility
condition is necessary for the ambient multiplication characteristic
polynomial, even if that polynomial is a power of the minimal polynomial.
As an additional independent check, every Gram candidate was tested using
its square-free minimal polynomial. The integrality and d-number decisions
agree exactly with the engine's ambient characteristic-polynomial tests.

## Local and global branch coverage

`forced_module_data(R)` reconstructs all anti-invariant representations from
the tensor; no precomputed pattern table is trusted. It selects a fixed
self-dual simple of cubic dimension 2 or 4 only when every module branch has
the negative stabilizer sign. Third indicators are rational because prime 3
is absent from the exponent support. The rotation multiplicity equations
and the bound `nu3 <= H-3` are therefore necessary; for cubic dimension 4
this is precisely the Clifford upper bound 1.

The verifier reconstructs every low induction frame and every allowed second
indicator assignment, then checks each Farkas inequality with exact integer
arithmetic. The general wrapper additionally reconstructs the unrestricted
signed-sphericalization reduction. The mathematical entry points accept only
the tensor and certificate; census labels occur solely in CLI input selection.
The ambient-conductor list is an explicit eligibility restriction, not a
special rule for any census entry.

Reproduce all independent checks:

```bash
python -O research/round2_center/quartic_independent_audit.py
python -O research/round2_center/quartic_phase_check.py
python -O research/round2_center/quartic_pruning_audit.py
```

The same exact field, finite-phase, and d-number arguments apply to the two
multiplicity-eight certificates, whose complete systems were independently
reconstructed in their general replays. Their additional replay commands are:

```bash
python -O research/round2_center/quartic_independent_audit.py R6_8_570 --output research/round2_center/quartic_m8_570_independent_audit_report.json
python -O research/round2_center/quartic_independent_audit.py R6_8_2203 --output research/round2_center/quartic_m8_2203_independent_audit_report.json
```

No further discovery was initiated after these audits. The phase-covariant
Galois-balance proposal is confined to the separate deferred research note.
