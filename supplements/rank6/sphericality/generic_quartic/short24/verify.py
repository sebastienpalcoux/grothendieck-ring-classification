"""Exact conductor-24 exclusions for signed codegrees 8 plus or minus 4 sqrt(2)."""
from fractions import Fraction as F
from itertools import product
from math import gcd,isqrt
from pathlib import Path
import json,subprocess,sys,tempfile

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
S=10**12
M=10**6
CHARS=((1,1,-1,-1),(1,-1,1,-1),(1,-1,-1,1))
CS=(8,12,24)
SPECIAL=(52,18,14,10,96,40,4)


def upperroot(x):
    return F(isqrt(x.numerator*S*S//x.denominator)+1,S)


def constraints():
    rows=[]
    zero=(0,)*4
    def add(p,q,b):
        rows.append(([F(M*z).__floor__() for z in p],[F(M*z).__floor__() for z in q],F(M*b).__ceil__()))
    for sg in (-1,1):
        add([sg]*4,zero,sg);add(zero,[sg]*4,sg)
    for i in range(1,4):
        w=[1,0,0,0]; w[i]=-1
        add(w,zero,0);add(zero,w,0)
    for c,v in zip(CS,CHARS):
        rad=F(isqrt(c*S*S),S)
        for sg in (-1,1):
            add([sg*z for z in v],zero,2*upperroot(F(gcd(c,2),c)))
            add(zero,[sg*z for z in v],2*upperroot(F(gcd(c,4),c)))
            for n in range(-15,16):
                r=F(n,14)
                add([2*c*r*z for z in v],[2*sg*rad*z for z in v],8+c*r*r)
        if c==8:
            for a,b in product(range(-6,7),repeat=2):
                if gcd(a,b)==1:
                    add([a*z for z in v],[b*z for z in v],upperroot(F(a*a,2)+b*b))
            for sg in (-1,1):
                add(zero,[sg*z for z in v],F(2,3)*upperroot(F(2)))
    return rows


def materialize(rows,data):
    A,*d=data[:4]
    roots=[(isqrt(c*S*S),isqrt(c*S*S)+1) for c in CS]
    lo=[];hi=[]
    for i in range(4):
        v=[a*h[i] for a,h in zip(d,CHARS)]
        lo.append((A*S+sum(k*g[k<0] for k,g in zip(v,roots)))//4)
        hi.append(-((-A*S-sum(k*g[k>=0] for k,g in zip(v,roots)))//4))
    j=lo.index(min(lo));assert all(hi[j]<lo[i] for i in range(4) if i!=j)
    return [([a[i]*(lo[i^j] if a[i]>=0 else hi[i^j])+b[i]*S for i in range(4)],w*S) for a,b,w in rows]


def certificate(rows,weights):
    assert all(type(i) is int and 0<=i<len(rows) and type(v) is int and v>0 for i,v in weights)
    h=[sum(v*rows[i][0][k] for i,v in weights) for k in range(4)]
    return min(h)>sum(v*rows[i][1] for i,v in weights)


def propose(rows):
    import numpy as np
    from scipy.optimize import linprog
    x=np.array([v for v,w in rows],dtype=float)/(S*M);y=np.array([w for v,w in rows],dtype=float)/(S*M)
    res=linprog([0,0,0,0,1],A_ub=np.column_stack((x,-np.ones(len(rows)))),b_ub=y,bounds=[(0,None)]*4+[(None,None)],method='highs')
    assert res.success
    for scale in (10**6,10**9,10**12):
        w=[[i,round(-v*scale)] for i,v in enumerate(res.ineqlin.marginals) if -v*scale>.5]
        if certificate(rows,w):return w
    raise AssertionError('An exact separating combination was not found')


def moments():
    A=52;d=(18,14,10);corr=(6,4,2)
    ratios=[F(A,2)+F(m*d[(i+1)%3]*d[(i+2)%3],2*d[i]) for i,m in enumerate(corr)]
    total=F(A*A+sum(c*a*a for c,a in zip(CS,d)),4)
    triples=[]
    for x in range(1,52,2):
        for y in range(1,52-x,2):
            z=51-x-y
            if z<1:continue
            Y=(1,x,y,z);T=[sum(u*v for u,v in zip(row,Y)) for row in CHARS]
            second=(total+sum(a*b for a,b in zip(T,ratios)))/4
            if second.denominator!=1:continue
            triples.append((x,y,z))
            # q_0-q_2=(Q_8+Q_24)/2, both odd characters have negative signs
            # at the least embedding. Strict positivity follows with rational bounds.
            lo=F(0)
            for k in (0,2):
                rad=isqrt(CS[k]*S*S)
                lo+=F(-T[k]*S,d[k]*(rad+(-T[k]>=0)))
            assert lo>0
    assert triples==[(1,25,25),(7,39,5),(25,11,15)]


def verify(generate=False):
    with tempfile.TemporaryDirectory() as td:
        tmp=Path(td);fld=tmp/'fields';out=tmp/'ratios';exe=tmp/'enumerate';fld.write_text('8 12 24 320\n')
        subprocess.run(['c++','-O3','-std=c++17',str(ROOT/'quartic_more'/'biquadratic.cpp'),'-o',str(exe)],check=True)
        subprocess.run([str(exe),str(fld),str(out)],check=True)
        data=[tuple(map(int,l.split()))[3:] for l in out.read_text().splitlines()]
    assert len(data)==len(set(data))==444 and SPECIAL in data
    path=HERE/'short24_duals.json';dual={} if generate else json.loads(path.read_text());rows=constraints()
    for candidate in data:
        if candidate==SPECIAL:continue
        xy=materialize(rows,candidate);key=','.join(map(str,candidate))
        if generate:dual[key]=propose(xy)
        assert certificate(xy,dual[key])
    assert len(dual)==443
    if generate:path.write_text(json.dumps(dual,separators=(',',':'))+'\n')
    moments(); print('443 exact linear exclusions and one finite shifted-moment exclusion.')


if __name__=='__main__':verify('--generate' in sys.argv)
