# Exact full center compatibility for R6_3_215

The strongest verified result in this directory is a **full modular datum and
positive based-ring homomorphism** from the center of the cyclic-eight
Generalized Haagerup de-equivariantization to `R6_3_215`. No tensor functor,
commutative algebra multiplication, or categorification of R6_3_215 is asserted.

The source is Pinhas Grossman and Masaki Izumi, *Drinfeld centers of fusion
categories arising from generalized Haagerup subfactors*, Quantum Topology 13
(2022), 593–668, Theorem 6.8 with m=2 and Example 6.10,
https://ems.press/content/serial-article-files/36923.

## Reproduce the complete exact check

From the release root:

```bash
python research/center_continuation/exact_cyclic8_center.py
python -O research/center_continuation/exact_cyclic8_center.py
python research/center_continuation/mutation_controls.py
```

The checker is read-only by default. `--write` regenerates the two frozen JSON
files after every check passes. Arithmetic is in Z[x]/Phi_136(x), with all S
entries having denominator 136. The checker verifies:

* The exact source labels, nonnegative integral table F, its unit, and all 22 dimension equations.
* All 10,648 Verlinde spectral equations, with an integer fusion tensor.
* Symmetry, S²=I, and STS=T⁻¹ST⁻¹.
* Unit, duality, and full associativity of the rank-22 fusion tensor.
* All 2,904 coefficient equations for the displayed restriction ring map.
* Second Frobenius–Schur indicator +1 for each of the 22 central simples.

`cyclic8_center_tensor.json` contains labels, the full rank-22 tensor and the
22-by-6 restriction matrix. `cyclic8_modular_data.json` contains the exact S
polynomials and the T exponents for zeta_136. The integer arithmetic checks enforce explicit coefficient bounds: field operations
stay below 2^57 and matrix/indicator sums below 2^39, so int64 arithmetic is exact.
Four negative controls reject the zero map, a missing row, a wrong label and a wrong
unit, including under Python optimization.

The source formulas are implemented
in the checker itself, so the S file is not trusted without reconstruction.

## Additional deductions and scope

`aggregate_twist.py` reconstructs the partial S rows and all low-low balancing
identities from the inherited low-product certificate. The high restriction
classes have sizes (4,8,4). Their twist sums are respectively
0, -(1+sqrt(17))/2, and -4; their squared-twist sums are
0, -(1+sqrt(17))/2, and +4. Hence all four objects in the last type have twist
-1, and the first four twists form a rotated regular fourth-root orbit.
The exact known completion chooses the four primitive eighth roots.

`congruence_compression.py` constructs the universal compression eSe for the
finite groups PSL_2(Z/4) and PSL_2(Z/8). Its spectra are respectively
{1,-1/2,0} and {1,-1/2,0,+sqrt(2)/4,-sqrt(2)/4}.
These are auxiliary experiments, not a general exclusion certificate.

Matching the Asaeda–Haagerup global dimension is insufficient: that center has
different twists. Grossman–Izumi–Snyder's one-sigma argument excludes a specific
Morita configuration, not an arbitrary fusion category having R6_3_215 as its
Grothendieck ring. Similarly, agreement with the cyclic-eight center datum does
not prove that the proposed rank-six Lagrangian algebra exists.
