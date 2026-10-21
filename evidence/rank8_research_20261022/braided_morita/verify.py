#!/usr/bin/env python3
"""Exact source-ring hypotheses for the minimal-image Morita criterion."""
import argparse
import hashlib
import json
from pathlib import Path
import sympy as s

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
IDS = [f'R8_3_{i}' for i in (65,928,941,982,1154,1768,1795,3472)]

def compute(record):
    R = record['tensor']; n = len(R)
    tensor_hash = hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest()
    assert tensor_hash == record['tensor_sha256']
    dual = []
    for i in range(n):
        ds = [j for j in range(n) if R[i][j][0]]
        assert len(ds) == 1 and R[i][ds[0]][0] == 1
        dual.append(ds[0])
    invertibles = [i for i in range(n) if sum(R[i][dual[i]]) == 1]
    subrings = []
    for mask in range(1 << (n-1)):
        subset = [0] + [i for i in range(1,n) if mask & (1 << (i-1))]
        allowed = set(subset)
        if not all(dual[i] in allowed for i in subset): continue
        if all(not R[i][j][k] or k in allowed
               for i in subset for j in subset for k in range(n)):
            subrings.append(subset)
    assert all(set(B) <= set(invertibles) for B in subrings if len(B)<n)
    matrices = [s.Matrix(R[i]).T for i in range(n)]
    casimir = sum((matrices[i]*matrices[dual[i]] for i in range(n)),s.zeros(n))
    polynomial = casimir.charpoly().as_poly()
    # Its largest real eigenvalue is FPdim(R): the positive FP character
    # is a common eigenvector of the transposes, with that eigenvalue.
    intervals = polynomial.intervals(eps=s.Rational(1,100))
    interval, multiplicity = max(intervals, key=lambda item:item[0][1])
    lo, hi = interval
    factors = s.factor_list(polynomial)[1]
    containing = [f for f,m in factors if f.count_roots(lo,hi)]
    assert len(containing)==1 and containing[0].degree()>1
    assert lo != hi
    return {'id':record['id'],'tensor_sha256':tensor_hash,
            'invertible_indices':invertibles,'all_based_subrings':subrings,
            'all_proper_subrings_pointed':True,
            'casimir_characteristic_polynomial':str(polynomial.as_expr()),
            'global_fp_dimension_minimal_polynomial':str(containing[0].as_expr()),
            'global_fp_dimension_isolating_interval':[str(lo),str(hi)],
            'global_fp_dimension_irrational':True,
            'consequence':'A categorification is Morita equivalent to a braided category only if it itself admits a braiding.'}

if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('--write',action='store_true'); args=parser.parse_args()
    source={r['id']:r for r in json.loads((ROOT/'evidence/rank8_m3_20261021/pipeline/census_m3.json').read_text())}
    result=[compute(source[rid]) for rid in IDS]
    path=HERE/'verification.json'
    if args.write: path.write_text(json.dumps(result,indent=2)+'\n')
    else: assert result==json.loads(path.read_text())
    print('PASS: complete based-subring and irrational-dimension audit for all eight rank-eight rings')
