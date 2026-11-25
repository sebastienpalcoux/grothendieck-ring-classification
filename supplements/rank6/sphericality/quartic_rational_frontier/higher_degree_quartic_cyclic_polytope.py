#!/usr/bin/env python3
"""Rational Fourier dual certificates for the cyclic outer presentations."""
from pathlib import Path
from fractions import Fraction as F
from math import isqrt,gcd
from itertools import product
import json,sys
from higher_degree_quartic_polytope import floorf,ceilf,certificate

BASE=Path(__file__).parent
SCALE=10**12


def embeddings(row):
    a,J,D,b,c,m,I,A,u,v,w,B,C,N=row
    k=1 if a==D else 2
    dl=isqrt(D*SCALE*SCALE);du=dl+1
    yl=isqrt(m*(D*SCALE+b*dl)*SCALE)
    yu=isqrt(m*(D*SCALE+b*du)*SCALE)+1
    zl=isqrt(m*(D*SCALE-b*du)*SCALE)
    zu=isqrt(m*(D*SCALE-b*dl)*SCALE)+1
    vectors=((u*k,4,v,I,w,I),(-u*k,4,-w,I,v,I),
             (u*k,4,-v,I,-w,I),(-u*k,4,w,I,-v,I))
    lo=[];hi=[]
    for z in vectors:
        lower=upper=F(A*SCALE,4)
        for (num,den),(L,U) in zip(zip(z[::2],z[1::2]),((dl,du),(yl,yu),(zl,zu))):
            lower+=F(num*(L if num>=0 else U),den)
            upper+=F(num*(U if num>=0 else L),den)
        lo.append(floorf(lower));hi.append(ceilf(upper))
    j=min(range(4),key=lambda i:lo[i])
    assert all(hi[j]<lo[i] for i in range(4) if i!=j)
    lo=[lo[(i+j)%4] for i in range(4)];hi=[hi[(i+j)%4] for i in range(4)]
    assert lo[0]>0 and hi[0]<SCALE
    return lo,hi


def constraints(row):
    lo,hi=embeddings(row)
    bl=[F(SCALE,SCALE+x) for x in hi];bu=[F(SCALE,SCALE+x) for x in lo]
    rows=[];rhs=[]
    def add(cc,bound):
        rows.append([floorf(x*SCALE) for x in cc]);rhs.append(ceilf(bound*SCALE))
    def add_pq(wp,wq,bound):
        cc=[]
        for i in range(4):
            z=wq[i]-wp[i];cc.append(wp[i]+z*(bl[i] if z>=0 else bu[i]))
        add(cc,bound)
    zero=[F(0)]*4
    for j in range(1,4):
        z=zero.copy();z[0]=F(1);z[j]=F(-1)
        add_pq(zero,z,F(0));add_pq(z,zero,F(0))
    add_pq([F(1)]*4,zero,F(1,2));add_pq([F(-1)]*4,zero,F(-1,4))
    for j in range(1,4):
        cc=[]
        for i in range(4):
            lower=F(lo[i]-hi[(i+j)%4],SCALE)
            cc.append(lower*(bl[i] if lower>=0 else bu[i]))
        add(cc,F(0))
    a,J=row[:2]
    dirs=[(x,y) for x in range(-4,5) for y in range(-4,5) if gcd(x,y)==1]
    def upper_sqrt(n,d):return F(isqrt(n*d*SCALE*SCALE)+1,d*SCALE)
    C=(1,-1,1,-1)
    for ordinary in (False,True):
        bound=upper_sqrt(gcd(a,2 if ordinary else 4),a)
        for sign in (-1,1):
            z=[F(sign*x) for x in C]
            add_pq(z if ordinary else zero,zero if ordinary else z,bound)
    for x,y in dirs:
        add_pq([F(x*z) for z in C],[F(y*z) for z in C],upper_sqrt(2*x*x+4*y*y,a))
    root=F(isqrt(a*SCALE*SCALE),SCALE)
    for sign in (-1,1):
        for rn in range(-32,33):
            r=F(rn,64)
            add_pq([2*a*r*x for x in C],[sign*root*x for x in C],2+a*r*r)
    R=(1,0,-1,0);S=(0,1,0,-1)
    def coeff(x,y):return [x*R[i]+y*S[i] for i in range(4)]
    for x,y in dirs:
        for ordinary in (False,True):
            z=coeff(F(x),F(y))
            bound=upper_sqrt(gcd(J,2 if ordinary else 4)*(x*x+y*y),J)
            add_pq(z if ordinary else zero,zero if ordinary else z,bound)
    for x,y,z,w in product((-1,0,1),repeat=4):
        if not(x or y or z or w):continue
        add_pq(coeff(F(x),F(y)),coeff(F(z),F(w)),upper_sqrt(2*(x*x+y*y)+4*(z*z+w*w),J))
    roots=F(isqrt(J*SCALE*SCALE),SCALE)
    unitdirs={(F(1),F(0)),(F(-1),F(0)),(F(0),F(1)),(F(0),F(-1))}
    for signs in product((-1,1),repeat=2):
        for x,y in ((3,4),(4,3)):
            unitdirs.add((F(signs[0]*x,5),F(signs[1]*y,5)))
    for x,y in sorted(unitdirs):
        for rn,sn in product(range(-3,4),repeat=2):
            r,s=F(rn,8),F(sn,8)
            add_pq(coeff(2*J*r,2*J*s),coeff(roots*x,roots*y),2+J*(r*r+s*s))
    return rows,rhs


def run():
    import numpy as np
    from scipy.optimize import linprog
    data=[list(map(int,l.split())) for l in (BASE/'higher_degree_quartic_cyclic_candidates.txt').read_text().splitlines()]
    records=[];survivors=[]
    for ci,row in enumerate(data):
        rows,rhs=constraints(row);A=np.asarray(rows,dtype=float)/SCALE;b=np.asarray(rhs,dtype=float)/SCALE
        res=linprog([0]*4+[1],A_ub=np.column_stack([A,-np.ones(len(A))]),b_ub=b,A_eq=[[1]*4+[0]],b_eq=[1],bounds=[(0,None)]*5,method='highs')
        assert res.success,res.message
        rejected=False
        if res.fun>1e-10:
            for precision in (10**6,10**9,10**12):
                weights=[(j,int(round(-x*precision))) for j,x in enumerate(res.ineqlin.marginals) if x<-1e-14]
                gap=certificate(rows,rhs,weights)
                if gap>0:
                    records.append(dict(index=ci,weights=weights,gap=str(gap)));rejected=True;break
        if not rejected:survivors.append(dict(index=ci,ratio=row,phase1=float(res.fun),point=list(res.x[:4])))
        if ci%25==0:print(ci,'excluded',len(records),'remaining',len(survivors),flush=True)
    result=dict(scale=SCALE,constraint_version=1,certificates=records,survivors=survivors)
    (BASE/'higher_degree_quartic_cyclic_polytope.json').write_text(json.dumps(result,indent=2)+'\n')
    print('FINAL excluded',len(records),'remaining',len(survivors),flush=True)


def verify():
    data=[list(map(int,l.split())) for l in (BASE/'higher_degree_quartic_cyclic_candidates.txt').read_text().splitlines()]
    result=json.loads((BASE/'higher_degree_quartic_cyclic_polytope.json').read_text())
    assert result['scale']==SCALE and result['constraint_version']==1
    assert len(data)==281 and len(result['certificates'])==281
    assert result['survivors']==[]
    ids=set()
    for record in result['certificates']:
        i=record['index'];assert type(i) is int and 0<=i<len(data) and i not in ids;ids.add(i)
        rows,rhs=constraints(data[i]);used=set()
        for pair in record['weights']:
            assert type(pair) is list and len(pair)==2
            j,w=pair;assert type(j) is int and type(w) is int and 0<=j<len(rows) and w>=0 and j not in used;used.add(j)
        gap=certificate(rows,rhs,record['weights']);assert gap>0 and str(gap)==record['gap']
    residual=set(range(len(data)))-ids
    assert len(ids)==281 and not residual
    print('Exact cyclic dual certificates',len(ids),'; survivors',len(residual))


if __name__=='__main__':verify() if sys.argv[-1]=='--verify' else run()
