#!/usr/bin/env python3
"""Read-only exact replay of integer phase branching and positive witnesses."""
from pathlib import Path
from fractions import Fraction as F
import argparse,hashlib,importlib.util,json,sys

HERE=Path(__file__).resolve().parent;BASE=HERE.parent
sys.path.insert(0,str(BASE))
spec=importlib.util.spec_from_file_location('quartic_integer_verify',BASE/'complex_semion.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
saved=json.loads((BASE/'R928_complex_semion.json').read_text())
search=json.loads((HERE/'search.json').read_text())
branches=json.loads((HERE/'branches.json').read_text())
original=module.mod.base.lp.verify
records=[]

def need(c,m):
    if not c:raise ValueError(m)

def check_tree(A,b,n,tree):
    need(tree['status']=='infeasible','complete infeasible tree required')
    if 'certificate'in tree:
        need(tree['certificate']['status']=='exact_infeasible_relaxation','exact negative leaf required')
        original(A,b,tree['certificate'])
        return 1,1
    j=tree['variable'];floor=tree['floor']
    need(isinstance(j,int) and 0<=j<n and isinstance(floor,int),'valid integer partition')
    count=1;leaves=0
    for key,lower in [('left',False),('right',True)]:
        row=[0]*(len(A[0])+1);row[j]=1;row[-1]=-1 if lower else 1
        childA=[v+[0]for v in A]+[row];childb=b+[floor+1 if lower else floor]
        nn,ll=check_tree(childA,childb,n,tree[key]);count+=nn;leaves+=ll
    return count,leaves

def verify(A,b,decision):
    original(A,b,decision)
    case=saved['cases'][len(records)];n=case['metadata']['complex_phase_atoms'];N=len(A[0])
    report={'pattern':case['metadata']['pattern']}
    positive=search['records'][len(records)];cut=branches['records'][len(records)]
    need(positive['pattern']==cut['pattern']==report['pattern'],'pattern ordering')
    for data in (positive,cut):
        need(all(data[k]==case['metadata'][k]for k in ('matrix_sha256','rhs_sha256')),'matrix binding')
    if positive['outcome']=='exact_integer_phase_feasible':
        counts=[0]*n;seen=set()
        for j,c in positive['phase_counts']:
            need(isinstance(j,int)and 0<=j<n and j not in seen and isinstance(c,int)and c>0,'positive integer phase count')
            seen.add(j);counts[j]=c
        auxA=[row[n:]for row in A];auxb=[rhs-sum(c*x for c,x in zip(row[:n],counts))for row,rhs in zip(A,b)]
        need(positive['auxiliary_certificate']['status']=='exact_feasible_relaxation','positive auxiliary witness')
        original(auxA,auxb,positive['auxiliary_certificate'])
        report['outcome']='exact_integer_phase_feasible'
    else:
        need(cut['outcome']=='infeasible','completed negative branch proof required')
        zero=set()
        for step in cut['zero_deductions']:
            i=step['row'];need(isinstance(i,int)and 0<=i<len(A) and b[i]==0,'zero-equation row')
            row=A[i];support=[j for j,v in enumerate(row)if v and j not in zero]
            need(support==step['new_zero_columns']and support,'exact zero-support deduction')
            need(all(row[j]>0 for j in support)or all(row[j]<0 for j in support),'one-signed remaining support')
            zero.update(support)
        active=[j for j in range(N)if j not in zero]
        need(active==cut['active_columns'],'active variables')
        integer_count=sum(j<n for j in active)
        need(integer_count==cut['integer_variables'],'integer phase count')
        selected=cut['selected_rows']
        need(len(selected)==len(set(selected))and all(isinstance(i,int)and 0<=i<len(A)for i in selected),'selected necessary rows')
        reduced=[[A[i][j]for j in active]for i in selected];rhs=[b[i]for i in selected]
        nodes,leaves=check_tree(reduced,rhs,integer_count,cut['tree'])
        need(nodes==cut['nodes'],'complete tree node count')
        report.update(outcome='exact_integer_phase_impossible',nodes=nodes,farkas_leaves=leaves)
    records.append(report);print('PASS integer phase',report,flush=True)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--write',action='store_true');args=parser.parse_args()
    files=['README.md','PROOF.md','verify.py','search.py','search.json','branch_search.py','branches.json']
    hashes={name:hashlib.sha256((HERE/name).read_bytes()).hexdigest()for name in files}
    hashes['../verification.json']=hashlib.sha256((BASE/'verification.json').read_bytes()).hexdigest()
    path=HERE/'verification.json';prior=None if args.write else json.loads(path.read_text())
    if prior is not None:need(prior['bindings']==hashes,'integer evidence binding')
    need(len(search['records'])==len(branches['records'])==10,'complete ten-pattern domain')
    module.mod.base.lp.verify=verify
    sys.argv=['complex_semion.py'];module.main()
    result={'status':'PASS','bindings':hashes,'records':records,
            'scope':'Exact integer-phase pattern cuts and exact surviving phase witnesses; R928 remains unresolved.'}
    if args.write:path.write_text(json.dumps(result,indent=2)+'\n')
    else:need(result==prior,'deterministic integer verification')
    print('PASS exact integer phase refinement',flush=True)

if __name__=='__main__':main()
