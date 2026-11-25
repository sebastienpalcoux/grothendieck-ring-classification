"""Exact arithmetic for the two irrational conductor-five codegree pairs theorem."""
from fractions import Fraction as Q
from functools import cache
from math import lcm
from golden_orbit_check import add, divisors, greater, mul, one, power_u, scale, trace_seq as B, v


@cache
def gap_numerator(e, i):
    return 5**e * B(e, i)**2 - 4


def direct():
    """Signed survivors for E < 1000 and rational complementary mass <= 9/25."""
    survivors = []
    for e in (0, 1):
        for k in range(8):
            if not e and not k:
                continue
            for m in range(1, 1000):
                if (not e and m%5) or B(e,k) >= m:
                    continue
                if not greater((1000,0), scale(mul(power_u(k), v if e else one), m)):
                    continue
                for f in (0,1):
                    for j in range(1,8):
                        for n in divisors(m):
                            if (f>e and m%(5*n)) or (not f and n%5):
                                continue
                            gap = Q(gap_numerator(e,k), 5**e*m*m) + Q(gap_numerator(f,j), 5**f*n*n)
                            if gap > Q(1,5):
                                continue
                            rem = 1 - Q(B(e,k),m) - Q(B(f,j),n)
                            if not 0 < rem <= Q(9,25):
                                continue
                            for a in divisors(m):
                                if a<3 or rem<=Q(1,a):
                                    continue
                                b=1/(rem-Q(1,a))
                                if b.denominator==1 and b>=a and m%b==0:
                                    survivors.append((e,k,m,f,j,n,a,int(b)))
    return survivors


@cache
def unit_ratio(index, family_shift, reciprocal=False):
    # P_{d,l}/P_{e,k}, or the ratio of leading coefficients in their reciprocal traces.
    factors = {-1:(Q(3,5),Q(-1,5)), 0:one, 1:v}
    if reciprocal:
        factors = {-1:(3,-1), 0:one, 1:scale(v,Q(1,5))}
    return mul(factors[family_shift], power_u(index))


def tuples(a,b):
    q=lcm(a,b)
    for e in (0,1):
        for f in (0,1):
            if (a,b)!=(5,5) and (e+f)%2 != int((a,b) in ((3,15),(4,5))):
                continue
            for d in (0,1):
                for r in range(-1,7):
                    W=B(e,0)*B(d,r+1)-B(e,1)*B(d,r)
                    for c in range(1,14):
                        if not greater(unit_ratio(r,d-e),(c,0)) or (d>e and c%5):
                            continue
                        assert 0<abs(W)<=720
                        for h in divisors(q*c*abs(W)):
                            if f>e and h%5:
                                continue
                            for z in range(-15,5):
                                if 2*z+f<=2*r+d and (f,z,h)!=(d,r,c):
                                    yield e,f,d,r,c,h,z


def scalar_conditions(e,f,d,m,h,c,q):
    return (m%q==0 and m%h==0 and m%c==0 and (e or m%5==0)
            and (f or m%(5*h)==0) and (d or m%(5*c)==0))


def small(a,b,L,p,k):
    e,f,d,r,c,h,z=p
    j,l=k+z,k+r
    if j<1 or l<1 or 2*k+e<1:
        return False
    q=lcm(a,b)
    be,bf,bd=B(e,k),B(f,j),B(d,l)
    mq=(be+h*bf)*L.denominator
    if mq%L.numerator:
        return False
    m=mq//L.numerator
    if not scalar_conditions(e,f,d,m,h,c,q):
        return False
    if 5*(gap_numerator(e,k)*5**f + gap_numerator(f,j)*5**e*h*h)>m*m*5**(e+f):
        return False
    if 5*gap_numerator(d,l)*c*c>m*m*5**d:
        return False
    for Z in range(q//a+q//b,q):
        residual=m*(q-Z)-q*c*bd
        if residual>0 and residual%(q*h)==0:
            return True
    return False


@cache
def asymptotic_ratios(p):
    e,f,d,r,c,h,z=p
    x=scale(unit_ratio(z,f-e,True),h)
    y=scale(unit_ratio(r,d-e,True),c)
    return x,y,add(one,x)


eta=Q(999999,1000000)

def tail(L,p):
    x,y,denom=asymptotic_ratios(p)
    g=5*(eta*L)**2
    right=mul(denom,denom)
    return (not greater(scale(add(one,mul(x,x)),g),right)
            and not greater(scale(mul(y,y),g),right))


def periodic(a,b,L,p):
    e,f,d,r,c,h,z=p
    q=lcm(a,b)
    _,y,denom=asymptotic_ratios(p)
    zs=[Z for Z in range(q//a+q//b,q) if greater(scale(denom,1-Q(Z,q)),scale(y,eta*L))]
    mod=L.numerator*lcm(q*h,5*h,5*c,q)
    initial=tuple(B(g,i)%mod for g,i in ((e,0),(e,1),(f,z),(f,z+1),(d,r),(d,r+1)))
    st=initial
    period=0
    while True:
        be,b1,bf,f1,bd,d1=st
        mq=(be+h*bf)*L.denominator
        if mq%L.numerator==0:
            m=mq//L.numerator
            if scalar_conditions(e,f,d,m,h,c,q):
                assert all((m*(q-Z)-q*c*bd)%(q*h) for Z in zs)
        period+=1
        st=(b1,(3*b1-be)%mod,f1,(3*f1-bf)%mod,d1,(3*d1-bd)%mod)
        if st==initial:
            return period


if __name__=='__main__':
    print('Small intrinsic dimensions:', direct(), flush=True)
    assert greater(power_u(42),(10**9,0))
    for a,b in ((3,15),(4,4),(4,5),(4,9),(5,5)):
        L=1-Q(1,a)-Q(1,b)
        ps=list(tuples(a,b))
        finite=sum(small(a,b,L,p,k) for p in ps for k in range(36))
        candidates=[p for p in ps if tail(L,p)]
        periods=[periodic(a,b,L,p) for p in candidates]
        assert not finite
        print((a,b),'tuples',len(ps),'small',finite,'tail',len(candidates),'maximum period',max(periods,default=0),flush=True)
        asymptotic_ratios.cache_clear()
