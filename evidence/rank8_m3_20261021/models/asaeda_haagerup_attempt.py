#!/usr/bin/env python3
"""Exact, family-scoped Asaeda--Haagerup model audit.

All 277 baseline tensors are checked against the AH global dimension.
Both known rank-eight AH based tensors are independently reconstructed and
matched against the existing positive catalog. No general exclusion follows.
Default replay is read-only; --write explicitly regenerates the receipt.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse
import hashlib
import itertools
import json
import sympy as s

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
X = s.Symbol('x')
AH_POLY = s.Poly(X*X-272*X+1088, X)
TARGET = 'R8_3_721'

def require(condition, message):
    if not condition:
        raise ValueError(message)

def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':')).encode()).hexdigest()

def add(u, v):
    return (u[0]+v[0], u[1]+v[1])

def mul(u, v):
    return (u[0]*v[0]+17*u[1]*v[1], u[0]*v[1]+u[1]*v[0])

def encoded(u):
    return [[F(a).numerator, F(a).denominator] for a in u]

def dimension_check(R, dims):
    require(dims[0] == (1, 0), 'dimension normalization')
    require(all(a >= 0 and b >= 0 and a+b > 0 for a, b in dims),
            'strict positivity in Q(sqrt17)')
    for i, j in itertools.product(range(8), repeat=2):
        rhs = (0, 0)
        for k in range(8):
            rhs = add(rhs, (R[i][j][k]*dims[k][0], R[i][j][k]*dims[k][1]))
        require(mul(dims[i], dims[j]) == rhs, 'exact dimension character identity')
    D = (0, 0)
    for v in dims:
        D = add(D, mul(v, v))
    require(D == (136, 32), 'AH global dimension identity')
    return {'positive_dimension_character_Qsqrt17': [encoded(v) for v in dims],
            'dimension_products_checked': 64, 'global_dimension_Qsqrt17': encoded(D)}

def dual_and_invertibles(R):
    dual = []
    for i in range(8):
        candidates = [j for j in range(8) if R[i][j][0]]
        require(len(candidates) == 1, 'unique source dual')
        dual.append(candidates[0])
    require(all(R[i][j][0] == int(j == dual[i]) for i, j in itertools.product(range(8), repeat=2)),
            'normalized dual coefficients')
    invertibles = [i for i in range(8) if R[i][dual[i]] == [1]+[0]*7]
    return dual, invertibles

def ah_rank8_tensor(cyclic):
    """GIS Lemmas3.7,3.15: alpha_g rho alpha_h rho = alpha_(g-h)+2 sum alpha_k rho."""
    plus = (lambda a,b: (a+b) % 4) if cyclic else (lambda a,b: a ^ b)
    minus = (lambda a: (-a) % 4) if cyclic else (lambda a: a)
    R = [[[0]*8 for _ in range(8)] for _ in range(8)]
    for g, h in itertools.product(range(4), repeat=2):
        R[g][h][plus(g,h)] = 1
        R[g][4+h][4+plus(g,h)] = 1
        R[4+g][h][4+plus(g,minus(h))] = 1
        R[4+g][4+h][plus(g,minus(h))] = 1
        for k in range(4):
            R[4+g][4+h][4+k] = 2
    require(max(v for a in R for row in a for v in row) == 2, 'AH multiplicity')
    dual, inv = dual_and_invertibles(R)
    require(inv == [0,1,2,3], 'AH invertible group order')
    require(all(R[i][j][k] == R[dual[j]][dual[i]][dual[k]] == R[dual[i]][k][j]
                for i,j,k in itertools.product(range(8),repeat=3)), 'AH reciprocity')
    require(all(sum(R[i][j][a]*R[a][k][b] for a in range(8)) ==
                sum(R[j][k][a]*R[i][a][b] for a in range(8))
                for i,j,k,b in itertools.product(range(8),repeat=4)), 'AH associativity')
    dimension_check(R, [(1,0)]*4+[(4,1)]*4)
    return R

def exact_map(R, S):
    _, inv = dual_and_invertibles(S)
    others = [i for i in range(8) if i not in inv]
    require(len(inv) == 4 and inv[0] == 0, 'catalog AH invertibles')
    for a in itertools.permutations(inv[1:]):
        for b in itertools.permutations(others):
            p = [0]+list(a)+list(b)
            if all(R[i][j][k] == S[p[i]][p[j]][p[k]] for i,j,k in itertools.product(range(8),repeat=3)):
                return p
    raise ValueError('reconstructed AH tensor differs from positive control')

def derive():
    rows = json.loads((HERE.parent/'pipeline/survivors_baseline.json').read_text())
    require(len(rows) == 277 and len({r['id'] for r in rows}) == 277, 'baseline scope')
    records = []
    hits = []
    for row in rows:
        R = row['tensor']
        require(digest(R) == row['tensor_sha256'], 'source tensor binding')
        dual, inv = dual_and_invertibles(R)
        matrices = [s.Matrix(a) for a in R]
        require(all(matrices[dual[i]] == matrices[i].T for i in range(8)), 'Casimir transpose identity')
        C = sum((matrices[i]*matrices[dual[i]] for i in range(8)), s.zeros(8))
        cp = C.charpoly(X).as_poly()
        remainder = cp.rem(AH_POLY)
        record = {'id': row['id'], 'tensor_sha256': row['tensor_sha256'],
                  'casimir_characteristic_polynomial': [int(c) for c in cp.all_coeffs()],
                  'AH_dimension_polynomial_remainder': [int(c) for c in remainder.all_coeffs()],
                  'rank': 8, 'invertibles': inv,
                  'maximum_multiplicity': max(v for a in R for r in a for v in r),
                  'scope': 'known_Asaeda_Haagerup_Morita_family_only',
                  'general_categorification_excluded': False}
        require(record['maximum_multiplicity'] == 3, 'exact multiplicity-three source')
        if remainder.is_zero:
            dims = [(1,0) if i in inv else (4,1) for i in range(8)]
            if row['id'] == TARGET:
                dims = [(1,0),(F(3,2),F(1,2)),(F(3,2),F(1,2)),(4,1),
                        (F(5,2),F(1,2)),(3,1),(F(5,2),F(1,2)),(5,1)]
                require(inv == [0] and dual == [0,2,1,3,4,5,6,7], 'R721 source invariants')
                record['small_dimension_objects_are_self_dual'] = False
                record['GS_Lemma4_5_applicable'] = False
            record.update(dimension_check(R, dims))
            hits.append(row['id'])
            record['family_outcome'] = 'same_global_dimension_but_no_AH_model:AH1_to3_rank_mismatch;AH4_to6_multiplicity_mismatch'
            if row['id'] == TARGET:
                record['additional_AH4_to6_obstruction'] = 'one_invertible_instead_of_four'
        else:
            record['family_outcome'] = 'different_global_dimension_so_no_AH_Morita_model'
        records.append(record)
    require(len(hits) == 14 and TARGET in hits, 'AH-dimension baseline matches changed')
    catalog = {r['id']:r for r in json.loads((ROOT/'supplements/rank8/data/model_catalog.json').read_text())}
    controls = []
    for cyclic, ident, names in [(True,'R8_2_39',['AH4','AH6']), (False,'R8_2_484',['AH5'])]:
        R = ah_rank8_tensor(cyclic)
        row = catalog[ident]
        require(digest(row['tensor']) == row['tensor_sha256'], 'AH positive-control tensor binding')
        p = exact_map(R, row['tensor'])
        controls.append({'categories':names, 'positive_control_id':ident,
                         'positive_control_sha256':row['tensor_sha256'],
                         'independently_constructed_tensor':R,
                         'basis_map_model_to_positive_control':p,
                         'coefficients_checked':512, 'maximum_multiplicity':2})
    return {'schema':'asaeda_haagerup_family_audit_v1',
            'scope':'specific_known_Morita_family_and_R721_extension_dimension_filter_only',
            'references':[
                {'url':'https://arxiv.org/pdf/1202.4396v2',
                 'locators':['Section4.3, Tables1-3, printed p27','Lemma4.5, printed p26'],
                 'input':'AH1,AH2,AH3 have ranks6,9,9 and invertible counts1,2,2; Lemma4.5 requires its stated self-square fusion rule'},
                {'url':'https://arxiv.org/pdf/1501.07324v1',
                 'locators':['Lemma3.4, p14','Lemma3.7, pp16-17','Lemma3.15, p22','Theorem4.21, p37'],
                 'input':'Exactlysix categories in the AH Morita class; AH4,AH5,AH6 have4invertibles,4objects of dimension4+sqrt17; their two based rings have maximum multiplicity2'}],
            'AH_global_dimension':'136+32*sqrt(17)',
            'AH_global_dimension_minimal_polynomial':[1,-272,1088],
            'known_category_rank_and_invertible_count':[
                {'category':'AH1','rank':6,'invertibles':1},
                {'category':'AH2','rank':9,'invertibles':2},
                {'category':'AH3','rank':9,'invertibles':2},
                {'category':'AH4','rank':8,'invertibles':4},
                {'category':'AH5','rank':8,'invertibles':4},
                {'category':'AH6','rank':8,'invertibles':4}],
            'rank8_AH_positive_controls':controls,
            'same_global_dimension_ids':hits,
            'R721_nontrivial_extension_or_equivariantization_filter':
                'Every faithful nontrivial finite-group extension or equivariantization of an AH category has dimension |G|*(136+32*sqrt17), hence differs from R721. Morita duals preserve this dimension. This does not classify de-equivariantizations, modified constructions, or categories outside the known family.',
            'records':records}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    actual = derive()
    target = HERE/'asaeda_haagerup_attempt.json'
    if args.write:
        target.write_text(json.dumps(actual, indent=2)+'\n')
    else:
        require(actual == json.loads(target.read_text()), 'AH-family receipt differs')
    print('PASS:277 exact AH-family comparisons;14 equal dimensions;2 independent positive controls;no exact-M3 AH model.')

if __name__ == '__main__':
    main()
