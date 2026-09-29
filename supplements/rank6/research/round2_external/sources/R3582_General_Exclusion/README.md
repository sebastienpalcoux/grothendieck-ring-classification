# General noncategorifiability of R6_7_3582

## Result

The rank-six, multiplicity-seven fusion ring with the full tensor in `ring.json`
has no categorification as a fusion category over the complex numbers. No
pivotal, spherical, braided, unitary, or pseudo-unitary hypothesis is imposed on
the hypothetical category.

The proof has two parts:

1. A theoretical sphericalization argument uses ramification at 2 and a sharp
   Casimir trace comparison to show that every hypothetical categorification
   would have a pseudo-unitary Galois conjugate.
2. An independent central-induction obstruction excludes pseudo-unitarity.
   Two small, exhaustively bounded integer enumerations leave one possible
   Gram pattern. The first twist identity then requires
   `-18 - 6*sqrt(226)` to be a sum of 434 roots of unity, whereas a quadratic
   Gauss-sum estimate requires at least 1344.

No previous pseudo-unitary exclusion certificate is imported.

## Contents

- `proof.pdf`: full mathematical proof, including every enumeration bound.
- `proof.tex`: editable LaTeX source; bibliography is included in the file.
- `ring.json`: full ordered multiplication tensor in the basis `(1,a,b,c,d,e)`.
- `verify.py`: independent exact arithmetic and exhaustive-enumeration verifier.
- `verification.json`: actual verification report from standard Python.
- `verification_optimized.json`: actual verification report from optimized Python.
- `requirements.txt`: tested Python dependency.
- `SHA256SUMS.txt`: hashes of the supplied proof, input, code, and reports.

## Reproduce the exact checks

Use Python 3.10 or newer. From this directory:

```bash
python -m pip install -r requirements.txt
python verify.py --output verification.json
python -O verify.py --output verification_optimized.json
```

Both commands must print `PASS`. The verifier uses explicit exception-raising
checks, not Python `assert`, so optimization does not disable the checks.
The reports include a hash of the input tensor, the SymPy version, all surviving
columns, and the complete finite-stage counts. Timing fields vary by machine.
Re-running a report changes its hash; the supplied manifest describes the
original bundled files.

The low-column stage checks 32 individual deviations, 59 bounded quadruples,
11 modular-reciprocity survivors, and 3 positive-semidefinite residuals.
The three high-column branches have 377/4483/377 bounded candidates,
48/236/48 Gram-compatible candidates, and 2/18/2 integral-quotient survivors.

## Build the PDF

```bash
pdflatex -halt-on-error proof.tex
pdflatex -halt-on-error proof.tex
```

A standard TeX installation with AMS packages, Latin Modern, microtype,
booktabs, geometry, and hyperref is sufficient. No external bibliography,
images, fonts, or data files are needed for compilation.

## Verification scope

The code certifies the finite ring arithmetic and both exhaustive enumerations.
The sphericalization, local-field, and all-orders Gauss-sum arguments are proved
in the manuscript and are not replaced by numerical experiments. This is not
a Lean formalization of fusion-category theory. No pentagon solver or floating-
point optimizer is used. No conclusion is claimed about other fusion rings or
about the minimum possible rank of a non-pivotal fusion category.

No external repository has been modified by preparing this package.
