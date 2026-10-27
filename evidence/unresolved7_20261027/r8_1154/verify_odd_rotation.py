#!/usr/bin/env python3
"""Replay all exact third-rotation certificates without numerical optimization."""
from fractions import Fraction as Q
from pathlib import Path
import hashlib, itertools, json, time
from build_odd_rotation_system import build

HERE=Path(__file__).resolve().parent
def need(p,msg):
    if not p: raise ValueError(msg)
def digest(x):
    return hashlib.sha256(json.dumps(x,separators=(',',':')).encode()).hexdigest()
def rhs_for(base,constants,domain,pattern,values):
    return base+domain['completions'][pattern]+[int(d*values[k//2]-l) for k,(d,l) in enumerate(constants)]
def ray_pass(A,b,ray):
    return (len(ray)==len(b) and all(type(v) is int for v in ray)
      and sum(v*w for v,w in zip(ray,b))<0
      and all(sum(row[j]*v for row,v in zip(A,ray))>=0 for j in range(len(A[0]))))

start=time.monotonic();summary=[]
for objects,name,choices in [
    ((4,5),'odd_rotation_probe_h3.json',list(itertools.product((-1,2),repeat=2))),
    ((1,4,5,6),'odd_rotation_discrete_h3.json',[(a,2,2,b) for a,b in itertools.product((Q(-1),Q(1,2),Q(2)),repeat=2)])]:
    A,base,constants,domain,meta=build(objects)
    need(digest(meta['source_tensor'])=='c399505be76a64c8aba65feaf2cd55125dc7132f5894b74e58b64473d1387e25','Source binding')
    rec=json.loads((HERE/name).read_text());seen=set();excluded=feasible=0
    receipts=[]
    for r in rec['results']:
        pattern=r['pattern']; values=tuple(map(Q,r['projected_third_indicators']))
        key=(pattern,values);need(key not in seen,'Duplicate case');seen.add(key)
        b=rhs_for(base,constants,domain,pattern,values)
        if 'exact_primal' in r:
            p={int(j):Q(v) for j,v in r['exact_primal']}
            need(len(p)==len(r['exact_primal']) and all(0<=j<len(A[0]) and v>=0 for j,v in p.items()),'Primal domain')
            need(all(sum(row[j]*v for j,v in p.items())==bb for row,bb in zip(A,b)),'Primal equations')
            need(all(v==2 for v in values),'Unexpected feasible branch')
            feasible+=1
        else:
            need(ray_pass(A,b,r['exact_ray']),'Exact Farkas certificate')
            need(not ray_pass(A,b,[0]*len(b)),'Zero-ray negative control')
            excluded+=1
        receipts.append({'pattern':pattern,'values':list(map(str,values)),'matrix_rhs_sha256':digest([A,b])})
    need(seen=={(p,tuple(map(Q,vs))) for p in (6971,8766,8772) for vs in choices},'Complete discrete branch coverage')
    need(feasible==3,'Exactly one surviving value choice per center pattern')
    summary.append({'objects':list(objects),'excluded_discrete_branches':excluded,'retained_patterns':3,'systems':receipts})

out={'status':'PASS','conclusion':'All six noninvertible source simples necessarily have third indicator 2; all three center patterns remain unresolved.','seconds':time.monotonic()-start,'stages':summary}
(HERE/'odd_rotation_verification.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS: 33 discrete branches excluded; 3 center patterns remain; all six noninvertible third rotations must be identity.')
