#!/usr/bin/env python3
"""Fresh exact split-module certificate for the two dimension-280 tensors.
Default replay; --write explicitly regenerates certificate.json.
"""
import argparse
import hashlib
import itertools
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[4]
MAPS={'R8_3_1051':[0,3,4,5,6,1,2,7],'R8_3_2415':[0,1,2,3,4,5,7,6]}
SHAS={'R8_3_1051':'cd605d3e939b87963cd5d90ef3d9c1d6b104dcfbbbd2fbc1cfc098bb50220395',
      'R8_3_2415':'9ea87e95a05dbe117c8997cd19115057451d30161631c7ee079814bfd291e221'}
def require(c,m):
    if not c: raise ValueError(m)
def fingerprint(v):
    return hashlib.sha256(json.dumps(v,separators=(',',':')).encode()).hexdigest()
def multiply(A,B):
    n=len(A)
    return [[sum(A[i][k]*B[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
def polynomial(A):
    n=len(A); V=[[int(i==j) for j in range(n)] for i in range(n)]
    for root in [0,5,1,-1,-2]:
        V=multiply(V,[[A[i][j]-root*int(i==j) for j in range(n)] for i in range(n)])
    return V
def main():
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('--write',action='store_true'); args=p.parse_args()
    census=json.loads((ROOT/'evidence/rank8_m3_20261021/pipeline/census_m3.json').read_text())
    records=[]
    for name,m in MAPS.items():
        row=next(r for r in census if r['id']==name); source=row['tensor']
        require(fingerprint(source)==row['tensor_sha256']==SHAS[name],'source hash mismatch')
        T=[[[source[m[i]][m[j]][m[k]] for k in range(8)] for j in range(8)] for i in range(8)]
        dims=[1,1,5,5,6,8,8,8]
        require(all(sum(T[i][j][k]*dims[k] for k in range(8))==dims[i]*dims[j] for i,j in itertools.product(range(8),repeat=2)),'wrong dimensions')
        require(all(T[1][i][j]==int(j==[1,0,3,2,4,5,6,7][i]) for i,j in itertools.product(range(8),repeat=2)),'wrong invertible action')
        require(T[2][2][0]==1,'chosen dimension-five simple is not self-dual')
        block=[[T[2][i][j] for j in range(4,8)] for i in range(4,8)]
        require(block==[[1,1,1,1],[1,0,2,1],[1,2,0,1],[1,1,1,1]],'wrong split block')
        require(polynomial(T[2])==[[0]*8 for _ in range(8)],'source based-ring polynomial identity failed')
        records.append({'id':name,'tensor_sha256':SHAS[name],'source_line':row['source_line'],
                        'normalized_to_source_basis':m,'dimensions':dims,'fixed_object_block':block,'excluded':True})
    witnesses=[]
    for a,c,d,e in itertools.product([-1,1],repeat=4):
        for b in [-2,0,2]:
            S=[[a,1,1,1],[1,0,b,c],[1,b,0,d],[1,c,d,e]]
            residual=polynomial(S)
            nonzero=[(i,j,residual[i][j]) for i,j in itertools.product(range(4),repeat=2) if residual[i][j]]
            require(nonzero,'split difference matrix escaped polynomial obstruction')
            witnesses.append({'parameters':[a,b,c,d,e],'first_nonzero_polynomial_entry':list(nonzero[0])})
    require(len(witnesses)==48,'incomplete difference-matrix enumeration')
    result={'theorem':'rank-one pointed-module splitting obstructs the two dimension-280 tensors',
            'scope':'general complex fusion categories','recovery':'fresh exact reconstruction',
            'annihilating_polynomial_roots':[0,5,1,-1,-2],
            'candidate_difference_matrix_count':48,'rejected_difference_matrices':witnesses,'records':records}
    path=HERE/'certificate.json'
    if args.write: path.write_text(json.dumps(result,indent=2)+'\n')
    else: require(json.loads(path.read_text())==result,'certificate does not replay')
    print(json.dumps({'excluded':list(MAPS),'difference_matrices_rejected':48,'mode':'write' if args.write else 'compare'}))
if __name__=='__main__': main()
