"""Check ordinary quadratic-pair enumeration and rational tangent caps."""
from fractions import Fraction as F
from math import isqrt,gcd
from two_nonhalf import FIELDS,CYCLIC

SCALE=10**14
def root(v):
    v=F(v); u=isqrt(v.numerator*SCALE*SCALE//v.denominator)
    return F(u,SCALE),F(u+1,SCALE)

def check():
    conductors=set(x for r in FIELDS for x in r[:3])
    found=set()
    for c in conductors:
        for N in range(1,257):
            for L in range(2*c,N+1,c):
                disc=L*L-4*N
                if 3*N>8*L or 2*L>N or L*L%N or disc<=0 or disc%c or c*disc>N*N:continue
                if isqrt(disc//c)**2==disc//c:found.add((c,L,N))
    assert found=={(8,16,32),(8,96,256)}
    for cs,cap in [(r[:3],r[-1]) for r in FIELDS]+[(r[:2],r[-1]) for r in CYCLIC]:
        if len(cs)==3:
            B=sum(root(F(gcd(c,2),c))[1] for c in cs[1:])
            small=[root(F(gcd(c,4),c))[1] for c in cs[1:]]
        else:
            B=2*root(F(2,cs[1]))[1];small=[root(F(8,cs[1]))[1]]
        tmin=F(23,36) if cs==(8,28,56) else F(5,8)
        for s,t in [(F(5,8),tmin),(F(1,2),F(5,7))]:
            r=s-B
            # Choose rational r using an upper bound on B, hence every
            # subsequent denominator and numerator inequality is outward.
            sl,su=root(8)
            assert r>0 and su*t-16*r*B-8*r*r-2<0
            y=(sl*t+8*r*r-2)/(2*su+32*r)
            assert y>0
            ups=[1+2*s/y]+[1+4*t/(t-x) for x in small]
            assert all(x<cap+1 for x in ups),(cs,s,t,cap,ups)

if __name__=='__main__':check()
