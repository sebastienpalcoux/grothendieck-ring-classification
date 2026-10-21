#!/usr/bin/env python3
"""Independent exact checks of central-moment restriction and Toeplitz code.

The rational DP summary is checked against both the frozen rank-six RREF
enumerator exposed by weighted_rank8.core and complete bounded Cartesian
enumeration. No LP is run. Default receipt replay is read-only; --write is
required to regenerate the deterministic validation receipt.
"""
from fractions import Fraction
import argparse
import hashlib
import inspect
import itertools
import json
import math
from pathlib import Path
import sympy as s
import central_moments as subject
import weighted_rank8 as w
from exact import Embedding,field,require,t

HERE=Path(__file__).resolve().parent

def digest(value):
    return hashlib.sha256(json.dumps(value,separators=(',',':')).encode()).hexdigest()

def restriction_checks():
    polynomial=s.Poly(t-1,t,domain=s.QQ)
    K=field(polynomial)
    embedding=Embedding(polynomial,(1,1))
    records=[]
    for n in range(2,9):
        for pattern in range(3):
            dimensions=[1]+[1 if pattern==0 else 1+i%3 if pattern==1 else 2+i%4
                            for i in range(1,n)]
            for m in [1,2]:
                B=s.zeros(n)
                for i in range(1,n):
                    first=2 if pattern!=1 else i%3
                    diagonal=2 if pattern!=2 else i%3
                    B[i,i]=diagonal*diagonal
                    B[0,i]=B[i,0]=0 if not diagonal else m*first+(i%m)
                # The arrow-shaped fixture is genuinely positive semidefinite.
                B[0,0]=1+sum(s.ceiling(B[0,i]**2/B[i,i]) for i in range(1,n) if B[i,i])
                bounds=[min(int(B[0,i])//m,math.isqrt(int(B[i,i]))) for i in range(1,n)]
                ceiling=sum(d*b for d,b in zip(dimensions[1:],bounds))
                remainders=sorted(set([s.Rational(-2),s.Rational(-1),s.Rational(0),
                                      s.Rational(1,2),s.Rational(1),s.Rational(3,2),s.Rational(2),
                                      s.Rational(ceiling//2),s.Rational(ceiling),s.Rational(ceiling+1)]))
                for remainder in remainders:
                    beta=K(m+remainder);ds=[K(d) for d in dimensions]
                    a={'K':K,'embedding':embedding,'Gram':B,'ds':ds}
                    original_gram=B.copy()
                    columns=w.core.restriction(ds,beta,m,K,B)
                    brute=sorted((m,)+values for values in itertools.product(*(range(b+1) for b in bounds))
                                 if sum(d*v for d,v in zip(dimensions[1:],values))==remainder)
                    require(columns==brute,'frozen RREF enumeration differs from complete bounded box')
                    expected=(len(columns),tuple(min(c[i] for c in columns) for i in range(n)) if columns else None)
                    actual=subject.restriction(a,beta,m)
                    require(actual==expected,'central DP count/minimum mismatch')
                    require(B==original_gram,'subject mutated the original Gram matrix')
                    records.append({'rank':n,'dimension_pattern':pattern,'dimensions':dimensions,'multiplicity':m,
                                    'beta':str(m+remainder),'original_Gram':[[int(B[i,j]) for j in range(n)] for i in range(n)],
                                    'original_coordinate_bounds':bounds,'complete_cartesian_box_size':math.prod(b+1 for b in bounds),
                                    'column_count':expected[0],'coordinate_minima':list(expected[1]) if expected[1] is not None else None,
                                    'complete_column_list_sha256':digest(columns)})
    require(set(r['rank'] for r in records)==set(range(2,9)),'rank coverage missing')
    require(set(r['multiplicity'] for r in records)=={1,2},'multiplicity coverage missing')
    require(any(r['column_count']==0 for r in records) and any(r['column_count']>1 for r in records),'empty/multiple-column cases missing')
    require(max(r['complete_cartesian_box_size'] for r in records)<=3**7,'fixture enumeration not modest')
    return records

def toeplitz_checks():
    T,L,D,nu=s.symbols('T L D nu',real=True)
    h=nu*D
    matrix=s.Matrix([[T-L,-L,h-L],[-L,T-L,-L],[h-L,-L,T-L]])
    formulas=[T-L,T*T-2*T*L,T*T-h*h-2*L*(T-h),
              (T-h)*(T*(T+h)-L*(3*T+h))]
    records=[]
    for size in range(1,4):
        for indices in itertools.combinations(range(3),size):
            actual=matrix.extract(indices,indices).det()
            slot=0 if size==1 else 3 if size==3 else 2 if indices==(0,2) else 1
            require(s.expand(actual-formulas[slot])==0,'Toeplitz principal minor identity failed')
            records.append({'principal_indices':list(indices),'formula_index':slot,
                            'direct_determinant_expanded':str(s.expand(actual)),
                            'verified_factored_formula':str(s.factor(formulas[slot]))})
    require(len(records)==7 and {r['formula_index'] for r in records}=={0,1,2,3},'incomplete Toeplitz minors')
    return {'matrix':[[str(matrix[i,j]) for j in range(3)] for i in range(3)],
            'distinct_formulas':[str(s.factor(v)) for v in formulas],'principal_minors':records,
            'scope':'symbolic polynomial identities for all real T,L,D,nu; no indicator or categorification assumption'}

def validate():
    cases=restriction_checks()
    return {'result':'PASS','scope':'independent arithmetic validation only; no LP or classification decision',
            'subject_restriction_source_sha256':hashlib.sha256(inspect.getsource(subject.restriction).encode()).hexdigest(),
            'frozen_reference_restriction_source_sha256':hashlib.sha256(inspect.getsource(w.core.restriction).encode()).hexdigest(),
            'rational_restriction_method':'optimized DP versus frozen RREF enumeration and complete original-Gram bounded Cartesian enumeration',
            'rational_fixture_count':len(cases),'rational_fixtures':cases,'toeplitz':toeplitz_checks()}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write',action='store_true',help='explicitly regenerate the deterministic receipt')
    args=parser.parse_args();result=validate();path=HERE/'central_moments_validation.json'
    if args.write:path.write_text(json.dumps(result,indent=2)+'\n')
    else:require(json.loads(path.read_text())==result,'central moment validation receipt changed')
    print(json.dumps({'result':'PASS','rational_fixtures':result['rational_fixture_count'],
                      'symbolic_principal_minors':7,'mode':'write' if args.write else 'read_only_replay'}),flush=True)

if __name__=='__main__':main()
