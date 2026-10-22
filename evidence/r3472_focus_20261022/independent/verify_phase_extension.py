#!/usr/bin/env python3
"""Exact, fast verification of the fixed integer center point's phase extension.

No optimizer or large center matrix is imported. The independently replayed
integer_witness.json binds the restriction labels to the full center system.
This verifier checks every additional indicator/rotation equation, with no
claim to impose a complete complex modular STS relation or actual twists.
"""
from fractions import Fraction as Q
from pathlib import Path
import hashlib
import json
import math
from verify_third_indicators import need, mul

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
TENSOR = ROOT / 'site/dist/downloads/fusion-tensors/R8_3_3472.txt'
BASE = HERE.parent / 'center/integer_witness.json'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def factors(n):
    out = {}
    p = 2
    while p*p <= n:
        while n % p == 0:
            out[p] = out.get(p, 0)+1
            n //= p
        p += 1
    if n > 1:
        out[n] = 1
    return out


def mobius(n):
    fs = factors(n)
    return 0 if any(v > 1 for v in fs.values()) else (-1)**len(fs)


def phi(n):
    out = n
    for p in factors(n):
        out = out//p*(p-1)
    return out


def chi8(n):
    return 0 if n % 2 == 0 else (1 if n % 8 in (1, 7) else -1)


def trace_types():
    # At height four the complete relative-trace box is 2^5*5*7.
    # Orders outside this divisor box have all four relative traces zero.
    bound = 1120
    out = {tuple((Q(0), Q(0)) for _ in range(4))}
    orders = sorted(2**a*5**b*7**c for a in range(6) for b in range(2) for c in range(2))
    for order in orders:
        for sign in (-1, 1):
            values = []
            for k in range(1, 5):
                g = math.gcd(order, k)
                n = order//g
                a, b = Q(mobius(n), phi(n)), Q(0)
                if n % 8 == 0:
                    z = n//8
                    if math.gcd(z, 8) == 1:
                        b = Q(sign*mobius(z)*chi8(z)*chi8(k//g)*2, phi(n))
                values.append((a, b))
            out.add(tuple(values))
    need(len(out) == 37, 'complete quadratic relative-trace domain')
    return sorted(out), bound


def build_system(R, lows, highs, types):
    ds = [(1, 0), (6, 5), (6, 5), (7, 5), (6, 5), (8, 5), (8, 5), (8, 5)]
    D = (700, 490)
    def dim(v):
        return tuple(sum(v[i]*ds[i][k] for i in range(8)) for k in range(2))
    rows, rhs, labels = [], [], []
    def row(label, coefficients, b):
        rows.append(coefficients)
        rhs.append(Q(b))
        labels.append(label)
    nt = len(types)
    for at, (index, v, weight) in enumerate(highs):
        row(('high_mass', index), {at*nt+j: Q(1) for j in range(nt)}, weight)
    for power in (1, 2, 3):
        for obj in range(1, 8):
            for k in range(2):
                values = {at*nt+j: Q(v[obj])*mul(dim(v), tt[power-1])[k]
                          for at, (_, v, _) in enumerate(highs) for j, tt in enumerate(types)}
                target = D[k]*[0, 0, 1, 2][power] - sum(weight*v[obj]*dim(v)[k] for _, v, weight in lows)
                row(('moment', power, obj, k), values, target)
    for obj in range(1, 8):
        offset = len(highs)*nt+3*(obj-1)
        h4 = sum(x*x for x in R[obj][obj])
        trace_square = sum(R[obj][obj])  # nu_2(X_i^2), because all simple nu_2=1.
        row(('rotation4_sum', obj), {offset: Q(1), offset+1: Q(1), offset+2: Q(1)}, h4)
        row(('rotation4_square', obj), {offset: Q(1), offset+1: Q(-1), offset+2: Q(1)}, trace_square)
        for k in range(2):
            values = {at*nt+j: Q(v[obj])*mul(dim(v), tt[3])[k]
                      for at, (_, v, _) in enumerate(highs) for j, tt in enumerate(types)}
            values[offset], values[offset+2] = Q(D[k]), Q(-D[k])
            target = -sum(weight*v[obj]*dim(v)[k] for _, v, weight in lows)
            row(('moment4', obj, k), values, target)
    return rows, rhs, labels, len(highs)*nt+21


def main():
    cert = json.loads((HERE/'phase_certificate.json').read_text())
    expected_dependencies = {
        str(p.relative_to(ROOT)): digest(p)
        for p in (Path(__file__).resolve(), HERE/'verify_third_indicators.py', TENSOR, BASE)
    }
    need(cert['dependency_sha256'] == expected_dependencies, 'complete phase-verifier file dependency closure')
    R = json.loads(TENSOR.read_text())
    tensor_sha = hashlib.sha256(json.dumps(R, separators=(',', ':')).encode()).hexdigest()
    base = json.loads(BASE.read_text())
    need(tensor_sha == cert['tensor_sha256'] == base['tensor_sha256'], 'canonical source binding')
    need(cert['base_system_metadata_sha256'] == base['system_metadata_sha256'], 'base matrix binding')
    bindings = dict(base['restriction_bindings'])
    weights = {j: Q(n, d) for j, n, d in base['entries']}
    lows = [(j, tuple(v), Q(w)) for j, v, w in cert['lows']]
    highs = [(j, tuple(v), Q(w)) for j, v, w in cert['highs']]
    need(len(lows) == 7 and len(highs) == 10, 'fixed point restriction counts')
    need(len(set(j for j, _, _ in lows+highs)) == 17, 'distinct source restriction variables')
    need(set(j for j, _, _ in lows+highs) == set(bindings), 'all positive restriction columns covered')
    for j, v, w in lows:
        need(bindings[j][0] == 'low' and tuple(bindings[j][2]) == v and weights[j] == w == 1, 'distinguished restriction binding')
    for j, v, w in highs:
        label = bindings[j]
        need(label[0] == 'high_orbit' and len(label[2]) == 1 and tuple(label[2][0]) == v, 'high restriction binding')
        need(weights[j] == w and w.denominator == 1 and w > 0, 'positive integral high multiplicity')
    types, bound = trace_types()
    encoded = [[[str(x) for x in pair] for pair in tt] for tt in types]
    need(cert['trace_types'] == encoded and cert['trace_compression_bound'] == bound, 'reconstructed complete relative-trace domain')
    rows, rhs, labels, nv = build_system(R, lows, highs, types)
    need(len(rows) == cert['rows'] == 80 and nv == cert['variables'] == 391, 'phase system dimensions')
    values = [Q(0)]*nv
    need(len({j for j, _ in cert['phase_entries']}) == len(cert['phase_entries']), 'distinct phase support')
    for j, value in cert['phase_entries']:
        need(0 <= j < nv and Q(value) > 0, 'positive phase support')
        values[j] = Q(value)
    for label, row, b in zip(labels, rows, rhs):
        need(sum(values[j]*a for j, a in row.items()) == b, 'exact phase equation '+repr(label))
    return {
        'case_id': 'R8_3_3472', 'status': 'PASS', 'tensor_sha256': tensor_sha,
        'base_integer_witness_sha256': digest(BASE), 'additional_rows': 80,
        'variables': nv, 'positive_support': sum(x > 0 for x in values),
        'complete_trace_types': 37, 'trace_compression_bound': bound,
        'integral_high_multiplicities': [int(w) for _, _, w in highs],
        'equation_counts': {'fixed_high_masses': 10, 'indicator_moments_degrees_1_2_3': 42,
                            'fourth_rotation_dimension_and_square_trace': 14, 'fourth_indicator_moments': 14},
        'dependencies': expected_dependencies,
        'scope': 'Exact nonnegative rational phase extension of the separately verified integral center relaxation. Indicator and rotation moments through degree4 only; no complete complex STS, actual twist assignment, or categorification.'
    }


if __name__ == '__main__':
    print(json.dumps(main(), indent=2))
