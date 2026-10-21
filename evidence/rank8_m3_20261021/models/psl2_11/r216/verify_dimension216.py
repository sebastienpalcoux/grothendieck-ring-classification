#!/usr/bin/env python3
"""Fresh source-bound arithmetic certificate for the dimension-216 theorem.
The categorical argument is proof.md. Default replay; --write regenerates.
"""
import argparse
import hashlib
import itertools
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[4]
TARGETS=['R8_3_810','R8_3_812','R8_3_2492','R8_3_2494','R8_3_2620','R8_3_2622']
def require(c,m):
    if not c: raise ValueError(m)
def fingerprint(v):
    return hashlib.sha256(json.dumps(v,separators=(',',':')).encode()).hexdigest()
def subdimensions(inv,other):
    return sorted({a+sum(d*d*c for (d,n),c in zip(other,counts))
                   for a in inv for counts in itertools.product(*(range(n+1) for d,n in other))})
def main():
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument('--write',action='store_true'); args=parser.parse_args()
    top=subdimensions([1,2],[(2,1),(3,2),(8,3)])
    require(not any(v in top for v in [108,72]),'top extension obstruction failed')
    A=subdimensions([1,3],[(3,1),(4,6)])
    B=subdimensions([1,3],[(3,1),(4,2),(8,1)])
    require(not any(v in A or v in B for v in [54,36]),'base extension obstruction failed')
    alternatives=[]
    for fixed8 in range(2):
        free4=3-2*fixed8
        alternatives.append({'dimension1':3,'dimension3':1,'dimension4':2*free4,'dimension8':fixed8})
    require(alternatives==[{'dimension1':3,'dimension3':1,'dimension4':6,'dimension8':0},
                           {'dimension1':3,'dimension3':1,'dimension4':2,'dimension8':1}], 'orbit types changed')
    stabilizers=[a for a in [1,2,4] if (16-a)%4==0]
    require(stabilizers==[4],'dimension-four stabilizer gate failed')
    require(36%20!=0,'adjoint obstruction changed')
    # Exact finite final group obstruction: every fixed-free involution on
    # either abelian group of order 9 is inversion, so V4 cannot act freely.
    c9=[a for a in range(9) if a%3 and a*a%9==1 and all(a*x%9!=x for x in range(1,9))]
    require(c9==[8],'unexpected fixed-free C9 involution')
    linear=[]
    vectors=list(itertools.product(range(3),repeat=2))
    for a,b,c,d in itertools.product(range(3),repeat=4):
        if (a*d-b*c)%3==0: continue
        def f(v): return ((a*v[0]+b*v[1])%3,(c*v[0]+d*v[1])%3)
        if all(f(f(v))==v for v in vectors) and all(f(v)!=v for v in vectors[1:]):
            linear.append([a,b,c,d])
    require(linear==[[2,0,0,2]],'unexpected fixed-free F3^2 involution')
    census=json.loads((ROOT/'evidence/rank8_m3_20261021/pipeline/census_m3.json').read_text())
    records=[]
    for name in TARGETS:
        row=next(r for r in census if r['id']==name); T=row['tensor']
        require(fingerprint(T)==row['tensor_sha256'],'source hash mismatch')
        inv=[i for i in range(8) if all(sum(v)==1 for v in T[i])]
        require(len(inv)==2,'wrong invertible count')
        other=[i for i in range(8) if i not in inv]
        found=None
        for dim2 in other:
            for dim3 in itertools.combinations([i for i in other if i!=dim2],2):
                d=[1 if i in inv else 2 if i==dim2 else 3 if i in dim3 else 8 for i in range(8)]
                if all(sum(T[i][j][k]*d[k] for k in range(8))==d[i]*d[j]
                       for i,j in itertools.product(range(8),repeat=2)):
                    found=d; break
            if found is not None: break
        require(found is not None and sum(v*v for v in found)==216,'wrong FP dimension type')
        records.append({'id':name,'tensor_sha256':row['tensor_sha256'],'source_line':row['source_line'],
                        'dimensions':found,'excluded':True})
    result={'theorem':'no complex fusion category of type (1,2;2,1;3,2;8,3)',
            'scope':'general complex fusion categories','recovery':'fresh exact reconstruction',
            'top_subcategory_dimensions':top,'base_types':alternatives,
            'base_A_subcategory_dimensions':A,'base_B_subcategory_dimensions':B,
            'dimension4_possible_stabilizers':stabilizers,
            'C9_fixed_free_involutions':c9,'F3_squared_fixed_free_involutions':linear,'records':records}
    path=HERE/'certificate.json'
    if args.write: path.write_text(json.dumps(result,indent=2)+'\n')
    else: require(json.loads(path.read_text())==result,'certificate does not replay')
    print(json.dumps({'excluded':TARGETS,'mode':'write' if args.write else 'compare'}))
if __name__=='__main__': main()
