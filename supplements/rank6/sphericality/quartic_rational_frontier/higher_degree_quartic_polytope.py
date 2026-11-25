#!/usr/bin/env python3
"""Exact outer-polytope certificates for primitive biquadratic ratios.

The numerical solver only proposes nonnegative dual weights. Every recorded
exclusion is subsequently checked over the integers with outward bounds.
The normalization is w_i=(p_i+q_i)/(s+t), so sum w_i=1. Since s+t>=1,
all unnormalized Fourier bounds remain necessary after this normalization.
This script does not enumerate the twenty-four unbounded exceptional fields.
"""
from pathlib import Path
from math import isqrt, gcd
from fractions import Fraction as F
import json, sys

BASE = Path(__file__).parent
SCALE = 10**12
CHAR = ((1, 1, -1, -1), (1, -1, 1, -1), (1, -1, -1, 1))


def floorf(x):
    return x.numerator // x.denominator


def ceilf(x):
    return -((-x.numerator) // x.denominator)


def embeddings(row):
    a, b, c, A, u, v, w, B, C, N = row
    signs = ((1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1))
    roots = [isqrt(d*SCALE*SCALE) for d in (a,b,c)]
    lo, hi = [], []
    for sg in signs:
        lower = upper = A*SCALE
        for coefficient, sign, root in zip((u,v,w), sg, roots):
            z = coefficient*sign
            lower += z*(root if z >= 0 else root+1)
            upper += z*(root+1 if z >= 0 else root)
        lo.append(lower//4)
        hi.append(-((-upper)//4))
    k = min(range(4), key=lambda i:lo[i])
    assert all(hi[k] < lo[i] for i in range(4) if i != k)
    lo, hi = [lo[i^k] for i in range(4)], [hi[i^k] for i in range(4)]
    assert lo[0] > 0 and hi[0] < SCALE
    return lo, hi


def constraints(row):
    lo, hi = embeddings(row)
    # b_i=1/(1+alpha_i), a_i=1-b_i.
    bl = [F(SCALE, SCALE+x) for x in hi]
    bu = [F(SCALE, SCALE+x) for x in lo]
    rows, rhs = [], []

    def add(coeffs, bound):
        rows.append([floorf(x*SCALE) for x in coeffs])
        rhs.append(ceilf(bound*SCALE))

    def add_pq(wp, wq, bound):
        cc = []
        for i in range(4):
            z = wq[i]-wp[i]
            cc.append(wp[i]+z*(bl[i] if z >= 0 else bu[i]))
        add(cc, bound)

    zero = [F(0)]*4
    for j in range(1,4):
        r=zero.copy(); r[0]=F(1); r[j]=F(-1)
        add_pq(zero,r,F(0))
        add_pq(r,zero,F(0))
    # s<=t and s>=1/3, t<1 imply 1/4 < s/(s+t) <= 1/2.
    add_pq([F(1)]*4,zero,F(1,2))
    add_pq([F(-1)]*4,zero,F(-1,4))
    # All nontrivial shifted central traces are at least s.
    for j in range(1,4):
        cc=[]
        for i in range(4):
            lower=F(lo[i]-hi[i^j],SCALE)
            cc.append(lower*(bl[i] if lower>=0 else bu[i]))
        add(cc,F(0))

    directions=[(x,y) for x in range(-4,5) for y in range(-4,5)
                if gcd(x,y)==1]
    for c, C in zip(row[:3],CHAR):
        for ordinary in (False,True):
            n=gcd(c,2 if ordinary else 4)
            upper=F(isqrt(n*c*SCALE*SCALE)+1,c*SCALE)
            for sign in (-1,1):
                v=[F(sign*x) for x in C]
                add_pq(v if ordinary else zero,zero if ordinary else v,upper)
        for x,y in directions:
            upper=F(isqrt((2*x*x+4*y*y)*c*SCALE*SCALE)+1,c*SCALE)
            add_pq([F(x*z) for z in C],[F(y*z) for z in C],upper)
        root_lower=F(isqrt(c*SCALE*SCALE),SCALE)
        for sign in (-1,1):
            for rnum in range(-32,33):
                r=F(rnum,64)
                add_pq([2*c*r*x for x in C],
                       [sign*root_lower*x for x in C],F(2)+c*r*r)
    return rows,rhs


def certificate(rows,rhs,weights):
    assert all(w>=0 for _,w in weights)
    return min(sum(rows[j][i]*w for j,w in weights) for i in range(4))-sum(rhs[j]*w for j,w in weights)


def run():
    import numpy as np
    from scipy.optimize import linprog
    data=[list(map(int,line.split())) for line in
          (BASE/'higher_degree_quartic_biquadratic_candidates.txt').read_text().splitlines()]
    certificates=[];survivors=[]
    for ci,row in enumerate(data):
        rows,rhs=constraints(row)
        A=np.array(rows,dtype=float)/SCALE; b=np.array(rhs,dtype=float)/SCALE
        res=linprog([0]*4+[1],A_ub=np.column_stack([A,-np.ones(len(A))]),
                    b_ub=b,A_eq=[[1]*4+[0]],b_eq=[1],bounds=[(0,None)]*5,method='highs')
        assert res.success,res.message
        rejected=False
        if res.fun>1e-10:
            for precision in (10**6,10**9,10**12):
                weights=[(j,int(round(-x*precision))) for j,x in enumerate(res.ineqlin.marginals) if x < -1e-14]
                gap=certificate(rows,rhs,weights)
                if gap>0:
                    certificates.append(dict(index=ci,weights=weights,gap=str(gap)))
                    rejected=True;break
        if not rejected:
            survivors.append(dict(index=ci,ratio=row,phase1=float(res.fun),point=list(res.x[:4])))
        if ci%25==0:
            print(ci,'excluded',len(certificates),'remaining',len(survivors),flush=True)
    result=dict(scale=SCALE,constraint_version=1,certificates=certificates,survivors=survivors)
    (BASE/'higher_degree_quartic_biquadratic_polytope.json').write_text(json.dumps(result,indent=2)+'\n')
    print('FINAL excluded',len(certificates),'remaining',len(survivors),flush=True)


def verify():
    data=[list(map(int,line.split())) for line in
          (BASE/'higher_degree_quartic_biquadratic_candidates.txt').read_text().splitlines()]
    result=json.loads((BASE/'higher_degree_quartic_biquadratic_polytope.json').read_text())
    assert result['scale']==SCALE and result['constraint_version']==1
    assert len(data)==258 and len(result['certificates'])==258
    assert result['survivors']==[]
    ids=set()
    for record in result['certificates']:
        i=record['index']
        assert type(i) is int and 0<=i<len(data) and i not in ids
        ids.add(i)
        rows,rhs=constraints(data[i])
        used=set()
        for pair in record['weights']:
            assert type(pair) is list and len(pair)==2
            j,w=pair
            assert type(j) is int and type(w) is int
            assert 0<=j<len(rows) and w>=0 and j not in used
            used.add(j)
        gap=certificate(rows,rhs,record['weights'])
        assert gap>0 and str(gap)==record['gap']
    residual=set(range(len(data)))-ids
    assert len(ids)==258 and not residual
    print('Exact quartic dual certificates:',len(ids),'; surviving ratios:',len(residual))


if __name__=='__main__':
    verify() if sys.argv[-1]=='--verify' else run()
