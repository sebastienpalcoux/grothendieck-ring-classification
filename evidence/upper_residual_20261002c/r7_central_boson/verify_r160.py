#!/usr/bin/env python3
"""Exact small premises of the R160 general exclusion (Python + SymPy)."""
import argparse
import collections
import gzip
import hashlib
import itertools
import json
from pathlib import Path
import sympy as s

HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'supplements/rank7/data/rank7_tables.txt.gz').exists())

def require(ok,msg):
    if not ok:raise ValueError(msg)

def flat(T):return tuple(x for A in T for row in A for x in row)
def digest(T):return hashlib.sha256(json.dumps(T,separators=(',',':')).encode()).hexdigest()
def closure(T,xs):
    out=set(xs)
    while True:
        nxt=out|{k for i in out for j in out for k,v in enumerate(T[i][j]) if v}
        if nxt==out:return sorted(out)
        out=nxt

def verify():
    path=ROOT/'supplements/rank7/data/rank7_tables.txt.gz'
    packed=path.read_bytes()
    require(hashlib.sha256(packed).hexdigest()=='6ddea4c66de7fbe077e9552e71e8cf95ec3fec5bbd30a615e68e2d8fcb9ae9c9','census archive hash')
    buckets=collections.defaultdict(list)
    for line in gzip.decompress(packed).decode().splitlines():
        if line.strip():
            T=json.loads(line.replace('{','[').replace('}',']'));buckets[max(flat(T))].append(T)
    require({m:len(v) for m,v in buckets.items()}=={1:43,2:319,3:1059,4:2780},'census multiplicity counts')
    T=buckets[2][159];d=[1,1,2,6,6,6,6];n=7
    require(len(T)==n and all(len(A)==n and all(len(row)==n for row in A) for A in T),'shape')
    require(all(type(v) is int and v>=0 for v in flat(T)),'nonnegative integer coefficients')
    for i,j,k in itertools.product(range(n),repeat=3):
        require(T[0][i][j]==T[i][0][j]==int(i==j),'unit')
        require(T[i][j][0]==int(i==j),'self duality')
        require(T[i][j][k]==T[j][i][k]==T[i][k][j],'commutativity and reciprocity')
    for i,j,k,l in itertools.product(range(n),repeat=4):
        require(sum(T[i][j][a]*T[a][k][l] for a in range(n))==sum(T[j][k][a]*T[i][a][l] for a in range(n)),'associativity')
    require(all(sum(T[i][j][k]*d[k] for k in range(n))==d[i]*d[j] for i,j in itertools.product(range(n),repeat=2)),'exact positive dimension character')
    require(sum(x*x for x in d)==150,'global dimension')
    require(T[1][1]==[1,0,0,0,0,0,0] and T[2][2]==[1,1,1,0,0,0,0],'RepS3 subring')
    for i in range(2,7):require(T[1][i]==[int(i==k) for k in range(n)],'sign action')
    for i in range(3,7):require(T[2][i]==[2*int(i==k) for k in range(n)],'rank-one RepS3 module action')
    require(closure(T,[k for i in range(n) for k,v in enumerate(T[i][i]) if v])==list(range(n)),'whole adjoint subring')
    N=list(map(s.Matrix,T));C=sum((A*A.T for A in N),s.zeros(n));t=s.Symbol('t')
    require(s.expand(C.charpoly(t).as_expr()-(t-150)*(t-3)*(t-2)*(t-25)**4)==0,'formal codegrees')
    I1=[1,50,75,6,6,6,6]
    gram=[[sum(T[a][j][u]*T[u][a][k] for a in range(n) for u in range(n)) for k in range(n)] for j in range(n)]
    require(gram==[list(map(int,row)) for row in C.tolist()],'induction Gram identity')
    require(gram[0][1]==5 and gram[0][2]==9 and gram[1][1]==7,'three small Gram entries')
    small=[(b,c) for b in range(6) for c in range(3) if 1+b+2*c==6]
    small_quad=[q for q in itertools.product(small,repeat=4) if sum(b for b,c in q)<=5 and sum(c for b,c in q)<=9]
    require(small_quad==[((1,2),)*4],'forced small restrictions')
    big=[(b50,b75,c50,c75) for b50,b75,c50,c75 in itertools.product(range(2),repeat=4) if b50+b75==1 and c50+c75==1 and (50-1-b50-2*c50)%6==0 and (75-1-b75-2*c75)%6==0]
    require(big==[(1,0,0,1)],'forced large g/E restrictions')
    shared_dim=4*6+50;remaining=150-shared_dim;divisors=s.divisors(150)
    pairs=[(a,b) for a in divisors for b in divisors if a<=b and a+b==remaining]
    require(shared_dim==74 and remaining==76 and pairs==[(1,75)],'central invertible divisor pair')
    proper=[3+9*k for k in range(1,8) if 75%(3+9*k)==0]
    require(proper==[],'dimension75 adjoint whole')
    # Exhaust all involutions over F5, without searching pentagon or modular data.
    def mul(A,B):
        a,b,c,e=A;f,g,h,j=B
        return ((a*f+b*h)%5,(a*g+b*j)%5,(c*f+e*h)%5,(c*g+e*j)%5)
    I=(1,0,0,1);minus=(4,0,0,4)
    gl=[A for A in itertools.product(range(5),repeat=4) if (A[0]*A[3]-A[1]*A[2])%5]
    require(len(gl)==480,'GL2(5) order')
    free_invol=[A for A in gl if A!=I and mul(A,A)==I and ((A[0]-1)*(A[3]-1)-A[1]*A[2])%5]
    require(free_invol==[minus],'only free involution is -I')
    require(len([a for a in range(25) if s.gcd(a,25)==1])==20,'Aut(C25) order')
    return {'status':'PASS','scope':'general_complex','id':'R7_2_160','tensor_sha256':digest(T),'dimensions':d,'global_dimension':150,'formal_codegrees':[150,3,2,25,25,25,25],'induced_unit_simple_dimensions':I1,'small_Gram_entries':{'I1_Ig':5,'I1_IE':9,'Ig_Ig':7},'small_constituent_g_E_multiplicities':small_quad,'large_constituent_g_E_multiplicities':big,'Ig_residual_dimension':remaining,'complete_divisor_pairs':pairs,'dimension75_proper_adjoint_possibilities':proper,'GL2_F5_order':480,'all_fixed_point_free_involutions':free_invol,'python_optimized':not __debug__}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path);args=parser.parse_args()
    result=verify();encoded=json.dumps(result,indent=2)+'\n'
    if args.output:args.output.write_text(encoded)
    print(encoded)
