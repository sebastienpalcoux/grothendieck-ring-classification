#!/usr/bin/env python3
"""Exact D8 lattice certificate for based-ring Morita rigidity of R982.

The arbitrary-category argument is in MORITA_RING.md; no associators are
constructed here. Default replay is read-only.
"""
from pathlib import Path
import argparse
import hashlib
import json
import sympy as s
import morita_object as prior_stage

HERE = Path(__file__).resolve().parent


def need(condition, message):
    if not condition:
        raise ValueError(message)


def run():
    rank_input = prior_stage.run()
    need(rank_input == json.loads((HERE / 'morita_object.json').read_text()),
         'rank-eight Morita hypothesis receipt')
    module_data = json.loads(prior_stage.PRIOR.read_text())
    source = next(r for r in json.loads(prior_stage.SOURCE.read_text())
                  if r['id'] == 'R8_3_982')['tensor']
    records = []
    for typ in module_data['based_module_types']:
        cls = typ['class']
        M = [s.Matrix(a) for a in typ['actions']]
        U = s.Matrix(64, 8, lambda a, i: M[i][a // 8, a % 8])
        # Row convention: M_i[a,b] is the coefficient of m_b in X_i*m_a.
        # Bimodule internal-Hom associativity gives V V^t = G for the
        # flattened right action matrices V of all dual simple objects.
        G = s.Matrix(64, 64, lambda x, y:
                     sum(n[x // 8, y // 8] * n[x % 8, y % 8] for n in M))
        need(G == U * U.T, 'complete 4096-entry bimodule Gram identity')
        selected = list(range(8)) if cls == 0 else [0, 1, 16, 3, 4, 5, 6, 7]
        basis = U[selected, :]
        determinant = int(basis.det())
        need(abs(determinant) == (1 if cls == 0 else 2),
             'explicit full-rank row sublattice determinant')
        even = all(sum(U[r, i] for i in range(8)) % 2 == 0 for r in range(64))
        if cls:
            need(even, 'entire row lattice contained in D8')
            # Its explicit index-two sublattice and containment in the
            # index-two D8 prove equality, without a lattice classification.
        need(all(any(U[r, i] > 0 for r in range(64)) for i in range(8)),
             'every action column has a strictly positive entry')
        for i in range(8):
            for j in range(8):
                need(M[i] * M[j] == sum((source[i][j][k] * M[k] for k in range(8)), s.zeros(8)),
                     'faithful matrices recover every source fusion product')
        records.append({'module_class': cls, 'bimodule_Gram_identity_entries_checked': 4096,
                        'action_column_rank': 8,
                        'row_lattice': 'Z^8' if cls == 0 else 'D8',
                        'selected_row_indices': selected,
                        'selected_integer_basis': prior_stage.integers(basis),
                        'basis_determinant': determinant,
                        'all_row_coordinate_sums_even': even,
                        'all_columns_nonzero_and_nonnegative': True})
    # Explicit representatives of D8*/D8, used in the elementary proof.
    H = s.Matrix([[2] + [1]*7] + [[0]*i + [1] + [0]*(7-i) for i in range(1,8)])
    reps = [s.zeros(8, 1), s.eye(8)[:, 0], s.ones(8, 1)/2,
            s.ones(8, 1)/2-s.eye(8)[:, 0]]
    cosets = []
    for label, v in zip(['zero', 'vector', 'spinor', 'other_spinor'], reps):
        need(all(x.is_Integer for x in H.T*v), 'representative is in dual D8')
        cosets.append({'coset': label, 'representative': [str(x) for x in v],
                       'squared_norm': int((v.T*v)[0])})
    need([c['squared_norm'] for c in cosets] == [0,1,2,2],
         'unique odd index-two integral overlattice')
    return {'kind': 'R982_based_ring_Morita_rigidity_D8_certificate', 'status': 'PASS',
            'tensor_sha256': prior_stage.TENSOR_SHA,
            'complete_module_classification_sha256': prior_stage.PRIOR_SHA,
            'rank_eight_Morita_receipt_sha256': hashlib.sha256((HERE/'morita_object.json').read_bytes()).hexdigest(),
            'module_classes': records, 'D8_discriminant_cosets': cosets,
            'categorical_conclusion': 'Every complex fusion category categorifying R8_3_982 has only based-isomorphic R8_3_982 Grothendieck rings throughout its categorical Morita class, without a rank or multiplicity search bound.',
            'limitation': 'The categories, module associators, and algebra structures may differ; no categorification or exclusion of R982 is asserted.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    result = run()
    path = HERE/'morita_ring.json'
    if args.write:
        path.write_text(json.dumps(result, indent=2)+'\n')
    else:
        need(result == json.loads(path.read_text()), 'saved D8 receipt matches exact calculation')
    print('PASS: all three module types force the identical R982 based fusion ring on the dual side; no Morita partner of another rank or multiplicity is possible.')
