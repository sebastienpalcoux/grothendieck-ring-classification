# Complex central products and fourth moments for R6_4_155

**Categorical status: unresolved. No new exclusion or model is allocated.**

The tensor has invertible group `C2 x C2`, two dual noninvertibles of
Frobenius–Perron dimension `4+3 sqrt(2)`, and global dimension
`72+48 sqrt(2)` (minimal polynomial `t^2-144t+576`). This is Meng–Yu's
`R′(4)`, identified by a complete tensor comparison in the preceding round.
Their primary source is https://arxiv.org/abs/2608.06064; it leaves this
family open. The full source consulted in the preceding round has the
checksum recorded in `research/round3/models/literature_audit.md`.

## New uniform necessary constraints

`software/round4_155.py` reconstructs all constraints from the input tensor:

1. Complex low Verlinde coefficients, using the actual low-object duality,
   and nonnegative integral restriction-product decompositions.
2. Fourth spectral moments, which equal sums of squares of fusion
   multiplicities; integer-square tangent bounds connect these moments
   to the first product counts. The cutoff is explicit and configurable.
3. When the forgetful kernel on central invertibles is trivial, enumeration
   of its possible pointed image and the resulting restriction-count
   identities. Involutory lifts with second indicator `-1` act freely and
   change twist traces by multiplication with powers of `+i` or `-i`;
   integral matching variables impose the resulting pairings.

Proofs and scope are in `papers/chapters/round4_155.tex`.
These are necessary systems, and their surviving points are not modular
data, fusion rings for centers, or categorifications.

## Strongest exact survivor

`quartic_exact_primal.json` contains a nonnegative **integral** point of
7,764 equations in 9,982 variables, at conductor 8 and height 3, including
fourth moments with cuts `0 <= k < min(B,8)` and the pointed-image branch
`{0,3}`. Its conditional central-object count is 36.

`quartic_exact_replay_optimized.json` rechecks every equation exactly under
`python -O`, with `linprog` and `milp` disabled. The tensor-parametric entry
point is `round4_155.verify_primal(R, certificate)`.

`exact_primal_certificates.json` contains eight additional exact integral
survivors: conductor 8 at heights 3 and 6; conductor 24 at height 3; and
all five pointed-image subgroups in the conductor-eight height-three
relaxation. Their ranks are respectively 46, 48, 49, and 48/36/46/46/36.
`exact_primal_replay_optimized.json` verifies all eight without optimizers.
The height-six solution has 2,674 equations and 4,295 variables.

The stronger fourth-moment test rejects some earlier fixed numerical
branches, but those solver outcomes are not exact exclusion certificates
and are not counted as categorical progress. The unrestricted fourth-moment
MILP exhausted its 120-second optimization budget without a primal point;
this is recorded as inconclusive. Fixing existing trace counts then found
the exact rank-36 survivor above.

## General-scope reduction

`reduction.json` reconstructs 40 signed quotients in three sign orbits,
with one original-gauge orbit and eight nongauge character rejections.
The accepted signed-reduction theorem therefore shows that every
categorification would be spherical and would have a pseudo-unitary Galois
conjugate. This is a reduction theorem, not an exclusion.

## Complete applicability/control coverage

Each of the following scans has exactly 64 records, comprising all ten
input frontier rings and all 54 realized controls.

| Domain | Exact rational survival | Numerical survival | Ineligible | Budget incomplete |
|---|---:|---:|---:|---:|
| Complex low products | 18 | 2 | 29 | 15 |
| Fourth moments, cutoff 8 | 14 | 1 | 29 | 20 |
| Pointed-image transport | 5 | 0 | 41 | 18 |

Files: `scan_controls.json`, `scan_quartic_controls.json`, and
`scan_pointed_controls.json`. These bounded scans test eligible systems;
they do not infer exclusion from a missing primal point. Exact rational
survival in a control scan checks every equation of the computed point,
but the saved standalone integral certificates above are the independently
replayable survivor evidence for the target. Its short scan timeouts are
superseded by the dedicated deeper follow-ups.

An interrupted worker pool in the quartic scan was resumed for precisely
its eight missing inputs by `finish_scans.py`, using fresh subprocesses
and a hard wall-clock limit. The final 64-record receipt is complete. The
initial conductor-24 ambient search was stopped once a strictly stronger
exact surviving branch had been obtained; its partial log is not a
complete enumeration or an exclusion certificate.

## Reproduction

From the package root:

```sh
python -O research/round4/m4_155/replay_primal.py
python -O research/round4/m4_155/freeze_quartic.py
python -O research/round4/m4_155/mutation_controls.py
python research/round4/m4_155/scan_controls.py
python research/round4/m4_155/scan_quartic_controls.py
python research/round4/m4_155/scan_pointed_controls.py
```

Discovery scripts use explicit per-job budgets of at most 840 seconds.
No optimizer result is used as a proof of nonexistence.
