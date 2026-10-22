#!/usr/bin/env python3
"""Rebuild the terminal necessary integer model from the canonical fusion tensor.

SymPy is used only to construct Phi_1120. All model and orbit arithmetic uses
Python integers. No optimizer, floating point, binary model, or cache is used.
"""

if not __debug__:
    raise RuntimeError('Proof verification requires assertions enabled; run without -O.')
from pathlib import Path
import hashlib
import itertools
import json
import math
import sys
import sympy as sp

HERE = Path(__file__).resolve().parent
PACKAGE = HERE.parent
ROOT = HERE.parents[2]
TENSOR = ROOT / 'site/dist/downloads/fusion-tensors/R8_3_3472.txt'
TERMINAL = PACKAGE / 'terminal'
N = 1120
ORDERS = [4, 5, 7, 8, 10, 16, 20]
R = json.loads(TENSOR.read_text())
assert hashlib.sha256(json.dumps(R, separators=(',', ':')).encode()).hexdigest() == '33984d45e69ff778e70847def8349abda79ed6c0eaea242a73b533649f9b153a'
x = sp.Symbol('x')
poly = sp.Poly(sp.cyclotomic_poly(N, x), x)
degree = poly.degree()
modulus = {i: int(poly.nth(i)) for i in range(degree) if poly.nth(i)}
assert degree == 384

def add_scaled(out, vec, c=1):
    for j, a in vec.items():
        out[j] = out.get(j, 0) + c*a
        if not out[j]:
            del out[j]
    return out

powers = []
v = {0: 1}
for _ in range(N):
    powers.append(v)
    shifted = {j+1: a for j, a in v.items()}
    lead = shifted.pop(degree, 0)
    v = add_scaled(shifted, modulus, -lead)
assert v == {0: 1}

local2 = [(0, 0, 1), (1, 1, 1)] + [(2, r, 1) for r in (1, 3)] + [(a, r, 2**(a-3)) for a in range(3, 10) for r in (1, 3, 5, 7)]
local5 = [(0, 0, 1)] + [(a, r, 2*5**(a-1)) for a in range(1, 4) for r in (1, 2)]
local7 = [(0, 0, 1)] + [(a, r, 3*7**(a-1)) for a in range(1, 3) for r in (1, 3)]
orbits = [o for o in itertools.product(local2, local5, local7) if math.prod(t[2] for t in o) <= 98]
assert len(orbits) == 424

def size(o):
    return math.prod(t[2] for t in o)

def local_moment(p, t, n):
    a, r, sz = t
    if not a:
        return {0: 1}
    if p == 2:
        if a <= 2:
            return {N//(2**a)*(r*n % (2**a)): 1}
        if n % sz:
            return {}
        return {N//8*(r*(n//sz) % 8): sz}
    if n % (p**(a-1)):
        return {}
    if n % (p**a) == 0:
        return {0: sz}
    squares = sorted({j*j % p for j in range(1, p)})
    return {N//p*(r*(n//(p**(a-1)))*j % p): p**(a-1) for j in squares}

needed_exponents = {1, 2, 3}
terms_cache = {}
def terms(o, n):
    needed_exponents.add(n)
    key = (o, n)
    if key not in terms_cache:
        answer = {0: 1}
        for p, t in zip((2, 5, 7), o):
            out = {}
            for e, c in answer.items():
                for f, d in local_moment(p, t, n).items():
                    j = (e+f) % N
                    out[j] = out.get(j, 0) + c*d
            answer = out
        terms_cache[key] = answer
    return terms_cache[key]

def moment(o, n):
    answer = {}
    for e, c in terms(o, n).items():
        add_scaled(answer, powers[e], c)
    return answer

radical = add_scaled(dict(powers[N//8]), powers[7*N//8])

def chi(a):
    return 1 if a % 8 in (1, 7) else -1

power_cache = {}
def power(i, n):
    key = (i, n)
    if key not in power_cache:
        w = [1]+[0]*7
        for _ in range(n):
            w = [sum(w[j]*R[j][i][k] for j in range(8)) for k in range(8)]
        power_cache[key] = w
    return power_cache[key]

rows, rhs = [], []
lo = [0]*len(orbits)
up = [98//size(o) for o in orbits]
def push(row, b):
    row = {j: int(a) for j, a in row.items() if a}
    if not row and not b:
        return
    g = math.gcd(b, *row.values()) or 1
    rows.append({j: a//g for j, a in row.items()})
    rhs.append(b//g)

push({j: size(o) for j, o in enumerate(orbits)}, 98)
for n in (1, 2, 3):
    columns = [moment(o, n) for o in orbits]
    target = {0: -2}
    add_scaled(target, radical, -10 if n == 1 else 10 if n == 3 else 0)
    for d in range(degree):
        push({j: z.get(d, 0) for j, z in enumerate(columns)}, target.get(d, 0))

congruences = set()
def add_congruence(coeff, b, modulus):
    coeff = [c % modulus for c in coeff]
    b %= modulus
    g = math.gcd(modulus, b, *coeff)
    modulus //= g
    b //= g
    coeff = [c//g for c in coeff]
    coeff = [c if c <= modulus//2 else c-modulus for c in coeff]
    key = tuple(coeff+[b, modulus])
    if key in congruences or modulus == 1:
        return
    congruences.add(key)
    lower = sum(c*up[j] for j, c in enumerate(coeff) if c < 0)
    upper = sum(c*up[j] for j, c in enumerate(coeff) if c > 0)
    index = len(lo)
    lo.append(-(-(lower+b)//modulus))
    up.append((upper+b)//modulus)
    row = {j: c for j, c in enumerate(coeff) if c}
    row[index] = -modulus
    push(row, -b)

# Constant coefficients of the exact inverse Fourier multiplicities. The
# shift is multiplication by zeta_n^(-kt), with sqrt(2) expanded inside
# Q(zeta_1120). Cache the part independent of the source simple.
fourier_cache = {}
for n in ORDERS:
    for obj in (1, 3, 5):
        H = power(obj, n)[0]
        coeff = [[0]*len(orbits) for _ in range(n)]
        constants = [140*H]*n
        for k in range(1, n):
            g = math.gcd(n, k)
            m, ell = n//g, k//g
            a = next(a for a in range(ell, N*m, m) if math.gcd(a, N) == 1)
            vv = power(obj, g)
            total, unit = sum(vv[1:]), vv[0]
            base = sum(vv[j]*[1, 6, 6, 7, 6, 8, 8, 8][j] for j in range(8)) if m % 7 == 0 else unit+total
            key = (n, k, m*a)
            if key not in fourier_cache:
                values = []
                for t in range(n):
                    shift = k*t*N//n
                    values.append([sum(c*(powers[(e+N//8-shift) % N].get(0, 0)+powers[(e+7*N//8-shift) % N].get(0, 0)) for e, c in terms(o, m*a).items()) for o in orbits])
                fourier_cache[key] = values
            for t in range(n):
                shift = k*t*N//n
                sign = chi(a)
                values = fourier_cache[key][t]
                coeff[t] = [c+7*total*sign*v for c, v in zip(coeff[t], values)]
                constants[t] += 140*base*powers[-shift % N].get(0, 0)+14*total*sign*(powers[(N//8-shift) % N].get(0, 0)+powers[(7*N//8-shift) % N].get(0, 0))
        for t in range(n):
            add_congruence(coeff[t], constants[t], 140*n)
    print('reconstructed Fourier order', n, 'rows', len(rows), flush=True)

models = json.loads((TERMINAL/'models.json').read_text())
def unpack(model):
    return [{int(j): int(a) for j, a in r} for r in model['rows']]
base = models['base']
assert ORDERS == base['orders']
assert rows == unpack(base) and rhs == base['rhs']
assert lo == base['lo'] and up == base['up']
assert len(rows) == 362 and len(lo) == 572
base_rows = len(rows)

# Indicator field membership. Independently substitute x -> x^a in each
# already reduced moment instead of reusing moment(o, n*a) as the builder did.
seen = {tuple(sorted(row.items()))+(('rhs', b),) for row, b in zip(rows, rhs)}
field_counts = []
for n in ORDERS:
    columns = [moment(o, n) for o in orbits]
    actions = {}
    for a in range(1, N):
        if math.gcd(a, N) == 1 and a % n == 1:
            actions.setdefault((a % 8, pow(a, 2, 5), pow(a, 3, 7)), a)
    for a in actions.values():
        newrows = [{} for _ in range(degree)]
        sign = chi(a)
        for j, col in enumerate(columns):
            delta = dict(col)
            for exponent, c in col.items():
                add_scaled(delta, powers[exponent*a % N], -sign*c)
            # Separate direct power evaluation cross-checks the substitution.
            direct = add_scaled(dict(col), moment(orbits[j], n*a), -sign)
            assert delta == direct
            for d, v in delta.items():
                newrows[d][j] = v
        for d, row in enumerate(newrows):
            b = 2*(sign-1) if d == 0 else 0
            g = math.gcd(b, *row.values())
            if not g:
                continue
            row = {j: c//g for j, c in row.items()}
            b //= g
            if row and row[min(row)] < 0:
                row = {j: -c for j, c in row.items()}
                b = -b
            key = tuple(sorted(row.items()))+(('rhs', b),)
            if key not in seen:
                seen.add(key)
                rows.append(row)
                rhs.append(b)
    field_counts.append([n, len(actions), len(rows)])
field = models['field']
assert rows == unpack(field) and rhs == field['rhs']
assert ORDERS == field['orders'] and len(rows) == 628
certified = json.loads((TERMINAL/'certified_all_bounds.json').read_text())
assert list(zip(field['lo'], field['up'])) == list(map(tuple, certified['bounds']))

# Independent verification of all local Gauss-period moments used above:
# enumerate the actual primitive squared-unit cosets and reduce modulo Phi_p^a.
def remainder(values, p, a):
    if not a:
        return (sum(values),)
    step = p**(a-1)
    deg = (p-1)*step
    values = list(values)
    for j in range(len(values)-1, deg-1, -1):
        z = values[j]
        if z:
            for k in range(p-1):
                values[j-deg+k*step] -= z
    return tuple(values[:deg])

checks = 0
for p, local in ((2, local2), (5, local5), (7, local7)):
    for t in local:
        a, r, sz = t
        q = p**a
        residues = sorted({r*j*j % q for j in range(q) if math.gcd(j, q) == 1}) if a else [0]
        assert len(residues) == sz
        for n in sorted(needed_exponents):
            direct, predicted = [0]*q, [0]*q
            for j in residues:
                direct[j*n % q] += 1
            for e, c in local_moment(p, t, n).items():
                assert e*q % N == 0
                predicted[e*q//N % q] += c
            assert remainder(direct, p, a) == remainder(predicted, p, a)
            checks += 1

result = {'status': 'PASS_source_derived_terminal_model', 'tensor_sha256': hashlib.sha256(json.dumps(R, separators=(',', ':')).encode()).hexdigest(), 'orders': ORDERS, 'cyclotomic_order': N, 'cyclotomic_degree': degree, 'orbit_types': len(orbits), 'base_rows': base_rows, 'field_rows_added': len(rows)-base_rows, 'final_rows': len(rows), 'variables': len(lo), 'local_moment_checks': checks, 'moment_exponents_checked': len(needed_exponents), 'per_order_field_actions_cumulative_rows': field_counts, 'arithmetic': 'Python arbitrary-precision integers; no solver or saved binary model', 'model_json_sha256': hashlib.sha256((TERMINAL/'models.json').read_bytes()).hexdigest()}
if '--write' in sys.argv:
    (HERE/'replay.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps(result, indent=2))
