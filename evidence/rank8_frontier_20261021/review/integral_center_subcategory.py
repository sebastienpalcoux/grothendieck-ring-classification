#!/usr/bin/env python3
"""Exact bindings for the integral-center subcategory theorem; read-only replay."""
from pathlib import Path
import argparse
import hashlib
import itertools
import json
import math

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
REPO = BASE.parents[1]

def need(value, message):
    if not value:
        raise ValueError(message)

def add(x, y):
    return (x[0]+y[0], x[1]+y[1])

def mul(x, y):
    return (x[0]*y[0]+3*x[1]*y[1], x[0]*y[1]+x[1]*y[0])

def smul(a, x):
    return (a*x[0], a*x[1])

def total(xs):
    out = (0, 0)
    for x in xs:
        out = add(out, x)
    return out

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def tensor_digest(R):
    return hashlib.sha256(json.dumps(R, separators=(',', ':')).encode()).hexdigest()

def closure(R, labels):
    out = set(labels)
    while True:
        new = out | {k for i in out for j in out for k, n in enumerate(R[i][j]) if n}
        if new == out:
            return sorted(out)
        out = new

def check_ring(ident, R, dims, expected_hash, center_source=False):
    n = len(R)
    need(tensor_digest(R) == expected_hash, 'tensor hash '+ident)
    need(all(len(M) == n and all(len(row) == n and
        all(type(c) is int and c >= 0 for c in row) for row in M) for M in R), 'tensor shape')
    need(all(R[0][i][j] == R[i][0][j] == int(i == j)
             for i, j in itertools.product(range(n), repeat=2)), 'unit')
    need(all(mul(dims[i], dims[j]) == total(smul(R[i][j][k], dims[k]) for k in range(n))
             for i, j in itertools.product(range(n), repeat=2)), 'FP dimension homomorphism')
    need(all(a > 0 and b >= 0 for a, b in dims), 'positive dimensions')
    du = []
    for i in range(n):
        candidates = [j for j in range(n) if R[i][j][0]]
        need(len(candidates) == 1 and R[i][candidates[0]][0] == 1, 'unique dual')
        du.append(candidates[0])
    need(all(du[du[i]] == i and dims[i] == dims[du[i]] for i in range(n)), 'duality')
    integral = [i for i, (_, b) in enumerate(dims) if b == 0]
    need(closure(R, integral) == integral and all(du[i] in integral for i in integral), 'integral subcategory')
    D = total(mul(x, x) for x in dims)
    need(D == (48, 24), 'global FP dimension')
    D2 = mul(D, D)
    need(D2 == (4032, 2304), 'center FP dimension')
    norm = mul(D, (D[0], -D[1]))
    need(norm == (576, 0), 'global norm')
    norm2 = mul(D2, (D2[0], -D2[1]))
    need(norm2 == (576**2, 0), 'center norm')
    need(math.gcd(*D2) == 576 and 576 == 2**6*3**2, 'two-prime divisor support')
    result = {'id': ident, 'tensor_sha256': expected_hash, 'FP_dimensions': dims,
              'integral_source_labels': integral, 'global_FP_dimension': D,
              'center_FP_dimension': D2, 'center_FP_dimension_norm': norm2[0],
              'integral_center_subcategory_dimension_divides': 576,
              'integral_center_subcategory_dimension_prime_support': [2, 3]}
    if center_source:
        inv = [i for i in range(n) if sum(R[i][du[i]]) == 1]
        central = [i for i in inv if all(R[i][j] == R[j][i] for j in range(n))]
        adjoint = closure(R, {k for i in range(n) for k, c in enumerate(R[i][du[i]]) if c})
        need(len(inv) == 6 and central == [0] and adjoint == list(range(n)), 'trivial center invertibles')
        result.update({'source_invertibles': inv, 'central_source_invertibles': central,
                       'adjoint_closure': adjoint, 'center_invertibles': 'trivial'})
    else:
        result['center_invertibles'] = 'trivial only for the specified R439 Morita dual'
    return result

def compute():
    census_path = REPO/'evidence/rank8_m3_20261021/pipeline/census_m3.json'
    bindings_path = BASE/'structural_models/rank5_route_bindings.json'
    census = {r['id']: r for r in json.loads(census_path.read_text())}
    records = []
    for ident in ['R8_3_439', 'R8_3_567']:
        row = census[ident]
        R = row['tensor']
        du = [next(j for j in range(8) if R[i][j][0]) for i in range(8)]
        dims = [(1, 0) if sum(R[i][du[i]]) == 1 else (3, 2) for i in range(8)]
        records.append(check_ring(ident, R, dims, row['tensor_sha256'], True))
    bindings = json.loads(bindings_path.read_text())
    row = next(r for r in bindings['records'] if r['route_tensor'] == 'S3_dual_selfdual_a3')
    need(row['rank5_source_id'] == 'R5_3_40' and row['basis_map_source_to_constructor'] == list(range(5)), 'rank-five source binding')
    need(row['constructor_tensor'] == row['rank5_source_tensor'], 'rank-five tensor equality')
    records.append(check_ring('R5_3_40 as the R439 Morita dual', row['constructor_tensor'],
        [(1, 0), (1, 0), (2, 0), (3, 2), (3, 2)], row['constructor_sha256']))
    inputs = [census_path, bindings_path, BASE/'structural_models/KNOWN_MODEL_ROUTES.md',
              BASE/'structural_models/POINTED_S3_SCOPE.md', HERE/'INTEGRAL_CENTER_SUBCATEGORY.md']
    return {'kind': 'integral_center_subcategory_two_prime_solvability',
            'source_sha256': {str(p.relative_to(REPO)): digest(p) for p in inputs},
            'records': records,
            'categorical_inputs': ['ENO math/0203060 Propositions 8.12,8.15; Corollary 8.14',
                                   'ENO 0809.3031 Theorem 1.6 and Proposition 4.5(iv)'],
            'conclusion': 'The tensor unit is the only integral-dimensional central simple; no general exclusion by this check alone.'}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    result = compute()
    path = HERE/'integral_center_subcategory.json'
    if args.write:
        path.write_text(json.dumps(result, indent=2)+'\n')
    else:
        need(json.loads(json.dumps(result)) == json.loads(path.read_text()), 'receipt mismatch')
    print('PASS: integral central subcategory is Vec for R439/R567 and the specified rank-five Morita dual; no exclusion alone.')
