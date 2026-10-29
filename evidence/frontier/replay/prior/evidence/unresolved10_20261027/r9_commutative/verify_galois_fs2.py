"""Exact, short checks for the new zero-shift Galois/FS2 obstruction.

This verifies the stated finite inputs, not the categorical pairing theorem.
Explicit exceptions remain enabled under python -O.
"""
import hashlib
import itertools
import json
from pathlib import Path
import runpy

import sympy as s

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def check(condition, label):
    if not condition:
        raise ValueError(label)


def eq(a, b):
    return s.expand(a-b) == 0


G = list(itertools.product(range(2), repeat=3))
Q = list(itertools.product(range(2), repeat=2))


def mul(a, b):
    x, y, n = a
    u, v, m = b
    if m:
        x, y = y, x
    return (x ^ u, y ^ v, n ^ m)


def quotient(a):
    x, y, n = a
    return (x ^ y, n)


def w(a, b, c, t):
    x, y, n = a
    u, v, m = b
    ell = c[2]
    xp, yp = (y, x) if m else (x, y)
    return (ell*(3*m*(x ^ y)+xp*u+yp*v+2*yp*u)+2*t*n*m*ell) % 4


N = [[[0]*12 for _ in range(12)] for _ in range(12)]
for i, a in enumerate(G):
    for j, b in enumerate(G):
        N[i][j][G.index(mul(a, b))] = 1
for i, a in enumerate(G):
    aq = quotient(a)
    for j, q in enumerate(Q):
        r = (aq[0] ^ q[0], aq[1] ^ q[1])
        N[i][8+j][8+Q.index(r)] = 1
        N[8+j][i][8+Q.index(r)] = 1
for i, p in enumerate(Q):
    for j, q in enumerate(Q):
        r = (p[0] ^ q[0], p[1] ^ q[1])
        for k, g in enumerate(G):
            N[8+i][8+j][k] = int(quotient(g) == r)
        for k in range(8, 12):
            N[8+i][8+j][k] = 2
unit = G.index((0, 0, 0))
dual = [next(j for j in range(12) if N[i][j][unit]) for i in range(12)]
check(dual[8:] == [8, 9, 10, 11], "zero-shift noninvertibles selfdual")

rt = s.sqrt(2)
d, dc = 4+3*rt, 4-3*rt
D, Dc = 144+96*rt, 144-96*rt
scalar_reps = []
for a, b in Q:
    roots = (d, dc) if (a, b) == (0, 0) else (rt, -rt)
    psi = lambda q: (-1)**(a*q[0]+b*q[1])
    for t in roots:
        values = [s.Integer(psi(quotient(g))) for g in G]
        values += [t*psi(q) for q in Q]
        f = s.expand(sum(values[i]*values[dual[i]] for i in range(12)))
        expected_f = (D if t == d else Dc) if (a, b) == (0, 0) else s.Integer(16)
        check(eq(f, expected_f), "scalar formal codegree")
        for i in range(12):
            for j in range(12):
                check(eq(values[i]*values[j],
                         sum(N[i][j][k]*values[k] for k in range(12))),
                      "scalar representation multiplication")
        v = s.expand(1+sum(values[8:]))
        sigma_f = f.xreplace({rt: -rt})
        check(eq(v*sigma_f, f), "Galois-unit scalar on scalar representation")
        scalar_reps.append({"a": a, "b": b, "t": str(t), "f": str(f), "v": str(v)})

P = s.diag(1, -1)
S = s.Matrix([[0, 1], [1, 0]])
matrices = [S**n * P**x * (-P)**y for x, y, n in G]
matrices += [s.zeros(2) for _ in Q]
for i in range(12):
    for j in range(12):
        rhs = sum((N[i][j][k]*matrices[k] for k in range(12)), s.zeros(2))
        check(matrices[i]*matrices[j] == rhs, "two-dimensional representation")
formal_matrix = sum((s.trace(matrices[i])*matrices[dual[i]]
                     for i in range(12)), s.zeros(2))
check(formal_matrix == 4*s.eye(2), "two-dimensional formal codegree is 4")
check(s.eye(2)+sum(matrices[8:], s.zeros(2)) == s.eye(2),
      "Galois-unit scalar on two-dimensional representation")
check(8*1**2+2**2 == 12, "complete irreducible dimensions")
central_dimensions = [1, s.simplify(D/Dc), D/16, D/4]
check(len(set(map(str, map(s.expand, central_dimensions)))) == 4,
      "Galois object dimension distinct in I(1)")
check(eq(s.expand((1+4*d)*Dc), D), "Galois object dimension")

pointed = {}
for t in (0, 1):
    indicators = []
    for g in G:
        if mul(g, g) != (0, 0, 0):
            indicators.append(0)
        else:
            exponent = w(g, g, g, t)
            check(exponent in (0, 2), "involution cocycle sign")
            indicators.append(1 if exponent == 0 else -1)
    epsilon = (-1)**t
    check(sum(indicators) == 4+2*epsilon, "TY/pointed indicator cancellation")
    pointed[str(epsilon)] = {"indicators": indicators,
                            "total": sum(indicators), "TY_total": 4+2*epsilon}

TENSORS = runpy.run_path(str(ROOT / "data/current_remaining_cases.py"))["TENSORS"]
expected = json.loads((HERE / "source_checks.json").read_text())
sources = {}
for rid in ("R9_2_137", "R9_2_1607", "R9_2_1976"):
    n = TENSORS[rid]
    digest = hashlib.sha256(json.dumps(n, separators=(",", ":")).encode()).hexdigest()
    check(digest == expected[rid]["sha256"], "source hash")
    sd = [next(j for j in range(9) if n[i][j][0]) for i in range(9)]
    large = expected[rid]["large"]
    bound = sum(sd[i] == i for i in large)
    check(bound == {"R9_2_137": 4, "R9_2_1607": 2, "R9_2_1976": 0}[rid],
          "source large indicator bound")
    sources[rid] = {"sha256": digest, "selfdual_large": bound,
                    "forced_sum": 4, "contradiction": bound < 4}

receipt = {
    "zero_shift_tensor_sha256": hashlib.sha256(
        json.dumps(N, separators=(",", ":")).encode()).hexdigest(),
    "scalar_representations": scalar_reps,
    "two_dimensional_formal_codegree": 4,
    "galois_unit_restriction": [1]+[0]*7+[1]*4,
    "pointed_indicator_comparison": pointed,
    "sources": sources,
    "scope": "Exact finite checks; categorical pairing and Morita theorem are proved in the note."
}
target = HERE / "galois_fs2_receipt.json"
if target.exists():
    check(json.loads(target.read_text()) == receipt, "receipt mismatch")
else:
    target.write_text(json.dumps(receipt, indent=2)+"\n")
print("PASS: zero-shift characters, Galois restriction, pointed signs, source bounds")
