# R567: a complete central integer-Gram and cubic obstruction

There is no complex fusion category with based ring `R8_3_567`.
The independently certified Galois-pseudo-unitary gate reduces general
existence to pseudo-unitary existence. The ring has trivial center
invertibles, and the integral-center-subcategory lemma therefore
forbids every nonunit integral-dimensional central simple. This proof
uses the original rank-eight ring, with no Morita-partner assumption.

## Complete finite domain

The exact source and complete character table are reconstructed by
`source.py`; the full tensor SHA256 is stored in `source.json`.
The complex algebra has four scalar representations and one M2 block.
The scalar characters split in Q(√3,i), which is used exactly; none of
the complex characters is omitted. Character orthogonality is checked.

The formal codegrees, with representation dimensions, are
`(D,1), (D′,1), (12,1), (12,1), (3,2)`, where
D=48+24√3 and D′=48−24√3. Complete low-frame enumeration and full
S symmetry leave one frame, with two assignments of the complex
conjugate characters:

```
(1,0,0,0,0,0,0,0)
(1,0,0,1,1,0,0,0)
(1,0,0,0,1,0,0,0)
(1,0,0,1,0,0,0,0)
(2,1,1,2,2,0,0,0)
```

Each column represents one central simple. The last has multiplicity
two in I(1), and is still counted once in the sum over central simples.
This distinction is explicit in both the arithmetic and the formula.

There are exactly45 high restriction vectors, obtained using the
residual-Gram bound, positivity, the central dimension d-number
condition (Ostrik arXiv:0810.3242, Theorem1.8), and algebraic
integrality of D/d_Z (ENO Proposition3.3 for the modular center).
For a distinguished central simple A_E, the normalized character row
is

S(A_E,Z) = D/(f_E dim(E)) · χ_E(FZ).

Consequently S(A_E,Z)/d_Z is an eigenvalue of an integral fusion matrix
and must be an algebraic integer. The full exact character table
excludes nine high vectors by this condition. Two further vectors
have integral dimension and are excluded by the integral-center lemma.
There are34 allowed vectors.

Every allowed high vector has the form `(u,u,p,q,w,w,w)`. On coordinates
`(u,w,p,q)` the full residual7×7Gram is exactly equivalent to

```
[4 0 4 4]
[0 4 6 6]
[4 6 42 31]
[4 6 31 42]
```

`gram.py` exhausts nonnegative integer multiplicities by two independent
algorithms. They agree on1,071 solutions and check all49 original Gram
entries. Central duality swaps the restriction coordinates p and q;
the corresponding multiplicities must agree. This leaves exactly155
patterns. No bound is imposed on the number of central simples beyond
the exact Gram-derived finite bounds.

## One cubic coefficient excludes the entire domain

Let A be the distinguished simple corresponding to the scalar
conjugate-FP character χ and codegree D′. It is self-dual, since it is
the unique distinguished simple of its dimension D/D′=7+4√3 in the
self-dual I(1). The unnormalized center S matrix has S(1,Z)=d_Z and
center global dimension D². Deshpande's equation(39), inverted using
character orthogonality, and Verlinde give

N(A,A;A) = D/(D′)³ · Σ_Z χ(FZ)³/d_Z.

The complete155 patterns give exactly84 values equal to1/3 and71
values equal to4/3. Every value contradicts integrality of a fusion
coefficient. This excludes pseudo-unitary existence and, through the
certified gate, general complex existence.

## Canonical exact replay

```
python evidence/rank8_frontier_20261021/r567_centerless_integer/verlinde_exclusion.py
python -O evidence/rank8_frontier_20261021/r567_centerless_integer/verlinde_exclusion.py
```

The verifier reconstructs the complete source/domain, both integer
Gram enumerations and all155 coefficients. It compares the scalar
D/(D′)³ expression with the full S-normalized expression on every
restriction. An actual Fibonacci-center control gives its known
coefficient1. No numerical optimizer is used in this exclusion.

The separate `rotation_spectral.py` receipt preserves the preceding
height-six rotation test with all eleven high-column cuts. Its eight
indicator branches have seven exact dual certificates and one exact
rational primal witness. These relaxations alone do not exclude the
ring; the complete integer cubic step supplies the contradiction.

## Scope dependencies and primary sources

- `noncommutative_followup/additional_scope_gates.py/.json`: general
  Galois-pseudo-unitary gate for R567.
- `structural_models/known_model_routes.py/.json`: trivial center
  invertibles from the original ring's adjoint closure and invertibles.
- `review/INTEGRAL_CENTER_SUBCATEGORY.md` and its exact checker: the
  no-integral-center lemma; ENO Proposition8.15 and the solvability
  theorem in arXiv:0809.3031, Theorem1.6 and Proposition4.5(iv).
- V. Ostrik, arXiv:1309.4822, Theorem2.13: induced-unit constituents;
  arXiv:0810.3242, Theorem1.8: dimension d-numbers.
- T. Deshpande, arXiv:1611.04486, equation(39): distinguished S rows.
- P. Etingof, D. Nikshych, V. Ostrik, arXiv:math/0203060,
  Proposition3.3: D/d_Z algebraic integrality in the modular center.
