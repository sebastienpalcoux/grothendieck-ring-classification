"""Bounded short discovery of established involution-module obstructions.

All accepted negatives are exhaustions of the displayed finite candidate set.
Discovery limits (at most two generators, fixed rank <=4, <=4096 generator
assignments) return no conclusion and are recorded, never called exclusions.
"""
from pathlib import Path
import collections,importlib.util,json,signal,sys,time
ROOT=Path(__file__).resolve().parent
P=ROOT/'sources/evidence/rank11_m1_20261023/work/rank11/structural'
sys.path.insert(0,str(P))
from support import generated_basis
sys.path.insert(0,str(ROOT/'sources/work/rank11'))
import common
def load():
    src=(ROOT/'sources/work/rank11/structural/legacy_noncomm_module.py').read_text()
    src=src.replace('if not 0<f<=3:return None','if not 0<f<=4:return None')
    src=src.replace('for count in range(1,n):','for count in range(1,3):')
    src=src.replace('_,seed,(words,inv)=min(choices,key=lambda v:(v[0],v[1]));','budget,seed,(words,inv)=min(choices,key=lambda v:(v[0],v[1]));\n if budget>4096:return None\n ')
    ns={'__name__':'adapted_module'};exec(compile(src,'adapted_module.py','exec'),ns)
    (ROOT/'adapted_module.py').write_text(src)
    return ns
def handler(*args):raise TimeoutError('short-check budget; no conclusion')

def main():
    start=time.monotonic();ns=load();data=json.loads((ROOT/'tensors.json').read_text())
    cl=json.loads((ROOT/'subrings.json').read_text())['classes'];results=[]
    targets=[('subring_class_'+str(i),c['tensor'])for i,c in enumerate(cl)if not c['certificate']]
    targets += [(rid,data[rid])for rid in json.loads((ROOT/'remaining_after_basic.json').read_text())]
    signal.signal(signal.SIGALRM,handler)
    for rid,R in targets:
        cache={}
        def basis(A,seed):
            key=tuple(seed)
            if key not in cache:cache[key]=generated_basis(A,seed)
            return cache[key]
        ns['generated_basis']=basis;c=None;attempts=[]
        for g in ns['invs'](R):
            fixed=[x for x in range(len(R))if R[x][g][x]]
            if not 0<len(fixed)<=4:continue
            if any(sum(R[i][x][y]for x in fixed for y in fixed)>12 for i in range(len(R))):
                attempts.append(dict(involution=g,result='candidate_size_budget'));continue
            signal.setitimer(signal.ITIMER_REAL,0.8)
            try:z=ns['solve'](R,g)
            except TimeoutError:
                attempts.append(dict(involution=g,result='time_budget'));continue
            finally:signal.setitimer(signal.ITIMER_REAL,0)
            attempts.append(dict(involution=g,result='no_conclusion'if z is None else'feasible'if z['feasible']else'excluded',search=z))
            if z is not None and not z['feasible']:
                c=dict(kind='involution_module',involution=g,scope='general_complex_fusion_category',**z);break
        results.append(dict(id=rid,tensor_sha256=common.sha(R),certificate=c,attempts=attempts))
        if len(results)%20==0:print('processed',len(results),'excluded',sum(r['certificate']is not None for r in results),'seconds',round(time.monotonic()-start,2),flush=True)
    out=dict(records=results,discovery_limits=dict(fixed_rank=4,generators=2,generator_assignments=4096,seconds_per_involution=0.8),elapsed_seconds=time.monotonic()-start)
    (ROOT/'modules.json').write_text(json.dumps(out,indent=2)+'\n')
    print('DONE',len(results),'excluded',sum(r['certificate']is not None for r in results),'seconds',time.monotonic()-start)

if __name__=='__main__':main()
