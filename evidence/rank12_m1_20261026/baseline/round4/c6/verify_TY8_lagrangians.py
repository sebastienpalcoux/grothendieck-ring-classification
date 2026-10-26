#!/usr/bin/env python3
"""Exact TY(|A|=4) center Lagrangian count from GNN §4.3 S,T.
Standard library; Q(zeta16)=Q[t]/(t^8+1). No float, assert, or optimizer.
"""
from itertools import combinations, product
from collections import Counter
import json
from pathlib import Path
Z=(0,)*8

def root(k):
    k%=16
    return tuple((1 if k<8 else -1) if j==k%8 else 0 for j in range(8))
ONE=root(0)
def add(a,b): return tuple(x+y for x,y in zip(a,b))
def scale(a,k): return tuple(k*x for x in a)
def mul(a,b):
    out=[0]*8
    for i,x in enumerate(a):
        for j,y in enumerate(b):
            q,r=divmod(i+j,8)
            out[r]+=(-1 if q else 1)*x*y
    return tuple(out)
def conj(a):
    out=Z
    for i,x in enumerate(a): out=add(out,scale(root(-i),x))
    return out
def sumc(vals):
    out=Z
    for v in vals: out=add(out,v)
    return out

def data(kind,sgn):
    A=list(range(4))
    if kind=='C4_i' or kind=='C4_-i':
        s=1 if kind=='C4_i' else 3
        plus=lambda a,b:(a+b)%4
        chi=lambda a,b:root(4*s*a*b)
        rhos=[tuple(root(2*k*a-4*s*(a*(a-1)//2)) for a in A) for k in (1,3,5,7)]
    else:
        plus=lambda a,b:a^b
        if kind=='V4_alternating':
            chi=lambda a,b:root(8*(((a&1)*(b>>1)+(a>>1)*(b&1))%2))
            rhos=[tuple(root(8*(u*(a&1)+v*(a>>1)+(a&1)*(a>>1))) for a in A) for u,v in product(range(2),repeat=2)]
        else:
            chi=lambda a,b:root(8*(((a&1)*(b&1)+(a>>1)*(b>>1))%2))
            rhos=[tuple(root(4*(u*(a&1)+v*(a>>1))) for a in A) for u,v in product((1,3),repeat=2)]
    for r in rhos:
        for a,b in product(A,repeat=2):
            if r[plus(a,b)]!=mul(conj(chi(a,b)),mul(r[a],r[b])):
                raise ValueError('quadratic rho equation')
    xs=[]
    for a in A:
        eps=[e for e in range(16) if root(2*e)==conj(chi(a,a))]
        if len(eps)!=2: raise ValueError('epsilon square roots')
        xs += [('X',a,e) for e in eps]
    ys=[('Y',a,b) for a,b in combinations(A,2)]
    zs=[]
    for ir,r in enumerate(rhos):
        gauss=sumc(conj(x) for x in r)
        if any(x%2 for x in gauss): raise ValueError('Gauss half')
        dsq=tuple(sgn*x//2 for x in gauss)
        ds=[e for e in range(16) if root(2*e)==dsq]
        if len(ds)!=2: raise ValueError('Delta square roots')
        zs += [('Z',ir,e) for e in ds]
    labs=xs+ys+zs
    dims=[1]*8+[2]*14
    def twist(o):
        t,a,b=o
        return conj(chi(a,a)) if t=='X' else conj(chi(a,b)) if t=='Y' else root(b)
    def sij(o,p):
        if 'XYZ'.index(o[0])>'XYZ'.index(p[0]): o,p=p,o
        t,a,b=o;u,c,d=p
        if t==u=='X': return mul(chi(a,c),chi(a,c))
        if t=='X' and u=='Y': return scale(chi(a,plus(c,d)),2)
        if t=='X' and u=='Z': return scale(mul(root(b),rhos[c][a]),2)
        if t==u=='Y': return scale(add(mul(chi(a,d),chi(b,c)),mul(chi(a,c),chi(b,d))),2)
        if t=='Y' and u=='Z': return Z
        if t==u=='Z': return mul(root(-b-d),sumc(mul(mul(chi(x,x),chi(x,x)),mul(rhos[a][x],rhos[c][x])) for x in A))
        raise ValueError('S case')
    S=[[sij(o,p) for p in labs] for o in labs]
    T=[twist(o) for o in labs]
    if labs[0]!=('X',0,0): raise ValueError('unit label')
    if S[0]!=[scale(ONE,d) for d in dims]: raise ValueError('S unit row')
    for i,j in product(range(22),repeat=2):
        v=sumc(mul(S[i][k],conj(S[j][k])) for k in range(22))
        if v!=scale(ONE,64 if i==j else 0): raise ValueError(f'S unitarity {kind} {sgn} {i} {j}')
    bosons=[i for i in range(22) if T[i]==ONE]
    def commute(i,j): return S[i][j]==scale(ONE,dims[i]*dims[j])
    lags=[]
    if all(i in bosons for i in range(8)) and all(commute(i,j) for i,j in product(range(8),repeat=2)):
        lags.append(list(range(8)))
    for invs in combinations([i for i in bosons if i<8],4):
        if 0 not in invs: continue
        for z in [i for i in bosons if i>=8]:
            inds=list(invs)+( [z] )
            if all(commute(i,j) for i,j in product(inds,repeat=2)):
                lags.append(inds)
    return {'category':kind,'tau_sign':sgn,'lagrangian_count':len(lags),'count_mod_3':len(lags)%3,'lagrangians':[[labs[i] for i in l] for l in lags], 'boson_count':len(bosons), 'unitarity_exact':True}

def main():
    rows=[data(k,s) for k in ('V4_alternating','V4_nonalternating','C4_i','C4_-i') for s in (1,-1)]
    report={'status':'PASS','field':'Q(zeta16)','source':'Gelaki–Naidu–Nikshych arXiv:0905.3117 §4.3 Prop4.1 and S,T formulas','cases':rows}
    Path(__file__).with_name('TY8_lagrangians_verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps([{'category':r['category'],'tau':r['tau_sign'],'count':r['lagrangian_count']} for r in rows],indent=2))
if __name__=='__main__': main()
