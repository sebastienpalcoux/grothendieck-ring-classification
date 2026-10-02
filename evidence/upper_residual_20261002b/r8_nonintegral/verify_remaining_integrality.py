#!/usr/bin/env python3
"""Replay all 55 exact nonintegral FP-dimension witnesses; no FP search."""
import argparse
import importlib.util
import json
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents
            if (p / 'supplements/rank8/data/rank8_tables.txt.gz').exists())
spec = importlib.util.spec_from_file_location(
    'integrality_recovery',
    ROOT / 'evidence/upper_residual_20261002b_recovery/verify_recovery.py')
rec = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rec)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def verify():
    audit = json.loads((HERE / 'remaining_integrality_audit.json').read_text())
    rings = rec.read_source(ROOT, 8)
    require(audit['status'] == 'PASS' and audit['remaining_cases'] == 55,
            'final frontier size')
    require(audit['integral_remaining'] == [], 'no integral remaining case')
    cases = audit['cases']
    require(len(cases) == 55 and len({c['id'] for c in cases}) == 55,
            '55 distinct witness cases')
    x = sp.Symbol('x')
    checked = []
    for case in cases:
        ring_id = case['id']
        N = rings[ring_id]
        require(rec.fingerprint(N) == case['source_sha256'],
                ring_id + ': source fingerprint')
        witness = case['nonintegral_fpdim_witness']
        i = witness['simple_index']
        matrix = sp.Matrix(N[i])
        coefficients = [int(c) for c in matrix.charpoly(x).all_coeffs()]
        require(coefficients == witness['polynomial'],
                ring_id + ': source characteristic polynomial')
        polynomial = sp.Poly.from_list(coefficients, x, domain=sp.QQ)
        lo, hi = map(sp.Rational, witness['largest_real_root_interval'])
        require(0 < lo < hi and polynomial.eval(lo) != 0
                and polynomial.eval(hi) != 0, ring_id + ': strict endpoints')
        require(polynomial.count_roots(lo, hi) == 1,
                ring_id + ': unique real root in witness interval')
        require(polynomial.count_roots(hi, sp.oo) == 0,
                ring_id + ': witness is largest real root')
        require(sp.ceiling(lo) > sp.floor(hi),
                ring_id + ': interval has no integer')
        # A nonnegative fusion matrix has its spectral radius as a real
        # eigenvalue. Therefore its largest real root is its FP eigenvalue.
        require(all(c >= 0 for c in matrix), ring_id + ': nonnegative matrix')
        checked.append(ring_id)
    excluded = audit['excluded_integral_case']
    require(excluded['id'] == 'R8_2_68' and excluded['scope'] == 'general_complex',
            'separate integral-case decision')
    N = rings['R8_2_68']
    require(rec.fingerprint(N) == excluded['source_sha256'],
            'R68 source fingerprint')
    dims = excluded['fp_dimensions']
    for i in range(8):
        for j in range(8):
            require(sum(N[i][j][k] * dims[k] for k in range(8)) == dims[i] * dims[j],
                    'R68 exact positive integral character')
    require((HERE / excluded['proof']).is_file()
            and (HERE / excluded['verifier']).is_file(), 'R68 proof dependencies')
    return {'status': 'PASS', 'remaining_cases': len(checked),
            'source_bound_nonintegral_fpdim_witnesses': len(checked),
            'exact_characteristic_polynomial_checks': len(checked),
            'exact_sturm_root_count_checks': 2 * len(checked),
            'integral_remaining': [], 'excluded_integral_case': 'R8_2_68',
            'r68_proof': excluded['proof'], 'optimization_safe': True}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = json.dumps(verify(), indent=2)
    if args.output:
        args.output.write_text(result + '\n')
    print(result)
