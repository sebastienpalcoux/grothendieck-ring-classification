#!/usr/bin/env python3
"""Replay the new exact model-identification proofs in isolated output copies.

These checks identify actual constructions using the categorical premises
stated in the revised manuscripts. They do not reconstruct all literature
associators or replay the entire classification.
"""
from pathlib import Path
import argparse,ast,hashlib,json,os,shutil,subprocess,sys,tempfile,time
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
SCRIPTS=['rank8-ng-partial-fusion.py','rank8-neargroup-associativity-classify.py',
         'rank8_neargroup_seed_indicator.py','rank8-neargroup-twist-distinction.py',
         'rank6_r143_module_repair.py','r721_exact_completion.py','verify_r189_pieri_branching.py']

def need(c,m):
    if not c:raise RuntimeError(m)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def semantic(value):
    if isinstance(value,dict):return {k:semantic(v)for k,v in value.items()if k not in ('seconds','elapsed_seconds','optimized_python','optimized')}
    if isinstance(value,list):return [semantic(v)for v in value]
    return value

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output-dir',type=Path,required=True);a=p.parse_args()
    a.output_dir.mkdir(parents=True,exist_ok=False);out=a.output_dir.resolve();records=[];start=time.monotonic()
    sources={name:sha(HERE/name) for name in SCRIPTS+['r721_completion_controls.py']}
    env=dict(os.environ,FUSION_CLASSIFICATION_REPO=str(ROOT),OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1')
    with tempfile.TemporaryDirectory(prefix='exact-model-repair-')as td:
        work=Path(td)
        for name in sources:shutil.copy2(HERE/name,work/name)
        for name in SCRIPTS:
            need(not any(isinstance(n,ast.Assert)for n in ast.walk(ast.parse((HERE/name).read_text()))),'optimization-sensitive proof guard: '+name)
            receipts=[]
            for optimized in (False,True):
                prefix=Path(name).stem+('-optimized'if optimized else'-normal');log=out/(prefix+'.log')
                before=set(work.glob('*.json'))
                with log.open('x')as stream:run=subprocess.run([sys.executable]+(['-O']if optimized else[])+[str(work/name)],env=env,cwd=ROOT,stdout=stream,stderr=subprocess.STDOUT)
                need(run.returncode==0,'proof replay failed: '+name+'; see '+str(log))
                generated=(work/('r721-exact-completion-optimized.json'if optimized else'r721-exact-completion.json'))if name=='r721_exact_completion.py'else work/Path(name).with_suffix('.json')
                if name=='verify_r189_pieri_branching.py':generated=work/'r189_pieri_branching_receipt.json'
                need(generated.is_file(),'proof receipt missing: '+name)
                target=out/(prefix+'.json');shutil.copy2(generated,target);receipts.append(json.loads(target.read_text()))
                records.append({'script':name,'optimized_python':optimized,'status':'PASS','receipt':target.name,'receipt_sha256':sha(target),'log':log.name,'log_sha256':sha(log)})
                print('PASS',prefix,flush=True)
            need(semantic(receipts[0])==semantic(receipts[1]),'normal/optimized mathematical receipts disagree: '+name)
        log=out/'r721-controls.log'
        with log.open('x')as stream:run=subprocess.run([sys.executable,'-O',str(work/'r721_completion_controls.py')],env=env,cwd=ROOT,stdout=stream,stderr=subprocess.STDOUT)
        need(run.returncode==0,'independent small completion controls failed');shutil.copy2(work/'r721-completion-controls.json',out/'r721-completion-controls.json')
        records.append({'script':'r721_completion_controls.py','optimized_python':True,'status':'PASS','receipt':'r721-completion-controls.json','receipt_sha256':sha(out/'r721-completion-controls.json'),'log':log.name,'log_sha256':sha(log)})
    for optimized in (False,True):
        prefix='ng-full-transport-'+('optimized'if optimized else'normal');log=out/(prefix+'.log');receipt=out/(prefix+'.json')
        with log.open('x')as stream:run=subprocess.run([sys.executable]+(['-O']if optimized else[])+[str(ROOT/'evidence/unified_20261016/rank8/verify_neargroup_centralizer.py'),'--repo',str(ROOT),'--output',str(receipt)],env=env,cwd=ROOT,stdout=stream,stderr=subprocess.STDOUT)
        need(run.returncode==0 and json.loads(receipt.read_text())['status']=='PASS','full NG tensor transport failed')
        records.append({'script':'existing exact candidate-to-census transport','optimized_python':optimized,'status':'PASS','receipt':receipt.name,'receipt_sha256':sha(receipt),'log':log.name,'log_sha256':sha(log),'scope':'Exact ring transport only; categorical identification uses the new proof.'})
    need(all(sha(HERE/name)==h for name,h in sources.items()),'proof sources changed during replay')
    result={'status':'PASS','scope':'Three repaired model proofs and direct R721 completion; explicit external categorical premises retained.','source_sha256':sources,'normal_and_optimized_semantics_agree':True,'runs':records,'seconds':time.monotonic()-start}
    (out/'receipt.json').write_text(json.dumps(result,indent=2)+'\n');print('COMPLETE',len(records),'PASS',flush=True)
if __name__=='__main__':main()
