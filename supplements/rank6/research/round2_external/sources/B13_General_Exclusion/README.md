# General complex noncategorifiability of B_13

This package proves that the explicit simple, self-dual rank-six fusion ring
of multiplicity thirteen defined in `proof.pdf` and `tensor.json` has no fusion
categorification over the complex numbers. `B_13` is a local label, not a census ID.
The basis is `(1,a,b,c,d,e)` and `N[i][j][k]` is the coefficient of the k-th basis
element in the product of the i-th and j-th basis elements.

## Mathematical argument

Sphericalization forces the dimension field Q(sqrt(5),sqrt(149)). Character
orthogonality and the Casimir bound restrict the global-dimension trace.
Formal-codegree divisibility and the d-number norm–trace condition leave only
Delta = 3725. The two other signed formal codegrees would be the roots of
x^2 - 3721*x + 3725. That polynomial is irreducible and its roots fail the
quadratic d-number condition: 3721^2 is 16 modulo 3725.

No pivotal assumption is placed on the hypothetical category. No associator
search, signed-associativity search, pre-existing exclusion certificate, census,
or online computation is used. The cited categorical inputs are given precisely
in the manuscript. The arithmetic checker is not a proof-assistant formalization
of those categorical inputs.

## Reproduction

Python 3.10 or later, with the standard library only. No installation is needed.

```bash
python verify.py --output verification.json --candidates positive_candidates.csv
python -O verify.py --output verification_optimized.json
python norm_check.py
```

The first two commands check the full tensor (including all 1,296 associativity
equations), the complete character table and formal codegrees, the Casimir trace,
the product integral basis discriminant and residue calculations, all 1,129
integral totally positive candidates in the proved finite box, and the final
quadratic contradiction. Each candidate's norm formula is also checked independently
against a 4-by-4 integer determinant. Checks stay active under `python -O`.
Both verification reports in this package were generated successfully.

The short `norm_check.py` is exactly the complete arithmetic loop printed in the
proof. It reports:

```text
[0, 66, 132, 267, 664]
[(4, 0, 0, 0, 22201)]
```

The sole survivor has theta=sqrt(149), hence Delta=25*149=3725.
`positive_candidates.csv` contains every candidate counted in the first row,
its norm, and the result of the norm–trace divisibility test.

## Contents

`proof.tex` and `proof.pdf` contain the complete mathematical proof.
`verify.py` is the full independent finite checker; `norm_check.py` is the short
printed arithmetic check. `tensor.json` fixes the entire multiplication tensor.
The CSV and two JSON reports record the actual checks. `SHA256SUMS` records the
file hashes, excluding the manifest itself.

To compile the manuscript:

```bash
pdflatex -interaction=nonstopmode -halt-on-error proof.tex
pdflatex -interaction=nonstopmode -halt-on-error proof.tex
```
