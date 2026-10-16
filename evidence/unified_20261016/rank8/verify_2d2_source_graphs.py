"""Bind the four 2D2 graph-pair obstructions to complete census tensors.

This standard-library checker establishes only the exact tensor hypotheses.
The algebraic planar-algebra rigidity theorem is proved separately.
"""
import argparse
from collections import deque
from fractions import Fraction as F
import gzip
import hashlib
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def flat(ring):
    return tuple(v for matrix in ring for row in matrix for v in row)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', type=Path, required=True)
    root = parser.parse_args().repo.resolve()
    with gzip.open(root / 'supplements/rank8/data/rank8_tables.txt.gz', 'rt') as stream:
        rings = [json.loads(line.replace('{', '[').replace('}', ']')) for line in stream]
    rings = sorted((ring for ring in rings if max(flat(ring)) == 2), key=flat)
    ledger = {entry['id']: entry for entry in json.loads(
        (root / 'supplements/rank8/data/decisions.json').read_text())}
    edges = {(0, 1), (1, 2), (2, 3), (2, 4), (3, 5), (4, 5), (5, 6), (6, 7)}
    even, odd = [0, 2, 5, 7], [1, 3, 4, 6]
    adjacency = {v: [] for v in range(8)}
    for a, b in edges:
        adjacency[a].append(b)
        adjacency[b].append(a)
    depths = {0: 0}
    queue = deque([0])
    while queue:
        for neighbor in adjacency[queue.popleft()]:
            if neighbor not in depths:
                depths[neighbor] = min(depths[v] for v in adjacency[neighbor] if v in depths) + 1
                queue.append(neighbor)
    require([depths[i] for i in range(8)] == [0, 1, 2, 3, 3, 4, 5, 6], 'rooted graph depths')
    # Graph weights are in Q(sqrt(5)); odd PF weights are divided by delta.
    def add(a, b):
        return (a[0] + b[0], a[1] + b[1])
    def mul(a, b):
        return (a[0] * b[0] + 5 * a[1] * b[1], a[0] * b[1] + a[1] * b[0])
    weights = [(F(1), F(0)), (F(1), F(0)), (F(2), F(1)),
               (F(1, 2), F(1, 2)), (F(1, 2), F(1, 2)),
               (F(2), F(1)), (F(1), F(0)), (F(1), F(0))]
    for v in range(8):
        total = (F(0), F(0))
        for w in adjacency[v]:
            total = add(total, weights[w])
        expected = weights[v] if v in even else mul((F(3), F(1)), weights[v])
        require(total == expected, 'PF weights')
    # Fixed graph vertex order: tail, tail, diamond, upper, lower,
    # opposite diamond, tail, endpoint.
    cases = [(152, [0, 1, 5, 3, 4, 7, 2, 6]),
             (153, [0, 1, 5, 3, 4, 7, 2, 6]),
             (166, [0, 3, 7, 1, 2, 6, 4, 5]),
             (495, [0, 2, 6, 4, 5, 3, 7, 1])]
    receipts = []
    for index, mapping in cases:
        name = f'R8_2_{index}'
        ring = rings[index - 1]
        digest = hashlib.sha256(json.dumps(ring, separators=(',', ':')).encode()).hexdigest()
        require(digest == ledger[name]['tensor_sha256'], f'{name} source tensor hash')
        require(sorted(mapping) == list(range(8)) and mapping[0] == 0, 'based bijection')
        neutral = [mapping[i] for i in even]
        odd_labels = [mapping[i] for i in odd]
        degrees = [int(i in odd_labels) for i in range(8)]
        require(all(degrees[k] == (degrees[i] + degrees[j]) % 2
                    for i in range(8) for j in range(8) for k in range(8)
                    if ring[i][j][k]), f'{name} faithful C2 grading')
        x, r, gr, g = [mapping[i] for i in [1, 2, 5, 7]]
        duals = [next(j for j in range(8) if ring[i][j][0]) for i in range(8)]
        target = [int(i in [0, r]) for i in range(8)]
        require(ring[x][duals[x]] == target == ring[duals[x]][x], f'{name} internal ends')
        # Neutral ordered basis (1,g,r,gr) has g^2=1, gr=rg,
        # r^2=1+2r+2gr; this verifies all 4^3 neutral coefficients.
        qbasis = [0, g, r, gr]
        for i in range(4):
            for j in range(4):
                expected = [0] * 4
                if i < 2 and j < 2:
                    expected[i ^ j] = 1
                elif i < 2:
                    expected[2 + (i ^ (j - 2))] = 1
                elif j < 2:
                    expected[2 + ((i - 2) ^ j)] = 1
                else:
                    expected[(i - 2) ^ (j - 2)] = 1
                    expected[2] = expected[3] = 2
                require([ring[qbasis[i]][qbasis[j]][k] for k in qbasis] == expected,
                        f'{name} neutral 2D2 multiplication')
        generated = {0, r}
        while True:
            enlarged = generated | {k for i in generated for j in generated
                                    for k in range(8) if ring[i][j][k]}
            if enlarged == generated:
                break
            generated = enlarged
        require(generated == set(neutral), f'{name} both internal ends generate entire even category')
        for i in even:
            for j in odd:
                expected = int(tuple(sorted((i, j))) in edges)
                require(ring[mapping[i]][x][mapping[j]] == expected,
                        f'{name} left module principal graph')
                require(ring[x][mapping[i]][mapping[j]] == expected,
                        f'{name} right module principal graph')
        receipts.append({'id': name, 'tensor_sha256': digest,
                         'graph_vertices_to_census_zero_based': mapping,
                         'neutral_basis_1_g_r_gr': qbasis,
                         'odd_generator': x, 'odd_generator_dual': duals[x],
                         'faithful_C2_grading_checked': True,
                         'left_and_right_graph': '2D2',
                         'both_even_parts_generated': True,
                         'both_even_ranks': 4})
    print(json.dumps({'status': 'PASS', 'graph_edges': sorted(edges),
                      'rooted_depths': [depths[i] for i in range(8)],
                      'graph_modulus_squared': '3+sqrt(5)',
                      'PF_weights_verified_exactly': True,
                      'cases': receipts,
                      'scope': 'exact tensor hypotheses only; algebraic planar-algebra rigidity is a separate proof'}, indent=2))


if __name__ == '__main__':
    main()
