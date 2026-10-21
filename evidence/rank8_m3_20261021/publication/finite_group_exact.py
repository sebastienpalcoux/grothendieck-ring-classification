"""Small exact permutation-group and tensor utilities for the structural proofs."""
from fractions import Fraction
from itertools import permutations, combinations
import hashlib
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
def require(ok,message):
    if not ok:raise ValueError(message)
def digest(x):return hashlib.sha256(json.dumps(x,separators=(',',':')).encode()).hexdigest()
def source(rid,expected):
    row=next(r for r in json.loads((ROOT/'evidence/rank8_m3_20261021/pipeline/census_m3.json').read_text()) if r['id']==rid)
    R=row['tensor'];require(digest(R)==row['tensor_sha256']==expected,'exact source tensor binding')
    return R

def compose(a,b):return tuple(a[b[i]] for i in range(len(a)))
def inverse(a):return tuple(a.index(i) for i in range(len(a)))
def identity(n):return tuple(range(n))
def even(a):return sum(a[i]>a[j] for i in range(len(a)) for j in range(i+1,len(a)))%2==0
def alternating(n=5):return set(p for p in permutations(range(n)) if even(p))
def generated(gens,n=5):
    out={identity(n)};queue=list(out)
    for x in queue:
        for g in gens:
            y=compose(x,g)
            if y not in out:out.add(y);queue.append(y)
    return out

def conjugate(g,x):return compose(compose(g,x),inverse(g))
def classes(G):
    todo=set(G);out=[]
    while todo:
        x=min(todo);C={conjugate(g,x) for g in G};require(C<=todo,'conjugacy partition')
        out.append(C);todo-=C
    return out

def subgroup(G,H):
    return bool(H) and identity(len(next(iter(G)))) in H and all(compose(a,b) in H for a in H for b in H)
def closed_subsets(R,universe):
    U=sorted(universe);out=[]
    for size in range(1,len(U)+1):
        for J in combinations(U,size):
            if 0 not in J:continue
            S=set(J)
            if all(not R[i][j][k] or k in S for i in S for j in S for k in range(len(R))):out.append(list(J))
    return out

def adjoint(R,universe):
    n=len(R);du=[next(j for j in range(n) if R[i][j][0]) for i in range(n)]
    S={0}|{k for i in universe for k in range(n) if R[i][du[i]][k]}
    while True:
        T=S|{k for i in S for j in S for k in range(n) if R[i][j][k]}
        if T==S:return sorted(S)
        S=T

def quadratic_dimensions(R,d,q):
    def mul(x,y):return (x[0]*y[0]+q*x[1]*y[1],x[0]*y[1]+x[1]*y[0])
    n=len(R)
    for i in range(n):
        for j in range(n):
            z=tuple(sum(R[i][j][k]*d[k][l] for k in range(n)) for l in (0,1))
            require(mul(d[i],d[j])==z,'dimension character equation')
    return sum(mul(x,x)[0] for x in d)

def grading(R,neutral,odd):
    require(sorted(neutral+odd)==list(range(len(R))),'grading partition')
    bits={i:0 for i in neutral}|{i:1 for i in odd}
    require(all(not R[i][j][k] or bits[k]==bits[i]^bits[j] for i in bits for j in bits for k in bits),'faithful C2 grading')

def matrix_rank(A):
    a=[[Fraction(x) for x in row] for row in A];r=0
    if not a:return 0
    for c in range(len(a[0])):
        p=next((i for i in range(r,len(a)) if a[i][c]),None)
        if p is None:continue
        a[r],a[p]=a[p],a[r];v=a[r][c];a[r]=[x/v for x in a[r]]
        for i in range(len(a)):
            if i!=r and a[i][c]:
                v=a[i][c];a[i]=[x-v*y for x,y in zip(a[i],a[r])]
        r+=1
    return r
