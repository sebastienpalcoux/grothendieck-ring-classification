#!/usr/bin/env python3
"""Check strict dimension boundaries by exhaustive multiplicity-one tensors.

The tensor presentation and canonicalization are shared with census export.
Associativity is checked by matrix commutation, and determinants are evaluated
by direct expansion, without the C++ elimination or Bareiss implementation.
"""
import argparse
import itertools
import json
from pathlib import Path
import subprocess
import tempfile
import time
from rank4 import tensor, canonical, require

ROOT=Path(__file__).resolve().parent

def determinant(A):
    if len(A)==1:
        return A[0][0]
    return sum((-1)**j*A[0][j]*determinant([r[:j]+r[j+1:] for r in A[1:]])
               for j in range(len(A)))

def commutes(A,B):
    return all(sum(A[i][k]*B[k][j]-B[i][k]*A[k][j] for k in range(4))==0
               for i,j in itertools.product(range(4),repeat=2))

def run():
    start=time.monotonic()
    rings={}
    assignments=0
    for tag,size in [('S',10),('N',6)]:
        for parameters in itertools.product(range(2),repeat=size):
            assignments+=1
            R=tensor(tag,parameters)
            if not all(commutes(R[i],R[j]) for i,j in [(1,2),(1,3),(2,3)]):
                continue
            rings[canonical(R)]=R
    reports=[]
    with tempfile.TemporaryDirectory(prefix='rank4-boundary-audit-') as temporary:
        executable=Path(temporary)/'enumerate'
        subprocess.run(['g++','-O3','-std=c++17',str(ROOT/'enumerate.cpp'),
                        '-o',str(executable)],check=True)
        for D in range(5,13):
            expected=set()
            equal=set()
            for key,R in rings.items():
                Q=[[D*int(i==j)-sum(R[k][i][z]*R[k][j][z]
                     for k,z in itertools.product(range(4),repeat=2))
                     for j in range(4)] for i in range(4)]
                minors=[determinant([row[:k] for row in Q[:k]]) for k in range(1,5)]
                if all(m>0 for m in minors):
                    expected.add(key)
                # All principal minors (not only leading minors) characterize
                # positive semidefiniteness, including repeated top roots.
                principal=[determinant([[Q[i][j] for j in subset] for i in subset])
                           for size in range(1,5)
                           for subset in itertools.combinations(range(4),size)]
                if all(m>=0 for m in principal) and minors[-1]==0:
                    equal.add(key)
            output=subprocess.run([str(executable),'1',str(D)],check=True,
                                  capture_output=True,text=True).stdout
            observed=[]
            for line in output.splitlines():
                tag,*parameters=line.split()
                observed.append(canonical(tensor(tag,list(map(int,parameters)))))
            require(len(observed)==len(set(observed)), 'duplicate boundary census ring')
            require(set(observed)==expected, 'strict dimension comparison differs at '+str(D))
            require(not equal.intersection(observed), 'equality admitted at '+str(D))
            reports.append({'exclusive_bound':D,'rings':len(observed),
                            'equality_cases_rejected':len(equal),'exact_set_equality':True})
    require(any(r['equality_cases_rejected'] for r in reports), 'no equality case exercised')
    return {'passed':True,'maximum_multiplicity':1,'parameter_assignments':assignments,
            'boundary_checks':reports,'seconds':round(time.monotonic()-start,3),
            'scope':'Shared tensor presentations and canonicalization; direct matrix commutation and determinant expansion; every exclusive integer bound from 5 through 12.'}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    report=run()
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
