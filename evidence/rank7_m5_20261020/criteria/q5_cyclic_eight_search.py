"""Source-bound exploratory C8 systems for the two unresolved rank-seven rings.

An exact feasible integer vector certifies only these necessary conditions.
A solver's infeasible/timeout status is not a mathematical exclusion.  Exact
Farkas vectors, when found, are checked against the exported integer system.
"""
import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import sys
import time

HERE=Path(__file__).resolve().parent
EVIDENCE=HERE.parent
sys.path.insert(0,str(EVIDENCE/'integral_gram'))
sys.path.insert(0,str(EVIDENCE/'modules'))
import full_field_verlinde as old
import integer_norm_cuts as nc
from cyclic_eight_constraints import append_cyclic_eight
from full_source_phases import phase_records_powers

q=old.q;m=old.m;e=old.e;f=old.f


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def bound_inputs(rid):
    if rid=='R7_5_3895':
        word=EVIDENCE/'modules/all_word_R7_5_3895_full_field_verlinde_branch0_fp5_words.json'
        norm=EVIDENCE/'models/sqrt5/R3895_branch0_fp5_integral_norm_cut.json'
    else:
        word=EVIDENCE/'modules/all_word_R7_5_5039_full_field_verlinde_chi8_0_fp5.json'
        norm=EVIDENCE/'models/sqrt5/R5039_c2_fp5_integral_norm_cut.json'
    return word,norm


def prepare(rid):
    N=next(r['tensor'] for r in json.loads((q.ROOT/'supplements/rank7/output/m5/census.json').read_text()) if r['id']==rid)
    d,D,B,zs,T,signs=q.source_data(N,rid)
    table=m.ExactQuadraticCharacterTable(N,d,5)
    low_index=8 if rid=='R7_5_3895' else 3
    dom=next(z for z in e.domains(rid) if z['low_index']==low_index)
    low=[tuple(z) for z in dom['low']]
    orbits=[[(tuple(a),tuple(b),tuple(c)) for a,b,c in orb] for orb in dom['orbits']]
    spectrum=old.Spectrum(table,[(1,0,0,0,0,0,0)]+low,[(a,c) for orb in orbits for a,b,c in orb])
    q.require(not spectrum.missing_low,'eligible complete low spectrum')
    forbidden=set(map(tuple,spectrum.forbidden))
    orbits=[orb for orb in orbits if all(a not in forbidden for a,b,c in orb)]
    V=old.v.coefficients(table,{'id':rid,'low_index':low_index,'low':low,'orbits':orbits})
    word_path,norm_path=bound_inputs(rid)
    word=json.loads(word_path.read_text());norm=json.loads(norm_path.read_text())
    q.require(word['id']==rid and word['source_sha256']==q.tensor_hash(N),'all-word canonical source identity')
    q.require(word['domain_sha256']==V['domain_sha256'],'all-word complete spectral domain identity')
    q.require(norm['id']==rid and norm['source_sha256']==q.tensor_hash(N),'norm-cut canonical source identity')
    return dict(N=N,d=d,D=D,zs=zs,T=T,table=table,dom=dom,low=low,orbits=orbits,V=V,
                word=word,norm=norm,inputs={str(p.relative_to(q.ROOT)):digest(p) for p in (word_path,norm_path)})


def build(rid,case_index,branch,prepared=None):
    p=prepared or prepare(rid)
    N,d,D,zs,T,table,dom,low,orbits,V=(p[k] for k in ('N','d','D','zs','T','table','dom','low','orbits','V'))
    case=dom['cases'][case_index]
    q.require(-1 not in case['sign'],'representative positive second-indicator branch')
    records=phase_records_powers(max_power=3)
    columns,rhs,labels=f.build_system(table,low,case['label'],orbits,dom['bound'],D,zs,case['sign'],T,records,rid,chi8_branch=branch)
    columns,rhs,labels=old.fifth_primary_refinement(columns,rhs,labels,orbits,records,rid,T)
    cut=nc.coefficient_cut(table,{'id':rid,'low':low,'orbits':orbits},case['label'],N,T.dual,V,p['norm'])
    columns,rhs,labels=nc.append_cuts(columns,rhs,labels,[cut])
    columns,rhs,labels=old.all_word_congruences(columns,rhs,labels,p['word']['constraints'])
    columns,rhs,labels,c4=old.fourth_cyclic_constraints(columns,rhs,labels,orbits,records,low,d,D,N,case['sign'])
    columns,rhs,labels,c8=append_cyclic_eight(columns,rhs,labels,orbits,records,low,d,D,N,case['sign'],c4)
    auxiliary_count=len(columns)-len(labels)
    old_count=len(rhs)
    known=list(map(F,V['known']));vcols=[list(map(F,c)) for c in V['orbits']]
    columns=[list(map(F,col))+([labels[j]['multiplicity_unit']*x for x in vcols[labels[j]['orbit']]] if j<len(labels) else [F(0)]*len(known)) for j,col in enumerate(columns)]
    rhs=list(map(F,rhs))+[-x for x in known]
    verlinde_indices=[]
    for ti in range(len(V['triples'])):
        col=[F(0)]*len(rhs);col[old_count+2*ti]=-1
        verlinde_indices.append(len(columns));columns.append(col)
    columns,rhs=m.integral_system(columns,rhs)
    inputs=dict(p['inputs'])
    for path in [Path(__file__),EVIDENCE/'modules/cyclic_eight_constraints.py',EVIDENCE/'integral_gram/full_field_verlinde.py',EVIDENCE/'models/sqrt5/full_source_phases.py',HERE/'q5_full_field.py']:
        inputs[str(path.relative_to(q.ROOT))]=digest(path)
    return {'schema':'q5-source-bound-c8-v1','scope':'Necessary center and C8 rotation conditions only; no whole-ring exclusion from solver status.',
            'id':rid,'source_sha256':q.tensor_hash(N),'domain_sha256':V['domain_sha256'],'low_index':dom['low_index'],
            'case':case_index,'label':case['label'],'indicator_sign':case['sign'],'chi8_branch':branch,
            'columns':columns,'rhs':rhs,'phase_labels':labels,'phase_records':records,
            'low':low,'orbits':orbits,'auxiliary_count':auxiliary_count,
            'cyclic_four':c4,'cyclic_eight':c8,'verlinde_variables':verlinde_indices,
            'norm_cut_record':p['norm'],'norm_cut_coefficients':cut,'all_word_congruences':p['word'],
            'inputs_sha256':inputs}


def solve(system,time_limit):
    import numpy as np
    from scipy.optimize import milp,Bounds,LinearConstraint
    from scipy.sparse import csc_matrix
    cols=system['columns'];rhs=system['rhs'];labels=system['phase_labels'];pool=[]
    start=time.monotonic();sep=q.separate(cols,rhs,pool)
    result={'exact_separator':sep,'separators':pool,'separation_seconds':time.monotonic()-start}
    if sep is not None:return result
    ub=[min([rhs[i]//col[i] for i in range(21) if col[i]>0] or [np.inf]) for col in cols]
    q.require(all(u>=0 for u in ub),'nonnegative Gram capacities')
    start=time.monotonic()
    res=milp(np.r_[np.ones(len(labels)),np.zeros(len(cols)-len(labels))],integrality=np.ones(len(cols)),
             bounds=Bounds(np.zeros(len(cols)),ub),constraints=LinearConstraint(csc_matrix(np.array(cols,dtype=float).T),rhs,rhs),
             options={'time_limit':time_limit})
    result.update({'solver_status':int(res.status),'solver_message':str(res.message),'seconds':time.monotonic()-start,
                   'solver_infeasibility_is_not_a_proof':True})
    if res.x is not None:
        counts=[round(float(x)) for x in res.x]
        exact=all(n>=0 for n in counts) and all(sum(c[i]*n for c,n in zip(cols,counts))==b for i,b in enumerate(rhs))
        result.update({'exact_feasible':exact,'counts':counts})
        if exact:
            result['support']=[{**label,'count':count} for label,count in zip(labels,counts) if count]
            result['cyclic_four_multiplicities']=[{'object':ob['source_object'],'multiplicities':[counts[j] for j in ob['variables']]} for ob in system['cyclic_four']]
            result['cyclic_eight_multiplicities']=[{'object':ob['source_object'],'multiplicities':[counts[j] for j in ob['variables']]} for ob in system['cyclic_eight']]
    return result


def main():
    a=argparse.ArgumentParser();a.add_argument('ring',choices=['R7_5_3895','R7_5_5039']);a.add_argument('--case',type=int,required=True)
    a.add_argument('--chi8-branch',type=int,choices=[0,2]);a.add_argument('--time-limit',type=int,default=60);a.add_argument('--export-only',action='store_true');a.add_argument('--reuse-system',action='store_true')
    arg=a.parse_args();q.require((arg.ring=='R7_5_5039')==(arg.chi8_branch is not None),'conductor-eight branch required exactly for5039')
    stem=arg.ring+'_c8_case'+str(arg.case)+(('_chi8_'+str(arg.chi8_branch)) if arg.chi8_branch is not None else '')
    path=HERE/(stem+'_system.json')
    system=json.loads(path.read_text()) if arg.reuse_system else build(arg.ring,arg.case,arg.chi8_branch)
    if not arg.reuse_system:path.write_text(json.dumps(system)+'\n')
    print(json.dumps({'event':'exact_system_export','file':path.name,'columns':len(system['columns']),'equations':len(system['rhs']),'phase_variables':len(system['phase_labels']),'sha256':digest(path)}),flush=True)
    if arg.export_only:return
    result=solve(system,arg.time_limit)
    output={'id':arg.ring,'case':arg.case,'chi8_branch':arg.chi8_branch,'system_file':path.name,'system_sha256':digest(path),'source_sha256':system['source_sha256'],'result':result}
    (HERE/(stem+'_result.json')).write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('counts','support','separators')}),flush=True)


if __name__=='__main__':main()
