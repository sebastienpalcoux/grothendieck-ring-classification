"""Exact source-bound arithmetic for the general exclusion of R8_2_857.

Uses Python 3, SymPy, and rational arithmetic in Q[z]/(z^16+1).
No floating point, signed-table search, or associator enumeration.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import sympy as s

HERE = Path(__file__).resolve().parent
INPUTS = json.loads((HERE / 'source_tensors.json').read_text())
entry = INPUTS['R8_2_857']
raw = entry['tensor']
digest = hashlib.sha256(json.dumps(raw, separators=(',', ':')).encode()).hexdigest()

def require(ok, message):
    if not ok:
        raise ValueError(message)

require(digest == entry['tensor_sha256'], 'source tensor hash mismatch')
perm = [0, 1, 7, 2, 5, 4, 3, 6]
R = [[[raw[i][j][k] for k in perm] for j in perm] for i in perm]
require(all(R[i][j][0] == int(i == j) for i in range(8) for j in range(8)),
        'source is not completely self-dual')

# Exact cyclotomic arithmetic. z is a primitive 32nd root.
ZERO = (F(0),) * 16
ONE = (F(1),) + (F(0),) * 15

def add(*rows):
    return tuple(sum(row[j] for row in rows) for j in range(16))

def scale(row, q):
    return tuple(q*v for v in row)

def zp(n):
    n %= 32
    row = list(ZERO)
    row[n % 16] = F(1 if n < 16 else -1)
    return tuple(row)

def mul(a, b):
    out = [F(0)] * 16
    for i, av in enumerate(a):
        if not av:
            continue
        for j, bv in enumerate(b):
            k = i+j
            out[k % 16] += av*bv*(1 if k < 16 else -1)
    return tuple(out)

def gal(a, power):
    return add(*(scale(zp(i*power), v) for i, v in enumerate(a)))

ds = [add(*(zp(r) for r in range(-j, j+1))) for j in range(8)]
for i in range(8):
    for j in range(8):
        require(mul(ds[i], ds[j]) == add(*(scale(ds[k], R[i][j][k]) for k in range(8))),
                'dimension character product mismatch')
D = add(*(mul(v, v) for v in ds))
invD = scale(add(scale(ONE, 2), scale(zp(1), -1), scale(zp(-1), -1)), F(1, 16))
require(mul(D, invD) == ONE, 'reciprocal global dimension mismatch')
powers = [pow(3, j, 32) for j in range(8)]
require(len({min(a, 32-a) for a in powers}) == 8, 'wrong Galois generator')
require(len({gal(ds[1], a) for a in powers}) == 8, 'dimension field has degree below eight')
fourier = []
for k in range(8):
    gh = add(*(mul(zp(4*k*j), gal(invD, a)) for j, a in enumerate(powers)))
    norm = mul(gh, gal(gh, -1))
    expected = F(1) if k == 0 else (F(1, 8) if k % 2 else F(0))
    require(norm == scale(ONE, expected), 'Fourier norm mismatch')
    fourier.append({'character_index': k,
                    'primitive_conductor_32': bool(k % 2),
                    'squared_norm': str(expected),
                    'fourier_coefficients_zeta32': [str(v) for v in gh]})

x = s.Symbol('x')
I = s.eye(8)
N = [s.Matrix(M) for M in R]
J = s.diag(0, 1, 1, 1, 1, 1, 1, 2)
for i in range(7):
    J[i, i+1] = J[i+1, i] = 1
require(J == N[1], 'source generator is not the stated Jacobi matrix')
M = [I, J]
for j in range(1, 7):
    M.append((J-I)*M[j]-M[j-1])
require(M == N, 'source does not satisfy the complete polynomial recurrence')
require(s.Poly(J.charpoly(x).as_expr(), x).is_irreducible,
        'source generator polynomial is not irreducible')
require(all(R[1][j][j] == R[j][j][1] == 1 for j in range(1, 7)),
        'multiplicity-one square channel mismatch')

branches = []
for t in [-2, 0, 2]:
    Jt = J.copy()
    Jt[7, 7] = t
    cp = s.factor(Jt.charpoly(x).as_expr())
    if t == -2:
        bad = (Jt*Jt-Jt-I)[7, 7]
        require(bad == 6 and R[2][7][7] == 2, 'negative endpoint bound mismatch')
        why = 'signed coefficient 6 exceeds original multiplicity 2'
    elif t == 0:
        expected = (x-1)*(x+1)*(x*x-2*x-1)*(x**4-4*x**3+2*x*x+4*x-1)
        require(s.expand(cp-expected) == 0, 'zero endpoint factorization mismatch')
        require(max(s.degree(f, x) for f, _ in s.factor_list(cp)[1]) == 4,
                'zero endpoint permits degree eight')
        why = 'generator field has degree at most 4, contradicting forced degree 8'
    else:
        require(Jt == N[1] and M == N, 'positive endpoint not source ring')
        why = 'all signed products positive, producing an excluded spherical categorification'
    branches.append({'last_diagonal': t, 'generator_polynomial': str(cp), 'contradiction': why})

certificate = {
    'status': 'PASS', 'id': 'R8_2_857', 'decision': 'excluded',
    'scope': 'general_complex', 'tensor_sha256': digest,
    'source_label_order': perm, 'dimension_field': 'Q(zeta_32 + zeta_32^-1)',
    'dimension_field_degree': 8, 'primitive_conductor': 32,
    'global_dimension': '4*csc(pi/32)^2',
    'reciprocal_global_dimension': '(2-zeta_32-zeta_32^-1)/16',
    'fourier_norms': fourier,
    'spherical_conductor_ratio': '4',
    'sphericalization_compression_lower_bound': 'e^2/4',
    'sphericalization_compression_upper_bound': 'e/4',
    'forced_sphericalization_field_index': 1,
    'signed_branches': branches,
    'proof': 'R857_GENERAL_PROOF.md',
    'verifier_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
}
(HERE / 'R857_general_certificate.json').write_text(json.dumps(certificate, indent=2) + '\n')
print(json.dumps({k: certificate[k] for k in ['status', 'id', 'decision', 'scope',
      'tensor_sha256', 'dimension_field_degree', 'spherical_conductor_ratio']}, indent=2))
