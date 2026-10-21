#!/usr/bin/env python3
"""Exact source hypotheses for the unitary Haagerup-extension obstruction.

R455_HAAGERUP_EXTENSION_PROOF.md states the categorical inputs and the
fixed-object untwisting argument. No general complex exclusion is claimed.
Default replay is read-only; only --write regenerates the receipt.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse
import hashlib
import itertools
import json

HERE = Path(__file__).resolve().parent
IDENT = 'R8_3_455'
SOURCE_SHA = '358b5323c54c66e80684b34dbe39d7bff44c5fe227bb8fb188794a0a9a722d88'
KIND = 'haagerup_extension_unitary_obstruction'

def require(condition, message):
    if not condition:
        raise ValueError(message)

def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':')).encode()).hexdigest()

def reconstructed_tensor():
    # Basis: 1,g,g^2,rho,g*rho,g^2*rho,Y,Z; Z=rho*Y=Y*rho.
    R = [[[0]*8 for _ in range(8)] for _ in range(8)]
    for g,h in itertools.product(range(3),repeat=2):
        R[g][h][(g+h)%3] = 1
        R[g][3+h][3+(g+h)%3] = 1
        R[3+g][h][3+(g-h)%3] = 1
        R[3+g][3+h][(g-h)%3] = 1
        for k in range(3):
            R[3+g][3+h][3+k] = 1
    for g in range(3):
        for y in (6,7):
            R[g][y][y] = R[y][g][y] = 1
        R[3+g][6][7] = R[6][3+g][7] = 1
        R[3+g][7][6] = R[7][3+g][6] = 1
        R[3+g][7][7] = R[7][3+g][7] = 3
        R[6][6][g] = R[7][7][g] = 1
        R[6][7][3+g] = R[7][6][3+g] = 1
        R[7][7][3+g] = 3
    return R

def add(u,v):
    return tuple(a+b for a,b in zip(u,v))

def mul(u,v):
    # Basis 1,sqrt3,sqrt13,sqrt39; all arithmetic is rational.
    out = [F(0)]*4
    for i,j in itertools.product(range(4),repeat=2):
        common = i & j
        out[i^j] += u[i]*v[j]*(3 if common & 1 else 1)*(13 if common & 2 else 1)
    return tuple(out)

def encoded(v):
    return [[F(a).numerator,F(a).denominator] for a in v]

def certificate(R):
    require(digest(R) == SOURCE_SHA, 'source tensor differs')
    S = reconstructed_tensor()
    p = [0,1,2,3,7,6,4,5]
    require(all(S[i][j][k] == R[p[i]][p[j]][p[k]]
                for i,j,k in itertools.product(range(8),repeat=3)), 'independent full tensor differs')
    neutral = [0,1,2,3,6,7]
    odd = [4,5]
    degree = [int(i in odd) for i in range(8)]
    require(all(not R[i][j][k] or (degree[i]+degree[j])%2 == degree[k]
                for i,j,k in itertools.product(range(8),repeat=3)), 'not a faithful C2 grading')
    require(len(neutral) == 6 and len(odd) == 2 and set(neutral+odd) == set(range(8)), 'graded ranks')
    dual = [next(j for j in range(8) if R[i][j][0]) for i in range(8)]
    require(dual == [0,2,1,3,4,5,6,7], 'source duality')
    inv = [i for i in range(8) if R[i][dual[i]] == [1]+[0]*7]
    require(inv == [0,1,2], 'pointed subgroup')
    require(all(R[g][h] == [int(k == (g+h)%3) for k in range(8)]
                for g,h in itertools.product(range(3),repeat=2)), 'pointed subgroup is not C3')
    Y = 4
    require(all(R[g][Y] == R[Y][g] == [int(k == Y) for k in range(8)] for g in inv),
            'fixed-simple untwisting hypothesis')
    require(R[Y][Y] == [1,1,1,0,0,0,0,0], 'TY square hypothesis')
    require(all(degree[dual[i]] == degree[i] for i in range(8)), 'grading duality')
    dims = [(1,0,0,0)]*3+[(F(3,2),0,F(1,2),0),(0,1,0,0),
            (0,F(3,2),0,F(1,2)),(F(3,2),0,F(1,2),0),(F(3,2),0,F(1,2),0)]
    require(all(all(a >= 0 for a in v) and sum(v)>0 for v in dims), 'positive dimension character')
    for i,j in itertools.product(range(8),repeat=2):
        value = (0,0,0,0)
        for k in range(8):
            value = add(value,tuple(R[i][j][k]*a for a in dims[k]))
        require(value == mul(dims[i],dims[j]), 'dimension character identity')
    component_dimensions = []
    for indices in (neutral,odd):
        total = (0,0,0,0)
        for i in indices:
            total = add(total,mul(dims[i],dims[i]))
        component_dimensions.append(total)
    require(component_dimensions == [(F(39,2),0,F(9,2),0)]*2, 'equal Haagerup component dimensions')
    return {
        'id':IDENT, 'kind':KIND, 'tensor_sha256':digest(R),
        'scope':'unitary_only', 'outcome':'unitary_excluded',
        'unitary_excluded':True, 'general_complex_excluded':False,
        'independently_constructed_tensor':S,
        'basis_map_model_to_source':p,
        'source_coefficients_checked':512,
        'neutral_basis':neutral, 'odd_basis':odd, 'source_C2_degrees':degree,
        'neutral_HI_C3_model_to_source':[0,1,2,3,7,6],
        'neutral_HI_C3_tensor':[[row[:6] for row in a[:6]] for a in S[:6]],
        'neutral_rank':6, 'odd_rank':2, 'duality':dual,
        'pointed_C3_basis':inv, 'pointed_fixed_simple':Y,
        'TY_subring_basis':[0,1,2,4],
        'fixed_simple_square_source_coefficients':R[Y][Y],
        'positive_dimension_character_basis_1_sqrt3_sqrt13_sqrt39':[encoded(v) for v in dims],
        'dimension_products_checked':64,
        'component_dimensions':[encoded(v) for v in component_dimensions],
        'global_dimension':'39+9*sqrt(13)',
        'untwisting_argument':'The fixed simple spans a rank-one Vec(C3,omega) module; its scalar module pentagon forces omega to be a coboundary.',
        'second_cohomology_input':'H^2(C3,C^*)=0, hence Izumi c^(1,2)=0 after c^(0,3)=0.',
        'unitary_neutral_classification':'Izumi Theorems5.9 and9.1: the two untwisted C*-HI(C3) categories are H2 and H3.',
        'Brauer_Picard_input':'Grossman-Snyder Theorem1.5: each H_i has exactly one invertible self-bimodule class, the regular class.',
        'contradiction':{'required_odd_rank':6,'observed_odd_rank':2},
        'general_scope_limitation':'The C* classification is not invoked for arbitrary nonunitary untwisted HI(C3) categorifications.',
    }

def verify(R,saved):
    require(saved == certificate(R), 'Haagerup extension certificate differs')

def record():
    rows = json.loads((HERE.parent/'pipeline/census_m3.json').read_text())
    row = next(r for r in rows if r['id'] == IDENT)
    require(row['tensor_sha256'] == SOURCE_SHA, 'census SHA binding')
    return {'schema':'rank8-haagerup-extension-unitary-v1',
            'proof':'evidence/rank8_m3_20261021/models/R455_HAAGERUP_EXTENSION_PROOF.md',
            'references':[
                {'url':'https://arxiv.org/pdf/1609.07604v2',
                 'author':'Masaki Izumi',
                 'locators':['Section2.1, pp9-12','Definition2.7, p12','Theorem5.9, p36','Section9.2 and Theorem9.1, pp56-57'],
                 'scope':'C*-generalized Haagerup classification after both cohomological obstructions vanish; twisted alternatives are explicitly acknowledged after Definition2.7'},
                {'url':'https://arxiv.org/pdf/1102.2631v2',
                 'authors':'Grossman-Snyder',
                 'locators':['Theorem1.4, p4','Theorem1.5, p5'],
                 'scope':'Known Haagerup H2,H3 are inequivalent unitary categories with the same rank-six rules and trivial Brauer-Picard groups'},
                {'url':'https://arxiv.org/pdf/0909.3140v2',
                 'authors':'Etingof-Nikshych-Ostrik',
                 'locators':['Theorem6.1(i), pp32-33'],
                 'scope':'Every homogeneous component of a faithful finite-group extension is an invertible bimodule over the neutral component'}],
            'certificate':certificate(row['tensor'])}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--write',action='store_true')
    args = parser.parse_args()
    actual = record()
    target = HERE/'r455_haagerup_extension.json'
    if args.write:
        target.write_text(json.dumps(actual,indent=2)+'\n')
    else:
        require(actual == json.loads(target.read_text()), 'saved R455 receipt differs')
    print('PASS: R455 full512 tensor, C2 ranks6+2, fixed-simple untwisting and exact dimensions; unitary-only obstruction.')

if __name__ == '__main__':
    main()
