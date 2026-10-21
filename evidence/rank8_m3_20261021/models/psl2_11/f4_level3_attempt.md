# Exact F4 level-3 model attempt

The denominator 24 occurring in the quartic candidate dimensions suggested
checking the unitary WZW category of type F4 at level 3. This attempt does
not produce a model. Its global dimension is exactly
`240+96*sqrt(6)`, whereas R8_3_916, R8_3_928, R8_3_941, and R8_3_1348 have
global dimension `144+96*sqrt(2)+80*sqrt(3)+56*sqrt(6)`. Consequently it is
not a Morita source for these rings. This is a limitation of this specific
construction attempt, not a general categorifiability obstruction.

The accompanying script constructs all 48 roots of F4 in Euclidean
coordinates, selects its 24 positive roots, and computes fundamental
weights from their defining coroot pairings. The highest-root comarks
are `(2,3,2,1)`. It enumerates the nine dominant weights of level at most
three and evaluates the quantum Weyl formula

    d(lambda) = product over positive roots alpha of
      sin(pi*(lambda+rho,alpha)/(3+9)) / sin(pi*(rho,alpha)/(3+9)).

Long roots have squared length 2 and the dual Coxeter number is 9. All
arithmetic is exact in `Q(zeta_48)`, reduced modulo
`Phi_48(z)=z^16-z^8+1`; no numerical recognition is used.

| Dynkin labels | Quantum dimension |
|---|---|
| 0000 | 1 |
| 0001 | 3+sqrt(6) |
| 0002 | 4+2 sqrt(6) |
| 0003 | 2+sqrt(6) |
| 0010 | 5+2 sqrt(6) |
| 0011 | 6+2 sqrt(6) |
| 0100 | 3+sqrt(6) |
| 1000 | 2+sqrt(6) |
| 1001 | 4+2 sqrt(6) |

The exact sum of squares gives the claimed global dimension. The saved
receipt includes a nonzero reduced cyclotomic polynomial for the
difference from the candidate dimension. Replay with

    python -O evidence/rank8_m3_20261021/models/psl2_11/f4_level3_attempt.py

The default mode compares the recomputed result to the saved JSON;
`--write` explicitly regenerates it.
