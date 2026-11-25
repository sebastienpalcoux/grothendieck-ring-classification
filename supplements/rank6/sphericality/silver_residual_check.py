"""Exact exclusions for the three quadratic signed orbits over Q(sqrt(2))."""
from fractions import Fraction as F
from functools import cache
from itertools import product
from math import isqrt
from silver_small_check import trace, greater_ratio, gap


def divisors(n):
    small = [i for i in range(1, isqrt(n)+1) if n % i == 0]
    return sorted(set(small+[n//i for i in small]))


def parameters():
    for e,f,r,a in product(range(2),range(2),range(4),range(1,15)):
        if not greater_ratio(e,f,r,a) or (f>e and a%2):
            continue
        W = trace(e,0)*trace(f,r+1)-trace(e,1)*trace(f,r)
        assert 0 < abs(W) <= 1912
        for h in divisors(2*a*abs(W)):
            if h % 8 == 0:
                continue
            for b in range(-6,3):
                if 2*r+f > 2*b+e:
                    yield e,f,r,a,h,b


def small(p,k,mass_bound=None):
    e,f,r,a,h,b = p
    j, ell = k+b, k+r
    if j < 2:
        return False
    B, G, C = trace(e,k), trace(e,j), trace(f,ell)
    m = 2*(B+h*G)
    if m%h or m%a or (a*C-B)%h or m%(4 if e else 8):
        return False
    n, M = m//h, m//a
    if n%(2 if e else 4) or M%(2 if f else 4):
        return False
    s, t = F(C,M), F(B,m)
    if s >= F(1,2) or t <= F(1,100):
        return False
    if mass_bound is not None:
        return s >= mass_bound and F(1,8)+gap((e,k,m))+gap((e,j,n))+2*gap((f,ell,M)) <= F(1,2)
    return (F(1,8)+gap((e,k,m))+gap((e,j,n))+2*gap((f,ell,M))
            +(F(1,2)-s)**2 <= F(1,2))


def add(x,y):
    return x[0]+y[0],x[1]+y[1]


def scale(x,q):
    return x[0]*q,x[1]*q


def mul(x,y):
    return x[0]*y[0]+2*x[1]*y[1],x[0]*y[1]+x[1]*y[0]


def positive(x):
    a,b=x
    return (a or b)>0 if a*b>=0 else a*(a*a-2*b*b)>0


one=(1,0)


@cache
def u_power(n):
    if n==0:
        return one
    base=(3,2) if n>0 else (3,-2)
    return mul(base,u_power(n-1 if n>0 else n+1))


def sq(x):
    return mul(x,x)


def large(p,mass_bound=None):
    e,f,r,a,h,b=p
    eta=F(10**9-1,10**9+1)
    x=scale(u_power(b),h)
    ratio={-1:(2,-1),0:one,1:(1,F(1,2))}[f-e]
    y=scale(mul(ratio,u_power(r)),a)
    # Multiply through by 4(1+x)^2.
    d=add(one,x)
    tail=add(d,scale(y,-1/eta))
    tail=sq(tail) if positive(tail) else (0,0)
    if mass_bound is not None:
        if positive(add(scale(d,2*mass_bound*eta),scale(y,-1))):
            return False
        tail=(0,0)
    left=add(scale(add(add(one,sq(x)),scale(sq(y),2)),eta*eta),tail)
    return not positive(add(left,scale(sq(d),F(-3,2))))


if __name__=="__main__":
    tuples=list(parameters())
    assert not any(small(p,k) for p in tuples for k in range(24))
    assert not any(large(p) for p in tuples)
    for lower_bound in (F(7,24),F(11,42)):
        assert not any(small(p,k,lower_bound) for p in tuples for k in range(24))
        assert not any(large(p,lower_bound) for p in tuples)
    print("The signed involution is an actual invertible.")
    print(len(tuples),"parameter choices checked at finite and unbounded exponents.")
    print("The remaining two-transposition ordinary spectra are excluded.")
