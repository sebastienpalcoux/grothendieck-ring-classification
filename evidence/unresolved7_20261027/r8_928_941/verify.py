#!/usr/bin/env python3
"""Short exact source/rank/Galois checks; no categorification decision."""
from collections import Counter
from fractions import Fraction as Q
from itertools import product
from math import isqrt
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / 'evidence/rank8_frontier_20261021'
HERE = Path(__file__).resolve().parent
ONE = (Q(1), Q(0), Q(0), Q(0))
ZERO = (Q(0),) * 4
D = tuple(map(Q, (144, 96, 80, 56)))

def need(ok, msg):
    if not ok:
        raise ValueError(msg)

def add(x, y):
    return tuple(a+b for a,b in zip(x,y))

def scale(n, x):
    return tuple(n*a for a in x)

def mul(x, y):
    z = [Q(0)]*4
    for i,a in enumerate(x):
        for j,b in enumerate(y):
            k=i&j
            z[i^j] += a*b*(2 if k&1 else 1)*(3 if k&2 else 1)
    return tuple(z)

def sigma(x, s, t):
    return (x[0], s*x[1], t*x[2], s*t*x[3])

def inv(x):
    y=ONE
    for s,t in [(-1,1),(1,-1),(-1,-1)]:
        y=mul(y,sigma(x,s,t))
    norm=mul(x,y)
    need(norm[1:]==ZERO[1:] and norm[0]!=0, 'field norm')
    return scale(1/norm[0],y)

def sign(x):
    if x==ZERO:
        return 0
    den=10**20
    lo=hi=x[0]
    for n,v in zip((2,3,6),x[1:]):
        k=isqrt(n*den*den)
        a,b=Q(k,den),Q(k+1,den)
        lo+=v*(a if v>=0 else b)
        hi+=v*(b if v>=0 else a)
    need(lo>0 or hi<0, 'exact sign interval separates zero')
    return 1 if lo>0 else -1

def dot(v, ds):
    z=ZERO
    for n,d in zip(v,ds):
        z=add(z,scale(n,d))
    return z

def enc(x):
    return [str(a) for a in x]

def closed_subrings(N, dual):
    ans=[]
    for bits in product((0,1),repeat=7):
        S={0}|{i+1 for i,b in enumerate(bits) if b}
        if any(dual[i] not in S for i in S):
            continue
        if any(N[i][j][k] and k not in S for i in S for j in S for k in range(8)):
            continue
        ans.append(sorted(S))
    return sorted(ans,key=lambda x:(len(x),x))

def main():
    paths=[BASE/'quartic_integer_center/source.json',
           BASE/'quartic_integer_center/gram_cubic.json',
           BASE/'review/r941_fusion_traces.json',
           ROOT/'evidence/unresolved_retry_20261024/proofs/unresolved11_20261024/rank8_quartic_pair/R928_MORITA_RIGIDITY.md']
    source=json.loads(paths[0].read_text())
    pats=json.loads(paths[1].read_text())['patterns']
    fermion=json.loads(paths[2].read_text())
    out={'status':'PASS', 'date':'2026-10-27', 'checks':[], 'dependencies_sha256':{
        str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}}
    records={r['id']:r for r in source['records']}
    for cid,g in [('R8_3_928',7),('R8_3_941',3)]:
        r=records[cid]; N=r['tensor']
        h=hashlib.sha256(json.dumps(N,separators=(',',':')).encode()).hexdigest()
        need(h==r['tensor_sha256'], cid+' tensor SHA')
        dual=[next(j for j in range(8) if N[i][j][0]) for i in range(8)]
        ds=[tuple(map(Q,x)) for x in r['full_characters'][0]]
        for i,j in product(range(8),repeat=2):
            need(mul(ds[i],ds[j])==dot(N[i][j],ds),cid+' dimension character')
        need(all(sign(d)>0 for d in ds),cid+' positivity')
        need(dot([1]*8,[mul(d,d) for d in ds])==D,cid+' global dimension')
        subs=closed_subrings(N,dual)
        need(subs==[[0],[0,g],list(range(8))],cid+' fusion-subring lattice')
        need(any(N[i][j]!=N[j][i] for i,j in product(range(8),repeat=2)),cid+' noncommutative')
        need(all(all(ds[i][j]>0 for j in (1,2,3)) for i in range(8) if i not in (0,g)),cid+' irrational support')
        low=[dot(v,ds) for v in r['low_columns']]
        need(sum((v[0] for v in r['low_columns'][:4]))==4,cid+' scalar low objects')
        need(dot([1]*4,low[:4])==scale(Q(1,2),D),cid+' neutral canonical algebra dimension')
        for d,e in zip(low[1:4],[(2,1,1,1),(2,2,1,1),(3,2,2,1)]):
            need(d==mul(tuple(map(Q,e)),tuple(map(Q,e))),cid+' distinguished square dimensions')
        out['checks'].append({'id':cid,'tensor_sha256':h,'dual':dual,'fusion_subrings':subs,
                              'distinguished_dimensions':list(map(enc,low)),
                              'neutral_algebra_dimension':enc(scale(Q(1,2),D))})
    r=records['R8_3_928']; ds=[tuple(map(Q,x)) for x in r['full_characters'][0]]
    cols=r['low_columns']+[[0]+v for v in r['canonical_high_vectors']]
    dims=[dot(v,ds) for v in cols]
    out['R928_patterns']=[]
    for ix,rank in [(40,46),(49,40),(186,40),(191,34)]:
        multiplicities=[1]*5+pats[ix]
        need(sum(multiplicities)==rank,'semion center rank')
        hist=Counter()
        for d,n in zip(dims,multiplicities):
            hist[d]+=n
        hist=+hist
        need(all(n%2==0 for n in hist.values()),'semion dimension orbit pairing')
        galois=[]
        for s,t in [(-1,1),(1,-1),(-1,-1)]:
            ratio=mul(D,inv(sigma(D,s,t)))
            need(sign(ratio)>0,'Galois dimension ratio positive')
            transformed=Counter()
            for d,n in hist.items():
                v=mul(ratio,sigma(d,s,t)); v=scale(sign(v),v)
                transformed[v]+=n
            need(transformed==hist,'Galois dimension multiplicity closure')
            galois.append({'sigma':[s,t],'ratio':enc(ratio),'pass':True})
        out['R928_patterns'].append({'index':ix,'center_rank':rank,'simple_factor_rank':rank//2,
                                     'dimension_galois_checks':galois})
    retained=fermion['paired_surviving_allocations']
    need(retained==[8,19,21,31,34,43,45,56,60,72,73,77,79,85],'complete retained allocation IDs')
    cases={r['allocation_index']:r for r in fermion['cases']}
    out['R941_allocations']=[]
    for ix in retained:
        r=cases[ix]
        need(r['positive_charge_count']==22,'fermion centralizer rank')
        rank=r['positive_charge_count']+r['negative_charge_count']
        need(rank in (34,37,40,43),'retained full center rank')
        need(rank not in (33,44),'split-centralizer rank obstruction')
        need(rank==5+sum(pats[r['pattern_index']]),'center rank agrees with independent full Gram pattern')
        out['R941_allocations'].append({'allocation':ix,'pattern':r['pattern_index'],
                                      'centralizer_rank':22,'center_rank':rank})
    out['scope']='Exact input and necessary-domain checks only. Theoretical center simplicity and etale-algebra results are proved in REPORT.md. Neither ring is excluded or modelized.'
    (HERE/'verification.json').write_text(json.dumps(out,indent=2)+'\n')
    print('PASS: two source tensors, four semion patterns, fourteen fermion allocations; no categorification decision')

if __name__=='__main__':
    main()
