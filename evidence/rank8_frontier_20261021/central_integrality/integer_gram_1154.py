"""Complete nonnegative integral Gram completions for R1154, low frame 31.

This is a pseudo-unitary necessary-condition computation, not a general
noncategorification certificate. Enumeration uses exact affine bounds on every
pivot variable; no floating-point solver or arbitrary search limit is used.
"""
from pathlib import Path
import argparse
import hashlib
import itertools
import json
import math
import sys
import time

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'noncommutative'))
import full_rotation as full


def need(ok, message):
    if not ok:
        raise ValueError(message)


def enumerate_bounded(A, b, bounds):
    """Solve Ax=b, 0<=x<=bounds over Z, by complete affine elimination."""
    s = full.s
    n = A.cols
    rr, pivots = A.row_join(b).rref()
    need(n not in pivots, 'Consistent Gram equations')
    free = [j for j in range(n) if j not in pivots]
    # Larger contributions first tighten the nonnegative pivot constraints early.
    free.sort(key=lambda j: max(abs(rr[i, j]) for i in range(len(pivots))) * bounds[j], reverse=True)
    coefficients, lower, upper = [], [], []
    for i, p in enumerate(pivots):
        den = int(s.ilcm(*[rr[i, j].q for j in free + [n]]))
        coefficients.append([int(rr[i, j] * den) for j in free])
        upper.append(int(rr[i, n] * den))
        lower.append(upper[-1] - bounds[p] * den)
    k, rank = len(free), len(pivots)
    suffix_min = [[0] * (k + 1) for _ in pivots]
    suffix_max = [[0] * (k + 1) for _ in pivots]
    for i, row in enumerate(coefficients):
        for at in reversed(range(k)):
            contribution = row[at] * bounds[free[at]]
            suffix_min[i][at] = suffix_min[i][at + 1] + min(0, contribution)
            suffix_max[i][at] = suffix_max[i][at + 1] + max(0, contribution)
    partial = [0] * rank
    values = [0] * n
    results = []
    visited = 0

    def dfs(at):
        nonlocal visited
        visited += 1
        if at == k:
            vector = list(values)
            for i, p in enumerate(pivots):
                value = rr[i, n] - sum(rr[i, j] * vector[j] for j in free)
                if value.q != 1 or not 0 <= value <= bounds[p]:
                    return
                vector[p] = int(value)
            results.append(vector)
            return
        lo, hi = 0, bounds[free[at]]
        for i, row in enumerate(coefficients):
            coefficient = row[at]
            a = lower[i] - partial[i] - suffix_max[i][at + 1]
            b = upper[i] - partial[i] - suffix_min[i][at + 1]
            if coefficient > 0:
                lo = max(lo, -((-a) // coefficient))
                hi = min(hi, b // coefficient)
            elif coefficient < 0:
                lo = max(lo, -((-b) // coefficient))
                hi = min(hi, a // coefficient)
            elif not a <= 0 <= b:
                return
        for value in range(lo, hi + 1):
            values[free[at]] = value
            for i in range(rank):
                partial[i] += coefficients[i][at] * value
            dfs(at + 1)
            for i in range(rank):
                partial[i] -= coefficients[i][at] * value

    dfs(0)
    results.sort()
    # Every returned vector is checked against all 28 original equations.
    need(len(results) == len(set(map(tuple, results))), 'Unique integral completions')
    for vector in results:
        need(A * s.Matrix(vector) == b, 'Original Gram equations')
        need(all(0 <= v <= limit for v, limit in zip(vector, bounds)), 'Original Gram bounds')
    return results, {'equation_rank': rank, 'free_coordinate_order': free,
                     'unpruned_box_size': math.prod(bounds[j] + 1 for j in free),
                     'visited_nodes': visited, 'complete': True}


def compute():
    full.base.install()
    row = next(r for r in json.loads((full.c.OLD.parent / 'pipeline/census_m3.json').read_text())
               if r['id'] == 'R8_3_1154')
    R = row['tensor']
    a = full.c.w.data(R)
    cols = a['lows'][31]
    Q, high = full.base.grams.high_columns(a, full.s.Matrix.hstack(*map(full.s.Matrix, cols)))
    pairs = list(itertools.combinations_with_replacement(range(7), 2))
    A = full.s.Matrix([[v[i] * v[j] for v, dimension in high] for i, j in pairs])
    b = full.s.Matrix([Q[i, j] for i, j in pairs])
    bounds = [min(int(Q[j, j]) // (v[j] ** 2) for j in range(7) if v[j]) for v, dimension in high]
    solutions, metadata = enumerate_bounded(A, b, bounds)
    payload = {'id': row['id'], 'tensor_sha256': row['tensor_sha256'],
               'scope': 'pseudo_unitary_necessary_conditions_only', 'low_index': 31,
               'low_columns': [list(v) for v in cols],
               'high_columns': [list(v) for v, dimension in high],
               'gram_remainder': [[int(x) for x in rr] for rr in Q.tolist()],
               'bounds': bounds, 'completions': solutions, 'metadata': metadata,
               'conclusion': 'Complete integer Gram enumeration; surviving completions are not models.'}
    return payload


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    result = compute()
    path = HERE / 'integer_gram_1154.json'
    if args.write:
        path.write_text(json.dumps(result, indent=2) + '\n')
    else:
        need(result == json.loads(path.read_text()), 'Exact integer Gram replay')
    print('PASS R1154 frame 31: complete', len(result['completions']), 'integral Gram completions;', result['metadata'])


if __name__ == '__main__':
    main()
