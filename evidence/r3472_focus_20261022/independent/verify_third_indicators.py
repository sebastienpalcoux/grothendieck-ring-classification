#!/usr/bin/env python3
"""Exact source-bound arithmetic for the maximal third-indicator proposition.

The categorical inputs are stated, with primary-source theorem numbers, in
THIRD_INDICATORS.md. This script does not claim to prove those theorems or to
construct a fusion category. It also audits the third-rotation coordinates of
the previously certified height-four feasible point, without claiming to
replay its entire expensive cone construction.
"""
from fractions import Fraction as Q
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
TENSOR = ROOT / 'site/dist/downloads/fusion-tensors/R8_3_3472.txt'
WITNESS = ROOT / 'evidence/rank8_frontier_20261021/global_induction/atomic_spectrum_results/R8_3_3472_h4.json'


def need(ok, message):
    if not ok:
        raise ValueError(message)


def add(x, y):
    return x[0] + y[0], x[1] + y[1]


def mul(x, y):
    return x[0] * y[0] + 2 * x[1] * y[1], x[0] * y[1] + x[1] * y[0]


def scale(n, x):
    return n * x[0], n * x[1]


def total(xs):
    value = (0, 0)
    for x in xs:
        value = add(value, x)
    return value


def main():
    R = json.loads(TENSOR.read_text())
    need(len(R) == 8 and all(len(m) == 8 and all(len(v) == 8 for v in m) for m in R), 'tensor shape')
    need(all(type(n) is int and n >= 0 for m in R for v in m for n in v), 'nonnegative integral tensor')
    need(all(R[0][i][j] == int(i == j) for i in range(8) for j in range(8)), 'unit')
    need(all(R[i][j][0] == int(i == j) for i in range(8) for j in range(8)), 'self duality')
    delta = (7, 5)
    dims = [(1, 0), (6, 5), (6, 5), delta, (6, 5), (8, 5), (8, 5), (8, 5)]
    need(all(a > 0 and b >= 0 for a, b in dims), 'strictly positive dimension embedding')
    for i in range(8):
        for j in range(8):
            need(mul(dims[i], dims[j]) == total(scale(R[i][j][k], dims[k]) for k in range(8)), 'dimension character')
    D = total(mul(d, d) for d in dims)
    need(D == (700, 490), 'global dimension')
    Dbar = (D[0], -D[1])
    norm = mul(D, Dbar)
    need(norm == (9800, 0) and 9800 == 2**3 * 5**2 * 7**2, 'global dimension norm and prime support')
    delta2 = mul(delta, delta)
    need(delta2 == (99, 70) and mul(delta2, Dbar) == D, 'D/conjugate(D)')
    cubic = [sum(R[i][i][k] * R[k][i][0] for k in range(8)) for i in range(8)]
    need(cubic == [1, 2, 2, 2, 2, 2, 2, 2], 'cubic invariant dimensions')
    maximum = total(scale(n, d) for n, d in zip(cubic, dims))
    need(maximum == delta2, 'third-indicator maximum saturation')
    odd_square_witnesses = []
    for i in range(8):
        j = next((j for j in range(8) if R[j][j][i] % 2), None)
        need(j is not None, 'odd adjoint multiplicity for every simple')
        odd_square_witnesses.append({'simple': i, 'square_of': j, 'multiplicity': R[j][j][i]})
    # An order-three operator on a two-dimensional complex space is diagonalizable.
    # In Q(omega), omega^2=-1-omega, so its trace has coordinates (a-c,b-c).
    traces = []
    for a in range(3):
        for b in range(3-a):
            c = 2-a-b
            traces.append({'multiplicities': [a, b, c], 'trace_in_basis_1_omega': [a-c, b-c], 'real_part': str(Q(2*a-b-c, 2))})
    saturating = [x['multiplicities'] for x in traces if Q(x['real_part']) == 2]
    need(saturating == [[2, 0, 0]], 'unique maximal third-rotation spectrum')
    old = json.loads(WITNESS.read_text())
    cert = old['certificate']
    meta = cert['metadata']
    source_sha = hashlib.sha256(json.dumps(R, separators=(',', ':')).encode()).hexdigest()
    need(source_sha == old['tensor_sha256'], 'old witness source tensor binding')
    need(meta['height'] == 4 and meta['field']['q'] == 2, 'expected witness height and field')
    need(cert['indicators'] == [1]*7, 'old second indicators')
    need(len(cert['indices']) == len(cert['weights']) and len(set(cert['indices'])) == len(cert['indices']), 'witness support')
    weights = {i: Q(v) for i, v in zip(cert['indices'], cert['weights'])}
    need(all(v >= 0 for v in weights.values()), 'nonnegative witness')
    high_end = sum(meta['low_column_counts']) + meta['high_duality_orbits'] * meta['trace_types']
    # tensor_rotation.rotation_types sorts the normalized rational traces.
    # Over Q(sqrt(2)), order3 has [-1/2,1] and order4 has three types.
    # streaming.Cone places these blocks consecutively, object by object.
    order3_types = [Q(-1, 2), Q(1)]
    order4_types = [(Q(-1), Q(1)), (Q(0), Q(-1)), (Q(1), Q(1))]
    need(high_end == 57406 and meta['variables'] == high_end + 7*(len(order3_types)+len(order4_types)), 'rotation indexing')
    rotation_audit = []
    for obj in range(1, 8):
        offset = high_end + 5*(obj-1)
        block = [weights.get(offset+j, Q(0)) for j in range(2)]
        need(block == [Q(0), Q(2)], 'cached third-rotation block already maximal')
        need(sum(v*t for v, t in zip(block, order3_types)) == 2, 'cached third indicator')
        rotation_audit.append({'simple': obj, 'nontrivial_type_weight': '0', 'identity_type_weight': '2', 'third_indicator': 2})
    return {
        'case_id': 'R8_3_3472', 'status': 'PASS', 'tensor_sha256': source_sha,
        'dimension_basis': ['1', 'sqrt(2)'], 'dimensions': dims, 'global_dimension': D,
        'global_dimension_norm': 9800, 'exponent_prime_support': [2, 5, 7],
        'regular_third_indicator': delta2, 'cubic_invariant_dimensions': cubic,
        'odd_square_witnesses': odd_square_witnesses,
        'forced_second_indicators': [1]*8, 'forced_third_indicators': cubic,
        'third_rotation_spectra': traces, 'maximal_spectrum': saturating[0],
        'cached_phase_witness': str(WITNESS.relative_to(ROOT)),
        'cached_phase_witness_sha256': hashlib.sha256(WITNESS.read_bytes()).hexdigest(),
        'cached_third_rotation_audit': rotation_audit,
        'scope': 'Necessary categorical restrictions, not a construction or exclusion. Cached audit checks third-rotation coordinates only; inherited full cone feasibility is a separately certified result.'
    }


if __name__ == '__main__':
    print(json.dumps(main(), indent=2))
