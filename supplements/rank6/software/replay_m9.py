"""Independent bounded exact replay of new multiplicity-nine certificates.

Run with optimized Python to verify proofs independently of assert statements:
  timeout 890 python -O software/replay_m9.py --jobs 4 --seconds 840 --resume
No earlier certificate campaign is read or recomputed. Discovery optimizers are
unavailable to the replay worker; every failure remains a failed verification.
"""
import os
for name in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):
    os.environ[name]='1'
import argparse,hashlib,json,signal,subprocess,sys,time,traceback
from concurrent.futures import ProcessPoolExecutor,ThreadPoolExecutor,wait,FIRST_COMPLETED
from pathlib import Path
P=Path(__file__).resolve().parents[1]
class ReplayDeadline(Exception):pass

def verify_worker(payload):
    row,record=payload;start=time.monotonic()
    out={'id':row['id'],'m':row['m'],'kind':record['certificate']['kind'],'passed':False,
         'optimized_python':not __debug__,'optimizer_disabled':True,
         'certificate_sha256':hashlib.sha256(json.dumps(record['certificate'],sort_keys=True,separators=(',',':')).encode()).hexdigest()}
    try:
        def stop(*args):raise ReplayDeadline('exact replay deadline exhausted')
        signal.signal(signal.SIGALRM,stop);signal.alarm(240)
        import scipy.optimize
        def forbidden(*args,**kwargs):raise RuntimeError('optimizer forbidden during exact M9 replay')
        scipy.optimize.linprog=scipy.optimize.milp=forbidden
        cert=record['certificate']
        if cert['kind']=='module_dual_gram':
            from module_dual_gram import verify
        else:
            from check import verify
        verify(row['N'],cert);out['passed']=True
    except Exception as exc:out.update(error=f'{type(exc).__name__}: {exc}',traceback=traceback.format_exc())
    finally:signal.alarm(0);out['seconds']=time.monotonic()-start
    return out

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--jobs',type=int,default=4);ap.add_argument('--seconds',type=int,default=840);ap.add_argument('--resume',action='store_true')
    args=ap.parse_args()
    if args.jobs<1 or not 1<=args.seconds<=840:ap.error('jobs positive and seconds in 1..840 required')
    deadline=time.monotonic()+args.seconds
    source=P/'certificates/m9_classification.jsonl';source_bytes=source.read_bytes();records=[json.loads(line) for line in source_bytes.splitlines()]
    rows={r['id']:r for r in json.loads((P/'data/census.json').read_text()) if r['m']==9}
    if len({r['id'] for r in records})!=len(records):raise ValueError('duplicate certificate identifiers')
    if any(r['id'] not in rows or not r.get('exact_checked') or r.get('status')!='excluded' or r.get('m')!=9 for r in records):raise ValueError('malformed input certificate campaign')
    identity={'certificate_file_sha256':hashlib.sha256(source_bytes).hexdigest(),'census_sha256':hashlib.sha256((P/'data/census.json').read_bytes()).hexdigest(),'input_count':len(records),'optimized_python':not __debug__}
    base=P/'verification/m9/replay';base.mkdir(parents=True,exist_ok=True)
    name='optimized' if not __debug__ else 'normal';manifest=base/(name+'_manifest.json');progress=base/(name+'.jsonl');seen={}
    def atomic_text(path,value):
        temporary=path.with_name(path.name+'.tmp');temporary.write_text(value);os.replace(temporary,path)
    if manifest.exists():
        if not args.resume:raise ValueError('existing replay: pass --resume')
        prior=json.loads(manifest.read_text())
        if any(prior[key]!=identity[key] for key in ('census_sha256','optimized_python')):raise ValueError('replay tensor source changed')
        if prior['input_count']>identity['input_count']:raise ValueError('replay certificate source shrank')
        lines=progress.read_text().splitlines()
        for i,line in enumerate(lines):
            try:x=json.loads(line)
            except json.JSONDecodeError:
                if i!=len(lines)-1:raise ValueError('damaged replay checkpoint')
                atomic_text(progress,''.join(v+'\n' for v in lines[:i]));break
            seen[x['id']]=x
        current={r['id']:hashlib.sha256(json.dumps(r['certificate'],sort_keys=True,separators=(',',':')).encode()).hexdigest() for r in records}
        if any(rid not in current or rec['certificate_sha256']!=current[rid] for rid,rec in seen.items()):raise ValueError('previously replayed certificate changed')
        atomic_text(manifest,json.dumps(identity,indent=2)+'\n')
    else:atomic_text(manifest,json.dumps(identity,indent=2)+'\n');progress.write_text('')
    tasks=iter((rows[r['id']],r) for r in records if r['id'] not in seen)
    with progress.open('a') as stream,ProcessPoolExecutor(max_workers=args.jobs) as pool:
        pending={}
        def submit():
            if time.monotonic()+248>=deadline:return False
            task=next(tasks,None)
            if task is None:return False
            pending[pool.submit(verify_worker,task)]=task[0]['id'];return True
        for _ in range(args.jobs):submit()
        while pending:
            done,_=wait(pending,return_when=FIRST_COMPLETED)
            for future in done:
                pending.pop(future);out=future.result();seen[out['id']]=out
                stream.write(json.dumps(out,separators=(',',':'))+'\n');stream.flush()
                if len(seen)%250==0 or not out['passed']:print('REPLAY',len(seen),'/',len(records),out['id'],out['passed'],out.get('error',''),flush=True)
                submit()
    result=dict(identity,completed=len(seen),passed=sum(x['passed'] for x in seen.values()),failed=[x['id'] for x in seen.values() if not x['passed']],complete=len(seen)==len(records),optimizer_disabled=True)
    atomic_text(base/(name+'_summary.json'),json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

if __name__=='__main__':main()
