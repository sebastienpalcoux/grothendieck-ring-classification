"""Independent un-gauged exact verifier for the four simultaneous exclusions.

No imports from the discovery program.  Checks polynomial identities in the
original rank-eight regular ring, then enumerates every bounded symmetric
matrix without sign gauge.  A necessary characteristic-polynomial trace
filter is used only to accelerate the complete integer enumeration.
"""
from pathlib import Path
import argparse
import hashlib
import itertools
import json
import math
import sympy as s

HERE = Path(__file__).resolve().parent


def check(value, message):
    if not value:
        raise ValueError(message)


def mat_product(a, b):
    columns = list(zip(*b))
    return [[sum(x * y for x, y in zip(row, col)) for col in columns] for row in a]


def mat_eval(a, coeff):
    v = [[0 for _ in row] for row in a]
    for c in coeff:
        v = mat_product(v, a)
        for k in range(len(a)):
            v[k][k] += int(c)
    return v


def possible_trace_pairs(coefficients, dimension):
    t = s.Symbol('t')
    polynomial = s.Poly.from_list(coefficients, t)
    factors = [f for f, _ in s.factor_list(polynomial)[1]]
    # A rational matrix killed by squarefree p has characteristic polynomial
    # a product of irreducible factors of p, with nonnegative multiplicities.
    check(s.gcd(polynomial, polynomial.diff()).degree() == 0, 'p is not squarefree')
    pairs = set()
    for powers in itertools.product(*(range(dimension // f.degree() + 1) for f in factors)):
        if sum(k * f.degree() for k, f in zip(powers, factors)) != dimension:
            continue
        charpoly = s.Poly(1, t)
        for f, k in zip(factors, powers):
            charpoly *= f ** k
        coefficients = charpoly.all_coeffs()
        pairs.add((-int(coefficients[1]), int(coefficients[1] ** 2 - 2 * coefficients[2])))
    return sorted(pairs)


def verify_record(row, record):
    R = row['tensor']
    digest = hashlib.sha256(json.dumps(R, separators=(',', ':')).encode()).hexdigest()
    check(digest == row['tensor_sha256'] == record['tensor_sha256'], 'source digest mismatch')
    a = record['search']['setup']
    g, x = a['involution'], a['generator']
    check(all(R[i][j] == R[j][i] for i in range(8) for j in range(8)), 'not commutative')
    check(g != 0 and R[g][g] == [1] + [0] * 7, 'not an involution')
    fixed = [j for j in range(8) if R[g][j][j]]
    check(fixed == a['fixed'] and fixed, 'fixed basis mismatch')
    check(all(any(R[g][z][z] and R[z][v][v] % 2 for z in range(8)) for v in fixed),
          'S_g=I hypothesis failed')
    check(R[x][x][0] == 1, 'chosen generator is not self-dual')
    N = [s.Matrix(v) for v in R]
    plus = s.eye(8) + N[g]
    p = a['quotient_polynomial']
    # These identities suffice; no quotient matrix implementation is reused.
    check(s.Matrix(mat_eval(R[x], p)) * plus == s.zeros(8), 'polynomial does not vanish on g=1 quotient')
    for i, data in enumerate(a['interpolation']):
        den = data['denominator']
        check(isinstance(den, int) and den > 0, 'invalid rational denominator')
        value = s.Matrix(mat_eval(R[x], list(reversed(data['ascending_numerators']))))
        check((value - den * N[i]) * plus == s.zeros(8), 'interpolation not an identity modulo g-1')
    f = len(fixed)
    cells = [(i, j) for i in range(f) for j in range(i, f)]
    bounds = [R[x][fixed[i]][fixed[j]] for i, j in cells]
    domains = [range(-b, b + 1, 2) for b in bounds]
    count = math.prod(len(v) for v in domains)
    traces = possible_trace_pairs(p, f)
    trace_filtered = polynomial_survivors = bounded_representations = tested = 0
    for values in itertools.product(*domains):
        tested += 1
        tr = sum(z for z, (i, j) in zip(values, cells) if i == j)
        tr2 = sum(z * z * (1 if i == j else 2) for z, (i, j) in zip(values, cells))
        if (tr, tr2) not in traces:
            continue
        trace_filtered += 1
        B = [[0] * f for _ in range(f)]
        for z, (i, j) in zip(values, cells):
            B[i][j] = B[j][i] = z
        if any(z for row0 in mat_eval(B, p) for z in row0):
            continue
        polynomial_survivors += 1
        valid = True
        for k, data in enumerate(a['interpolation']):
            numerators = mat_eval(B, list(reversed(data['ascending_numerators'])))
            den = data['denominator']
            for i, v in enumerate(fixed):
                for j, w in enumerate(fixed):
                    num, bound = numerators[i][j], R[k][v][w]
                    if num % den or abs(num // den) > bound or (num // den - bound) % 2:
                        valid = False
            if not valid:
                break
        if valid:
            bounded_representations += 1
    check(tested == count, 'not every matrix was enumerated')
    check(bounded_representations == 0, 'a bounded simultaneous system survives')
    check(polynomial_survivors > 0, 'expected strict improvement over single-generator test')
    return {'id': row['id'], 'tensor_sha256': digest, 'ungauged_cases': tested,
            'possible_trace_pairs': traces, 'trace_filter_survivors': trace_filtered,
            'polynomial_survivors': polynomial_survivors,
            'simultaneous_bounded_survivors': bounded_representations,
            'outcome': 'excluded', 'scope': 'general_complex_fusion_category'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    rows = {r['id']: r for r in json.loads((HERE.parents[1] / 'rank8_m3_20261021/pipeline/census_m3.json').read_text())}
    evidence = json.loads((HERE / 'simultaneous_split_results.json').read_text())
    check({r['id'] for r in evidence['records']} == {f'R8_3_{i}' for i in (1203, 1350, 2842, 2885)},
          'wrong four target records')
    result = {'kind': 'independent_ungauged_simultaneous_split_validation',
              'records': [verify_record(rows[r['id']], r) for r in evidence['records']]}
    destination = HERE / 'simultaneous_split_independent_validation.json'
    # JSON normalizes tuple-valued trace pairs to lists.
    result = json.loads(json.dumps(result))
    if args.write:
        destination.write_text(json.dumps(result, indent=2) + '\n')
    else:
        check(json.loads(destination.read_text()) == result, 'independent replay changed')
    print('PASS: all 345600 ungauged matrices checked; no simultaneous bounded representation for four rings')


if __name__ == '__main__':
    main()
