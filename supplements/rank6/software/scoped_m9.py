"""Recover bounded PU-only obstructions whose general signed lift did not finish.

Discovery and independent optimized replay are separate bounded subprocesses.
No proposed certificate changes a categorical status before exact replay.
"""
import os
for name in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):
    os.environ[name]='1'
import argparse,hashlib,json,signal,subprocess,sys,time,traceback
from concurrent.futures import ThreadPoolExecutor,as_completed
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def sha(x):return hashlib.sha256(json.dumps(x,separators=(',',':'),sort_keys=True).encode()).hexdigest()

def worker(task):
    row,mode,certificate=task;out=dict(id=row['id'],m=row['m'],tensor_sha256=sha(row['N']),mode=mode)
    try:
        import oriented_extension as O
        if mode=='discover':
            c=O.pseudo_discover(row['N'],height=6,integral=True)
            out.update(status='proposed' if c is not None else 'survives',certificate=c)
        else:
            import scipy.optimize as opt
            def denied(*a,**kw):raise RuntimeError('optimizer forbidden in exact PU replay')
            opt.linprog=opt.milp=denied
            O.pseudo_check(row['N'],certificate)
            out.update(status='verified',passed=True,optimized_python=not __debug__,optimizer_disabled=True,
                       certificate_sha256=sha(certificate))
    except Exception as exc:
        out.update(status='ineligible' if type(exc).__name__=='Ineligible' else 'error',diagnostic=type(exc).__name__+': '+str(exc),traceback=traceback.format_exc())
    return out

def bounded(task,seconds):
    start=time.monotonic();row,mode,c=task
    command=[sys.executable]+(['-O'] if mode=='verify' else [])+[str(Path(__file__).resolve()),'--worker']
    with subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,start_new_session=True) as p:
        try:
            stdout,stderr=p.communicate(json.dumps(task),timeout=seconds)
            if p.returncode:raise RuntimeError('worker exit '+str(p.returncode)+': '+stderr[-3000:])
            out=json.loads(stdout)
            if out['id']!=row['id'] or out['mode']!=mode or out['tensor_sha256']!=sha(row['N']):raise ValueError('worker source mismatch')
        except subprocess.TimeoutExpired:
            os.killpg(p.pid,signal.SIGKILL);p.communicate()
            out=dict(id=row['id'],m=row['m'],mode=mode,status='budget_exhausted',tensor_sha256=sha(row['N']))
        except Exception as exc:
            out=dict(id=row['id'],m=row['m'],mode=mode,status='error',diagnostic=str(exc),tensor_sha256=sha(row['N']))
    out.update(wall_seconds=time.monotonic()-start,deadline_seconds=seconds);return out

def process(row,seconds):
    out=bounded((row,'discover',None),seconds)
    if out['status']=='proposed':
        check=bounded((row,'verify',out['certificate']),180);out['exact_replay']=check
        out['status']='pseudo_unitary_excluded' if check['status']=='verified' else 'unverified_proposal'
    return out

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--input',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True);ap.add_argument('--jobs',type=int,default=2)
    ap.add_argument('--seconds',type=int,default=30);ap.add_argument('--skip',nargs='*',default=['R6_9_8200'])
    args=ap.parse_args()
    if not 1<=args.seconds<=60 or not 1<=args.jobs<=3:ap.error('seconds 1..60; jobs 1..3')
    rows=json.loads(args.input.read_text());args.output.mkdir(parents=True,exist_ok=True)
    if any(r['m']!=9 for r in rows):raise ValueError('multiplicity-nine input only')
    manifest=dict(input_sha256=sha(rows),input_ids=[r['id']for r in rows],input_count=len(rows),
        census_sha256=hashlib.sha256((ROOT/'data/census.json').read_bytes()).hexdigest(),
        seconds_per_discovery=args.seconds,seconds_per_exact_replay=180,skip=args.skip,
        scope='Pseudo-unitary-only exclusions; general/pivotal/spherical status unaffected.')
    (args.output/'input_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    outputs=[]
    with (args.output/'attempts.jsonl').open('w') as stream,ThreadPoolExecutor(max_workers=args.jobs)as ex:
        fs=[ex.submit(process,r,args.seconds)for r in rows if r['id']not in args.skip]
        for f in as_completed(fs):
            z=f.result();outputs.append(z);stream.write(json.dumps(z,separators=(',',':'))+'\n');stream.flush()
            print(z['id'],z['status'],round(z['wall_seconds'],2),flush=True)
    accepted=[dict(id=z['id'],m=9,structure='pseudo_unitary',certificate=z['certificate'],tensor_sha256=z['tensor_sha256'],
        source='verification/m9/scoped/attempts.jsonl',exact_checked=True,optimized_replay=z['exact_replay'])
        for z in outputs if z['status']=='pseudo_unitary_excluded']
    (args.output/'accepted.json').write_text(json.dumps(accepted,separators=(',',':'))+'\n')
    summary=dict(manifest,complete=True,attempts=len(outputs),accepted=len(accepted),accepted_ids=[z['id']for z in accepted],
        statuses={s:sum(z['status']==s for z in outputs)for s in sorted({z['status']for z in outputs})})
    (args.output/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2),flush=True)

if __name__=='__main__':
    if '--worker'in sys.argv:print(json.dumps(worker(json.load(sys.stdin))))
    else:main()
