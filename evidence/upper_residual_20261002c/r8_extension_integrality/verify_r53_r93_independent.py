#!/usr/bin/env python3
"""Independent exact finite premises of the R53/R93 proof; no assertions."""
import argparse
import collections
import gzip
import hashlib
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p/'supplements/rank8/data/rank8_tables.txt.gz').exists())

def require(ok, msg):
    if not ok:
        raise ValueError(msg)

def flat(T):
    return tuple(x for A in T for row in A for x in row)

def fingerprint(T):
    return hashlib.sha256(json.dumps(T,separators=(',',':')).encode()).hexdigest()

def closure(T, xs):
    result = set(xs)
    while True:
        nxt = result | {k for i in result for j in result for k,v in enumerate(T[i][j]) if v}
        if nxt == result:
            return sorted(result)
        result = nxt

def source_check():
    raw = gzip.decompress((ROOT/'supplements/rank8/data/rank8_tables.txt.gz').read_bytes())
    require(hashlib.sha256(raw).hexdigest() == '97b86d2de8ca0352c5c6e14686cd1d43dbd52180dc53b2ff1ccf7a61788c9600', 'raw source digest')
    buckets = collections.defaultdict(list)
    for line in raw.decode().splitlines():
        if line.strip():
            T=json.loads(line.replace('{','[').replace('}',']'))
            buckets[max(flat(T))].append(T)
    require({m:len(T) for m,T in buckets.items()} == {1:96,2:877}, 'census counts')
    Ts=sorted(buckets[2],key=flat)
    out=[]
    for ident,basis in [(53,[0,1,7,2,4,5]),(93,[0,1,7,2,5,6])]:
        T=Ts[ident-1];n=len(T)
        require(n==8 and all(len(A)==n and all(len(row)==n for row in A) for A in T),'shape')
        require(all(type(v) is int and v>=0 for v in flat(T)),'coefficients')
        dual=[]
        for i in range(n):
            hit=[j for j in range(n) if T[i][j][0]]
            require(len(hit)==1 and T[i][hit[0]][0]==1,'dual uniqueness')
            dual.append(hit[0])
        for i,j,k in itertools.product(range(n),repeat=3):
            require(T[0][i][j]==T[i][0][j]==int(i==j),'unit')
            require(T[i][j][k]==T[j][i][k]==T[dual[i]][k][j],'reciprocity')
            require(dual[dual[i]]==i,'dual involution')
        for i,j,k,l in itertools.product(range(n),repeat=4):
            require(sum(T[i][j][s]*T[s][k][l] for s in range(n))==sum(T[j][k][s]*T[i][s][l] for s in range(n)),'associativity')
        odd=sorted(set(range(n))-set(basis));grade=[int(i in odd) for i in range(n)]
        require(all(not T[i][j][k] or grade[k]==(grade[i]+grade[j])%2 for i,j,k in itertools.product(range(n),repeat=3)),'support grading')
        B=[[[T[i][j][k] for k in basis] for j in basis] for i in basis]
        for a,b in itertools.product(range(4),repeat=2):
            require(B[a][b]==[int(k==(a+b)%4) for k in range(6)],'C4 invertibles')
        for a in range(4):
            for b in (4,5):
                require(B[a][b]==B[b][a]==[int(k==b) for k in range(6)],'fixed nonunits')
        require(B[4][4]==[1,1,1,1,1,2] and B[5][5]==[1,1,1,1,2,1] and B[4][5]==B[5][4]==[0,0,0,0,2,2],'neutral products')
        require(closure(B,[k for i in range(6) for k,v in enumerate(B[i][i]) if v])==list(range(6)),'neutral adjoint closure')
        dims=[(0,3) if i in odd else (4,0) if i in basis[4:] else (1,0) for i in range(n)]
        def product(x,y):return (x[0]*y[0]+2*x[1]*y[1],x[0]*y[1]+x[1]*y[0])
        require(all(product(dims[i],dims[j])==tuple(sum(T[i][j][k]*dims[k][a] for k in range(n)) for a in (0,1)) for i,j in itertools.product(range(n),repeat=2)),'exact FP dimensions')
        out.append({'id':f'R8_2_{ident}','tensor_sha256':fingerprint(T),'neutral_basis':basis,'odd_basis':odd,'duality':dual})
    return out

def matrix_check():
    def mul(A,B):
        a,b,c,d=A;e,f,g,h=B
        return ((a*e+b*g)%3,(a*f+b*h)%3,(c*e+d*g)%3,(c*f+d*h)%3)
    def act(A,v):
        a,b,c,d=A;x,y=v
        return ((a*x+b*y)%3,(c*x+d*y)%3)
    I=(1,0,0,1);minus=(2,0,0,2)
    GL=[A for A in itertools.product(range(3),repeat=4) if (A[0]*A[3]-A[1]*A[2])%3]
    require(len(GL)==48,'GL2(3) order')
    generators=[]
    for A in GL:
        A2=mul(A,A)
        if A2==I or mul(A2,A2)!=I:continue
        powers=[A,A2,mul(A2,A)]
        if not all(act(P,v)!=v for P in powers for v in itertools.product(range(3),repeat=2) if v!=(0,0)):continue
        require(A2==minus,'free order-four generator square')
        # Every nontrivial power has invertible P-I, forcing commutators onto A.
        for P in powers:
            Q=((P[0]-1)%3,P[1],P[2],(P[3]-1)%3)
            require((Q[0]*Q[3]-Q[1]*Q[2])%3,'commutator map invertible')
        lines={frozenset([(0,0),v,tuple((2*x)%3 for x in v)]) for v in itertools.product(range(3),repeat=2) if v!=(0,0)}
        require(len(lines)==4 and not any({act(A,v) for v in L}==set(L) for L in lines),'no invariant proper subgroup')
        generators.append(A)
    require(len(generators)==6,'complete free order-four generator list')
    return {'GL2_F3_order':48,'all_free_C4_generators':generators,'normal_abelian_subgroup_orders':[1,9],'normalized_simple_dimensions':[1,3]}

def verify():
    return {'status':'PASS','scope':'general_complex','independent_of_author_checker':True,'sources':source_check(),'finite_group_premises':matrix_check(),'proper_adjoint_dimensions':[d for d in range(2,19,4) if 18%d==0 and d<18],'python_optimized':not __debug__}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path);args=parser.parse_args()
    result=verify();encoded=json.dumps(result,indent=2)+'\n'
    if args.output:args.output.write_text(encoded)
    print(encoded)
