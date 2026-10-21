#!/usr/bin/env python3
"""Fresh recovery certificate for the dimension-80 ring-rigidity theorem.
Default compares the saved certificate; --write explicitly regenerates it.
"""
import argparse
import hashlib
import itertools
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[4]
EXPECTED=['R8_3_275','R8_3_276','R8_3_344','R8_3_345']
def require(c,m):
    if not c: raise ValueError(m)
def fingerprint(v):
    return hashlib.sha256(json.dumps(v,separators=(',',':')).encode()).hexdigest()
def action(v):
    return ((v<<1)&15) ^ (15 if v&8 else 0)
def main():
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('--write',action='store_true'); args=p.parse_args()
    require(all(action(a^b)==action(a)^action(b) for a,b in itertools.product(range(16),repeat=2)),'action not linear')
    orbits=[]; remaining=set(range(1,16))
    while remaining:
        v=min(remaining); o=[]; w=v
        for _ in range(5): o.append(w); w=action(w)
        require(w==v and len(set(o))==5,'not a free order-five orbit')
        remaining-=set(o); orbits.append(sorted(o))
    require(len(orbits)==3,'wrong orbit count')
    R=[[[0]*8 for _ in range(8)] for _ in range(8)]
    for i,j in itertools.product(range(5),repeat=2): R[i][j][(i+j)%5]=1
    for i,j in itertools.product(range(5),range(3)): R[i][5+j][5+j]=R[5+j][i][5+j]=1
    for i,j in itertools.product(range(3),repeat=2):
        for a in range(5): R[5+i][5+j][a]=int(i==j)
        for k in range(3):
            counts=[sum(a^b==z for a in orbits[i] for b in orbits[j]) for z in orbits[k]]
            require(len(set(counts))==1,'orbit convolution not constant')
            R[5+i][5+j][5+k]=counts[0]
    dims=[1]*5+[5]*3
    require(max(x for A in R for row in A for x in row)==2,'unexpected orbit-ring multiplicity')
    require(all(sum(R[i][j][k]*dims[k] for k in range(8))==dims[i]*dims[j] for i,j in itertools.product(range(8),repeat=2)),'dimension equation failed')
    require(all(sum(R[i][j][k]*R[k][l][m] for k in range(8))==sum(R[j][l][k]*R[i][k][m] for k in range(8)) for i,j,l,m in itertools.product(range(8),repeat=4)),'orbit ring not associative')
    allowed_subcategory_dimensions=sorted({a+25*b for a in [1,5] for b in range(4)})
    require(16 not in allowed_subcategory_dimensions and 40 not in allowed_subcategory_dimensions,'extension gate failed')
    census=json.loads((ROOT/'evidence/rank8_m3_20261021/pipeline/census_m3.json').read_text())
    records=[]
    for row in census:
        T=row['tensor']; inv=[i for i in range(8) if all(sum(v)==1 for v in T[i])]
        if len(inv)!=5: continue
        d=[1 if i in inv else 5 for i in range(8)]
        if not all(sum(T[i][j][k]*d[k] for k in range(8))==d[i]*d[j] for i,j in itertools.product(range(8),repeat=2)): continue
        require(fingerprint(T)==row['tensor_sha256'],'source hash mismatch')
        require(max(x for A in T for v in A for x in v)==3,'source multiplicity changed')
        records.append({'id':row['id'],'tensor_sha256':row['tensor_sha256'],'source_line':row['source_line'],'dimensions':d,'invertible_indices':inv,'excluded':True})
    require(sorted(r['id'] for r in records)==sorted(EXPECTED),'dimension-80 scope changed')
    result={'theorem':'every category of type (1,5;5,3) has fixed-free (C2)^4 semidirect C5 representation ring',
            'scope':'general complex fusion categories','recovery':'fresh exact reconstruction',
            'extension_neutral_dimensions':[40,16],'possible_subcategory_dimensions':allowed_subcategory_dimensions,
            'nonzero_F2_4_orbits':orbits,'forced_ring_tensor':R,'forced_ring_maximum_multiplicity':2,'records':records}
    destination=HERE/'certificate.json'
    if args.write: destination.write_text(json.dumps(result,indent=2)+'\n')
    else: require(json.loads(destination.read_text())==result,'certificate does not replay')
    print(json.dumps({'excluded':[r['id'] for r in records],'forced_ring_maximum_multiplicity':2,'mode':'write' if args.write else 'compare'}))
if __name__=='__main__': main()
