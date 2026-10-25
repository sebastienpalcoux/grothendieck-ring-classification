#!/usr/bin/env python3
"""Complete current rank-six certificate replay with exact historical adapters.

All original raw outcomes are retained. Ordinary arithmetic failures require
full unchanged reference-backend workers. The eleven M9 certificates bind
immutable source trees, replayed without weakening any hash check. Each is
transported to its unchanged current tensor/certificate. No unknown passes.
"""
from pathlib import Path
import argparse,ast,hashlib,json,os,shutil,subprocess,sys,time
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];BASE=ROOT/'supplements/rank6'
def need(c,m):
    if not c:raise RuntimeError(m)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return json.loads(Path(p).read_text())
def save(p,v):Path(p).write_text(json.dumps(v,indent=2)+'\n')
def source_state():
    paths=[BASE/'verify.py']
    paths+=sorted(p for folder in('software','research','certificates','data')for p in(BASE/folder).rglob('*')if p.is_file()and p.suffix in('.py','.cpp','.json','.jsonl')and'__pycache__'not in p.parts and not p.name.endswith('.build.json'))
    return {str(p.relative_to(ROOT)):sha(p)for p in paths}
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output-dir',type=Path,required=True);p.add_argument('--jobs',type=int,default=2);p.add_argument('--resume-collection',type=Path,help='reuse a source-bound complete original worker stream');p.add_argument('--immutable-replay',type=Path,help='reuse an independently completed immutable M9 replay');p.add_argument('--reference-replays',type=Path,help='reuse a completed source-bound full reference-worker campaign');a=p.parse_args()
    need(a.jobs>0,'positive worker count');a.output_dir.mkdir(parents=True,exist_ok=False);out=a.output_dir.resolve();start=time.monotonic();sources=source_state();save(out/'current-sources.json',sources)
    execution={f:sha(HERE/f)for f in('replay_rank6.py','collect_rank6_workers.py','replay_immutable_m9.py','replay_rank6_reference_workers.py')};save(out/'execution-sources.json',execution)
    collection=a.resume_collection
    if collection is None:
        collection=out/'collection';log=out/'collection.log'
        with log.open('x')as stream:run=subprocess.run([sys.executable,str(HERE/'collect_rank6_workers.py'),'--output-dir',str(collection),'--jobs',str(a.jobs),'--collect-only'],stdout=stream,stderr=subprocess.STDOUT,cwd=ROOT)
        need(run.returncode==0,'raw worker collection failed; see '+str(log))
    collection=collection.resolve();old_sources=read(collection/'sources.json')
    old_sources={k:v for k,v in old_sources.items()if not k.endswith('.build.json')}
    need(old_sources==sources,'collected worker source/input context differs')
    shutil.copy2(collection/'original-results.jsonl',out/'original-results.jsonl');raw=[json.loads(line)for line in(out/'original-results.jsonl').read_text().splitlines()]
    need(sha(collection/'original-results.jsonl')==sha(out/'original-results.jsonl'),'raw collection changed during copy')
    rows=read(BASE/'data/census.json');ledger=read(BASE/'data/decisions.json');idx={r['id']:r for r in rows};work=[d for d in ledger if d['status']=='excluded']
    need(len(work)==len(raw)==25362 and[r['id']for r in raw]==[d['id']for d in work],'full retained ordered original stream required')
    need(all(r['kind']==d['certificate']['kind']for r,d in zip(raw,work)),'certificate-kind binding')
    current={d['id']:d for d in work};m9={d['id']for d in work if d['certificate']['kind'].startswith('m9_completion_')};need(len(m9)==11,'immutable M9 inventory')
    source_errors=('completion checker closure changed','completion proof/checker bytes changed:','completion proof tree inventory changed:')
    for r in raw:
        if r['id']in m9 and not r['passed']:need(any(r.get('error','').startswith(t)for t in source_errors),'unexpected mathematical failure in corrected M9 path: '+r['id'])
    failures=[r for r in raw if not r['passed']and r['id']not in m9];retries=[]
    reused_reference=0
    if a.reference_replays:
        reference_receipt=read(a.reference_replays/'receipt.json')
        need(reference_receipt['status']=='PASS'and reference_receipt['source_context']==sources and reference_receipt['raw_collection_sha256']==sha(collection/'original-results.jsonl'),'reference campaign source/input differs')
        need(all(sha(a.reference_replays/n)==h for n,h in reference_receipt['files'].items()),'reference campaign output changed')
    for r in failures:
        target=out/(r['id']+'-python.json');log=out/(r['id']+'-python.log')
        if a.reference_replays:
            old=a.reference_replays/target.name;old_log=a.reference_replays/log.name
            value=read(old);need(value['id']==r['id']and value['passed']and old_log.is_file(),'incomplete retained reference worker: '+r['id'])
            shutil.copy2(old,target);shutil.copy2(old_log,log);retries.append(value);reused_reference+=1;print('PASS retained complete reference worker',r['id'],flush=True);continue
        with log.open('x')as stream:run=subprocess.run([sys.executable,str(HERE/'collect_rank6_workers.py'),'--one',r['id'],'--output-dir',str(target)],env=dict(os.environ,SYMPY_GROUND_TYPES='python'),stdout=stream,stderr=subprocess.STDOUT,cwd=ROOT)
        value=read(target);need(run.returncode==0 and value['id']==r['id']and value['passed'],'full unchanged reference worker failed: '+r['id']);retries.append(value);print('PASS reference worker',r['id'],flush=True)
    immutable=out/'immutable-m9'
    if a.immutable_replay:
        shutil.copytree(a.immutable_replay,immutable)
        v=read(immutable/'receipt.json');need(v['status']=='PASS'and set(v['ids'])==m9,'reused complete immutable M9 inventory')
        need(v['completion_receipt_sha256']==sha(immutable/'completion.json')and v['log_sha256']==sha(immutable/'replay.log'),'immutable replay bytes changed')
        for rel,h in v['current_inputs'].items():need(sha(BASE/rel)==h,'immutable current-input transport differs')
    else:
        from replay_immutable_m9 import replay
        v=replay(ROOT,immutable)
    need(set(v['ids'])==m9,'all frozen completions replayed')
    sys.path[:0]=[str(BASE),str(BASE/'software')];import verify as original
    original.verify_source(rows);original.verify_ledger(ledger)
    tree=ast.parse((BASE/'verify.py').read_text());body=next(n.body for n in tree.body if isinstance(n,ast.FunctionDef)and n.name=='main');i=next(i for i,n in enumerate(body)if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='m1'for t in n.targets));j=next(j for j,n in enumerate(body[i:],i)if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='stats'for t in n.targets));env=dict(vars(original),ledger=ledger);exec(compile(ast.Module(body=body[i:j],type_ignores=[]),'exact original rank6 post-loop checks','exec'),env)
    effective={r['id']:r['passed']for r in raw};effective.update({r['id']:True for r in retries});effective.update({rid:True for rid in m9});need(all(effective.values())and len(effective)==25362,'complete effective coverage')
    need(source_state()==sources and all(sha(HERE/f)==h for f,h in execution.items()),'source changed during corrected replay')
    with(out/'effective-case-coverage.jsonl').open('x')as stream:
        for r in raw:
            mode='immutable_exact_source_context'if r['id']in m9 else'complete_reference_backend_worker'if r['id']in{v['id']for v in retries}else'original_worker'
            stream.write(json.dumps({'id':r['id'],'certificate_sha256':hashlib.sha256(json.dumps(current[r['id']]['certificate'],sort_keys=True,separators=(',',':')).encode()).hexdigest(),'passed':True,'verification_route':mode,'record_kind':'DERIVED_EFFECTIVE_CASE_COVERAGE_NOT_ORIGINAL_RAW_RUNTIME'},separators=(',',':'))+'\n')
    receipt={'status':'PASS','mode':'COMPLETE_RAW_COMPOSITE_WITH_IMMUTABLE_SOURCE_CONTEXTS','scope':'All25362 current exclusion certificates; complete original raw stream, full reference-backend retries, all11 exact immutable M9 proofs and current tensor/certificate transport; exact original source-import, ledger and post-loop checks. Positive categorical constructions are separate.','original_raw_rows':len(raw),'original_worker_failures':sum(not r['passed']for r in raw),'complete_reference_backend_retries':len(retries),'retained_complete_reference_workers':reused_reference,'reference_source_manifest_sha256':sha(collection/'sources.json'),'reference_campaign_receipt_sha256':sha(a.reference_replays/'receipt.json')if a.reference_replays else None,'immutable_source_completions':11,'effective_exclusions':25362,'positive_registry_allocation':len(env['positive']),'all_source_states_fixed':True,'original_results_sha256':sha(out/'original-results.jsonl'),'immutable_replay_receipt_sha256':sha(immutable/'receipt.json'),'seconds':time.monotonic()-start}
    save(out/'receipt.json',receipt);print(json.dumps(receipt,indent=2))
if __name__=='__main__':main()
