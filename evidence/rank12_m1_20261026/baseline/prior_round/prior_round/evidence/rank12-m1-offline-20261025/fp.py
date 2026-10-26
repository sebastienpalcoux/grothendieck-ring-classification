from pathlib import Path
import sys, sympy as s
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/"sources/work/rank11/arithmetic/legacy"))
import exact
require=exact.require

def solve_field(B, v, K):
    n=len(v); A=[list(B[i])+[v[i]] for i in range(n)]
    for j in range(n):
        q=next((i for i in range(j,n) if A[i][j]),None)
        require(q is not None,'singular Perron cofactor')
        A[j],A[q]=A[q],A[j]; a=A[j][j]
        A[j]=[x/a for x in A[j]]
        for i in range(n):
            if i==j or not A[i][j]:continue
            a=A[i][j]; A[i]=[x-a*y for x,y in zip(A[i],A[j])]
    return [A[i][-1] for i in range(n)]

def fp_character(R):
    n=len(R); A=sum(map(s.Matrix,R),s.zeros(n)); t=exact.t
    require(all(x>0 for x in A),'positive separating sum')
    factors=A.charpoly(t).as_poly().factor_list()[1]
    real=[(f,m,e) for f,m in factors for e in exact.embeddings(f)]
    f,m,emb=max(real,key=lambda x:x[2].hi)
    require(m==1,'Perron multiplicity')
    K=exact.field(f); u=K(s.Poly(t,t).rem(f).all_coeffs())
    B=[[K(A[i,j])-(u if i==j else K.zero) for j in range(1,n)] for i in range(1,n)]
    v=[-K(A[i,0]) for i in range(1,n)]
    d=[K.one]+solve_field(B,v,K)
    require(all(emb.sign(x)>0 for x in d),'positive Perron dimensions')
    require(all(sum((K(R[i][j][k])*d[k] for k in range(n)),K.zero)==d[i]*d[j]
                for i in range(n) for j in range(n)),'exact dimension homomorphism')
    D=sum((x*x for x in d),K.zero)
    return f,K,u,d,D,emb

def polynomial_of(q,f,K,u):
    d=f.degree()
    M=s.Matrix.hstack(*(exact.vector(q*u**i,d) for i in range(d)))
    return M.charpoly(exact.t).as_poly()
