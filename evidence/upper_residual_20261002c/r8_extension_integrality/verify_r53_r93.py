#!/usr/bin/env python3
"""Exact source and finite-group premises for the R53/R93 extension proof."""
import argparse
import itertools
import json
from pathlib import Path
import sys
import time

HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'supplements/rank8/data/rank8_tables.txt.gz').exists())
sys.path.insert(0,str(ROOT/'evidence/upper_residual_20261002b_recovery'))
from verify_recovery import read_source,validate_ring,fingerprint,require


def neutral():
    N=[[[0]*6 for _ in range(6)] for _ in range(6)]
    # 1,g,g^2,g^3,X,Y.
    for a,b in itertools.product(range(4),repeat=2):N[a][b][(a+b)%4]=1
    for a in range(4):
        for b in (4,5):N[a][b][b]=N[b][a][b]=1
    N[4][4]=[1,1,1,1,1,2]
    N[5][5]=[1,1,1,1,2,1]
    N[4][5]=N[5][4]=[0,0,0,0,2,2]
    return N


def group_check():
    # G=(F3)^2 semidirect C4, J(a,b)=(-b,a).
    elements=list(itertools.product(range(3),range(3),range(4)))
    def act(v,k):
        a,b=v
        for _ in range(k):a,b=-b%3,a
        return a,b
    def mul(x,y):
        a,b=act(y[:2],x[2]);return ((x[0]+a)%3,(x[1]+b)%3,(x[2]+y[2])%4)
    unit=(0,0,0)
    require(all(mul(mul(x,y),z)==mul(x,mul(y,z)) for x,y,z in itertools.product(elements,repeat=3)), 'semidirect group associativity')
    inverse={x:next(y for y in elements if mul(x,y)==mul(y,x)==unit) for x in elements}
    def generate(xs):
        H={unit};todo=list(xs)
        while todo:
            x=todo.pop()
            if x in H:continue
            H.add(x);old=list(H)
            todo += [mul(x,y) for y in old]+[mul(y,x) for y in old]+[inverse[x]]
        return frozenset(H)
    subgroups={frozenset([unit])};queue=list(subgroups)
    while queue:
        H=queue.pop()
        for x in elements:
            if x not in H:
                K=generate(list(H)+[x])
                if K not in subgroups:subgroups.add(K);queue.append(K)
    normal_abelian=[]
    for H in subgroups:
        require(all(mul(x,y) in H for x,y in itertools.product(H,repeat=2)), 'enumerated subgroup not closed')
        if (all(mul(x,y)==mul(y,x) for x,y in itertools.product(H,repeat=2))
                and all(mul(mul(x,h),inverse[x]) in H for x in elements for h in H)):
            normal_abelian.append(sorted(H))
    normal_abelian.sort(key=len)
    require(len(subgroups)==38, 'G36 subgroup exhaustion count')
    require([len(H) for H in normal_abelian]==[1,9], 'unexpected normal abelian stabilizer')
    require(all(act(v,k)!=v for v in itertools.product(range(3),repeat=2) if v!=(0,0) for k in (1,2,3)), 'C4 not fixed-point-free')
    return {'group_order':36,'all_subgroups_enumerated':len(subgroups),'normal_abelian_subgroups':normal_abelian,'bimodule_simple_dimensions':[1,3]}


def verify():
    start=time.monotonic();source=read_source(ROOT,8);B=neutral();validate_ring(B)
    receipts=[]
    for case,p in [('R8_2_53',[0,1,7,2,4,5]),('R8_2_93',[0,1,7,2,5,6])]:
        T=source[case];validate_ring(T);odd=[i for i in range(8) if i not in p]
        require(all(T[p[i]][p[j]][p[k]]==B[i][j][k] for i,j,k in itertools.product(range(6),repeat=3)), 'neutral full tensor mismatch')
        require(all(T[p[i]][p[j]][k]==0 for i,j in itertools.product(range(6),repeat=2) for k in odd), 'neutral not closed')
        grade=[int(i in odd) for i in range(8)]
        require(all(not T[i][j][k] or grade[k]==(grade[i]+grade[j])%2 for i,j,k in itertools.product(range(8),repeat=3)), 'faithful C2 grading fails')
        dims=[(0,3) if i in odd else (4,0) if i in p[4:] else (1,0) for i in range(8)]
        def mul(a,b):return a[0]*b[0]+2*a[1]*b[1],a[0]*b[1]+a[1]*b[0]
        require(all(mul(dims[i],dims[j])==tuple(sum(T[i][j][k]*dims[k][a] for k in range(8)) for a in (0,1)) for i,j in itertools.product(range(8),repeat=2)), 'dimension character fails')
        require(sum(mul(d,d)[0] for d in dims)==72 and sum(mul(dims[i],dims[i])[0] for i in p)==36, 'dimension totals')
        require(set(k for i in p for k in range(8) if T[i][i][k])==set(p), 'neutral adjoint support incomplete')
        receipts.append({'id':case,'source_sha256':fingerprint(T),'neutral_basis_map':p,'odd_basis':odd,'grading':grade,'dimensions_Z_sqrt2':dims})
    require([a for a in range(2,19,4) if 18%a==0]==[2,6,18], 'adjoint dimension possibilities')
    result={'status':'PASS','scope':'general_complex','source_witnesses':receipts,'neutral_dimension':36,'descent_type_dimension18':'1^2,2^4','proper_adjoint_dimensions':[2,6],'group_verification':group_check(),'python_optimized':not __debug__}
    result['seconds']=round(time.monotonic()-start,3)
    return result


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path);args=ap.parse_args();result=verify()
    if args.output:args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
