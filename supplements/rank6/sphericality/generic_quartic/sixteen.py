"""Exact height and projection tests in the real cyclotomic field of conductor 16."""
from fractions import Fraction as F
from itertools import product
from math import isqrt
from pathlib import Path
import sys, json, subprocess, tempfile
HERE = Path(__file__).resolve().parent
S=10**9
CERT=HERE/'sixteen_duals.json'

def upper(q):
    q=F(q);return F(isqrt(q.numerator*S*S//q.denominator)+1,S)

def conjugates(a,u,v,w):
    precision=10**16
    rt=isqrt(2*precision**2)
    f=isqrt((2*precision+rt)*precision)
    g=isqrt((2*precision-rt-1)*precision)
    y=[(f,f+2),(g,g+2),(-f-2,-f),(-g-2,-g)]
    vals=[]
    for i in range(4):
        lo=hi=a*precision
        for k,(l,h) in [(2*u*(-1)**i,(rt,rt+1)),(4*v,y[i]),(4*w,y[(i+1)%4])]:
            lo+=min(k*l,k*h);hi+=max(k*l,k*h)
        vals.append((lo*S//(4*precision),-(-hi*S//(4*precision))))
    j=min(range(4),key=lambda k:vals[k][0]);out=vals[j:]+vals[:j]
    assert 0<out[0][0] and out[0][1]<S and all(out[0][1]<l for l,h in out[1:])
    return out

def examples(cap):
    with tempfile.TemporaryDirectory() as t:
        p=Path(t); (p/'field').write_text(f'8 16 2 1 1 1 1 {cap}\n')
        subprocess.run(['c++','-O3','-std=c++17',str(HERE.parent/'quartic_more/cyclic.cpp'),'-o',str(p/'enum')],check=True)
        subprocess.run([str(p/'enum'),str(p/'field'),str(p/'out')],check=True)
        return [tuple(map(int,l.split()))[7:] for l in (p/'out').read_text().splitlines()]

def template(smin,tmin):
    R=[];z=(0,)*4;one=(1,)*4;neg=(-1,)*4
    def add(p,q,b):R.append(([int((F(x)*S).__floor__()) for x in p],[int((F(x)*S).__floor__()) for x in q],int((F(b)*S).__ceil__())))
    def times(k,v):return tuple(k*x for x in v)
    for v in range(1,4):
        d=tuple(int(i==0)-int(i==v) for i in range(4));add(d,z,0);add(z,d,0)
    add(one,z,1);add(z,one,1);add(neg,z,-smin);add(z,neg,-tmin)
    for c in (8,16):
        if c==8: dirs=[(t,-t,t,-t) for t in (-1,1)]
        else:
            U=[(1,0),(0,1),(F(3,5),F(4,5)),(F(4,5),F(3,5)),(F(7,10),F(7,10))]
            dirs=sorted({(a*x,b*y,-a*x,-b*y) for a,b in product((-1,1),repeat=2) for x,y in U})
        for v in dirs:
            add(v,z,upper(F(2,c)));add(z,v,upper(F(4,c)))
            for w in dirs:
                for h in (F(1,10),F(1,5),F(3,10),F(2,5),F(1,2)):
                    add(times(2*c*h,v),times(F(isqrt(c*S*S),S),w),2+c*h*h)
    return R

def transform(T,x):
    return [([p[i]*x[i][p[i]<0]//S+q[i] for i in range(4)],b) for p,q,b in T]

def gap(R,W):
    coeff=[0]*4;rhs=0
    for i,k in W:
        assert type(i) is int and type(k) is int and 0<=i<len(R) and k>0
        v,b=R[i];rhs+=k*b
        for j in range(4):coeff[j]+=k*v[j]
    return min(0,*coeff)-rhs

def tryone(R):
    import numpy as np
    from scipy.optimize import linprog
    m=np.array([v for v,b in R],float)/S;b=np.array([b for v,b in R],float)/S
    opt=linprog([0]*4+[1],A_ub=np.column_stack([m,-np.ones(len(m))]),b_ub=b,bounds=[(0,None)]*4+[(None,None)])
    assert opt.success
    if opt.fun<=1e-9:return []
    W=[[j,round(-w*10**12)] for j,w in enumerate(opt.ineqlin.marginals) if -w*10**12>.5]
    assert gap(R,W)>0
    return W

if __name__=='__main__':
    generate='--generate' in sys.argv;cap=740
    ratios=examples(cap);T=template(F(0),F(71,100));data=[] if generate else json.loads(CERT.read_text());survive=[]
    for j,r in enumerate(ratios):
        R=transform(T,conjugates(*r[:4]));w=tryone(R) if generate else data[j]
        if generate:data.append(w)
        if w:assert gap(R,w)>0
        else:survive.append(r);print('unexcluded',r,flush=True)
    assert len(ratios)==695 and survive==[(460,162,106,44,418,84,1)]
    x=conjugates(*survive[0][:4]);R=transform(template(F(1,2),F(71,100)),x)
    R.append(([x[i][0]-x[(i+2)%4][1] for i in range(4)],0))
    zero=(0,)*4; one=(1,)*4; neg=(-1,)*4
    extra=((zero,neg,F(-711,1000)),(one,zero,F(63,100)),
           (neg,zero,F(-67,100)),(zero,(-2,0,-2,0),F(-2,94)))
    for i,(p,q,b) in enumerate(extra,len(ratios)):
        rr=R+transform([([S*v for v in p],[S*v for v in q],(S*b).__ceil__())],x)
        w=tryone(rr) if generate else data[i]
        assert gap(rr,w)>0
        if generate:data.append(w)
    assert len(data)==699
    print('Cyclic conductor 16: 695 primitive ratios and 698 strict certificates.')
    if generate:CERT.write_text(json.dumps(data,separators=(',',':'))+'\n')
