#!/usr/bin/env python3
"""Independent SymPy audit: no imported candidate arithmetic."""
from pathlib import Path
import json, hashlib
import sympy as s
import argparse
ap = argparse.ArgumentParser()
ap.add_argument('--input-dir', type=Path, default=Path(__file__).parent)
ap.add_argument('--output', type=Path)
args = ap.parse_args()
p = args.input_dir
z = s.Symbol('z')
mod = s.Poly(s.cyclotomic_poly(48, z), z, domain=s.QQ)

def poly(v):
    return s.Poly(sum((s.Rational(a) * z ** i for i, a in enumerate(v))), z, domain=s.QQ)

def reduce(v):
    return s.Poly(v, z, domain=s.QQ).rem(mod)

def vector(v):
    v = s.Poly(v, z, domain=s.QQ)
    return s.Matrix([v.nth(i) for i in range(16)])
powers = [reduce(s.Poly(z ** i, z, domain=s.QQ)) for i in range(48)]
one = powers[0]
q2 = powers[6] + powers[42]
q3 = powers[4] + powers[44]
q6 = reduce(q2 * q3)
d = 3 * one + 2 * q2 + 2 * q3 + q6
D = 4 * reduce(one + d * d)
basis = s.Matrix.hstack(*(vector(x) for x in [one, q2, q3, q6]))
dimfield = s.Matrix.hstack(*(vector(x) for x in [one, q2, d, reduce(q2 * d)]))
if not basis.rank() == dimfield.rank() == 4:
    raise ValueError('Independent exact audit: basis.rank() == dimfield.rank() == 4')
input_data = json.loads((p / 'all_indicators.json').read_text())
expected = json.loads((p / 'phase_masses.json').read_text())
receipts = []
for case in input_data['cases']:
    if not case['cyclic_dimension_three_compatible']:
        continue
    target = next((c for c in expected['cases'] if c['chi3_pair'] == case['chi3_pair']))
    target = {m['phase']: m for m in target['masses']}
    seq = []
    for n in range(1, 49):
        vals = case['moments_ascending_zeta48_coefficients'][str(n)]
        twist = [one, -one, powers[9]]
        dims = [one, one, q2]
        sigma = s.Poly(0, z, domain=s.QQ)
        for i, j in [(0, 2), (2, 0), (1, 2), (2, 1)]:
            exponents = [0, 24, 9]
            sigma += reduce(dims[i] * dims[j] * powers[(exponents[i] - exponents[j]) * n % 48]) / 4
        asserted = s.Poly(0, z, domain=s.QQ) if n % 2 else reduce(q2 * (powers[9 * n % 48] + powers[-9 * n % 48])) / 2
        if not sigma == asserted:
            raise ValueError('Independent exact audit: sigma == asserted')
        seq.append([one, one if n % 2 == 0 else s.Poly(0, z, domain=s.QQ), poly(vals['X']), poly(vals['X']), sigma, poly(vals['T'])])
    observed = {}
    weighted_checks = 0
    for k in range(48):
        row = []
        for i in range(6):
            value = reduce(D * sum((reduce(seq[n - 1][i] * powers[-k * n % 48]) for n in range(1, 49)), s.Poly(0, z, domain=s.QQ))) / 48
            coords = list(basis.gauss_jordan_solve(vector(value))[0])
            row.append([str(x) for x in coords])
            exp = target.get(k, {}).get('masses_K', [['0'] * 4] * 6)[i]
            if not row[-1] == exp:
                raise ValueError((k, i, row[-1], exp))
            weighted_checks += 1
        if any((s.Rational(x) for r in row for x in r)):
            observed[k] = row
    if not set(observed) == set(target):
        raise ValueError('Independent exact audit: set(observed) == set(target)')
    if not seq[-1] == [one, one, d, d, q2, reduce(q2 * d)]:
        raise ValueError('Independent exact audit: seq[-1] == [one, one, d, d, q2, reduce(q2 * d)]')
    for n in range(1, 49):
        for i in range(6):
            recon = s.Poly(0, z, domain=s.QQ)
            for k, row in observed.items():
                mass = sum((s.Rational(c) * v for c, v in zip(row[i], [one, q2, q3, q6])), s.Poly(0, z, domain=s.QQ))
                recon += reduce(mass * powers[k * n % 48])
            if not reduce(recon) == reduce(D * seq[n - 1][i]):
                raise ValueError('Independent exact audit: reduce(recon) == reduce(D * seq[n - 1][i])')
    receipts.append({'chi3_pair': case['chi3_pair'], 'chi6_pair': case['chi6_pair'], 'phase_masses_checked': weighted_checks, 'twist_support': list(observed), 'fourier_roundtrip': True, 'Ising_modular_formula_all_48': True})
result = {'status': 'PASS', 'independent_backend': 'SymPy polynomial remainder and rational linear solve; no imported candidate arithmetic', 'cases': receipts, 'field_basis_independence': True, 'scope': 'Arithmetic Fourier, full Ising sequence, inverse transform and dimension-field identities; categorical justification audited separately', 'inputs_sha256': {f: hashlib.sha256((p / f).read_bytes()).hexdigest() for f in ['all_indicators.json', 'phase_masses.json']}}
if args.output:
    args.output.write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result))
