#!/usr/bin/env python3
"""Exact field arithmetic for type-A level-plus-rank 10 dimensions."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json

# Basis 1,phi,t,phi*t with phi²=phi+1 and t²=phi+2.
Z=(F(0),)*4
ONE=(F(1),F(0),F(0),F(0))
PHI=(F(0),F(1),F(0),F(0))
T=(F(0),F(0),F(1),F(0))
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def neg(a):return tuple(-x for x in a)
def scale(a,b):return tuple(x*b for x in a)
def mul(a,b):
    z=Z
    for i,x in enumerate(a):
        for j,y in enumerate(b):
            p=(i%2)+(j%2);t=(i//2)+(j//2)
            pp=[0]*(p+2);pp[p]=x*y
            if t==2:
                pp=[2*v for v in pp]
                for k in range(len(pp)-1):pp[k+1]+=([0]*(p)+[x*y,0])[k]
                t=0
            for k in range(len(pp)-1,1,-1):
                pp[k-1]+=pp[k];pp[k-2]+=pp[k]
            out=[F(0)]*4;out[2*t]=pp[0];out[2*t+1]=pp[1]
            z=add(z,out)
    return z
def inv(a):
    cols=[mul(a,tuple(F(i==j) for i in range(4))) for j in range(4)]
    mat=[[cols[j][i] for j in range(4)]+[F(i==0)] for i in range(4)]
    for i in range(4):
        p=next(j for j in range(i,4) if mat[j][i]);mat[i],mat[p]=mat[p],mat[i]
        v=mat[i][i];mat[i]=[x/v for x in mat[i]]
        for j in range(4):
            if j!=i:
                v=mat[j][i];mat[j]=[x-v*y for x,y in zip(mat[j],mat[i])]
    return tuple(mat[i][4] for i in range(4))
def power(a,n):
    if n<0:return power(inv(a),-n)
    ans=ONE
    for _ in range(n):ans=mul(ans,a)
    return ans
assert mul(PHI,PHI)==add(PHI,ONE)
assert mul(T,T)==add(PHI,scale(ONE,2))
qn=[Z,ONE]
for n in range(2,11):qn.append(add(mul(T,qn[-1]),neg(qn[-2])))
assert qn[10]==Z and qn[9]==ONE
def compositions(n,k):
    if n==0:yield ();return
    for a in range(k+1):
        for tail in compositions(n-1,k-a):yield (a,)+tail
def dim(labels):
    n=len(labels)+1;ans=ONE
    for i in range(n):
        for j in range(i+1,n):ans=mul(ans,mul(qn[sum(labels[i:j])+j-i],inv(qn[j-i])))
    return ans
def encode(a):return [str(x) for x in a]
receipt={"basis":["1","phi","t","phi*t"],"relations":["phi²=phi+1","t²=phi+2"],"cases":{}}
for n in (3,4,5,6):
    rows=[(a,dim(a)) for a in compositions(n-1,10-n)]
    total=Z
    for a,d in rows:total=add(total,mul(d,d))
    assert all(all(x>=0 for x in d) for a,d in rows)
    zeros=[a for a,d in rows if sum(d[1:])==0]
    assert len(zeros)==n and all(dim(a)==ONE for a in zeros)
    expected={3:None,4:800,5:2000,6:1200}[n]
    if expected:assert total==scale(power(PHI,6),expected)
    receipt['cases'][f'SU({n})_{10-n}']={"rank":len(rows),"global_dimension_coefficients":encode(total),"only_zero_nonconstant_coordinates":len(zeros),"zero_labels":[list(a) for a in zeros],"all_nonconstant_coordinates_nonnegative":True}
Path(__file__).with_name('r1154_quantum_extensions_verified.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
