#!/usr/bin/env python3
"""Trace lattices and exact small-trace enumeration in cyclic sextic fields.

The proof commands use --exact: rational LDL decomposition, integer square
roots and rational isolating intervals make every inclusion or rejection
exact.  The optional mode without that flag is exploratory only and labels
its output accordingly.  Floating embedding matrices built by field() are
diagnostic and are not used for any rejection in the exact enumeration.
"""
from functools import lru_cache
from itertools import product
from math import gcd, isqrt, sqrt, ceil, floor, cos, pi
from pathlib import Path
import json
import argparse
import numpy as np
import sympy as s


def egcd(a, b):
    if b == 0:
        return abs(a), (1 if a >= 0 else -1), 0
    g, x, y = egcd(b, a % b)
    return g, y, x - (a // b)*y


def trace_basis(t):
    U = s.eye(len(t)); r = list(t)
    for j in range(1, len(t)):
        a, b = r[0], r[j]
        if not b:
            continue
        g, x, y = egcd(a, b)
        P = s.eye(len(t))
        P[0,0], P[j,0], P[0,j], P[j,j] = x,y,-b//g,a//g
        U = U*P
        r[0],r[j]=g,0
    assert s.Matrix([t])*U == s.Matrix([[r[0]]+[0]*(len(t)-1)])
    assert abs(U.det()) == 1
    return U, r[0]


def cubic(b):
    if b == 9:
        one = np.array([1,0,0],dtype=np.int64)
        def mul(v,w):
            c = np.convolve(v,w).tolist()
            for k in range(4,2,-1):
                c[k-2] += 3*c[k]
                c[k-3] -= c[k]
            return np.array(c[:3],dtype=np.int64)
        roots=[2*cos(2*pi*j/9) for j in (1,2,4)]
        E=np.array([[1,x,x*x] for x in roots])
        G=np.array([[1,0,0],[0,0,-1],[0,1,-1]],dtype=np.int64)
        # Compute sigma(t)=t^2-2 instead of relying on the displayed seed.
        t=np.array([-2,0,1],dtype=np.int64)
        G=np.column_stack([one,t,mul(t,t)])
        return one,mul,E,G
    g=int(s.primitive_root(b))
    H={pow(g,3*k,b) for k in range((b-1)//3)}
    cosets=[{(pow(g,j,b)*h)%b for h in H} for j in range(3)]
    tensor=np.zeros((3,3,3),dtype=np.int64)
    for i,j in product(range(3),repeat=2):
        c=[0]*b
        for x,y in product(cosets[i],cosets[j]):c[(x+y)%b]+=1
        for k in range(3):
            vals={c[x] for x in cosets[k]};assert len(vals)==1
            tensor[i,j,k]=vals.pop()-c[0]
    one=-np.ones(3,dtype=np.int64)
    def mul(v,w):return np.einsum('i,j,ijk->k',v,w,tensor)
    periods=[sum(cos(2*pi*x/b) for x in h) for h in cosets]
    E=np.array([[periods[(i+j)%3] for j in range(3)] for i in range(3)])
    G=np.array([[int(i==(j+1)%3) for j in range(3)] for i in range(3)],dtype=np.int64)
    return one,mul,E,G


def overlap_field(a):
    assert a in (65,104)
    def bv(k):
        k%=13
        return -2*np.ones(6,dtype=np.int64) if k==0 else np.eye(6,dtype=np.int64)[min(k,13-k)-1]
    tensor=np.array([[bv(i+j+2)+bv(i-j) for j in range(6)] for i in range(6)])
    def mul13(v,w):return np.einsum('i,j,ijk->k',v,w,tensor)
    G13=np.column_stack([bv(2*j) for j in range(1,7)])
    tau=np.linalg.matrix_power(G13,3)
    E13=np.array([[2*cos(2*pi*(2**k)*j/13) for j in range(1,7)] for k in range(6)])
    if a==65:
        B=np.vstack([np.eye(6,dtype=np.int64),tau-np.eye(6,dtype=np.int64)])
        rows=list(range(6));trw=1;d=1;w=(1+sqrt(5))/2
    else:
        reps=[0,1,3]
        plus=np.column_stack([np.eye(6,dtype=np.int64)[:,j]+tau[:,j] for j in reps])
        minus=np.column_stack([np.eye(6,dtype=np.int64)[:,j]-tau[:,j] for j in reps])
        B=np.block([[plus,np.zeros((6,3),dtype=np.int64)],
                    [np.zeros((6,3),dtype=np.int64),minus]])
        rows=reps+[j+6 for j in reps];trw=0;d=2;w=sqrt(2)
    assert np.array_equal(B[rows,:],np.eye(6,dtype=np.int64))
    def extract(z):
        v=z[rows];assert np.array_equal(B@v,z);return v
    def mul(v,w):
        x=B@v;y=B@w;vv=mul13(x[6:],y[6:])
        z=np.r_[mul13(x[:6],y[:6])+d*vv,
                mul13(x[:6],y[6:])+mul13(x[6:],y[:6])+trw*vv]
        return extract(z)
    one=extract(np.r_[-np.ones(6,dtype=np.int64),np.zeros(6,dtype=np.int64)])
    E=np.column_stack([E13,w*E13])@B
    GG=np.block([[G13,np.zeros((6,6),dtype=np.int64)],
                 [np.zeros((6,6),dtype=np.int64),G13]])
    G=(GG@B)[rows,:]
    matrices=[np.column_stack([mul(np.eye(6,dtype=np.int64)[i],np.eye(6,dtype=np.int64)[j])
                               for j in range(6)]) for i in range(6)]
    t=np.array([int(np.trace(x)) for x in matrices],dtype=np.int64)
    Gram=np.array([[int(np.trace(x@y)) for y in matrices] for x in matrices],dtype=np.int64)
    assert s.Matrix(Gram).det()==a*13**2*a**2
    assert np.max(np.abs(E@G-E[np.r_[1:6,0]]))<1e-7
    return one,mul,E,G,matrices,t,Gram


def field(a,b):
    if gcd(a,b)!=1:
        assert b==13
        return overlap_field(a)
    one3,mul3,E3,G3=cubic(b)
    odd=a%4==1
    trw=1 if odd else 0
    d=(a-1)//4 if odd else a//4
    wplus=(1+sqrt(a))/2 if odd else sqrt(a//4)
    wminus=trw-wplus
    one=np.r_[one3,[0,0,0]]
    def mul(v,w):
        vv=mul3(v[3:],w[3:])
        return np.r_[mul3(v[:3],w[:3])+d*vv,
                     mul3(v[:3],w[3:])+mul3(v[3:],w[:3])+trw*vv]
    E=np.array([np.r_[E3[k%3],(wplus if k%2==0 else wminus)*E3[k%3]]
                for k in range(6)])
    G=np.block([[G3,trw*G3],[np.zeros((3,3),dtype=np.int64),-G3]])
    matrices=[np.column_stack([mul(np.eye(6,dtype=np.int64)[i],np.eye(6,dtype=np.int64)[j])
                               for j in range(6)]) for i in range(6)]
    t=np.array([int(np.trace(x)) for x in matrices],dtype=np.int64)
    Gram=np.array([[int(np.trace(x@y)) for y in matrices] for x in matrices],dtype=np.int64)
    assert s.Matrix(Gram).det()==a**3*b**4
    assert np.max(np.abs(E@G-E[np.r_[1:6,0]]))<1e-7
    assert np.allclose(E@one,np.ones(6))
    return one,mul,E,G,matrices,t,Gram


def ldl(A):
    n=len(A);L=np.eye(n);D=np.zeros(n)
    for i in range(n):
        D[i]=A[i,i]-sum(L[i,k]**2*D[k] for k in range(i))
        for j in range(i+1,n):
            L[j,i]=(A[j,i]-sum(L[j,k]*L[i,k]*D[k] for k in range(i)))/D[i]
    assert np.all(D>0)
    assert np.allclose(A,L@np.diag(D)@L.T)
    return L,D


def lattice_vectors(Gram, center, bound):
    L,D=ldl(Gram)
    n=len(center);z=np.zeros(n,dtype=np.int64);y=np.zeros(n)
    def rec(i,left):
        if i<0:
            yield z.copy();return
        shift=sum(L[j,i]*y[j] for j in range(i+1,n))
        c=center[i]-shift;radius=sqrt(max(left,0)/D[i])+1e-8
        for v in range(ceil(c-radius),floor(c+radius)+1):
            z[i]=v;y[i]=v-center[i]
            used=D[i]*(y[i]+shift)**2
            if used<=left+1e-7:yield from rec(i-1,left-used)
    yield from rec(n-1,bound)


def exact_lattice_vectors(Gram, center_numerators, A):
    """Enumerate Tr(alpha^2)<=A^2 at fixed trace A, with integer bounds."""
    from math import lcm
    L,D=s.Matrix(Gram).LDLdecomposition()
    denoms=[lcm(*[int(L[j,i].q) for j in range(i,5)]) for i in range(5)]
    numer=[[int(L[j,i]*denoms[i]) for j in range(5)] for i in range(5)]
    terms=[D[i,i]/(36*denoms[i]**2) for i in range(5)]
    scale=lcm(6,*[int(x.q) for x in terms]);weights=[int(scale*x) for x in terms]
    z=[0]*5;Y=[0]*5
    def rec(i,left):
        if i<0:
            yield np.array(z,dtype=np.int64);return
        shift=sum(numer[i][j]*Y[j] for j in range(i+1,5))-denoms[i]*int(center_numerators[i])
        step=6*denoms[i];radius=isqrt(left//weights[i])
        lower=-((radius+shift)//step)
        upper=(radius-shift)//step
        for v in range(lower,upper+1):
            z[i]=v;Y[i]=6*v-int(center_numerators[i])
            S=step*v+shift;cost=weights[i]*S*S
            assert cost<=left
            yield from rec(i-1,left-cost)
    yield from rec(4,scale*5*A*A//6)


def imul(x,y):
    v=[a*b for a in x for b in y];return min(v),max(v)


def iadd(x,y):return x[0]+y[0],x[1]+y[1]


def iscale(c,x):return (c*x[0],c*x[1]) if c>=0 else (c*x[1],c*x[0])


def polynomial_interval(coeffs,x):
    result=(s.Rational(0),s.Rational(0))
    for c in reversed(coeffs):result=iadd(imul(result,x),(c,c))
    return result


@lru_cache(None)
def embedding_bounds(a,b,scale=10**12):
    """Certified rational intervals for a cyclically ordered embedding matrix."""
    eps=s.Rational(1,10000*scale)
    if gcd(a,b)==1:
        one,mul,E,G3=cubic(b)
        gen=np.array([0,1,0] if b==9 else [1,0,0],dtype=np.int64)
        genmat=s.Matrix(np.column_stack([mul(gen,np.eye(3,dtype=np.int64)[j]) for j in range(3)]))
        poly=s.Poly(genmat.charpoly().as_expr())
        intervals=s.polys.polytools.intervals(poly,eps=eps)
        root=intervals[-1][0]
        powers=s.Matrix(np.column_stack([one,gen,mul(gen,gen)]))
        polys=powers.inv()
        row=[polynomial_interval(list(polys[:,j]),root) for j in range(3)]
        rows=[]
        for k in range(3):
            Gk=np.linalg.matrix_power(G3,k)
            rows.append([sum_intervals([iscale(int(Gk[i,j]),row[i]) for i in range(3)]) for j in range(3)])
        rad=a if a%4==1 else a//4
        z=isqrt(rad*(10000*scale)**2);sq=(s.Rational(z,10000*scale),s.Rational(z+1,10000*scale))
        if a%4==1:wp=iscale(s.Rational(1,2),iadd((1,1),sq));wm=iadd((1,1),iscale(-1,wp))
        else:wp=sq;wm=iscale(-1,wp)
        matrix=[rows[k%3]+[imul(wp if k%2==0 else wm,x) for x in rows[k%3]] for k in range(6)]
    else:
        assert b==13 and a in (65,104)
        x=s.Symbol('x');poly=s.Poly(x**6+x**5-5*x**4-4*x**3+6*x*x+3*x-1,x)
        root=s.polys.polytools.intervals(poly,eps=eps)[-1][0]
        polys=[[2],[0,1]]
        for j in range(2,7):
            prev=[0]+polys[-1];old=polys[-2]+[0]*(len(prev)-len(polys[-2]))
            polys.append([v-w for v,w in zip(prev,old)])
        vals=[polynomial_interval(p,root) for p in polys[1:]]
        index=lambda k:min(k%13,13-k%13)-1
        E13=[[vals[index((2**k)*j)] for j in range(1,7)] for k in range(6)]
        tau=[index(8*j) for j in range(1,7)]
        rad=5 if a==65 else 2;z=isqrt(rad*(10000*scale)**2)
        sq=(s.Rational(z,10000*scale),s.Rational(z+1,10000*scale))
        if a==65:
            w=iscale(s.Rational(1,2),iadd((1,1),sq));onew=iadd((1,1),iscale(-1,w))
            matrix=[[iadd(imul(onew,row[j]),imul(w,row[tau[j]])) for j in range(6)] for row in E13]
        else:
            reps=[0,1,3]
            matrix=[[iadd(row[j],row[tau[j]]) for j in reps]+[imul(sq,iadd(row[j],iscale(-1,row[tau[j]]))) for j in reps] for row in E13]
    lo=np.array([[int(s.floor(x[0]*scale)) for x in row] for row in matrix],dtype=np.int64)
    hi=np.array([[int(s.ceiling(x[1]*scale)) for x in row] for row in matrix],dtype=np.int64)
    assert np.all(lo<=hi)
    return lo,hi,scale


def sum_intervals(xs):
    out=(s.Rational(0),s.Rational(0))
    for x in xs:out=iadd(out,x)
    return out


def candidates(a,b,Amax,exact=False):
    one,mul,E,G,matrices,t,H=field(a,b)
    U,g=trace_basis(t.tolist());Ui=U.inv()
    U=np.array(U,dtype=np.int64);coords=np.array(Ui*s.Matrix(one.tolist()),dtype=np.int64).reshape(6)
    Hnew=U.T@H@U;H5=Hnew[1:,1:]
    if exact:
        ML,MU,scale=embedding_bounds(a,b)
        Hinv=s.Matrix(H).inv()
        coefbound=Amax*(1+int(s.ceiling(max(Hinv[i,i] for i in range(6)))))
        assert 6*coefbound*max(abs(int(x)) for x in MU.flat)<2**63
    pos=[];count=0
    for A in range(g,Amax+1,g):
        center=A*coords[1:]/6
        vectors=exact_lattice_vectors(H5,A*coords[1:],A) if exact else lattice_vectors(H5.astype(float),center,5*A*A/6+1e-8)
        for z in vectors:
            v=U@np.r_[A//g,z];count+=1
            if exact:
                vp=np.maximum(v,0);vn=np.minimum(v,0)
                lower=ML@vp+MU@vn;upper=MU@vp+ML@vn
                if min(upper)<=0 or min(lower)>scale:continue
                if np.array_equal(v,one):pass
                else:assert min(lower)>0 and min(upper)<scale,('Insufficient interval precision',a,b,v,lower,upper)
                emb=[]
            else:
                emb=E@v
                if min(emb)<1e-7 or min(emb)>1+1e-7:continue
            # Choose one representative of each Galois orbit, with its minimum
            # embedding in position 0; tie-break by lexicographic coordinates.
            orbit=[];vv=v.copy()
            for k in range(6):orbit.append(tuple(map(int,vv)));vv=G@vv
            if tuple(v)!=min(orbit):continue
            M=sum(int(c)*m for c,m in zip(v,matrices))
            norm=int(s.polys.matrices.DomainMatrix.from_Matrix(s.Matrix(M)).det())
            if norm<=0 or isqrt(norm)**2!=norm:continue
            poly=list(map(int,s.Matrix(M).charpoly().all_coeffs()))
            degree=len(set(orbit))
            x=s.Symbol('x');f=s.Poly.from_list(poly,x)
            minpoly=s.sqf_part(f)
            coeffs=list(map(int,minpoly.all_coeffs()))
            n=len(coeffs)-1;N=abs(coeffs[-1])
            if any(coeffs[i]**n % (N**i) for i in range(1,n+1)):continue
            pos.append(dict(coefficients=list(map(int,v)),trace=A,norm=norm,
                            degree=degree,minpoly=coeffs,embeddings=list(map(float,emb))))
        print(f'field({a},{b}) trace {A}: {len(pos)} cumulative square-norm d-numbers; {count} lattice vectors',flush=True)
    return dict(a=a,b=b,Amax=Amax,lattice_vectors=count,candidates=pos,
                status='EXACT_INTEGER_ENUMERATION' if exact else 'EXPLORATORY_FLOAT_ENUMERATION_NOT_A_CERTIFICATE')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('a',type=int);p.add_argument('b',type=int);p.add_argument('bound',type=int)
    p.add_argument('--exact',action='store_true')
    args=p.parse_args();data=candidates(args.a,args.b,args.bound,exact=args.exact)
    path=Path(__file__).with_name(f'sextic_{args.a}_{args.b}_'+('exact' if args.exact else 'exploratory')+'.json')
    path.write_text(json.dumps(data,indent=2)+'\n')
    print('Saved',path)
