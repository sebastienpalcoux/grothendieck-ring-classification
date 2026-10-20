"""Exact aggregate chi-minus-eight branches; optimizer proposals are not proofs."""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):
    os.environ[key]='1'
import argparse
import hashlib
import json
import sys
import time
from pathlib import Path

import explore as e
sys.path.insert(0,str(e.HERE.parent/'computation'))


def validate_domain(system,inventory):
    """Bind the source, exact row order and weaker packet divisibilities."""
    active=inventory['active_orbits']
    labels=system['phase_labels']
    e.q.require(system['source_sha256']==inventory['source_sha256'],'source binding')
    for name,key in (('orbits','orbit_sha256'),('low','low_sha256')):
        e.q.require(hashlib.sha256(json.dumps(system[name],separators=(',',':')).encode()).hexdigest()==inventory[key],
                    'exact '+name+' domain binding')
    # Verify the only active orbits in this (possibly stronger) domain are
    # contained in the complete inventory. Missing types are harmless.
    for lab in labels:
        orbit=system['orbits'][lab['orbit']]
        weight=sum((v[0]-v[1])**2 for v,g,z in orbit)
        if weight:
            e.q.require(lab['orbit'] in active,'complete active inventory')
            e.q.require(weight==int(inventory['weights'][str(lab['orbit'])]),'orbit weight')
            e.q.require(lab['multiplicity_unit']%int(inventory['multiplicity_units'][str(lab['orbit'])])==0,
                        'stronger domain preserves packet divisibility')


def restrict(system, inventory, branch_index):
    """Fix actual multiplicity per active row orbit, preserving phase freedom."""
    validate_domain(system,inventory)
    chosen=dict(inventory['branches'][branch_index])
    active=inventory['active_orbits']
    labels=system['phase_labels']
    kept=[j for j in range(len(system['columns']))
          if j>=len(labels) or labels[j]['orbit'] not in active
          or chosen.get(labels[j]['orbit'],0)>0]
    live=[j for j in active if chosen.get(j,0)>0]
    cols=[]
    for j in kept:
        lab=labels[j] if j<len(labels) else None
        cols.append(system['columns'][j]+[
            lab['multiplicity_unit'] if lab is not None and lab['orbit']==k else 0
            for k in live])
    return cols,system['rhs']+[chosen[k] for k in live],kept


def verify_ray(cols,rhs,ray):
    e.q.require(len(rhs)==len(ray),'ray dimension')
    e.q.require(sum(a*b for a,b in zip(rhs,ray))<0,'negative target')
    e.q.require(all(sum(a*b for a,b in zip(col,ray))>=0 for col in cols),'nonnegative columns')


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('system',type=Path);ap.add_argument('--branch',type=int)
    ap.add_argument('--replay',action='store_true');args=ap.parse_args()
    path=args.system;raw=path.read_bytes();system=json.loads(raw)
    ipath=e.HERE/f"R7_5_5039_chi8_active_{system['chi8_branch']}.json"
    iraw=ipath.read_bytes();inventory=json.loads(iraw)
    outpath=e.HERE/(path.stem+'_active_branches.json')
    hashes={'system':hashlib.sha256(raw).hexdigest(),'inventory':hashlib.sha256(iraw).hexdigest()}
    if args.replay:
        result=json.loads(outpath.read_text());e.q.require(result['hashes']==hashes,'input hashes')
        for record in result['branches']:
            if 'ray' in record:
                cols,rhs,kept=restrict(system,inventory,record['branch'])
                verify_ray(cols,rhs,record['ray'])
        print(json.dumps({'status':'PASS','verified_leaves':sum('ray' in b for b in result['branches']),
                          'optimized_python':not __debug__}),flush=True);return
    import numpy as np
    from scipy.optimize import linprog
    from exact_branch_bound import exact_ray
    result={'id':system['id'],'chi8_branch':system['chi8_branch'],'case':system['case'],
            'hashes':hashes,'branches':[]}
    for bi in range(len(inventory['branches'])) if args.branch is None else [args.branch]:
        start=time.monotonic();cols,rhs,kept=restrict(system,inventory,bi)
        A=[list(row) for row in zip(*cols)]
        aa=np.array(A,dtype=float);bb=np.array(rhs,dtype=float)
        scale=np.maximum(1,np.maximum(np.max(abs(aa),axis=1),abs(bb)))
        sol=linprog(np.zeros(len(cols)),A_eq=aa/scale[:,None],b_eq=bb/scale,
                    bounds=(0,None),method='highs')
        record={'branch':bi,'lp_status':int(sol.status),'columns':len(cols),'equations':len(rhs)}
        if sol.status==2:
            ray=exact_ray(A,rhs)
            if ray is not None:
                verify_ray(cols,rhs,ray);record['ray']=ray
            else:record['no_exact_ray']=True
        result['branches'].append(record);record['seconds']=time.monotonic()-start
        outpath.write_text(json.dumps(result,separators=(',',':'))+'\n')
        print(json.dumps({k:v for k,v in record.items() if k!='ray'}|{'exact': 'ray' in record}),flush=True)


if __name__=='__main__':main()
