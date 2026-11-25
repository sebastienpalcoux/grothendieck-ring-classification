"""Check the trace-39 enumeration and all seven moment exclusions exactly."""
from fractions import Fraction as Q
from itertools import product
from math import isqrt

BIQUADRATIC = [(8,60,120), (8,76,152), (8,21,168), (8,92,184),
               (8,29,232), (8,33,264), (8,37,296), (8,41,328)]
SCALE = 10**16


def admissible(a, b, c, n):
    if min(b, c, n) <= 0 or a % 2 or b % 2 or c % 2 or not n % 2:
        return False
    if min(b-3*a+6, c-2*b+3*a-4, n-c+b-a+1) > 0:
        return False
    return a**4 % n == b**4 % n**2 == c**4 % n**3 == 0


def candidate_polynomials():
    rows = {}
    for d, e, f in BIQUADRATIC:
        k = isqrt(d*e*f)
        assert k*k == d*e*f
        for a in range(6, 40, 2):
            bounds = [isqrt((a*a-1)//r) for r in (d,e,f)]
            for u,v,w in product(*(range(-t,t+1) for t in bounds)):
                if (u!=0)+(v!=0)+(w!=0)<2:
                    continue
                x,y,z = d*u*u,e*v*v,f*w*w
                s,t = x+y+z,k*u*v*w
                b8=3*a*a-s
                c16=a**3-a*s+2*t
                n256=(a**4-2*a*a*s+8*a*t+s*s-4*(x*y+x*z+y*z))
                if b8%8 or c16%16 or n256%256:
                    continue
                poly=(a,b8//8,c16//16,n256//256)
                if admissible(*poly):
                    rows[poly]='biquadratic'
    for m in (5,7):
        for t in range(2,10):
            a=4*t
            v_bound=isqrt((a*a-1)//(8*m))
            s_bound=isqrt((a*a-1)//8)
            for s,v,w in product(range(-s_bound,s_bound+1),
                                 range(-v_bound,v_bound+1),
                                 range(-v_bound,v_bound+1)):
                if not (v or w):
                    continue
                h=v*v+w*w
                g=v*v-w*w+2*v*w
                b=6*t*t-4*s*s-4*m*h
                c=4*t**3-8*t*s*s-8*t*m*h+8*m*s*g
                n=(t*t+2*s*s-2*m*h)**2-2*(2*t*s-m*g)**2
                if admissible(a,b,c,n):
                    rows[a,b,c,n]='cyclic'
    return rows


def mul(i,j):
    v=[a*b for a in i for b in j]
    return min(v),max(v)


def add(i,j):
    return i[0]+j[0],i[1]+j[1]


def eval_interval(coeff, x):
    i=(0,0)
    for b in coeff:
        i=add(mul(i,x),(b,b))
    return i


def roots(poly):
    a,b,c,n=poly
    def at(x):
        return (((x-a)*x+b)*x-c)*x+n
    grid=1
    while True:
        lo=Q(0); val=at(lo); out=[]
        for k in range(1,grid*a+1):
            hi=Q(k,grid); new=at(hi)
            assert new
            if new*val<0:
                out.append((lo,hi))
            lo,val=hi,new
        if len(out)==4:
            break
        grid*=2
    for lo,hi in out:
        sign=at(lo)>0
        for _ in range(95):
            mid=(lo+hi)/2
            if (at(mid)>0)==sign:
                lo=mid
            else:
                hi=mid
        yield lo,hi


def scaled(i):
    lo,hi=i
    return (lo*SCALE).__floor__(), (hi*SCALE).__ceil__()


def odd_in(lo,hi):
    k=-(-lo//(SCALE*SCALE))
    k += (k+1)%2
    return k*SCALE*SCALE<=hi


def moments(poly, kind, weight_cap=None, golden_unit=False):
    a,b,c,n=poly
    root=list(roots(poly))
    x=[scaled(r) for r in root]
    coeff=[]
    for r in root:
        p=eval_interval([4,-3*a,2*b,-c],r)
        assert p[0]*p[1]>0
        inv=(1/p[1],1/p[0])
        coeff.append([scaled(mul(eval_interval(col,r),inv)) for col in
                      ([1,1-a,b-a,b-c],[1,-a],[1])])
    survivors=[0,0,0]
    for m in range(2 if golden_unit else 3,a,2):
        for h in range(m*m+(1 if golden_unit else 0),a*m,2):
            q=[(v0[0]+m*v1[0]+h*v2[0],v0[1]+m*v1[1]+h*v2[1])
               for v0,v1,v2 in coeff]
            if any(i[1]<=0 for i in q):
                continue
            survivors[0]+=1
            if any(q[0][0]>i[1] for i in q):
                continue
            survivors[1]+=1
            if weight_cap is not None and any(lo>SCALE*weight_cap for lo,_ in q):
                continue
            if kind=='biquadratic':
                passes=True
                for perm in ((1,0,3,2),(2,3,0,1),(3,2,1,0)):
                    v=[mul(q[i],x[j]) for i,j in enumerate(perm)]
                    low=sum(k[0] for k in v); high=sum(k[1] for k in v)
                    if golden_unit:
                        # Intersect all integer translates in either parity.
                        feasible=-(-low//(SCALE*SCALE))*(SCALE*SCALE)<=high
                    else:
                        feasible=odd_in(low,high)
                    if not feasible:
                        passes=False
                        break
                if not passes:
                    continue
            survivors[2]+=1
    return tuple(survivors)


if __name__=='__main__':
    polys=candidate_polynomials()
    expected={
        (20,80,100,25):(7,0,0), (24,90,72,9):(68,0,0),
        (36,270,468,9):(260,0,0), (24,170,312,1):(21,0,0),
        (20,56,20,1):(31,1,0), (28,238,588,49):(24,0,0),
        (28,166,28,1):(25,0,0)}
    assert set(polys)==set(expected)
    for p,kind in sorted(polys.items()):
        result=moments(p,kind)
        assert result==expected[p]
        print(p,kind,result)
