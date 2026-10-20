"""Conditional discovery after the exact forced order-320 packet reduction."""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[key]='1'
import argparse
import hashlib
import json
import math
import sys
import time
from pathlib import Path
import explore as e
from chi8_phase_gram import build as gram_build
sys.path.insert(0,str(e.HERE.parent/'computation'))
from chi8_branch_system import verify_ray


def fixed_packets(system,grams):
    labels=system['phase_labels'];records=system['phase_records']
    high45=[j for j,l in enumerate(labels) if l['orbit']==45 and records[l['phase']]['orders']==[320]]
    high50=[j for j,l in enumerate(labels) if l['orbit']==50 and records[l['phase']]['orders']==[320]]
    result=[]
    for pi,g in enumerate(grams):
        e.q.require(len(g['support'])==1 and g['support'][0][1]==1,'single active packet')
        active=g['support'][0][0];mu=records[labels[active]['phase']]['eighth_scaled8']
        matches=[j for j in high50 if all(4*records[labels[j]['phase']]['eighth_scaled8'][h]==-mu[h] for h in (2,6))]
        e.q.require(len(matches)==2 and all(labels[j]['multiplicity_unit']==16 for j in matches),'two forced packet types')
        for j in matches:result.append({'phase_case':pi,'forced50_column':j,'support':g['support']+[[j,1]],'forbidden':high45+high50})
    return result


def branch_system(system,phase_inventory,packet,phi=None):
    support=packet['support']+(phi or [])
    kept,removed,rhs=gram_build(system,phase_inventory,support)
    c4=system['cyclic_four'][0];fixed=dict(zip(c4['variables'],[3,1,0,0]))
    excluded=set(packet['forbidden'])|set(fixed)
    if phi is not None:
        for j,l in enumerate(system['phase_labels']):
            if any(v[2]!=v[3] for v,g,z in system['orbits'][l['orbit']]):excluded.add(j)
    kept=[j for j in kept if j not in excluded]
    rhs=[a-sum(system['columns'][j][i]*n for j,n in fixed.items()) for i,a in enumerate(rhs)]
    return [system['columns'][j] for j in kept],rhs,kept,removed


def orbit_capacity_cuts(system,cols,rhs,kept,support):
    """Round exact PSD capacities to possible integral orbit row counts."""
    N=next(r['tensor'] for r in json.loads((e.q.ROOT/'supplements/rank7/output/m5/census.json').read_text()) if r['id']==system['id'])
    e.q.require(e.q.tensor_hash(N)==system['source_sha256'],'capacity source binding')
    ds,D,B,zs,T,signs=e.q.source_data(N,system['id']);pairs=e.q.base.PAIRS
    bound=[B[i+1][j+1]-sum(v[i+1]*v[j+1] for v in system['low']) for i,j in pairs]
    labels=system['phase_labels'];orbit_grams={oi:[sum(r[1][i] for r in orb) for i in range(21)] for oi,orb in enumerate(system['orbits'])}
    for j,n in support:
        lab=labels[j];bound=[a-n*lab['multiplicity_unit']*b for a,b in zip(bound,orbit_grams[lab['orbit']])]
    index={tuple(sorted(pair)):i for i,pair in enumerate(pairs)}
    def psd(v):return e.q.base.psd([[v[index[tuple(sorted((i,j)))]] for j in range(6)] for i in range(6)])
    e.q.require(min(bound)>=0 and psd(bound),'capacity residual Gram')
    groups={}
    for k,j in enumerate(kept):
        if j<len(labels):groups.setdefault(labels[j]['orbit'],[]).append((k,labels[j]['multiplicity_unit']))
    records=[]
    for oi,variables in sorted(groups.items()):
        gram=orbit_grams[oi];upper=min(a//b for a,b in zip(bound,gram) if b)
        left=0;right=upper+1
        while right-left>1:
            mid=(left+right)//2
            if psd([a-mid*b for a,b in zip(bound,gram)]):left=mid
            else:right=mid
        divisor=math.gcd(*(u for j,u in variables));capacity=left-left%divisor
        row=len(rhs)
        for col in cols:col.append(0)
        for j,unit in variables:cols[j][row]=unit
        rhs.append(capacity);slack=[0]*len(rhs);slack[-1]=1;cols.append(slack)
        records.append({'orbit':oi,'integer_psd_capacity':left,'packet_gcd':divisor,'capacity':capacity})
    return cols,rhs,records


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('case',type=int,choices=[0,1]);ap.add_argument('--phi',action='store_true');ap.add_argument('--exact',action='store_true');ap.add_argument('--capacities',action='store_true');args=ap.parse_args()
    import numpy as np
    from scipy.optimize import linprog
    from exact_branch_bound import exact_ray
    stem=f'R7_5_5039_c8_case{args.case}_chi8_0';path=e.HERE.parent/'criteria'/(stem+'_system.json');raw=path.read_bytes();system=json.loads(raw)
    grams=json.loads((e.HERE/(stem+'_phase_gram.json')).read_text());inventory=json.loads((e.HERE/(stem+'_system_phase_lattice.json')).read_text())
    packets=fixed_packets(system,grams);phis=json.loads((e.HERE/(stem+'_phi_cross_allocations.json')).read_text())['allocations'] if args.phi else None
    output={'system_sha256':hashlib.sha256(raw).hexdigest(),'case':args.case,'scope':'Conditional packet branches; requires the separate forced-packet proof.','branches':[]}
    outpath=e.HERE/(stem+'_forced50'+('_phi' if args.phi else '')+('_capacities' if args.capacities else '')+'.json')
    for pi,packet in enumerate(packets):
        for fi in ([2,14,46,49] if args.phi else [None]):
            start=time.monotonic();record={'packet':pi,**packet,'phi_case':fi}
            try:cols,rhs,kept,removed=branch_system(system,inventory,packet,None if fi is None else phis[fi])
            except RuntimeError as exc:
                if 'fixed packets fit source Gram' not in str(exc):raise
                record['invalid_residual_gram']=True
            else:
                if args.capacities:
                    cols,rhs,capacities=orbit_capacity_cuts(system,[c[:] for c in cols],rhs[:],kept,packet['support']+(phis[fi] if fi is not None else []))
                    record['capacities']=capacities
                aa=np.array(cols,dtype=float).T;bb=np.array(rhs,dtype=float);scale=np.maximum(1,np.maximum(np.max(abs(aa),axis=1),abs(bb)))
                sol=linprog(np.zeros(len(cols)),A_eq=aa/scale[:,None],b_eq=bb/scale,bounds=(0,None),method='highs')
                record.update({'kept':kept,'removed':removed,'lp_status':int(sol.status)})
                if not sol.success and args.exact:
                    ray=exact_ray(list(map(list,zip(*cols))),rhs)
                    if ray is not None:verify_ray(cols,rhs,ray);record['ray']=ray
            record['seconds']=time.monotonic()-start;output['branches'].append(record)
            outpath.write_text(json.dumps(output,separators=(',',':'))+'\n')
            print(json.dumps({k:v for k,v in record.items() if k not in ('kept','removed','forbidden','ray','capacities')}|{'exact':'ray'in record}),flush=True)


if __name__=='__main__':main()
