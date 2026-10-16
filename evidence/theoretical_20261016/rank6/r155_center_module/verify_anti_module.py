"""Exact replay of a natural based module for the rank-26 R155 candidate.

This is a passing necessary condition, not a module-category construction.
Python 3 standard library only; all matrix entries are arbitrary-precision ints.
"""
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
source = HERE.parent/'r155_reflection/r155_data.json'
raw = source.read_bytes()
expected_hash = '769250938d8bd0c8a251aaacc18832174af8175ed9b44fc487ec3f6d04357353'

def require(ok, message):
    if not ok:
        raise ValueError(message)

require(hashlib.sha256(raw).hexdigest() == expected_hash, 'source modular datum mismatch')
data = json.loads(raw)
R, dual = data['fusion'], data['duality']
witness = json.loads((HERE/'anti_module_witness.json').read_text())
T = witness['anti_matrices']
fixed = witness['fixed']
perm = [row.index(1) for row in R[0]]
require(fixed == [i for i in range(26) if perm[i] == i] == [4, 7, 20, 21, 24, 25],
        'fermion fixed-label mismatch')
free = [i for i in range(26) if i < perm[i]]
n = len(free)+2*len(fixed)
require(n == 22, 'wrong module rank')

def identity(n, sign=1):
    return [[sign*int(i == j) for j in range(n)] for i in range(n)]

def transpose(A):
    return list(map(list, zip(*A)))

def multiply(A, B):
    n = len(A)
    C = [[0]*n for _ in range(n)]
    for i in range(n):
        for k, c in enumerate(A[i]):
            if c:
                for j, b in enumerate(B[k]):
                    C[i][j] += c*b
    return C

def linear(coefficients, matrices):
    n = len(matrices[0])
    out = [[0]*n for _ in range(n)]
    for c, A in zip(coefficients, matrices):
        if c:
            for i in range(n):
                for j in range(n):
                    out[i][j] += c*A[i][j]
    return out

require(T[0] == identity(6, -1) and T[1] == identity(6), 'wrong anti-sector unit/sign')
for i in range(26):
    require(transpose(T[i]) == T[dual[i]], 'anti-sector dual-transpose mismatch')
    for a, u in enumerate(fixed):
        for b, v in enumerate(fixed):
            require(abs(T[i][a][b]) <= R[i][u][v] and
                    (T[i][a][b]-R[i][u][v]) % 2 == 0, 'anti-sector bound/parity failure')
for i in range(26):
    for j in range(26):
        require(multiply(T[i], T[j]) == linear(R[i][j], T), 'anti-sector fusion failure')

# Faddeev--LeVerrier checks the natural generator spectrum exactly.
B = identity(6)
characteristic = [1]
for k in range(1, 7):
    B = multiply(T[16], B)
    trace = sum(B[i][i] for i in range(6))
    require(trace % k == 0, 'nonintegral characteristic coefficient')
    c = -trace//k
    characteristic.append(c)
    for i in range(6):
        B[i][i] += c
require(characteristic == [1, 0, 9, 0, -1, 0, -9], 'natural generator spectrum mismatch')

# Reconstruct the full nonnegative based-module matrices from orbit and split labels.
M = [[[0]*n for _ in range(n)] for _ in range(26)]
for i in range(26):
    for a, u in enumerate(free):
        for b, v in enumerate(free):
            M[i][a][b] = R[i][u][v]+R[i][u][perm[v]]
        for b, v in enumerate(fixed):
            for sign in range(2):
                M[i][a][len(free)+2*b+sign] = R[i][u][v]
    for a, u in enumerate(fixed):
        for sign in range(2):
            row = len(free)+2*a+sign
            for b, v in enumerate(free):
                M[i][row][b] = R[i][u][v]
            for b, v in enumerate(fixed):
                for other in range(2):
                    M[i][row][len(free)+2*b+other] = (
                        R[i][u][v]+(-1)**(sign+other)*T[i][a][b])//2
require(M[data['unit']] == identity(n), 'based-module unit mismatch')
require(all(c >= 0 for A in M for row in A for c in row), 'negative based-module entry')
require(all(transpose(M[i]) == M[dual[i]] for i in range(26)), 'based-module dual mismatch')
for i in range(26):
    for j in range(26):
        require(multiply(M[i], M[j]) == linear(R[i][j], M), 'based-module fusion failure')

digest = lambda obj: hashlib.sha256(json.dumps(obj, separators=(',', ':')).encode()).hexdigest()
receipt = {
    'status': 'PASS', 'mathematical_verdict': 'PASS_NECESSARY',
    'source_data_sha256': expected_hash,
    'fermion_label': 0, 'fixed_labels': fixed, 'anti_invariant_rank': 6,
    'module_rank': n, 'anti_fusion_identities_checked': 676,
    'generator16_characteristic_polynomial': '(x^2+9)(x^2+1)(x^2-1)',
    'based_module_fusion_identities_checked': 676,
    'anti_matrices_sha256': digest(T), 'based_module_matrices_sha256': digest(M),
    'verifier_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'scope': 'Integer based-module witness only. No associator, module category, or categorification is constructed. R6_4_155 remains unresolved.',
}
(HERE/'receipt.json').write_text(json.dumps(receipt, indent=2)+'\n')
print(json.dumps(receipt, indent=2))
