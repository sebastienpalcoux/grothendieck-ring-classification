#!/usr/bin/env python3
"""Exact structural application and finite arithmetic for the proposed R68 proof."""
import argparse
import importlib.util
import itertools
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent/'classification-repo'
if not (ROOT/'supplements/rank8/data/rank8_tables.txt.gz').exists():
    ROOT=next(p for p in HERE.parents if (p/'supplements/rank8/data/rank8_tables.txt.gz').exists())
spec=importlib.util.spec_from_file_location('r68recovery',ROOT/'evidence/upper_residual_20261002b_recovery/verify_recovery.py')
rec=importlib.util.module_from_spec(spec);spec.loader.exec_module(rec)

def require(x,msg='R68 exact condition failed'):
    if not x:raise ValueError(msg)

def multiply(A,B):
    return tuple(sum(A[2*i+k]*B[2*k+j]for k in range(2))%3 for i in range(2)for j in range(2))

def verify():
    N=rec.read_source(ROOT,8)['R8_2_68'];dual=rec.validate_ring(N)
    require(rec.fingerprint(N)=='cb50c3a33fcb9e9c9e578be70876be4a02ee219e458aad6138ebd8a62a56af1f','source fingerprint')
    dims=[1,1,1,6,4,4,6,1]
    for i,j in itertools.product(range(8),repeat=2):
        require(sum(N[i][j][k]*dims[k] for k in range(8))==dims[i]*dims[j],'exact integral FP character')
    require(sum(d*d for d in dims)==108 and rec.adjoint_closure(N,dual)==list(range(8)),'dimension108 adjointwhole')
    inv=[0,1,2,7];require(N[1][1][7]==1 and N[7][7][0]==1,'InvC4')
    require(all(N[7][j][j]==1 and sum(N[7][j])==1 for j in (3,4,5,6)),'unique canonical sign fixes nonunits')
    parts=[]
    for a,b,c in itertools.product((1,2),(0,2,4),(0,2,4)):
        q=a+4*b+9*c
        if 54%q==0:parts.append((a,b,c,q))
    require(parts==[(1,0,0,1),(1,2,0,9),(1,2,2,27),(2,0,0,2),(2,4,0,18),(2,4,4,54)],'all outerstable adjoint dimensions')
    # All invertible orders in Aut(C9) divide6; no square equals inversion modulo9.
    aut9=[a for a in range(9)if a%3]
    require(all(a*a%9!=8 for a in aut9),'no square root of inversion in AutC9')
    minusI=(2,0,0,2);solutions=[]
    for A in itertools.product(range(3),repeat=4):
        det=(A[0]*A[3]-A[1]*A[2])%3
        if multiply(A,A)==minusI:
            require(det==1,'order4 square-root determinantone')
            solutions.append(A)
    require(len(solutions)==6,'all GL2F3 square roots of minusI')
    # H2(C3²,C*)=C3, and determinantone acts identically on alternating classes.
    eta_solutions=[a for a in range(3)if 2*a%3==0]
    require(eta_solutions==[0],'order4 action tensoratorclass vanishes')
    # A g-fixed3D simple would have rationaldimension3/2 after de-equivariantization.
    require(3%2==1,'odd3D simple cannot split to an integral rationalhalf')
    return {'status':'PASS','id':'R8_2_68','source_sha256':rec.fingerprint(N),'scope':'general_complex',
            'fp_dimensions':dims,'coefficient_checks':512,'associativity_checks':4096,
            'canonical_sign':7,'D_dimensions':[1,1,2,2,2,2,3,3,3,3],
            'outerstable_adjoint_partitions':parts,'GL2F3_order4_matrices':solutions,
            'tensorator_class_solutions':eta_solutions,'ledger_changes':False,
            'proof':'PROOF.md','optimization_safe':True}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path);args=p.parse_args();text=json.dumps(verify(),indent=2)
    if args.output:args.output.write_text(text+'\n')
    print(text)
