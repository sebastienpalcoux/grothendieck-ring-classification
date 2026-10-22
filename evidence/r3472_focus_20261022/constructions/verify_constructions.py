#!/usr/bin/env python3
"""Exact R3472 seven-invertible tensor and RW parity certificates."""
from pathlib import Path
from fractions import Fraction
import argparse
import hashlib
import itertools
import json

HERE = Path(__file__).resolve().parent


def need(condition, message):
    if not condition:
        raise ValueError(message)


def add(x, y):
    return (x[0] + y[0], x[1] + y[1])


def mul(x, y):
    return (x[0]*y[0] + 2*x[1]*y[1], x[0]*y[1] + x[1]*y[0])


def tensor(action):
    n = 7
    R = [[[0]*14 for _ in range(14)] for _ in range(14)]
    for i in range(n):
        for j in range(n):
            R[i][j][(i+j) % n] = 1
            R[i][n+j][n+(i+j) % n] = 1
            R[n+i][j][n+(i+action*j) % n] = 1
            R[n+i][n+j][(i+action*j) % n] = 1
            for k in range(n):
                R[n+i][n+j][n+k] = 2
    return R


def check_tensor(R, action):
    rank = len(R)
    dual = [(-i) % 7 for i in range(7)] + [7+(-action*i) % 7 for i in range(7)]
    dims = [(1, 0)]*7 + [(7, 5)]*7
    association_count = 0
    for i in range(rank):
        need(dual[dual[i]] == i, 'Involution square')
        for j in range(rank):
            need(R[0][i][j] == R[i][0][j] == int(i == j), 'Unit')
            need(R[i][j][0] == int(j == dual[i]), 'Dual coefficient')
            product_dim = (0, 0)
            for k in range(rank):
                c = R[i][j][k]
                need(type(c) is int and c >= 0, 'Nonnegative integers')
                need(c == R[dual[j]][dual[i]][dual[k]], 'Dual anti-automorphism')
                need(c == R[dual[i]][k][j] == R[k][dual[j]][i], 'Frobenius reciprocity')
                product_dim = add(product_dim, (c*dims[k][0], c*dims[k][1]))
                for l in range(rank):
                    need(sum(R[i][j][t]*R[t][k][l] for t in range(rank)) ==
                         sum(R[j][k][t]*R[i][t][l] for t in range(rank)), 'Associativity')
                    association_count += 1
            need(product_dim == mul(dims[i], dims[j]), 'Dimension character')
    global_dim = (0, 0)
    for d in dims:
        global_dim = add(global_dim, mul(d, d))
    need(global_dim == (700, 490), 'Global dimension')
    commutative = all(R[i][j] == R[j][i] for i in range(rank) for j in range(rank))
    need(commutative == (action == 1), 'Commutativity classification')
    canonical = json.dumps(R, separators=(',', ':')).encode()
    return {
        'name': 'C7_quadratic_m2_' + ('identity' if action == 1 else 'inversion'),
        'right_action_exponent': action,
        'rank': rank,
        'dimensions_in_Qsqrt2': [list(d) for d in dims],
        'global_dimension_in_Qsqrt2': list(global_dim),
        'dual': dual,
        'commutative': commutative,
        'associativity_equations_checked': association_count,
        'tensor_sha256': hashlib.sha256(canonical).hexdigest(),
        'fusion_ring_axioms': 'PASS',
        'categorification': 'not established',
        'Morita_identification_with_R3472': 'not established',
    }


def compute():
    records = [check_tensor(tensor(a), a) for a in (1, -1)]
    need(mul((7, 5), (7, 5)) == (99, 70), 'Quadratic relation')
    # Every possible residue of A mod 4: trace 2 and determinant 3.
    residues = []
    alternating = []
    for a, b, c, d in itertools.product(range(4), repeat=4):
        if (a+d) % 4 == 2 and (a*d-b*c) % 4 == 3:
            residues.append([a, b, c, d])
            if b % 2 == c % 2 == 0:
                alternating.append([a, b, c, d])
    need(residues and not alternating, 'RW 2-primary parity contradiction')
    # Uniform commutative multiplication choices forced by Phi_7.
    choices = [(14-6*b, b, 14-7*b) for b in range(3)]
    need(choices == [(14, 0, 14), (8, 1, 7), (2, 2, 0)], 'Coefficient classification')
    # At t=7: f=7(1+x^2) satisfies f^2-371f+2597=0,
    # with discriminant 49^2 * 53, outside Q(sqrt(2)).
    need(371**2-4*2597 == 49**2*53, 'Nonuniform codegree discriminant')
    # N=196 and required quotient h=28m. The general bound is h^2<=2Nm^2.
    need(28**2 > 2*196, 'Pointed stabilization bound')
    return {
        'schema': 'r3472-focus-constructions/v1',
        'status': 'PASS',
        'case_id': 'R8_3_3472',
        'arithmetic': 'exact integers and rational pairs; no floating point',
        'fusion_ring_records': records,
        'commutative_coefficient_choices_A_B_t': [list(x) for x in choices],
        'nonuniform_t7_formal_codegree_polynomial': [1, -371, 2597],
        'rw_parity_residues_count': len(residues),
        'rw_parity_residues': residues,
        'rw_alternating_residues_count': len(alternating),
        'rw_parent_order': 196,
        'required_quotient_order_per_pointed_factor_dimension': 28,
        'required_quotient_order_squared_coefficient': 784,
        'upper_bound_quotient_order_squared_coefficient': 392,
        'categorical_scope': 'RW gamma-input parents; direct ordinary central de-equivariantization; arbitrary pointed tensor factors',
        'general_categorification_status': 'unresolved',
        'new_categorical_model': False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    out = compute()
    path = HERE/'verification.json'
    if args.write:
        path.write_text(json.dumps(out, indent=2)+'\n')
        for a, label in [(1, 'identity'), (-1, 'inversion')]:
            (HERE/f'C7_m2_{label}_tensor.json').write_text(json.dumps(tensor(a), indent=2)+'\n')
    else:
        need(json.loads(path.read_text()) == out, 'Saved verification receipt')
        for a, label in [(1, 'identity'), (-1, 'inversion')]:
            need(json.loads((HERE/f'C7_m2_{label}_tensor.json').read_text()) == tensor(a), 'Saved tensor')
    print('PASS: two complete rank-14 fusion tensors; RW parity and dimension-bound certificates')


if __name__ == '__main__':
    main()
