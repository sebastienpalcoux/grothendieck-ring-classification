"""Terminal bounded integer-count attempts on all16 surviving fermion cones."""
from pathlib import Path
import argparse,hashlib,json,sys
from flint import nmod_mat
import r941_paired_rotation as pair
HERE=Path(__file__).resolve().parent;need=pair.need
sys.path.insert(0,str(HERE.parent/'r928_semion_rotation'))
import integer_counts as shared
import integer_support_lattice as support

def run(write):
    data=pair.setup();prior=json.loads((HERE/'r941_paired_rotation.json').read_text())
    positive=[c for c in prior['cases']if c['decision']['status']=='exact_feasible_relaxation']
    need(len(positive)==16,'complete surviving paired domain')
    path=HERE/'r941_integer_counts.json';progress=HERE/'r941_integer_counts.progress.json'
    saved=None if write else json.loads(path.read_text());cached=json.loads(progress.read_text())if write and progress.exists()else[]
    cases=[]
    for previous in positive:
        index=previous['metadata']['allocation_index'];A,b,meta=pair.build(data,index)
        need(meta==previous['metadata'],'full paired system identity');pair.lp.verify(A,b,previous['decision'])
        ub,rows=support.bounds(A,b);active=[j for j,u in enumerate(ub)if u];tests=[];obstruction=None
        for prime in shared.PRIMES:
            Z,n=nmod_mat([[row[j]%prime for j in active]for row in A],prime).transpose().nullspace()
            bad=next(([int(Z[i,k])for i in range(len(A))]for k in range(n)
                if sum(int(Z[i,k])*b[i]for i in range(len(A)))%prime),None)
            tests.append({'prime':prime,'supported_matrix_rank':len(A)-n,'consistent':bad is None})
            if bad is not None:
                obstruction={'prime':prime,'row':bad,'rhs_residue':sum(x*y for x,y in zip(bad,b))%prime}
                support.check_ray(A,b,active,obstruction);break
        if write:
            if len(cases)<len(cached)and cached[len(cases)]['metadata']==meta:result=cached[len(cases)]['result']
            elif obstruction is not None:result={'status':'exact_supported_integer_lattice_obstruction','certificate':obstruction}
            else:result=shared.search(A,b)
        else:
            old=saved['cases'][len(cases)]
            need(old['metadata']==meta and old['finite_exact_upper_bounds']==ub and old['bound_witness_rows']==rows
                and old['modular_tests']==tests,'complete supported modular/bounded input domain')
            result=old['result']
        if result['status']=='exact_nonnegative_integer_witness':shared.check_integer(A,b,result['witness'])
        elif result['status']=='exact_supported_integer_lattice_obstruction':
            need(result['certificate']==obstruction and obstruction is not None,'exact supported modular contradiction')
        else:need(result['status']=='integer_feasibility_unresolved'and obstruction is None,'honest bounded unresolved integer outcome')
        cases.append({'metadata':meta,'finite_exact_upper_bounds':ub,'bound_witness_rows':rows,'modular_tests':tests,'result':result})
        if write:progress.write_text(json.dumps(cases,indent=2)+'\n')
        print('941 integer',index,result['status'],flush=True)
    result={'id':'R8_3_941','status':'all_planned_integer_count_attempts_finished','planned_allocation_indices':[v['metadata']['allocation_index']for v in positive],
        'cases':cases,'exact_integer_witness_count':sum(c['result']['status']=='exact_nonnegative_integer_witness'for c in cases),
        'exact_modular_exclusion_count':sum(c['result']['status']=='exact_supported_integer_lattice_obstruction'for c in cases),
        'unresolved_integer_feasibility_count':sum(c['result']['status']=='integer_feasibility_unresolved'for c in cases),
        'dependencies':{str(p.relative_to(HERE.parent)):hashlib.sha256(p.read_bytes()).hexdigest()for p in
            (HERE/'r941_paired_rotation.py',HERE/'r941_paired_rotation.json',HERE.parent/'r928_semion_rotation/integer_counts.py',HERE.parent/'r928_semion_rotation/integer_support_lattice.py')},
        'scope':'complete supported modular tests at primes2,3,5,7,11,13 and one30-second/20000-node bounded MIP attempt per surviving cone; numerical infeasibility is not an exact exclusion'}
    if write:path.write_text(json.dumps(result,indent=2)+'\n')
    else:need(result==saved,'integer-count attempt receipt differs')
    print('PASS941 terminal integer attempts:',result['exact_integer_witness_count'],'exact witnesses;',result['unresolved_integer_feasibility_count'],'unresolved.')

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--write',action='store_true');args=p.parse_args();run(args.write)
