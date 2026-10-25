#!/usr/bin/env python3
"""Replay the eleven immutable M9 proofs in their exact original source context.

This preserves every frozen manifest and matches each current tensor and
certificate. Corrected reusable kernels remain in the current checkout; old
bounded proof programs run only on their eleven originally certified inputs.
"""
from pathlib import Path
import argparse,hashlib,json,os,shutil,subprocess,sys,tarfile,tempfile,time
BASE_COMMIT='8014c749c17ddd2ad3d1b99a4359d49a8be921c5'
def need(c,m):
    if not c:raise RuntimeError(m)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return json.loads(Path(p).read_text())
def replay(repo,out):
    repo=Path(repo).resolve();out=Path(out).resolve();out.mkdir(parents=True,exist_ok=False);start=time.monotonic()
    need(shutil.which('git')is not None,'Git and the pinned source commit are required')
    with tempfile.TemporaryDirectory(prefix='immutable-m9-source-')as td:
        context=Path(td);proc=subprocess.Popen(['git','-C',str(repo),'archive',BASE_COMMIT,'supplements/rank6'],stdout=subprocess.PIPE)
        with tarfile.open(fileobj=proc.stdout,mode='r|')as t:t.extractall(context,filter='data')
        need(proc.wait()==0,'cannot export the immutable rank-six source context')
        root=context/'supplements/rank6'
        for item in read(repo/'data/large_files_manifest.json')['files']:
            rel=item['path']
            if not rel.startswith('supplements/rank6/'):continue
            source=repo/rel
            if source.is_file() and not(context/rel).is_file():
                target=context/rel;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,target)
        # Bound copies of the canonical input and the unchanged eleven certs.
        for rel in ('data/census.json','data/decisions.json','certificates/m9_completion.jsonl'):
            need((root/rel).is_file()and sha(root/rel)==sha(repo/'supplements/rank6'/rel),'current/historical input differs: '+rel)
        log=out/'replay.log';receipt=out/'completion.json'
        env=dict(os.environ,SYMPY_GROUND_TYPES='python',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1')
        with log.open('x')as stream:run=subprocess.run([sys.executable,str(root/'software/replay_m9_completion.py'),'--output',str(receipt)],cwd=root,env=env,stdout=stream,stderr=subprocess.STDOUT)
        need(run.returncode==0,'immutable M9 replay failed; see '+str(log))
        result=read(receipt);need(result.get('passed')is True and result.get('complete')is True and result.get('count')==11,'incomplete M9 replay')
        files=read(root/'verification/m9/completion/proof_manifest.json');current={r['id']:r for r in read(repo/'supplements/rank6/data/decisions.json')}
        records=[json.loads(line)for line in(root/'certificates/m9_completion.jsonl').read_text().splitlines()if line.strip()]
        need(len(records)==11 and all(current[r['id']]['certificate']==r['certificate']for r in records),'current certificates differ from immutable replay')
        bound={'status':'PASS','source_context_commit':BASE_COMMIT,'scope':'All eleven frozen M9 completion certificates and unchanged current tensor/certificate transport; historical source manifests remain exact.','count':11,'ids':[r['id']for r in records],'current_inputs':{rel:sha(repo/'supplements/rank6'/rel)for rel in('data/census.json','data/decisions.json','certificates/m9_completion.jsonl')},'proof_manifest_sha256':sha(root/'verification/m9/completion/proof_manifest.json'),'completion_receipt_sha256':sha(receipt),'log_sha256':sha(log),'seconds':time.monotonic()-start}
        (out/'receipt.json').write_text(json.dumps(bound,indent=2)+'\n');print(json.dumps(bound,indent=2));return bound
if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--repo',type=Path,default=Path(__file__).resolve().parents[2]);ap.add_argument('--output-dir',type=Path,required=True);a=ap.parse_args();replay(a.repo,a.output_dir)
