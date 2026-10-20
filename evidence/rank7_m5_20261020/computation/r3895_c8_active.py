"""Exact C8 restriction to the four previously surviving phi-active counts.

Discovery may use a numerical LP to propose Farkas rays. Every accepted ray,
Gram removal, and integer-lattice obstruction is checked with exact arithmetic.
"""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[key]='1'
import argparse,hashlib,json,sys,time
from pathlib import Path
from inactive_lattice import require,prepare,check_counts,hermite_basis
from branch_lattice import matrix,negative_vector
HERE=Path(__file__).resolve().parent;BASE=HERE.parent;INPUT=BASE/'integral_gram'

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def fixed_counts(system,branch):
    dompath=INPUT/'R7_5_3895_domains.json';oldpath=INPUT/'R7_5_3895_system_8_0.json';apath=INPUT/'R7_5_3895_active_8.json'
    dom=next(r for r in json.loads(dompath.read_text()) if r['low_index']==8)
    old=json.loads(oldpath.read_text());allocation=json.loads(apath.read_text())['branches'][branch]
    key=lambda orbit:tuple(tuple(v) for v,g,z in orbit)
    wanted={}
    for j,count in allocation:
        original=old['phase_selection'][j];k=key(dom['orbits'][original//10])
        require(k not in wanted,'one forced saturated phase per old active orbit')
        wanted[k]=count*old['multipliers'][original]
    active=[];support=[];seen=set()
    for j,l in enumerate(system['phase_labels']):
        orb=system['orbits'][l['orbit']]
        if not any(v[3]!=v[4] for v,g,z in orb):continue
        k=key(orb);require(k not in seen,'one complete C8 phase per phi-active orbit');seen.add(k);active.append(j)
        count=wanted.get(k,0);require(count%l['multiplicity_unit']==0,'forced actual count is divisible by full C8 packet unit')
        if count:support.append([j,count//l['multiplicity_unit']])
    require(all(k in seen for k in wanted),'all positive active orbit types survive in full C8 domain')
    return active,support,{str(p.relative_to(HERE.parents[2])):sha(p) for p in (dompath,oldpath,apath)}

def restrict(system,branch):
    active,support,hashes=fixed_counts(system,branch);active=set(active);cols=system['columns']
    rhs=[b-sum(cols[j][i]*n for j,n in support) for i,b in enumerate(system['rhs'])]
    require(all(x>=0 for x in rhs[:21]) and negative_vector(matrix(rhs[:21])) is None,'residual Gram entrywise nonnegative and PSD')
    kept=[];removed=[];cache={}
    for j,c in enumerate(cols):
        if j in active:continue
        key=tuple(c[:21]);require(all(x>=0 for x in key),'nonnegative Gram columns')
        if key not in cache:
            entry=next((i for i in range(21) if c[i]>rhs[i]),None)
            if entry is not None:cache[key]={'entry':entry}
            else:
                w=negative_vector(matrix([rhs[i]-c[i] for i in range(21)]));cache[key]=None if w is None else {'negative_vector':w}
        if cache[key] is None:kept.append(j)
        else:removed.append({'column':j,**cache[key]})
    return [cols[j] for j in kept],rhs,{'active':sorted(active),'support':support,'kept':kept,'removed':removed,'source_hashes':hashes}

def verify_ray(cols,rhs,ray):
    require(len(ray)==len(rhs) and all(type(x)is int for x in ray),'integer covector')
    require(sum(a*b for a,b in zip(rhs,ray))<0,'negative target')
    require(all(sum(a*b for a,b in zip(c,ray))>=0 for c in cols),'nonnegative columns')

def run(branch,replay=False):
    start=time.monotonic();output=HERE/f'R7_5_3895_c8_active_{branch}.json'
    systems=[];sources={}
    for case in (0,2):
        path=BASE/'criteria'/f'R7_5_3895_c8_case{case}_system.json';systems.append(json.loads(path.read_text()));sources[str(path.relative_to(HERE.parents[2]))]=sha(path)
    if replay:
        saved=json.loads(output.read_text());require(saved['system_hashes']==sources,'C8 source hashes')
    results=[];basis_cache={}
    for case,system in zip((0,2),systems):
        cols,rhs,details=restrict(system,branch);record={'case':case,**details};key=hashlib.sha256(json.dumps(cols,separators=(',',':')).encode()).hexdigest()
        if replay:
            old=next(r for r in saved['cases'] if r['case']==case)
            require(all(old[k]==v for k,v in record.items()),'exact fixed counts and every Gram removal replay')
            if 'ray' in old:verify_ray(cols,rhs,old['ray']);record['ray']=old['ray'];record['status']='exact_farkas'
            elif 'prepared' in old:
                p=prepare(cols,rhs,[],basis=old['prepared']['basis']);require(p==old['prepared'],'recorded exact lattice tests')
                ok,why=check_counts(p,[],return_failure=True);require(ok==old['lattice_pass'] and why==old['failure'],'lattice verdict')
                record.update({'prepared':p,'lattice_pass':ok,'failure':why,'status':'lattice_feasible' if ok else 'exact_lattice_obstruction'})
            else:raise ValueError('no replayable case outcome')
        else:
            import numpy as np
            from scipy.optimize import linprog
            from exact_branch_bound import exact_ray
            A=np.array(cols,dtype=float).T;b=np.array(rhs,dtype=float);scale=np.maximum(1,np.maximum(abs(A).max(axis=1),abs(b)))
            lp=linprog(np.zeros(len(cols)),A_eq=A/scale[:,None],b_eq=b/scale,bounds=(0,None),method='highs')
            print(json.dumps({'event':'LP','branch':branch,'case':case,'columns':len(cols),'removed':len(details['removed']),'status':int(lp.status),'seconds':time.monotonic()-start}),flush=True)
            if lp.status==2:
                ray=exact_ray([list(row) for row in zip(*cols)],rhs)
                if ray is not None:verify_ray(cols,rhs,ray);record['ray']=ray;record['status']='exact_farkas'
            if 'status' not in record:
                if key not in basis_cache:
                    print(json.dumps({'event':'HNF','branch':branch,'case':case,'columns':len(cols)}),flush=True)
                    basis_cache[key]=hermite_basis(cols)
                p=prepare(cols,rhs,[],basis=basis_cache[key]);ok,why=check_counts(p,[],return_failure=True)
                record.update({'prepared':p,'lattice_pass':ok,'failure':why,'status':'lattice_feasible' if ok else 'exact_lattice_obstruction'})
        results.append(record)
        if not replay:output.write_text(json.dumps({'branch':branch,'system_hashes':sources,'cases':results},separators=(',',':'))+'\n')
        print(json.dumps({'event':'case_complete','branch':branch,'case':case,'status':record['status'],'seconds':time.monotonic()-start}),flush=True)
    report={'status':'PASS' if replay else 'COMPLETE','branch':branch,'case_statuses':[r['status'] for r in results],'optimized_python':not __debug__,'seconds':time.monotonic()-start}
    if replay:(HERE/f'R7_5_3895_c8_active_{branch}_replay_{"optimized" if not __debug__ else "normal"}.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--branch',type=int,nargs='+',choices=[0,19,160,165],default=[0,19,160,165]);p.add_argument('--replay',action='store_true');a=p.parse_args()
    for branch in a.branch:run(branch,a.replay)
