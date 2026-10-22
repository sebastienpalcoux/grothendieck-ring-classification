#!/usr/bin/env python3
"""Exact E21 graph reconstruction and R8_3_982 neutral-component identification.

The category exists by the SU(3)_21 into E7_1 conformal embedding; see
E21_MODEL.md. This certificate identifies its fusion rules, not merely a
numerically compatible dimension list. Default replay is read-only.
"""
from pathlib import Path
import argparse
import hashlib
import json
import numpy as np
import sympy as s

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SOURCE = ROOT / 'evidence/rank8_m3_20261021/pipeline/census_m3.json'
TENSOR_SHA = 'f4a9fb77b3a78e9dcd8370ca9fa822ea331f1b71e3fad7990efdd386445fcd1c'
PERM = [0, 2, 3, 4, 5, 1, 7, 6]


def need(condition, message):
    if not condition:
        raise ValueError(message)


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':')).encode()).hexdigest()


def integers(matrix):
    need(all(x.is_Integer for x in matrix), 'integral matrix')
    return [[int(x) for x in row] for row in matrix.tolist()]


def run():
    graph = json.loads((HERE / 'e21_graph.json').read_text())
    labels, grades = graph['vertex_labels'], graph['triality']
    edges = graph['directed_edges']
    need(len(labels) == len(set(labels)) == 24, '24 distinct source vertices')
    need(len(edges) == len(set(map(tuple, edges))) == 60, '60 distinct source edges')
    need(grades == [0]*8 + [1]*8 + [2]*8, 'three triality classes of size eight')
    A = s.zeros(24)
    for i, j in edges:
        need((grades[j]-grades[i]) % 3 == 1, 'oriented triality of source edge')
        A[i, j] = 1
    need(A*A.T == A.T*A, 'normal fundamental fusion graph')
    triangles = int(s.trace(A**3)/3)
    need(triangles == 40, '40 oriented triangles in source')
    monomials, matrices, evaluation, rank_by_degree = [], [], [], []
    for degree in range(7):
        for a in range(degree+1):
            b = degree-a
            H = A**a * A.T**b
            candidate = evaluation + [list(H[0, :])]
            if s.Matrix(candidate).rank() > len(evaluation):
                monomials.append([a, b])
                matrices.append(H)
                evaluation = candidate
        rank_by_degree.append(len(evaluation))
    need(rank_by_degree == [1, 3, 6, 10, 15, 21, 24], 'cyclic unit evaluation ranks')
    B = s.Matrix(evaluation)
    C = B.inv()
    F = [sum((C[i, j]*matrices[j] for j in range(24)), s.zeros(24))
         for i in range(24)]
    tensor = [integers(x) for x in F]
    need(all(x >= 0 for n in tensor for row in n for x in row),
         'all 13824 source fusion coefficients are nonnegative integers')
    need(F[0] == s.eye(24), 'source vertex 1_1 is the tensor unit')
    need(F[8] == A and F[16] == A.T, 'source fundamental and dual generators')
    need(all(F[i][0, j] == int(i == j) for i in range(24) for j in range(24)),
         'unit row labels every simple')
    dual = []
    for i in range(24):
        candidates = [j for j in range(24) if F[i].T == F[j]]
        need(len(candidates) == 1, 'unique dual determined by transposition')
        dual.append(candidates[0])
    max_coefficient = max(x for n in tensor for row in n for x in row)
    # Integer arithmetic is exact: each tested entry is a sum of at most
    # 24 products, bounded far below the signed-int64 overflow threshold.
    need(24*max_coefficient**2 < 2**63, 'exact integer matrix product bound')
    N = np.asarray(tensor, dtype=np.int64)
    for i in range(24):
        for j in range(24):
            need(np.array_equal(N[i, j], N[j, i]), 'commutative source fusion rules')
            need(np.array_equal(N[i] @ N[j], np.tensordot(N[i, j], N, axes=1)),
                 'all 331776 associativity matrix entries')
            need(int(N[i, j, 0]) == int(j == dual[i]), 'based duality normalization')
            for k in range(24):
                need(not N[i, j, k] or grades[k] == (grades[i]+grades[j]) % 3,
                     'exact faithful Z3 grading')
    neutral = [[[int(N[i, j, k]) for k in range(8)] for j in range(8)]
               for i in range(8)]
    source = next(r for r in json.loads(SOURCE.read_text()) if r['id'] == 'R8_3_982')
    R = source['tensor']
    need(digest(R) == TENSOR_SHA == source['tensor_sha256'], 'canonical tensor binding')
    need(all(R[i][j][k] == neutral[PERM[i]][PERM[j]][PERM[k]]
             for i in range(8) for j in range(8) for k in range(8)),
         'all 512 canonical fusion coefficients match the neutral component')
    need(max(x for a in neutral for b in a for x in b) == 3,
         'neutral component has multiplicity exactly three')
    # Exact dimensions from Section 4.6 of the graph source, expressed as
    # g[a,b,c,d]=(a+b sqrt(2)+c sqrt(3)+d sqrt(6))/2.
    coeffs = [[2,0,0,0], [4,2,2,2], [4,4,2,2], [4,4,2,2],
              [6,4,4,2], [6,4,4,2], [4,2,2,2], [2,0,0,0],
              [2,1,0,1], [4,1,2,1], [6,5,4,3], [4,3,2,1],
              [4,3,2,1], [6,5,4,3], [4,1,2,1], [2,1,0,1],
              [2,1,0,1], [4,1,2,1], [6,5,4,3], [4,3,2,1],
              [4,3,2,1], [6,5,4,3], [4,1,2,1], [2,1,0,1]]
    radicals = [s.Integer(1), s.sqrt(2), s.sqrt(3), s.sqrt(6)]
    dims = s.Matrix([sum(v*r for v, r in zip(c, radicals))/2 for c in coeffs])
    delta = 1+(s.sqrt(2)+s.sqrt(6))/2
    need(all(s.expand(x) == 0 for x in A*dims-delta*dims), 'exact positive Perron vector')
    need(all(c >= 0 for row in coeffs for c in row), 'manifestly positive dimension vector')
    for i in range(24):
        need(all(s.expand(x) == 0 for x in F[i]*dims-dims[i]*dims),
             'all source dimension homomorphism identities')
    D = 144+96*s.sqrt(2)+80*s.sqrt(3)+56*s.sqrt(6)
    grade_masses = [s.expand(sum(dims[i]**2 for i in range(24) if grades[i] == g))
                    for g in range(3)]
    need(grade_masses == [D]*3, 'each homogeneous component has target dimension')
    need(list(N[8,16]) == [int(i in [0,1]) for i in range(24)],
         'fundamental internal end is 1 plus canonical X5')
    module_source = ROOT/'evidence/rank8_research_20261022/r982/module_types.json'
    module_sha = '44d470d2e1cd8620dec52314c1aae9ab282d9cf0aa1f4b823c2b65b50a9eb768'
    need(hashlib.sha256(module_source.read_bytes()).hexdigest() == module_sha,
         'complete prior module classification binding')
    module_types = json.loads(module_source.read_text())['based_module_types']
    module_matches = []
    for grade, cls, permutation in [(1,2,[0,2,7,4,5,6,3,1]),
                                     (2,1,[0,3,6,5,4,7,2,1])]:
        actions = next(t['actions'] for t in module_types if t['class'] == cls)
        need(all(int(N[PERM[i], 8*grade+a, 8*grade+b]) ==
                 actions[i][permutation[a]][permutation[b]]
                 for i in range(8) for a in range(8) for b in range(8)),
             'source homogeneous component matches prior nonregular module type')
        module_matches.append({'triality': grade, 'prior_module_class': cls,
                               'local_source_to_prior_vertex': permutation,
                               'action_entries_checked': 512})
    fusion_payload = {'vertex_labels': labels, 'triality': grades,
                      'dual': dual, 'tensor': tensor,
                      'neutral_vertex_indices': list(range(8)),
                      'neutral_tensor': neutral,
                      'canonical_R8_3_982_to_neutral_vertex': PERM}
    receipt = {
        'kind': 'E21_neutral_component_R8_3_982_exact_identification', 'status': 'PASS',
        'source_graph_sha256': hashlib.sha256((HERE/'e21_graph.json').read_bytes()).hexdigest(),
        'source_pdf_sha256': graph['source_pdf_sha256'],
        'canonical_tensor_sha256': TENSOR_SHA,
        'source_graph_vertex_count': 24, 'source_graph_edge_count': 60,
        'source_graph_oriented_triangle_count': triangles,
        'unit_evaluation_rank_by_total_degree': rank_by_degree,
        'independent_monomials_A_power_At_power': monomials,
        'unit_evaluation_matrix': integers(B),
        'unit_evaluation_determinant': int(B.det()),
        'all_source_fusion_coefficients_nonnegative_integral': True,
        'source_fusion_tensor_sha256': digest(tensor),
        'source_fusion_maximum_coefficient': max_coefficient,
        'source_associativity_entries_checked': 24**4,
        'source_duality': dual,
        'faithful_grading': 'Z/3Z',
        'source_dimension_coefficients_in_1_sqrt2_sqrt3_sqrt6_divided_by_2': coeffs,
        'homogeneous_component_dimension': str(D),
        'total_dimension': str(3*D),
        'neutral_rank': 8, 'neutral_maximum_coefficient': 3,
        'neutral_tensor_sha256': digest(neutral),
        'canonical_to_neutral_vertex_indices': PERM,
        'canonical_to_source_labels': [labels[i] for i in PERM],
        'canonical_structure_constants_checked': 512,
        'fundamental_internal_end_canonical': 'X0 + X5',
        'complete_module_classification_sha256': module_sha,
        'homogeneous_component_based_module_identifications': module_matches,
        'categorical_conclusion': 'The neutral component of the unitary E21 chiral fusion category from SU(3)_21 into E7_1 categorifies R8_3_982.',
        'scope': 'The integer graph reconstruction identifies a category whose existence is established independently by the conformal embedding, not by these ring checks alone.'}
    return receipt, fusion_payload


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    receipt, tensor = run()
    for filename, payload in [('e21_model.json', receipt), ('e21_fusion_tensor.json', tensor)]:
        path = HERE/filename
        if args.write:
            path.write_text(json.dumps(payload, indent=2)+'\n')
        else:
            need(payload == json.loads(path.read_text()), 'saved '+filename+' matches exact replay')
    print('PASS: E21 neutral component matches every R8_3_982 fusion coefficient; unitary model identified.')
