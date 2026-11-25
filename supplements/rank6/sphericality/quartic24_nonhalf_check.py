"""Exact positive-dual certificates for 4,8;4,9;4,16 in the quartic K24 field."""
from fractions import Fraction as F
from math import gcd,isqrt
from pathlib import Path
import json
import sys
from quartic24_fast import inventory

S=10**10
D=(8,12,24)
CH=((1,1,-1,-1),(1,-1,1,-1),(1,-1,-1,1))
def embed(row):
    _,_,_,a,*rest=row
    raw=rest[:3]
    roots=[isqrt(d*S*S) for d in D]
    vals=[]
    for i in range(4):
        coeff=[raw[j]*CH[j][i] for j in range(3)]
        l=sum(e*(u+(e<0)) for e,u in zip(coeff,roots))
        h=sum(e*(u+(e>0)) for e,u in zip(coeff,roots))
        vals.append((F(a*S+l,4*S),F(a*S+h,4*S)))
    n=min(range(4),key=lambda i:vals[i][0])
    assert all(vals[n][1]<vals[i][0] for i in range(4) if i!=n)
    return [vals[i^n] for i in range(4)]

def inequalities(row):
    al=embed(row);rs=[]
    def raw(coefs,rhs):
        rs.append(([int((r*S).__floor__()) for r in coefs],int((rhs*S).__ceil__())))
    def add(p,q,b):
        raw([p[i]*al[i][p[i]<0]+q[i] for i in range(4)],b)
    zero=(0,0,0,0);s=F(5,8)
    for h in (1,-1):add([h]*4,zero,h)
    for j in (1,2,3):
        co=[0]*4;co[0]=1;co[j]=-1
        add(co,zero,0);add(zero,co,0)
        raw([-al[i^j][1] for i in range(4)],-1)
    for j in range(4):raw([-al[i][1]*al[i^j][1] for i in range(4)],-1)
    for c,row in zip(D,CH):
        root=F(isqrt(c*S*S),S)
        for sg in (1,-1):
            v=[sg*r for r in row]
            add(v,zero,F(isqrt(gcd(c,2)*c*S*S)+1,c*S)/s)
            add(zero,v,F(isqrt(gcd(c,4)*c*S*S)+1,c*S)/s)
            for i in range(-32,33):
                t=F(i,32)
                add([2*c*s*s*t*z for z in row],[root*s*z for z in v],2+c*s*s*t*t)
    return rs

def gap(rows,w):
    assert all(type(j) is int and type(v) is int and 0<=j<len(rows) and v>0 for j,v in w)
    return min(sum(v*(rows[j][0][i]-rows[j][1]) for j,v in w) for i in range(4))
def solve():
    data=sorted(inventory(60))
    path=Path(__file__).with_name('quartic24_nonhalf_duals.json')
    make='--generate' in sys.argv
    if make:
        import numpy as np
        from scipy.optimize import linprog
        records=[]
    else:records=json.loads(path.read_text());assert len(records)==len(data)
    hits=[]
    for i,row in enumerate(data):
        rs=inequalities(row)
        if make:
            A=np.array([z[0] for z in rs],float)/S;b=np.array([z[1] for z in rs],float)/S
            opt=linprog([0]*4+[1],A_ub=np.column_stack((A,-np.ones(len(A)))),b_ub=b,A_eq=[[1]*4+[0]],b_eq=[1])
            assert opt.success
            w=[[j,round(-r*1e11)] for j,r in enumerate(opt.ineqlin.marginals) if -r*1e11>=1]
            if not w or gap(rs,w)<=0:hits.append((i,row));w=[]
            records.append(w)
        elif records[i]:assert gap(rs,records[i])>0
        else:hits.append((i,row))
    if make:path.write_text(json.dumps(records,separators=(',',':'))+'\n')
    assert len(data)==62 and not hits
    print('primitive conjugacy classes',len(data),'exact exclusions',len(records),flush=True)

if __name__=='__main__':solve()
