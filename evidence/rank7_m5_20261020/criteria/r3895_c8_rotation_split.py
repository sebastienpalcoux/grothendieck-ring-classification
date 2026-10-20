"""Exact conditional 30-way C4 source-character split for R3895 C8 data."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import time
import q5_cyclic_eight_search as search

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'computation'))
from r3895_c8_active import restrict
q=search.q


def separate(columns,rhs,pool):
    # A feasible primal proposal prevents a slow, degenerate dual-ray search.
    # It never certifies anything: every accepted exclusion remains an exact
    # integer covector checked by q.separate and by the optimizer-free replay.
    for i,y in enumerate(pool):
        if q.base.dot(rhs,y)<0 and all(q.base.dot(col,y)>=0 for col in columns):return i
    import numpy as np
    from scipy.optimize import linprog
    A=np.array(columns,dtype=float).T;b=np.array(rhs,dtype=float)
    scale=np.maximum(1,np.maximum(abs(A).max(axis=1),abs(b)))
    result=linprog(np.zeros(A.shape[1]),A_eq=A/scale[:,None],b_eq=b/scale,bounds=(0,None),method='highs',options={'time_limit':15})
    if result.success:return None
    import signal
    def timeout(signum,frame):raise TimeoutError('bounded exact-ray discovery')
    previous=signal.signal(signal.SIGALRM,timeout);signal.alarm(20)
    try:return q.separate(columns,rhs,pool)
    except TimeoutError:return None
    finally:signal.alarm(0);signal.signal(signal.SIGALRM,previous)


def run(case,branch,replay=False):
    start=time.monotonic()
    path=HERE/f'R7_5_3895_c8_case{case}_system.json';raw=path.read_bytes();system=json.loads(raw)
    target=HERE/f'R7_5_3895_c8_case{case}_branch{branch}_rotation_split.json'
    cols,rhs,details=restrict(system,branch)
    ob=system['cyclic_four'][0]
    q.require(ob['A']==9 and ob['B']==2,'complete thirty-value C4 character domain')
    indices=ob['variables'];fixed=set(indices)
    q.require(fixed<=set(details['kept']),'all source C4 variables survived Gram pruning')
    keep=[j for j in details['kept'] if j not in fixed]
    columns=[system['columns'][j] for j in keep]
    old=json.loads(target.read_text()) if replay else None
    if replay:
        q.require(old['source_sha256']==hashlib.sha256(raw).hexdigest(),'source-bound C8 system')
        q.require(old['restriction']==details,'exact source active/Gram restriction')
        pool=old['separators']
    else:
        pool=[]
        for prior in sorted(HERE.glob('R7_5_3895_c8_case*_branch*_rotation_split.json')):
            try:previous=json.loads(prior.read_text())
            except json.JSONDecodeError:continue  # another discovery job may be checkpointing
            for ray in previous['separators']:
                if ray not in pool:pool.append(ray)
    results=[]
    def output():
        out={'scope':'Conditional on the source-bound saturated active allocation; only exact rays are exclusions.',
             'case':case,'branch':branch,'source_sha256':hashlib.sha256(raw).hexdigest(),'restriction':details,
             'results':results,'separators':pool,'unresolved':[{'r':z['r'],'s':z['s']} for z in results if z['separator'] is None]}
        if not replay:target.write_text(json.dumps(out)+'\n')
        return out
    for r in range(10):
        for s in range(3):
            counts=(r,9-r,s,2-s)
            residual=[b-sum(n*system['columns'][j][i] for j,n in zip(indices,counts)) for i,b in enumerate(rhs)]
            if replay:
                sep=old['results'][3*r+s]['separator']
                if sep is not None:
                    ray=pool[sep]
                    q.require(len(ray)==len(rhs) and all(type(x)is int for x in ray),'integer Farkas covector')
                    q.require(q.base.dot(residual,ray)<0 and all(q.base.dot(col,ray)>=0 for col in columns),'exact C4 branch separation')
            else:sep=separate(columns,residual,pool)
            record={'r':r,'s':s,'separator':sep}
            if replay:q.require(record==old['results'][3*r+s],'same finite character branch')
            results.append(record);output()
        print(json.dumps({'case':case,'branch':branch,'r':r,'pool':len(pool),'unresolved':sum(z['separator'] is None for z in results),'seconds':time.monotonic()-start}),flush=True)
    out=output()
    if replay:q.require(out==old,'complete exact replay')
    receipt={'status':'PASS' if replay else 'COMPLETE','case':case,'branch':branch,'exact_separated':sum(z['separator'] is not None for z in results),'unresolved':out['unresolved'],'seconds':time.monotonic()-start,'optimized_python':not __debug__}
    if replay:(HERE/f'R7_5_3895_c8_case{case}_branch{branch}_rotation_replay_{"normal" if __debug__ else "optimized"}.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--case',type=int,choices=[0,2],required=True);parser.add_argument('--branch',type=int,choices=[0,19,160,165],required=True);parser.add_argument('--replay',action='store_true');a=parser.parse_args();run(a.case,a.branch,a.replay)
