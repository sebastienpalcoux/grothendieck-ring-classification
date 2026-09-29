# Second-round higher-multiplicity continuation

The new ramification/formal-codegree criterion excludes **R6_7_3812,
R6_8_6234, and R6_8_6509 over C without additional categorical hypotheses**.
The canonical proof is [ramification_proof.md](ramification_proof.md).
The canonical records are the corresponding `*_general.json` files;
`new_ramified_signed.verify(R,c)` reconstructs every finite hypothesis from
the full tensor and checks the trace contradiction.

The final certificates require neither a signed-table enumeration nor a
pseudo-unitary certificate. All original codegrees enter the exact
integrality conditions. A rational codegree of 15 forces the sum of squares
of the irrational dimension coefficients to be at least 15, while the
Casimir trace permits less than six.

The frozen baseline is 40 residuals, including 39 at multiplicities 4–8.
`apply_ramification.py` applies the criterion uniformly to this fixed list,
without reading a changing residual list or modifying any decisions. It
also supplies an independent field-containment exclusion of R6_8_6940,
already covered by the new biquadratic criterion, and a finite signed
reduction for R6_7_3582, covered by the independently imported general
proof. All other higher inputs fail the checked hypotheses; no conclusion
is drawn from that failure.

Reproduction:

```sh
python research/round2_higher/apply_ramification.py
python research/round2_higher/verify_ramified.py --audit
python -O research/round2_higher/verify_ramified.py --audit
```

The audit checks all 54 existing positive controls, regenerates each of the
three new proofs after a nontrivial basis permutation, and rejects six
certificate corruptions plus a corrupted tensor. Explicit `require`
checks remain active in optimized Python.

`spherical_character_profiles.json` retains the complete initial character
profile scan. The optional `new_signed_csp.py/.cpp` is a discovery tool,
independent of the final three proofs. It was compared exactly against the
original signed backend on R6_3_215 (185 gauge-normalized tables).
Unrestricted 60-second trials on R6_7_3812 were incomplete; no exclusion
uses those trials. Once the theoretical trace bound was imposed, both
backends agreed on the complete remaining finite domain. That longer
route was superseded by the direct codegree-15 trace contradiction.

## All-orders Gauss continuation: R6_8_6520

`new_gauss_family.py` now excludes the remaining parameter-seven member of
the dense rank-six family in the pseudo-unitary scope. Combined with the
independent unrestricted signed trace-ideal reduction, this is a **general
complex-fusion-category exclusion of R6_8_6520**. The complete wrapper is
`../round2_external/R6_8_6520_general.json`; its pseudo-unitary component is
`R6_8_6520_pseudo.json`. The standalone proof is
`../../papers/chapters/gauss_family.tex`.

The verifier recovers the parameter and basis ordering from the tensor.
It exhausts all low central columns (32 deviations, 59 bounded quadruples,
11 reciprocal lists, three positive-semidefinite branches) and every high
column. The high-stage counts are `(511,58,1)`, `(6147,282,9)`, and
`(511,58,1)`. Two branches fail a rank condition. In the middle branch,
exact Gram identities force four cross-column types twice each and 590
uniform columns. The first twist moment would express
`-(49+7*sqrt(1229))/2` as a sum of 590 roots of unity, whereas the primitive
quadratic Gauss bound requires at least 4298. This bound covers roots of
**all** orders.

`verify_gauss_family.py` and both `gauss_verification*.json` reports record
normal and optimized-Python replay, all 54 realized controls, a tensor
relabelling, seven corruption rejections, and application to all 40 frozen
continuation inputs. Only R6_7_3582 and R6_8_6520 match the tensor family;
both pass the new pseudo-unitary exclusion. `explore_6520.py` and
`R6_8_6520_low_high.json` are the initial discovery computation; the
self-contained software module and canonical certificate supersede them.

The additional all-census scan in `gauss_census_application.json` checks all
16,612 tensors. It identifies exactly one family member at each multiplicity
4–8: R6_4_803, R6_5_1500, R6_6_2554, R6_7_3582, and R6_8_6520. All five
fail the new Gauss necessary criterion. The respective forced root counts
are 110, 194, 302, 434, 590, versus lower bounds 342, 400, 1440, 1344, 4298.
The first three were already excluded and are independent confirmations.
