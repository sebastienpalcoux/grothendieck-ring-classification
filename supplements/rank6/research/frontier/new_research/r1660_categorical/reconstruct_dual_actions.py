#!/usr/bin/env python3
"""Exact nonnegative integral Gram bases for all nontrivial Morita types.

No optimizer or center-profile enumeration. Bounds follow from the diagonal
entries of the residual Gram matrix. All square Gram factors are enumerated
as orthonormal bases for its rational inverse quadratic form.
"""
import itertools
import json
import math
from pathlib import Path
import sympy as s


def require(ok,msg):
    if not ok: raise ValueError(msg)


I3=s.eye(3)
g=s.Matrix([[0,1,0],[1,0,0],[0,0,1]])
sig=s.Matrix([[0,0,1],[0,0,1],[1,1,0]])
I=s.eye(6);G=s.kronecker_product(s.eye(2),g)
S=s.kronecker_product(s.eye(2),sig)
vec=lambda M:s.Matrix(list(M))
mat=lambda v:s.Matrix(6,6,list(v))


def run(tag,a,b,c,f,V):
    U=s.Matrix([[a,b],[b,6-a]]);R=s.Matrix([[c,f],[f,4-c]])
    P=(U+V)/2;Q=(U-V)/2
    X=s.kronecker_product(P,I3)+s.kronecker_product(Q,g)+s.kronecker_product(R,sig)
    N=[I,G,X,G*X,S,S*X]
    K=sum((s.kronecker_product(n,n) for n in N),s.zeros(36))
    fixed=[I,G]
    if tag.startswith('III_'):
        Y=mat(K[:,0]-vec(I))
        fixed += [Y,G*Y]
    H=K-sum((vec(m)*vec(m).T for m in fixed),s.zeros(36))
    rank=H.rank()
    inds=[]
    for j in sorted(range(36),key=lambda j:H[j,j]):
        trial=inds+[j]
        if H.extract(trial,trial).det()!=0:
            inds=trial
            if len(inds)==rank:break
    B=H.extract(inds,inds);Binv=B.inv();lift=H[:,inds]*Binv
    denom=s.ilcm(*(x.q for x in Binv))
    qform=[[int(denom*Binv[i,j]) for j in range(rank)] for i in range(rank)]
    bounds=[math.isqrt(int(B[j,j])) for j in range(rank)]
    candidates=[]
    for v in itertools.product(*(range(b+1) for b in bounds)):
        if sum(v[i]*qform[i][j]*v[j] for i in range(rank) for j in range(rank))!=denom:
            continue
        full=lift*s.Matrix(v)
        if not all(x.is_Integer and x>=0 for x in full):continue
        candidates.append((v,full))
    orth=lambda v,w:sum(v[i]*qform[i][j]*w[j] for i in range(rank) for j in range(rank))==0
    adj={i:{j for j in range(i+1,len(candidates)) if orth(candidates[i][0],candidates[j][0])}
         for i in range(len(candidates))}
    cliques=[]
    def recurse(chosen,pool):
        if len(chosen)==rank:
            cliques.append(chosen);return
        if len(chosen)+len(pool)<rank:return
        for j in sorted(pool):recurse(chosen+[j],{k for k in pool & adj[j] if k>j})
    recurse([],set(range(len(candidates))))
    solutions=[]
    for clique in cliques:
        basis=fixed+[mat(candidates[j][1]) for j in clique]
        require(sum((vec(m)*vec(m).T for m in basis),s.zeros(36))==K,'Gram mismatch')
        W=s.Matrix.hstack(*(vec(m) for m in basis))
        tensor=[];valid=True
        for ma in basis:
            row=[]
            for mb in basis:
                coeff,params=W.gauss_jordan_solve(vec(ma*mb))
                if params.rows or not all(x.is_Integer and x>=0 for x in coeff):
                    valid=False;break
                row.append([int(x) for x in coeff])
            if not valid:break
            tensor.append(row)
        if not valid:continue
        dual=[]
        for i,ma in enumerate(basis):
            ds=[j for j,mb in enumerate(basis) if ma.T==mb]
            if len(ds)!=1:valid=False;break
            dual.append(ds[0])
        if not valid:continue
        if any(tensor[i][j][0]!=int(j==dual[i]) for i in range(len(basis)) for j in range(len(basis))):continue
        dims=[]
        # Perron vector for the module, with first Ising block weight1.
        d=3+2*s.sqrt(2)+2*s.sqrt(3)+s.sqrt(6)
        z=s.radsimp((d-a-c*s.sqrt(2))/(b+f*s.sqrt(2)))
        pvec=s.Matrix([1,1,s.sqrt(2),z,z,s.sqrt(2)*z])
        for ma in basis:dims.append(str(s.expand(s.radsimp((ma*pvec)[0]))))
        solutions.append({'action_matrices':[[list(map(int,row)) for row in m.tolist()] for m in basis],
                          'dual':dual,'FPdims':dims,'fusion_tensor':tensor})
    result={'type':tag,'residual_rank':rank,'pivot_indices':inds,'pivot_diagonal':[int(B[i,i]) for i in range(rank)],
            'candidate_vectors':len(candidates),'orthogonal_Gram_bases':len(cliques),
            'fusion_ring_solutions':len(solutions),'solutions':solutions}
    print(json.dumps({k:v for k,v in result.items() if k!='solutions'}),flush=True)
    for z in solutions: print(z['FPdims'],flush=True)
    return result


cases=[('II',2,3,2,2,s.Matrix([[0,1],[1,0]])),
       ('III_mixed',1,2,0,1,s.diag(1,-1)),
       ('III_same',1,2,0,1,s.eye(2)),
       ('IV_mixed',1,2,1,2,s.diag(1,-1)),
       ('IV_same',1,2,1,2,s.eye(2))]
results=[run(*case) for case in cases]
Path(__file__).with_name('dual_actions_receipt.json').write_text(json.dumps(results,indent=2)+'\n')
