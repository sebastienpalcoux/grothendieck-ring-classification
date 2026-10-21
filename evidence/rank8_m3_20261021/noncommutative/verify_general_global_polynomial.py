#!/usr/bin/env python3
"""Independent exact validation of the global engine's biquadratic minpoly.

This consolidates the criteria review's 324 fixtures. The independent
reference is the squarefree characteristic polynomial of the rational
multiplication matrix, not the engine's sparse-support/Newton procedure.
Default execution only reads and compares the receipt; --write regenerates.
"""
from fractions import Fraction
import argparse
import itertools
import json
from pathlib import Path
import sys
import sympy as s

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'criteria'))
import global_induction as engine

def require(condition,message):
    if not condition: raise ValueError(message)

def validate():
    reports=[]
    for q,r in [(2,3),(3,5),(3,7),(3,13)]:
        def multiply(a,b):
            out=[Fraction(0)]*4
            for i,x in enumerate(a):
                for j,y in enumerate(b):
                    out[i^j]+=x*y*(q if i&j&1 else 1)*(r if i&j&2 else 1)
            return tuple(out)
        cases=[]
        for value in itertools.product((-1,0,1),repeat=4):
            columns=[multiply(value,tuple(int(i==j) for i in range(4))) for j in range(4)]
            matrix=s.Matrix.hstack(*(s.Matrix(column) for column in columns))
            characteristic=matrix.charpoly().as_poly()
            reference=characteristic.sqf_part().monic()
            expected=[Fraction(str(c)) for c in reference.all_coeffs()]
            actual=engine.biquadratic_polynomial(value,multiply)
            require(actual==expected,'minimal polynomial mismatch '+str((q,r,value)))
            cases.append({'value':list(value),
                          'multiplication_matrix':[[str(matrix[i,j]) for j in range(4)] for i in range(4)],
                          'characteristic_polynomial':[str(c) for c in characteristic.all_coeffs()],
                          'minimal_polynomial':[str(c) for c in actual]})
        require(len(cases)==81,'incomplete coefficient cube')
        reports.append({'radicands':[q,r],'exact_checks':len(cases),'cases':cases})
    require(sum(r['exact_checks'] for r in reports)==324,'incomplete field coverage')
    return {'result':'PASS','fixture_count':324,
            'scope':'minimal-polynomial routine only; no LP feasibility or categorification conclusion',
            'method':'independent exact rational 4x4 multiplication matrix; monic squarefree characteristic polynomial',
            'coefficient_cube':[-1,0,1],'reports':reports}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write',action='store_true',help='explicitly regenerate the deterministic receipt')
    args=parser.parse_args();result=validate()
    destination=HERE/'general_global_polynomial_validation.json'
    if args.write: destination.write_text(json.dumps(result,indent=2)+'\n')
    else: require(json.loads(destination.read_text())==result,'saved polynomial receipt does not replay')
    print(json.dumps({'result':'PASS','fixture_count':324,'fields':[r['radicands'] for r in result['reports']],
                      'mode':'write' if args.write else 'read_only_replay'}))

if __name__=='__main__': main()
