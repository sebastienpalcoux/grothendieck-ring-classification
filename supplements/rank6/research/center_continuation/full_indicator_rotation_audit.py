"""Exact cyclic-rotation multiplicities for the cyclic-eight central witness.

This checks a necessary condition only. It supplies neither an associator nor
an algebra object. Coefficients are exact in Q(sqrt(17)); no floating point is
used. Run with --write to refresh the summary JSON.
"""
import json
import math
import sys
from fractions import Fraction as Q
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
rec = json.loads((HERE / 'cyclic8_center_tensor.json').read_text())
F = rec['F']
R = next(r['N'] for r in json.loads((ROOT / 'data/census.json').read_text())
         if r['id'] == 'R6_3_215')
dimensions = [(1, 0), (1, 0), (4, 1), (4, 1), (3, 1), (5, 1)]


def add(a, b):
    return a[0] + b[0], a[1] + b[1]


def scale(a, z):
    return a[0] * z, a[1] * z


def mul(a, b):
    return a[0]*b[0] + 17*a[1]*b[1], a[0]*b[1] + a[1]*b[0]


def total(items):
    result = (0, 0)
    for item in items:
        result = add(result, item)
    return result


def character(a):
    a %= 17
    return 0 if a == 0 else 1 if pow(a, 8, 17) == 1 else -1


central_dimensions = [total(scale(dimensions[i], row[i]) for i in range(6))
                      for row in F]
for first, count in [(6, 4), (10, 8), (18, 4)]:
    if any(F[j] != F[first] for j in range(first, first + count)):
        raise ValueError('restriction types are not constant')


def indicator(n, i):
    low = total(scale(central_dimensions[j], F[j][i]) for j in range(6))
    sa = (4 * (-1)**(n//4), 0) if n % 4 == 0 else (0, 0)
    sb = (8, 0) if n % 17 == 0 else (Q(-1, 2), Q(-character(n), 2))
    sc = (4 * (-1)**n, 0)
    a, b = total([low] + [scale(mul(central_dimensions[j], v), F[j][i])
                         for j, v in [(6, sa), (10, sb), (18, sc)]])
    return Q(136*a - 544*b, 1088), Q(136*b - 32*a, 1088)


def ramanujan(d, j):
    return sum(k * int(sp.mobius(d//k)) for k in sp.divisors(math.gcd(d, j)))


def run(bound=136):
    indicators = {n: [indicator(n, i) for i in range(6)]
                  for n in range(1, bound+1)}
    failures = []
    counts = 0
    minima = []
    for i in range(6):
        powers = [[1, 0, 0, 0, 0, 0]]
        for k in range(bound):
            powers.append([sum(powers[-1][a]*R[a][i][b] for a in range(6))
                           for b in range(6)])
        for n in range(1, bound+1):
            traces = {}
            for d in sp.divisors(n):
                v = powers[n//d]
                traces[d] = total(scale(indicators[d][a], v[a]) for a in range(6))
            multiplicities = []
            for j in range(n):
                numerator = Q(0)
                for d, (a, b) in traces.items():
                    numerator += a * ramanujan(d, j)
                    if d % 17 == 0:
                        m = d//17
                        numerator += 17*b*character(j*m)*ramanujan(m, j)
                    elif b:
                        raise ValueError('indicator does not lie in the required cyclotomic field')
                value = numerator/n
                multiplicities.append(value)
                if value.denominator != 1 or value < 0:
                    failures.append({'simple': i, 'rotation_order': n,
                                     'eigenvalue_exponent': j, 'multiplicity': str(value)})
                counts += 1
            if sum(multiplicities) != powers[n][0]:
                raise ValueError('multiplicity sum does not equal invariant-space dimension')
            minima.append({'simple': i, 'rotation_order': n,
                           'minimum_multiplicity': str(min(multiplicities)),
                           'invariant_space_dimension': str(powers[n][0])})
    result = {
        'id': 'R6_3_215',
        'scope': 'specified cyclic-eight central witness; necessary conditions only',
        'bound': bound,
        'simple_objects': 6,
        'rotation_spaces_checked': 6*bound,
        'eigenvalue_multiplicities_checked': counts,
        'failures': failures,
        'outcome': 'all checked multiplicities are nonnegative integers' if not failures else 'obstruction found',
        'indicator_values_Q_sqrt17': {
            str(n): [[str(a), str(b)] for a, b in row] for n, row in indicators.items()},
        'minima_and_space_dimensions': minima,
        'method': 'exact cyclic Fourier inversion; quadratic Gauss sums and Ramanujan sums',
        'not_claimed': ['associator', 'etale algebra', 'categorification', 'exhaustive central-witness search'],
    }
    return result


if __name__ == '__main__':
    result = run()
    if '--write' in sys.argv:
        (HERE / 'full_indicator_rotation_audit.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: result[k] for k in ['id', 'scope', 'bound',
          'rotation_spaces_checked', 'eigenvalue_multiplicities_checked', 'failures', 'outcome']}, indent=2))
