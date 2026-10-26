"""Independent audit of the new rank-twelve signed-descent exclusions.

No import from root/signed_mod4.py or root/characters.py.  Uses BFS trace
orbits, an explicit uint8 GF(2) matrix, full integer associativity, and the
commutator-ideal quotient rather than a common commutator kernel.
"""
from pathlib import Path
from itertools import product
from collections import Counter
import json, time
import numpy as np
import sympy as s
from independent_audit import BASE,HERE,dual,require,casimir,polynomial
t=s.Symbol('t')

def signed_descent(R):
    n=len(R);du=dual(R);unseen=set(product(range(1,n),repeat=3));orbits=[];locations={}
    while unseen:
        seed=min(unseen);todo=[seed];orb=set()
        while todo:
            a,b,c=todo.pop()
            if(a,b,c)in orb:continue
            orb.add((a,b,c));todo.extend([(b,c,a),(du[c],du[b],du[a])])
        unseen.difference_update(orb)
        vals={R[a][b][du[c]]for a,b,c in orb};require(len(vals)==1,'trace orbit bounds')
        if vals=={0}:continue
        require(vals=={1},'multiplicity one');v=len(orbits);orbits.append(sorted(orb))
        for a,b,c in orb:locations[a,b,du[c]]=v
    m=len(orbits);equations=set()
    for i,j,k,l in product(range(n),repeat=4):
        counts=Counter()
        for p in range(n):
            for first,second in (((i,j,p),(p,k,l)),((j,k,p),(i,p,l))):
                if R[first[0]][first[1]][first[2]]and R[second[0]][second[1]][second[2]]:
                    for term in (first,second):
                        if term in locations:counts[locations[term]]+=1
        row=tuple(v for v in range(m)if counts[v]%2)
        if row:equations.add(row)
    for i in range(1,n):
        if du[i]!=i:continue
        for j in range(n):
            if R[j][du[j]][i]:equations.add((locations[j,du[j],i],))
    A=np.zeros((len(equations),m),dtype=np.uint8)
    for row,indices in enumerate(sorted(equations)):
        A[row,list(indices)]=1
    raw=A.copy();rank=0;pivots=[]
    for col in range(m):
        hits=np.flatnonzero(A[rank:,col])
        if not len(hits):continue
        p=int(hits[0])+rank;A[[p,rank]]=A[[rank,p]]
        for row in np.flatnonzero(A[:,col]):
            if row!=rank:A[row]^=A[rank]
        pivots.append(col);rank+=1
    free=[i for i in range(m)if i not in pivots];basis=[]
    for f in free:
        x=np.zeros(m,dtype=np.uint8);x[f]=1
        for i,p in enumerate(pivots):x[p]=A[i,f]
        require(not np.any(raw@x%2),'nullspace vector');basis.append(x)
    # All dual-compatible changes of simple lifts, independently generated.
    unseen=set(range(1,n));label_orbits=[]
    while unseen:
        i=min(unseen);orb={i,du[i]};unseen.difference_update(orb);label_orbits.append(orb)
    gauges={}
    for choice in product((1,-1),repeat=len(label_orbits)):
        eps=[1]*n
        for sign,orb in zip(choice,label_orbits):
            for a in orb:eps[a]=sign
        signature=tuple(int(eps[a]*eps[b]*eps[c]<0)for orb in orbits for a,b,c in [orb[0]])
        gauges[signature]=eps
    template=np.zeros((n,n,n),dtype=np.int64)
    for i in range(n):template[0,i,i]=template[i,0,i]=template[i,du[i],0]=1
    survivors=[];rejected=0
    for bits in product((0,1),repeat=len(basis)):
        x=np.zeros(m,dtype=np.uint8)
        for bit,v in zip(bits,basis):
            if bit:x^=v
        T=template.copy()
        for v,orb in enumerate(orbits):
            for a,b,c in orb:T[a,b,du[c]]=1-2*int(x[v])
        L=np.einsum('ijm,mkl->ijkl',T,T,optimize=True);Q=np.einsum('jkm,iml->ijkl',T,T,optimize=True)
        if not np.array_equal(L,Q):rejected+=1;continue
        signature=tuple(map(int,x));require(signature in gauges,'surviving signed table is an original gauge')
        eps=gauges[signature]
        require(all(int(T[i,j,k])==eps[i]*eps[j]*eps[k]*R[i][j][k]for i,j,k in product(range(n),repeat=3)),'every coefficient agrees with the gauge')
        survivors.append(signature)
    return dict(variables=m,equations=len(equations),kernel_dimension=len(basis),linear_candidates=2**len(basis),associativity_rejections=rejected,associative_count=len(survivors),all_gauge_original=True)

def linear_characters(R):
    n=len(R);N=[s.Matrix(M).T for M in R]
    cols=[s.Matrix([R[i][j][k]-R[j][i][k]for k in range(n)])for i,j in product(range(n),repeat=2)if R[i][j]!=R[j][i]]
    I=s.Matrix.hstack(*cols)if cols else s.zeros(n,0)
    I=s.Matrix.hstack(*I.columnspace())if I.cols else I
    while I.cols:
        C=s.Matrix.hstack(I,*(A*I for A in N));new=s.Matrix.hstack(*C.columnspace())
        if new.cols==I.cols:break
        I=new
    W=s.Matrix.hstack(*I.T.nullspace())if I.cols else s.eye(n)
    Q=W.T;P=W*(W.T*W).inv();B=[Q*A*P for A in N];r=Q.rows
    require(all(Q*A==M*Q for A,M in zip(N,B)),'quotient action')
    require(all(A*B0==B0*A for A in B for B0 in B),'commutator ideal quotient is commutative')
    for k in range(1,20):
        H=sum((k**i*A for i,A in enumerate(B)),s.zeros(r));p=H.charpoly(t).as_poly()
        if s.gcd(p,p.diff()).degree()==0:break
    else:raise ValueError('separating element')
    unit=Q[:,0];powers=s.Matrix.hstack(*(H**j*unit for j in range(r)));require(powers.det()!=0,'unit is cyclic')
    co=[powers.inv()*A*unit for A in B]
    require(all(A==sum((c[j]*H**j for j in range(r)),s.zeros(r))for A,c in zip(B,co)),'all quotient matrices represented')
    quadratic=polynomial([1,-720,2592]);Cpoly=casimir(R).charpoly(t).as_poly()
    require(Cpoly.rem(quadratic).is_zero and quadratic.is_irreducible,'required central quadratic field')
    linear=polynomial([1,-36]);require(Cpoly.rem(linear).is_zero and not Cpoly.rem(linear**2).is_zero,'multiplicity-one central root 36')
    out=[];du=dual(R)
    for f,m in p.factor_list()[1]:
        K=s.QQ.alg_field_from_poly(f);ds=[K(s.Poly.from_list(list(reversed(list(c))),t).rem(f).all_coeffs())for c in co]
        require(ds[0]==K.one and all(sum((K(R[i][j][k])*ds[k]for k in range(n)),K.zero)==ds[i]*ds[j]for i,j in product(range(n),repeat=2)),'all exact character products')
        if any(not d for d in ds):why='zero dimension'
        elif any(ds[i]!=ds[du[i]]for i in range(n)):why='unequal dual dimensions'
        elif f.degree()%2:why='odd field degree cannot contain required quadratic Casimir roots'
        else:
            require(f.degree()==2,'only quadratic case remains')
            d=next(v for v in ds if v!=K.one)
            require(d*d-8*d-2*K.one==K.zero,'quadratic dimension relation')
            require(Counter(ds)==Counter({K.one:2,d:8,d+K.one:2}),'dimension order is Z plus Z*d')
            D=sum((v*v for v in ds),K.zero);beta=D/K(36)
            require(beta==K(s.Rational(2,3))+K(s.Rational(7,3))*d,'central forgotten dimension has noninteger lattice coefficients')
            why='central root36 gives 2/3+(7/3)d outside Z+Z*d'
        out.append(dict(field_polynomial=list(map(str,f.all_coeffs())),obstruction=why))
    return dict(one_dimensional_count=r,characters=out)

if __name__=='__main__':
    data=json.loads((BASE/'tensors.json').read_text());out=[];start=time.monotonic()
    for i in (63,64,215,365):
        rid=f'R12_1_{i}';R=data[rid]
        q=dict(id=rid,signed_descent=signed_descent(R),spherical_characters=linear_characters(R));out.append(q)
        print(rid,q['signed_descent'],flush=True)
    result=dict(status='PASS',records=out,elapsed_seconds=time.monotonic()-start)
    (HERE/'quadratic_signed_independent.json').write_text(json.dumps(result,indent=2)+'\n');print('PASS',result['elapsed_seconds'])
