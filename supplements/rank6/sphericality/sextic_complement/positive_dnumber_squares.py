#!/usr/bin/env python3
"""Exact square-lattice enumeration of small-trace positive d-numbers.

For K=Q(sqrt(a))*K_b, a=5 or8 and b=7,9,13, explicit
units certify full signature rank. Thus every totally positive unit is a
square. Galois-invariant ideals and square norms then give
alpha=n*delta^r*u^2, n>=1, r=0,1,2, with u an algebraic integer unit.
Here delta=2-2cos(2pi/b) for b=7,9; for b=13 its cubic-period
coordinates are (-3,-6,-4).  Its cubic norm is the ramified prime.
"""
from pathlib import Path
from math import lcm,isqrt
from itertools import product
import json,sys,time
import numpy as np
import sympy as s
from sextic_lattice import field,cubic,embedding_bounds


def norm_evaluator(a,b):
    one,mul,E,G=cubic(b)
    tensor=np.array([[mul(np.eye(3,dtype=np.int64)[i],np.eye(3,dtype=np.int64)[j]) for j in range(3)] for i in range(3)])
    trw=1 if a%4==1 else 0;d=(a-1)//4 if trw else a//4
    def norm(vs):
        # Prove every fixed-width intermediate safe before computing it.
        zmax=max(abs(int(x)) for x in vs.flat)
        tensor_max=max(abs(int(x)) for x in tensor.flat)
        relative_bound=9*tensor_max*(1+abs(trw)+abs(d))*zmax*zmax
        matrix_bound=3*tensor_max*relative_bound
        assert 6*matrix_bound**3<2**63
        u,v=vs[:,:3],vs[:,3:]
        r=np.einsum('bi,bj,ijk->bk',u,u,tensor)+trw*np.einsum('bi,bj,ijk->bk',u,v,tensor)-d*np.einsum('bi,bj,ijk->bk',v,v,tensor)
        M=np.einsum('bi,ijk->bkj',r,tensor)
        maxentry=max(abs(int(x)) for x in M.flat)
        assert 6*maxentry**3<2**63
        return (M[:,0,0]*(M[:,1,1]*M[:,2,2]-M[:,1,2]*M[:,2,1])
               -M[:,0,1]*(M[:,1,0]*M[:,2,2]-M[:,1,2]*M[:,2,0])
               +M[:,0,2]*(M[:,1,0]*M[:,2,1]-M[:,1,1]*M[:,2,0]))
    return norm


def signature_certificate(a,b):
    norm=norm_evaluator(a,b);ML,MU,scale=embedding_bounds(a,b)
    vs=np.array(list(product([-1,0,1],repeat=6)),dtype=np.int64)
    units=vs[abs(norm(vs))==1];pivots={};selected=[]
    for z in units:
        zp=np.maximum(z,0);zn=np.minimum(z,0);lo=ML@zp+MU@zn;hi=MU@zp+ML@zn
        assert all(l>0 or h<0 for l,h in zip(lo,hi))
        bits=sum(1<<i for i,h in enumerate(hi) if h<0);red=bits
        for p in sorted(pivots,reverse=True):
            if red>>p&1:red^=pivots[p]
        if red:pivots[red.bit_length()-1]=red;selected.append(dict(unit=list(map(int,z)),signature=bits))
        if len(selected)==6:break
    assert len(selected)==6
    return selected


def ellipsoid(Gram,bound):
    L,D=s.Matrix(Gram).LDLdecomposition();n=len(Gram)
    den=[lcm(*[int(L[j,i].q) for j in range(i,n)]) for i in range(n)]
    nums=[[int(L[j,i]*den[i]) for j in range(n)] for i in range(n)]
    terms=[D[i,i]/den[i]**2 for i in range(n)]
    scale=lcm(*[int(x.q) for x in terms]);weights=[int(x*scale) for x in terms]
    z=[0]*n
    def rec(i,left):
        if i<0:
            yield tuple(z);return
        shift=sum(nums[i][j]*z[j] for j in range(i+1,n));rad=isqrt(left//weights[i])
        for v in range(-((rad+shift)//den[i]),(rad-shift)//den[i]+1):
            z[i]=v;cost=weights[i]*(den[i]*v+shift)**2
            assert cost<=left
            yield from rec(i-1,left-cost)
    yield from rec(n-1,bound*scale)


def enumerate_ratios(a,b,Amax):
    assert a in (5,8) and b in (7,9,13)
    witness=signature_certificate(a,b)
    one,mul,E,G,matrices,t,H=field(a,b);norm=norm_evaluator(a,b)
    # Positivity and trace<=A imply Tr(alpha^2)<=A^2.  The inverse
    # trace Gram matrix therefore bounds every alpha coefficient by 2A.
    Hinv=s.Matrix(H).inv()
    assert all(Hinv[i,i]<=4 for i in range(6))
    ML,MU,scale=embedding_bounds(a,b)
    one3,mul3,_,_=cubic(b);gen=np.array([0,1,0] if b==9 else [1,0,0],dtype=np.int64)
    delta=np.r_[([-3,-6,-4] if b==13 else 2*one3-gen),[0,0,0]]
    prime=3 if b==9 else b
    assert norm(np.array([delta]))[0]==prime**2
    delta3=s.Matrix(np.column_stack([mul3(delta[:3],np.eye(3,dtype=np.int64)[j]) for j in range(3)]))
    assert delta3.det()==prime
    dlo=ML@np.maximum(delta,0)+MU@np.minimum(delta,0);assert min(dlo)>0
    assert 6*(2*Amax)*max(abs(int(x)) for x in MU.flat)<2**63
    allratios={};counts=[]
    for r in range(3):
        factor=one.copy()
        for _ in range(r):factor=mul(factor,delta)
        M=sum(int(x)*B for x,B in zip(factor,matrices));Gram=H@M
        vectors=units=0;buffer=[]
        def process(buffer):
            nonlocal vectors,units
            zs=np.array(buffer,dtype=np.int64);vectors+=len(zs)
            zs=zs[abs(norm(zs))==1];units+=len(zs)
            for z in zs:
                base=mul(factor,mul(z,z));A=int(t@base);assert A>0
                for n in range(1,Amax//A+1):
                    v=n*base;vp=np.maximum(v,0);vn=np.minimum(v,0)
                    assert max(abs(int(x)) for x in v)<=2*Amax
                    lo=ML@vp+MU@vn;hi=MU@vp+ML@vn
                    if min(lo)>scale:continue
                    if not np.array_equal(v,one):assert min(hi)<scale
                    orbit=[];vv=v.copy()
                    for _ in range(6):orbit.append(tuple(map(int,vv)));vv=G@vv
                    key=min(orbit)
                    allratios[key]=dict(coefficients=list(key),trace=n*A,degree=len(set(orbit)))
        for z in ellipsoid(Gram,Amax):
            buffer.append(z)
            if len(buffer)==10000:process(buffer);buffer=[]
        if buffer:process(buffer)
        counts.append(dict(r=r,vectors=vectors,units=units,ratios_so_far=len(allratios)))
        print(a,b,'square power',r,'vectors',vectors,'units',units,'ratios',len(allratios),flush=True)
    out=dict(a=a,b=b,Amax=Amax,signature_witnesses=witness,counts=counts,
             candidates=sorted(allratios.values(),key=lambda x:(x['trace'],x['coefficients'])),
             status='EXACT_UNIT_SQUARE_ENUMERATION')
    path=Path(__file__).with_name(f'sextic_{a}_{b}_squares.json');path.write_text(json.dumps(out,indent=2)+'\n')
    return out


if __name__=='__main__':enumerate_ratios(*map(int,sys.argv[1:]))
