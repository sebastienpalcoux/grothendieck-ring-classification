#!/usr/bin/env python3
"""Exact LP-leaf integer branching; numerical outcomes alone never certify a cut."""
from pathlib import Path
from fractions import Fraction as F
import importlib.util,json,sys,time,math
from flint import fmpq_mat

HERE=Path(__file__).resolve().parent;BASE=HERE.parent
sys.path.insert(0,str(BASE))
spec=importlib.util.spec_from_file_location('quartic_branch_followup',BASE/'complex_semion.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
saved=json.loads((BASE/'R928_complex_semion.json').read_text())
search=json.loads((HERE/'search.json').read_text())
original=module.mod.base.lp.verify
records=[]

def need(c,m):
    if not c:raise ValueError(m)

def solve(A,b,n,limit=150):
    start=time.monotonic();nodes=0
    def child(A,b,j,k,lower):
        row=[0]*(len(A[0])+1);row[j]=1;row[-1]=-1 if lower else 1
        return [v+[0]for v in A]+[row],b+[k]
    def rec(A,b):
        nonlocal nodes
        nodes+=1
        if nodes>1000 or time.monotonic()-start>limit:return {'status':'unfinished'}
        decision=module.mod.base.lp.decide(A,b)
        if decision['status'] not in ('exact_feasible_relaxation','exact_infeasible_relaxation'):
            return {'status':'unfinished','reason':decision['status']}
        original(A,b,decision)
        if decision['status']=='exact_infeasible_relaxation':return {'status':'infeasible','certificate':decision}
        p={j:F(v)for j,v in decision['primal']};fractional=[j for j,v in p.items()if j<n and v.denominator!=1]
        if not fractional:return {'status':'integer_feasible','certificate':decision}
        bounds={j:None for j in fractional}
        for row,rhs in zip(A,b):
            if rhs<0 or any(x<0 for x in row):continue
            for j in fractional:
                if row[j]>0:
                    value=F(rhs,row[j]);bounds[j]=value if bounds[j] is None else min(bounds[j],value)
        j=min(fractional,key=lambda j:(bounds[j]if bounds[j]is not None else 10**9,-min(p[j]%1,1-p[j]%1)))
        floor=p[j].numerator//p[j].denominator
        left=rec(*child(A,b,j,floor,False))
        if left['status']=='integer_feasible':return {'status':'integer_feasible','variable':j,'floor':floor,'left':left}
        right=rec(*child(A,b,j,floor+1,True))
        status='infeasible'if left['status']==right['status']=='infeasible'else 'integer_feasible'if right['status']=='integer_feasible'else 'unfinished'
        return {'status':status,'variable':j,'floor':floor,'left':left,'right':right}
    tree=rec(A,b)
    return tree,nodes

def verify(A,b,decision):
    original(A,b,decision)
    case=saved['cases'][len(records)];n=case['metadata']['complex_phase_atoms'];N=len(A[0]);m=len(A)
    report={'pattern':case['metadata']['pattern'],'matrix_sha256':case['metadata']['matrix_sha256'],'rhs_sha256':case['metadata']['rhs_sha256']}
    if search['records'][len(records)]['outcome']=='exact_integer_phase_feasible':
        report['outcome']='positive_certificate_in_search_json'
    else:
        zero=set();deductions=[]
        while True:
            changed=False
            for i,(row,rhs)in enumerate(zip(A,b)):
                if rhs:continue
                support=[j for j,v in enumerate(row)if v and j not in zero]
                if support and (all(row[j]>0 for j in support)or all(row[j]<0 for j in support)):
                    zero.update(support);deductions.append({'row':i,'new_zero_columns':support});changed=True
            if not changed:break
        active=[j for j in range(N)if j not in zero];n=sum(j<n for j in active)
        reduced=[[row[j]for j in active]for row in A]
        R,rank=fmpq_mat([[row[j]for row in reduced]for j in range(len(active))]).rref()
        selected=[next(i for i in range(m)if R[k,i])for k in range(rank)]
        tree,nodes=solve([reduced[i]for i in selected],[b[i]for i in selected],n)
        report.update(outcome=tree['status'],zero_deductions=deductions,active_columns=active,
                      selected_rows=selected,integer_variables=n,nodes=nodes,tree=tree)
    records.append(report)
    (HERE/'branches.json').write_text(json.dumps({'records':records,'scope':'Only complete branching trees with exact Farkas leaves certify integer infeasibility.'},indent=2)+'\n')
    print('BRANCH',report['pattern'],report['outcome'],report.get('nodes'),flush=True)

module.mod.base.lp.verify=verify
sys.argv=['complex_semion.py']
module.main()
