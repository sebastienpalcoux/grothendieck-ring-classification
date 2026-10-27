#!/usr/bin/env python3
"""Short exact checks for R6_8_1660; no categorical existence claim."""
from pathlib import Path
import hashlib, itertools, json, math, runpy

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
def need(condition, message):
    if not condition:
        raise RuntimeError(message)

SOURCE = ROOT / 'data/current_remaining_cases.py'
N = runpy.run_path(str(SOURCE))['TENSORS']['R6_8_1660']
tensor_hash = hashlib.sha256(json.dumps(N, separators=(',', ':')).encode()).hexdigest()
need(tensor_hash == '697ec27fe203356199bfcf674587be9c71455dbb681f2e086a076f726b03d267', 'Source tensor hash mismatch')

def red(a):
    a = list(a) + [0] * max(0, 16 - len(a))
    for k in range(len(a) - 1, 15, -1):
        a[k - 8] += a[k]
        a[k - 16] -= a[k]
    return tuple(a[:16])

def z(k):
    a = [0] * 48
    a[k % 48] = 1
    return red(a)

def add(a, b): return tuple(x + y for x, y in zip(a, b))
def scale(a, n): return tuple(n * x for x in a)
def sub(a, b): return add(a, scale(b, -1))
def mul(a, b):
    c = [0] * 31
    for i, v in enumerate(a):
        for j, w in enumerate(b): c[i + j] += v * w
    return red(c)
def auto(a, k):
    out = red([])
    for j, v in enumerate(a): out = add(out, scale(z(j * k), v))
    return out

one = z(0)
r = add(z(6), z(42))
s = add(z(4), z(44))
d = add(add(scale(one, 3), scale(r, 2)), add(scale(s, 2), mul(r, s)))
mom_source = HERE / 'all_indicators_source.json'
moment_data = json.loads(mom_source.read_text())
need(moment_data['source_tensor_sha256'] == tensor_hash, 'Indicator tensor binding mismatch')
surviving_moments = [c['moments_ascending_zeta48_coefficients']
                     for c in moment_data['cases'] if c['cyclic_dimension_three_compatible']]
need(len(surviving_moments) == 2, 'Unexpected indicator branch count')
mom = surviving_moments[0]
third_x = red(list(map(int, mom['3']['X'])))
third_t = red(list(map(int, mom['3']['T'])))
need(third_x == add(one, z(8)) and third_t == scale(one, 2), 'Third indicator mismatch')
need(auto(third_x, 47) != third_x, 'Third indicator unexpectedly real')
conjugate_pair = {third_x, auto(third_x, 47)}
need({auto(third_x, k) for k in range(48) if math.gcd(k, 48) == 1} == conjugate_pair, 'Unexpected Galois orbit')
need({red(list(map(int, m['3']['X']))) for m in surviving_moments} == conjugate_pair,
     'Surviving indicator branches are not the conjugate pair')
need(all(red(list(map(int, m['3']['T']))) == scale(one, 2) for m in surviving_moments),
     'Surviving T indicator mismatch')
W3 = add(one, add(scale(mul(d, third_x), 2), scale(mul(r, d), 2)))
need(sub(W3, auto(W3, 47)) == scale(mul(d, sub(z(8), z(40))), 2), 'Weighted indicator imaginary part mismatch')
need(W3 != auto(W3, 47), 'Weighted indicator unexpectedly real')

auts = []
for tail in itertools.permutations(range(1, 6)):
    p = (0,) + tail
    if all(N[p[i]][p[j]][p[k]] == N[i][j][k]
           for i, j, k in itertools.product(range(6), repeat=3)):
        auts.append(list(p))
need(auts == [[0,1,2,3,4,5], [0,1,3,2,4,5]], 'Ring automorphisms mismatch')
dual = [next(j for j in range(6) if N[i][j][0]) for i in range(6)]
induced_unit = [sum(N[i][dual[i]][k] for i in range(6)) for k in range(6)]
need(induced_unit == [6,2,12,12,0,16], 'Induced-unit restriction mismatch')

# Exhaust the full 76 x 7 irreducible table, not only a prior chosen witness.
tab_dir = ROOT / 'evidence/theoretical_20261016/rank6/r1660_modular_witness/inputs'
tables = {m: json.loads((tab_dir / f'sl2_{m}.json').read_text()) for m in (16, 3)}
support = {0,8,9,12,14,15,20,24,26,30,32,33,36,39,42,44}
spin_phases = {9,15,33,39}
spin_odd = []
allowed = []
for i, a in enumerate(tables[16]['irreps']):
    for j, b in enumerate(tables[3]['irreps']):
        spec = [0] * 48
        for u, v in enumerate(a['T_multiplicities']):
            for w, x in enumerate(b['T_multiplicities']): spec[(3*u+16*w)%48] += v*x
        if any(v and k not in support for k, v in enumerate(spec)): continue
        rec = {'factors':[i,j], 'degree':a['degree']*b['degree'],
               'central_sign':a['central_sign']*b['central_sign'],
               'spectrum':[[k,v] for k,v in enumerate(spec) if v]}
        allowed.append(rec)
        if rec['central_sign'] == -1 and any(spec[k] for k in spin_phases): spin_odd.append(rec)
need([r['factors'] for r in spin_odd] == [[16,2], [20,2], [44,2]], 'Unexpected spin irreducible')
need(len(allowed) == 42, 'Allowed irreducible count mismatch')

receipt = {
    'status':'PASS', 'ring':'R6_8_1660', 'classification':'UNRESOLVED',
    'tensor_sha256':tensor_hash,
    'inputs_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
                    for p in [SOURCE, mom_source, tab_dir/'sl2_16.json', tab_dir/'sl2_3.json']},
    'ring_automorphisms':auts,
    'induced_unit_restriction':induced_unit,
    'negative_second_indicator_sigma_absent_from_induced_unit':induced_unit[4] == 0,
    'third_X_ascending_zeta48':third_x,
    'all_cyclotomic_conjugates_nonreal':True,
    'positive_weighted_third_indicator_nonreal':True,
    'allowed_irreps_by_phase_support':len(allowed),
    'spin_odd_irreps':spin_odd,
    'spin_odd_summand_alternatives':[[[16,2],[20,2]], [[44,2]]],
    'source_ring_excluded':False, 'categorification_constructed':False,
}
(HERE / 'verification.json').write_text(json.dumps(receipt, indent=2)+'\n')
print(json.dumps({k:receipt[k] for k in ['status','classification','ring_automorphisms',
      'all_cyclotomic_conjugates_nonreal','positive_weighted_third_indicator_nonreal',
      'allowed_irreps_by_phase_support','spin_odd_summand_alternatives']}, indent=2))
