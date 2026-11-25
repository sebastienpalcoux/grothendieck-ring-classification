"""Exact trace and norm test for a quadratic E in a quartic character field."""
from math import isqrt
from fractions import Fraction

def positive(a,b,d):
    """The sign of a+b sqrt(d) is positive (d is positive and nonsquare)."""
    if not b:return a>0
    if b>0:return a>=0 or d*b*b>a*a
    return a>0 and a*a>d*b*b

def fundamental(trace):
    delta=trace*trace-4
    for v in range(isqrt(delta),0,-1):
        if delta%(v*v)==0 and (delta//(v*v))%4 in (0,1):
            return delta//(v*v),v
    raise AssertionError

def check():
    counts=[0,0,0,0]
    for t in range(3,25):
        d,beta=fundamental(t)
        for a in range(5,50):
            c=(a-4)*(t+2)
            if c%(d*beta):continue
            b=c//(d*beta)
            ns4=a*a-d*b*b
            if ns4<=0 or ns4%4:continue
            ns=ns4//4
            if (2*a-ns)%4:continue
            for m in range(1,(a*a-2*ns)//4+1):
                hi=isqrt(m*m//d)
                for n in range(-hi,hi+1):
                    z4=m*m-d*n*n
                    if z4<=0 or z4%4:continue
                    z=z4//4
                    if (16*(t+2))**2%z:continue
                    c2=m+ns; c3num=a*m-d*b*n
                    if c3num%2:continue
                    c3=c3num//2
                    if a**4%z or c2**4%z**2 or c3**4%z**3:continue
                    counts[0]+=1
                    # Four times each relative quadratic discriminant.
                    dx=a*a+d*b*b-8*m
                    dy=2*a*b-8*n
                    if not positive(dx,dy,d) or not positive(dx,-dy,d):continue
                    counts[1]+=1
                    k=Fraction(m,2)-Fraction(d*beta*n,2*(t+2))
                    if k.denominator!=1 or k<=0 or k.numerator%2==0:continue
                    counts[2]+=1
                    nd=ns**2-4*(a*c3-ns*m)+16*z
                    if isqrt(nd)**2!=nd and isqrt(d*nd)**2!=d*nd:continue
                    counts[3]+=1
                    # Evaluate both polynomials at 1/2, then use the vertex.
                    xa=1-a+2*m;xb=2*n-b
                    assert positive(a-2,b,d) and positive(xa,xb,d)
                    assert positive(2-a,b,d) or positive(-xa,xb,d)
    assert counts==[526,32,14,10],counts
    print('d-number tests, real roots, odd moment, Galois tests:',*counts)
    print('all physical minima excluded')

if __name__=='__main__':check()
