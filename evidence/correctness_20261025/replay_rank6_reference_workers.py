#!/usr/bin/env python3
"""Run complete failed rank-six reference workers in separate processes.

Optional retained outputs must come from the same source-bound collection.
No mathematical condition is removed and no unknown outcome is accepted.
"""
from pathlib import Path
import argparse,hashlib,json,os,shutil,subprocess,sys,time
from concurrent.futures import ThreadPoolExecutor,as_completed
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def need(c,m):
    if not c:raise RuntimeError(m)
def read(p):return json.loads(Path(p).read_text())
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--collection',type=Path,required=True);p.add_argument('--output-dir',type=Path,required=True);p.add_argument('--jobs',type=int,default=2);p.add_argument('--retain',nargs='*',default=[]);a=p.parse_args();need(a.jobs>0,'positive workers required')
    from replay_rank6 import source_state
    sources=source_state();old={k:v for k,v in read(a.collection/'sources.json').items()if not k.endswith('.build.json')};need(old==sources,'retained source context differs')
    raw=[json.loads(x)for x in(a.collection/'original-results.jsonl').read_text().splitlines()];need(len(raw)==25362,'complete raw collection required')
    failures=[r for r in raw if not r['passed']and not r['kind'].startswith('m9_completion_')];need(len(failures)==7 and set(a.retain)<={r['id']for r in failures},'exact reference-worker inventory')
    a.output_dir.mkdir(parents=True,exist_ok=False);out=a.output_dir.resolve();start=time.monotonic();execution={n:sha(HERE/n)for n in('replay_rank6_reference_workers.py','collect_rank6_workers.py')}
    def run(r):
        rid=r['id'];target=out/(rid+'-python.json');log=out/(rid+'-python.log')
        with log.open('x')as s:v=subprocess.run([sys.executable,str(HERE/'collect_rank6_workers.py'),'--one',rid,'--output-dir',str(target)],cwd=ROOT,env=dict(os.environ,SYMPY_GROUND_TYPES='python',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1'),stdout=s,stderr=subprocess.STDOUT)
        value=read(target);need(v.returncode==0 and value['id']==rid and value['kind']==r['kind']and value['passed'],'complete reference worker failed: '+rid);return rid
    with ThreadPoolExecutor(max_workers=a.jobs)as pool:
        for f in as_completed([pool.submit(run,r)for r in failures if r['id']not in a.retain]):print('PASS full reference worker',f.result(),flush=True)
    for rid in a.retain:
        target=a.collection/(rid+'-python.json');value=read(target);r=next(r for r in failures if r['id']==rid);need(value['id']==rid and value['kind']==r['kind']and value['passed'],'retained full worker incomplete: '+rid)
        for suffix in('-python.json','-python.log'):shutil.copy2(a.collection/(rid+suffix),out/(rid+suffix))
        print('PASS retained full reference worker',rid,flush=True)
    need(source_state()==sources and all(sha(HERE/n)==h for n,h in execution.items()),'reference source changed during replay')
    receipt={'status':'PASS','scope':'All seven complete unchanged failed workers under the Python reference backend; retained workers are identified separately.','source_context':sources,'execution_sources':execution,'raw_collection_sha256':sha(a.collection/'original-results.jsonl'),'retained_worker_ids':a.retain,'files':{p.name:sha(p)for p in sorted(out.iterdir())if p.is_file()},'seconds':time.monotonic()-start}
    (out/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps({'status':'PASS','reference_workers':7,'seconds':receipt['seconds']}))
if __name__=='__main__':main()
