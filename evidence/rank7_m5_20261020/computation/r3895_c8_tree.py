"""Finite exact integer-split trees for the four surviving R3895 phi frames."""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[key]='1'
import argparse,hashlib,json,math,sys,time
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
from r3895_c8_active import restrict
from inactive_lattice import require
from exact_branch_bound import bound_system,exact_ray,replay
HERE=Path(__file__).resolve().parent;BASE=HERE.parent
sys.path.insert(0,str(BASE/'integral_gram'))
from forced_eighth_packets import orbit_capacity_cuts

def build(case,branch,r=None,s=None):
    path=BASE/'criteria'/f'R7_5_3895_c8_case{case}_system.json';raw=path.read_bytes();system=json.loads(raw)
    cols,rhs,details=restrict(system,branch);kept=details['kept']
    if r is not None:
        obj=system['cyclic_four'][0];require(type(r)is int and 0<=r<=obj['A'] and type(s)is int and 0<=s<=obj['B'],'complete cyclic multiplicity bound')
        fixed=dict(zip(obj['variables'],[r,obj['A']-r,s,obj['B']-s]))
        rhs=[b-sum(system['columns'][j][i]*n for j,n in fixed.items()) for i,b in enumerate(rhs)]
        kept=[j for j in kept if j not in fixed];cols=[system['columns'][j][:] for j in kept]
    cols,rhs,capacities=orbit_capacity_cuts(system,[c[:] for c in cols],rhs[:],kept,details['support'])
    paths=[path,HERE/'r3895_c8_active.py',BASE/'integral_gram/forced_eighth_packets.py']
    bindings={str(p.relative_to(HERE.parents[2])):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths};bindings.update(details['source_hashes'])
    return [list(row) for row in zip(*cols)],rhs,kept,len(system['phase_labels']),bindings,capacities

def main():
    p=argparse.ArgumentParser();p.add_argument('--case',type=int,choices=[0,2],default=0);p.add_argument('--branch',type=int,choices=[0,19,160,165],default=0);p.add_argument('--r',type=int);p.add_argument('--s',type=int);p.add_argument('--seconds',type=int,default=300);p.add_argument('--nodes',type=int,default=500);p.add_argument('--replay',action='store_true');a=p.parse_args()
    A,b,kept,phase_count,bindings,capacities=build(a.case,a.branch,a.r,a.s)
    stem=f'R7_5_3895_c8_case{a.case}_phi{a.branch}'+(f'_r{a.r}_s{a.s}' if a.r is not None else '')
    path=HERE/(stem+'_tree.json');progress=HERE/(stem+'_tree.progress.json')
    if a.replay:
        cert=json.loads(path.read_text());require(cert['source_hashes']==bindings and cert['capacities']==capacities,'source binding and exact capacity replay')
        leaves=replay(A,b,cert['tree']);require(leaves==cert['leaves'],'complete exact tree leaf count')
        report={'status':'PASS','case':a.case,'branch':a.branch,'r':a.r,'s':a.s,'leaves':leaves,'optimized_python':not __debug__}
        (HERE/(stem+'_tree_replay_'+('optimized' if not __debug__ else 'normal')+'.json')).write_text(json.dumps(report)+'\n');print(json.dumps(report),flush=True);return
    started=time.monotonic();aa=np.array(A,dtype=float);bb=np.array(b,dtype=float);scale=np.maximum(1,np.maximum(np.max(abs(aa),axis=1),abs(bb)));aa/=scale[:,None];bb/=scale
    stats={'nodes':0,'leaves':0,'depth':0}
    print(json.dumps({'event':'start','case':a.case,'branch':a.branch,'r':a.r,'s':a.s,'variables':len(A[0]),'equations':len(b),'capacities':len(capacities)}),flush=True)
    def solve(bounds,depth):
        stats['nodes']+=1;stats['depth']=max(stats['depth'],depth)
        if stats['nodes']>a.nodes or time.monotonic()-started>a.seconds:raise TimeoutError('bounded certificate search exhausted')
        proposal=linprog(np.zeros(len(A[0])),A_eq=aa,b_eq=bb,bounds=[bounds.get(j,(0,None)) for j in range(len(A[0]))],method='highs')
        if not proposal.success:
            matrix,target=bound_system(A,b,bounds);ray=exact_ray(matrix,target)
            if ray is None:raise RuntimeError('unsuccessful LP has no exact Farkas witness: '+proposal.message)
            stats['leaves']+=1;progress.write_text(json.dumps(stats)+'\n')
            print(json.dumps({'event':'leaf',**stats,'seconds':time.monotonic()-started}),flush=True);return {'y':ray}
        fractions=[(min(x-math.floor(x),math.ceil(x)-x),j,x) for j,x in enumerate(proposal.x) if abs(x-round(x))>1e-6]
        if not fractions:
            values=[round(float(x)) for x in proposal.x]
            if all(sum(v*x for v,x in zip(row,values))==y for row,y in zip(A,b)):raise RuntimeError('exact integer feasible point; no exclusion')
            raise RuntimeError('near-integer proposal fails exact equations')
        aux=[f for f in fractions if f[1]>=len(kept) or kept[f[1]]>=phase_count]
        _,j,value=max(aux or fractions);k=math.floor(value);lo,hi=bounds.get(j,(0,None));require(k>=lo and (hi is None or k<hi),'valid full integer split')
        left,right=dict(bounds),dict(bounds);left[j]=(lo,k);right[j]=(k+1,hi)
        return {'variable':j,'floor':k,'left':solve(left,depth+1),'right':solve(right,depth+1)}
    try:tree=solve({},0)
    except (RuntimeError,TimeoutError) as error:
        out={'status':'no_complete_certificate','case':a.case,'branch':a.branch,'r':a.r,'s':a.s,'reason':str(error),**stats,'seconds':time.monotonic()-started}
        progress.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out),flush=True);return
    leaves=replay(A,b,tree);out={'scope':'Exact integer infeasibility conditional on the audited phi allocation and optional C4 multiplicities.','case':a.case,'branch':a.branch,'r':a.r,'s':a.s,'source_hashes':bindings,'capacities':capacities,'tree':tree,'leaves':leaves,'statistics':stats,'seconds':time.monotonic()-started}
    path.write_text(json.dumps(out,separators=(',',':'))+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('tree','capacities','source_hashes')}),flush=True)
if __name__=='__main__':main()
