# Rank-seven residual register after twenty-nine general exclusions

The current revision resolves 29 of the 39 previously open cases. The other 10 are listed below, with no existence or exclusion claim. The totals are 4,164 excluded, 27 modeled, and 10 unresolved among 4,201 source tables.

| Family | Count | Remaining IDs |
|---|---:|---|
| Four invertibles, quadratic field Q(sqrt5) | 5 | `R7_4_35`, `R7_4_2053`, `R7_4_2591`, `R7_4_2603`, `R7_4_2665` |
| Two invertibles, quadratic field Q(sqrt3) | 2 | `R7_4_106`, `R7_4_2155` |
| Two invertibles, quadratic field Q(sqrt6) | 1 | `R7_3_146` |
| Integral dimension vectors | 1 | `R7_3_601` |
| Three invertibles and a dimension-three simple | 1 | `R7_3_1022` |

## New general conclusions

| Mechanism | IDs |
|---|---|
| Cyclic module divisibility | `R7_4_1212`, `R7_4_1213`, `R7_4_1438`, `R7_4_1440`, `R7_4_2731` |
| Forced positive signed sphericalization, then dimension block | `R7_3_783`, `R7_3_1015` |
| Full-I(1) compression saturation and a modulo-four contradiction | `R7_3_695` |
| Three-fixed anti-module spectral arguments | `R7_2_116`, `R7_2_261`, `R7_3_364`, `R7_3_938`, `R7_3_970`, `R7_4_2644`, `R7_4_2683` |
| Three-fixed dual-module Gram arguments | `R7_2_11`, `R7_2_205`, `R7_2_275`, `R7_2_287`, `R7_3_387`, `R7_4_2473`, `R7_3_1055` |
| Positive-semidefinite Gram subtraction | `R7_4_776`, `R7_4_927`, `R7_4_2126`, `R7_3_909` |
| C3/V4 Morita reduction and formal-codegree arithmetic | `R7_2_236`, `R7_4_2167`, `R7_4_2716` |

The earlier one-matrix proof for `R7_4_1212` and `R7_4_1213` remains an independent verification; the new divisibility proof handles them directly.

## What was checked on every remaining case

The companion JSON records exact positive dimension vectors, source tensor digests, Casimir polynomials, full-I(1) quadratic obstruction quantities, and every prime-order invertible tested by the cyclic-module lemma. Every dimension vector is verified against all 49 source products. No remaining case violates the directly applicable cyclic-module divisibility condition.

The four- and three-invertible quadratic families have compression quantity below one. The three remaining sqrt3/sqrt6 cases have quantity exactly one; this does not contradict spherical categorifiability, and its sphericalization contribution is only one quarter of the general bound. The remaining integral case has no quadratic Casimir factor detected by this test. Passing these conditions does not construct an associator.

## Further routes and exact limitations

- For the four-invertible families, an equivariantization description would require an actual tensor action, including coherent associativity data. Matching orbit dimensions or a proposed group inversion does not supply that action.
- For the sqrt3/sqrt6 families, compression equality can constrain a hypothetical spherical categorification but does not imply that every categorification is spherical. The positive-signed-lift argument used for the C3 pair has not been established for these tensors.
- For the remaining integral case R7_3_601, induction multiplicities admit solutions to preliminary relaxations. Those relaxations are neither categorifications nor exclusion proofs; a group-theoretical classification cannot be applied without proving its hypothesis.
- The remaining three-invertible ring reduces to an allowable quadratic A4 ring. This based-ring reduction does not reconstruct the module associators needed for an actual rank-seven categorification.

The published status must therefore retain all 10 as unresolved unless a further complete proof or explicit monoidal model is supplied.

## The final C3 case and the limitation of the first relaxation

The first C3 module and Gram equations pass all four original cases R7_2_236, R7_4_2167, R7_4_2716, and R7_3_1022; the historical receipt remains an exact record of that relaxation. The additional categorical Morita argument now excludes the first three. Its first dual has12 invertibles and3 noninvertibles of dimension d with d²=4+md. For m=6, two-dimension divisibility4|m fails. For m=12, a second V4 dual has12 invertibles A4 and12 noninvertibles t=d/2; all possible quadratic rings have formal codegrees outside Q(t), contrary to the general-complex Galois pseudo-unitarity theorem.

Only R7_3_1022 remains in this family. Its second Morita ring is the possible k=4 quadratic A4 ring, realized by the known HI(V4) crossed product with C3. This does not construct the original rank-seven category. In the known realization, both full A4 algebra twists instead give the rank-eight4442 category, so that particular construction route is closed. No uniqueness of arbitrary complex realizations has been proved here, and no exclusion or model is claimed for R7_3_1022.
