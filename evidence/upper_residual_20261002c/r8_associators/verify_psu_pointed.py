#!/usr/bin/env python3
"""Exact replay: ordinary PSU(2)_6 cannot have a negative pointed indicator.

This reuses the census's independently documented exact induction/indicator
engine. No LP solver is invoked: all three integer separating rays are fixed.
The source-bound part locates both conflicting subrings in R315 and R317.
"""
import argparse
import hashlib
import itertools
import json
import os
from pathlib import Path
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / 'supplements/rank8/data/rank8_tables.txt.gz').exists())
os.environ['RANK6_REFERENCE_GRAM'] = '1'
sys.path.insert(0, str(ROOT / 'supplements/rank7/software'))
import balanced_traces as b
sys.path.insert(0, str(ROOT / 'evidence/upper_residual_20261002b_recovery'))
from verify_recovery import read_source, validate_ring, fingerprint, require


def psu(pseudo=False):
    R = [[[0]*4 for _ in range(4)] for _ in range(4)]
    for i in range(4):
        R[0][i][i] = R[i][0][i] = 1
    R[1][1][0] = 1
    for i, j in ((1, 2), (2, 1)):
        R[i][j][3] = 1
    for i, j in ((1, 3), (3, 1)):
        R[i][j][2] = 1
    R[2][2] = R[3][3] = [int(not pseudo), int(pseudo), 1, 1]
    R[2][3] = R[3][2] = [int(pseudo), int(not pseudo), 1, 1]
    return R


RAYS = [
    [0,9,0,1,0,9,0,0,0,0,5,0,6,0,-1,0,-11,7,0,0,-2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6],
    [1,0,0,1,2,1,0,0,1,0,1,0,2,0,-2,1,-2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [0,0,9,9,0,1,0,0,3,2,0,0,6,0,-11,7,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6],
]
LOW_COLUMNS = [
    [[1,0,0,0], [1,0,0,2], [1,0,1,0], [1,0,1,0]],
    [[1,0,0,0], [1,0,1,1], [1,0,0,1], [1,0,1,0]],
    [[1,0,0,0], [1,0,2,0], [1,0,0,1], [1,0,0,1]],
]


def subring_maps(T, R):
    maps = []
    for tail in itertools.permutations(range(1, len(T)), 3):
        p = (0,) + tail
        if (all(T[p[i]][p[j]][p[k]] == R[i][j][k] for i,j,k in itertools.product(range(4), repeat=3))
                and all(T[p[i]][p[j]][k] == 0 for i,j in itertools.product(range(4), repeat=2)
                        for k in range(len(T)) if k not in p)):
            maps.append(list(p))
    return maps


def verify():
    start = time.monotonic()
    R = psu(); validate_ring(R)
    data = b.quadratic_data(R, gram_prune=True)
    require(data is not None, 'missing ordinary PSU quadratic data')
    require(data['q'] == 2 and data['conductor'] == 8 and data['primes'] == [2], 'wrong field/exponent prime support')
    require(list(map(len, data['columns'])) == [3, 2, 2], 'wrong complete low columns')
    require([[list(v) for v in cols] for cols in data['lows']] == LOW_COLUMNS, 'incomplete low matrices')
    require((-1, 1, 1) in b.indicator_choices(R), 'wrong candidate indicators')
    # All other negative-g choices are excluded by FRS odd multiplicity parity.
    require([ep for ep in b.indicator_choices(R) if ep[0] == -1] == [(-1,1,1)], 'missing negative-g indicator branch')
    branches = []
    for cols, ray in zip(data['lows'], RAYS):
        require(b.low_failure(cols, data['ch'].C, data['ds'], data['D'], data['K'], data['embedding'], data['ch'].du) is None, 'unexpected ordinary low obstruction')
        L = b.s.Matrix.hstack(*map(b.s.Matrix, cols))
        A, rhs, meta = b.system(R, data, L, (-1,1,1), 4)
        b.check_farkas(A, rhs, ray)
        require(meta['trace_types'] == 10 and meta['order_bound'] == 32 and meta['galois_rows'] == 2, 'wrong trace/balance system')
        products = [sum(A[i][j]*ray[i] for i in range(len(rhs))) for j in range(len(A[0]))]
        matrix_hash = hashlib.sha256(json.dumps({'A':A, 'b':rhs}, separators=(',',':')).encode()).hexdigest()
        branches.append({'low_columns':[list(v) for v in cols], 'rows':len(rhs), 'variables':len(A[0]),
                         'high_columns':meta['column_count'], 'trace_types':meta['trace_types'],
                         'galois_rows':meta['galois_rows'], 'integer_ray':ray,
                         'minimum_yA':min(products), 'bTy':sum(x*y for x,y in zip(rhs,ray)),
                         'system_sha256':matrix_hash})
    source = read_source(ROOT, 8)
    witnesses = []
    for key in ('R8_2_315', 'R8_2_317'):
        T = source[key]; validate_ring(T)
        ordinary = subring_maps(T, R)
        pseudo = subring_maps(T, psu(True))
        shared = [[p,q] for p in ordinary for q in pseudo if p[1] == q[1]]
        require(shared, 'ordinary/pseudo subrings with common invertible absent')
        witnesses.append({'id':key, 'source_sha256':fingerprint(T), 'shared_invertible_subrings':shared})
    return {'status':'PASS', 'claim':'ordinary_PSU2_6_PU_pointed_indicator_positive',
            'negative_indicator_tested':[-1,1,1], 'height':4,
            'scope_upgrade':'general_complex_via_Galois_invariant_H3_C2',
            'branches':branches, 'source_witnesses':witnesses,
            'python_optimized':not __debug__, 'seconds':round(time.monotonic()-start,3)}


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--output', type=Path); args = ap.parse_args()
    result = verify()
    if args.output:
        args.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))
