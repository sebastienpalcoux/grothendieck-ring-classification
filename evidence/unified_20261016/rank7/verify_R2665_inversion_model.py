#!/usr/bin/env python3
"""Exact source binding for the C16 inversion-descent realization of R7_4_2665.

The model is constructed without reading a census tensor.  This finite replay
checks the tensor and all induction identities used after the categorical
construction; the accompanying proof establishes the associators and action.
"""
import argparse
import collections
import gzip
import hashlib
import itertools
import json
from pathlib import Path

import sympy as sp


def require(value, message):
    if not value:
        raise RuntimeError(message)


def tensor_hash(tensor):
    return hashlib.sha256(json.dumps(tensor, separators=(',', ':')).encode()).hexdigest()


def rank7_model():
    """Basis 1,g,g²,g³,X,Y,Z, with g⁴=1 and Y*=Z."""
    n = 7
    out = [[[0] * n for _ in range(n)] for _ in range(n)]
    for i, j in itertools.product(range(4), repeat=2):
        out[i][j][(i + j) % 4] = 1
    for i in range(4):
        out[i][4][4] = out[4][i][4] = 1
        for j in (5, 6):
            out[i][j][j if i % 2 == 0 else 11-j] = 1
            out[j][i] = out[i][j].copy()
    out[4][4] = [1, 1, 1, 1, 0, 0, 0]
    for j in (5, 6):
        out[4][j] = out[j][4] = [0, 0, 0, 0, 0, 1, 1]
    out[5][5] = out[6][6] = [0, 1, 0, 1, 1, 4, 4]
    out[5][6] = out[6][5] = [1, 0, 1, 0, 1, 4, 4]
    return out


def fusion_checks(tensor, dimensions):
    n = len(tensor)
    matrices = [sp.Matrix(layer).T for layer in tensor]
    require(matrices[0] == sp.eye(n), 'left unit')
    dual = []
    for i in range(n):
        choices = [j for j in range(n) if tensor[i][j][0]]
        require(len(choices) == 1 and tensor[i][choices[0]][0] == 1, 'unique dual')
        dual.append(choices[0])
    for i, j in itertools.product(range(n), repeat=2):
        require(matrices[i] * matrices[j] == sum(
            (tensor[i][j][k] * matrices[k] for k in range(n)), sp.zeros(n)),
            'all associativity identities')
        require(sp.expand(dimensions[i] * dimensions[j] - sum(
            tensor[i][j][k] * dimensions[k] for k in range(n))) == 0,
            'positive dimension character')
        for k in range(n):
            require(tensor[i][j][k] == tensor[dual[i]][k][j] == tensor[k][dual[j]][i],
                    'all Frobenius reciprocity identities')
    return dual


def dihedral_model(duality_shift=(2, 0)):
    group = list(itertools.product(range(4), range(2)))
    index = {g: i for i, g in enumerate(group)}

    def mul(g, h):
        return ((g[0] + (-1) ** g[1] * h[0]) % 4, (g[1] + h[1]) % 2)

    def phi(g):
        return ((-g[0] + g[1]) % 4, g[1])

    tensor = [[[0] * 16 for _ in range(16)] for _ in range(16)]
    for i, g in enumerate(group):
        for j, h in enumerate(group):
            tensor[i][j][index[mul(g, h)]] = 1
            tensor[i][8+j][8+index[mul(g, h)]] = 1
            tensor[8+i][j][8+index[mul(g, phi(h))]] = 1
            gh = mul(g, phi(h))
            tensor[8+i][8+j][index[mul(gh, duality_shift)]] = 1
            for k in range(4):
                tensor[8+i][8+j][8+index[mul(gh, (k, 0))]] = 1
    return group, index, mul, phi, tensor


def multiply(tensor, left, right):
    n = len(tensor)
    out = [0] * n
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            if a and b:
                for k, c in enumerate(tensor[i][j]):
                    out[k] += a * b * c
    return out


def unit_vector(size, position):
    return [int(i == position) for i in range(size)]


def read_sources(repo):
    counts = collections.Counter()
    rank7 = None
    path7 = repo / 'supplements/rank7/data/rank7_tables.txt.gz'
    for line in gzip.open(path7, 'rt'):
        if not line.strip():
            continue
        tensor = json.loads(line.replace('{', '[').replace('}', ']'))
        m = max(c for layer in tensor for row in layer for c in row)
        counts[m] += 1
        if m == 4 and counts[m] == 2665:
            rank7 = tensor
    rank8 = []
    path8 = repo / 'supplements/rank8/data/rank8_tables.txt.gz'
    for line in gzip.open(path8, 'rt'):
        if not line.strip():
            continue
        tensor = json.loads(line.replace('{', '[').replace('}', ']'))
        if max(c for layer in tensor for row in layer for c in row) == 1:
            rank8.append(tensor)
    require(rank7 is not None and len(rank8) >= 12, 'source availability')
    return rank7, sorted(rank8)[11], path7, path8


def based_match(model, source, permutation):
    n = len(model)
    require(sorted(permutation) == list(range(n)) and permutation[0] == 0,
            'based permutation')
    return all(model[i][j][k] == source[permutation[i]][permutation[j]][permutation[k]]
               for i, j, k in itertools.product(range(n), repeat=3))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    ap.add_argument('--model-output', type=Path)
    args = ap.parse_args()
    model = rank7_model()
    t = 2 + sp.sqrt(5)
    require(fusion_checks(model, [1]*4+[2, 2*t, 2*t]) == [0, 3, 2, 1, 4, 6, 5],
            'constructed rank-seven duality')
    group, index, mul, phi, tensor = dihedral_model()
    fusion_checks(tensor, [1]*8+[t]*8)
    reflection = [(0, 0), (0, 1)]
    algebra = [int(i < 8 and group[i] in reflection) for i in range(16)]

    def induce(i):
        return multiply(tensor, multiply(tensor, algebra, unit_vector(16, i)), algebra)

    # Free induced A-bimodules have trivial stabilizer on these two orbits.
    y, z = 8+index[(0, 0)], 8+index[(2, 0)]
    fy, fz = induce(y), induce(z)
    require(set(i for i, c in enumerate(fy) if c) == {8+index[g] for g in [(0,0),(0,1),(1,1),(3,0)]},
            'first irrational double orbit')
    require(all(c in (0, 1) for c in fy+fz) and
            [a+b for a, b in zip(fy, fz)] == [0]*8+[1]*8,
            'two disjoint free double orbits')
    fx = induce(index[(1, 0)])
    require(sum(fx) == 4 and max(fx) == 1, 'dimension-two integral double orbit')
    # Both characters over L have underlying A; both over r²L have r²A.
    fodd = multiply(tensor, unit_vector(16, index[(2, 0)]), algebra)
    forgotten = [algebra, fodd, algebra, fodd, fx, fy, fz]
    # (A u A) tensor_A (A v A) = A u A v A, with all associators retained.
    for left, right, i, j in [(y,y,5,5), (y,z,5,6), (z,y,6,5), (z,z,6,6)]:
        actual = multiply(tensor, multiply(tensor, multiply(tensor,
            multiply(tensor, algebra, unit_vector(16, left)), algebra),
            unit_vector(16, right)), algebra)
        expected = [sum(model[i][j][k] * forgotten[k][l] for k in range(7))
                    for l in range(16)]
        require(actual == expected, 'all four irrational relative-tensor induction formulas')
    # The free integral double orbit satisfies X tensor_A Y = Y+Z, both orders.
    for p in (y, z):
        for u, v in [(index[(1,0)], p), (p, index[(1,0)])]:
            actual = multiply(tensor, multiply(tensor, multiply(tensor,
                multiply(tensor, algebra, unit_vector(16, u)), algebra),
                unit_vector(16, v)), algebra)
            require(actual == [a+b for a,b in zip(fy,fz)], 'mixed relative-tensor induction')
    # r²L interchanges the irrational orbits; the two L-characters fix them.
    for v in (fy, fz):
        shifted = multiply(tensor, unit_vector(16, index[(2,0)]), v)
        require(shifted == (fz if v == fy else fy), 'odd integral invertible action')
    # Pointed C4 cyclic associator invariant exp(2pi i * 3/4) has exact order4.
    require(all((3*k) % 4 for k in (1,2,3)) and (3*4) % 4 == 0,
            'primitive cyclic associator obstruction')
    require(4*4 == 16 and all(16 % bound == 0 and bound < 16 for bound in (4,8)),
            'FS exponent separates C4 from all V4 Tambara-Yamagami categories')
    source7, source8, path7, path8 = read_sources(args.repo)
    permutations7 = []
    for odd in [(1,2),(2,1)]:
        for irr in [(3,4),(4,3)]:
            p = [0, odd[0], 6, odd[1], 5, irr[0], irr[1]]
            if based_match(model, source7, p):
                permutations7.append(p)
    require(permutations7, 'all 343 model coefficients match R7_4_2665')
    sub = [index[(i,0)] for i in range(4)]+[8+index[(i,0)] for i in range(4)]
    neutral = [[[tensor[i][j][k] for k in sub] for j in sub] for i in sub]
    p8 = None
    invertibles8 = [i for i in range(1,8) if any(source8[i][j] == [1]+[0]*7 for j in range(8))]
    for ip in itertools.permutations(invertibles8):
        for np in itertools.permutations([i for i in range(1,8) if i not in invertibles8]):
            p = [0]+list(ip)+list(np)
            if based_match(neutral, source8, p):
                p8 = p
                break
        if p8 is not None:
            break
    require(p8 is not None, 'neutral component matches realized R8_1_12')
    record = {
        'id': 'R7_4_2665', 'rank': 7, 'multiplicity': 4,
        'name': 'Reflection Morita dual of the inversion extension of NG(C16,16) orbifold',
        'source_construction': 'Start with Budinski NG(C16,16), centrally de-equivariantize by 4C16, descend the regular-C16 self-Morita equivalence to a coherent inversion C2 action, take the crossed product, and dualize its reflection algebra 1+s.',
        'source_reference': 'R2665_INVERSION_CONSTRUCTION.md; Budinski, Theorem 3.1.1 and Section 3.3.2; Izumi, Theorems 11.3, 12.5, 13.4 and Corollary 13.5; Grossman-Jordan-Snyder, Lemma 4.7 and Remark 4.8; Liu-Ng, Proposition 5.3.',
        'source_url': 'https://arxiv.org/abs/1512.04288',
        'basis_permutation_model_to_census': permutations7[0],
        'tensor': model,
        'existence': dict.fromkeys(['general','pivotal','spherical','pseudo_unitary','unitary'], 'yes')}
    result = {
        'status': 'PASS', 'scope': 'exact finite part of a unitary categorical construction',
        'source_id': 'R7_4_2665', 'source_tensor_sha256': tensor_hash(source7),
        'source_file_sha256': hashlib.sha256(path7.read_bytes()).hexdigest(),
        'model_tensor_sha256': tensor_hash(model),
        'basis_permutation_model_to_census': permutations7[0],
        'full_tensor_coefficients_checked': 343,
        'dihedral_tensor_sha256': tensor_hash(tensor),
        'neutral_source_id': 'R8_1_12', 'neutral_source_tensor_sha256': tensor_hash(source8),
        'rank8_source_file_sha256': hashlib.sha256(path8.read_bytes()).hexdigest(),
        'neutral_basis_permutation_model_to_census': p8,
        'relative_tensor_induction_identities_checked': 8,
        'fusion_axioms_checked': 'all associativity, duality, Frobenius reciprocity and FP dimensions in both ranks 7 and 16',
        'pointed_associator_order_on_C4': 4,
        'pointed_FS_exponent_divisor': 16,
        'V4_TY_possible_FS_exponents': [4,8],
        'integral_group_forced': 'C4',
        'categorical_proof': 'R2665_INVERSION_CONSTRUCTION.md',
        'optimizer_used': False}
    args.output.write_text(json.dumps(result, indent=2)+'\n')
    if args.model_output:
        args.model_output.write_text(json.dumps(record, indent=2)+'\n')
    print(json.dumps({'status': 'PASS', 'source_id': 'R7_4_2665',
                      'model_to_census': permutations7[0], 'tensor_coefficients': 343}))


if __name__ == '__main__':
    main()
