"""Exact bounded-mass test for distinct rational four-rows over Q(sqrt(2))."""
from fractions import Fraction as Q
from functools import cache
from math import isqrt


@cache
def trace(family, index):
    if index == 0:
        return 2
    if index == 1:
        return 10 if family else 6
    if index < 0:
        return 6*trace(family,index+1)-trace(family,index+2)
    return 6*trace(family,index-1)-trace(family,index-2)


@cache
def power(k):
    if k == 0:
        return 1,0
    a,b=power(k-1)
    return 3*a+4*b,2*a+3*b


def positive(a,b):
    if a*b >= 0:
        return a>0 or b>0
    return a*(a*a-2*b*b)>0


@cache
def divisors(n):
    return sorted({s for a in range(1,isqrt(n)+1) if n%a==0 for s in (a,n//a)})


def candidates():
    for d in range(2):
        for r in range(1,5):
            a,b=power(r)
            for c in range(1,35):
                if not (positive(a-c,b) if d else positive(a-2*c,b-c)):
                    continue
                wr=trace(1,0)*trace(d,r+1)-trace(1,1)*trace(d,r)
                assert wr
                for h in divisors(4*c*abs(wr)):
                    if h%4!=1:
                        continue
                    assert h<5**14
                    for z in range(-15,4):
                        if 2*z+1<2*r+d:
                            yield d,r,c,h,z


def small(p,k):
    d,r,c,h,z=p
    if k+z<1:
        return False
    b,g,o=trace(1,k),trace(1,k+z),trace(d,k+r)
    m=2*(b+h*g)
    if m%(32*h)!=24*h or m%32!=24 or m%((2 if d else 4)*c):
        return False
    if 1000*b<m or c*o<3*b:
        return False
    if not any(m*(4-Z)>4*c*o and (m*(4-Z)-4*c*o)%(8*h)==0 for Z in (2,3)):
        return False
    gap=(b*b-2)+h*h*(g*g-2)+2*c*c*(o*o-(2 if d else 4))
    if 2*gap>m*m:
        return False
    if 8*c*o>=3*m:
        return True
    # Additional ordinary irrational pair. For d=0 it cannot be
    # accompanied by two rational four-rows.
    cap=4 if d else 5
    extra=max(cap*m-8*c*o,0)
    return 64*gap+extra**2<=32*m*m


def tail(p):
    d,r,c,h,z=p
    b,g,o=trace(1,32),trace(1,32+z),trace(d,32+r)
    m=2*(b+h*g)
    eps=Q(999999,1000000)
    t,w,s=Q(b,m),Q(h*g,m),Q(c*o,m)
    if 1000*t<eps:
        return False
    gap=eps**2*(t*t+w*w+2*s*s)
    if gap>Q(1,2):
        return False
    if s/eps>=Q(3,8):
        return True
    cap=Q(1,2) if d else Q(5,8)
    return gap+max(0,cap-s/eps)**2<=Q(1,2)


if __name__=='__main__':
    count=0
    for p in candidates():
        count+=1
        assert all(not small(p,k) for k in range(32)),p
        assert not tail(p),p
    print(count,'relative-index tuples; no bounded-mass candidates')
