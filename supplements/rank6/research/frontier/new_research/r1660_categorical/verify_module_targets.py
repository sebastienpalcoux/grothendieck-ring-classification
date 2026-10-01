#!/usr/bin/env python3
"""Exact, optimizer-free verification of the four-row module reduction.

Completeness of the finite bounds and the module-rank theorem are proved in
module_rank_and_morita_targets.tex. This script does not test associators.
"""
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def add(A, B):
    return [[a + b for a, b in zip(x, y)] for x, y in zip(A, B)]


def scale(n, A):
    return [[n*x for x in row] for row in A]


def mul(A, B):
    return [[sum(x*y for x, y in zip(row, col)) for col in zip(*B)]
            for row in A]


I = [[1, 0], [0, 1]]
solutions = []
for a in range(7):
    for b in range(5):
        for c in range(5):
            for f in range(4):
                U = [[a, b], [b, 6-a]]
                R = [[c, f], [f, 4-c]]
                if add(mul(U, U), scale(2, mul(R, R))) != add(I, add(scale(6, U), scale(8, R))):
                    continue
                if add(mul(U, R), mul(R, U)) != add(scale(6, R), scale(4, U)):
                    continue
                solutions.append((a, b, c, f))

expected = [(0, 1, 0, 0), (2, 3, 2, 2), (1, 2, 0, 1), (1, 2, 1, 2)]
all_expected = sorted(expected + [(6-a, b, 4-c, f) for a, b, c, f in expected])
require(sorted(solutions) == all_expected, 'Four-row U,R classification failed')

rows = []
for a, b, c, f in expected:
    U = [[a, b], [b, 6-a]]
    R = [[c, f], [f, 4-c]]
    choices = []
    for x in [-1, 0, 1]:
        for y in [-1, 0, 1]:
            for z in [-1, 0, 1]:
                V = [[x, y], [y, z]]
                if mul(V, V) != I:
                    continue
                if any((U[i][j] + V[i][j]) % 2 or U[i][j] < abs(V[i][j])
                       for i in range(2) for j in range(2)):
                    continue
                P = [[(U[i][j]+V[i][j])//2 for j in range(2)] for i in range(2)]
                Q = [[(U[i][j]-V[i][j])//2 for j in range(2)] for i in range(2)]
                rhs = add(scale(3, add(P, Q)), scale(4, R))
                require(add(add(mul(P,P),mul(Q,Q)),mul(R,R)) == add(I,rhs), 'Identity coefficient')
                require(add(add(mul(P,Q),mul(Q,P)),mul(R,R)) == rhs, 'g coefficient')
                choices.append({'V': V, 'P': P, 'Q': Q,
                                'leaf_algebra_coefficients_1_g_X_gX_sigma_T':
                                [1, 0, P[0][0], Q[0][0], 0, R[0][0]]})
    rows.append({'parameters_a_b_c_f': [a,b,c,f], 'U': U, 'R': R, 'choices': choices})

require([len(row['choices']) for row in rows] == [2,2,4,4], 'V choices')
receipt = {
    'status': 'Necessary based-module conditions only; no algebra associators checked.',
    'indecomposable_module_rank_theorem': 6,
    'raw_U_R_solutions': len(solutions),
    'U_R_types_up_to_block_exchange': 4,
    'based_modules_up_to_Ising_block_and_leaf_relabeling': 10,
    'based_modules_also_modulo_X_gX_exchange': 6,
    'rows': rows,
}
path = Path(__file__).with_name('module_targets_receipt.json')
path.write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps({k: v for k,v in receipt.items() if k != 'rows'}, indent=2))
