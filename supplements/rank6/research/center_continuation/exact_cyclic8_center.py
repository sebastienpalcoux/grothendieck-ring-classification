"""Exact full modular-data/ring-map check for the cyclic-eight candidate center.
Arithmetic is Z[x]/Phi_136(x), Phi_136=sum_{j=0}^16(-x^4)^j.
No associator, tensor functor, algebra object, or target categorification is claimed.
"""
import json, hashlib, itertools, time, sys, argparse
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
n = 22
degree = 64
den = 136
ap = argparse.ArgumentParser(description=__doc__)
ap.add_argument('--tensor-certificate', type=Path, default=OUT/'cyclic8_center_tensor.json')
ap.add_argument('--write', action='store_true')
args = ap.parse_args()
# Every field product has at most 64*2**48 < 2**55 before reduction.
# The closed reduction formula combines at most four coefficients,
# staying below 2**57. Outputs are bounded by 2**24.
# N <= 32 bounds all subsequent 22-term matrix products and 484-term
# indicator sums by 32*484*2**24 < 2**39, hence safely inside int64.
FIELD_BOUND = 2**24

def field_bound(p):
    if np.max(np.abs(p), initial=0) > FIELD_BOUND:
        raise AssertionError('field coefficient exceeded certified arithmetic bound')
    return p

def reduce(p):
    # Phi_136 divides x^68+1. Fold degrees >=68 once, then replace
    # x^(64+r) using Phi_136. Each output combines at most four
    # input coefficients, so the pre-reduction 2**55 bound stays <2**57.
    if len(p)>136:
        raise AssertionError('unexpected polynomial degree')
    p = np.array(p, dtype=np.int64)
    if len(p)<136:
        p=np.pad(p,(0,136-len(p)))
    for k in range(135,67,-1):
        p[k-68]-=p[k]
    for r in range(4):
        z=p[64+r]
        for j in range(16):
            p[4*j+r]-=z*(-1)**j
    return field_bound(p[:degree])

def mul(a, b):
    field_bound(a); field_bound(b)
    return reduce(np.convolve(a, b))

def power(k):
    k %= 136
    p = np.zeros(k + 1, dtype=np.int64)
    p[k] = 1
    return reduce(p)
I = power(0)
zero = np.zeros(degree, dtype=np.int64)
leg = lambda a: 1 if pow(a % 17, 8, 17) == 1 else -1
sqrt17 = sum((leg(j) * power(8 * j) for j in range(1, 17)), zero.copy())
if not np.array_equal(mul(sqrt17, sqrt17), 17 * I):
    raise AssertionError('exact verification failed')
labels = [('0',), ('pi',), ('sig', 0, 1), ('sig', 2, 1), ('phi', 1), ('phi', -1)] + [('sig', 1, k) for k in range(4)] + [('xi', j) for j in range(1, 9)] + [('psi', e, f) for e, f in itertools.product([1, -1], repeat=2)]
loc = {v: i for i, v in enumerate(labels)}

def ss(v, w):
    if loc[v] > loc[w]:
        return ss(w, v)
    if v == ('0',):
        return 17 * I - 4 * sqrt17 if w == ('0',) else 17 * I + 4 * sqrt17 if w == ('pi',) else 34 * I if w[0] == 'sig' else 8 * sqrt17 if w[0] == 'xi' else 17 * I
    if v == ('pi',):
        return 17 * I - 4 * sqrt17 if w == ('pi',) else 34 * I if w[0] == 'sig' else -8 * sqrt17 if w[0] == 'xi' else 17 * I
    if v[0] == 'sig':
        if w[0] == 'sig':
            _, g, k = v
            _, h, l = w
            return 34 * (power(34 * (g * h + g * l + h * k)) + power(-34 * (g * h + g * l + h * k)))
        if w[0] == 'phi':
            return (-1) ** v[1] * 34 * I
        if w[0] == 'psi':
            return w[1] ** v[1] * (-1) ** v[2] * 34 * I
        return zero.copy()
    if v[0] == 'phi':
        if w[0] == 'phi':
            return (17 + 68 * v[1] * w[1]) * I
        if w[0] == 'sig':
            return (-1) ** w[1] * 34 * I
        if w[0] == 'psi':
            return 17 * I
        return zero.copy()
    if v[0] == 'xi':
        return -8 * mul(sqrt17, power(48 * v[1] * w[1]) + power(-48 * v[1] * w[1])) if w[0] == 'xi' else zero.copy()
    if v[0] == 'psi' and w[0] == 'psi':
        return (17 - 68 * v[2] * w[2] * (v[1] == w[1])) * I
    raise ValueError((v, w))
start = time.monotonic()
S = np.array([[ss(v, w) for w in labels] for v in labels])
tp = [0 if v[0] in ['0', 'pi', 'phi'] else 17 * (v[1] ** 2 + 2 * v[1] * v[2]) % 136 if v[0] == 'sig' else 24 * v[1] ** 2 % 136 if v[0] == 'xi' else 68 for v in labels]
T = [power(k) for k in tp]
record = json.loads(args.tensor_certificate.read_text())
if record.get('labels') != [list(v) for v in labels]:
    raise AssertionError('certificate labels differ from the source ordering')
rawN = record.get('N')
if not (isinstance(rawN,list) and len(rawN)==n and
        all(isinstance(row,list) and len(row)==n and
            all(isinstance(col,list) and len(col)==n and
                all(type(z) is int and 0 <= z <= 32 for z in col) for col in row)
            for row in rawN)):
    raise AssertionError('invalid center tensor shape, integrality or bound')
expectedF = [[1,0,0,0,0,0], [1,0,2,2,2,2],
             [1,1,1,3,2,2], [1,1,3,1,2,2],
             [1,0,0,0,2,2], [1,0,2,2,0,0]] + \
            [[0,0,2,2,1,3]]*4 + [[0,0,2,2,2,2]]*8 + \
            [[0,1,1,1,1,1]]*4
rawF=record.get('F')
if not (isinstance(rawF,list) and len(rawF)==n and
        all(isinstance(row,list) and len(row)==6 and
            all(type(z) is int and z>=0 for z in row) for row in rawF)):
    raise AssertionError('invalid restriction shape or nonnegative integrality')
if rawF != expectedF or rawF[0] != [1,0,0,0,0,0]:
    raise AssertionError('restriction differs from the stated unital map')
N = np.array(rawN, dtype=np.int64)
F = np.array(rawF, dtype=np.int64)
d = 4*I+sqrt17
rdims = [I,I,d,d,d-I,d+I]
for a in range(n):
    fd = sum((int(F[a,i])*rdims[i] for i in range(6)),zero.copy())
    if not np.array_equal(mul(fd,S[0,0]),S[0,a]):
        raise AssertionError(('dimension preservation',a))
if not ((N >= 0).all() and np.array_equal(N[0], np.eye(n, dtype=np.int64))):
    raise AssertionError('exact verification failed')
if not (np.array_equal(N, N.transpose(1, 0, 2)) and np.array_equal(N, N.transpose(2, 1, 0))):
    raise AssertionError('exact verification failed')
if not np.array_equal(N[:, :, 0], np.eye(n, dtype=np.int64)):
    raise AssertionError('exact verification failed')
if not np.array_equal(S, S.transpose(1, 0, 2)):
    raise AssertionError('exact verification failed')
for l in range(n):
    lhs = np.array([mul(S[k, l], S[0, l]) for k in range(n)])
    sums = np.einsum('ijk,ka->ija', N, lhs)
    for i in range(n):
        for j in range(n):
            if not np.array_equal(sums[i, j], mul(S[i, l], S[j, l])):
                raise AssertionError(('eigen', i, j, l))
print('exact Verlinde spectral identities passed', flush=True)
for i in range(n):
    for j in range(i, n):
        sq = sum((mul(S[i, k], S[k, j]) for k in range(n)), zero.copy())
        if not np.array_equal(sq, den * den * I if i == j else zero):
            raise AssertionError(('S2', i, j))
        sts = sum((mul(mul(S[i, k], T[k]), S[k, j]) for k in range(n)), zero.copy())
        tst = den * mul(S[i, j], power(-tp[i] - tp[j]))
        if not np.array_equal(sts, tst):
            raise AssertionError(('STS', i, j))
print('exact modular relations passed', flush=True)
R = np.array(next((r for r in json.loads((ROOT / 'data/census.json').read_text()) if r['id'] == 'R6_3_215'))['N'])
if R.shape!=(6,6,6) or np.max(np.abs(R))>32:
    raise AssertionError('target tensor shape or arithmetic bound failed')
if not np.array_equal(np.einsum('abc,ck->abk', N, F), np.einsum('ai,bj,ijk->abk', F, F, R)):
    raise AssertionError('exact verification failed')
if not np.array_equal(np.einsum('abx,xcd->abcd', N, N), np.einsum('bcx,axd->abcd', N, N)):
    raise AssertionError('exact verification failed')
fs = []
for a in range(n):
    v = sum((int(N[i, j, a]) * mul(mul(S[0, i], S[0, j]), power(2 * tp[i] - 2 * tp[j])) for i in range(n) for j in range(n) if N[i, j, a]), zero.copy())
    if not np.array_equal(v, den * den * I):
        raise AssertionError(('FS2', a))
    fs.append(1)
record.update(status='exact modular datum and based ring homomorphism; target categorification not established', source='Grossman-Izumi, Quantum Topology13(2022), Theorem6.8 at m=2 and Example6.10', source_url='https://ems.press/content/serial-article-files/36923', twists_as_136th_root_exponents=tp, second_indicators=fs, coefficient_equations_verified=2904, Verlinde_spectral_equations_verified=10648, arithmetic='Z[x]/Phi_136(x), all S denominators136', seconds=time.monotonic() - start)
modular_record = {'denominator': den, 'cyclotomic_order': 136, 'labels': [list(v) for v in labels], 'S_coefficients': S.tolist(), 'T_exponents': tp}
if args.write:
    (OUT / 'cyclic8_center_tensor.json').write_text(json.dumps(record, separators=(',', ':')) + '\n')
    (OUT / 'cyclic8_modular_data.json').write_text(json.dumps(modular_record, separators=(',', ':')) + '\n')
elif json.loads((OUT / 'cyclic8_modular_data.json').read_text()) != modular_record:
    raise AssertionError('frozen modular data differs')
print(json.dumps({k: record[k] for k in ['status', 'second_indicators', 'coefficient_equations_verified', 'Verlinde_spectral_equations_verified', 'seconds']}, indent=2))
