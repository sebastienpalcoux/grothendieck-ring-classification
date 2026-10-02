#!/usr/bin/env python3
"""Exact source/module and A4 group premises for the two dimension24 cases."""
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
    T=[[[0]*6 for _ in range(6)] for _ in range(6)]
    for a,b in itertools.product(range(4),repeat=2):T[a][b][a^b]=1
    for a in range(4):
        for b in (4,5):T[a][b][b]=T[b][a][b]=1
    T[4][4][5]=T[5][5][4]=2
    T[4][5]=T[5][4]=[1,1,1,1,0,0]
    return T


def a4():
    elements=list(itertools.product(range(2),range(2),range(3)))
    def act(v,k):
        a,b=v
        for _ in range(k):a,b=b,a^b
        return a,b
    def mul(x,y):
        a,b=act(y[:2],x[2]);return x[0]^a,x[1]^b,(x[2]+y[2])%3
    unit=(0,0,0);inverse={x:next(y for y in elements if mul(x,y)==mul(y,x)==unit) for x in elements}
    require(all(mul(mul(x,y),z)==mul(x,mul(y,z)) for x,y,z in itertools.product(elements,repeat=3)),'A4 associativity')
    subgroups=[];normal_abelian=[]
    for flags in itertools.product((0,1),repeat=11):
        H={unit}|{elements[i+1] for i,v in enumerate(flags) if v}
        if not all(mul(x,y) in H for x,y in itertools.product(H,repeat=2)):continue
        subgroups.append(H)
        if all(mul(x,y)==mul(y,x) for x,y in itertools.product(H,repeat=2)) and all(mul(mul(x,h),inverse[x]) in H for x in elements for h in H):normal_abelian.append(sorted(H))
    normal_abelian.sort(key=len)
    require([len(H) for H in normal_abelian]==[1,4],'A4 normal abelian subgroup orders')
    require(len(subgroups)==10,'A4 subgroup exhaustion')
    # Aut(V4) is GL(2,2); exactly two automorphisms have order three.
    autos=[];order_three=[]
    points=list(itertools.product(range(2),repeat=2))
    for a,b,c,d in itertools.product(range(2),repeat=4):
        if (a*d-b*c)%2!=1:continue
        f=lambda v:((a*v[0]+b*v[1])%2,(c*v[0]+d*v[1])%2)
        autos.append([a,b,c,d])
        if all(f(f(f(v)))==v for v in points) and any(f(v)!=v for v in points):order_three.append([a,b,c,d])
    require(len(autos)==6 and len(order_three)==2,'V4 order3 action alternatives')
    return {'group_order':12,'all_subgroups_enumerated':len(subgroups),'normal_abelian_subgroups':normal_abelian,'bimodule_simple_dimensions':[1,2],'Aut_V4_order':6,'order_three_actions':order_three}


def verify():
    start=time.monotonic();S=read_source(ROOT,8);B=neutral();validate_ring(B);witnesses=[]
    for case,p in [('R8_2_191',[0,5,6,7,3,4]),('R8_2_299',[0,5,6,7,1,2])]:
        T=S[case];validate_ring(T);odd=[i for i in range(8) if i not in p];units=p[:4]
        require(all(T[p[i]][p[j]][p[k]]==B[i][j][k] for i,j,k in itertools.product(range(6),repeat=3)),'neutral full tensor')
        require(all(T[p[i]][p[j]][k]==0 for i,j in itertools.product(range(6),repeat=2) for k in odd),'neutral closure')
        grade=[int(i in odd) for i in range(8)]
        require(all(not T[i][j][k] or grade[k]==(grade[i]+grade[j])%2 for i,j,k in itertools.product(range(8),repeat=3)),'ambient faithful C2 grading')
        neutral_grade=[0,0,0,0,1,2]
        require(all(not B[i][j][k] or neutral_grade[k]==(neutral_grade[i]+neutral_grade[j])%3 for i,j,k in itertools.product(range(6),repeat=3)),'neutral faithful C3 grading')
        actions=[[next(k for k in range(8) if T[g][m][k]) for m in odd] for g in units]
        require(all(T[g][m]==[int(k==actions[a][b]) for k in range(8)] for a,g in enumerate(units) for b,m in enumerate(odd)),'unit acts as permutation')
        require({row[0] for row in actions}==set(odd),'pointed module not transitive')
        stabilizer=[g for g,row in zip(units,actions) if row[0]==odd[0]]
        require(len(stabilizer)==2,'rank2 pointed stabilizer size')
        dims=[(0,1) if i in odd else (2,0) if i in p[4:] else (1,0) for i in range(8)]
        def mul(a,b):return a[0]*b[0]+6*a[1]*b[1],a[0]*b[1]+a[1]*b[0]
        require(all(mul(dims[i],dims[j])==tuple(sum(T[i][j][k]*dims[k][a] for k in range(8)) for a in (0,1)) for i,j in itertools.product(range(8),repeat=2)),'positive exact dimension character')
        require(sum(mul(d,d)[0] for d in dims)==24,'ambient dimension24')
        # The nonneutral D-action maps either odd object to the sum of both.
        require(all(T[x][m]==[int(k in odd) for k in range(8)] for x in p[4:] for m in odd),'D action on rank2 module')
        witnesses.append({'id':case,'source_sha256':fingerprint(T),'neutral_basis_map':p,'odd_basis':odd,'pointed_group_action':actions,'pointed_module_stabilizer':stabilizer,'dimensions_Z_sqrt6':dims})
    result={'status':'PASS','scope':'general_complex','source_witnesses':witnesses,'group_verification':a4(),'python_optimized':not __debug__};result['seconds']=round(time.monotonic()-start,3);return result


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path);args=ap.parse_args();result=verify()
    if args.output:args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
