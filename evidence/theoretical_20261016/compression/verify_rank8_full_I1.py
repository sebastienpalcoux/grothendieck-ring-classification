"""Exact tensor and character audit for the two full-I(1) scoped exclusions.

The categorical theorem is proved in full_I1_compression.tex. This verifier
checks its finite arithmetic inputs; it does not claim arbitrary nonpivotal
noncategorifiability. Run with ordinary Python 3 and SymPy.
"""
import hashlib
import json
from pathlib import Path
import sympy as s

HERE = Path(__file__).resolve().parent
INPUTS = json.loads((HERE / 'source_tensors.json').read_text())
TENSORS = {k: v['tensor'] for k, v in INPUTS.items()}
LEDGER = INPUTS
r = s.sqrt(2)
x = s.Symbol('x')
CHARACTERS = {
    'R8_2_318': [
        [1, 2, 2, -2, 1, -1, -1, 0],
        [1, 0, 0, 2, 1, -1, -1, 0],
        [1, 2*s.I, -2*s.I, 0, 1, 1, 1, -2],
        [1, -2*s.I, 2*s.I, 0, 1, 1, 1, -2],
        [1, 0, 0, 0, -1, -1-r, 1+r, 0],
        [1, 0, 0, 0, -1, -1+r, 1-r, 0],
        [1, 2+2*r, 2+2*r, 2+2*r, 1, 3+2*r, 3+2*r, 4+2*r],
        [1, 2-2*r, 2-2*r, 2-2*r, 1, 3-2*r, 3-2*r, 4-2*r],
    ],
    'R8_2_735': [
        [1, 1, 1, 1, 0, 2, -2, -2],
        [1, 1, 1, 1, 0, -2, 2, -2],
        [1, 1, -1, -1, 2, 0, 0, 0],
        [1, 1, -1, -1, -2, 2, 2, 0],
        [1, -1, -1+r, 1-r, 0, 0, 0, 0],
        [1, -1, -1-r, 1+r, 0, 0, 0, 0],
        [1, 1, 3+2*r, 3+2*r, 2+2*r, 2+2*r, 2+2*r, 4+2*r],
        [1, 1, 3-2*r, 3-2*r, 2-2*r, 2-2*r, 2-2*r, 4-2*r],
    ],
}

def require(condition, message):
    if not condition:
        raise ValueError(message)

reports = []
for key, chars in CHARACTERS.items():
    R = TENSORS[key]
    digest = hashlib.sha256(json.dumps(R, separators=(',', ':')).encode()).hexdigest()
    require(digest == LEDGER[key]['tensor_sha256'], key + ': source tensor mismatch')
    n = len(R)
    dual = [next(j for j in range(n) if R[i][j][0]) for i in range(n)]
    require(all(R[i][j] == R[j][i] for i in range(n) for j in range(n)),
            key + ': noncommutative input')
    codegrees = []
    for c in chars:
        for i in range(n):
            for j in range(n):
                require(s.expand(c[i]*c[j] - sum(R[i][j][k]*c[k] for k in range(n))) == 0,
                        key + ': invalid character')
        codegrees.append(s.expand(sum(c[i]*c[dual[i]] for i in range(n))))
    require(s.simplify(s.Matrix(chars).det()) != 0, key + ': incomplete character table')
    require(all(any(v == 0 for v in c) for c in chars[:6]),
            key + ': unexpected everywhere-nonzero character')
    require(all(c[i] == c[dual[i]] for c in chars[6:] for i in range(n)),
            key + ': candidate pivotal dimensions are not spherical')
    require(all(v > 0 for v in chars[6]), key + ': wrong positive character')
    N = [s.Matrix(M) for M in R]
    B = sum((M*M.T for M in N), s.zeros(n))
    casimir = s.factor(B.charpoly(x).as_expr())
    expected = (x-16)**3*(x-8)*(x*x-192*x+1024)*(x*x-16*x+32)
    require(s.expand(casimir-expected) == 0, key + ': wrong Casimir polynomial')
    ratio = 8*(s.Rational(192**2-4*1024, 1024**2)
               + s.Rational(16**2-4*32, 32**2))
    require(ratio == s.Rational(5, 4), key + ': compression arithmetic')
    reports.append({
        'id': key, 'tensor_sha256': digest, 'dual': dual,
        'characters': [[str(v) for v in c] for c in chars],
        'formal_codegrees': [str(v) for v in codegrees],
        'casimir_polynomial': str(casimir),
        'quadratic_field': 'Q(sqrt(2))', 'conductor': 8,
        'compression_ratio': str(ratio),
        'categorical_scope': 'no pivotal or spherical categorification',
        'general_scope': 'arbitrary nonpivotal categorification remains unresolved',
    })

result = {'status': 'PASS', 'cases': reports}
Path(__file__).with_name('rank8_full_I1_certificate.json').write_text(
    json.dumps(result, indent=2) + '\n')
print(json.dumps({'status': 'PASS', 'cases': list(CHARACTERS),
                  'compression_ratio': '5/4', 'scope': 'pivotal and spherical'}, indent=2))
