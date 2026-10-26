"""Rank-eleven input identity and exact tensor utilities.

Physical source line numbers are permanent identifiers.  Approximate spectral
data may guide discovery but never assign mathematical classification status.
"""
from pathlib import Path
import collections, gzip, hashlib, itertools, json
import numpy as np
import networkx as nx

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE = ROOT / 'repositories/fusion-ring-census/results/rank11/tables.txt.gz'

def require(condition, message='exact verification failed'):
    if not condition:
        raise ValueError(message)

def read():
    with gzip.open(SOURCE, 'rt') as f:
        lines = f.read().splitlines()
    require(len(lines) == 182, 'expected 182 physical source lines')
    return {f'R11_1_{i}': json.loads(line.replace('{','[').replace('}',']'))
            for i,line in enumerate(lines,1)}

def sha(R):
    return hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest()

def dual(R):
    n=len(R)
    out=[]
    for i in range(n):
        hits=[j for j in range(n) if R[i][j][0]]
        require(len(hits)==1, 'duality not unique')
        out.append(hits[0])
    return out

def validate(R):
    n=len(R); N=np.array(R,dtype=np.int64)
    require(N.shape==(n,n,n), 'shape')
    require(all(type(x) is int and x>=0 for A in R for B in A for x in B), 'coefficients')
    require(np.array_equal(N[0],np.eye(n,dtype=int)), 'left unit')
    require(np.array_equal(N[:,0,:],np.eye(n,dtype=int)), 'right unit')
    d=dual(R)
    require(all(d[d[i]]==i for i in range(n)), 'dual involution')
    require(all(R[i][j][0]==int(d[i]==j) for i,j in itertools.product(range(n),repeat=2)), 'unit coefficients')
    require(np.array_equal(np.einsum('ijx,xkl->ijkl',N,N),np.einsum('jkx,ixl->ijkl',N,N)), 'associativity')
    for i,j,k in itertools.product(range(n),repeat=3):
        require(R[i][j][k]==R[d[i]][k][j]==R[k][d[j]][i], 'Frobenius reciprocity')
        require(R[i][j][k]==R[d[j]][d[i]][d[k]], 'dual anti-involution')
    return True

def signature(R):
    n=len(R); d=dual(R)
    return [(i==0,d[i]==i,tuple(sorted(sum(r) for r in R[i])),
             tuple(sorted(sum(R[j][i]) for j in range(n))),
             tuple(sorted(R[i][d[i]])),sum(R[i][j][j] for j in range(n)))
            for i in range(n)]

def coarse(R):
    return tuple(sorted(signature(R)))

def based_iso(A,B):
    """Return input-to-output basis bijection, verifying every coefficient."""
    n=len(A)
    if len(B)!=n:return None
    sa,sb=signature(A),signature(B)
    if sorted(sa)!=sorted(sb):return None
    ca=[{j for j in range(n) if sa[i]==sb[j]} for i in range(n)]
    p={0:0}; used={0}; da,db=dual(A),dual(B)
    def okay(i,j):
        if A[i][i][i]!=B[j][j][j]:return False
        if da[i] in p and db[j]!=p[da[i]]:return False
        for a,b in p.items():
            if (A[i][i][a],A[i][a][i],A[a][i][i])!=(B[j][j][b],B[j][b][j],B[b][j][j]):return False
            for c,d in p.items():
                if (A[i][a][c],A[a][i][c],A[a][c][i])!=(B[j][b][d],B[b][j][d],B[b][d][j]):return False
        return True
    def dfs():
        if len(p)==n:return [p[i] for i in range(n)]
        choices=None; best=None
        for i in range(n):
            if i in p:continue
            cs=[j for j in sorted(ca[i]-used) if okay(i,j)]
            if not cs:return None
            if choices is None or len(cs)<len(choices):best,choices=i,cs
        for j in choices:
            p[best]=j;used.add(j); ans=dfs()
            if ans is not None:return ans
            del p[best];used.remove(j)
        return None
    ans=dfs()
    if ans is not None:
        require(sorted(ans)==list(range(n)) and ans[0]==0, 'basis bijection')
        require(all(A[i][j][k]==B[ans[i]][ans[j]][ans[k]] for i,j,k in itertools.product(range(n),repeat=3)), 'full tensor comparison')
    return ans

def subrings(R):
    n=len(R); d=dual(R)
    supp=[[sum(1<<k for k,x in enumerate(R[i][j]) if x) for j in range(n)] for i in range(n)]
    def closure(mask):
        while True:
            old=mask; a=[i for i in range(n) if mask>>i&1]
            for i in a:
                mask|=1<<d[i]
                for j in a:mask|=supp[i][j]
            if mask==old:return mask
    seen={1}; todo=[1]
    while todo:
        S=todo.pop()
        for i in range(1,n):
            if not S>>i&1:
                T=closure(S|1<<i)
                if T not in seen:seen.add(T);todo.append(T)
    return [[i for i in range(n) if S>>i&1] for S in sorted(seen,key=lambda x:(x.bit_count(),x))]

def dump(path, obj):
    Path(path).write_text(json.dumps(obj,indent=2)+'\n')
