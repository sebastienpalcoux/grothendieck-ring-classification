"""Bounded split-module tests for self-dual direct sums, not only simples.

Default replay is read-only. --write explicitly runs the current residual
frontier, with at most 100000 enumeration cases for each proposed object.
Skipped objects remain explicit budget records, never feasibility claims.
"""
from pathlib import Path
import argparse,hashlib,itertools,json,math,sys,time
import sympy as s
from split_module_polynomial import require,search_setup,PRIME
HERE=Path(__file__).resolve().parent
def setup(R,g,weights):
    n=len(R);require(len(weights)==n and all(isinstance(w,int) and w>=0 for w in weights),'invalid object')
    require(all(R[i][j]==R[j][i] for i in range(n) for j in range(n)),'commutativity required')
    require(g!=0 and R[g][g]==[1]+[0]*(n-1),'involution required')
    du=[next(j for j in range(n) if R[i][j][0]) for i in range(n)]
    require(all(weights[i]==weights[du[i]] for i in range(n)),'object not self-dual')
    fixed=[i for i in range(n) if R[g][i][i]];require(fixed,'no fixed object')
    N=sum((weights[i]*s.Matrix(R[i]) for i in range(n)),s.zeros(n))
    A=[[int(N[i,j]) for j in fixed] for i in fixed];require(A==list(map(list,zip(*A))),'nonsymmetric block')
    f=len(fixed);parent=list(range(f));entries=[]
    def root(i):
        while i!=parent[i]:i=parent[i]
        return i
    for i in range(f):
        for j in range(i,f):
            a=A[i][j];allowed=list(range(-a,a+1,2));gauge=False
            if i!=j and a%2 and root(i)!=root(j):
                parent[root(i)]=root(j);allowed=[v for v in allowed if v>0];gauge=True
            entries.append([i,j,allowed,gauge])
    raw=N.charpoly().as_poly().sqf_part().all_coeffs()
    require(all(c.q==1 for c in raw),'nonintegral source polynomial')
    coefficients=[int(c) for c in raw]
    V=s.zeros(n)
    for c in coefficients:V=V*N+c*s.eye(n)
    require(V==s.zeros(n),'source polynomial identity')
    return dict(fixed=fixed,bounds=A,entries=entries,polynomial=coefficients,cases=math.prod(len(e[2]) for e in entries),prime=PRIME)
def verify(R,c):
    require(c['kind']=='rank8_split_module_object_polynomial','wrong certificate')
    a=search_setup(setup(R,c['involution'],c['generator_object']),c['search']['cases'])
    require(a['outcome']=='excluded' and a==c['search'],'object certificate did not replay')

def fingerprint(R):
    return hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest()

def tensor_profile(R):
    du=[]
    for i in range(8):
        candidates=[j for j in range(8) if R[i][j][0]]
        require(len(candidates)==1,'unique source dual required')
        du.append(candidates[0])
    require(all(R[i][j][0]==int(j==du[i]) for i,j in itertools.product(range(8),repeat=2)),'source dual coefficients')
    inv=[i for i in range(8) if R[i][du[i]]==[1]+[0]*7]
    comm=all(R[i][j]==R[j][i] for i,j in itertools.product(range(8),repeat=2))
    involutions=[g for g in inv if g and R[g][g]==[1]+[0]*7 and any(R[g][i][i] for i in range(8))]
    return {'dual':du,'invertibles':inv,'commutative':comm,'fixed_point_involutions':involutions}

def candidates(R,profile):
    if not profile['commutative']:return []
    atoms=[]
    for i in range(1,8):
        j=profile['dual'][i]
        if j<i:continue
        weights=[0]*8;weights[i]=1
        if j!=i:weights[j]=1
        atoms.append(weights)
    objects=[a for a in atoms if sum(a)>1]+[[a[i]+b[i] for i in range(8)] for a,b in itertools.combinations(atoms,2)]
    result=[]
    for g in profile['fixed_point_involutions']:
        for weights in objects:
            a=setup(R,g,weights);result.append((a['cases'],g,weights,a))
    return sorted(result,key=lambda v:(v[0],v[1],v[2]))

def record_outcome(profile,reports,certificate):
    if not profile['commutative']:return 'inapplicable_noncommutative'
    if not profile['fixed_point_involutions']:return 'inapplicable_no_fixed_involution'
    if certificate:return 'excluded'
    if any(r['search']['outcome']=='enumeration_budget' for r in reports):return 'partial_enumeration_budget'
    return 'no_conclusion'

def discover(budget):
    require(1<=budget<=100000,'per-object enumeration budget must be at most100000')
    sys.path.insert(0,str(HERE.parents[2]/'supplements/rank8/software'))
    import finalize_m3
    _,summary=finalize_m3.reconcile()
    pending=set(summary['unresolved_ids'])
    rows=json.loads((HERE.parent/'pipeline/census_m3.json').read_text())
    out=[];path=HERE/'split_module_object_results.json'
    for row in rows:
        if row['id'] not in pending:continue
        R=row['tensor'];require(fingerprint(R)==row['tensor_sha256'],'source hash mismatch')
        start=time.monotonic();profile=tensor_profile(R);options=candidates(R,profile);reports=[];cert=None
        for count,g,weights,a in options:
            result=search_setup(a,budget)
            reports.append({'involution':g,'generator_object':weights,'search':result})
            if result['outcome']=='excluded':
                cert={'kind':'rank8_split_module_object_polynomial','involution':g,'generator_object':weights,'search':result}
                verify(R,cert);break
        outcome=record_outcome(profile,reports,cert)
        record={'id':row['id'],'tensor_sha256':row['tensor_sha256'],'scope':'general_complex_fusion_category',
                'frontier_ledger_digest':summary['ledger_digest'],'profile_derived_from_tensor':profile,
                'object_family':'one nontrivial dual-pair atom or sum of two distinct nonunit self-dual orbit atoms',
                'per_object_case_budget':budget,'candidate_object_count':len(options),
                'outcome':outcome,'certificate':cert,'attempts':reports,
                'budget_skipped_objects':sum(r['search']['outcome']=='enumeration_budget' for r in reports),
                'completed_objects':sum(r['search']['outcome']!='enumeration_budget' for r in reports),
                'scope_note':'a modular survivor gives no exclusion; it is not a feasible categorification or an exact module witness'}
        out.append(record)
        temporary=path.with_suffix('.json.tmp');temporary.write_text(json.dumps(out,indent=2)+'\n');temporary.replace(path)
        print(row['id'],outcome,'objects',len(reports),'skipped',record['budget_skipped_objects'],
              'seconds',round(time.monotonic()-start,3),flush=True)
    require({r['id'] for r in out}==pending,'incomplete frontier traversal')
    return out

def replay():
    rows={r['id']:r for r in json.loads((HERE.parent/'pipeline/census_m3.json').read_text())}
    out=json.loads((HERE/'split_module_object_results.json').read_text())
    require(len({r['id'] for r in out})==len(out),'duplicate source record')
    for item in out:
        row=rows[item['id']];R=row['tensor']
        require(fingerprint(R)==row['tensor_sha256']==item['tensor_sha256'],'source hash mismatch')
        profile=tensor_profile(R);require(profile==item['profile_derived_from_tensor'],'tensor profile mismatch')
        budget=item['per_object_case_budget'];require(1<=budget<=100000,'unsafe replay budget')
        options=candidates(R,profile);reports=item['attempts']
        require(len(options)==item['candidate_object_count'],'candidate family changed')
        require(len(reports)<=len(options),'too many attempt records')
        require(item['certificate'] is not None or len(reports)==len(options),'unrecorded object attempts')
        for report,(count,g,weights,a) in zip(reports,options):
            require(report['involution']==g and report['generator_object']==weights,'object order changed')
            require(search_setup(a,budget)==report['search'],'bounded object search does not replay')
        if item['certificate']:
            require(reports and reports[-1]['search']['outcome']=='excluded','missing final exclusion')
            verify(R,item['certificate'])
        require(item['outcome']==record_outcome(profile,reports,item['certificate']),'misclassified bounded outcome')
        require(item['budget_skipped_objects']==sum(r['search']['outcome']=='enumeration_budget' for r in reports),'skip count mismatch')
        require(item['completed_objects']==sum(r['search']['outcome']!='enumeration_budget' for r in reports),'completion count mismatch')
    return out

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write',action='store_true',help='explicitly run and save the current residual frontier')
    parser.add_argument('--budget',type=int,default=100000,help='per-object bound, at most100000; used only with --write')
    args=parser.parse_args();out=discover(args.budget) if args.write else replay()
    print(json.dumps({'records':len(out),'excluded':[r['id'] for r in out if r['outcome']=='excluded'],
                      'noncommutative_inapplicable':sum(r['outcome']=='inapplicable_noncommutative' for r in out),
                      'budget_skipped_objects':sum(r['budget_skipped_objects'] for r in out),
                      'completed_objects':sum(r['completed_objects'] for r in out),
                      'mode':'write' if args.write else 'read_only_replay'}),flush=True)

if __name__=='__main__':main()
