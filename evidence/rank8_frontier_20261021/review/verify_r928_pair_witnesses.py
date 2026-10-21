#!/usr/bin/env python3
"""Direct paired-semion operator and exact witness/dual review; no solver."""
from pathlib import Path
from fractions import Fraction as F
import argparse,hashlib,json,math,sys
HERE=Path(__file__).resolve().parent;BASE=HERE.parent;REPO=BASE.parents[1]
sys.path.insert(0,str(BASE/'noncommutative'))
import rotation_search as rot,character_modular as mod

def need(ok,msg):
    if not ok:raise ValueError(msg)

def digest(v):return hashlib.sha256(json.dumps(v,separators=(',',':')).encode()).hexdigest()

def check_primal(A,b,entries,integer=False):
    need(len(dict(entries))==len(entries),'unique primal coordinates')
    w={j:F(v)for j,v in entries}
    need(all(type(j)is int and 0<=j<len(A[0])and v>0 and(not integer or v.denominator==1)for j,v in w.items()),'nonnegative exact count domain')
    need(all(sum(row[j]*v for j,v in w.items())==rhs for row,rhs in zip(A,b)),'all exact primal equations')

def compute():
    folder=BASE/'r928_semion_rotation';quartic=BASE/'quartic_integer_center'
    r=json.loads((quartic/'source.json').read_text())['records'][0];need(r['id']=='R8_3_928','source identity')
    patterns=json.loads((quartic/'gram_cubic.json').read_text())['patterns']
    indices=[j for j,m in enumerate(patterns)if all(m[k]%2==0 for k in range(40))]
    prior=json.loads((folder/'results.json').read_text());pair=json.loads((folder/'pair_rotation.json').read_text());integers=json.loads((folder/'integer_counts.json').read_text())
    need([c['metadata']['pattern_index']for c in prior['cases']]==indices,'complete semion parity case order')
    R=r['tensor'];rot.install();a=rot.bq.data(R);lows=a['lows'][0]
    A,b,metadata=rot.bq.system(R,a,lows,(0,0,0,0,0,0,-1),6)
    A,b,metadata=mod.append_sts(R,a,lows,(0,1,2,3,4),A,b,metadata,6)
    types,bound=rot.bq.trace_types(6);nt=len(types);order=r['original_high_order'];oldn=len(A[0]);baseb=b[:]
    need(nt==38 and bound==288,'complete approved individual trace domain')
    for raw in order:
        row=[0]*oldn
        for j in range(nt):row[raw*nt+j]=1
        A.append(row)
    moments=[(j,k,0)for j in range(40)for k in(2,6)]+[(j,k,t)for j in(40,41,42,43,57)for k,t in enumerate((0,-1,0,1,0,-1),1)]
    moment_rhs=[]
    for j,k,t in moments:
        need(all(m[j]==1 for m in patterns)if j>=40 else True,'known translated multiplicity one')
        for coordinate in range(4):
            c=[tt[k-1][coordinate]for tt in types];rhs=F(t if coordinate==0 else 0)
            den=math.lcm(rhs.denominator,*(v.denominator for v in c));vals=[int(v*den)for v in c];rhs=int(rhs*den)
            gcd=math.gcd(rhs,*vals)or 1;row=[0]*oldn
            for z,v in enumerate(vals):row[order[j]*nt+z]=v//gcd
            A.append(row);moment_rhs.append(rhs//gcd)
    need(len(A)==873,'full old rows')
    common=digest(A);excluded=[];survivors=[]
    sparsecols=[[(i,row[j])for i,row in enumerate(A)if row[j]]for j in range(oldn)]
    for case in prior['cases']:
        j=case['metadata']['pattern_index'];rhs=baseb+patterns[j]+moment_rhs
        need(case['metadata']['matrix_sha256']==common and case['metadata']['rhs_sha256']==digest(rhs),'old full matrix/RHS identity')
        decision=case['decision']
        if decision['status']=='exact_infeasible_relaxation':
            ray=decision['ray'];need(len(ray)==len(rhs),'full ray dimension')
            need(sum(x*y for x,y in zip(ray,rhs))<0 and all(sum(ray[i]*v for i,v in col)>=0 for col in sparsecols),'full-domain exact separator')
            excluded.append(j)
        else:
            need(decision['status']=='exact_feasible_relaxation','exact old decision')
            check_primal(A,rhs,decision['primal']);survivors.append(j)
    trace=json.loads((HERE/'semion_pair_traces.json').read_text());pairtypes=[tuple(tuple(map(F,row))for row in typ)for typ in trace['pair_trace_types']]
    matches=[]
    for tt in pairtypes:
        options=[(i,j)for i,u in enumerate(types)for j,v in enumerate(types)if i<=j and tuple(tuple(x+y for x,y in zip(q,r))for q,r in zip(u,v))==tt]
        need(bool(options),'all thirty true paired phase types are represented');matches.append(options[0])
    rawcanon={raw:j for j,raw in enumerate(order)};groups=[]
    for raw in range(65):
        if rawcanon[raw]<40:groups.extend((raw*nt+i,raw*nt+j)for i,j in matches)
        else:groups.extend((raw*nt+i,)for i in range(nt))
    groups.extend((j,)for j in range(65*nt,oldn))
    B=[[sum(row[j]for j in group)for group in groups]for row in A]
    need(len(groups)==2227 and len(matches)==30,'complete pair domain and auxiliary block once')
    need([c['metadata']['pattern_index']for c in pair['cases']]==survivors,'complete paired case order')
    for case in pair['cases']:
        j=case['metadata']['pattern_index'];rhs=baseb+patterns[j]+moment_rhs
        need(case['metadata']['matrix_sha256']==digest(B)and case['metadata']['rhs_sha256']==digest(rhs),'independent paired full matrix/RHS identity')
        need(case['decision']['status']=='exact_feasible_relaxation','ten paired rational witnesses')
        check_primal(B,rhs,case['decision']['primal'])
    need([c['metadata']['pattern_index']for c in integers['cases']]==survivors,'complete integer research case order')
    integer_indices=[];unresolved=[]
    for case in integers['cases']:
        j=case['metadata']['pattern_index'];rhs=baseb+patterns[j]+moment_rhs;result=case['result']
        if result['status']=='exact_nonnegative_integer_witness':
            check_primal(B,rhs,result['witness'],True);integer_indices.append(j)
        else:
            need(result['status']=='integer_feasibility_unresolved','no numerical exclusion accepted');unresolved.append(j)
    need(excluded==[2,6,61,64,199] and integer_indices==[40,49,186,191],'stated exact outcomes')
    files=[Path(__file__),HERE/'semion_pair_traces.py',HERE/'semion_pair_traces.json',HERE/'quartic_central_orbits.json',quartic/'source.json',quartic/'gram_cubic.json']+[folder/f for f in('verify.py','results.json','pair_rotation.py','pair_rotation.json','integer_counts.py','integer_counts.json')]
    return {'kind':'independent_R928_complete_pair_operator_and_witness_review','old_domain':{'rows':len(A),'columns':oldn,'complete_patterns':indices,'exact_excluded_patterns':excluded},
        'pair_domain':{'rows':len(B),'columns':len(groups),'correlated_types':len(matches),'all_ten_exact_rational_witnesses':survivors},
        'exact_full_integer_witness_patterns':integer_indices,'remaining_integer_feasibility_unresolved_patterns':unresolved,
        'scope':'finite necessary constraints survive; no categorification and no numerical infeasibility claim',
        'files_sha256':{str(p.relative_to(REPO)):hashlib.sha256(p.read_bytes()).hexdigest()for p in files}}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');args=ap.parse_args();actual=compute();path=HERE/'r928_pair_witness_review.json'
    if args.write:path.write_text(json.dumps(actual,indent=2)+'\n')
    else:need(actual==json.loads(path.read_text()),'review receipt differs')
    print('PASS R928 all15 old branches, all30 pair types/2227 columns, ten rational and four integer witnesses')
