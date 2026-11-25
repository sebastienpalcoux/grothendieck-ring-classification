#!/usr/bin/env python3
"""Exact finite trace-system exclusions, including singular Galois spans.

Every exclusion uses integer or rational arithmetic.  Input candidate lists
come from the exact trace-lattice or unit-square enumeration.  A nonempty
Fourier survivor set causes failure and is never discarded numerically.
"""
import sys,json
from pathlib import Path
from math import gcd,lcm
from itertools import product
import numpy as np
import sympy as s
from sextic_lattice import field,embedding_bounds


def compositions(n,k):
    if k==1:
        yield (n,);return
    for x in range(1,n-k+2):
        for tail in compositions(n-x,k-1):yield (x,)+tail


def integer_matrix(M):
    d=s.ilcm(*[x.q for x in M]);A=np.array(M*d,dtype=np.int64)
    return A,int(d)


def run(a,b):
    suffix='squares' if (a,b) in [(5,7),(5,9)] else 'exact'
    path=Path(__file__).with_name(f'sextic_{a}_{b}_{suffix}.json')
    data=json.loads(path.read_text())
    one,mul,E,G,matrices,t,H=field(a,b)
    ML,MU,scale=embedding_bounds(a,b)
    SG=s.Matrix(G);SH=s.Matrix(H)
    weights=[[1,1,-1,-2,-1,1],[2,-1,-1,2,-1,-1],[1,-1,1,-1,1,-1]]
    weights[0]=[2,1,-1,-2,-1,1]
    halves=[2,2,1]
    forms=[sum((s.Rational(w,den)*SH*SG**j for j,w in enumerate(ws)),s.zeros(6))
           for ws,den in zip(weights,halves)]
    conductors=[lcm(a,b),b,a]
    records=[]
    for ci,cand in enumerate(data['candidates']):
        if cand['degree']!=6:continue
        v=np.array(cand['coefficients'],dtype=np.int64)
        for _ in range(6):
            vp=np.maximum(v,0);vn=np.minimum(v,0)
            lower=ML@vp+MU@vn;upper=MU@vp+ML@vn
            if all(upper[0]<lower[i] for i in range(1,6)):break
            v=G@v
        assert upper[0]<scale and all(upper[0]<lower[i] for i in range(1,6))
        orbit=[];vv=v.copy()
        for _ in range(6):orbit.append(vv);vv=G@vv
        total_new=cand['trace']-6;m,r=divmod(total_new,5)
        moment_lower=6*(5*m*m+2*m*r+r)-total_new*total_new
        vv=s.Matrix(v)
        moment_upper=sum(mult*s.Rational(gcd(c,4),c)*(vv.T*F*vv)[0] for mult,c,F in zip([2,2,1],conductors,forms))
        if moment_lower>moment_upper:
            records.append(dict(alpha=list(map(int,v)),trace=cand['trace'],fourier_survivors=0,
                                moment_lower=moment_lower,moment_upper=str(moment_upper),method='summed_moment'))
            print(a,b,'candidate',ci,'trace',cand['trace'],'summed moment excludes',flush=True)
            continue
        C=s.Matrix(np.array(orbit)@H)
        rank=C.rank()
        if rank==6:
            Q=C.inv();kernel=s.zeros(6,0)
        else:
            rows=list(C.T.rref()[1]);cols=list(C.rref()[1])
            minor=C.extract(rows,cols).inv();Q=s.zeros(6)
            for i,ci0 in enumerate(cols):
                for j,rj in enumerate(rows):Q[ci0,rj]=minor[i,j]
            kernel=s.Matrix.hstack(*C.nullspace())
        consistency,dc=integer_matrix(C*Q-s.eye(6))
        assert max(abs(int(x)) for x in consistency.flat)*cand['trace']<2**63
        M=sum((int(x)*s.Matrix(y) for x,y in zip(v,matrices)),s.zeros(6))
        tests=[]
        def eliminate(B):
            result=Q.T*B*Q
            if kernel.cols:
                cross=Q.T*B*kernel
                result-=cross*(kernel.T*B*kernel).pinv()*cross.T
            return result
        for F,c in zip(forms,conductors):
            for B,cap in [(F,s.Rational(gcd(c,4),c)),(M.T*F*M,s.Rational(gcd(c,2),c)),
                          (2*M.T*F*M+F,s.Rational(4,c))]:
                A,den=integer_matrix(eliminate(B));tests.append((A,int(cap*den),den,cap))
        for A,lim,den,cap in tests:
            assert int(np.max(np.abs(A)))*cand['trace']**2<2**63
        total=surv=0
        buffer=[]
        def process(buffer):
            nonlocal total,surv
            h=np.array(buffer,dtype=np.int64);total+=len(h)
            h=h[np.all(h@consistency.T==0,axis=1)]
            if not len(h):return
            for F,lim,den,cap in tests:
                vals=np.einsum('bi,ij,bj->b',h,F,h)
                h=h[vals<=lim]
                if not len(h):return
            surv+=len(h)
        for htail in compositions(cand['trace']-1,5):
            buffer.append((1,)+htail)
            if len(buffer)==10000:process(buffer);buffer=[]
        if buffer:process(buffer)
        records.append(dict(alpha=list(map(int,v)),trace=cand['trace'],rank=rank,
                            trace_vectors=total,fourier_survivors=surv))
        print(a,b,'candidate',ci,'trace',cand['trace'],'vectors',total,'Fourier',surv,
              'rank',rank,flush=True)
    assert all(r.get('fourier_survivors')==0 for r in records), 'A trace vector survives the proved necessary inequalities.'
    out=Path(__file__).with_name(f'sextic_{a}_{b}_trace_exact.json')
    out.write_text(json.dumps(records,indent=2)+'\n')


if __name__=='__main__':run(int(sys.argv[1]),int(sys.argv[2]))
