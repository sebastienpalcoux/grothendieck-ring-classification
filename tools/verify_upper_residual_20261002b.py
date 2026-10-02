#!/usr/bin/env python3
"""Verify each new decision, immutable sources and exact historical preservation.

The old stages are replayed in an isolated temporary copy. No published ledger
or old receipt is mutated to make a historical check pass.
"""
from pathlib import Path
import collections,copy,hashlib,importlib.util,json,shutil,subprocess,sys,tempfile
ROOT=Path(__file__).resolve().parents[1]
E=ROOT/'evidence/upper_residual_20261002b'
MANIFEST_SHA256='b595f524ce8f19285e51bc2daf665393731553c1c95558217d094b8d28861315'
PREVIOUS_SHA256='8d7751d4fe14350002b1125cfe855395708a88f3ecfe2c87b551c38ff36aee82'
LEDGERS={7:'supplements/rank7/output/rank7_ledger.json',8:'supplements/rank8/data/decisions.json'}
SCRIPTS=['r7_integral/verify_general_families.py','r7_nonintegral/verify_nonintegral_results.py','r8_integral/verify_integral.py','r8_integral/r575/verify_r575.py','r8_nonintegral/verify_nonintegral.py','r8_nonintegral/verify_scoped.py','r8_integral/verify_d96_pair.py','r8_integral/r68/verify_r68.py','r8_nonintegral/verify_remaining_integrality.py']
def require(ok,msg):
 if not ok:raise ValueError(msg)
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def cd(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def td(v):return hashlib.sha256(json.dumps(v,separators=(',',':')).encode()).hexdigest()
def replay(path,root=ROOT):
 cmd=[sys.executable]+(['-O']if sys.flags.optimize else[])+[str(root/path)]
 result=subprocess.run(cmd,cwd=root,capture_output=True,text=True)
 require(result.returncode==0,path+' failed:\n'+result.stdout+result.stderr)
 report=json.loads(result.stdout);require(report.get('status')=='PASS',path+' did not PASS');return report

def verify_update():
 require(sha(E/'source_files.json')==MANIFEST_SHA256,'source manifest hash')
 sources=load(E/'source_files.json')
 for rel,expected in sources.items():
  p=(ROOT/rel).resolve();require(ROOT in p.parents and p.is_file(),'source path '+rel);require(sha(p)==expected,'source content '+rel)
 require(sha(E/'previous_records.json')==PREVIOUS_SHA256,'preservation manifest hash')
 previous=load(E/'previous_records.json');D=load(E/'decisions.json');approved={d['id']:d for d in D}
 require(len(approved)==len(D)==43,'decision inventory')
 require(collections.Counter(d['status']for d in D)=={'excluded':30,'unitarily_realized':13},'decision scopes/counts')
 ledgers={r:load(ROOT/p)for r,p in LEDGERS.items()};restored={}
 for rank,L in ledgers.items():
  meta=previous['ranks'][str(rank)];by={d['id']:d for d in L};changes={d['id']:d for d in D if d['rank']==rank};old={d['id']:d for d in meta['previous_records']}
  require(len(by)==len(L)==meta['records'],'ledger coverage')
  require(set(changes)==set(old)==set(meta['transitions']),'transition coverage')
  for rid,d in changes.items():
   x=by[rid];t=meta['transitions'][rid]
   require(old[rid]['status']==t['from']=='unresolved' and x['status']==t['to']==d['status'],'transition status '+rid)
   require(cd(x)==t['new_record_sha256'],'changed record contents '+rid)
   stable=('id','rank','multiplicity','source_line','commutative','tensor')if rank==7 else('id','multiplicity','index','tensor_sha256','commutative')
   require(all(old[rid][k]==x[k]for k in stable),'census identity '+rid)
   if x['status']=='excluded':require(d['scope']=='general_complex' and x['certificate']['scope']=='general_complex','scope promotion '+rid)
   else:
    model=next(z for z in load(ROOT/f'supplements/rank{rank}/data/model_catalog.json')if z['id']==rid)
    M=model['tensor']if rank==7 else model['constructors'][0]['tensor'];p=d['model_to_census'];T=d['census_tensor']
    require(p[0]==0 and sorted(p)==list(range(rank)),'basis '+rid)
    require(all(M[i][j][k]==T[p[i]][p[j]][p[k]]for i in range(rank)for j in range(rank)for k in range(rank)),'registry tensor '+rid)
  require(cd([x for x in L if x['id']not in changes])==meta['unchanged_records_sha256'],'unaffected records changed')
  H=[copy.deepcopy(old.get(x['id'],x))for x in L];require(cd(H)==meta['baseline_canonical_sha256'],'complete baseline digest')
  require(cd([x for x in H if x['status']=='excluded'])==meta['previous_negative_records_sha256'],'previous negatives')
  require(all(by[x['id']]==x for x in H if x['status']=='excluded'),'prior negative altered');restored[rank]=H
 remaining=load(E/'remaining_ids.json')
 for rank,L in ledgers.items():
  require(remaining[str(rank)]==[x['id']for x in L if x['status']=='unresolved'],'remaining frontier')
  require(len(load(ROOT/f'supplements/rank{rank}/data/model_catalog.json'))==sum(x['status']=='unitarily_realized'for x in L),'model coverage')
  baseline=load(E/f'baseline_files/supplements/rank{rank}/data/model_catalog.json');now=load(ROOT/f'supplements/rank{rank}/data/model_catalog.json');by={x['id']:x for x in now}
  require(all(by[x['id']]==x for x in baseline),'earlier model records changed')
 reports={p:replay('evidence/upper_residual_20261002b/'+p)for p in SCRIPTS}
 # All independent constructors compare every coefficient to the original census.
 new_models=set();new_exclusions=set()
 for p,rep in reports.items():
  positives=rep.get('unitary_models',rep.get('models',[]));negatives=rep.get('general_exclusions',rep.get('case_applications',rep.get('records',[])) if rep.get('scope')=='general_complex' else [])
  new_models.update(positives if isinstance(positives,dict)else(x['id']for x in positives))
  new_exclusions.update(negatives if isinstance(negatives,dict)else(x['id']for x in negatives))
  if 'unitary_modular_model'in rep:new_models.add(rep['unitary_modular_model']['id'])
  if p.endswith('r575/verify_r575.py'):new_models.add('R8_2_575')
  if rep.get('scope')=='general_complex' and rep.get('id')=='R8_2_68':new_exclusions.add(rep['id'])
 require(new_models=={d['id']for d in D if d['status']=='unitarily_realized'},'independent model replay coverage')
 require(new_exclusions=={d['id']for d in D if d['status']=='excluded'},'general premise replay coverage: '+repr(new_exclusions^{d['id']for d in D if d['status']=='excluded'}))
 with tempfile.TemporaryDirectory(prefix='upper-historical-')as directory:
  H=Path(directory)/'repo'
  shutil.copytree(ROOT,H,ignore=shutil.ignore_patterns('__pycache__','.git','*.pdf','*.zip','*.bin','restore_selection.json','restore_pending.json'))
  for path in (E/'baseline_files').rglob('*'):
   if path.is_file():q=H/path.relative_to(E/'baseline_files');q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(path,q)
  for rank,L in restored.items():(H/LEDGERS[rank]).write_text(json.dumps(L,indent=2,ensure_ascii=False)+'\n')
  recovery=replay('evidence/upper_residual_20261002b_recovery/verify_recovery.py',H)
  spec=importlib.util.spec_from_file_location('historical_residual',H/'tools/verify_residual_20261002.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
  historical_report,anyon_ledgers=m.verify_update()
  anyon_report=replay('tools/verify_anyonwiki_import.py',H)
 require(historical_report['status']=='PASS'and anyon_report['status']=='PASS','historical replay')
 report={'status':'PASS','python_optimized':bool(sys.flags.optimize),'changed_records':43,'new_general_exclusions':30,'new_unitary_models':13,'previous_negative_records_unchanged':True,'unaffected_records_unchanged':True,'complete_historical_ledgers_restored':True,'pinned_source_files':len(sources),'source_manifest_sha256':MANIFEST_SHA256,'preservation_manifest_sha256':PREVIOUS_SHA256,'historical_oct2_replay':historical_report['status'],'historical_anyonwiki_replay':anyon_report['status'],'recovery_replay':recovery['status'],'independent_model_replays':sorted(new_models),'general_premise_replays':sorted(new_exclusions),'status_totals':{str(r):dict(collections.Counter(x['status']for x in L))for r,L in ledgers.items()},'remaining_general_cases':{str(r):len(remaining[str(r)])for r in ledgers},'scope':'Only general exclusions change negative decisions. Pivotal, pseudo-unitary, unitary and braided obstructions retain their stated scopes.'}
 return report,anyon_ledgers

def main():
 report,_=verify_update();print(json.dumps(report,indent=2));return report
if __name__=='__main__':main()
