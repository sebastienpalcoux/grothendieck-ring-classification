"""Exact signed and ordinary row tests for rational E and two rational codegrees."""
from collections import Counter
from fractions import Fraction as Q
from functools import cache
from itertools import combinations_with_replacement, permutations, product
from math import isqrt, lcm
from golden_orbit_check import add, divisors, greater, mul, one, power_u, scale, sign, trace_seq as B, v


def conj(x):
    return (x[0]+x[1], -x[1])


def tr(x, f):
    a,b=x; c,d=f
    return Q((2*c+d)*a+(c-2*d)*b, c*c+c*d-d*d)


def parameters(m):
    for f in (0,1):
        for j in range(1,5):
            for n in divisors(m):
                if (f and m%(5*n)) or (not f and n%5):
                    continue
                mass=Q(B(f,j),n)
                gap=mass**2-Q(4,5**f*n*n)
                if mass<1 and gap<=Q(1,5):
                    yield f,j,n,mass,gap,scale(mul(power_u(j),v if f else one),n)


def column_possible(m,f,j,n,a,b,s,dgap):
    q=lcm(a,b)
    for Z in range(q//a+q//b,q):
        t=n*(1-Q(Z,q)-s)
        if t<=0 or t.denominator!=1:
            continue
        t=int(t)
        for y in range(-2*t,2*t+1):
            if not f and (t-y)%2:
                continue
            x=t if f else (t-y)//2
            norm=x*x+x*y-y*y
            if norm>0 and t*t-Q(4*norm,5**f)<=n*n*(Q(1,5)-dgap):
                return True
    return False


def profiles():
    for m in range(5,61,5):
        data=list(parameters(m))
        for f,j,n,w,_,H in data:
            rem=1-Q(2,m)-w
            for a in divisors(m):
                if a<3 or rem<=Q(1,a):
                    continue
                b=1/(rem-Q(1,a))
                if b.denominator!=1 or b<a or m%b:
                    continue
                b=int(b)
                if a==b:
                    if a==3 or (f and (2*a)%5):
                        continue
                else:
                    sf=a*b*5**f
                    if isqrt(sf)**2!=sf or (a==3 and (a+b)%9):
                        continue
                for d,l,M,s,dgap,D in data:
                    if not greater(D,(m,0)) or D==H or 2*l+d<2*j+f or s<Q(3,m):
                        continue
                    if column_possible(m,f,j,n,a,b,s,dgap):
                        yield m,H,a,b,D


@cache
def shell(k,n):
    if n<0:
        return []
    if k==0:
        return [()] if n==0 else []
    return [(x,*v) for x in range(-isqrt(n),isqrt(n)+1) for v in shell(k-1,n-x*x)]


def dot(x,y):
    return sum(a*b for a,b in zip(x,y))


@cache
def signed_h_rows(codegree):
    c,d=codegree
    bnorm=(2*c+d)//5
    avecs=[(1,*r) for r in shell(5,c-bnorm-1) if min(r)>=0 and tuple(sorted(r))==r]
    bvecs=[(0,*r) for r in shell(5,bnorm)]
    hs=set()
    for A,Bv in product(avecs,bvecs):
        if 2*dot(A,Bv)!=d-bnorm or any(y<0 and x==0 for x,y in zip(A,Bv)):
            continue
        hs.add(((1,0),*sorted(zip(A[1:],Bv[1:]))))
    return sorted(hs)


def signed_x_rows(m,H):
    C,D=zip(*H)
    def orthogonal(rows):
        return [r for r in rows if dot(r,C)==dot(r,D)==0]
    avecs=orthogonal((1,*v) for v in shell(5,3*m//5-1))
    bvecs=orthogonal((0,*v) for v in shell(5,2*m//5))
    xs=set()
    for A,Bv in product(avecs,bvecs):
        if dot(A,Bv)!=-m//5 or any(x==y==0 for x,y in zip(A,Bv)):
            continue
        pairs=[]
        for h,x in zip(H[1:],zip(A[1:],Bv[1:])):
            if h==(0,0) and next(t for t in x if t)<0:
                x=scale(x,-1)
            pairs.append((h,x))
        xs.add(((1,0),*(y for _,y in sorted(pairs))))
    return sorted(xs)


I=range(6)

def remaining_rows(a,b,p,P,X,H):
    if a==b:
        C=[a*x/2 for x in p]
        K=[[a*P[i][j]/2-C[i]*C[j] for j in I] for i in I]
        if any((2*x).denominator!=1 for x in C):
            return
        for eps in (1,-1):
            if any((C[i]**2-eps*K[i][i]).denominator!=1 for i in I):
                continue
            yield lambda i,j,k: Q(2,a)*(C[i]*C[j]*C[k]+C[i]*K[j][k]+C[j]*K[i][k]+eps*C[k]*K[i][j])
    else:
        blocks=(*zip(*X),*zip(*H))
        for r0 in shell(5,a-1):
            r=(1,*r0)
            if any(dot(r,z) for z in blocks):
                continue
            s=[b*(p[i]-Q(r[i],a)) for i in I]
            if any(x.denominator!=1 for x in s):
                continue
            yield lambda i,j,k: Q(r[i]*r[j]*r[k],a)+s[i]*s[j]*s[k]/b


@cache
def tables(m,G,a,b):
    found=[]
    for H in signed_h_rows(G):
        for X in signed_x_rows(m,H):
            def partial(ix):
                x=h=one
                for i in ix:
                    x=mul(x,X[i]); h=mul(h,H[i])
                return tr(x,(m,0))+tr(h,G)
            p=[(i==0)-partial((i,)) for i in I]
            P=[[(i==j)-partial((i,j)) for j in I] for i in I]
            triples={ix:partial(ix) for ix in combinations_with_replacement(I,3)}
            for contribution in remaining_rows(a,b,p,P,X,H):
                N=[[[triples[tuple(sorted((i,j,k)))]+contribution(i,j,k) for k in I] for j in I] for i in I]
                if all(x.denominator==1 for row in N for col in row for x in col):
                    found.append((X,H,[[[int(x) for x in col] for col in row] for row in N]))
    return found


@cache
def ordinary_rows(D):
    c,d=D; bs=(2*c+d)//5; asq=c-bs; mixed=(d-bs)//2
    choices=[]
    for b in range(isqrt(bs)+1):
        for a in range(-isqrt(asq),isqrt(asq)+1):
            z=(a,b)
            if greater(one,z) or 2*a+b<0 or greater(mul(conj(z),conj(z)),add(conj(D),(-1,0))):
                continue
            choices.append(z)
    @cache
    def extend(k,off,x,y,z):
        if min(x,y)<0 or z*z>x*y:
            return []
        if k==0:
            return [()] if x==y==z==0 else []
        return [(t,*r) for j,t in enumerate(choices[off:],off) for r in extend(k-1,j,x-t[0]**2,y-t[1]**2,z-t[0]*t[1])]
    return extend(5,0,asq-1,bs,mixed)


def match(X,H,N,fp):
    for x,h,d in zip(X,H,fp):
        for z in (x,h,conj(x),conj(h)):
            if greater(z,d) or greater(scale(z,-1),d):
                return False
    @cache
    def cone(k,x,y):
        if x==y==0:
            return True
        if k==6 or y<0 or sign((x,y))<0:
            return False
        # Every ordinary nonunit dimension is at least one. Here 0 <= y and phi < 2.
        a,b=fp[k]
        cap=x+2*y if b==0 else min(x+2*y,y//b)
        return any(cone(k+1,x-n*a,y-n*b) for n in range(cap+1))
    for i,j in combinations_with_replacement(range(1,6),2):
        r,s=mul(fp[i],fp[j])
        for t,(a,b) in zip(N[i][j],fp):
            r-=abs(t)*a; s-=abs(t)*b
        if r%2 or s%2 or not cone(1,r//2,s//2):
            return False
    return True


if __name__=='__main__':
    cases=list(profiles())
    assert len(cases)==7
    for m,G,a,b,D in cases:
        tabs=tables(m,G,a,b)
        survivors=set()
        for X,H,N in tabs:
            for u in ordinary_rows(D):
                for r in set(permutations(u)):
                    fp=(one,*r)
                    if match(X,H,N,fp):
                        survivors.add((X,H,fp))
        print((m,G,a,b,D), 'signed tables',len(tabs),'ordinary multisets',len(ordinary_rows(D)),'matches',len(survivors),flush=True)
        for s in sorted(survivors):
            print(s)
