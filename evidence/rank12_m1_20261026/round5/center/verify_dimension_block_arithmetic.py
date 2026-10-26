#!/usr/bin/env python3
"""Exact arithmetic for the independently audited dimension-block obstruction.

The categorical and operator-norm proofs are in the companion Markdown note.
This script is only an exact check of their finite scalar identities.
"""
import json
from pathlib import Path
import sympy as s


def need(test, message):
    if not test:
        raise ValueError(message)


r = s.sqrt(10)
d = 3 + r
D, Dp = 120 + 36*r, 120 - 36*r
z = (-1+s.sqrt(3)*s.I)/2
need(s.simplify(D*Dp) == 1440, "dimension norm")
need(s.simplify(D/Dp-d**2) == 0, "conjugate simple dimension")
need(s.simplify((1/D-1/Dp)**2) == s.Rational(1, 40), "exact saturation")
need(s.simplify((3/D-3/Dp)**2) == s.Rational(9, 40), "Tannakian quotient violation")
cases = []
for a in (1, 2):
    S = s.Matrix(3, 3, lambda i, j: z**(2*a*i*j))/s.sqrt(3)
    T = s.diag(1, z**a, z**a)
    need(all(s.simplify(v) == 0 for v in S*S.conjugate().T-s.eye(3)),
         "Fourier unitarity")
    for n in (1, 2):
        vector = (S*T**n*S.conjugate().T*s.Matrix([1, 0, 0])).applyfunc(s.simplify)
        expected = s.Matrix([(1+2*z**(a*n))/3,
                             (1-z**(a*n))/3,
                             (1-z**(a*n))/3])
        need(all(s.simplify(v) == 0 for v in vector-expected), "lower-unipotent formula")
        need(vector[1] != 0 and vector[2] != 0, "nonzero vacuum dispersion")
        cases.append(dict(metric_parameter=a, n_mod3=n,
                          vector=[str(v) for v in vector]))
codegree = s.simplify(D**2/2/(4+12*d)**2)
need(codegree == s.Rational(9, 2), "secondary R623 factor restriction")
report = dict(status="PASS", dimension_norm=1440,
              saturation="1/40", Tannakian_quotient_violation="9/40 > 1/40",
              metric_C3_lower_unipotent_cases=cases,
              R623_secondary_formal_codegree="9/2", optimizer_used=False)
Path(__file__).with_name("dimension_block_independent_arithmetic.json").write_text(
    json.dumps(report, indent=2)+"\n")
print(json.dumps(report))
