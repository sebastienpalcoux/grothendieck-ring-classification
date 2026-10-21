"""General-complex exclusion of R8_3_921 by normal split-module matrices.

Default: read-only exact replay. --write creates the evidence JSON.
The spectral support proof and an independent full bounded-matrix search
both verify the necessary annihilator, using exact integer arithmetic.
"""
from pathlib import Path
import argparse
import hashlib
import itertools
import json
import sympy as s

HERE = Path(__file__).resolve().parent


def need(value, message):
    if not value:
        raise ValueError(message)


def product(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(a)))
             for j in range(len(a))] for i in range(len(a))]


def evaluate(a, coefficients):
    n = len(a)
    v = [[0] * n for _ in range(n)]
    for c in coefficients:
        v = product(v, a)
        for i in range(n):
            v[i][i] += c
    return v


def run():
    row = next(r for r in json.loads((HERE.parents[1] / 'rank8_m3_20261021/pipeline/census_m3.json').read_text())
               if r['id'] == 'R8_3_921')
    R = row['tensor']
    digest = hashlib.sha256(json.dumps(R, separators=(',', ':')).encode()).hexdigest()
    need(digest == row['tensor_sha256'], 'tensor digest mismatch')
    need(all(R[i][j] == R[j][i] for i in range(8) for j in range(8)), 'not commutative')
    g, x, y = 5, 3, 6
    need(R[g][g] == [1] + [0] * 7 and g != 0, 'involution missing')
    fixed = [v for v in range(8) if R[g][v][v]]
    need(fixed == [3, 4, 6, 7], 'fixed basis changed')
    bounds = [[R[x][v][w] for w in fixed] for v in fixed]
    need(all(b % 2 for line in bounds for b in line), 'every entry must be odd')
    need(all(bounds[i][i] == 1 for i in range(4)), 'diagonal trace bound changed')
    dual = next(j for j in range(8) if R[x][j][0])
    need(dual == 4, 'dual index changed')
    N = [s.Matrix(a) for a in R]
    # Compute p from its factors rather than trusting listed coefficients.
    t = s.Symbol('t')
    p = [int(c) for c in s.Poly(t * (t*t - 8*t + 6) * (t*t + 2*t + 4), t).all_coeffs()]
    need(s.Matrix(evaluate(R[x], p)) == s.zeros(8), 'source annihilator failed')
    need(s.gcd(s.Poly.from_list(p, t), s.Poly.from_list(p, t).diff()).degree() == 0,
         'source annihilator is not squarefree')
    q = [1, 2, 4]
    coefficients = [0, -7, -7, -3, 0, 0, 30, -7]
    transport = sum((a * n for a, n in zip(coefficients, N)), s.zeros(8))
    need(s.Matrix(evaluate(R[x], q)) * transport == 148 * N[y], 'annihilator transport failed')
    norm_lower_bound = sum(b % 2 for line in bounds for b in line)
    trace_bound = sum(bounds[i][i] for i in range(4))
    options = []
    for a, b, c in itertools.product(range(5), range(3), range(3)):
        if a + 2*b + 2*c != 4:
            continue
        # Rational characteristic factors t^a, real quadratic^b,
        # complex quadratic^c; real normality gives spectral Frobenius norm.
        trace, norm = 8*b - 2*c, 52*b + 8*c
        reason = ('trace_bound' if abs(trace) > trace_bound else
                  'frobenius_norm_bound' if norm < norm_lower_bound else 'survives')
        options.append({'multiplicities': [a, b, c], 'trace': trace,
                        'frobenius_norm_squared': norm, 'outcome': reason})
    survivors = [r for r in options if r['outcome'] == 'survives']
    need(len(survivors) == 1 and survivors[0]['multiplicities'] == [0, 0, 2],
         'spectral support not confined to q')
    # Independent un-gauged exhaustive check: do not use the trace/norm proof
    # to prune the domain. Check normality and p(B)=0 on the full parity box.
    domains = [range(-b, b + 1, 2) for line in bounds for b in line]
    tested = normal = polynomial_survivors = 0
    witness_matrices = []
    for values in itertools.product(*domains):
        tested += 1
        B = [list(values[4*i:4*i+4]) for i in range(4)]
        BT = list(map(list, zip(*B)))
        # Equality of row/column squared norms is necessary for normality.
        if any(sum(z*z for z in B[i]) != sum(z*z for z in BT[i]) for i in range(4)):
            continue
        if product(B, BT) != product(BT, B):
            continue
        normal += 1
        if any(z for line in evaluate(B, p) for z in line):
            continue
        polynomial_survivors += 1
        need(not any(z for line in evaluate(B, q) for z in line), 'q does not annihilate bounded survivor')
        witness_matrices.append(B)
    need(tested == 131072, 'full normal-matrix box was not exhausted')
    need(polynomial_survivors > 0, 'expected surviving single-generator matrices')
    obstruction = next((i, j, R[y][v][w]) for i, v in enumerate(fixed)
                       for j, w in enumerate(fixed) if R[y][v][w] % 2)
    return {'id': row['id'], 'tensor_sha256': digest,
            'criterion': 'normal_split_spectral_support_and_annihilator_transport',
            'scope': 'general_complex_fusion_category', 'outcome': 'excluded',
            'involution': g, 'fixed': fixed, 'normal_generator': x, 'dual_generator': dual,
            'bounds': bounds, 'source_polynomial': p, 'forced_annihilator': q,
            'characteristic_factor_options': options,
            'trace_absolute_bound': trace_bound, 'frobenius_norm_squared_lower_bound': norm_lower_bound,
            'transport_coefficients': coefficients, 'transport_denominator': 148,
            'forced_zero_basis_index': y, 'nonzero_parity_witness': list(obstruction),
            'independent_full_box': {'tested': tested, 'normal_matrices': normal,
                                     'source_polynomial_survivors': polynomial_survivors,
                                     'all_survivors_killed_by_forced_annihilator': True,
                                     'matrices': witness_matrices}}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    actual = run()
    path = HERE / 'normal_split_spectral_results.json'
    if args.write:
        path.write_text(json.dumps(actual, indent=2) + '\n')
    else:
        need(json.loads(path.read_text()) == actual, 'evidence did not replay')
    print('PASS: R8_3_921 excluded over C by exact spectral support and 131072-matrix independent enumeration')
