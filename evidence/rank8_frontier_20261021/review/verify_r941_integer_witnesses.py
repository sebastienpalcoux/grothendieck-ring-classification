#!/usr/bin/env python3
"""Independent exact replay of the twelve full fermionic integer witnesses."""
from pathlib import Path
import argparse,hashlib,json,sys
HERE=Path(__file__).resolve().parent;BASE=HERE.parent;REPO=BASE.parents[1]
sys.path.insert(0,str(BASE/'quartic_integer_center'))
import r941_paired_rotation as operator

def need(ok,msg):
    if not ok:raise ValueError(msg)

def compute():
    for filename in('r941_fermion_operator_review.json','r941_fermion_campaign_review.json'):
        receipt=json.loads((HERE/filename).read_text())
        for p,h in receipt['files_sha256'].items():need(hashlib.sha256((REPO/p).read_bytes()).hexdigest()==h,'reviewed source pin '+p)
    folder=BASE/'quartic_integer_center';prior=json.loads((folder/'r941_paired_rotation.json').read_text());saved=json.loads((folder/'r941_integer_counts.json').read_text())
    positives=[c for c in prior['cases']if c['decision']['status']=='exact_feasible_relaxation']
    need(len(positives)==16 and len(saved['cases'])==16,'complete rational survivor domain')
    cols,b,labels,charges,meta=operator.setup();verified=[];unresolved=[]
    for case,previous in zip(saved['cases'],positives):
        need(case['metadata']==previous['metadata'],'same full reviewed system')
        index=case['metadata']['allocation_index'];a=charges['solutions'][index]
        selected=[j for j,(kind,v,t)in enumerate(labels)if kind=='rotation_auxiliary'or(a['plus_pairs'][v]>0 if kind=='plus_pair'else a['minus_individuals'][v]>0)]
        need(selected==case['metadata']['selected_universal_columns'],'exact selected column list')
        rhs=b[:-80]+a['plus_pairs']+a['minus_individuals'];result=case['result']
        if result['status']=='exact_nonnegative_integer_witness':
            entries=result['witness'];need(len(dict(entries))==len(entries),'distinct integer coordinates')
            need(all(type(j)is int and 0<=j<len(selected)and type(v)is int and v>0 for j,v in entries),'positive exact integer entries')
            witness=[(selected[j],v)for j,v in entries]
            need(all(sum(cols[j][i]*v for j,v in witness)==q for i,q in enumerate(rhs)),'every original integer equation')
            verified.append({'allocation':index,'pattern':a['pattern_index'],'positive_entries':len(witness),'original_rows':len(rhs)})
        else:
            need(result['status']=='integer_feasibility_unresolved','no numerical-negative promotion')
            unresolved.append({'allocation':index,'pattern':a['pattern_index']})
    need(len(verified)==12 and len(unresolved)==4,'terminal integer outcome counts')
    files=[Path(__file__),HERE/'r941_fermion_operator_review.json',HERE/'r941_fermion_campaign_review.json',folder/'r941_integer_counts.py',folder/'r941_integer_counts.json']
    return {'kind':'independent_R941_full_integer_witness_review','exact_integer_witnesses':verified,
        'remaining_integer_feasibility_unresolved':unresolved,
        'scope':'twelve exact finite-system witnesses; four unproved integer questions; no categorification claim',
        'files_sha256':{str(p.relative_to(REPO)):hashlib.sha256(p.read_bytes()).hexdigest()for p in files}}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');args=ap.parse_args();result=compute();path=HERE/'r941_integer_witness_review.json'
    if args.write:path.write_text(json.dumps(result,indent=2)+'\n')
    else:need(result==json.loads(path.read_text()),'integer review receipt differs')
    print('PASS941 twelve integer witnesses against every original equation;four cases explicitly unresolved')
