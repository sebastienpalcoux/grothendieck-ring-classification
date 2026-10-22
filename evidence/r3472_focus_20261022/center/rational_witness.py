"""Exact rational and integer witnesses for the published R3472 center relaxation.

Default replay reconstructs the published system and checks every equation
using rational arithmetic. Discovery may use SciPy and python-flint; their
numerical result is never accepted without the same exact checks.
"""
from pathlib import Path
from fractions import Fraction
import argparse
import gzip
import hashlib
import json
import pickle
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OLD = ROOT / "evidence/rank8_frontier_20261021/quadratic"
sys.path.insert(0, str(OLD))
from strong_integer_3472 import domain, sources
from features import require
import streaming as st


def check(S, values, box_receipt):
    require(len(values) == len(S.columns), "witness length differs")
    require(all(isinstance(x, Fraction) for x in values), "nonrational witness entry")
    require(all(lo <= x <= hi for x, lo, hi in zip(values, box_receipt['lower_bounds'], box_receipt['upper_bounds'])),
            "propagated box bound fails")
    sums = [Fraction(0)] * len(S.rhs)
    for x, col in zip(values, S.columns):
        if x:
            for i, a in enumerate(col):
                if a:
                    sums[i] += x*a
    require(sums == list(S.rhs), "exact equation fails")
    return {
        "equations_checked": len(S.rhs),
        "variables_checked": len(values),
        "nonzero_entries": sum(x != 0 for x in values),
        "nonintegral_entries": sum(x.denominator != 1 for x in values),
        "largest_denominator": max(x.denominator for x in values),
    }


def propose(S, box_receipt, destination):
    import numpy as np
    from scipy.optimize import linprog
    from scipy.sparse import csc_matrix
    m, n = len(S.rhs), len(S.columns)
    scales = [max(1, abs(b)) for b in S.rhs]
    for col in S.columns:
        for i, a in enumerate(col):
            scales[i] = max(scales[i], abs(a))
    data, indices, offsets = [], [], [0]
    for col in S.columns:
        for i, a in enumerate(col):
            if a:
                data.append(float(a/scales[i])); indices.append(i)
        offsets.append(len(data))
    A = csc_matrix((np.asarray(data), np.asarray(indices, dtype=np.int32), np.asarray(offsets, dtype=np.int32)), shape=(m,n))
    target = np.asarray([float(b/t) for b,t in zip(S.rhs,scales)])
    limits = list(zip(box_receipt['lower_bounds'],box_receipt['upper_bounds']))
    answer = linprog(np.zeros(n), A_eq=A, b_eq=target, bounds=limits, method="highs-ds", options={"time_limit": 180})
    require(answer.success, "numerical proposal inconclusive: "+str(answer.message))
    np.save('/tmp/r3472_center_numeric.npy', answer.x)
    print('numerical proposal support',sum(answer.x > 1e-9),flush=True)
    for max_denominator in (100,1000,10000,1000000,100000000):
        values = [Fraction(float(x)).limit_denominator(max_denominator) for x in answer.x]
        try:
            receipt = check(S,values,box_receipt)
            print('direct rational reconstruction',max_denominator,receipt,flush=True)
            return values,receipt
        except RuntimeError:
            pass
    # Recover the exact basic feasible solution on the proposed support.
    # Entries at their exact box endpoints are moved to the right side.
    from flint import fmpz_mat
    free = []
    values = [Fraction(0)]*n
    for j,(x,(lo,hi)) in enumerate(zip(answer.x,limits)):
        if abs(x-lo) < 1e-8:
            values[j] = Fraction(lo)
        elif abs(x-hi) < 1e-8:
            values[j] = Fraction(hi)
        else:
            free.append(j)
    rhs = list(S.rhs)
    for x,col in zip(values,S.columns):
        if x:
            for i,a in enumerate(col):
                rhs[i] -= a*x
    require(all(Fraction(x).denominator == 1 for x in rhs),"endpoint residual not integral")
    rows = [[int(S.columns[j][i]) for j in free]+[int(rhs[i])] for i in range(m)]
    print('exact rational elimination',len(rows),len(free),flush=True)
    echelon, denominator, rank = fmpz_mat(rows).rref()
    require(rank == len(free),"proposed free support is dependent or inconsistent")
    for i,j in enumerate(free):
        require(int(echelon[i,i]) == int(denominator),"unexpected pivot position")
        values[j] = Fraction(int(echelon[i,len(free)]),int(denominator))
    receipt = check(S,values,box_receipt)
    print('exact reconstruction passed',receipt,flush=True)
    return values,receipt


def check_integer_extension(S, box_receipt, rational_record, rational_values):
    record = json.loads((HERE/'integer_witness.json').read_text())
    for key in ('source_sha256','tensor_sha256','system_metadata_sha256','published_bounds_sha256'):
        require(record[key] == rational_record[key], 'integer witness source differs: '+key)
    require(record['derivation'] == {
        'rational_witness_file':'rational_witness.json',
        'removed_column':13024,'removed_value':[49,50],
        'added_column':12917,'added_value':98,'column_ratio':100,
    }, 'integer replacement receipt differs')
    small, large = 12917, 13024
    require(S.column_labels[small][0] == S.column_labels[large][0] == 'high_orbit',
            'replacement is not between high columns')
    require(S.column_labels[small][2] == ((0,1,1,1,1,1,1,1),), 'small restriction differs')
    require(S.column_labels[large][2] == ((0,10,10,10,10,10,10,10),), 'large restriction differs')
    require(all(a == 100*b for a,b in zip(S.columns[large],S.columns[small])),
            'claimed complete-column scaling fails')
    require(rational_values[small] == 0 and rational_values[large] == Fraction(49,50),
            'replacement input differs')
    expected = rational_values.copy()
    expected[small], expected[large] = Fraction(98), Fraction(0)
    values = [Fraction(0)]*len(S.columns)
    seen = set()
    for j,num,den in record['entries']:
        require(j not in seen and 0 <= j < len(values) and den == 1,
                'invalid integer witness entry')
        seen.add(j); values[j] = Fraction(num,den)
    require(values == expected, 'integer witness is not the exact replacement')
    bindings = [[j,st.encode(S.column_labels[j])] for j,x in enumerate(values)
                if x and S.column_labels[j][0] in ('low','high_orbit')]
    require(record['restriction_bindings'] == bindings, 'integer restriction bindings differ')
    require(check(S,values,box_receipt) == record['verification'],
            'integer verification receipt differs')
    require(all(x.denominator == 1 for x in values), 'integer witness is nonintegral')
    return record['verification']


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--discover',action='store_true')
    parser.add_argument('--checkpoint',help='Discovery-only local pickle; never used in certificate replay.')
    args=parser.parse_args()
    require(not args.checkpoint or args.discover,"checkpoint is discovery-only")
    if args.checkpoint:
        with gzip.open(args.checkpoint,'rb') as f: source,support,S=pickle.load(f)
    else:
        source,support,S=domain()
    previous=json.loads((OLD/'strong_integer_3472_results.json').read_text())
    require(source['tensor_sha256']==previous['tensor_sha256'],"source tensor differs")
    require(st.encode(S.metadata)==previous['metadata'],"published full system differs")
    require(previous['source_sha256']==sources(),"published generator inventory differs")
    box_receipt=previous['box']
    # Reuse the exact published bounds only after replaying their derivation.
    import bounds
    bounds.verify(S,box_receipt)
    path=HERE/'rational_witness.json'
    if args.discover:
        values,receipt=propose(S,box_receipt,path)
        record={
            'kind':'exact_nonnegative_rational_witness_for_published_R3472_center_relaxation',
            'tensor_sha256':source['tensor_sha256'],
            'source_sha256':sources(),
            'system_metadata_sha256':st.digest(S.metadata),
            'published_bounds_sha256':st.digest(box_receipt),
            'entries':[[j,x.numerator,x.denominator]for j,x in enumerate(values)if x],
            'verification':receipt,
            'scope':'A rational point in the published Gram/S/cubic/Galois/FP/unit-product necessary relaxation. It is not an integer point or a categorification.',
            'classification_status':'unresolved',
        }
        path.write_text(json.dumps(record,indent=2)+'\n')
    else:
        record=json.loads(path.read_text())
        require(record['source_sha256']==sources(),"witness source inventory differs")
        require(record['tensor_sha256']==source['tensor_sha256'],"witness tensor differs")
        require(record['system_metadata_sha256']==st.digest(S.metadata),"witness matrix differs")
        require(record['published_bounds_sha256']==st.digest(box_receipt),"witness box differs")
        values=[Fraction(0)]*len(S.columns)
        seen=set()
        for j,num,den in record['entries']:
            require(j not in seen and 0<=j<len(values) and den>0,"invalid witness support")
            seen.add(j);values[j]=Fraction(num,den)
        require(check(S,values,box_receipt)==record['verification'],"verification receipt differs")
        receipt = check_integer_extension(S,box_receipt,record,values)
        print('PASS exact integer center witness',receipt,flush=True)
    print('PASS exact rational center witness; categorification remains unresolved',flush=True)


if __name__=='__main__':
    main()
