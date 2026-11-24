"""Twist inequality and norm comparison at quartic codegree sixteen."""
from fractions import Fraction as Q
from math import gcd, isqrt
from itertools import product

def phi(n):
    return sum(gcd(i,n)==1 for i in range(1,n+1))

def mu(n):
    d=2
    value=1
    while d*d<=n:
        if n%d==0:
            n//=d
            if n%d==0:
                return 0
            value=-value
        d+=1
    return -value if n>1 else value

def chi(c,x):
    two=1 if x%8 in (1,7) else -1
    five=1 if x%5 in (1,4) else -1
    return {1:1,5:five,8:two,40:five*two}[c]

def coeff(c,n,t):
    """Normalized Gauss coefficient divided by sqrt(c)."""
    g=gcd(n,t)
    n,t=n//g,t//g
    if n%c or gcd(n//c,c)>1:
        return Q(0)
    d=n//c
    return Q(mu(d)*chi(c,t*d),phi(n))

def check_twists():
    rad=(1,5,8,40)
    scale=10**6
    smallest=Q(10**5)
    for a,b,m in product(range(5),range(2),(1,3)):
        n=2**a*5**b*m
        for t in range(1,n+1):
            if gcd(n,t)!=1:
                continue
            xs=[472*(coeff(c,n,t)+coeff(c,n,2*t)) for c in rad]
            xs[0]+=28*coeff(1,n,t)-304*coeff(1,n,2*t)
            xs[1]-=196*coeff(5,n,t)
            h=Q(337-1000*(n==1))
            for x,c in zip(xs,rad):
                lo=isqrt(c*scale**2)
                h+=x*Q(lo+(x<0 and c!=1),scale)
            smallest=min(smallest,h)
    if smallest <= 1:
        raise ValueError("twist inequality failed")
    print("The twist inequality holds with slack greater than 1/1000.")

def check_moment_comparison():
    s = Q(15,16)
    p = Q(1,128**2)
    # Pair bounds at every D>17, using 1/sqrt(c) below each rational.
    for c, b, lower in [(5,Q(9,20),Q(1,6)), (8,Q(3,8),Q(1,5)), (40,Q(1,6),Q(3,10))]:
        if c*b*b <= 1 or (s-b)/2 - Q(1,17) <= lower:
            raise ValueError("invalid pair estimate")
    lower = Q(1000,256) - Q(304001,1000) + 598*(s-p) + 182*(Q(37,96)-p)
    upper = 323 + 846*p + Q(944,128)
    if lower-upper != Q(620053,3072000):
        raise ValueError("incorrect moment comparison")
    print("The norm lower bound contradicts the integrated twist majorant.")


if __name__ == "__main__":
    check_twists()
    check_moment_comparison()
