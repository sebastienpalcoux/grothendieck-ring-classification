"""Exact finite recurrence for the folded conductor-twelve profiles."""
from fractions import Fraction as F
from functools import cache
from math import isqrt, lcm
from itertools import product

ONE=(1,0)
ETA=F(999999,1000000)


def add(x,y): return x[0]+y[0],x[1]+y[1]
def scale(x,n): return x[0]*n,x[1]*n
def mul(x,y): return x[0]*y[0]+3*x[1]*y[1],x[0]*y[1]+x[1]*y[0]
def positive(x):
    a,b=x
    if a*b>=0:
        return a>0 or b>0
    return a*(a*a-3*b*b)>0


@cache
def power(k):
    if k==0: return ONE
    return mul((2,1),power(k-1)) if k>0 else mul((2,-1),power(k+1))


@cache
def B(e,k):
    if k==0: return 2-e
    if k==1: return 4-e
    if k<0: return 4*B(e,k+1)-B(e,k+2)
    return 4*B(e,k-1)-B(e,k-2)


@cache
def divisors(n):
    return sorted({a for i in range(1,isqrt(n)+1) if n%i==0 for a in (i,n//i)})


@cache
def coeff(t,scaled):
    if not t: return ONE
    if t>0: return (F(1,2),F(1,6)) if scaled else (3,1)
    return (3,-1) if scaled else (F(1,2),F(-1,6))


def tuples():
    for e,d,r,c in product(range(2),range(2),range(-1,7),range(1,28)):
        W=B(e,0)*B(d,r+1)-B(e,1)*B(d,r)
        if not positive(add(mul(power(r),coeff(d-e,False)),(-c,0))) or (d>e and c%6):
            continue
        assert 0<abs(W)<=9360
        for h in divisors(4*c*abs(W)):
            for z in range(-14,4):
                if 2*z+e<2*r+d:
                    yield e,d,r,c,h,z


def scalar_ok(m,e,d,h,c):
    return m%4==0 and m%((2 if e else 6)*h)==0 and m%((2 if d else 6)*c)==0


def small(para,k):
    e,d,r,c,h,z=para;j=k+z;l=k+r
    if j<1 or l<1: return False
    b,g,o=B(e,k),B(e,j),B(d,l)
    m=2*(b+h*g)
    if not scalar_ok(m,e,d,h,c): return False
    if not any(m*(4-Z)>4*c*o and (m*(4-Z)-4*c*o)%(4*h)==0 for Z in (2,3)): return False
    if c*o<2*b: return False
    # Six times the family denominator clears both rational gap inequalities.
    n=6**max(e,d)
    gap=n*b*b-4*(n//6**e) + h*h*(n*g*g-4*(n//6**e)) + 2*c*c*(n*o*o-4*(n//6**d))
    if 3*gap>n*m*m: return False
    return 9*c*o>2*m or 6*gap+n*(m-2*c*o)**2<=2*n*m*m


@cache
def tail_masses(e,d,r,c,h,z):
    x=scale(power(z),h); y=scale(mul(coeff(d-e,True),power(r)),c)
    return x,y,scale(add(ONE,x),2)


def tail(para):
    x,y,den=tail_masses(*para)
    den2=mul(den,den)
    if not positive(add(den,scale(y,-2*ETA))): return False
    # Lower gap-square total before the ordinary complementary pair.
    gap=scale(add(add(ONE,mul(x,x)),scale(mul(y,y),2)),3*ETA**2)
    if positive(add(gap,scale(den2,-1))): return False
    if positive(add(scale(y,9),scale(den,-2*ETA))): return True
    q=add(scale(den,F(1,2)),scale(y,-1/ETA))
    if positive(q): gap=add(gap,scale(mul(q,q),2))
    return not positive(add(gap,scale(den2,-1)))


def residues(para):
    e,d,r,c,h,z=para
    mod=lcm(4*h,6*h,6*c)
    s=tuple(B(f,j)%mod for f,j in [(e,0),(e,1),(e,z),(e,z+1),(d,r),(d,r+1)])
    initial=s;p=0
    while True:
        b,b1,g,g1,o,o1=s;m=2*(b+h*g)
        if scalar_ok(m,e,d,h,c):
            assert all((m*(4-Z)-4*c*o)%(4*h) for Z in (2,3))
        s=(b1,(4*b1-b)%mod,g1,(4*g1-g)%mod,o1,(4*o1-o)%mod);p+=1
        if s==initial: return p


if __name__=='__main__':
    assert positive(add(power(28),(-10**9,0)))
    finite=0;tail_list=[];count=0
    for p in tuples():
        count+=1
        finite+=sum(small(p,k) for k in range(28))
        if tail(p): tail_list.append((p,residues(p)))
    print(count,'parameters;',finite,'finite matches;',tail_list)
    assert finite==0 and len(tail_list)==4
