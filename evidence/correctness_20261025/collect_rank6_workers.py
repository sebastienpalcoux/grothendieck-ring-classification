#!/usr/bin/env python3
"""Replay every current rank-six exclusion, retaining complete raw results.

The new receipt is separate from every historical release manifest. Default
arithmetic failures are retried as full unchanged workers in fresh processes
using SYMPY_GROUND_TYPES=python. No timeout or unknown outcome is accepted.
This command does not claim to reconstruct every positive-category associator.
"""
from pathlib import Path
import argparse,ast,collections,hashlib,importlib.util,json,os,subprocess,sys,time
from concurrent.futures import ProcessPoolExecutor

ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'supplements/rank6'
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[key]='1'
sys.path.insert(0,str(BASE));sys.path.insert(0,str(BASE/'software'))
import verify as original

def need(condition,message):
    if not condition:raise RuntimeError(message)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(path,value):Path(path).write_text(json.dumps(value,indent=2)+'\n')
def state():
    paths=[BASE/'verify.py',BASE/'data/census.json',BASE/'data/decisions.json']
    paths += sorted(p for folder in ('software','research','certificates','data') for p in (BASE/folder).rglob('*') if p.is_file() and p.suffix in ('.py','.cpp','.json','.jsonl') and '__pycache__' not in p.parts and not p.name.endswith('.build.json'))
    return {str(p.relative_to(ROOT)):sha(p) for p in paths}
def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output-dir',type=Path,required=True);ap.add_argument('--jobs',type=int,default=2);ap.add_argument('--one',help=argparse.SUPPRESS);ap.add_argument('--collect-only',action='store_true',help='retain all original worker outcomes without interpreting failures');args=ap.parse_args()
    need(args.jobs>0,'positive worker count required')
    rows=json.loads((BASE/'data/census.json').read_text());ledger=json.loads((BASE/'data/decisions.json').read_text());idx={r['id']:r for r in rows}
    if args.one:
        d=next(x for x in ledger if x['id']==args.one);out=original.worker((idx[d['id']],d['certificate']));save(args.output_dir,out);return 0 if out['passed'] else 1
    args.output_dir.mkdir(parents=True,exist_ok=False);out=args.output_dir.resolve();start=time.monotonic();sources=state();save(out/'sources.json',sources)
    need([r['id']for r in rows]==[d['id']for d in ledger] and len(idx)==len(rows)==25421,'exact census and ledger coverage')
    original.verify_source(rows);original.verify_ledger(ledger)
    work=[(idx[d['id']],d['certificate']) for d in ledger if d['status']=='excluded'];need(len(work)==25362,'current exclusion count')
    failures=[];results=[]
    with ProcessPoolExecutor(max_workers=args.jobs)as pool,(out/'original-results.jsonl').open('x')as stream:
        for i,result in enumerate(pool.map(original.worker,work,chunksize=1),1):
            stream.write(json.dumps(result,separators=(',',':'))+'\n');stream.flush();results.append(result)
            if not result['passed']:failures.append(result);print('ORIGINAL_FAILURE',result['id'],result['error'],flush=True)
            if i%200==0:print('CHECKED',i,'/',len(work),flush=True)
    need([r['id']for r in results]==[r['id']for r,c in work],'complete retained ordered raw coverage')
    if args.collect_only:
        need(state()==sources,'rank-six source/input changed during raw collection')
        save(out/'receipt.json',{'status':'RAW_WORKERS_COMPLETE','raw_rows':len(results),'original_worker_failures':len(failures),'raw_results_sha256':sha(out/'original-results.jsonl'),'source_manifest_sha256':sha(out/'sources.json'),'scope':'Complete original raw worker stream; failures require explicit verification routes in replay_rank6.py.'})
        return 0
    retries=[]
    for record in failures:
        path=out/(record['id']+'-python.json');log=out/(record['id']+'-python.log')
        env=dict(os.environ,SYMPY_GROUND_TYPES='python')
        with log.open('x')as stream:run=subprocess.run([sys.executable,str(Path(__file__).resolve()),'--one',record['id'],'--output-dir',str(path)],env=env,stdout=stream,stderr=subprocess.STDOUT)
        retry=json.loads(path.read_text());need(run.returncode==0 and retry['id']==record['id'] and retry['passed'],'complete reference-worker retry failed: '+record['id']);retries.append(retry)
    # Re-execute exactly the original verifier's two post-loop assertions.
    tree=ast.parse((BASE/'verify.py').read_text());body=next(n.body for n in tree.body if isinstance(n,ast.FunctionDef)and n.name=='main')
    first=next(i for i,n in enumerate(body)if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='m1'for t in n.targets))
    last=next(i for i,n in enumerate(body[first:],first)if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='stats'for t in n.targets))
    env=dict(vars(original),ledger=ledger);exec(compile(ast.Module(body=body[first:last],type_ignores=[]),'rank6 exact original post-loop checks','exec'),env)
    need(state()==sources,'rank-six source/input changed during replay')
    effective={r['id']:r['passed']for r in results};effective.update({r['id']:r['passed']for r in retries});need(len(effective)==25362 and all(effective.values()),'effective full certificate coverage')
    receipt={'status':'PASS','scope':'All25362 current exclusion certificates, source import, ledger validation and both original post-loop checks; positive categorical existence is reviewed separately.','raw_original_rows':len(results),'original_worker_failures':len(failures),'complete_python_retries':len(retries),'effective_exclusions':len(effective),'models_in_exact_registry':len(env['positive']),'raw_results_sha256':sha(out/'original-results.jsonl'),'source_manifest_sha256':sha(out/'sources.json'),'source_state_unchanged':True,'mode':'COMPLETE_RAW_COMPOSITE_REPLAY','seconds':time.monotonic()-start}
    save(out/'receipt.json',receipt);print(json.dumps(receipt,indent=2),flush=True);return 0
if __name__=='__main__':raise SystemExit(main())
