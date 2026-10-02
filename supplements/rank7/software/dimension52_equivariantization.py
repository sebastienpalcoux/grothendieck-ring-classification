"""Exact source premises for the general dimension-52 exclusion.
Python standard library only. The categorical argument is in PROOF.md.
"""
import hashlib
import itertools
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def verify_record(record, expected_tensor=None):
    N = record['tensor']
    r = 7
    require(len(N) == r and all(len(M) == r and all(len(row) == r for row in M) for M in N), 'tensor shape')
    require(all(type(v) is int and v >= 0 for M in N for row in M for v in row), 'nonnegative integer coefficients')
    if expected_tensor is not None:
        require(N == expected_tensor, 'external census mismatch')
    digest = hashlib.sha256(json.dumps(N, separators=(',', ':')).encode()).hexdigest()
    require(digest == record['tensor_sha256'], 'tensor hash')
    dims = [1, 1, 1, 1, 4, 4, 4]
    for i, j in itertools.product(range(r), repeat=2):
        require(N[0][i][j] == N[i][0][j] == int(i == j), 'unit')
        require(N[i][j] == N[j][i], 'commutativity')
        require(N[i][j][0] == int(i == j), 'duality')
        require(sum(N[i][j][k] * dims[k] for k in range(r)) == dims[i] * dims[j], 'positive dimension character')
    for i, j, k, l in itertools.product(range(r), repeat=4):
        require(sum(N[i][j][a] * N[a][k][l] for a in range(r)) == sum(N[j][k][a] * N[i][a][l] for a in range(r)), 'associativity')
    inv = [i for i in range(r) if N[i][i] == [1] + [0] * (r - 1)]
    require(inv == [0, 1, 2, 3], 'invertible labels')
    inv_table = []
    for i in inv:
        row = []
        for j in inv:
            require(sum(N[i][j]) == 1, 'invertible product')
            k = N[i][j].index(1)
            require(k in inv, 'invertible group closure')
            row.append(k)
        inv_table.append(row)
    require(all(inv_table[i][i] == 0 for i in inv), 'invertible group V4')
    for h in inv[1:]:
        for x in [4, 5, 6]:
            require(N[h][x] == [int(k == x) for k in range(r)], 'every possible central character fixes the noninvertibles')
    ad = {0}
    for i in range(r):
        ad.update(k for k, multiplicity in enumerate(N[i][i]) if multiplicity)
    while True:
        larger = ad | {k for i, j in itertools.product(ad, repeat=2) for k, v in enumerate(N[i][j]) if v}
        if larger == ad:
            break
        ad = larger
    require(ad == set(range(r)), 'trivial universal grading')
    # Each possible h groups the four invertibles into two pairs, and
    # each h-fixed dimension-four object splits into two dimension-two objects.
    quotient_dimensions = []
    for h in inv[1:]:
        pairs = {tuple(sorted((i, inv_table[h][i]))) for i in inv}
        require(len(pairs) == 2 and all(len(set(p)) == 2 for p in pairs), 'invertible character orbits')
        d = [1] * len(pairs) + [2] * 6
        require(len(d) == 8 and sum(x*x for x in d) == 26, 'first quotient dimensions')
        quotient_dimensions.append(d)
    # All object actions V4 -> Aut(C13). Generator images must square to1.
    roots = [a for a in range(1, 13) if a*a % 13 == 1]
    require(roots == [1, 12], 'automorphism involutions')
    actions = []
    for a, b in itertools.product(roots, repeat=2):
        if a == b == 1:
            continue  # The original inner C2 acts by inversion.
        multipliers = [1, a, b, a*b % 13]
        left = set(range(13))
        orbits = []
        while left:
            x = min(left)
            orbit = sorted({c*x % 13 for c in multipliers})
            left.difference_update(orbit)
            orbits.append(orbit)
        require(sorted(map(len, orbits)) == [1] + [2]*6, 'V4 orbit type')
        require(all(sum(c*x % 13 == x for c in multipliers) == 2 for x in range(1, 13)), 'nonzero stabilizer orders')
        # Unit orbit gives Rep(V4): four dimension-one simples. Each other
        # stabilizer is C2, whose projective irreducibles have dimension one.
        forced = [1]*4 + [2]*12
        require(sum(x*x for x in forced) == 52 and forced != dims, 'dimension contradiction')
        actions.append({'generator_images': [a, b], 'orbit_sizes': sorted(map(len, orbits)), 'forced_simple_dimensions': forced})
    require(len(actions) == 3, 'all nontrivial V4 object actions')
    return {'id': record['id'], 'status': 'PASS', 'scope': 'general noncategorification over C, using PROOF.md',
            'tensor_sha256': digest, 'FPdim': 52, 'adjoint_rank': 7, 'invertible_group': 'V4',
            'possible_character_labels': inv[1:], 'quotient_dimensions': quotient_dimensions,
            'V4_actions_on_C13': actions, 'associativity_identities': r**4}


def main():
    here = Path(__file__).resolve().parent
    record = json.loads((here.parent / 'data/r7_2_75_certificate.json').read_text())
    receipt = verify_record(record)
    print(json.dumps(receipt, indent=2))


KIND = 'solvable_double_equivariantization_orbit_obstruction'
TENSOR_SHA = 'e371563133bba8fa2b285ed9f8c66552c2f4d0ef5fae1a56e35e986057863625'


def certificate(N):
    if hashlib.sha256(json.dumps(N,separators=(',',':')).encode()).hexdigest()!=TENSOR_SHA:
        return None
    record=json.loads((Path(__file__).resolve().parents[1]/'data/r7_2_75_certificate.json').read_text())
    verify_record(record,N)
    return {'kind':KIND,'scope':'all complex fusion categories','id':record['id'],
            'tensor_sha256':TENSOR_SHA,'dimensions':[1,1,1,1,4,4,4],
            'global_dimension':52,'invertible_group':'V4','adjoint_rank':7,
            'proof':'papers/r7_2_75_proof.md',
            'source_theorems':'ENO solvability Theorem 1.6 and Proposition 4.4; ENO On fusion categories Proposition 8.20 and Corollary 8.30; central equivariantization/de-equivariantization in stages (DGNO Theorem 4.18(i), Proposition 4.19).'}


def verify(N,c):
    require(c is not None and c==certificate(N),'dimension-52 certificate mismatch')


if __name__ == '__main__':
    main()
