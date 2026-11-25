"""Exact Wronskian sieves for rational silver codegrees (4,16) and (4,9)."""
from fractions import Fraction as F
from itertools import product
from math import lcm
from silver_small_check import trace, greater_ratio, gap
from silver_residual_check import divisors, add, scale, mul, sq, positive, u_power, one


PROFILES={16:(F(11,16),F(1,6)),9:(F(23,36),F(1,4))}
ETA=F(10**9-1,10**9+1)


def parameters(end):
    Q=PROFILES[end][0].denominator
    dyadic=Q & -Q
    for e,f,r,a in product(range(2),range(2),range(4),range(1,15)):
        if not greater_ratio(e,f,r,a) or (f>e and a%2):
            continue
        W=trace(e,0)*trace(f,r+1)-trace(e,1)*trace(f,r)
        assert 0<abs(W)<=1912
        for h in divisors(Q*a*abs(W)):
            if h%(4*dyadic)==0:
                continue
            for b in range(-10,3):
                if 2*b+e<2*r+f:
                    yield e,f,r,a,h,b


def small(p,k,end):
    L,lower=PROFILES[end]
    P,Q=L.as_integer_ratio()
    e,f,r,a,h,b=p
    j=k+b; ell=k+r
    if j<1 or ell<1:
        return False
    B,G,C=trace(e,k),trace(e,j),trace(f,ell)
    numerator=Q*(B+h*G)
    if numerator%P:
        return False
    m=numerator//P
    if m%lcm(4,end) or m%(a*(2 if f else 4)) or m%(h*(2 if e else 4)):
        return False
    if not any(m*(Q-z)>Q*a*C and (m*(Q-z)-Q*a*C)%(Q*h)==0 for z in range(Q-P,Q)):
        return False
    s=F(a*C,m)
    gaps=gap((e,k,m))+gap((e,j,m//h))+2*gap((f,ell,m//a))
    return gaps<=F(1,2) and (s>=lower or gaps+(F(1,2)-s)**2<=F(1,2))


def large(p,end):
    L,lower=PROFILES[end]
    e,f,r,a,h,b=p
    x=scale(u_power(b),h)
    ratio={-1:(2,-1),0:one,1:(1,F(1,2))}[f-e]
    y=scale(mul(ratio,u_power(r)),a)
    den=add(one,x)
    gaps=scale(add(add(one,sq(x)),scale(sq(y),2)),(ETA*L)**2)
    if positive(add(gaps,scale(sq(den),F(-1,2)))):
        return False
    if not positive(add(scale(den,lower*ETA),scale(y,-L))):
        return True
    deficit=add(scale(den,F(1,2)),scale(y,-L/ETA))
    assert positive(deficit)
    return not positive(add(add(gaps,sq(deficit)),scale(sq(den),F(-1,2))))


def period_length(p,end):
    e,f,r,a,h,b=p
    P,Q=PROFILES[end][0].as_integer_ratio()
    modulus=P*lcm(Q*h,Q,4*h,4*a)
    k=max(0,-b)
    indices=((e,k),(e,k+1),(e,k+b),(e,k+b+1),(f,k+r),(f,k+r+1))
    initial=tuple(trace(i,j)%modulus for i,j in indices)
    state=initial; period=0
    while True:
        B,B1,G,G1,C,C1=state
        numerator=Q*(B+h*G)
        if numerator%P==0:
            m=numerator//P
            if m%lcm(4,end)==0 and m%(h*(2 if e else 4))==0 and m%(a*(2 if f else 4))==0:
                assert all((m*(Q-z)-Q*a*C)%(Q*h) for z in range(Q-P,Q))
        state=(B1,(6*B1-B)%modulus,G1,(6*G1-G)%modulus,C1,(6*C1-C)%modulus)
        period+=1
        if state==initial:
            return period


if __name__=='__main__':
    for end in PROFILES:
        points=list(parameters(end))
        assert not any(small(p,k,end) for p in points for k in range(32))
        tail=[(p,period_length(p,end)) for p in points if large(p,end)]
        assert len(tail)==(2 if end==9 else 0)
        print((4,end),len(points),'parameter choices, no exact matches; residue periods',tail)
