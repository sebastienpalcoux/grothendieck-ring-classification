"""Longer exact searches, isolated from the accepted M5 ledger.

Discovery results are candidates until independently replayed and scope reviewed.
The process-group watchdog is strict; elapsed budgets never imply exclusion.
"""
import os
for name in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):
    os.environ[name]='1'
import argparse,concurrent.futures,faulthandler,hashlib,json,signal,subprocess,sys,time,traceback
from pathlib import Path
faulthandler.register(signal.SIGUSR1)
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
SUPP=ROOT/'supplements/rank7'
sys.path[:0]=[str(SUPP),str(SUPP/'software')]
LEDGER=HERE/'source_frontier.json'
PIN='508164c3f342f27988401e7c64e6efc83a844e5013a1d68f9b35c5124088c741'
FRONTIER_SHA='2ad72e27068d3a6d379c34aa8ea8a303649011440cb45443431f507fa8174105'

def emit(event,**data):
    print(json.dumps({'event':event,**data},separators=(',',':')),flush=True)

def stop_requested(rid):
    path=HERE/'stop_requests.json'
    return path.exists() and rid in json.loads(path.read_text())

def install_runtime(budget,fast=False):
    """Increase execution budgets without modifying the mathematical tests."""
    original=subprocess.run
    def run(cmd,*args,**kwargs):
        binary=Path(cmd[0]).name if isinstance(cmd,(list,tuple)) else ''
        if binary in ('enum','low_generic','gram_vectors_general'):
            if fast and binary=='low_generic':cmd=[str(HERE/'low_frames_fast')]+list(cmd[1:])
            kwargs['timeout']=budget
            emit('native_start',binary=binary,timeout=budget)
            start=time.monotonic();result=original(cmd,*args,**kwargs)
            emit('native_complete',binary=binary,seconds=time.monotonic()-start,
                 output_lines=len((result.stdout or '').splitlines()))
            return result
        return original(cmd,*args,**kwargs)
    subprocess.run=run
    import induction,higher_traces
    original_low=induction.low_matrices
    low_cache={}
    def low(*args,**kwargs):
        key=(tuple(tuple(cols) for cols in args[0]),tuple(map(int,args[1])),kwargs.get('gram_prune',False))
        if fast and key in low_cache:
            emit('low_cached',frames=len(low_cache[key]));return low_cache[key]
        emit('low_start',column_counts=list(map(len,args[0])))
        start=time.monotonic();out=original_low(*args,**kwargs)
        emit('low_complete',frames=len(out),seconds=time.monotonic()-start)
        if fast:low_cache[key]=out
        return out
    original_high=higher_traces.high_columns
    high_operation=original_high
    if fast:
        from high_columns_fast import high_columns
        high_operation=high_columns
    def high(*args,**kwargs):
        emit('high_start')
        start=time.monotonic();out=high_operation(*args,**kwargs)
        emit('high_complete',vectors=len(out[1]),seconds=time.monotonic()-start)
        return out
    # Modules use from-import aliases; replace every already-loaded alias.
    import advanced_criteria,character_induction,modular_character_induction
    import tensor_rotation,oriented_extension,balanced_traces,integer_gram,proofs,extension
    modules=[induction,higher_traces,advanced_criteria,character_induction,
             modular_character_induction,tensor_rotation,oriented_extension,
             balanced_traces,integer_gram,proofs,extension]
    for mod in modules:
        if getattr(mod,'low_matrices',None) is original_low:mod.low_matrices=low
        if getattr(mod,'high_columns',None) is original_high:mod.high_columns=high
    def phase_wrapper(name,operation):
        def wrapped(*args,**kwargs):
            details={}
            if name=='farkas':details={'rows':len(args[1]),'columns':len(args[0][0])}
            emit(name+'_start',**details);start=time.monotonic()
            ray_path=None
            if name=='farkas' and fast:
                digest=hashlib.sha256(json.dumps(args[:2],separators=(',',':')).encode()).hexdigest()
                ray_path=HERE/'exact_rays'/('system_'+digest+'.json')
                if ray_path.exists():
                    result=json.loads(ray_path.read_text())['y']
                    if higher_traces.check_farkas(args[0],args[1],result,raise_error=False):
                        emit('farkas_checkpoint_reused',system_sha256=digest);return result
            result=operation(*args,**kwargs)
            if ray_path is not None and result is not None:
                higher_traces.check_farkas(args[0],args[1],result)
                ray_path.parent.mkdir(exist_ok=True)
                temporary=ray_path.with_name(ray_path.name+'.'+str(os.getpid())+'.tmp')
                temporary.write_text(json.dumps({'system_sha256':digest,'rows':len(args[1]),'columns':len(args[0][0]),'y':result,'bTy':sum(x*y for x,y in zip(args[1],result))},separators=(',',':'))+'\n')
                temporary.replace(ray_path)
            emit(name+'_complete',seconds=time.monotonic()-start,
                 **({'found':result is not None} if name=='farkas' else {}))
            return result
        return wrapped
    for name in ('system_rotation','farkas'):
        operation=getattr(tensor_rotation,name);wrapped=phase_wrapper(name,operation)
        for mod in modules:
            if getattr(mod,name,None) is operation:setattr(mod,name,wrapped)
    return modules

def worker(task):
    row,stage,budget,height=task
    R=row['tensor'];start=time.monotonic()
    emit('start',id=row['id'],stage=stage,budget=budget,height=height,pid=os.getpid())
    if stop_requested(row['id']):
        result={'id':row['id'],'stage':stage,'height':height,'status':'cancelled_after_independent_exclusion','certificate':None,'scope':'No new conclusion from this cancelled search.','seconds':0}
        (HERE/(row['id']+'_'+stage+'_h'+str(height)+'.json')).write_text(json.dumps(result)+'\n')
        emit('cancelled',id=row['id']);return
    controls=HERE/'acceleration_controls.json'
    fast=controls.exists() and json.loads(controls.read_text())['status']=='PASS'
    install_runtime(budget-30,fast=fast)
    import advanced_criteria,oriented_extension,character_induction,proofs
    if stage in ('character','tensor_rotation','modular'):
        emit('eligibility',**advanced_criteria.eligibility(R,stage,height))
    if stage=='signed_quotients':
        from oriented_signed import enumerate_all
        values,problem,statistics=enumerate_all(R,timeout=budget-30)
        result={'id':row['id'],'stage':stage,'status':'complete_enumeration',
                'scope':'Necessary oriented sphericalization quotients only; no exclusion.',
                'values':[list(v) for v in values],'domains':problem['domains'],
                'active_orbits':problem['active'],'statistics':statistics,
                'seconds':time.monotonic()-start,'accepted_ledger_sha256':PIN}
        (HERE/(row['id']+'_'+stage+'_h'+str(height)+'.json')).write_text(json.dumps(result,separators=(',',':'))+'\n')
        emit('result',id=row['id'],stage=stage,status=result['status'],quotients=len(values),seconds=result['seconds'])
        return
    elif stage=='oriented_dimension_order':
        from m5_campaign import pure_dimension_order
        c=pure_dimension_order(R,2*budget)
    elif stage=='general_induction':
        c=oriented_extension.certificate(R,height=height,timeout=budget-30,integral=True)
    else:
        c=advanced_criteria.general_certificate(R,mode=stage,height=height,timeout=budget-30)
    result={'id':row['id'],'stage':stage,'height':height,'seconds':time.monotonic()-start,
            'status':'candidate_exclusion' if c else 'no_certificate',
            'scope':'unreviewed_candidate' if c else 'no_conclusion','certificate':c,
            'accepted_ledger_sha256':PIN}
    (HERE/(row['id']+'_'+stage+'_h'+str(height)+'.json')).write_text(json.dumps(result,separators=(',',':'))+'\n')
    emit('result',**{k:v for k,v in result.items() if k!='certificate'})

def isolated(task):
    row,stage,budget,height=task
    name=row['id']+'_'+stage+'_h'+str(height)
    log=HERE/(name+'.log')
    with log.open('w') as stream:
        proc=subprocess.Popen([sys.executable,str(Path(__file__).resolve()),'--worker'],
            stdin=subprocess.PIPE,stdout=stream,stderr=stream,text=True,start_new_session=True)
        try:proc.communicate(json.dumps(task),timeout=budget)
        except subprocess.TimeoutExpired:
            os.killpg(proc.pid,signal.SIGKILL);proc.communicate()
            return {'id':row['id'],'stage':stage,'height':height,'status':'budget_exhausted','budget':budget,'log':log.name}
    target=HERE/(name+'.json')
    if proc.returncode==124:
        return {'id':row['id'],'stage':stage,'height':height,'status':'budget_exhausted','budget':budget,'log':log.name}
    if proc.returncode or not target.exists():
        return {'id':row['id'],'stage':stage,'height':height,'status':'error','returncode':proc.returncode,'log':log.name}
    result=json.loads(target.read_text());result.pop('certificate',None);return result

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--jobs',type=int,default=3)
    parser.add_argument('--budget',type=int,default=1200)
    parser.add_argument('--height',type=int,default=6)
    parser.add_argument('--tasks',type=Path)
    parser.add_argument('--replay',type=Path)
    args=parser.parse_args()
    if hashlib.sha256(LEDGER.read_bytes()).hexdigest()!=FRONTIER_SHA:raise ValueError('initial frontier tensor snapshot changed')
    if args.replay:
        for optimized in (False,True):
            target=args.replay.with_name(args.replay.stem+('_optimized' if optimized else '_normal')+'.log')
            with target.open('w') as stream:
                cmd=[sys.executable]+(['-O'] if optimized else [])+[str(Path(__file__).resolve()),'--verify-worker']
                proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout=stream,stderr=stream,text=True,start_new_session=True)
                try:proc.communicate(json.dumps([str(args.replay.resolve()),args.budget]),timeout=args.budget)
                except subprocess.TimeoutExpired:
                    os.killpg(proc.pid,signal.SIGKILL);proc.communicate();raise TimeoutError('exact replay watchdog expired')
            if proc.returncode:raise RuntimeError('exact replay failed; see '+str(target))
        return
    if not args.tasks:parser.error('--tasks or --replay is required')
    rows={r['id']:r for r in json.loads(LEDGER.read_text()) if r['status']=='unresolved'}
    tasks=[(rows[rid],stage,args.budget,args.height) for rid,stage in json.loads(args.tasks.read_text())]
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as pool:
        for result in pool.map(isolated,tasks):
            with (HERE/'results.jsonl').open('a') as stream:stream.write(json.dumps(result,separators=(',',':'))+'\n')
            emit('finished',**result)
    if hashlib.sha256(LEDGER.read_bytes()).hexdigest()!=FRONTIER_SHA:raise ValueError('initial frontier tensor snapshot changed during campaign')

if __name__=='__main__':
    if '--verify-worker' in sys.argv:
        candidate,budget=json.load(sys.stdin);candidate=Path(candidate)
        result=json.loads(candidate.read_text());start=time.monotonic()
        install_runtime(budget-30)
        from verify_m5 import verify_new
        row=next(r for r in json.loads(LEDGER.read_text()) if r['id']==result['id'])
        row['certificate']=result['certificate'];verify_new(row)
        receipt={'status':'PASS','id':row['id'],'optimized_python':not __debug__,
                 'candidate_sha256':hashlib.sha256(candidate.read_bytes()).hexdigest(),
                 'accepted_ledger_sha256':PIN,'seconds':time.monotonic()-start,
                 'method':'Independent inherited exact checker; numerical optimizers disabled.'}
        target=candidate.with_name(candidate.stem+('_optimized' if not __debug__ else '_normal')+'_replay.json')
        target.write_text(json.dumps(receipt,indent=2)+'\n');emit('verified',**receipt)
    elif '--worker' in sys.argv:
        try:worker(json.load(sys.stdin))
        except (TimeoutError,subprocess.TimeoutExpired):
            traceback.print_exc();sys.exit(124)
        except Exception:
            traceback.print_exc();sys.exit(1)
    else:main()
