#!/usr/bin/env python3
"""Source hypotheses for the Galois-invariant R312 general exclusion."""
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

def pseudo_psu():
    N=[[[0]*4 for _ in range(4)] for _ in range(4)]
    for i in range(4):N[0][i][i]=N[i][0][i]=1
    N[1][1][0]=1
    for i,j in ((1,2),(2,1)):N[i][j][3]=1
    for i,j in ((1,3),(3,1)):N[i][j][2]=1
    N[2][2]=N[3][3]=[0,1,1,1]
    N[2][3]=N[3][2]=[1,0,1,1]
    return N

def verify():
    start=time.monotonic();source=read_source(ROOT,8);T=source['R8_2_312'];validate_ring(T)
    B=pseudo_psu();validate_ring(B)
    # Exact dimension arithmetic in Z[sqrt(2)].
    dims=[(1,0),(1,0),(1,1),(1,1)]
    def mul(a,b):return (a[0]*b[0]+2*a[1]*b[1],a[0]*b[1]+a[1]*b[0])
    for i,j in itertools.product(range(4),repeat=2):
        require(tuple(sum(B[i][j][k]*dims[k][v] for k in range(4)) for v in (0,1))==mul(dims[i],dims[j]),'exact two-dimension character')
    maps=[]
    for tail in itertools.permutations(range(1,8),3):
        p=(0,)+tail
        if all(T[p[i]][p[j]][p[k]]==B[i][j][k] for i,j,k in itertools.product(range(4),repeat=3)) and all(T[p[i]][p[j]][k]==0 for i,j in itertools.product(range(4),repeat=2) for k in range(8) if k not in p):maps.append(list(p))
    require(maps,'pseudo-PSU subring absent')
    witnesses=[]
    for p in maps:
        g=p[1]
        fixed=[m for m in range(8) if m not in p and T[g][m]==[int(k==m) for k in range(8)]]
        require(fixed,'rank-one pointed module absent')
        witnesses.append({'subring_map':p,'g':g,'fixed_outside':fixed})
    # H3(C2) normal forms have a single nontrivial scalar. A normalized
    # two-cochain has dpsi(g,g,g)=1 irrespective of psi(g,g).
    for sigma in (-1,1):
        def omega(a,b,c):return sigma if a==b==c==1 else 1
        for a,b,c,d in itertools.product(range(2),repeat=4):
            require(omega(b,c,d)*omega(a,(b+c)%2,d)*omega(a,b,c)==omega((a+b)%2,c,d)*omega(a,b,(c+d)%2),'C2 cocycle')
    result={'status':'PASS','id':'R8_2_312','scope':'general_complex','source_sha256':fingerprint(T),'two_dimension_nonunit':'1+sqrt(2)','witnesses':witnesses,'pointed_cocycle_class_forced':-1,'rank_one_module_requires':1,'galois_invariant_scalars':[-1,1],'python_optimized':not __debug__,'seconds':round(time.monotonic()-start,3)}
    return result

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path);args=ap.parse_args();r=verify()
    if args.output:args.output.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps(r,indent=2))
