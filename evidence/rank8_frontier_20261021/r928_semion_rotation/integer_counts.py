"""Bounded integer-count search and exact modular/witness checks for R928."""
from pathlib import Path
import argparse,hashlib,json,math,time
from flint import nmod_mat
import pair_rotation as pair
need=pair.need;HERE=Path(__file__).resolve().parent
PRIMES=(2,3,5,7,11,13)


def check_integer(A,b,witness):
    entries=dict(witness)
    need(len(entries)==len(witness)and all(type(j)is int and 0<=j<len(A[0])and type(v)is int and v>0 for j,v in witness),'integer witness domain')
    need(all(sum(row[j]*v for j,v in witness)==rhs for row,rhs in zip(A,b)),'every original integer equation')


def search(A,b):
    import numpy as np
    from scipy.optimize import milp,Bounds,LinearConstraint
    from scipy.sparse import csc_matrix
    ub=[None]*len(A[0])
    for row,rhs in zip(A,b):
        if rhs<0 or any(x<0 for x in row):continue
        for j,x in enumerate(row):
            if x>0:
                q=rhs//x;ub[j]=q if ub[j]is None else min(ub[j],q)
    need(all(u is not None for u in ub),'finite exact nonnegative-row bounds for every count')
    active=[j for j,u in enumerate(ub)if u]
    mat=np.array([[row[j]for j in active]for row in A],dtype=float);rhs=np.array(b,dtype=float)
    scale=np.maximum(1,np.maximum(np.max(np.abs(mat),axis=1),np.abs(rhs)))
    start=time.monotonic();sol=milp(np.zeros(len(active)),integrality=np.ones(len(active)),
        bounds=Bounds(np.zeros(len(active)),np.array([ub[j]for j in active],dtype=float)),
        constraints=LinearConstraint(csc_matrix(mat/scale[:,None]),rhs/scale,rhs/scale),
        options={'time_limit':30.,'node_limit':20000,'mip_rel_gap':0.,'presolve':True})
    out={'numeric_status':int(sol.status),'numeric_message':str(sol.message),'time_limit_seconds':30,
        'node_limit':20000,'active_variables':len(active),'finite_exact_upper_bounds':ub,
        'elapsed_seconds':round(time.monotonic()-start,3),'status':'integer_feasibility_unresolved'}
    if sol.x is not None:
        witness=[[j,int(round(float(v)))]for j,v in zip(active,sol.x)if int(round(float(v)))!=0]
        try:check_integer(A,b,witness)
        except ValueError:out['rounded_candidate_failed_exact_replay']=True
        else:out.update(status='exact_nonnegative_integer_witness',witness=witness)
    return out


def run(write):
    loaded=pair.setup();prior=json.loads((HERE/'pair_rotation.json').read_text());path=HERE/'integer_counts.json'
    saved=None if write else json.loads(path.read_text());cases=[];modular=None;matrix=None
    for previous in prior['cases']:
        index=previous['metadata']['pattern_index'];A,b,meta=pair.build(loaded,index)
        need(meta==previous['metadata'],'full correlated pair system binding')
        if modular is None:
            matrix=meta['matrix_sha256'];modular=[]
            for p in PRIMES:
                Z,nullity=nmod_mat([[x%p for x in row]for row in A],p).transpose().nullspace()
                basis=[[int(Z[i,j])for i in range(len(A))]for j in range(nullity)]
                modular.append((p,len(A)-nullity,basis))
        need(meta['matrix_sha256']==matrix,'one common full coefficient matrix')
        checks=[];congruence=None
        for p,rank,basis in modular:
            bad=next((row for row in basis if sum(x*y for x,y in zip(row,b))%p),None)
            checks.append({'prime':p,'matrix_rank':rank,'consistent':bad is None})
            if bad is not None:
                need(all(sum(bad[i]*A[i][j]for i in range(len(A)))%p==0 for j in range(len(A[0]))),'exact modular row certificate')
                congruence={'prime':p,'row':bad,'rhs_residue':sum(x*y for x,y in zip(bad,b))%p}
                break
        if write:
            result={'status':'exact_integer_lattice_obstruction','certificate':congruence}if congruence else search(A,b)
        else:
            old=saved['cases'][len(cases)];need(old['metadata']==meta and old['modular_tests']==checks,'integer/modular domain metadata')
            result=old['result']
            if result['status']=='exact_nonnegative_integer_witness':check_integer(A,b,result['witness'])
            elif result['status']=='exact_integer_lattice_obstruction':need(result['certificate']==congruence and congruence is not None,'modular exclusion certificate')
            else:need(result['status']=='integer_feasibility_unresolved'and congruence is None,'honest unresolved integer outcome')
        cases.append({'metadata':meta,'modular_tests':checks,'result':result})
        print('R928 integer counts',index,result['status'],flush=True)
    result={'id':'R8_3_928','tested_modular_primes':list(PRIMES),'complete_pair_surviving_indices':prior['complete_remaining_indices'],
        'dependencies_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest()for p in[HERE/'pair_rotation.py',HERE/'pair_rotation.json']},
        'cases':cases,'scope':'Exact positive witnesses and modular contradictions only. A bounded numerical failure leaves integer feasibility unresolved; no global exclusion follows.'}
    if write:path.write_text(json.dumps(result,indent=2)+'\n')
    else:need(result==saved,'bounded integer research receipt')
    print('PASS R928 bounded integer-count research replay',flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--write',action='store_true');run(p.parse_args().write)
