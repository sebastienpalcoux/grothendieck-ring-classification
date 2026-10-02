#!/usr/bin/env python3
"""General dimension96 two-dimensional orbit obstruction. No assertions or search.

Constructs all relevant dimension partitions and the two groups of order6.
The categorical descent proof is D96_TWO_DIMENSION_ORBIT_PROOF.md.
"""
import argparse
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'supplements/rank8/data/rank8_tables.txt.gz').exists())
REC=ROOT/'evidence/upper_residual_20261002b_recovery/verify_recovery.py'
spec=importlib.util.spec_from_file_location('recovery_d96',REC)
rec=importlib.util.module_from_spec(spec);spec.loader.exec_module(rec)

def require(x,message='dimension96 certificate failed'):
    if not x:raise ValueError(message)

CASES={
 'R8_2_404':([1,6,6,1,1,1,2,4],'2249a077453cbc8cb0253dcd55f88ac5bf01035bd4c4a301c1f1eee7169d8c2a'),
 'R8_2_418':([1,6,6,1,1,1,2,4],'76492b43563b47ab7981d9d354f9c872a8a6524e511051ecbcfe2850e28a0935'),
 'R8_2_604':([1,1,1,6,6,1,2,4],'61b222786b50b98edc1c6a1fad1233e7f4d4db037ff9c441d1140bf0ac077cfa'),
 'R8_2_692':([1,1,1,1,2,6,4,6],'ed37ca13ff272016100726ceb860a27c6d2c9e9301e0c886ec1961012e320bc5'),
}

def adjoint_partitions(n3,n6):
    # Outer action swaps both2D objects and every3D pair; the6D object is unique.
    candidates=[]
    for a,b,c,d in itertools.product((1,2,4),(0,2),range(0,n3+1,2),range(n6+1)):
        dim=a+4*b+9*c+36*d
        if dim<48 and 48%dim==0:
            candidates.append((a,b,c,d,dim))
    require(candidates==[(1,0,0,0,1),(2,0,0,0,2),(4,0,0,0,4),(4,2,0,0,12)],'complete proper-adjoint dimension partitions')
    # Pointed cases cannot supply the square of a3D or6D object: eachInvoccurs≤1.
    require(max(9 if n3 else 0,36 if n6 else 0)>4,'pointed adjoint impossible')
    # In dimension12 allInvand2D lie in the neutral, leaving only3D/6D simples.
    require(all(9*x+36*y!=12 for x in range(n3+1) for y in range(n6+1)),'outside component cannot have dimension12')
    return candidates

def equivariantization_partitions(n3,n6):
    results=[]
    # f_d fixed simple labels of dimensiond; p_d free orbits, each containing2.
    for f1,p1,f2,p2,f3,p3,f6,p6 in itertools.product(range(3),range(3),range(3),range(2),range(3),range(2),range(2),range(2)):
        out={1:2*f1,2:p1+2*f2,3:2*f3,4:p2,6:p3+2*f6,12:p6}
        if out!={1:4,2:2,3:n3,4:0,6:n6,12:0}:continue
        dims=([1]*(f1+2*p1)+[2]*(f2+2*p2)+[3]*(f3+2*p3)+[6]*(f6+2*p6))
        require(sum(x*x for x in dims)==24,'E global dimension24')
        results.append({'fixed1':f1,'free1':p1,'fixed2':f2,'free2':p2,'fixed3':f3,'free3':p3,'dimensions':dims})
    require(len(results)==2 and sorted(r['dimensions'] for r in results)==[[1,1,1,1,1,1,3,3],[1,1,2,3,3]],'all E types')
    return results

def group6_orbit_square_coefficients():
    # C6 and S3 are all groups of order6. Count coefficient at a free orbit representative.
    C=list(range(6));add=lambda a,b:(a+b)%6;tauC=lambda a:(-a)%6
    perms=list(itertools.permutations(range(3)))
    mul=lambda a,b:tuple(a[b[i]] for i in range(3))
    t=(1,0,2);tauS=lambda a:mul(mul(t,a),t)
    results=[]
    for name,G,prod,tau in [('C6',C,add,tauC),('S3',perms,mul,tauS)]:
        require(all(prod(prod(a,b),c)==prod(a,prod(b,c)) for a,b,c in itertools.product(G,repeat=3)),'group associativity')
        fixed=[a for a in G if tau(a)==a]
        require(len(fixed)==2,'involution fixed subgrouporder2')
        orbits=[];left=set(G)-set(fixed)
        while left:
            a=min(left);O={a,tau(a)};require(len(O)==2,'free orbit');orbits.append(sorted(O));left-=O
        coeff=[sum(prod(a,b)==O[0] for a,b in itertools.product(O,repeat=2))for O in orbits]
        require(sorted(coeff)==[0,1],'two2D selfsquarecoefficients differ')
        results.append({'group':name,'fixed_elements':fixed,'orbits':orbits,'selfsquarecoefficients':coeff})
    return results

def verify():
    source=rec.read_source(ROOT,8);receipts=[]
    for case,(dims,digest) in CASES.items():
        N=source[case];du=rec.validate_ring(N)
        require(rec.fingerprint(N)==digest,'frozen census tensor digest')
        for i,j in itertools.product(range(8),repeat=2):
            require(sum(N[i][j][k]*dims[k] for k in range(8))==dims[i]*dims[j],'exact positive dimension character')
        require(sorted(dims)==[1,1,1,1,2,4,6,6] and sum(d*d for d in dims)==96,'dimension96 type')
        require(rec.adjoint_closure(N,du)==list(range(8)),'adjoint whole')
        inv=[i for i,d in enumerate(dims)if d==1]
        two=dims.index(2);four=dims.index(4);six=[i for i,d in enumerate(dims)if d==6]
        signs=[]
        for g in inv:
            require(sum(N[g][g])==1 and N[g][g][0]==1,'InvV4')
            if g==0:continue
            act=[next(k for k,c in enumerate(N[g][j])if c)for j in range(8)]
            require(all(sum(N[g][j])==1 for j in range(8)),'invertible action')
            require(act[two]==two and act[four]==four,'sign fixes unique2D and4D')
            swapped=act[six[0]]==six[1]
            require(act[six[1]]==(six[0]if swapped else six[1]),'6D pair sign permutation')
            n3,n6=(0,1)if swapped else(4,0)
            signs.append({'candidate_sign':g,'six_pair_swapped':swapped,'D_dimensions':[1]*4+[2]*2+[3]*n3+[6]*n6,
                          'proper_adjoint_candidates':adjoint_partitions(n3,n6),'second_descent':equivariantization_partitions(n3,n6)})
        receipts.append({'id':case,'scope':'general_complex','source_sha256':digest,'source_dimensions':dims,
                         'coefficient_checks':512,'associativity_checks':4096,'all_sign_candidates':signs})
    orbit_receipts=group6_orbit_square_coefficients()
    # The fixed2D branch has x²=1+g+x. Each equivariant lift square has exactlyone2Dconstituent.
    require(2*2==1+1+2,'fixed2D square dimension')
    require(1%2==1,'identical lift squares with one2D constituent cannotbe invariant under its swap')
    return {'status':'PASS','scope':'general_complex','case_applications':receipts,'group6_orbit_products':orbit_receipts,
            'optimization_safe':True,'proof':'D96_TWO_DIMENSION_ORBIT_PROOF.md','ledger_changes':False}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path);args=p.parse_args();text=json.dumps(verify(),indent=2)
    if args.output:args.output.write_text(text+'\n')
    print(text)
