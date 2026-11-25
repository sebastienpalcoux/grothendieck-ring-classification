#!/usr/bin/env python3
"""Exact linear certificates for bounds implied by the matrix Hecke estimate.

The linear optimizer proposes a dual vector only.  The exported lower bound
is then checked over rational integers.  This file does not by itself prove
descent; it supplies a proved height bound when the certificate is positive.
"""
from fractions import Fraction as F
from itertools import product
from math import isqrt, gcd, lcm
from pathlib import Path
import json, sys
import numpy as np

SCALE=10**12


def root_interval(n):
    d=10**16;z=isqrt(n*d*d)
    return F(z,d),F(z+1,d)


def multiple(x, interval):
    a,b=interval
    return (x*a,x*b) if x>=0 else (x*b,x*a)


def make_constraints(a,b):
    rows=[];rhs=[];labels=[]
    def add(row, bound, label):
        rows.append([int(x*SCALE//1) for x in row])
        rr=bound*SCALE;rhs.append(-(-rr.numerator//rr.denominator))
        labels.append(label)
    def basic(row, label):add(list(map(F,row)),F(0),label)
    for offset in (0,6):
        for j in range(1,6):
            z=[0]*12;z[offset]=1;z[offset+j]=-1
            basic(z,('minimum',offset//6,j))
    z=[0]*12;z[0]=1;z[6]=-1;basic(z,('p0<=q0',))
    directions=[(A,B) for A in range(-4,5) for B in range(-4,5) if gcd(A,B)==1]
    phases=[(F(s),F(0)) for s in (-1,1)]+[(F(0),F(s)) for s in (-1,1)]
    phases += [(F(s*r,5),F(t*u,5)) for r,u in [(3,4),(4,3)] for s,t in product([-1,1],repeat=2)]
    for k,c,C,S in [
        (1,lcm(a,b),[2,1,-1,-2,-1,1],[0,1,1,0,-1,-1]),
        (2,b,[2,-1,-1,2,-1,-1],[0,1,-1,0,1,-1]),
        (3,a,[2,-2,2,-2,2,-2],[0]*6)]:
        rc, r3c=root_interval(c),root_interval(3*c)
        # Separate disk inequalities, with rational supporting directions.
        for A,B in directions:
            for ordinary in (True,False):
                cap=F(gcd(c,2 if ordinary else 4),c)
                norm2=F(A*A)+F(4*B*B,3)
                bound2=cap*norm2
                n,d=bound2.numerator,bound2.denominator
                bound=F(isqrt(n*d*10**32)+1,d*10**16)
                row=[F(0)]*12
                for j in range(6):row[j if ordinary else j+6]=F(A*C[j],2)+B*S[j]
                add(row,bound,('separate',k,ordinary,A,B))
        # Supporting half-spaces of |sqrt(c) qhat|+c|phat|^2<=2.
        tangents=[(F(r,4),F(s,4)) for r,s in product(range(-4,5),repeat=2)]
        if k==3:
            tangents=[(F(r,8),F(0)) for r in range(-12,13)]
            phase_use=[(F(-1),F(0)),(F(1),F(0))]
        else:phase_use=phases
        for r,s in tangents:
            for u,v in phase_use:
                row=[]
                for j in range(6):
                    x=multiple(r*C[j],rc);y=multiple(s*S[j],r3c)
                    row.append(x[0]+y[0])
                for j in range(6):
                    x=multiple(u*F(C[j],2),rc);y=multiple(v*F(S[j],2),r3c)
                    row.append(x[0]+y[0])
                add(row,2+r*r+s*s,('matrix',k,str(r),str(s),str(u),str(v)))
    return rows,rhs,labels


def check_bound(rows,rhs,weights,coordinate):
    assert coordinate in (7,8,9)
    assert len({j for j,_ in weights})==len(weights)
    assert all(isinstance(j,int) and 0<=j<len(rows) and isinstance(w,int) for j,w in weights)
    assert all(w>=0 for _,w in weights)
    c=[0]*12;c[coordinate]=SCALE*10**9
    coeff=[c[i]+sum(rows[j][i]*w for j,w in weights) for i in range(12)]
    numerator=min(coeff[:6])+min(coeff[6:])-sum(rhs[j]*w for j,w in weights)
    return F(numerator,SCALE*10**9)


def run(a,b):
    from scipy.optimize import linprog
    rows,rhs,labels=make_constraints(a,b)
    A=np.array(rows,dtype=float)/SCALE;bb=np.array(rhs,dtype=float)/SCALE
    eq=np.array([[1]*6+[0]*6,[0]*6+[1]*6],dtype=float)
    result=[]
    for k in (1,2,3):
        objective=np.zeros(12);objective[6+k]=1
        res=linprog(objective,A_ub=A,b_ub=bb,A_eq=eq,b_eq=[1,1],bounds=[(0,None)]*12,method='highs')
        assert res.success,res.message
        weights=[(j,int(round(-x*10**9))) for j,x in enumerate(res.ineqlin.marginals) if x< -1e-14]
        bound=check_bound(rows,rhs,weights,6+k)
        result.append(dict(coordinate=k,weights=weights,bound=str(bound),
                           labels=[labels[j] for j,w in weights]))
        print(a,b,'q',k,'certified >=',bound,'approximately',float(bound),flush=True)
    path=Path(__file__).with_name(f'sextic_{a}_{b}_matrix_bound.json')
    path.write_text(json.dumps(dict(a=a,b=b,scale=SCALE,weight_scale=10**9,certificates=result),indent=2)+'\n')


def verify(a,b):
    """Rebuild rational half-spaces and check the saved duals, without an optimizer."""
    path=Path(__file__).with_name(f'sextic_{a}_{b}_matrix_bound.json')
    data=json.loads(path.read_text())
    assert data['a']==a and data['b']==b
    assert data['scale']==SCALE and data['weight_scale']==10**9
    rows,rhs,labels=make_constraints(a,b)
    coordinates=set()
    for item in data['certificates']:
        k=item['coordinate']
        assert k in (1,2,3) and k not in coordinates
        coordinates.add(k)
        assert item['labels']==[list(labels[j]) for j,w in item['weights']]
        bound=check_bound(rows,rhs,item['weights'],6+k)
        assert bound==F(item['bound'])
        if (a,b)==(8,13):assert bound>F(1,160)
        print(a,b,'q',k,'exact certified lower bound',bound,flush=True)
    assert coordinates=={1,2,3}
    print('All three exact dual bounds verified; reflection covers q4 and q5.')


if __name__=='__main__':
    if sys.argv[-1]=='--verify':verify(*map(int,sys.argv[1:-1]))
    else:run(*map(int,sys.argv[1:]))
