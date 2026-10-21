#!/usr/bin/env python3
"""Exact hypotheses for the scoped Izumi--Xu inversion obstruction.

The source-bound categorical argument is in R436_INVERSION_PROOF.md. This
verifier independently constructs the abstract crossed *ring*, checks all
512 source coefficients, and records the distinction between a unitary
obstruction and the still-open general complex categorification problem.
Default replay is read-only; --write regenerates the deterministic receipt.
"""
from pathlib import Path
import argparse
import hashlib
import itertools
import json

HERE = Path(__file__).resolve().parent
IDENT = 'R8_3_436'
SOURCE_SHA = '0f6d68de67a7287db7dd32a786237f7af9f35ec7c26b3ada2ba50012ff5455c7'
KIND = 'izumi_xu_inversion_unitary_obstruction'

def require(condition, message):
    if not condition:
        raise ValueError(message)

def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':')).encode()).hexdigest()

def near_group():
    A = [[[0] * 4 for _ in range(4)] for _ in range(4)]
    for i, j in itertools.product(range(3), repeat=2):
        A[i][j][(i+j) % 3] = 1
    for i in range(3):
        A[i][3][3] = A[3][i][3] = 1
    A[3][3] = [1, 1, 1, 3]
    return A

def certificate(R):
    require(digest(R) == SOURCE_SHA, 'wrong source tensor')
    A = near_group()
    p = [0, 2, 1, 3]
    require(all(p[p[i]] == i for i in range(4)), 'inversion is not involutive')
    require(all(A[i][j][k] == A[p[i]][p[j]][p[k]]
                for i, j, k in itertools.product(range(4), repeat=3)),
            'inversion is not a based-ring automorphism')
    S = [[[0] * 8 for _ in range(8)] for _ in range(8)]
    for i, e, j, f, k in itertools.product(range(4), range(2), range(4), range(2), range(4)):
        S[2*i+e][2*j+f][2*k+(e+f) % 2] = A[i][p[j] if e else j][k]
    model_to_source = [0, 3, 1, 7, 2, 6, 5, 4]
    require(sorted(model_to_source) == list(range(8)), 'basis map is not a permutation')
    require(all(S[i][j][k] == R[model_to_source[i]][model_to_source[j]][model_to_source[k]]
                for i, j, k in itertools.product(range(8), repeat=3)), 'crossed tensor differs')
    neutral = [0, 1, 2, 5]
    require(all(R[i][j][k] == 0 for i in neutral for j in neutral
                for k in range(8) if k not in neutral), 'neutral subset is not closed')
    require([[[R[i][j][k] for k in neutral] for j in neutral] for i in neutral] == A,
            'neutral tensor is not NG(C3,3)')
    def unique_product(i, j):
        require(sum(R[i][j]) == 1, 'product is not simple')
        return R[i][j].index(1)
    g, t = 1, 3
    require(unique_product(t, t) == 0, 'odd invertible does not square to 1')
    require(unique_product(g, g) == 2 and unique_product(2, g) == 0, 'wrong C3 subgroup')
    conjugation = [unique_product(unique_product(t, i), t) for i in neutral]
    require(conjugation == [0, 2, 1, 5], 'conjugation does not invert C3')
    return {
        'kind': KIND,
        'id': IDENT,
        'tensor_sha256': digest(R),
        'scope': 'unitary_only',
        'outcome': 'unitary_excluded',
        'unitary_excluded': True,
        'general_complex_excluded': False,
        'neutral_basis': neutral,
        'neutral_tensor': A,
        'neutral_fusion_rule': 'X^2=1+g+g^2+3X; g^3=1; gX=Xg=X',
        'odd_invertible': t,
        'conjugation_on_neutral_basis': conjugation,
        'abstract_crossed_action': p,
        'abstract_crossed_tensor': S,
        'basis_map_model_to_source': model_to_source,
        'basis_map_source_to_model': [model_to_source.index(i) for i in range(8)],
        'source_coefficients_checked': 512,
        'literature_input': 'Every C*-NG(C3,3) category has trivial tensor automorphism group.',
        'construction_outcome': 'The exact based-ring inversion cannot lift on either known unitary Izumi-Xu category.',
        'general_scope_limitation': 'The cited C* classification does not exhaust all complex NG(C3,3) categorifications.',
    }

def verify(R, saved):
    require(saved == certificate(R), 'Izumi-Xu inversion certificate differs')

def record():
    rows = json.loads((HERE.parent / 'pipeline/census_m3.json').read_text())
    row = next(r for r in rows if r['id'] == IDENT)
    require(row['tensor_sha256'] == SOURCE_SHA, 'census source SHA differs')
    return {
        'schema': 'rank8-izumi-xu-inversion-v1',
        'proof': 'evidence/rank8_m3_20261021/models/R436_INVERSION_PROOF.md',
        'references': [
            {'url': 'https://arxiv.org/pdf/1512.04288v2',
             'author': 'Masaki Izumi',
             'locators': ['Theorem9.1, p71', 'Example9.4, p72', 'Example13.7, p123', 'Section13.3, p128', 'Remark9.2, pp71-72'],
             'scope': 'C* classification and tensor automorphisms; Remark9.2 discusses the unproved general nonunitary extension'},
            {'url': 'https://arxiv.org/pdf/1211.6414v2',
             'author': 'Grossman-Jordan-Snyder',
             'locators': ['Section4.2 following Remark4.10, p10', 'Remark4.11, p10'],
             'scope': 'Known Izumi-Xu categories have no outer tensor automorphisms; no claim classifying all complex near-group categorifications'},
        ],
        'certificate': certificate(row['tensor']),
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    actual = record()
    target = HERE / 'r436_inversion_attempt.json'
    if args.write:
        target.write_text(json.dumps(actual, indent=2) + '\n')
    else:
        require(actual == json.loads(target.read_text()), 'saved scoped receipt differs')
    print('PASS: R8_3_436 exact NG(C3,3) crossed tensor, 512 coefficients; unitary inversion obstruction only.')

if __name__ == '__main__':
    main()
