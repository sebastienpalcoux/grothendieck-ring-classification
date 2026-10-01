# Indicator and rotation audit: precise scope

Both rings remain unresolved. The checks below impose necessary conditions;
passing them does not provide associators or a category. R155 now has a complete
necessary modular candidate; R1660 still has partial center data.
They use the established spherical/pseudo-unitary reductions, without assuming
unitarity. This inventory does not claim that all indicators have been exhausted.

## R6_4_155

Only profile 296 remains. Its rank-52 center has a forced twist spectrum and
exponent 24; see the [twist proof](R6_4_155/forced_twists.md),
[symbolic verifier](R6_4_155/verify_forced_twists.py), and
[receipt](R6_4_155/forced_twists_certificate.json).
The forcing argument uses the modular second indicators of the two known low
simples A,L in the rank-26 semion centralizer, and the original X fourth rotation.
It does not assume a complete fusion table for that centralizer.

The round-nine [low-data verifier](R6_4_155/verify_low_checks.py) and its
[receipt](R6_4_155/low_checks_certificate.json) check:

| Check | Exact domain | Result |
|---|---|---|
| Generalized rotations | A,L; orders 2–24; all 36 pairs of the six known low S rows | 1656 blocks pass, with every cyclic eigenvalue multiplicity integral and nonnegative |
| Degree-one normalization | The same two objects and 36 row pairs | 72 identities pass, including target-twist and duality conventions |
| Anderson–Moore–Vafa equations | Every ordered quadruple from the five known fusion matrices for 1,h,A,hA,L | 625 equations pass |
| Character duality | The two distinct nonreal character rows and their associated central objects | Dual pairs (16,17) and (18,19) are forced in the retained ordering |

The generalized rotations include the correction for nontrivial target twist.
At that historical stage, the duality result left four patterns, with 20, 24,
or 28 self-dual simples in the full center. The complete reconstruction now
forces twenty (ten in the rank-26 centralizer). Spherical duality uses `nu_n(V*)=nu_n(V)`, without complex
conjugation. These historical checks used only the then-known rows and fusion matrices.
They have now been supplemented by the complete exact reconstruction: all
26³ Verlinde coefficients are nonnegative integers (maximum 9), all 456,976
ordered rank-26 Vafa equations pass, and all 676 restriction products agree.
The completed rank-26 candidate passes 182 ordinary cyclic spectra at orders
2, 3, 4, 6, 8, 12, 24, all 17,576 generalized second-indicator blocks, and
all 17,576 degree-one identities. The full rank-52 center passes 7,176
generalized cyclic spectra (52 central targets, six original simples, orders
2–24) and 312 degree-one normalization identities. See the
[new research](new_research/README.md) for exact matrices, conventions and replays.

## R6_8_1660

The prior [fermion and weighted-FS reduction](R6_8_1660/fermion_profiles/README.md)
left 1727 of 1764 labelled profiles. Its
[verifier](R6_8_1660/fermion_profiles/verify_fermion_profiles.py) and
[receipt](R6_8_1660/fermion_profiles/fermion_profiles_certificate.json)
cover all those input profiles, not merely a selected numerical witness.

The [new spin-profile reduction](R6_8_1660/spin_profiles/README.md),
[verifier](R6_8_1660/spin_profiles/verify_spin_profiles.py), and
[receipt](R6_8_1660/spin_profiles/spin_profiles_certificate.json) remove another
57 profiles: 18 by involution parity and 39 by the spin/field condition.
That stage left branch counts 164, 753, 753, totaling **1670**. The subsequent
signed Galois–fermion four-divisibility test removes raw profile 133 in low
frame zero, leaving **1669**, in branches **163, 753, 753**.
The spin condition combines a homogeneous-packet Anderson–Moore–Vafa equation,
its mod-3 specialization, and a sixteenth-indicator field constraint.
The replay checks rejected charge branches by a second exact recursion;
it uses no optimizer or full center fusion reconstruction.

The [R1660 manuscript chapter](../../papers/chapters/frontier_1660.tex) proves
all-order statements, separately from the finite profile computations:

- The neutral relative center is a C2-equivariantization of C. Its coherent
  tensor involution exchanges X and gX, so their indicators and entire cyclic
  rotation representations agree at every positive order.
- Writing Y for the relative-center lift of sigma X, every odd rotation on
  `Hom_C(1,(sigma X)^n)` is two copies of the rotation on `Hom_E(1,Y^n)`.
  Thus every such eigenvalue multiplicity is even, for every odd n.
- The associated odd identities are `2nu_n(Y)=nu_n(sigma X)` and
  `2nu_n(S)=nu_n(X)+nu_n(gX)`. These are derived from Morita invariance and
  cyclotomic field separation, not from a general claim that forgetful functors
  preserve indicators.

## Limits of the surviving tests

Exploratory higher-order ordinary and generalized rotation checks also used a
single global arithmetic witness. Its exact passes do not establish twist,
indicator, or modular-data feasibility for every remaining profile, and are not
used as such in the profile certificates. In particular, a global low-frame-zero
witness cannot settle a new phase constraint in low frame one.

For R155 the completed data now cover all central targets in the finite scopes
stated above; for R1660 high-target checks remain partial. Indicator periodicity
does not by itself certify every cyclic eigenspace condition at arbitrarily
large tensor order. All ordered rank-26 Vafa equations have been checked for
R155. R1660 still uses partial fusion data and aggregated Vafa identities, so
its surviving profiles must not be treated as complete Vafa solutions.
