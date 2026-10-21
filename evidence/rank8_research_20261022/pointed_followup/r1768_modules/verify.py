#!/usr/bin/env python3
"""Exact free-C2 filter on the complete saved R1768 induction factors.

No new Gram search or action-completion search is performed.
"""
import argparse
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
SOURCES={
 'evidence/rank8_next_20261021/quadratic/action_classes.json':'3c610085cf25cea6a7ea0e7b2841928ac63bbbac49805646ddb385ad57f89b18',
 'evidence/rank8_next_20261021/quadratic/profile_closure.json':'6b48256765fb6380a3080669b0d6b5c20f924f3c8277308aa036cc47c1e28140',
 'evidence/rank8_research_20261022/pointed_followup/verification_R8_3_1768.json':'ab3baabf62b0fbbbde7a8a01594250a3d22804c15c8da27a678fd755393716ab',
 'evidence/rank8_research_20261022/pivotality/general_spherical_gates.json':'89ad25baeb05b69c95519670eb4cdd894a29d3b7f4d920535b1f404f46ba13d4',
}
RID='R8_3_1768'
TENSOR_SHA='240509807c67da437c86f2a51efeb831364734feb93ed18a1d2f32087ebc1af0'

def need(c,m):
    if not c:raise ValueError(m)

def mul(A,B):
    return [[sum(x*y for x,y in zip(row,col))for col in zip(*B)]for row in A]

def run():
    for name,digest in SOURCES.items():
        need(hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest,'bound source changed: '+name)
    read=lambda p:json.loads((ROOT/p).read_text())
    row=next(r for r in read('evidence/rank8_m3_20261021/pipeline/census_m3.json')if r['id']==RID)
    R=row['tensor']
    need(hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest()==TENSOR_SHA,'canonical tensor')
    du=[next(j for j in range(8)if R[i][j][0])for i in range(8)]
    gp=[next(j for j in range(8)if R[1][i][j])for i in range(8)]
    need(gp==[1,0,7,6,5,4,3,2]and all(sum(R[1][i])==1 for i in range(8)),'source invertible permutation')
    need(all(R[1][i]==R[i][1]for i in range(8)),'central based-ring invertible')
    ds=[(1,0),(1,0),(5,1),(6,1),(7,1),(7,1),(6,1),(5,1)]
    qmul=lambda x,y:(x[0]*y[0]+37*x[1]*y[1],x[0]*y[1]+x[1]*y[0])
    need(all(qmul(ds[i],ds[j])==tuple(sum(R[i][j][k]*ds[k][l]for k in range(8))for l in range(2))
             for i,j in itertools.product(range(8),repeat=2)),'exact positive irrational FP character')
    pointed=read('evidence/rank8_research_20261022/pointed_followup/verification_R8_3_1768.json')
    need(pointed['tensor_sha256']==TENSOR_SHA,'pointed source tensor')
    even=next(p for p in pointed['parities']if p['pointed_second_indicator']==1)
    need(even['status']=='all_indicator_branches_exact_infeasible'and
         even['verified_indicator_branches']==even['admissible_indicator_branches']==8,'complete trivial-associator exclusion')
    gate=next(r for r in read('evidence/rank8_research_20261022/pivotality/general_spherical_gates.json')if r['id']==RID)
    need(gate['tensor_sha256']==TENSOR_SHA and gate['conclusion'].startswith('every categorification is spherical and has a pseudo-unitary Galois conjugate'),'general Galois gate')
    classes=read('evidence/rank8_next_20261021/quadratic/action_classes.json')[RID]['complete_action_classes']
    need(len(classes)==9,'nine fully determined classes')
    class_results=[]
    for index,c in enumerate(classes):
        n=c['module_rank'];M=c['actions']
        need(M[0]==[[int(i==j)for j in range(n)]for i in range(n)],'module unit')
        need(all(M[du[i]]==list(map(list,zip(*M[i])))for i in range(8)),'module duality')
        for i,j in itertools.product(range(8),repeat=2):
            need(mul(M[i],M[j])==[[sum(R[i][j][k]*M[k][a][b]for k in range(8))for b in range(n)]for a in range(n)],'full module multiplication')
        need(all(sum(r)==1 for r in M[1])and all(sum(col)==1 for col in zip(*M[1])),'g permutation matrix')
        fixed=sum(M[1][i][i]for i in range(n))
        class_results.append({'class_index':index,'rank':n,'g_fixed_simples':fixed,'survives_free_g_test':fixed==0})
    need([c['class_index']for c in class_results if c['survives_free_g_test']]==[0,1,3],'three recorded surviving classes')
    prior=read('evidence/rank8_next_20261021/quadratic/profile_closure.json')[RID]
    factors=prior['surviving_factors'];need(len(factors)==61,'complete prior factor domain')
    results=[]
    for f in factors:
        B=f['B'];n=len(B);a=B[0]
        need(all(sum(B[t][i]*B[t][j]for t in range(n))==sum(a[k]*R[i][k][j]for k in range(8))
                 for i,j in itertools.product(range(8),repeat=2)),'saved exact induction Gram')
        need(all(any(v)for v in B),'nonzero induced rows')
        counts=Counter(tuple(v)for v in B);bad=[]
        for v,m in sorted(counts.items()):
            gv=tuple(v[gp[i]]for i in range(8))
            if counts[gv]!=m:bad.append('unmatched_g_translated_restriction')
            if gv==v and m%2:bad.append('odd_multiplicity_of_g_fixed_restriction')
        if n==2:bad.append('rank_two_free_swap_forces_integral_FP_dimensions')
        results.append({'candidate_index':f['candidate_index'],'factor_index':f['factor_index'],
                        'rank':n,'full_action_previously_determined':f['full_rank_action']is not None,
                        'survives':not bad,'obstructions':sorted(set(bad))})
    keep=[r for r in results if r['survives']]
    need(len(keep)==21 and len({r['candidate_index']for r in keep})==21,'twenty-one residual objects/factors')
    need(Counter(r['rank']for r in keep)=={4:4,6:6,8:9,12:2},'complete residual rank counts')
    need(sum(not r['full_action_previously_determined']for r in keep)==15,'fifteen incomplete actions remain')
    return {'schema':'R1768-free-C2-module-filter/v1','id':RID,'tensor_sha256':TENSOR_SHA,
        'scope':'general complex categorification; complete necessary filter on saved induction factors, not categorical module classification',
        'source_sha256':SOURCES,'universal_conclusions':['g acts freely on all module simples','all module ranks are even','rank two is impossible'],
        'fully_determined_action_classes':class_results,
        'previous_algebra_objects':49,'previous_induction_factors':61,
        'remaining_algebra_objects':21,'remaining_induction_factors':21,
        'remaining_possible_module_ranks':[4,6,8,12],
        'remaining_factors_with_undetermined_actions':15,'factor_filter':results,
        'limitation':'The three retained fully determined actions have ranks6,6,8, but fifteen additional induction factors lack full action completions. No model or general exclusion is proved.'}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--write',action='store_true');args=parser.parse_args()
    actual=run();path=HERE/'verification.json'
    if args.write:path.write_text(json.dumps(actual,indent=2)+'\n')
    else:need(actual==json.loads(path.read_text()),'saved free-C2 module filter changed')
    print('PASS: R1768 free-C2 filter leaves21/61 factors on21/49 objects; three fully determined classes and15 incomplete actions remain.')
