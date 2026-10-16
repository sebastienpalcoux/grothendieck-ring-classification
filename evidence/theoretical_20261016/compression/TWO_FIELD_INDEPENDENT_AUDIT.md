# Independent audit: two-field obstruction for four rank-eight rings

Date: 2026-10-16. **Verdict: PASS, unrestricted complex categorification.**

For each of `R8_2_35`, `R8_2_38`, `R8_2_346`, and `R8_2_406`, the Casimir
matrix was independently recomputed directly from `source_tensors.json`
as `B = sum_i N_i N_i^T`. In every case its characteristic polynomial is

    (x-8)^4 (x^2-160x+640) (x^2-32x+128).

The source hashes were checked before this calculation:

| Ring | SHA-256 |
|---|---|
| R8_2_35 | a8d7e8dea9b085e12af44d01fa32ca6d6226ea7f5121929f2301862b9af98758 |
| R8_2_38 | 48dca764c064d7e6b981902c5bb1092e49138eb6353f49b531eb84dccfba3fe4 |
| R8_2_346 | 3948ca735e1c982cee3a46289b7120d8be7395b771577983747e02d6d058860e |
| R8_2_406 | fbd2f625f4e0bf21895e4da72c99eb06517e41e69c04d422ec6a796ccf88bbfd |

The quadratic factors generate `L=Q(sqrt(10))` and `L'=Q(sqrt(2))`.
Their exact compression values, using fundamental discriminants 40 and 8,
are

    Q_L  = 40 (160^2 - 4*640)/640^2 = 9/4,
    Q_L' =  8 ( 32^2 - 4*128)/128^2 = 1/4.

Suppose an arbitrary categorification exists and take its canonical
sphericalization. Let `K` be its spherical dimension field. Every formal
codegree belongs to `K`, by the induced-unit dimension formula. The
positive sign sector contributes the doubled original formal codegrees.
Since a Casimir eigenvalue is `(dim E) f_E` and `dim E` is an integer,
both `L` and `L'` are subfields of `K`. The fields are distinct quadratic
extensions, so `[K:L]>=2`.

Write `e=[K:L]`. Applying the full induced-unit inequality to the
quadratic character of `L`, and retaining the known positive-sector
coordinates, gives

    e Q_L / 4 <= 1.

Here the factor four is precisely the square of the sphericalization's
factor two on formal codegrees. However,

    e Q_L / 4 >= 2*(9/4)/4 = 9/8 > 1.

This contradiction excludes all four rings. There is no assumption of a
pivotal structure on the original category, no Galois pseudo-unitarity
reduction, no central-lift assumption, and no signed-tensor enumeration.
The argument only uses the already audited full induced-unit compression
inequality and the field inclusions forced by the source Casimir.
