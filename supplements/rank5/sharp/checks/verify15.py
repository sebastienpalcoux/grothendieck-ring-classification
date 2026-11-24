"""Exact verification of the twist inequality for the quartic field of conductor 15."""

if not __debug__:
    raise RuntimeError("Run this verifier with Python assertions enabled")

from fractions import Fraction as F
from math import gcd
from functools import lru_cache

SCALE = 10**8
# Lower endpoints for cos(2*pi*a/15) for a = 0,...,7. The endpoint tests
# below certify the entries using the real cyclotomic polynomials.
LOWER = (100000000,91354545,66913060,30901699,-10452847,-50000000,-80901700,-97814761)
J = (1,2,3,4,6)
C = (22,22,120,230,-61)

def polynomial(a,x):
    if a in (3,6):
        return 4*x*x + 2*x - 1
    y=2*x
    return y**4-y**3-4*y*y+4*y+1

def certify_cosines():
    for a in (1,2,3,4,6,7):
        lo=F(LOWER[a],SCALE)
        assert polynomial(a,lo)*polynomial(a,lo+F(1,SCALE)) < 0
    assert all(LOWER[a] > LOWER[a+1]+1 for a in range(7))

@lru_cache(maxsize=None)
def cos_interval(a):
    a=min(a%15,(-a)%15)
    x=F(LOWER[a],SCALE)
    return x,x+(F(1,SCALE) if a not in (0,5) else 0)

def scale(t,interval):
    a,b=interval
    return (t*a,t*b) if t>=0 else (t*b,t*a)

def mobius_phi(n):
    m=n;phi=n;mu=1;p=2
    while p*p<=m:
        if m%p==0:
            phi=phi//p*(p-1);mu=-mu
            m//=p
            if m%p==0: return F(0)
        p+=1
    if m>1:
        mu=-mu; phi=phi//m*(m-1)
    return F(mu,phi)

@lru_cache(maxsize=None)
def avg(t,n,g):
    # Mean real part of exp(2*pi*i*t*u/n), for units u congruent
    # to +/-g mod 15. t/n is reduced before Chinese remaindering.
    d=gcd(t,n)
    t//=d;n//=d
    d=gcd(15,n);m=n//d
    if gcd(15,m)!=1:
        return (F(0),F(0))
    a=0 if d==1 else 15//d*(t*g*pow(m,-1,d))
    return scale(mobius_phi(m),cos_interval(a))

def check(t,n):
    low=F(2003)
    for j,c in zip(J,C):
        low+=4*c*mobius_phi(n//gcd(n,j))
    for j,c in ((1,3334),(2,2236),(3,1098)):
        low+=scale(c,avg(j*t,n,1))[0]
    for g,c in ((1,-44),(2,-44),(4,44),(8,44)):
        low+=scale(c,avg(t,n,g))[0]
    return low-10000*(n==1)

def verify():
    certify_cosines()
    denominators=[d*m for d in range(1,361) if 360%d==0 for m in (1,7)]
    lower=min(check(t,n) for n in denominators for t in range(n) if gcd(t,n)==1)
    assert lower>0,lower
    print("Conductor-15 twist inequality verified; minimum lower margin",lower)

if __name__=="__main__":
    verify()
