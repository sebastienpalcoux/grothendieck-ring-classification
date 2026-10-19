#!/usr/bin/env python3
"""Identify Rep(C7 semidirect C6) by 343 exact character products.

Standard library only. Supply the census .txt.gz path as the first argument.
The certificate records its input SHA256 and a full based-ring isomorphism.
"""
import collections
import gzip
import hashlib
import itertools
import json
from pathlib import Path
import sys


SOURCE_SHA256 = "9018f6f195339fb153ea326ec308c955bb1adf9afe1ffc9423be1bef6818e073"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def mul(u, v):
    # Z[zeta_6], zeta_6^2 = zeta_6 - 1.
    a, b = u
    c, d = v
    return (a*c-b*d, a*d+b*c+b*d)


def conj(u):
    a, b = u
    return (a+b, -b)


def total(xs):
    a = b = 0
    for c, d in xs:
        a += c
        b += d
    return a, b


def exact_character_tensor():
    roots = [(1, 0)]
    for _ in range(5):
        roots.append(mul(roots[-1], (0, 1)))
    require(mul(roots[-1], (0, 1)) == (1, 0), "sixth root relation")
    # Group elements a^x b^y, bab^-1=a^3. The order-six action is faithful.
    require(len({pow(3, i, 7) for i in range(6)}) == 6, "faithful action")
    elements = list(itertools.product(range(7), range(6)))
    chars = [[roots[(j*y) % 6] for x, y in elements] for j in range(6)]
    # Induced nontrivial C7 character, equivalently the permutation module
    # of the affine action on F7 with its invariant line removed.
    chars.append([((6 if x == 0 else -1), 0) if y == 0 else (0, 0)
                  for x, y in elements])
    for i, j in itertools.product(range(7), repeat=2):
        require(total(mul(u, conj(v)) for u, v in zip(chars[i], chars[j])) == (42*int(i == j), 0), "character orthogonality")
    require(sum(chars[i][0][0]**2 for i in range(7)) == 42, "complete character table")
    tensor = [[[0]*7 for _ in range(7)] for _ in range(7)]
    for i, j, k in itertools.product(range(7), repeat=3):
        a, b = total(mul(mul(u, v), conj(w))
                     for u, v, w in zip(chars[i], chars[j], chars[k]))
        require(b == 0 and a >= 0 and a % 42 == 0, "nonnegative integral coefficient")
        tensor[i][j][k] = a//42
    require(tensor[6][6] == [1]*6+[5], "noninvertible square")
    for i, j in itertools.product(range(6), repeat=2):
        require(tensor[i][j] == [int(k == (i+j) % 6) for k in range(7)], "cyclic invertible multiplication")
    return tensor


def signature(N):
    return sorted(sorted(sum(row) for row in mat) for mat in N)


def main():
    source = Path(sys.argv[1])
    require(hashlib.sha256(source.read_bytes()).hexdigest() == SOURCE_SHA256, "source checksum")
    N = exact_character_tensor()
    counts = collections.Counter()
    hits = []
    with gzip.open(source, 'rt') as handle:
        for line_number, line in enumerate(handle, 1):
            if not line.strip():
                continue
            T = json.loads(line.replace('{', '[').replace('}', ']'))
            m = max(x for mat in T for row in mat for x in row)
            counts[m] += 1
            if m != 5 or signature(T) != signature(N):
                continue
            for tail in itertools.permutations(range(1, 7)):
                p = (0,)+tail
                if all(N[i][j][k] == T[p[i]][p[j]][p[k]]
                       for i, j, k in itertools.product(range(7), repeat=3)):
                    hits.append({'id': f'R7_5_{counts[5]}', 'source_line': line_number,
                                 'basis_permutation_model_to_census': list(p),
                                 'census_tensor': T})
                    break
    require(counts == {1:43, 2:319, 3:1059, 4:2780, 5:5805}, 'source band counts')
    require(len(hits) == 1, f'Expected unique tensor identification, got {len(hits)}')
    require(hits[0]['id'] == 'R7_5_5678' and hits[0]['source_line'] == 9688, 'expected model census label')
    result = {'status': 'PASS', 'model': 'Rep(C7 semidirect C6) = Rep(AGL(1,7))',
              'presentation': 'a^7=b^6=1, b a b^-1=a^3',
              'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
              'character_field': 'Q(zeta_6), zeta_6^2-zeta_6+1=0',
              'checked_character_inner_products': 49,
              'checked_tensor_coefficients': 343,
              'fp_dimensions_model_basis': [1]*6+[6], 'global_dimension': 42,
              'existence': {k: 'yes' for k in ('general', 'pivotal', 'spherical', 'pseudo_unitary', 'unitary')},
              'primary_reference': 'Jacob Siehler, Near-group categories, Algebraic & Geometric Topology 3 (2003), Theorem 1.2 and Section 4.1',
              'primary_url': 'https://arxiv.org/abs/math/0209073',
              'tensor_model_basis': N, 'match': hits[0]}
    destination = Path(__file__).with_name('frobenius42_match.json')
    destination.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: v for k, v in result.items() if k not in ('tensor_model_basis', 'match')}))
    print(json.dumps({k: v for k, v in hits[0].items() if k != 'census_tensor'}))


if __name__ == '__main__':
    main()
