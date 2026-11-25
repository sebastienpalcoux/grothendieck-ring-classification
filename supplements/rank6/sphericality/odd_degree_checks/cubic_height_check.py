#!/usr/bin/env python3
"""Exact finite certificate closing the remaining K7 double-orbit case.

The Fourier certificates prove E<2000 or E<44.  Every totally positive
integral d-number in K7 is n*delta^r*u^2, where n>=1, r in {0,1,2},
delta=1-theta+theta^2, and u is an integral unit.  We enumerate all such
E with trace<=6000, using exact LDL ellipsoid enumeration.  The signed
Fourier conditions leave seven values in the first branch and none in
the second.  All seven violate the ordinary Fourier bound.

Only the standard library and the companion exact certificate are used;
there are no floating-point computations or exploratory cutoff inputs.
"""
from fractions import Fraction as F
from math import isqrt, lcm
from cubic_ratio_fourier import (Interval, HEIGHT_CERTIFICATES,
                                root_intervals, matrix,
                                verify_positive_definite)

ONE = (1, 0, 0)
BASIS = ((1, 0, 0), (0, 1, 0), (0, 0, 1))


def add(a, b): return tuple(x+y for x, y in zip(a, b))
def scale(n, a): return tuple(n*x for x in a)
def mul(a, b):
    p = [0]*5
    for i in range(3):
        for j in range(3): p[i+j] += a[i]*b[j]
    for k in (4, 3):
        x = p[k]
        p[k-3] -= x; p[k-2] += 2*x; p[k-1] += x; p[k] = 0
    return tuple(p[:3])
def tr(a): return 3*a[0]+a[1]+5*a[2]
def sigma(a): return (a[0]+2*a[1]+3*a[2], a[2], -a[1]-a[2])
def norm(z):
    a,b,c = z
    return (a*a*a+a*a*b+5*a*a*c-2*a*b*b+a*b*c+6*a*c*c
            -b*b*b-b*b*c+2*b*c*c+c*c*c)
def inv(a):
    aa = mul(a, a); A = tr(a); B = F(A*A-tr(aa),2)
    return scale(F(1, norm(a)), add(add(aa, scale(-A, a)), scale(B, ONE)))
def variance(q):
    t=tr(q)
    return F(3*tr(mul(q,q))-t*t,2)


THETA = Interval(F(1801937735804, 10**12), F(1801937735805, 10**12))
assert (THETA.lo**3-THETA.lo**2-2*THETA.lo+1) < 0
assert (THETA.hi**3-THETA.hi**2-2*THETA.hi+1) > 0

def value(a): return a[0]+a[1]*THETA+a[2]*THETA*THETA
def positive(a):
    if a == (0, 0, 0): return False
    x = value(a)
    assert x.lo > 0 or x.hi < 0, (a, x.lo, x.hi)
    return x.lo > 0
def max_orientation(a):
    orbit = [a, sigma(a), sigma(sigma(a))]
    for x in orbit:
        if all(x == y or positive(add(x, scale(-1, y))) for y in orbit):
            return x
    raise AssertionError(orbit)


def check_signatures():
    """Three independent unit signatures prove all positive units square."""
    units=((-1,0,0),(0,1,0),sigma((0,1,0)))
    signatures=[]
    for u in units:
        assert abs(norm(u))==1
        orbit=(u,sigma(u),sigma(sigma(u)))
        signatures.append(sum((not positive(x)) << i for i,x in enumerate(orbit)))
    assert len({(signatures[0] if a else 0) ^
                (signatures[1] if b else 0) ^
                (signatures[2] if c else 0)
                for a in (0,1) for b in (0,1) for c in (0,1)})==8
    return signatures


def check_heights():
    for poly,(bound,lam,mu) in HEIGHT_CERTIFICATES.items():
        m=matrix(root_intervals(poly),1,F(lam,1000),F(0),0,
                 [F(mu,1000),F(0),F(0)])
        m[3][3]=m[3][3]-F(mu,1000*bound)
        verify_positive_definite(m)


def ellipsoid(gram, bound):
    n = len(gram)
    L = [[F(i==j) for j in range(n)] for i in range(n)]
    D = []
    for j in range(n):
        D.append(F(gram[j][j])-sum(L[j][k]**2*D[k] for k in range(j)))
        assert D[j] > 0
        for i in range(j+1,n):
            L[i][j]=(gram[i][j]-sum(L[i][k]*L[j][k]*D[k]
                                  for k in range(j)))/D[j]
    den=[lcm(*[L[j][i].denominator for j in range(i,n)]) for i in range(n)]
    nums=[[int(L[j][i]*den[i]) for j in range(n)] for i in range(n)]
    terms=[D[i]/den[i]**2 for i in range(n)]
    factor=lcm(*[x.denominator for x in terms]); weights=[int(x*factor) for x in terms]
    z=[0]*n
    def rec(i,left):
        if i<0:
            yield tuple(z); return
        shift=sum(nums[i][j]*z[j] for j in range(i+1,n));rad=isqrt(left//weights[i])
        for v in range(-((rad+shift)//den[i]),(rad-shift)//den[i]+1):
            z[i]=v;cost=weights[i]*(den[i]*v+shift)**2
            assert cost<=left
            yield from rec(i-1,left-cost)
    yield from rec(n-1,bound*factor)


def primitive_shapes(trace_bound):
    out = set(); delta = (1,-1,1); factor=ONE
    assert norm(delta) == 7
    assert all(positive(x) for x in (delta,sigma(delta),sigma(sigma(delta))))
    for r in range(3):
        gram=[[tr(mul(factor,mul(a,b))) for b in BASIS] for a in BASIS]
        vectors=units=0
        for z in ellipsoid(gram,trace_bound):
            vectors+=1
            if abs(norm(z)) != 1: continue
            units+=1
            base=mul(factor,mul(z,z))
            assert tr(base)<=trace_bound and norm(base)==7**r
            out.add(max_orientation(base))
        print('power',r,'vectors',vectors,'units',units,'total_shapes',len(out),flush=True)
        factor=mul(factor,delta)
    return sorted(out, key=lambda z:(tr(z),z))


def enumerate_E(bound,alpha,shapes):
    out=[]
    for base in shapes:
        if tr(base)>3*bound: continue
        qbase=inv(base); tbase=tr(qbase)
        lo=max(1,(10*tbase/7).__ceil__())
        hi=min((10*tbase/3).__floor__(),3*bound//tr(base))
        for n in range(lo,hi+1):
            E=scale(n,base)
            if norm(E)%49:continue
            if not positive(add(scale(bound,ONE),scale(-1,E))):continue
            q=scale(F(1,n),qbase);t=tr(q);P=variance(q)
            if P+(1-t)**2/4>F(1,7) or P<t*t/4:continue
            p=mul(alpha,q)
            out.append((E,t,P,tr(p),variance(p)))
    return out


def main():
    print('Full unit signature certificate:',check_signatures())
    check_heights()
    shapes=primitive_shapes(6000)
    assert len(shapes)==139
    alpha5=sigma(sigma((0,0,1)))
    alpha6=inv((0,0,1))
    assert alpha5==(2,-1,0) and alpha6==(5,1,-2)
    assert norm(alpha5)==norm(alpha6)==1
    assert positive(add(sigma(alpha5),scale(-1,alpha5)))
    assert positive(add(sigma(sigma(alpha5)),scale(-1,alpha5)))
    assert positive(add(sigma(alpha6),scale(-1,alpha6)))
    assert positive(add(sigma(sigma(alpha6)),scale(-1,alpha6)))
    rows=enumerate_E(2000,alpha5,shapes)
    expected={
        (0,14,14):F(13,28),
        (-7,14,21):F(9,49),
        (-15,27,33):F(73,63),
        (-20,36,44):F(73,112),
        (-25,45,55):F(73,175),
        (-30,54,66):F(73,252),
        (-112,168,210):F(61,196),
    }
    assert {row[0]:row[4] for row in rows}==expected
    assert all(row[4]>F(1,7) for row in rows)
    assert enumerate_E(44,alpha6,shapes)==[]
    for row in rows: print('Excluded E, t, P(q), s, P(p):',row)
    print('PASS: seven E values in the first branch, all violating P(p)<=1/7.')
    print('PASS: no E values in the reciprocal branch.')
    print('PASS: the conductor-seven cubic double-orbit residual is empty.')


if __name__=='__main__':main()
