#!/usr/bin/env python3
"""Verify the finite odd cyclic Clifford constraints for R6_4_155.

AI-generated research; independent verification pending. This checks necessary
character constraints on a pinned modular candidate, not categorification.
"""
from pathlib import Path
from collections import Counter
import argparse
import ast
import hashlib
import json
import sympy as s

CERTIFICATE = 'supplements/rank6/research/frontier/new_research/r155_generalized/certificate.json'
CERTIFICATE_SHA256 = 'b76cdb3fbc8c4cc6c23d3e177be26d0a74d1adab114069b9e40b04b62678fca7'
TENSOR_SHA256 = '012ef716d19b96a2a800d7bcbb33f3ae5e99e3c6a223f6e14bcd20144d4072a3'
PROOF_SOURCE = 'manuscripts/rank6/papers/chapters/frontier_155_odd_clifford.tex'
PROOF_SHA256 = 'a035b0c137a83e511ccd6a4c3e7c64f120eb25f288d773fff644a54522cafdf4'
ORDERS = tuple(range(3, 24, 2))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def spin_spectrum(n):
    require(type(n) is int and n >= 3 and n % 2 == 1, 'odd order at least three required')
    c = Counter({0: 1})
    inv2 = pow(2, -1, n)
    for j in range(1, (n + 1) // 2):
        nxt = Counter()
        for a, multiplicity in c.items():
            nxt[(a + j * inv2) % n] += multiplicity
            nxt[(a - j * inv2) % n] += multiplicity
        c = nxt
    result = [c[j] for j in range(n)]
    require(sum(result) == 2 ** ((n - 1) // 2), 'incorrect spin dimension')
    return result


def check_block(multiplicities, dimension, spin, matrix, inverse):
    n = len(spin)
    require(len(multiplicities) == n, 'rotation spectrum length')
    require(all(type(x) is int and x >= 0 for x in multiplicities), 'nonnegative integral rotation spectrum')
    require(type(dimension) is int and dimension >= 0, 'nonnegative integral dimension')
    require(sum(multiplicities) == dimension, 'rotation dimension mismatch')
    values = s.Matrix(multiplicities)
    quotient = inverse * values
    require(matrix * quotient == values, 'convolution identity')
    require(sum(quotient) * sum(spin) == dimension, 'quotient dimension mismatch')
    require(all(x.is_Integer is True and x >= 0 for x in quotient), 'quotient must be nonnegative integral')
    return [int(x) for x in quotient]


def source_rows(data):
    require(isinstance(data, dict) and isinstance(data.get('rows'), list), 'certificate schema')
    rows = data['rows']
    require(len(rows) == 7176, 'complete inherited rotation domain')
    expected = {(n, x, z) for n in range(2, 25) for x in range(6) for z in range(52)}
    keys = [(r['n'], r['base_simple'], r['central_simple']) for r in rows]
    require(len(set(keys)) == len(keys) and set(keys) == expected, 'rotation domain missing or duplicated')
    return [r for r in rows if r['n'] in ORDERS and r['base_simple'] in (1, 2)]


def pinned_input(path):
    raw = path.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == CERTIFICATE_SHA256, 'generalized-rotation source hash mismatch')
    return source_rows(json.loads(raw))


def source_tensor(repo):
    path = repo / 'data/remaining_cases.py'
    tree = ast.parse(path.read_text())
    rows = [node for node in tree.body if isinstance(node, ast.Assign)
            and any(isinstance(t, ast.Name) and t.id == 'R6_4_155' for t in node.targets)]
    require(len(rows) == 1, 'unique named source tensor')
    tensor = ast.literal_eval(rows[0].value)
    raw = json.dumps(tensor, separators=(',', ':')).encode()
    require(hashlib.sha256(raw).hexdigest() == TENSOR_SHA256, 'source tensor hash mismatch')
    require(tensor[1][1] == [0, 4, 4, 0, 1, 1] and tensor[1][2] == [1, 4, 4, 1, 0, 0], 'noninvertible basis binding')
    require(tensor[3][1][1] == tensor[3][2][2] == tensor[3][3][0] == 1, 'stabilizer basis binding')
    return {'path': str(path.relative_to(repo)), 'tensor_sha256': TENSOR_SHA256,
            'noninvertible_indices': [1, 2], 'stabilizer_index': 3}


def path_recurrence():
    """Check the universal polynomial identities, with m a formal parameter."""
    m = s.Symbol('m', integer=True)
    # Basis: 1, h, g, hg, x, y. The pointed indices use binary addition.
    unit = s.Matrix([1, 0, 0, 0, 0, 0])
    basis = [s.eye(6)[:, i] for i in range(6)]
    tensor = [[[s.Integer(0) for k in range(6)] for j in range(6)] for i in range(6)]
    for i in range(4):
        for j in range(4):
            tensor[i][j][i ^ j] = 1
        for j in (4, 5):
            k = j ^ (1 if i & 2 else 0)
            tensor[i][j][k] = tensor[j][i][k] = 1
    for i in (4, 5):
        for j in (4, 5):
            for k in ((2, 3) if i == j else (0, 1)):
                tensor[i][j][k] = 1
            tensor[i][j][4] = tensor[i][j][5] = m
    def multiply(a, b):
        return s.Matrix([s.expand(sum(a[i] * b[j] * tensor[i][j][k]
                                      for i in range(6) for j in range(6))) for k in range(6)])
    powers = [unit]
    for n in range(1, 6):
        powers.append(multiply(powers[-1], basis[4]))
    require(powers[3] == m * sum(basis[:4], s.zeros(6, 1)) + 2*m*m*basis[4] + (2+2*m*m)*basis[5], 'formal cubic identity')
    require(powers[4] == (2*m*powers[3] + 4*m*basis[4] + 2*(basis[0]+basis[1])).applyfunc(s.expand), 'formal quartic identity')
    require(powers[5] == (2*m*powers[4] + 4*m*powers[2] + 4*basis[4]).applyfunc(s.expand), 'formal recurrence seed')
    # Multiplication by x^(n-5) gives the displayed recurrence at every n>=5.
    return {'formal_parameter': 'm', 'identities_verified': ['x^3', 'x^4', 'x^5'],
            'all_orders_by_ring_multiplication': True,
            'divisibility_conclusion': 'The path-Clifford coefficient divisibilities at every positive order hold exactly when m is even.'}


def negative_controls():
    spin = spin_spectrum(3)
    matrix = s.Matrix(3, 3, lambda i, j: spin[(i - j) % 3])
    inverse = matrix.inv()
    rejected = []
    for label, values, dim in [('negative quotient', [2, 0, 0], 2),
                               ('nonintegral quotient', [1, 0, 0], 1),
                               ('wrong dimension', [0, 1, 1], 3)]:
        try:
            check_block(values, dim, spin, matrix, inverse)
        except ValueError:
            rejected.append(label)
        else:
            raise ValueError('negative control accepted: ' + label)
    try:
        spin_spectrum(4)
    except ValueError:
        rejected.append('even order')
    else:
        raise ValueError('even order accepted')
    return rejected


def run(repo, proof_source=None):
    proof_source = proof_source or repo / PROOF_SOURCE
    require(hashlib.sha256(proof_source.read_bytes()).hexdigest() == PROOF_SHA256, 'manuscript theorem source hash mismatch')
    binding = source_tensor(repo)
    rows = pinned_input(repo / CERTIFICATE)
    require(len(rows) == 1144, 'odd block count')
    by_order = []
    total = 0
    for n in ORDERS:
        spin = spin_spectrum(n)
        matrix = s.Matrix(n, n, lambda i, j: spin[(i - j) % n])
        inverse = matrix.inv()
        checked = []
        for row in rows:
            if row['n'] != n:
                continue
            require(all(isinstance(x, str) and str(int(x)) == x for x in row['multiplicities']), 'canonical integer strings')
            quotient = check_block([int(x) for x in row['multiplicities']], row['dimension'], spin, matrix, inverse)
            checked.append({'base_simple': row['base_simple'], 'central_simple': row['central_simple'],
                            'quotient_multiplicities': quotient})
        require(len(checked) == 104, 'two noninvertibles and all central targets')
        total += len(checked)
        by_order.append({'n': n, 'spin_multiplicities': spin, 'spin_dimension': sum(spin),
                         'checked_blocks': len(checked),
                         'minimum_quotient': min(min(r['quotient_multiplicities']) for r in checked),
                         'blocks': checked})
    return {'schema': 1, 'ring': 'R6_4_155', 'all_passed': True,
            'scope': 'Necessary odd cyclic Clifford character-extension constraints only; no categorical existence or exclusion conclusion.',
            'input_path': CERTIFICATE, 'input_sha256': CERTIFICATE_SHA256,
            'source_tensor': binding, 'proof_source': {'path': PROOF_SOURCE, 'sha256': PROOF_SHA256},
            'orders': list(ORDERS), 'checked_blocks': total,
            'negative_controls_rejected': negative_controls(), 'path_recurrence': path_recurrence(), 'rows': by_order}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=Path('.'))
    parser.add_argument('--output', type=Path)
    parser.add_argument('--proof-source', type=Path, help='Explicit manuscript source for a work-copy audit; default is the canonical repository chapter.')
    args = parser.parse_args()
    result = run(args.repo.resolve(), args.proof_source)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2) + '\n')
    print('PASS: 1144 odd cyclic Clifford blocks; four negative controls rejected; categorification remains unresolved.')


if __name__ == '__main__':
    main()
