"""Certify the small-trace abelian quartic scan and its rational Fourier tests."""
from fractions import Fraction as F
from itertools import permutations, product
from math import gcd, isqrt
from pathlib import Path
import json
import sys
import sympy as sp
from sympy.polys.numberfields import round_two

X=sp.Symbol('X')
SCALE=10**9
CERT=Path(__file__).with_name('quartic_field_duals.json')

def conductor(n):
    rad=1
    for prime,e in sp.factorint(n).items():
        if e%2: rad*=int(prime)
    return rad if rad%4==1 else 4*rad

def census():
    selected=[]
    for a in range(5,17):
        for n in sp.divisors(a**4):
            if n*256>a**4: continue
            fac=sp.factorint(n)
            def step(r):
                return int(sp.prod(p**((r*e+3)//4) for p,e in fac.items()))
            for b in range(step(2),3*a*a//8+1,step(2)):
                for c in range(step(3),a**3//16+1,step(3)):
                    if 9*a*c>4*b*b or min(b-3*a+6,c-2*b+3*a-4,n-c+b-a+1)>0: continue
                    def resolvent(k):
                        return k**3-b*k*k+(a*c-4*n)*k-(a*a-4*b)*n-c*c
                    roots=[k for k in range(1,b+1) if resolvent(k)==0]
                    if not roots: continue
                    poly=sp.Poly(X**4-a*X**3+b*X**2-c*X+n,X)
                    disc=poly.discriminant()
                    if disc<=0 or not poly.is_irreducible or poly.count_roots(0,1)==0: continue
                    if poly.count_roots(0,sp.oo)!=4: continue
                    gal,_=poly.galois_group()
                    if not gal.is_abelian: continue
                    if gal.is_cyclic:
                        d=conductor(disc)
                        if d<13: continue
                        cond=(d,d)  # odd quadratic conductor, a lower envelope for all faithful conductors
                    else:
                        rad=[a*a-4*(b-k) for k in roots]
                        fields={conductor(t) for t in rad if t>0}-{1}
                        if len(fields)==2:fields.add(conductor(sp.prod(fields)))
                        assert len(fields)==3
                        cond=tuple(sorted(fields))
                        if a>14 or cond[0]<13: continue
                    selected.append(((a,b,c,int(n)),cond))
    return sorted(selected)

def down(x): return F(x.numerator//x.denominator,1)
def rows(poly,cond,ordering,case="generic"):
    a,b,c,n=poly
    pol=sp.Poly(X**4-a*X**3+b*X**2-c*X+n,X)
    intervals=pol.intervals(eps=sp.Rational(1,10**12))
    real=[(F(int(l.p),int(l.q)),F(int(h.p),int(h.q))) for ((l,h),m) in intervals]
    vals=[real[i] for i in ordering]
    unit=[1]*4
    z=[0]*4
    out=[]
    def add(p,q,r):
        out.append(([int(down(SCALE*(p[i]*vals[i][int(p[i]<0)]+q[i]))) for i in range(4)],int(-down(-SCALE*F(r)))))
    def scale(k,v):return [k*j for j in v]
    add(z,unit,1);add(unit,z,1)
    if case=='generic':add(z,scale(-1,unit),F(-71,100))
    elif case=='gold-long':add(z,scale(-1,unit),F(-16,25))
    elif case=='gold-short':
        for factor in (-1,1):
            add(scale(factor,unit),z,F(factor,2))
            add(z,scale(factor,unit),F(factor,2))
    else:raise ValueError(case)
    for j in range(1,4):
        v=[int(i==0)-int(i==j) for i in range(4)]
        add(v,z,0);add(z,v,0)
    if len(cond)==3:
        chars=[([1,1,-1,-1],z,cond[0]),([1,-1,1,-1],z,cond[1]),([1,-1,-1,1],z,cond[2])]
    else:
        chars=[([1,-1,1,-1],z,cond[0]),([1,0,-1,0],[0,1,0,-1],cond[1])]
    for re,im,k in chars:
        if any(im):
            directions=sorted({(F(s*p),F(t*q)) for s,t in product((-1,1),repeat=2)
                for p,q in ((1,0),(0,1),(F(3,5),F(4,5)),(F(4,5),F(3,5)))})
        else:directions=[(F(1),F(0)),(F(-1),F(0))]
        tests=[[p*m+q*n for m,n in zip(re,im)] for p,q in directions]
        lower=F(isqrt(k*SCALE*SCALE),SCALE)
        for v in tests:
            if case=='gold-short' and k==5:
                add(z,v,F(isqrt(5*SCALE*SCALE)+1,10*SCALE))
            for power in (2,4):
                upper=F(1+isqrt(gcd(k,power)*k*SCALE**2),k*SCALE)
                add(v if power==2 else z,v if power==4 else z,upper)
            for w in tests:
                for t in (F(i,20) for i in range(1,11)):
                    add(scale(2*k*t,v),scale(lower,w),2+k*t*t)
    return out

def gap(R,weights):
    cols=[0]*4
    rhs=0
    for row,w in weights:
        assert 0<=row<len(R) and w>0
        v,r=R[row]
        for i in range(4):cols[i]+=w*v[i]
        rhs+=w*r
    return min(0,*cols)-rhs

def solve(R):
    import numpy as np
    from scipy.optimize import linprog
    g=np.array([v for v,_ in R],dtype=float)/SCALE
    h=np.array([b for _,b in R],dtype=float)/SCALE
    ans=linprog([0,0,0,0,1],A_ub=np.column_stack((g,-np.ones(len(R)))),b_ub=h,bounds=[(0,None)]*4+[(None,None)])
    assert ans.success and ans.fun>0
    w=[[i,round(-val*10**10)] for i,val in enumerate(ans.ineqlin.marginals) if round(-val*10**10)>0]
    assert gap(R,w)>0
    return w

if __name__=='__main__':
    generate='--generate' in sys.argv
    expected=[((9,19,9,1),(13,13)),((12,45,54,1),(28,44,77)),((13,40,13,1),(17,17)),((14,38,28,4),(21,60,140)),((15,60,72,9),(13,13))]
    assert census()==expected
    weights=[] if generate else json.loads(CERT.read_text())
    gaps=[]
    for coeff,cond in expected:
        for idx in permutations(range(1,4)):
            R=rows(coeff,cond,(0,*idx))
            if generate:weights.append(solve(R))
            d=gap(R,weights[len(gaps)])
            assert d>0
            gaps.append(d)
    assert len(gaps)==len(weights)==30
    if generate:CERT.write_text(json.dumps(weights,separators=(',',':'))+'\n')
    print('Five quartic polynomials; 30 exact exclusions; least scaled gap',min(gaps))
