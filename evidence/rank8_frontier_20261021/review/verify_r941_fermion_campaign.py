#!/usr/bin/env python3
"""All corrected R941 paired decisions, exact direct dot-product replay."""
from pathlib import Path
from fractions import Fraction as F
import argparse,hashlib,json,sys
HERE=Path(__file__).resolve().parent;BASE=HERE.parent;REPO=BASE.parents[1]
sys.path.insert(0,str(BASE/'quartic_integer_center'))
import r941_paired_rotation as producer

def need(ok,msg):
    if not ok:raise ValueError(msg)

def digest(x):return hashlib.sha256(json.dumps(x,separators=(',',':')).encode()).hexdigest()

def compute():
    review=json.loads((HERE/'r941_fermion_operator_review.json').read_text())
    for p,h in review['files_sha256'].items():need(hashlib.sha256((REPO/p).read_bytes()).hexdigest()==h,'independently reviewed operator source pin '+p)
    folder=BASE/'quartic_integer_center';saved=json.loads((folder/'r941_paired_rotation.json').read_text())
    cols,b,labels,charges,meta=producer.setup()
    need(meta==saved['metadata'],'complete corrected operator metadata')
    need(saved['complete_charge_allocation_count']==93 and len(saved['cases'])==93,'complete allocation list')
    sparse=[[(i,v)for i,v in enumerate(col)if v]for col in cols];rays={};negative=[];positive=[];positive_patterns=[]
    for index,(case,allocation)in enumerate(zip(saved['cases'],charges['solutions'])):
        selected=[j for j,(kind,v,t)in enumerate(labels)if kind=='rotation_auxiliary'or(allocation['plus_pairs'][v]>0 if kind=='plus_pair'else allocation['minus_individuals'][v]>0)]
        rhs=b[:-80]+allocation['plus_pairs']+allocation['minus_individuals']
        expected={'allocation_index':index,'pattern_index':allocation['pattern_index'],
            'plus_pairs':allocation['plus_pairs'],'minus_individuals':allocation['minus_individuals'],
            'selected_universal_columns':selected,'matrix_sha256':digest([list(row)for row in zip(*(cols[j]for j in selected))]),'rhs_sha256':digest(rhs)}
        need(expected==case['metadata'],'every complete selected matrix and RHS')
        decision=case['decision']
        if decision['status']=='exact_infeasible_relaxation':
            ray=tuple(decision['ray']);need(len(ray)==len(rhs)and all(type(x)is int for x in ray),'exact integer full row ray')
            if ray not in rays:rays[ray]=[sum(ray[i]*v for i,v in col)for col in sparse]
            need(all(rays[ray][j]>=0 for j in selected),'every selected full-domain ray inequality')
            need(sum(x*y for x,y in zip(ray,rhs))<0,'strict negative original RHS')
            negative.append(index)
        else:
            need(decision['status']=='exact_feasible_relaxation','no numerical-only result')
            entries=decision['primal'];need(len(dict(entries))==len(entries),'distinct local primal columns')
            witness={selected[j]:F(v)for j,v in entries if type(j)is int and 0<=j<len(selected)}
            need(len(witness)==len(entries)and all(x>0 for x in witness.values()),'exact positive rational witness coordinates')
            need(all(sum(cols[j][i]*v for j,v in witness.items())==q for i,q in enumerate(rhs)),'every original primal equation')
            positive.append(index);positive_patterns.append(allocation['pattern_index'])
    need(len(negative)==77 and len(positive)==16,'complete corrected outcomes')
    files=[Path(__file__),HERE/'verify_r941_fermion_operator.py',HERE/'r941_fermion_operator_review.json',folder/'r941_paired_rotation.py',folder/'r941_paired_rotation.json']
    return {'kind':'independent_corrected_R941_paired_campaign_review','complete_charge_allocations':93,
        'exact_negative_allocations':negative,'exact_positive_allocations':positive,'exact_positive_patterns':positive_patterns,
        'distinct_exact_rays':len(rays),'rays_valid_on_universal_columns':sum(all(x>=0 for x in values)for values in rays.values()),
        'scope':'77 finite charge branches excluded; 16 exact rational survivors; no global exclusion or categorification',
        'files_sha256':{str(p.relative_to(REPO)):hashlib.sha256(p.read_bytes()).hexdigest()for p in files}}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');args=ap.parse_args();result=compute();path=HERE/'r941_fermion_campaign_review.json'
    if args.write:path.write_text(json.dumps(result,indent=2)+'\n')
    else:need(result==json.loads(path.read_text()),'campaign review receipt differs')
    print('PASS corrected R941 all93 allocations:77 exact duals,16 full exact primals')
