"""Offline final-resolution verifier. Python 3 and SymPy; optional --baseline.

Categorical proofs are in report.pdf and the cited notes. This program checks
the ledger, source bindings, and exact arithmetic; it does not replace them.
"""
from pathlib import Path
import collections, csv, hashlib, itertools, json, os, shutil, subprocess, sys, tempfile, time

ROOT=Path(__file__).resolve().parent
LOG=ROOT/'verification'
MODE='normal' if __debug__ else 'optimized'

def need(ok,message):
    if not ok:raise RuntimeError(message)

def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def digest(t):return hashlib.sha256(json.dumps(t,separators=(',',':')).encode()).hexdigest()

def main():
    start=time.monotonic()
    LOG.mkdir(exist_ok=True)
    summary=read(ROOT/'summary.json')
    ledger=read(ROOT/'ledger.json')
    old={r['id']:r for r in read(ROOT/'baseline/ledger.json')['records']}
    by={r['id']:r for r in ledger['records']}
    all_tensors=read(ROOT/'baseline/prior_round/prior_round/evidence/rank12-m1-offline-20261025/tensors.json')
    resolved=read(ROOT/'resolved_tensors.json')
    decisions=read(ROOT/'new_decisions.json')
    need(ledger['summary']==summary,'summary binding')
    need((summary['total'],summary['excluded'],summary['modeled'],summary['unresolved'])==(632,480,152,0),'counts')
    need(not summary['online_revision_performed'],'offline scope')
    need(len(ledger['records'])==len(by)==632 and set(by)==set(old)==set(all_tensors),'complete input coverage')
    expected={'R12_1_561':'excluded','R12_1_623':'pseudo_unitarily_realized','R12_1_628':'excluded'}
    need(set(resolved)==set(expected),'resolved input list')
    need(set(decisions['exclusions'])=={'R12_1_561','R12_1_628'},'exclusion list')
    need(set(decisions['models'])=={'R12_1_623'},'model list')
    for rid,row in by.items():
        need(row['tensor_sha256']==digest(all_tensors[rid]),'physical tensor '+rid)
        if rid not in expected:
            need(row==old[rid],'unchanged settled record '+rid)
        else:
            need(old[rid]['status']=='unresolved' and row['status']==expected[rid],'new decision '+rid)
            need(resolved[rid]==all_tensors[rid],'resolved tensor '+rid)
    need(collections.Counter(r['status'] for r in by.values())=={'excluded':480,'unitarily_realized':151,'pseudo_unitarily_realized':1},'status counts')
    need(by['R12_1_623']['unitary_realization']=='not established','unitarity scope')
    for rid,row in decisions['exclusions'].items():
        need(row['scope']=='general_complex_fusion_category','general complex exclusion scope')
        for key in ['proof','central_lift_proof','replay','independent_audit']:
            need((ROOT/row[key]).is_file(),'evidence link '+row[key])
    model=decisions['models']['R12_1_623']
    need(model['unitary_realization']=='not established','model scope')
    for key in ['proof','replay','independent_audit','independent_replay']:
        need((ROOT/model[key]).is_file(),'model evidence '+model[key])
    p=model['basis_map']; M=model['model_tensor']; T=resolved['R12_1_623']
    need(model['basis_map_direction']=='model_to_census' and p[0]==0 and sorted(p)==list(range(12)),'basis map')
    need(all(M[i][j][k]==T[p[i]][p[j]][p[k]] for i,j,k in itertools.product(range(12),repeat=3)),'all 1728 model entries')
    frozen=read(ROOT/'round5/models/R623_model_frozen.json')
    need(frozen['fusion_tensor']==T and frozen['coordinate_to_input']==p,'model frozen binding')
    need(read(ROOT/'round5/premises/R623_tensor.json')==T,'independent frozen binding')
    exclusion_inputs=read(ROOT/'round5/c3_structure/inputs.json')
    central_inputs=read(ROOT/'baseline/round4/c6/audit/frozen_inputs.json')
    for rid in decisions['exclusions']:
        need(exclusion_inputs[rid]['tensor']==resolved[rid]==central_inputs['tensors'][rid],'exclusion frozen binding '+rid)
    with (ROOT/'ledger.csv').open(newline='') as f:
        rows=list(csv.DictReader(f))
    need(len(rows)==632 and {r['id'] for r in rows}==set(by),'CSV coverage')
    need(all(r['status']==by[r['id']]['status'] and r['tensor_sha256']==by[r['id']]['tensor_sha256'] for r in rows),'CSV consistency')
    snapshot=read(ROOT/'baseline_snapshot_manifest.json')
    need(set(snapshot)=={str(p.relative_to(ROOT/'baseline')) for p in (ROOT/'baseline').rglob('*') if p.is_file()},'baseline file coverage')
    for rel,h in snapshot.items():
        need(sha(ROOT/'baseline'/rel)==h,'unchanged baseline '+rel)
    if (ROOT/'MANIFEST.sha256').exists():
        for line in (ROOT/'MANIFEST.sha256').read_text().splitlines():
            h,rel=line.split('  ',1)
            need(sha(ROOT/rel)==h,'package hash '+rel)
    print('PASS all 632 inputs, exact three-decision delta, 629 unchanged records, full frozen baseline',flush=True)
    steps=[
        'baseline/round4/c6/verify_C3_sections.py',
        'round5/c3_structure/verify_saturation.py',
        'round5/center/verify_dimension_block_arithmetic.py',
        'round5/models/verify_R623_model.py',
        'round5/premises/verify_R623_condensation.py',
    ]
    checks=[]
    with tempfile.TemporaryDirectory(prefix='rank12-completion-') as tmp:
        shadow=Path(tmp)
        shutil.copytree(ROOT/'round5',shadow/'round5')
        if '--baseline' in sys.argv:
            shutil.copytree(ROOT/'baseline',shadow/'baseline')
            steps.append('baseline/verify.py')
        else:
            shutil.copytree(ROOT/'baseline/round4/c6',shadow/'baseline/round4/c6')
        env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',OPENBLAS_NUM_THREADS='1')
        env.pop('PYTHONPATH',None)
        for i,rel in enumerate(steps,1):
            script=shadow/rel
            tick=time.monotonic()
            run=subprocess.run([sys.executable,*([] if __debug__ else ['-O']),str(script)],cwd=script.parent,capture_output=True,text=True,env=env)
            (LOG/f'{MODE}_{i:02d}.log').write_text(run.stdout+run.stderr)
            if run.returncode:
                print((run.stdout+run.stderr)[-6000:])
                raise RuntimeError('Replay failed: '+rel)
            checks.append(dict(script=rel,status='PASS',seconds=time.monotonic()-tick))
            print(f'{i}/{len(steps)} PASS {rel}',flush=True)
    receipt=dict(status='PASS',excluded=480,modeled=152,unresolved=0,unitary_models=151,
        additional_pseudo_unitary_models=1,new_exclusions=2,new_models=1,
        unchanged_previously_settled_records=629,optimized_python=not __debug__,
        baseline_replayed='--baseline' in sys.argv,steps=checks,seconds=time.monotonic()-start)
    (LOG/f'{MODE}.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({k:v for k,v in receipt.items() if k!='steps'},indent=2))

if __name__=='__main__':main()
