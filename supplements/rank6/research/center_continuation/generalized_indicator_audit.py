"""Exact generalized FS rotation test for the cyclic-eight proposed functor.

Ng--Schauenburg, arXiv:0806.2493, Theorem 5.4 and Lemma 5.3.
This is a necessary-condition check; no tensor functor is constructed.
Python arbitrary-precision integers are used throughout.
"""
import json
import math
import sys
from functools import lru_cache
from pathlib import Path

import numpy as np
import sympy as sp

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
md = json.loads((HERE/'cyclic8_modular_data.json').read_text())
target = json.loads((HERE/'cyclic8_center_tensor.json').read_text())
canonical = json.loads((HERE/'cyclic8_canonical_restriction.json').read_text())
S = np.array(md['S_coefficients'], dtype=object)
twists = md['T_exponents']


def reduce136(poly):
    p = list(map(int, poly)) + [0]*max(0, 64-len(poly))
    for k in range(len(p)-1, 63, -1):
        v = p[k]
        if v:
            for j in range(16):
                p[k-64+4*j] -= v*(-1)**j
    return np.array(p[:64], dtype=object)


@lru_cache(None)
def root(k):
    k %= 136
    p = [0]*(k+1)
    p[k] = 1
    return reduce136(p)


def product(a, b):
    return reduce136(np.convolve(a, b))


def action_t(v, exponent):
    return np.array([product(row, root(exponent*twists[i]))
                     for i, row in enumerate(v)], dtype=object)


def action_s(v):
    result = []
    for row in S:
        z = sum((product(a, b) for a, b in zip(row, v)), np.zeros(64, dtype=object))
        if any(int(c) % 136 for c in z):
            raise ValueError('nonintegral cyclotomic indicator coefficient')
        result.append([int(c)//136 for c in z])
    return np.array(result, dtype=object)


def word(m, k):
    operators = []
    while k:
        q, k = divmod(k, m)
        operators.append(('T', -q))
        if k:
            operators.append(('S', 0))
            m, k = k, -m
    return operators, m


@lru_cache(None)
def cyclotomic(order):
    x = sp.Symbol('x')
    p = sp.Poly(sp.cyclotomic_poly(order, x), x)
    return p.degree(), [(int(e[0]), int(c)) for e, c in p.terms() if e[0] < p.degree()]


def reduce_order(coefficients, order):
    p = list(coefficients)
    degree, terms = cyclotomic(order)
    for k in range(len(p)-1, degree-1, -1):
        v = p[k]
        if v:
            for j, c in terms:
                p[k-degree+j] -= v*c
    return p[:degree]


def audit(F, R, bound):
    F = np.array(F, dtype=object)
    R = np.array(R, dtype=object)
    spaces = 0
    eigenvalues = 0
    failures = []
    for simple in range(len(R)):
        powers = [np.eye(len(R), dtype=object)[0]]
        for _ in range(bound):
            powers.append(powers[-1] @ R[simple])
        for m in range(1, bound+1):
            traces = []
            for k in range(m):
                operators, g = word(m, k)
                v = np.zeros((22, 64), dtype=object)
                v[:, 0] = F @ powers[g]
                for op, exponent in reversed(operators):
                    v = action_s(v) if op == 'S' else action_t(v, exponent)
                traces.append(v)
            order = 136*m
            for central in range(22):
                multiplicities = []
                for j in range(m):
                    p = [0]*order
                    for k in range(m):
                        shift = (twists[central] - 136*j)*k
                        for e, c in enumerate(traces[k][central]):
                            if c:
                                p[(m*e+shift) % order] += int(c)
                    reduced = reduce_order(p, order)
                    if any(reduced[1:]) or reduced[0] % m or reduced[0] < 0:
                        failures.append({'simple': simple, 'central': central,
                                         'rotation_order': m, 'eigenvalue_exponent': j,
                                         'cyclotomic_numerator': reduced})
                    multiplicities.append(reduced[0]//m)
                    eigenvalues += 1
                if not failures and sum(multiplicities) != int((F @ powers[m])[central]):
                    raise ValueError('wrong total multiplicity')
                spaces += 1
        print('checked simple', simple, flush=True)
    return {'spaces': spaces, 'eigenvalue_multiplicities': eigenvalues, 'failures': failures}


if __name__ == '__main__':
    bound = 8
    R = next(r['N'] for r in json.loads((ROOT/'data/census.json').read_text())
             if r['id'] == 'R6_3_215')
    report = {'bound': bound, 'source': 'Ng--Schauenburg, arXiv:0806.2493, Theorem 5.4 and Lemma 5.3',
              'scope': 'specified cyclic-eight modular datum and restriction matrices',
              'target': audit(target['F'], R, bound),
              'canonical_positive_control': audit(canonical['F_D'], canonical['N_D'], bound),
              'arithmetic': 'arbitrary-precision integers in cyclotomic polynomial quotients',
              'not_claimed': ['associator', 'tensor functor', 'etale algebra', 'categorification']}
    if '--write' in sys.argv:
        (HERE/'generalized_indicator_audit.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))
