"""Diagonal-fermion products with a resolved fixed point.

The local categorical data are published inputs (Aasen--Lake--Walker).
This module checks the scalar calculation, derives the complete fusion tensor
from the general theorem, and identifies it only afterwards in the census.
"""
import itertools
import json
from pathlib import Path
from exact import require
from oriented_signed import validate_general

ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ('Aasen--Lake--Walker, arXiv:1709.01941v2, Sections 2.1 and 7.1--7.2, '
             'equations (9)--(13), (235), (240), (467); '
             'diagonal-fermion fixed-point theorem in this manuscript')


def gaussian_mul(a, b):
    return (a[0]*b[0]-a[1]*b[1], a[0]*b[1]+a[1]*b[0])


def local_data(m):
    require(m in (0, 2), 'no categorical input supplied for this near-group parameter')
    return {'parameter': m, 'model': 'Ising' if m == 0 else 'half-E6',
            'unitary_published_input': True, 'fermion_order': 2,
            'fermion_self_braiding': [-1, 0], 'fixed_action_square': [1, 0],
            'fixed_object_second_indicator': 1, 'trivalent_rotation_scalar': [1, 0],
            'rotated_half_braiding_scalar': [0, -1]}


def local_certificate(m, n):
    a, b = local_data(m), local_data(n)
    braid = gaussian_mul(a['fermion_self_braiding'], b['fermion_self_braiding'])
    rotation = gaussian_mul(a['rotated_half_braiding_scalar'], b['rotated_half_braiding_scalar'])
    require(braid == (1, 0), 'diagonal object is not a boson')
    require(rotation == (-1, 0), 'same-rotation fixed-point theorem does not apply')
    # On the ordinary vacuum channel of V tensor V, the relative tensor-product
    # projector is (1 + epsilon*eta*rotation)/2. Thus opposite signs pair.
    vacuum = [[(1 - epsilon*eta)//2 for eta in (1, -1)] for epsilon in (1, -1)]
    require(vacuum == [[0, 1], [1, 0]], 'fixed-point duality calculation')
    return {'inputs': [a, b], 'diagonal_self_braiding': list(braid),
            'dual_action_scalar': list(rotation), 'vacuum_projector_ranks': vacuum,
            'fixed_point_duality': [1, 0], 'residual_invertible_action': [1, 0],
            'published_input_scope': 'Existence, unitarity and local coherence data are cited, not re-solved.'}


def fusion_tensor(m, n):
    """Tensor forced by the theorem; this function makes no existence claim."""
    require(type(m) is int and type(n) is int and m >= 0 and n >= 0
            and m % 2 == n % 2 == 0, 'even nonnegative parameters required')
    R = [[[0]*6 for _ in range(6)] for _ in range(6)]

    def put(i, j, terms):
        R[i][j] = [terms.get(k, 0) for k in range(6)]
        R[j][i] = R[i][j][:]

    # Basis (1,g,a,b,u,v), with a*=a, b*=b, and u*=v.
    for i in range(6):
        put(0, i, {i: 1})
    put(1, 1, {0: 1}); put(1, 2, {2: 1}); put(1, 3, {3: 1})
    put(1, 4, {5: 1}); put(1, 5, {4: 1})
    put(2, 2, {0: 1, 1: 1, 2: m}); put(3, 3, {0: 1, 1: 1, 3: n})
    put(2, 3, {4: 1, 5: 1})
    for k in (4, 5):
        put(2, k, {3: 1, 4: m//2, 5: m//2})
        put(3, k, {2: 1, 4: n//2, 5: n//2})
    square = {1: 1, 2: m//2, 3: n//2, 4: m*n//4, 5: m*n//4}
    put(4, 4, square); put(5, 5, square)
    product = dict(square); del product[1]; product[0] = 1
    put(4, 5, product)
    validate_general(R)
    return R


def examples():
    for m, n in ((0, 0), (0, 2), (2, 2)):
        local_certificate(m, n)
        names = {0: 'Ising', 2: 'half-E6'}
        name = f'Diagonal fermion: {names[m]} x {names[n]} (equal rotation phases)'
        yield name, fusion_tensor(m, n), REFERENCE, {'general': 'yes', 'pivotal': 'yes',
                'spherical': 'yes', 'pseudo_unitary': 'yes', 'unitary': 'yes'}


def verify_local_certificate(m, n, cert):
    require(cert == local_certificate(m, n), 'local fixed-point certificate mismatch')
    return True


if __name__ == '__main__':
    from prepare import key
    rows = json.loads((ROOT/'data/census.json').read_text())
    index = {key(r['N']): r['id'] for r in rows}
    records = []
    for (m, n), (name, N, ref, existence) in zip(((0, 0), (0, 2), (2, 2)), examples()):
        require(key(N) in index, 'constructed tensor is absent from the census')
        record = {'name': name, 'id': index[key(N)], 'N': N, 'parameters': [m, n],
                  'reference': ref, 'existence': existence, 'local_certificate': local_certificate(m, n)}
        records.append(record)
        print(record['id'], name)
    (ROOT/'data/fermionic_product_models.json').write_text(json.dumps(records, indent=2)+'\n')
