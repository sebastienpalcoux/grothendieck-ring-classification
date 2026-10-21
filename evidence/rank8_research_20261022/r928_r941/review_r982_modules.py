#!/usr/bin/env python3
"""Independent rational-matrix check of the R982 module-type receipt.

Imports no producer or SymPy code. Exhaustion of the Gram factor domain is
covered by the written lattice proof and optimized producer replay.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse
import hashlib
import itertools
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PROD = ROOT / 'evidence/rank8_research_20261022/r982'


def need(ok, message):
    if not ok:
        raise ValueError(message)


def transpose(a):
    return [list(x) for x in zip(*a)]


def multiply(a, b):
    return [[sum(x*y for x, y in zip(row, col)) for col in zip(*b)] for row in a]


def invert(a):
    n = len(a)
    m = [[F(x) for x in row] + [F(i == j) for j in range(n)] for i, row in enumerate(a)]
    for c in range(n):
        p = next((i for i in range(c, n) if m[i][c]), None)
        need(p is not None, 'singular induction matrix')
        m[c], m[p] = m[p], m[c]
        k = m[c][c]
        m[c] = [x/k for x in m[c]]
        for i in range(n):
            if i != c:
                k = m[i][c]
                m[i] = [x-k*y for x, y in zip(m[i], m[c])]
    return [r[n:] for r in m]


def run():
    files = [PROD / 'module_types.json', PROD / 'module_types.py',
             ROOT / 'evidence/rank8_m3_20261021/pipeline/census_m3.json']
    receipt = json.loads(files[0].read_text())
    source = next(x for x in json.loads(files[2].read_text()) if x['id'] == 'R8_3_982')
    R = source['tensor']
    n = len(R)
    dual = [next(j for j in range(n) if R[i][j][0]) for i in range(n)]
    groups = receipt['based_module_types']
    classes = [g['actions'] for g in groups]
    checked_factors = 0
    failures = []
    survivors = []
    for record in receipt['records']:
        a = record['algebra']
        gram = [[sum(a[k]*R[j][k][i] for k in range(n)) for j in range(n)] for i in range(n)]
        any_survivor = False
        for factor in record['factorizations']:
            B = transpose(factor['induction_columns'])
            need(multiply(B, transpose(B)) == gram, 'induction Gram')
            inverse = invert(B)
            actions = [multiply(multiply(inverse, r), B) for r in R]
            bad = [(i, j, k, x) for i, m in enumerate(actions) for j, row in enumerate(m)
                   for k, x in enumerate(row) if x.denominator != 1 or x < 0]
            need(factor['nimrep'] == (not bad), 'action obstruction truth value')
            if bad:
                i, j, k, x = bad[0]
                need(factor['first_obstruction'] == {'source_index': i, 'row': j,
                     'column': k, 'entry': str(x)}, 'exact first failed action coefficient')
                failures.append({'algebra_index': record['algebra_index'], 'first_entry': str(x)})
            else:
                any_survivor = True
                q = factor['permutation_to_class_representative']
                model = classes[factor['module_class']]
                need(sorted(q) == list(range(n)), 'class-identifying permutation')
                need(all(actions[k][i][j] == model[k][q[i]][q[j]]
                         for k, i, j in itertools.product(range(n), repeat=3)), 'class equivalence')
            checked_factors += 1
        if any_survivor:
            survivors.append(record['algebra_index'])
        big = record['rank_twelve_parity_obstruction']
        if big:
            U = transpose(big['plus_columns'])
            need(multiply(U, transpose(U)) == record['plus_gram'], 'five-column factor in ORIGINAL coordinates')
            odd = [sum(x % 2 for x in row) for row in U]
            norms = [record['minus_gram'][i][i] for i in range(3)]
            need(odd == big['odd_coordinate_counts'] and norms == big['minus_squared_norms'], 'parity data')
            need(any(x > y for x, y in zip(odd, norms)), 'five-column parity contradiction')
    need(survivors == receipt['surviving_algebra_indices'] == [0, 2, 5, 9, 12, 16, 19, 23], 'surviving algebra list')
    for matrices in classes:
        need(matrices[0] == [[int(i == j) for j in range(n)] for i in range(n)], 'unit action')
        for i, j in itertools.product(range(n), repeat=2):
            need(multiply(matrices[i], matrices[j]) ==
                 [[sum(R[i][j][k]*matrices[k][a][b] for k in range(n)) for b in range(n)] for a in range(n)],
                 'based-module action identity')
        need(all(matrices[dual[i]] == transpose(matrices[i]) for i in range(n)), 'dual transpose')
        need(all(matrices[6][i][i] == 0 and sum(matrices[6][i]) == 1 for i in range(n)), 'free g action')
        need(all(any(matrices[k][0][i] for k in range(n)) for i in range(n)), 'cyclic module generator')
    target = [1, 0, 0, 0, 0, 1, 0, 0]
    for matrices in classes[1:]:
        need(sum([matrices[k][j][j] for k in range(n)] == target for j in range(n)) == 2,
             '1+X5 internal ends in each nonregular type')
    files.append(Path(__file__).resolve())
    return {'kind': 'independent_rational_R982_module_action_audit',
            'algebra_candidates_checked': len(receipt['records']), 'induction_factors_checked': checked_factors,
            'exact_failed_actions': failures, 'surviving_algebra_indices': survivors,
            'based_module_types_checked': len(classes), 'general_module_rank_conclusion': 8,
            'scope': 'necessary module data, not algebra/module associator existence',
            'dependencies_sha256': {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in files}}


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--write', action='store_true')
    args = p.parse_args()
    result = run()
    target = HERE / 'r982_modules_independent_review.json'
    if args.write:
        target.write_text(json.dumps(result, indent=2) + '\n')
    else:
        need(result == json.loads(target.read_text()), 'independent module receipt changed')
    print('PASS: exact induction/action matrices, original-coordinate parity, and all three R982 based-module types.')
