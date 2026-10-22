#!/usr/bin/env python3
"""Exact input certificate for the regular-module/full-center theorem.

The categorical theorem is proved in MORITA_OBJECT.md. This script checks
its ring-theoretic hypotheses for every class in the complete prior module
classification. It does not construct a module or an algebra structure.
Default execution is read-only; --write regenerates this stage's receipt.
"""
from pathlib import Path
import argparse
import hashlib
import json
import sympy as s

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PRIOR = ROOT / 'evidence/rank8_research_20261022/r982/module_types.json'
PRIOR_SHA = '44d470d2e1cd8620dec52314c1aae9ab282d9cf0aa1f4b823c2b65b50a9eb768'
SOURCE = ROOT / 'evidence/rank8_m3_20261021/pipeline/census_m3.json'
TENSOR_SHA = 'f4a9fb77b3a78e9dcd8370ca9fa822ea331f1b71e3fad7990efdd386445fcd1c'


def need(condition, message):
    if not condition:
        raise ValueError(message)


def integers(matrix):
    need(all(x.is_Integer for x in matrix), 'integral matrix')
    return [[int(x) for x in row] for row in matrix.tolist()]


def run():
    need(hashlib.sha256(PRIOR.read_bytes()).hexdigest() == PRIOR_SHA,
         'complete prior module classification binding')
    prior = json.loads(PRIOR.read_text())
    need(prior['all_indecomposable_module_ranks'] == [8], 'complete module rank input')
    rows = json.loads(SOURCE.read_text())
    row = next(r for r in rows if r['id'] == 'R8_3_982')
    R = row['tensor']
    tensor_sha = hashlib.sha256(json.dumps(R, separators=(',', ':')).encode()).hexdigest()
    need(tensor_sha == TENSOR_SHA == row['tensor_sha256'] == prior['tensor_sha256'],
         'canonical tensor binding')
    N = [s.Matrix(n) for n in R]
    need(all(R[i][j] == R[j][i] for i in range(8) for j in range(8)),
         'commutative source Grothendieck ring')
    need(len(prior['based_module_types']) == 3, 'all three module types present')
    receipts = []
    for typ in prior['based_module_types']:
        cls = typ['class']
        actions = [s.Matrix(a) for a in typ['actions']]
        witnesses = [f for record in prior['records'] for f in record['factorizations']
                     if f.get('nimrep') and f['module_class'] == cls]
        need(bool(witnesses), 'module representative has induction witness')
        first = witnesses[0]
        B = s.Matrix(first['induction_columns']).T
        p = first['permutation_to_class_representative']
        need(sorted(p) == list(range(8)), 'permutation is bijective')
        P = s.zeros(8)
        for i, j in enumerate(p):
            P[i, j] = 1
        W = B * P
        need(W.det() != 0, 'rational regular-module intertwiner invertible')
        need(all(N[i] * W == W * actions[i] for i in range(8)),
             'simultaneous exact regular-module intertwining')
        need(all(N[i].trace() == actions[i].trace() for i in range(8)),
             'independent regular-character equality')
        receipts.append({'module_class': cls, 'induction_witness_count': len(witnesses),
                         'regular_intertwiner': integers(W),
                         'intertwiner_determinant': int(W.det()),
                         'character_values': [int(a.trace()) for a in actions]})
    # In a commutative based ring the spectrum of sum_i N_i N_i^t is the
    # complete multiset of formal codegrees, each irreducible character once.
    F = sum((n * n.T for n in N), s.zeros(8))
    t = s.Symbol('t')
    codegree_polynomial = s.Poly(F.charpoly(t).as_expr(), t)
    need(s.factor(codegree_polynomial.as_expr()) ==
         (t*t-32*t+128)**2 * (t**4-576*t**3+11520*t*t-73728*t+147456),
         'formal-codegree polynomial')
    noncommutative_controls = []
    for index in [928, 941, 1154]:
        other = next(r for r in rows if r['id'] == f'R8_3_{index}')
        Q = other['tensor']
        i, j = next((i, j) for i in range(8) for j in range(8) if Q[i][j] != Q[j][i])
        noncommutative_controls.append({'id': other['id'], 'tensor_sha256': other['tensor_sha256'],
            'noncommuting_basis_pair': [i, j], 'ij': Q[i][j], 'ji': Q[j][i]})
    return {'kind': 'R982_regular_module_full_center_hypothesis_certificate',
            'status': 'PASS', 'tensor_sha256': tensor_sha,
            'complete_prior_module_classification_sha256': PRIOR_SHA,
            'all_module_classes_regular_over_Q': receipts,
            'source_ring_commutative': True,
            'formal_codegree_polynomial_coefficients': [int(c) for c in codegree_polynomial.all_coeffs()],
            'formal_codegree_factorization': str(s.factor(codegree_polynomial.as_expr())),
            'noncommutative_Morita_partner_obstructions': noncommutative_controls,
            'categorical_conclusion': 'Every Morita partner has a commutative Grothendieck ring of rank 8; its canonical Lagrangian object has the same underlying center object and the same formal codegrees.',
            'scope': 'Every complex categorification, using the independently proved pseudo-unitary Galois-conjugate gate.',
            'limitation': 'Object isomorphism is not algebra isomorphism, a based-ring isomorphism, or a construction/exclusion of R982.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    result = run()
    path = HERE / 'morita_object.json'
    if args.write:
        path.write_text(json.dumps(result, indent=2) + '\n')
    else:
        need(result == json.loads(path.read_text()), 'saved receipt matches exact calculation')
    print('PASS: all three complete module types are regular over Q; every Morita partner must have commutative rank-eight Grothendieck ring. No associator claimed.')
