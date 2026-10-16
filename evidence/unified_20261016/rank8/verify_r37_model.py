"""Exact census identification of the nonsplit 2D2 extension and R170 scope.

The construction and automorphism argument are in the companion Markdown
proofs. This verifier checks their finite fusion-rule inputs independently.
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
    return tuple(x for matrix in ring for row in matrix for x in row)


def product(ring, left, right):
    return tuple(sum(left[i] * right[j] * ring[i][j][k]
                     for i in range(8) for j in range(8)) for k in range(8))


def model():
    # Basis a^i, a^i r (i=0,1,2,3); ra=a^-1 r,
    # r^2=1+2r+2a^2r.
    ring = [[[0 for _ in range(8)] for _ in range(8)] for _ in range(8)]
    for i in range(8):
        for j in range(8):
            a, b = i % 4, j % 4
            if i < 4 and j < 4:
                ring[i][j][(a + b) % 4] = 1
            elif i < 4:
                ring[i][j][4 + (a + b) % 4] = 1
            elif j < 4:
                ring[i][j][4 + (a - b) % 4] = 1
            else:
                ring[i][j][(a - b) % 4] = 1
                ring[i][j][4 + (a - b) % 4] = 2
                ring[i][j][4 + (a - b + 2) % 4] = 2
    return ring


def check_associativity(ring):
    count = 0
    for i in range(8):
        for j in range(8):
            for k in range(8):
                for target in range(8):
                    require(sum(ring[i][j][a] * ring[a][k][target] for a in range(8))
                            == sum(ring[j][k][a] * ring[i][a][target] for a in range(8)),
                            'associativity failure')
                    count += 1
    return count


def source(rows, ledger, index):
    name = f'R8_2_{index}'
    ring = rows[index - 1]
    digest = hashlib.sha256(json.dumps(ring, separators=(',', ':')).encode()).hexdigest()
    require(ledger[name]['tensor_sha256'] == digest, f'{name}: source tensor hash')
    return ring, digest


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', type=Path, required=True)
    args = parser.parse_args()
    root = args.repo.resolve()
    with gzip.open(root / 'supplements/rank8/data/rank8_tables.txt.gz', 'rt') as stream:
        rows = [json.loads(line.replace('{', '[').replace('}', ']')) for line in stream]
    rows = sorted((r for r in rows if max(flat(r)) == 2), key=flat)
    ledger = {row['id']: row for row in json.loads(
        (root / 'supplements/rank8/data/decisions.json').read_text())}
    ring, digest = source(rows, ledger, 37)
    built = model()
    mapping = [0, 1, 7, 2, 5, 3, 6, 4]
    comparisons = 0
    for i in range(8):
        for j in range(8):
            for k in range(8):
                require(built[i][j][k] == ring[mapping[i]][mapping[j]][mapping[k]],
                        'R37 tensor identification')
                comparisons += 1
    dual = [next(j for j in range(8) if built[i][j][0]) for i in range(8)]
    require(dual == [0, 3, 2, 1, 4, 5, 6, 7], 'model duals')
    degrees = [i % 2 for i in range(4)] * 2
    require(set(degrees) == {0, 1}, 'grading not faithful')
    require(all(degrees[k] == (degrees[i] + degrees[j]) % 2
                for i in range(8) for j in range(8) for k in range(8) if built[i][j][k]),
            'C2 grading')
    assoc = check_associativity(built)
    other, other_digest = source(rows, ledger, 170)
    neutral = [0, 5, 6, 7]
    q = [[[built[i][j][k] for k in [0, 2, 4, 6]]
          for j in [0, 2, 4, 6]] for i in [0, 2, 4, 6]]
    require(all(q[i][j][k] == other[neutral[i]][neutral[j]][neutral[k]]
                for i in range(4) for j in range(4) for k in range(4)),
            'R170 neutral 2D2 tensor')
    require(all(other[i][j][k] == 0 for i in neutral for j in neutral
                for k in range(8) if k not in neutral), 'neutral closure')
    unit = tuple(int(k == 0) for k in range(8))
    e = [tuple(int(k == i) for k in range(8)) for i in range(8)]
    require(tuple(other[3][3]) == unit, 'R170 odd invertible is involutive')
    require(product(other, product(other, e[3], e[6]), e[3]) == e[7],
            'R170 odd conjugation must swap neutral noninvertibles')
    print(json.dumps({
        'status': 'PASS',
        'general_decisions': [{
            'id': 'R8_2_37',
            'verdict': 'unitary_categorification_exists',
            'tensor_sha256': digest,
            'model_basis_to_census_zero_based': mapping,
            'structure_constants_compared': comparisons,
            'associativity_coefficients_checked': assoc,
            'model_duals': dual,
            'model_C2_degrees': degrees,
            'construction': 'nonsplit C2 extension of the unitary 2D2 category',
        }],
        'scoped_results': [{
            'id': 'R8_2_170',
            'verdict': 'unitary_categorification_excluded; general case unresolved',
            'tensor_sha256': other_digest,
            'neutral_basis_to_census_zero_based': neutral,
            'odd_invertible_census_zero_based': 3,
            'condition': 'the neutral category is equivalent or Galois conjugate to known 2D2',
        }],
        'categorical_proof_checked_by_this_program': False,
    }, indent=2))


if __name__ == '__main__':
    main()
