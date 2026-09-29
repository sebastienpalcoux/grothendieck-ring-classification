"""Repeat general-scope necessary conditions on every residual tensor.

Every worker has an external process-group deadline. Only an exactly checked
certificate changes status. Run with --jobs 4; inspect the JSONL checkpoint.
This does not rebuild or replace the original classification campaign.
"""
import os
for variable in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):
    os.environ[variable]='1'
import argparse, json, signal, subprocess, sys, time, traceback
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
P=Path(__file__).resolve().parents[1]

def worker(task):
    row,stage=task
    out={'id':row['id'],'m':row['m'],'stage':stage,'status':'survives'}
    try:
        R=row['N']
        if stage=='module_dual_gram':
            import module_dual_gram as mod
            cert=mod.certificate(R)
            check=mod.verify
        else:
            import advanced_criteria as mod
            out['eligibility']=mod.eligibility(R,stage)
            if not out['eligibility']['eligible']:
                out['status']='ineligible'
                return out
            cert=mod.general_certificate(R,mode=stage,timeout=90)
            check=mod.verify
        if cert is not None:
            import scipy.optimize
            def forbidden(*a,**k):
                raise RuntimeError('optimizer called while checking certificate')
            scipy.optimize.linprog=scipy.optimize.milp=forbidden
            check(R,cert)
            out.update(status='excluded',certificate=cert,exact_checked=True)
    except (TimeoutError, subprocess.TimeoutExpired) as exc:
        out.update(status='budget_exhausted',diagnostic=str(exc))
    except Exception as exc:
        out.update(status='error',diagnostic=str(exc),traceback=traceback.format_exc())
    return out

def bounded(task,seconds):
    start=time.monotonic()
    with subprocess.Popen([sys.executable,__file__,'--worker'],stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,start_new_session=True) as proc:
        try:
            stdout,stderr=proc.communicate(json.dumps(task),timeout=seconds)
            try:
                out=json.loads(stdout) if proc.returncode==0 else {
                    'id':task[0]['id'],'m':task[0]['m'],'stage':task[1],
                    'status':'error','diagnostic':stderr[-4000:]}
            except (ValueError,TypeError) as exc:
                out={'id':task[0]['id'],'m':task[0]['m'],'stage':task[1],
                     'status':'error','diagnostic':'Worker output was not a JSON certificate: '+str(exc),
                     'stdout_tail':stdout[-4000:],'stderr_tail':stderr[-4000:]}
        except subprocess.TimeoutExpired:
            os.killpg(proc.pid,signal.SIGKILL);proc.communicate()
            out={'id':task[0]['id'],'m':task[0]['m'],'stage':task[1],
                 'status':'budget_exhausted','deadline_seconds':seconds}
    out['seconds']=time.monotonic()-start
    return out

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--jobs',type=int,default=4)
    ap.add_argument('--seconds',type=int,default=150)
    ap.add_argument('--stages',nargs='+',default=['module_dual_gram','dimension_order','character','tensor_rotation','modular'])
    ap.add_argument('--resume',action='store_true')
    args=ap.parse_args()
    source=P/'verification/continuation/input_residuals.json'
    if not source.exists(): source=P/'data/unresolved_tensors.json'
    rows=json.loads(source.read_text())
    dest=P/'verification/continuation';dest.mkdir(exist_ok=True)
    path=dest/'attempts.jsonl'
    completed={}
    if args.resume and path.exists():
        for line in path.read_text().splitlines():
            record=json.loads(line);completed[record['id'],record['stage']]=record
    tasks=[(r,s) for r in rows for s in args.stages if (r['id'],s) not in completed]
    with path.open('a' if args.resume else 'w') as stream,ThreadPoolExecutor(max_workers=args.jobs) as ex:
        pending=[ex.submit(bounded,t,args.seconds) for t in tasks]
        for future in as_completed(pending):
            out=future.result();completed[out['id'],out['stage']]=out
            stream.write(json.dumps(out,separators=(',',':'))+'\n');stream.flush()
            print(out['id'],out['stage'],out['status'],round(out['seconds'],2),flush=True)
    summary={'input_path':str(source.relative_to(P)),'input_sha256':__import__('hashlib').sha256(source.read_bytes()).hexdigest(),'input_count':len(rows),'tasks':len(completed),'exclusions':sorted({r['id'] for r in completed.values() if r['status']=='excluded'}),
             'statuses':{s:sum(r['status']==s for r in completed.values()) for s in sorted({r['status'] for r in completed.values()})},
             'scope':'General only; ineligibility, errors, survival and deadlines make no classification claim.'}
    (dest/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':
    if '--worker' in sys.argv:print(json.dumps(worker(json.load(sys.stdin))))
    else:main()
