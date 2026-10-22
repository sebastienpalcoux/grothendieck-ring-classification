# Independent audit of the fixed-point phase extension

Result: **PASS**, with the limited conclusion of a rational relative-phase
extension of the separately verified integer center relaxation. This is not
an actual twist assignment, modular datum, or categorification.

The audit read `independent/verify_phase_extension.py` and replayed its exact
checker. It then recomputed the indicator moments directly, without calling
its `build_system` function. The 37 relative-trace types also agree exactly
with the pre-existing generic `trace_types(2,[2,5,7],4)` calculation in
`evidence/theoretical_20261016/rank7/gram_support/higher_traces.py`.

## Source and label binding

The phase certificate hashes the exact integer witness, its own verifier,
the third-indicator verifier, and the canonical tensor. It agrees with the
integer witness's full-system metadata digest. Its seven distinguished
restrictions and ten positive high restrictions exhaust, without duplicate
indices, all 17 `restriction_bindings` in `center/integer_witness.json`.
Every vector and positive integral weight matches. The complete center
verifier checks these bindings against the source-reconstructed matrix;
the phase verifier intentionally requires that separate replay.

The audited hashes are:

| File | SHA-256 |
|---|---|
| `independent/verify_phase_extension.py` | `cf239bd880c2e085098e2f03353930bf87f7f9a71fa5e648cecdd899498f7e24` |
| `independent/phase_certificate.json` | `520a658edc047251e9c4a4eba7c1a06881436049710d8236d8d0ddf72d173ae0` |
| `center/integer_witness.json` | `ed78c37a952080972e3c14c0b4975c5aaeb6ddf33ec578d62065ccbf85904fcd` |

## Equation normalization

Write `r=sqrt(2)`, `D=700+490r`, and `z(v)=sum_i v_i d_i`. A high phase
weight `y_(v,t)` contributes `y_(v,t) v_i z(v) t_n` to the degree-n
indicator numerator. Each distinguished restriction has twist 1, so its
contribution is `v_i z(v)`. The coefficientwise equation is exactly

`sum_low v_i z(v) + sum_(high,t) y_(v,t) v_i z(v) t_n = D nu_n(X_i)`.

Direct exact arithmetic verified all 56 rational/radical coordinates for
seven objects and degrees 1 through 4. The targets in degrees 1, 2, and 3
are respectively 0, 1, and 2. For degree 4, rotation weights `(a,b,c)`
correspond to normalized real traces `(-1,0,1)`, so `nu_4=c-a`.
The verifier's signs therefore give `high + D(a-c) = -low`, as required.

The additional fourth-rotation identities were independently checked:

- `a+b+c = dim Hom(1,X_i^4) = sum_k (N_ii^k)^2`;
- `a-b+c = tr(E_4^2) = nu_2(X_i^2) = sum_k N_ii^k`, using all second indicators equal to 1.

The unit's moment equations are automatic: the fixed central unit and the
seven distinguished restrictions have total dimension D and twist 1;
all high restrictions have unit coefficient zero.

Thus the 80 rows are precisely ten fixed-high-mass equations, 42 moment
coordinates for degrees 1–3, fourteen fourth-rotation identities, and
fourteen fourth-moment coordinates. The exact solution has 40 positive
entries among 391 variables. Rational phase and rotation weights remain
relaxation variables; the integer high totals alone do not turn them into
actual root-of-unity multiplicities.

## Replay

Run the two accepted verifiers together:

```
python evidence/r3472_focus_20261022/center/rational_witness.py
python evidence/r3472_focus_20261022/independent/verify_phase_extension.py
```

The first reconstructs the complete 3347-row center system and verifies
both base witnesses and their restriction labels. The second reconstructs
and verifies all 80 additional phase equations without rebuilding that
large matrix.
