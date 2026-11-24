"""Cyclic cubic profile bounds and exact minimal-polynomial enumeration."""
from fractions import Fraction
from functools import lru_cache
from math import gcd, isqrt, lcm

import sympy as sp


X = sp.Symbol("X")


@lru_cache(None)
def upper(s, conductor, odd):
    """First integral D excluded by the monotone profile inequality."""
    mass = sp.Rational(s.numerator, s.denominator)

    def admissible(d):
        if odd:
            return (mass - 1/sp.sqrt(conductor))*d <= 3+3*sp.sqrt(d-1)
        return mass <= sp.Rational(3,d)+2/sp.sqrt(conductor)

    lo, hi = 2, 4
    while admissible(hi):
        lo, hi = hi, 2*hi
    while hi-lo > 1:
        mid = (lo+hi)//2
        if admissible(mid):
            lo = mid
        else:
            hi = mid
    return hi


def cube_multiple(n):
    """Least positive a such that n divides a cubed."""
    h = 1
    for p, k in sp.factorint(n).items():
        h *= int(p)**((k+2)//3)
    return h


def search(conductor, s0, kind):
    odd = kind == "odd"
    common_cap = upper(s0, conductor, odd)
    tmax = int(sp.integer_nthroot(5*common_cap**2, 3)[0])
    survivors = []
    for r in range(3,tmax+1):
        for t in range(r,tmax+1):
            if (r==3 and t!=6) or (r,t)==(4,4):
                continue
            if kind=="odd" and not (r%2 and t%2):
                continue
            if kind=="large_codes" and (r<7 or (r%2 and t%2)):
                continue
            if kind=="four" and (r!=4 or t%32!=16):
                continue
            s = 1 - Fraction(1,r) - Fraction(1,t)
            if s < s0:
                continue
            h = upper(s,conductor,odd)
            amax = 2*h+5
            step = lcm(r,t)**3
            for n in range(step,5*h*h+1,step):
                if conductor!=19 and r*t*n%(conductor**2):
                    continue
                if r!=t and isqrt(r*t*n)**2 != r*t*n:
                    continue
                bq = s*n
                if bq.denominator != 1:
                    continue
                b=int(bq)
                mult = cube_multiple(n)
                for a in range(mult,amax+1,mult):
                    if s*s-Fraction(3*a,n)>Fraction(1,conductor):
                        continue
                    disc=a*a*b*b-4*b**3-4*a**3*n-27*n*n+18*a*b*n
                    if disc<=0 or isqrt(disc)**2!=disc:
                        continue
                    # In the F>=19 case require a possible conductor dividing
                    # both discriminants. Keeping arbitrary integer F enlarges
                    # the search and avoids classifying cubic conductors here.
                    if conductor==19:
                        g=gcd(disc,r*t*n)
                        square_root_divisor = 1
                        for prime, exponent in sp.factorint(g).items():
                            square_root_divisor *= int(prime)**(exponent//2)
                        if square_root_divisor < 19:
                            continue
                    elif disc%(conductor**2):
                        continue
                    p=sp.Poly(X**3-a*X**2+b*X-n,X)
                    if p.is_irreducible and p.count_roots(1,h)==3 and p.count_roots(17,h):
                        survivors.append((r,t,a,b,n))
    print(conductor,kind,common_cap,survivors)
    return survivors


def verify():
    survivors = []
    for conductor,s0,kind in [
        (19,Fraction(1,2),"conductor"),
        (13,Fraction(7,12),"conductor"),
        (7,Fraction(3,5),"odd"),
        (9,Fraction(3,5),"odd"),
        (7,Fraction(65,84),"large_codes"),
        (9,Fraction(65,84),"large_codes"),
        (9,Fraction(11,16),"four"),
    ]:
        survivors.extend(search(conductor,s0,kind))
    if set(survivors)!={(7,7,42,245,343)}:
        raise ArithmeticError(survivors)


if __name__=="__main__":
    verify()
