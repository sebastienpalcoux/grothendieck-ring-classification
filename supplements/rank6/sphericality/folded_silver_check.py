"""Exact finite recurrence for the folded conductor-eight profiles when t >= 1/1000."""
from fractions import Fraction as F
from functools import cache
from math import isqrt, lcm
from itertools import product

ONE=(1,0)
ETA=F(999999,1000000)


def add(x,y): return x[0]+y[0],x[1]+y[1]
def scale(x,n): return x[0]*n,x[1]*n
def mul(x,y): return x[0]*y[0]+2*x[1]*y[1],x[0]*y[1]+x[1]*y[0]
def positive(x):
    a,b=x
    if a*b>=0:
        return a>0 or b>0
    return a*(a*a-2*b*b)>0


@cache
def power(k):
    if k==0: return ONE
    return mul((3,2),power(k-1)) if k>0 else mul((3,-2),power(k+1))


@cache
def B(e,k):
    if k==0: return 2
    if k==1: return 6+4*e
    if k<0: return 6*B(e,k+1)-B(e,k+2)
    return 6*B(e,k-1)-B(e,k-2)


@cache
def divisors(n):
    return sorted({a for i in range(1,isqrt(n)+1) if n%i==0 for a in (i,n//i)})


@cache
def coeff(t,scaled):
    if not t: return ONE
    if t>0: return (1,F(1,2)) if scaled else (2,1)
    return (2,-1) if scaled else (1,F(-1,2))


def tuples():
    for e,d,r,c in product(range(2),range(2),range(-1,7),range(1,46)):
        W=B(e,0)*B(d,r+1)-B(e,1)*B(d,r)
        if not positive(add(mul(power(r),coeff(d-e,False)),(-c,0))) or (d>e and c%2):
            continue
        assert 0<abs(W)<=2*10**6
        for h in divisors(2*c*abs(W)):
            if (not e and not h%2) or (e and not h%4): continue
            for z in range(-14,4):
                if 2*z+e<2*r+d:
                    yield e,d,r,c,h,z


def scalar_ok(m,e,d,h,c):
    return m%4==0 and m%((2 if e else 4)*h)==0 and m%((2 if d else 4)*c)==0


def small(para,k):
    e,d,r,c,h,z=para;j=k+z;l=k+r
    if j<1 or l<1: return False
    b,g,o=B(e,k),B(e,j),B(d,l)
    m=2*(b+h*g)
    if not scalar_ok(m,e,d,h,c): return False
    if (c*o-b)%(2*h) or 1000*b<m or c*o<3*b or 2*c*o>=m: return False
    n=2**max(e,d)
    gap=n*b*b-4*(n//2**e) + h*h*(n*g*g-4*(n//2**e)) + 2*c*c*(n*o*o-4*(n//2**d))
    return 2*gap<=n*m*m



@cache
def tail_masses(e,d,r,c,h,z):
    x=scale(power(z),h); y=scale(mul(coeff(d-e,True),power(r)),c)
    return x,y,scale(add(ONE,x),2)


def tail(para):
    x,y,den=tail_masses(*para)
    den2=mul(den,den)
    if not positive(add(den,scale(y,-2*ETA))): return False
    if positive(add(scale(den,ETA),(-1000,0))): return False
    gap=scale(add(add(ONE,mul(x,x)),scale(mul(y,y),2)),2*ETA**2)
    return not positive(add(gap,scale(den2,-1)))



def residues(para):
    e,d,r,c,h,z=para
    mod=lcm(4*h,4*c)
    s=tuple(B(f,j)%mod for f,j in [(e,0),(e,1),(e,z),(e,z+1),(d,r),(d,r+1)])
    initial=s;p=0;kept=False
    while True:
        b,b1,g,g1,o,o1=s;m=2*(b+h*g)
        if scalar_ok(m,e,d,h,c):
            if (c*o-b)%(2*h)==0: kept=True
        s=(b1,(6*b1-b)%mod,g1,(6*g1-g)%mod,o1,(6*o1-o)%mod);p+=1
        if s==initial: return p,kept


if __name__=='__main__':
    assert positive(add(power(28),(-10**9,0)))
    finite=[];tail_list=[];count=0
    expected=(1,1,3,1,10,2)
    for p in tuples():
        count+=1
        finite.extend((p,k) for k in range(28) if small(p,k))
        if tail(p): tail_list.append((p,*residues(p)))
    assert set(p for p,k in finite)=={expected}
    assert set(p for p,_,kept in tail_list if kept)=={expected}
    print(count,'parameters;',len(finite),'small matches;',len(tail_list),'tail cases;',max(v for _,v,_ in tail_list),'max period')
