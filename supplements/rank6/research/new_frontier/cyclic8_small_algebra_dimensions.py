"""Exact small-algebra dimension check used by cyclic8_morita_exclusion.md.

Elements a+b*d are represented by pairs, with d^2=8*d+1 and d=4+sqrt(17).
No floating-point comparison or computer-algebra square test is used.
"""
import itertools
import json
from math import isqrt
from pathlib import Path


def positive(a, b):
    """Return a+b*d > 0, exactly."""
    c = a + 4*b
    if b == 0:
        return c > 0
    if b > 0:
        return c >= 0 or 17*b*b > c*c
    return c > 0 and c*c > 17*b*b


def norm(a, b):
    return a*a+8*a*b-b*b


def check(condition, message):
    if not condition:
        raise ArithmeticError(message)


# Bound L=4(d-1)^2/9=(8+24*d)/9. Every noninvertible has
# dimension >=d-1, and 4(d-1)>L, so at most three can occur.
check(positive(-44, 12), 'four noninvertibles must exceed the bound')
dimensions = set()
for epsilon in range(2):
    for n_d, n_minus, n_plus in itertools.product(range(4), repeat=3):
        if n_d+n_minus+n_plus > 3:
            continue
        a = 1+epsilon-n_minus+n_plus
        b = n_d+n_minus+n_plus
        if not positive(9*a-8, 9*b-24):
            dimensions.add((a, b))

expected = {(1, 0), (2, 0), (0, 1), (1, 1), (2, 1), (3, 1),
            (-1, 2), (0, 2), (1, 2), (2, 2), (3, 2), (4, 2), (-2, 3)}
check(dimensions == expected, 'incorrect exhaustive dimension list')
records = []
for a, b in sorted(dimensions, key=lambda x: (x[1], x[0])):
    n = norm(a, b)
    if (a, b) == (1, 0):
        reason = 'square; excluded separately by two distinct d+1 simples in the module'
    elif (a, b) == (2, 0):
        # (u+v*sqrt17)^2=2 forces uv=0; neither u^2=2 nor v^2=2/17
        # has a rational solution.
        reason = '2 is not a square in Q(sqrt17)'
    else:
        check(n < 0 or isqrt(n)**2 != n, 'unexpected square field norm')
        reason = 'field norm is not a nonnegative rational square'
    records.append({'dimension_in_basis_1_d': [a, b], 'field_norm': n,
                    'square_obstruction': reason})
output = {'bound_in_basis_1_d': ['8/9', '8/3'],
          'dimension_list_complete': True,
          'correction_to_GIS_Lemma_4_16': 'Include 3d-2, of field norm -53.',
          'dimensions': records}
path = Path(__file__).with_suffix('.json')
path.write_text(json.dumps(output, indent=2)+'\n')
print(json.dumps(output, indent=2))
