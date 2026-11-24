"""Exact biquadratic ratio census. Requires only the Python standard library."""

if not __debug__:
    raise RuntimeError("Run this verifier with Python assertions enabled")

from collections import Counter
from fractions import Fraction as Q
from functools import cache
from math import gcd, isqrt, prod

H = ((1,1,1,1), (1,1,-1,-1), (1,-1,1,-1), (1,-1,-1,1))
SCALE = 10**8


@cache
def sqrt_bounds(x):
    x = Q(x)
    low = isqrt(x.numerator*SCALE**2//x.denominator)
    return Q(low,SCALE), Q(low+1,SCALE)


def fold_interval(interval, factor):
    a,b = (x*factor for x in interval)
    return min(a,b), max(a,b)


def transform(intervals):
    result = []
    for signs in H:
        terms = [fold_interval(a,b) for a,b in zip(intervals,signs)]
        result.append(tuple(map(sum,zip(*terms))))
    return result


def squarefree(n):
    return all(n%(p*p) for p in range(2,isqrt(n)+1))


def conductor(n):
    return n if n%4==1 else 4*n


def fields():
    combinations = set()
    for a in range(2,40):
        if not squarefree(a) or conductor(a)>=40:
            continue
        for b in range(2,729):
            if a==b or not squarefree(b) or conductor(b)>=729:
                continue
            c=a*b//gcd(a,b)**2
            ds=tuple(sorted(map(conductor,(a,b,c))))
            if ds[0]<40 and ds[1]<729:
                combinations.add(ds)
    return sorted(combinations)


@cache
def minimum_maximum(ds, g):
    # Upper bound on (g disc K)^(-1/4).
    return sqrt_bounds(1/sqrt_bounds(g*prod(ds))[0])[1]


@cache
def fourier_max(c):
    return sqrt_bounds(Q(gcd(c,4),c))[1]


def survives_field_test(ds):
    m=minimum_maximum(ds,4)
    if (Q(3,4)-sum(map(fourier_max,ds)))/4>m:
        return False
    lhs=sqrt_bounds(3)[0]*(Q(3,4)-4*m)
    rhs=sum(2/sqrt_bounds(c)[0] for c in ds)
    return lhs<=rhs


@cache
def nonminimum_lower(ds,g):
    # For the pair 0,i selected by the kernel of a quadratic character,
    # q0+qi >= (t-B)/2 and q0 <= min(qi,(g disc K)^(-1/4)).
    t=1-Q(1,g)
    return min(max((t-fourier_max(c))/4,
                   (t-fourier_max(c))/2-minimum_maximum(ds,g))
               for c in ds)


def norms(A,u,v,w,mixed):
    e2, r2=divmod(6*A*A-2*(u+v+w),16)
    e3, r3=divmod(4*A**3-4*A*(u+v+w)+8*mixed,64)
    e4, r4=divmod(A**4-2*A*A*(u+v+w)+8*A*mixed+u*u+v*v+w*w-2*(u*v+v*w+u*w),256)
    if r2 or r3 or r4 or min(e2,e3,e4)<=0:
        return None
    if any(coefficient**4 % e4**j for j,coefficient in enumerate((1,A,e2,e3,e4))):
        return None
    return e2,e3,e4


def integer_pairs(A,coefficients,ds):
    e2,e3,e4=coefficients
    for r in range(1,A//4+1):
        n=gcd(A-4*r,e2-6*r*r,e3-4*r**3,e4-r**4)
        assert n!=0  # The polynomial of a primitive generator is not (X-r)^4.
        for g in range(4*r,n+1,r):
            if n%g:
                continue
            f=g//r
            if (A-1)*nonminimum_lower(ds,g) < 1-Q(1,f):
                yield f,g


def ratio_candidates(ds):
    roots=[d if d%4 else d//4 for d in ds]
    a,b,c=roots
    aprime=isqrt(a*b*c)
    assert aprime**2==a*b*c
    max_A=(1+1/nonminimum_lower(ds,4)).__floor__()
    results=set()
    for A in range(5,max_A+1):
        for i in range(isqrt((A*A-1)//a)+1):
            for j in range(isqrt((A*A-1)//b)+1):
                max_z=isqrt((A*A-1)//c)
                for z in range(-max_z,max_z+1):
                    if sum(bool(x) for x in (i,j,z))<2:
                        continue
                    es=norms(A,i*i*a,j*j*b,z*z*c,i*j*z*aprime)
                    if es is None:
                        continue
                    # All roots of the explicit radical polynomial are real.
                    # The alternating signs already imply they are positive.
                    pairs=list(integer_pairs(A,es,ds))
                    if not pairs:
                        continue
                    coeff=[(Q(A),Q(A))]+[fold_interval(sqrt_bounds(r),t)
                             for t,r in zip((i,j,z),roots)]
                    vals=transform(coeff)  # four times the embeddings of alpha
                    low=min(v[0] for v in vals)
                    high=min(v[1] for v in vals)
                    if low>=4:
                        continue
                    assert high<4
                    results.update((A,i,j,z,f,g) for f,g in pairs)
    return sorted(results)


def verify_moments(ds, candidate):
    A,i,j,z,f,g=candidate
    t=1-Q(1,g)
    s=1-Q(1,f)
    roots=[d if d%4 else d//4 for d in ds]
    a_hat=[(Q(A),Q(A))]+[fold_interval(sqrt_bounds(d),w)
                            for d,w in zip(roots,(i,j,z))]
    vals=transform(a_hat)
    index=min(range(4),key=lambda k:vals[k][1])
    assert all(vals[index][1]<vals[j][0] for j in range(4) if j!=index)
    a_hat=[fold_interval(v,sign) for v,sign in zip(a_hat,H[index])]
    alpha=[fold_interval(v,Q(1,4)) for v in transform(a_hat)]
    N=t*A-4*s
    assert N.denominator==1 and N>=0
    N=int(N)
    for n1 in range(N+1):
        for n2 in range(N-n1+1):
            n=(0,n1,n2,N-n1-n2)
            nh=[sum(u*v for u,v in zip(row,n)) for row in H]
            qh=[(t,t)]
            bad=False
            for j in range(1,4):
                # nh[j] = qhat[j] * alphahat[j]; Fourier bound, squared.
                v=(i,candidate[2],z)[j-1]
                m=v*v*roots[j-1]
                if nh[j]**2*ds[j-1] > m*gcd(ds[j-1],4):
                    bad=True
                    break
                if v:
                    a,b=a_hat[j]
                    u0,u1=Q(nh[j])/a,Q(nh[j])/b
                    qh.append((min(u0,u1),max(u0,u1)))
                else:
                    qh.append(None)
            if bad:
                continue
            assert None not in qh  # Checked exhaustively after the Fourier bound.
            q=[fold_interval(v,Q(1,4)) for v in transform(qh)]
            if min(b for a,b in q)<=0 or any(q[0][0]>b for a,b in q):
                continue
            p=[(al*max(0,ql),au*qu) for (al,au),(ql,qu) in zip(alpha,q)]
            if any(p[0][0]>b for a,b in p):
                continue
            ph=transform(p)
            def min_abs(ab):
                return max(0,ab[0],-ab[1])
            if any(min_abs(ph[j])**2*ds[j-1]>gcd(ds[j-1],4)
                   or (2*min_abs(ph[j])**2+min_abs(qh[j])**2)*ds[j-1]>4
                   for j in range(1,4)):
                continue
            raise AssertionError(('unresolved',ds,candidate,n))


def main():
    full=fields()
    retained=[ds for ds in full if survives_field_test(ds)]
    print('Biquadratic fields:',len(full),'after Fourier norm bounds:',len(retained))
    counts={}
    for ds in retained:
        rows=ratio_candidates(ds)
        for candidate in rows:
            verify_moments(ds,candidate)
        if rows:
            counts[ds]=len(rows)
    print('Ratio candidates by conductor triple:',counts)
    assert (len(full),len(retained))==(2097,52)
    assert counts=={(5,8,40):6,(8,12,24):12,(8,17,136):1,(8,21,168):2,
                    (8,28,56):4,(8,60,120):5}
    print('All 30 candidates fail the integral-moment Fourier tests.')


if __name__=='__main__':
    main()
