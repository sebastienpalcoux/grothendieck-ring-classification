#!/usr/bin/env python3
"""Replay accepted rank-nine M2 dependencies across all five historical phases.

Every stage uses a fresh copy of the unchanged source archive; two separately
bound omitted certificates are restored. Unlike the old root dispatcher this
runs the baseline and phases2--5. Stored GAP/cohomology narrowing records are
verified, not regenerated; the dated full audit contains the fresh searches.
The exact R920 completeness fallback shares the pseudo-Boolean discovery
implementation and is explicitly not an independent eight-bit replay.
"""
from pathlib import Path
import argparse,collections,hashlib,importlib.util,itertools,json,os,shutil,subprocess,sys,tempfile,time,zipfile
from concurrent.futures import ProcessPoolExecutor
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
ARCHIVE_SHA='38b4339c86c71fdba65cc7a72df57b16248b508f11dbe8fdb2016c43d77e6ff2'
LEDGER_SHA='0f8c9b45f328d084735eb2c514308a87bbf176c7fb0a7fcd99578f18d0d0097e'
SUPPLEMENT_SHA={'cert2.jsonl': 'a7051f82fde94a5e37f9c3813ac0262c92cc2e4b1567ed9afeb8aed41afd30a6', 'cert3.jsonl': '32536ad8dd7a2fc162a55401f4ae420a29fc073ed96565ce7d6cbd1aec238944'}
STAGES=['baseline','phase2','phase3','phase4','phase5']
for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[k]='1'
def need(c,m):
    if not c:raise RuntimeError(m)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return json.loads(Path(p).read_text())
def save(p,v):Path(p).write_text(json.dumps(v,indent=2)+'\n')
def load(name,path):
    s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);sys.modules[name]=m;s.loader.exec_module(m);return m
def baseline_init(context,corpus):
    global V
    sys.path[:0]=[str(context/'work'),str(context/'sources')]
    import verify_results as V
    V.CORPUS=read(corpus)
def baseline_check(rid):return V.check(rid)
def baseline(context,out,jobs):
    sys.path[:0]=[str(context/'work'),str(context/'sources')]
    import verify_results as v
    ledger=read(context/'phase5/results/ledger.json');corpus=read(context/'work/verification_corpus.json');ids=[];cache={}
    for r in ledger:
        if r['status']!='excluded' or not r['exclusion_certificates'][0]['record_file'].startswith('work/'):continue
        rid=r['id'];c=r['exclusion_certificates'][0];name=c['record_file'];ids.append(rid)
        if name not in cache:cache[name]={x['id']:x for x in read(context/name)}
        pr=cache[name][rid]
        if Path(name).stem in ('baseline','structural'):
            pr=dict(pr);pr['certificates']=[x for x in pr['certificates']if x['kind']==c['certificate_kind']]+[x for x in pr['certificates']if x['kind']!=c['certificate_kind']]
        corpus['ledger'][rid]=r;corpus['proofs'][rid]=pr
    need(len(ids)==1817,'current baseline first-route coverage');cp=out/'baseline-corpus.json';save(cp,corpus)
    with ProcessPoolExecutor(max_workers=jobs,initializer=baseline_init,initargs=(context,cp))as pool:results=list(pool.map(baseline_check,ids,chunksize=1))
    need([x['id']for x in results]==ids and all(x['status']=='PASS'for x in results),'baseline accepted exclusion failed');save(out/'baseline-cases.json',results)
    # Regenerate the seven actual baseline model tensors before transport.
    import standard_model_scan as standard,more_standard_models as more,near_group_models as near
    import group_theoretical as gt
    from extra_models import dicyclic_table
    from common import based_iso
    made={'R9_2_369':more.pgl27(),'R9_2_936':standard.psl2even(8),'R9_2_1374':standard.d16(),'R9_2_1979':near.extend(dicyclic_table(2))}
    perms,G=gt.permutation_group(4);H=gt.subgroup(G,[perms.index(g)for g in[(1,0,2,3),(0,1,3,2)]]);made['R9_2_1016']=gt.fusion(G,H)
    els,G=more.gl3f2();H=[i for i,a in enumerate(els)if(a[0],a[3],a[6])==(1,0,0)];made['R9_2_1557']=gt.fusion(G,H)
    made['R9_2_2083']=more.cyclic_equivariant(more.group((19,)),[(7*a)%19 for a in range(19)],3)[0]
    models=[]
    for rid,T in made.items():
        R=corpus['tensors'][rid];p=based_iso(R,T);need(p is not None and p[0]==0 and all(R[i][j][k]==T[p[i]][p[j]][p[k]]for i,j,k in itertools.product(range(9),repeat=3)),'baseline full model tensor: '+rid)
        models.append({'id':rid,'status':'PASS','coefficients':729,'source_to_model_map':p})
    save(out/'baseline-models.json',models);return {'status':'PASS','accepted_exclusions':1817,'models_regenerated':7}
def phase2_gates(context):
    sys.path[:0]=[str(context/'phase2/signed'),str(context/'work'),str(context/'sources')]
    import verify_nonzero_products as v
    from galois_pu_gate import GATE_TARGETS
    from signed_pb import FiniteProblem
    rows={r['id']:r['tensor']for r in v.read()};records=[];original=v.problem
    for index in GATE_TARGETS:
        rid=f'R9_2_{index}';report=read(context/f'phase2/signed/gate_{rid}.json')
        if index==920:
            def pb_problem(R):
                p=FiniteProblem(R,timeout=300000)
                variables=[v.z3.Sum(*[v.z3.If(c,x,0)for x,c in states.items()])for states in p.states]
                return p.s,variables,p.active,p.mapping,p.bounds,p.gauge,len(p.eqs)
            v.problem=pb_problem
        try:result=v.check(rows[rid],report,timeout=300000)
        finally:v.problem=original
        result['finite_completeness_backend']='exact pseudo-Boolean, shares discovery implementation'if index==920 else'independent eight-bit integer-equivalent encoding'
        records.append(result);print('PASS',rid,result['finite_completeness_backend'],flush=True)
    # The old controller expects this legacy key; the explicit backend field
    # qualifies it. The final current receipt removes the ambiguous R920 key.
    save(context/'phase2/signed/gate_verification.json',records)
    return records

def stage(context,out,name,jobs,frontier):
    need(__debug__,'historical assertion-based dependencies must run normal Python')
    def run(path,*args):
        print('RUN',path,*args,flush=True);subprocess.run([sys.executable,str(context/path),*args],cwd=context,check=True)
    if name=='baseline':return baseline(context,out,jobs)
    if name=='phase2':
        sys.path.insert(0,str(context/'phase2'));controller=load('rank9_phase2_controller',context/'phase2/verify_continuation.py');old=controller.run
        def dispatch(path,*args):
            if path=='phase2/signed/verify_nonzero_products.py'and list(args)==['--gates']:phase2_gates(context)
            else:old(path,*args)
        controller.run=dispatch;controller.main(True)
        for path in ['phase2/integral_theory/verify_prime_descent.py','phase2/weak_integral/frobenius52.py','phase2/replay_constructors.py']:run(path)
        records=read(context/'phase2/signed/gate_verification.json')
        for r in records:
            if r['id']=='R9_2_920':r['completeness_result']=r.pop('independent_completeness');r['independent_implementation']=False
        save(out/'phase2-gate-replays.json',records)
        return {'status':'PASS','fresh_criteria_and_constructors':True,'R920_backend':'exact pseudo-Boolean, shares discovery implementation; no independent-eight-bit success claimed'}
    if name=='phase3':run('phase3/verify_audit.py','--fresh');return read(context/'phase3/verification.json')
    if name=='phase4':run('phase4/verify.py');return read(context/'phase4/verification.json')
    if name=='phase5':
        run('phase5/verify.py',*(['--frontier']if frontier else[]));return read(context/'phase5/verification.json')
    raise RuntimeError(name)

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--archive',type=Path);p.add_argument('--output-dir',type=Path);p.add_argument('--jobs',type=int,default=2);p.add_argument('--frontier',action='store_true');p.add_argument('--plan',action='store_true');p.add_argument('--stage',choices=STAGES,help=argparse.SUPPRESS);p.add_argument('--context',type=Path,help=argparse.SUPPRESS);a=p.parse_args()
    if a.stage:
        value=stage(a.context.resolve(),a.output_dir.resolve(),a.stage,a.jobs,a.frontier);save(a.output_dir/(a.stage+'-receipt.json'),value);return
    if a.plan:
        print(json.dumps({'stages':STAGES,'baseline_accepted_exclusions':1817,'model_reconstruction_all_stages':True,'restored_missing_certificates':['cert2.jsonl','cert3.jsonl'],'R920_backend':'exact pseudo-Boolean; shared discovery implementation','group_searches':'Stored exact narrowing records verified, full fresh searches retained in the dated audit archive.','frontier_optional':True},indent=2));return
    need(a.output_dir is not None and a.jobs>0,'supply a new --output-dir and positive --jobs')
    archive=a.archive or(ROOT/'evidence/rank9_m2_20261024/replay.zip'if(ROOT/'evidence/rank9_m2_20261024/replay.zip').is_file()else HERE/'rank9-prior-replay.zip')
    need(sha(archive)==ARCHIVE_SHA,'historical source archive identity')
    a.output_dir.mkdir(parents=True,exist_ok=False);out=a.output_dir.resolve();records=[];start=time.monotonic()
    for name in STAGES:
        with tempfile.TemporaryDirectory(prefix='rank9-'+name+'-')as tmp:
            target=Path(tmp)
            with zipfile.ZipFile(archive)as z:
                for item in z.infolist():need((target/item.filename).resolve().is_relative_to(target),'unsafe archive path')
                z.extractall(target)
            context=target/'Rank9_M2_Theoretical_Continuation_20261023'
            for rel,h in read(context/'SHA256SUMS.json').items():need(sha(context/rel)==h,'historical packaged source: '+rel)
            need(sha(context/'phase5/results/ledger.json')==LEDGER_SHA,'current accepted ledger')
            if name=='phase3':
                for cert in ('cert2.jsonl','cert3.jsonl'):
                    source=HERE/'rank9_phase3'/cert
                    need(sha(source)==SUPPLEMENT_SHA[cert],'restored certificate identity: '+cert)
                    destination=context/'phase3/audit_small_subrings'/cert
                    need(not destination.exists(),'certificate unexpectedly already present')
                    destination.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,destination)
            log=out/(name+'.log');command=[sys.executable,str(Path(__file__).resolve()),'--stage',name,'--context',str(context),'--output-dir',str(out),'--jobs',str(a.jobs)]+(['--frontier']if a.frontier else[])
            with log.open('x')as stream:run=subprocess.run(command,cwd=context,stdout=stream,stderr=subprocess.STDOUT)
            need(run.returncode==0,'rank-nine stage failed: '+name+'; see '+str(log))
            receipt=out/(name+'-receipt.json');need(read(receipt)['status']=='PASS','stage did not produce a successful receipt')
            records.append({'stage':name,'status':'PASS','log':log.name,'log_sha256':sha(log),'receipt':receipt.name,'receipt_sha256':sha(receipt)});print('PASS stage',name,flush=True)
    result={'status':'PASS','scope':'Accepted baseline and all phases2--5; all36 model constructors/transports. Stored GAP/cohomology narrowing records verified, not regenerated in this command; external categorical premises remain explicit.','partition':{'excluded':2043,'unitarily_realized':36,'unresolved':4},'archive_sha256':ARCHIVE_SHA,'ledger_sha256':LEDGER_SHA,'stages':records,'R920_backend':'exact pseudo-Boolean shared implementation, not independent eight-bit replay','seconds':time.monotonic()-start};save(out/'receipt.json',result);print(json.dumps(result,indent=2))
if __name__=='__main__':main()
