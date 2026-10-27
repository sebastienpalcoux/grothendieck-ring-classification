#!/usr/bin/env python3
"""Independent short exact audit; does not import a producer verifier.

Completeness of the preceding 61-factor domain is inherited explicitly.
All 61 are refiltered here, and all 21 retained profiles are recomputed.
"""
from collections import Counter
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
RID = 'R8_3_1768'
BINDINGS = {
    'evidence/rank8_next_20261021/quadratic/profile_closure.json':
        '6b48256765fb6380a3080669b0d6b5c20f924f3c8277308aa036cc47c1e28140',
    'evidence/rank8_research_20261022/pointed_followup/r1768_modules/verification.json':
        'bf9cc03425acae958b9fe9a7a521350600614b5d3e8e44fbde424925edfcb11d',
}


def need(ok, message):
    if not ok:
        raise ValueError(message)


def read(name):
    return json.loads((ROOT / name).read_text())


def mul(x, y):
    return (x[0]*y[0]+37*x[1]*y[1], x[0]*y[1]+x[1]*y[0])


def div(x, y):
    norm = y[0]*y[0]-37*y[1]*y[1]
    need(norm != 0, 'zero quadratic denominator')
    z = mul(x, (y[0], -y[1]))
    return (F(z[0], norm), F(z[1], norm))


def encode(x):
    return [str(x[0]), str(x[1])]


def run():
    for path, digest in BINDINGS.items():
        need(hashlib.sha256((ROOT/path).read_bytes()).hexdigest() == digest,
             'source hash: '+path)
    row = read('evidence/unresolved_retry_20261024/proofs/unresolved11_20261024/inputs/R8_3_1768.json')
    R = row['fusion_tensor']
    need(hashlib.sha256(json.dumps(R, separators=(',', ':')).encode()).hexdigest()
         == '240509807c67da437c86f2a51efeb831364734feb93ed18a1d2f32087ebc1af0',
         'canonical tensor')
    ds = [(1,0),(1,0),(5,1),(6,1),(7,1),(7,1),(6,1),(5,1)]
    dim = lambda v: tuple(sum(v[i]*ds[i][k] for i in range(8)) for k in range(2))
    for i in range(8):
        for j in range(8):
            need(mul(ds[i],ds[j]) == dim(R[i][j]), 'FP character')
    need([next(j for j in range(8) if R[i][j][0]) for i in range(8)]
         == list(range(8)), 'all simples selfdual')
    gp = [next(j for j in range(8) if R[1][i][j]) for i in range(8)]
    need(gp == [1,0,7,6,5,4,3,2], 'pointed action')
    preceding = read('evidence/rank8_next_20261021/quadratic/profile_closure.json')[RID]
    factors = preceding['surviving_factors']
    need(len(factors) == 61, 'full inherited factor count')
    old_filter = read('evidence/rank8_research_20261022/pointed_followup/r1768_modules/verification.json')
    old_kept = {(r['candidate_index'],r['factor_index'])
                for r in old_filter['factor_filter'] if r['survives']}
    all_keys = [(f['candidate_index'], f['factor_index']) for f in factors]
    need(len(set(all_keys)) == 61, 'no duplicate inherited factors')
    kept = []
    rejected = 0
    for f in factors:
        B = f['B']; a = B[0]; n = len(B)
        need(all(any(v) for v in B), 'nonzero rows')
        for i in range(8):
            for j in range(8):
                need(sum(v[i]*v[j] for v in B) == sum(a[k]*R[i][k][j] for k in range(8)),
                     'exact induction Gram')
        counts = Counter(tuple(v) for v in B)
        passes = n != 2
        for v, count in counts.items():
            gv = tuple(v[gp[i]] for i in range(8))
            passes = passes and counts[gv] == count and (gv != v or count % 2 == 0)
        key = (f['candidate_index'],f['factor_index'])
        need(passes == (key in old_kept), 'independent free-action filter')
        if not passes:
            rejected += 1
            continue
        root = dim(a)
        need(root == tuple(map(F, f['root_dimension'])), 'root dimension')
        profile = [div(mul(dim(v),dim(v)),root) for v in B]
        need(sorted(profile) == sorted(tuple(map(F,p)) for p in f['profile']),
             'independent full profile')
        odd = [(i,p) for i,p in enumerate(profile) if p[1].denominator == 1 and p[1] % 2]
        units = [i for i,p in enumerate(profile) if p == (1,0)]
        need(bool(odd) != bool(units), 'exactly one of odd witness and regular witness')
        kept.append({'candidate_index':key[0], 'factor_index':key[1], 'rank':n,
                     'odd_witness': {'module_index':odd[0][0], 'internal_end_dimension':encode(odd[0][1])}
                                    if odd else None,
                     'unit_internal_end_indices':units})
    odd_keys = [(r['candidate_index'],r['factor_index']) for r in kept if r['odd_witness']]
    regular_keys = [(r['candidate_index'],r['factor_index']) for r in kept if r['unit_internal_end_indices']]
    need(len(kept)==21 and rejected==40, 'retained domain')
    need(len(odd_keys)==17, 'seventeen parity witnesses')
    need(regular_keys == [(0,0),(26,15),(42,0),(46,19)], 'four regular witnesses')
    return {'result':'PASS', 'scope':'independent exact arithmetic on all 61 inherited factors; no rerun of preceding exhaustive searches',
            'source_sha256':BINDINGS, 'inherited_factor_count':61,
            'independently_retained_factor_count':21, 'odd_profile_count':17,
            'regular_profile_count':4, 'factors':kept}


if __name__ == '__main__':
    result = run()
    (HERE/'r1768_profile_audit.json').write_text(json.dumps(result,indent=2)+'\n')
    print('PASS: all 61 refiltered; 21 profiles recomputed; 17 odd witnesses and four regular witnesses.')
