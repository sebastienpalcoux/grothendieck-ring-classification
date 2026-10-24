#!/usr/bin/env python3
"""Exploratory even cyclic stabilizer characters, with exact positive witnesses.

The input is the pinned published R155 generalized cyclic spectra. The
mathematical even-cycle character derivation is recorded separately. A failed
MILP is NOT by itself a categorical exclusion. Every returned positive witness
is checked using Python integers, including the large uniform subtraction.
"""
from collections import Counter
from pathlib import Path
import argparse, hashlib, json
import numpy as np
import sympy as sp
from scipy.optimize import Bounds, LinearConstraint, milp

PIN='b76cdb3fbc8c4cc6c23d3e177be26d0a74d1adab114069b9e40b04b62678fca7'
BASES={}

def spectra(n):
    if n<4 or n%2: raise ValueError('even n>=4 required')
    m=n//2
    even=Counter(); odd=Counter(); exchanged=Counter()
    for mask in range(1<<m):
        s=sum(2*a+1 for a in range(m) if mask>>a&1)
        if mask.bit_count()%2: odd[((1-s)//2)%n]+=1
        else: even[(-s//2)%n]+=1
    for mask in range(1<<(m-1)):
        s=sum(a+1 for a in range(m-1) if mask>>a&1)
        exchanged[(-s)%n]+=1; exchanged[(m-s)%n]+=1
    result=[[c[i] for i in range(n)] for c in (even,odd,exchanged)]
    if list(map(sum,result)) != [2**(m-1),2**(m-1),2**m]:
        raise ValueError('character dimensions')
    return result

def columns(n):
    specs=spectra(n)
    return [[s[(i-k)%n] for i in range(n)] for s in specs for k in range(n)]

def check(n, values):
    cols=columns(n); degree=sum(cols[0])
    # For large spectra, first solve rationally and round an exact particular
    # solution. The remaining integer correction has small coefficients.
    # This prevents false numerical infeasibility at 10^12-scale right sides.
    if max(values)>10**8:
        if n not in BASES:
            A=sp.Matrix(cols).T
            pivots=A.rref()[1]
            if len(pivots)!=n: raise ValueError('character span not full')
            BASES[n]=(pivots,A[:,list(pivots)].inv())
        pivots,inverse=BASES[n]
        uniform=min(values)//(4*degree)
        centered=sp.Matrix([v-4*degree*uniform for v in values])
        rational=inverse*centered
        baseline=[uniform]*len(cols)
        for k,v in zip(pivots,rational): baseline[k]+=int(sp.floor(v))
        residual=[values[i]-sum(cols[k][i]*baseline[k] for k in range(len(cols))) for i in range(n)]
        if min(baseline)>10000:
            matrix=np.array(cols,dtype=float).T
            result=milp(np.zeros(len(cols)),integrality=np.ones(len(cols)),
                        bounds=Bounds(-10000,10000),
                        constraints=LinearConstraint(matrix,residual,residual),
                        options={'time_limit':10,'mip_rel_gap':0})
            if result.x is not None:
                witness=[baseline[k]+int(round(v)) for k,v in enumerate(result.x)]
                if min(witness)>=0 and all(sum(cols[k][i]*witness[k] for k in range(len(cols)))==values[i] for i in range(n)):
                    return {'status':'exact_positive_witness','uniform':0,'witness':witness,'method':'exact_rational_rounding_then_bounded_integer_correction'}
    # Sum of all cyclic shifts of the first character is the constant degree
    # vector. Removing copies therefore records an exact positive summand.
    # Keep a conservative buffer: removing the largest possible uniform part
    # can itself destroy feasibility, since inverse spin characters have signs.
    uniform=max(0,min(values)//degree-(max(values)-min(values)+1))
    residual=[v-uniform*degree for v in values]
    if max(residual)>2**49: raise ValueError('float search domain too large')
    matrix=np.array(cols,dtype=float).T
    result=milp(np.zeros(len(cols)),integrality=np.ones(len(cols)),
                bounds=Bounds(0,np.inf),
                constraints=LinearConstraint(matrix,residual,residual),
                options={'time_limit':10,'mip_rel_gap':0})
    if result.x is None:
        return {'status':'no_witness','solver_status':int(result.status),
                'message':result.message,'uniform':uniform,'residual':residual}
    witness=[int(round(v)) for v in result.x]
    if min(witness)<0 or any(sum(cols[k][i]*witness[k] for k in range(len(cols)))!=residual[i] for i in range(n)):
        return {'status':'unverified_numeric_witness','solver_status':int(result.status),
                'uniform':uniform,'residual':residual}
    return {'status':'exact_positive_witness','uniform':uniform,'witness':witness}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input',type=Path);parser.add_argument('output',type=Path)
    args=parser.parse_args();raw=args.input.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=PIN: raise ValueError('source hash mismatch')
    source=json.loads(raw)['rows']
    rows=[r for r in source if r['n']>=4 and r['n']%2==0 and r['base_simple'] in (1,2)]
    if len(rows)!=1144: raise ValueError('incomplete scope')
    output={'input_sha256':PIN,'scope':'Even cyclic Clifford character constraint only. No categorification conclusion.','rows':[]}
    for n in range(4,25,2):
        scoped=[r for r in rows if r['n']==n]
        counts=Counter()
        for r in scoped:
            values=list(map(int,r['multiplicities']))
            if sum(values)!=r['dimension']:raise ValueError('dimension mismatch')
            answer=check(n,values);counts[answer['status']]+=1
            answer.update({k:r[k] for k in ('n','base_simple','central_simple','dimension')})
            output['rows'].append(answer)
        print(n,dict(counts),flush=True)
        args.output.write_text(json.dumps(output,indent=2)+'\n')

if __name__=='__main__':main()
