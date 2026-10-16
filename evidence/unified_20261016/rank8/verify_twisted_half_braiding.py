"""Source-bound inputs to the pointed-support twisted-half-braiding obstruction.

The categorical coherence argument is in TWISTED_HALF_BRAIDING_OBSTRUCTION.md.
This verifier uses only integer arithmetic and the Python standard library.
"""
import argparse
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
    rings = sorted((r for r in rings if max(flat(r)) == 2), key=flat)
    ledger = {row['id']: row for row in json.loads(
        (root / 'supplements/rank8/data/decisions.json').read_text())}
    unit_vectors = [[int(k == i) for k in range(8)] for i in range(8)]
    receipts = []
    for index, neutral, x, epsilon in [(314, [0, 7, 1, 2], 3, 1),
                                      (432, [0, 3, 4, 5], 6, 0)]:
        name = f'R8_2_{index}'
        ring = rings[index - 1]
        digest = hashlib.sha256(json.dumps(ring, separators=(',', ':')).encode()).hexdigest()
        require(digest == ledger[name]['tensor_sha256'], f'{name}: source hash')
        require(neutral[0] == 0, 'neutral unit')
        g, r, gr = neutral[1:]
        outside = [i for i in range(8) if i not in neutral]
        require(all(ring[a][b][c] == 0 for a in neutral for b in neutral for c in outside),
                'neutral closure')
        require(all(ring[a][b][c] == ring[b][a][c] == 0
                    for a in neutral for b in outside for c in neutral), 'complement is a bimodule')
        # All 64 coefficients of the rank-four ordinary/pseudo-PSU(2)_6 ring.
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
                    expected[(i - 2) ^ (j - 2) ^ epsilon] = 1
                    expected[2] = expected[3] = 1
                require([ring[neutral[i]][neutral[j]][k] for k in neutral] == expected,
                        'neutral multiplication')
        module_labels = []
        for a in neutral:
            require(sum(ring[a][x]) == 1, 'aX simple')
            module_labels.append(ring[a][x].index(1))
        require(sorted(module_labels) == outside, '(-)X gives a based bijection D to M')
        dual_x = next(j for j in range(8) if ring[x][j][0])
        require([ring[x][dual_x][a] for a in neutral] == [1, 0, 0, 0],
                'internal end over D is the tensor unit')
        f = {neutral[i]: neutral[j] for i, j in enumerate([0, 1, 3, 2])}
        require(all(ring[x][a] == ring[f[a]][x] for a in neutral),
                'right action induces the label flip')
        require(all(ring[f[a]][f[b]][f[c]] == ring[a][b][c]
                    for a in neutral for b in neutral for c in neutral),
                'F is a based ring automorphism')
        gx = module_labels[1]
        expected_square = [int(i == neutral[epsilon]) + int(i == x) + int(i == gx)
                           for i in range(8)]
        require(ring[x][x] == expected_square, 'X squared has M component (1+g)X')
        permutations = {}
        for a in neutral:
            permutation = []
            for h in [0, g]:
                matches = [j for j, k in enumerate([0, g])
                           if ring[h][a] == ring[f[a]][k]]
                require(len(matches) == 1, 'unique support matching for twisted half-braiding')
                permutation.append(matches[0])
            permutations[a] = permutation
        require(permutations[0] == permutations[g] == [0, 1], 'pointed objects fix support')
        require(permutations[r] == permutations[gr] == [1, 0], 'noninvertibles swap support')
        doubled = [permutations[r][permutations[r][i]] for i in range(2)]
        require(doubled == [0, 1] and doubled != permutations[r], 'swap squared versus swap')
        require(ring[r][r][r] == 1, 'nonzero channel r to r tensor r')
        receipts.append({'id': name, 'tensor_sha256': digest,
                         'neutral_basis_1_g_r_gr': neutral,
                         'generator_X': x, 'module_basis_aX': module_labels,
                         'X_square_neutral_part': neutral[epsilon],
                         'X_square_module_part': [x, gx],
                         'F_on_neutral_basis': [0, 1, 3, 2],
                         'pointed_support_permutations': {str(k): v for k, v in permutations.items()},
                         'nonzero_r_to_r_squared_channel': 1,
                         'obstructed_support_identity': 'swap = swap squared',
                         'general_exclusion': True})
    print(json.dumps({'status': 'PASS',
                      'criterion': 'pointed_support_twisted_half_braiding',
                      'cases': receipts,
                      'scope': 'exact source inputs; categorical coherence proof is separate'}, indent=2))


if __name__ == '__main__':
    main()
