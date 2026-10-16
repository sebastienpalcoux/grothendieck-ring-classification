#!/usr/bin/env python3
"""Source-bound verification of the R2591 twisted-V4 Morita reduction."""
import argparse, collections, gzip, hashlib, itertools, json
from pathlib import Path
import sympy as s

def need(v, message):
    if not v:
        raise RuntimeError(message)

def rank2(M):
    A=[[(int(x)%2) for x in row] for row in M]
    r=0
    for c in range(len(A[0])):
        q=next((i for i in range(r,len(A)) if A[i][c]),None)
        if q is None: continue
        A[r],A[q]=A[q],A[r]
        for i in range(len(A)):
            if i!=r and A[i][c]:A[i]=[x^y for x,y in zip(A[i],A[r])]
        r+=1
    return r

def block(a,B,b):
    J=[[0,1],[1,0]]
    return [[a*J[i][j] for j in range(2)]+B[i] for i in range(2)]+[[B[j][i] for j in range(2)]+[b*J[i][j] for j in range(2)] for i in range(2)]

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    counts=collections.Counter();N=None
    for line in gzip.open(args.repo/'supplements/rank7/data/rank7_tables.txt.gz','rt'):
        if not line.strip():continue
        T=json.loads(line.replace('{','[').replace('}',']'));m=max(v for a in T for b in a for v in b);counts[m]+=1
        if (m,counts[m])==(4,2591):N=T;break
    need(N is not None,'source found')
    G=[0,3,4,5];X=6;Y=1;Z=2;t=2+s.sqrt(5);dims=[s.Integer(1),2*t,2*t,s.Integer(1),s.Integer(1),s.Integer(1),s.Integer(2)]
    dual=[next(j for j in range(7) if N[i][j][0]) for i in range(7)]
    need(dual==[0,2,1,3,4,5,6],'duality')
    for i,j in itertools.product(range(7),repeat=2):
        need(s.expand(dims[i]*dims[j]-sum(N[i][j][k]*dims[k] for k in range(7)))==0,'FP dimension character')
        for k,l in itertools.product(range(7),repeat=2):
            need(sum(N[i][j][a]*N[a][k][l] for a in range(7))==sum(N[j][k][a]*N[i][a][l] for a in range(7)),'source associativity')
    need(all(N[g][g][0]==1 for g in G),'V4 group')
    for g in G:
        for w in [X,Y,Z]:need(N[g][w][w]==N[w][g][w]==1,'fixedness')
    def vector(**kw):
        a=[0]*7
        for k,v in kw.items():a[int(k)]=v
        return a
    need(N[X][X]==[1 if i in G else 0 for i in range(7)],'TY square')
    need(N[X][Y]==N[Y][X]==vector(**{str(Z):2}),'XY')
    need(N[X][Z]==N[Z][X]==vector(**{str(Y):2}),'XZ')
    need(N[Y][Y]==vector(**{str(X):2,str(Y):4,str(Z):4}),'Y square')
    allB=[[[v[0],v[1]],[v[2],v[3]]] for v in itertools.product([0,1],repeat=4)]
    chis=[B for B in allB if rank2(B)==2 and B[0][1]==B[1][0]]
    need(len(chis)==4,'all four nondegenerate symmetric bicharacters')
    rows=[]
    for chi in chis:
        allowed=[(a,b) for a,b in itertools.product([0,1],repeat=2) if rank2(block(a,chi,b))<=2]
        need(allowed==[(1,1)],'Y² multiplicity forces both classes nontrivial')
        need(rank2(block(1,chi,1))==2,'twisted X rank')
        rows.append({'chi':chi,'allowed_alpha_beta':allowed,'twisted_X_rank':2})
    allowedB=[B for B in allB if rank2(block(1,B,0))<=2]
    need(len(allowedB)==10,'ten singular mixed matrices')
    need(all(rank2(B)<=1 for B in allowedB),'XY multiplicity forces singular B')
    need(all(rank2(block(0,B,0))==2*rank2(B) for B in allowedB),'twisted Y rank formula')
    need(all(rank2(block(1,B,1))==4 for B in allowedB),'untwisted Y block nondegenerate')
    need(s.expand((t/2)*((2-s.sqrt(5))/2))==-s.Rational(1,4),'t/2 is not an algebraic integer')
    need(sum(rank2(B)==1 for B in allowedB)==9,'nine permissible nonzero mixed matrices')
    need(s.expand(4+4+8*t*t-sum(d*d for d in dims))==0,'Morita dimension balance')
    result={'status':'PASS','case':'R7_4_2591','tensor_sha256':hashlib.sha256(json.dumps(N,separators=(',',':')).encode()).hexdigest(),'source_labels':{'G':G,'X':X,'Y':Y,'Z':Z},'bicharacter_rank_checks':rows,'singular_mixed_matrices':allowedB,'nonzero_mixed_count':9,'dual_simple_dimensions':{'1':8,'2+sqrt(5)':8},'conclusion':'general complex categorification is Morita equivalent to a free-orbit two-dimension category and is Galois pseudo-unitary','classification_status':'unresolved','optimizer_used':False}
    args.output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':'PASS','case':'R7_4_2591','dual_type':'1^8,t^8','classification_status':'unresolved'}))

if __name__=='__main__':main()
