#!/usr/bin/env python3
"""Candidate-only integer refinement; every positive result is checked exactly."""
from pathlib import Path
from fractions import Fraction as F
import importlib.util,json,sys,time
import numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint
from scipy.sparse import csc_matrix

HERE=Path(__file__).resolve().parent
BASE=HERE.parent
sys.path.insert(0,str(BASE))
spec=importlib.util.spec_from_file_location('quartic_complex_followup',BASE/'complex_semion.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
saved=json.loads((BASE/'R928_complex_semion.json').read_text())
original=module.mod.base.lp.verify
records=[]

def verify(A,b,decision):
    original(A,b,decision)
    case=saved['cases'][len(records)];n=case['metadata']['complex_phase_atoms']
    total=len(A[0]);start=time.monotonic()
    result=milp(np.zeros(total),integrality=np.array([1]*n+[0]*(total-n)),
                bounds=Bounds(np.zeros(total),np.full(total,np.inf)),
                constraints=LinearConstraint(csc_matrix(np.array(A,dtype=float)),np.array(b,dtype=float),np.array(b,dtype=float)),
                options={'time_limit':60.0,'mip_rel_gap':0.0})
    report={'pattern':case['metadata']['pattern'],'integer_phase_variables':n,
            'matrix_sha256':case['metadata']['matrix_sha256'],
            'rhs_sha256':case['metadata']['rhs_sha256'],
            'numerical_status':int(result.status),'numerical_message':str(result.message),
            'outcome':'no_exact_conclusion'}
    if result.x is not None:
        counts=[int(round(v))for v in result.x[:n]]
        if all(x>=0 for x in counts) and max(abs(x-y)for x,y in zip(counts,result.x[:n]))<1e-5:
            auxA=[row[n:]for row in A]
            auxb=[rhs-sum(c*x for c,x in zip(row[:n],counts))for row,rhs in zip(A,b)]
            aux=module.mod.base.lp.decide(auxA,auxb)
            if aux['status']=='exact_feasible_relaxation':
                original(auxA,auxb,aux)
                report.update(outcome='exact_integer_phase_feasible',phase_counts=[[j,c]for j,c in enumerate(counts)if c],auxiliary_certificate=aux)
    records.append(report)
    (HERE/'search.json').write_text(json.dumps({'scope':'Candidate search only; exact positive certificates, no exclusions from numerical negatives.','records':records},indent=2)+'\n')
    print('INTEGER',report['pattern'],report['outcome'],report['numerical_status'],round(time.monotonic()-start,2),flush=True)

module.mod.base.lp.verify=verify
sys.argv=['complex_semion.py']
module.main()
