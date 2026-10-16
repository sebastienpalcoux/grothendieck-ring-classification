"""Exhaust the nonquadratic Casimir factors in the original 85 residuals.

Also verifies the mixed-quadratic-field general obstruction for four rings.
All arithmetic is exact; no categorical existence follows from a passing bound.
"""
import hashlib
import json
from pathlib import Path
import sympy as s

HERE = Path(__file__).resolve().parent
INPUTS = json.loads((HERE/'source_tensors.json').read_text())
x, z = s.symbols('x z')

def require(ok, message):
    if not ok:
        raise ValueError(message)

casimirs = {}
higher = []
for key, row in INPUTS.items():
    R = row['tensor']
    digest = hashlib.sha256(json.dumps(R, separators=(',', ':')).encode()).hexdigest()
    require(digest == row['tensor_sha256'], key+': source hash mismatch')
    N = [s.Matrix(M) for M in R]
    B = sum((M*M.T for M in N), s.zeros(len(N)))
    cp = B.charpoly(x).as_expr()
    casimirs[key] = cp
    if any(s.degree(f, x) > 2 for f, _ in s.factor_list(cp)[1]):
        higher.append(key)
require(set(higher) == {'R8_2_190', 'R8_2_489', 'R8_2_857', 'R6_8_1660'},
        'unexpected higher-degree source factor')

def cyclotomic_check(m, powers, character_indices, conductors, inv_factory, extras_factory,
                     source_polynomial, expected_ratios):
    P = s.cyclotomic_poly(m, z)
    red = lambda p: s.rem(s.expand(p), P, z)
    zp = lambda a: red(z**(a % m))
    gal = lambda p, a: red(p.subs(z, zp(a)))
    inv = inv_factory(red, zp)
    D = s.invert(inv, P, z)
    require(red(source_polynomial.subs(x, D)) == 0, 'wrong global codegree polynomial')
    require(len({str(gal(D, a)) for a in powers}) == len(powers), 'incorrect field degree')
    reciprocals = [gal(inv, a) for a in powers] + extras_factory(red, zp, P)
    rows = []
    for ki, indices in enumerate(character_indices):
        vals = [zp(q) for q in indices]
        total = s.S(0)
        representative_norm = None
        for ri, reciprocal in enumerate(reciprocals):
            gh = red(sum(c*gal(reciprocal, a) for c, a in zip(vals, powers)))
            norm = red(gh*gal(gh, -1))
            if ri == 0:
                representative_norm = norm
            total += norm
        ratio = s.factor(total*conductors[ki]/len(powers))
        require(ratio == expected_ratios[ki], 'unexpected full-I(1) ratio')
        rows.append({'character_index': ki, 'conductor': conductors[ki],
                     'representative_fourier_norm': str(representative_norm),
                     'full_I1_norm': str(total), 'upper_bound': str(s.Rational(len(powers), conductors[ki])),
                     'ratio': str(ratio)})
    return rows

P20 = x**4-120*x**3+2400*x**2-16000*x+32000
def inv20(red, zp):
    r5 = red(2*(zp(2)+zp(-2))-1)
    D = red(30+10*r5+(5+3*r5)*2*(zp(1)+zp(-1)))
    return s.invert(D, s.cyclotomic_poly(20, z), z)
def extra20(red, zp, P):
    r5 = red(2*(zp(2)+zp(-2))-1)
    return [s.invert(10+sign*2*r5, P, z) for sign in [1, 1, -1, -1]]
rows20 = cyclotomic_check(20, [1, 3, 9, 7],
    [[5*k*j for j in range(4)] for k in range(4)], [1, 20, 5, 20],
    inv20, extra20, P20, [s.Rational(1, 2), 1, s.Rational(1, 2), 1])
for key in ['R8_2_190', 'R8_2_489']:
    require(s.expand(casimirs[key]-P20*(x*x-20*x+80)**2) == 0, key+': Casimir mismatch')

P24 = x**4-576*x**3+11520*x**2-73728*x+147456
def inv24(red, zp):
    r2 = zp(3)+zp(-3)
    r3 = zp(2)+zp(-2)
    return red((6-2*r3-r2*r3)/48)
rows24 = cyclotomic_check(24, [1, 5, 7, 11],
    [[0, 0, 0, 0], [0, 12, 0, 12], [0, 12, 12, 0], [0, 0, 12, 12]],
    [1, 8, 12, 24], inv24, lambda red, zp, P: [s.Rational(1, 4)]*2,
    P24, [s.Rational(3, 4), 0, 1, 1])
require(s.expand(casimirs['R6_8_1660']-P24*(x-4)**2) == 0, 'R1660 Casimir mismatch')

P32 = x**8-512*x**7+43008*x**6-1376256*x**5+21626880*x**4-184549376*x**3+872415232*x**2-2147483648*x+2147483648
rows32 = cyclotomic_check(32, [pow(3, j, 32) for j in range(8)],
    [[4*k*j for j in range(8)] for k in range(8)], [1, 32, 16, 32, 8, 32, 16, 32],
    lambda red, zp: red((2-zp(1)-zp(-1))/16), lambda red, zp, P: [],
    P32, [1, 4, 0, 4, 0, 4, 0, 4])
require(s.expand(casimirs['R8_2_857']-P32) == 0, 'R857 Casimir mismatch')

mixed = []
expected = (x-8)**4*(x*x-160*x+640)*(x*x-32*x+128)
for key in ['R8_2_35', 'R8_2_38', 'R8_2_346', 'R8_2_406']:
    require(s.expand(casimirs[key]-expected) == 0, key+': mixed-field polynomial mismatch')
    q = 40*s.Rational(160**2-4*640, 640**2)
    require(q == s.Rational(9, 4), 'quadratic ratio mismatch')
    lower = 2*q/4
    require(lower == s.Rational(9, 8) and lower > 1, 'mixed-field general contradiction fails')
    mixed.append({'id': key, 'tensor_sha256': INPUTS[key]['tensor_sha256'],
                  'casimir_polynomial': str(s.factor(expected)),
                  'forced_subfield': 'Q(sqrt(2),sqrt(10))',
                  'index_over_Q_sqrt10_at_least': 2,
                  'quadratic_quantity': str(q),
                  'sphericalization_ratio_at_least': str(lower),
                  'scope': 'general_complex', 'decision': 'excluded'})

out = {'status': 'PASS', 'original_residual_tensors_checked': len(INPUTS),
       'higher_degree_cases': higher,
       'cases': {'R8_2_190': rows20, 'R8_2_489': rows20,
                 'R6_8_1660': rows24, 'R8_2_857': rows32},
       'mixed_field_general_exclusions': mixed,
       'verifier_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
(HERE/'higher_field_compression_certificate.json').write_text(json.dumps(out, indent=2)+'\n')
print(json.dumps({'status': 'PASS', 'higher_degree_cases': higher,
                  'mixed_field_general_exclusions': [r['id'] for r in mixed]}, indent=2))
