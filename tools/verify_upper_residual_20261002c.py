#!/usr/bin/env python3
"""Replay the new general exclusions and the exact published parent stage.

Historical sources are restored only in an isolated temporary copy.
"""
from pathlib import Path
import collections,copy,hashlib,importlib.util,json,shutil,subprocess,sys,tempfile
ROOT=Path(__file__).resolve().parents[1]
E=ROOT/'evidence/upper_residual_20261002c'
MANIFEST_SHA256='409c58594d1d004678becac5459df375c5a99c9d4e18c5ba99f0bb7881c7db04'
IDS={'R7_2_160','R7_4_1417','R7_4_1420','R8_2_312','R8_2_315','R8_2_317','R8_2_53','R8_2_93','R8_2_191','R8_2_299','R8_2_158','R8_2_186','R8_2_579','R8_2_682'}
LEDGERS={7:'supplements/rank7/output/rank7_ledger.json',8:'supplements/rank8/data/decisions.json'}
SCRIPTS=['r7_relative_trace/verify_relative_trace.py','r7_relative_trace/verify_relative_trace_independent.py','r8_associators/verify_r312.py','r8_associators/verify_psu_pointed.py','r8_extension_integrality/verify_r53_r93.py','r8_extension_integrality/verify_r191_r299.py','r8_extension_integrality/verify_r53_r93_independent.py','r7_central_boson/verify_r160.py','r8_extension_integrality/verify_dim48_four.py','r8_extension_integrality/verify_group_kernels.py']
def require(x,msg):
 if not x:raise ValueError(msg)
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def cd(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def replay(path,root=ROOT):
 cmd=[sys.executable]+(['-O']if sys.flags.optimize else[])+[str(root/path)]
 r=subprocess.run(cmd,cwd=root,capture_output=True,text=True)
 require(r.returncode==0,path+' failed:\n'+r.stdout+r.stderr)
 out=json.loads(r.stdout);require(out.get('status')=='PASS',path+' not PASS');return out

def verify_update():
 require(sha(E/'source_files.json')==MANIFEST_SHA256,'source manifest hash')
 sources=load(E/'source_files.json')
 for rel,h in sources.items():
  p=(ROOT/rel).resolve();require(ROOT in p.parents and p.is_file(),'missing source '+rel);require(sha(p)==h,'changed source '+rel)
 D=load(E/'decisions.json');require(len(D)==len(IDS) and {d['id']for d in D}==IDS,'decision inventory')
 require(all(d['status']=='excluded' and d['scope']=='general_complex'for d in D),'decision scope')
 previous=load(E/'previous_records.json');ledgers={r:load(ROOT/p)for r,p in LEDGERS.items()};restored={}
 for r,L in ledgers.items():
  meta=previous['ranks'][str(r)];by={x['id']:x for x in L};changes={x['id']:x for x in D if x['rank']==r};old={x['id']:x for x in meta['previous_records']}
  require(len(by)==len(L)==meta['records'],'ledger coverage')
  require(set(changes)==set(old)==set(meta['transitions']),'transition coverage')
  for rid,d in changes.items():
   x=by[rid];t=meta['transitions'][rid]
   require(old[rid]['status']==t['from']=='unresolved' and x['status']==t['to']=='excluded','transition '+rid)
   require(cd(x)==t['new_record_sha256'],'record contents '+rid)
   stable=('id','rank','multiplicity','source_line','commutative','tensor')if r==7 else('id','multiplicity','index','tensor_sha256','commutative')
   require(all(x[k]==old[rid][k]for k in stable),'census identity '+rid)
   require(x['certificate']['scope']=='general_complex' and x['certificate']['proof']=='evidence/upper_residual_20261002c/'+d['proof'],'certificate '+rid)
  require(cd([x for x in L if x['id']not in changes])==meta['unchanged_records_sha256'],'unaffected records')
  H=[copy.deepcopy(old.get(x['id'],x))for x in L]
  require(cd(H)==meta['baseline_canonical_sha256'],'complete parent ledger')
  require(cd([x for x in H if x['status']=='excluded'])==meta['previous_negative_records_sha256'],'previous negatives')
  require(all(by[x['id']]==x for x in H if x['status']=='excluded'),'prior negative modified')
  require(H==load(E/'baseline_files'/LEDGERS[r]),'baseline bytes/records mismatch');restored[r]=H
 remaining=load(E/'remaining_ids.json')
 require(all(remaining[str(r)]==[x['id']for x in L if x['status']=='unresolved']for r,L in ledgers.items()),'remaining frontier')
 reports={p:replay('evidence/upper_residual_20261002c/'+p)for p in SCRIPTS}
 r7=reports[SCRIPTS[0]];r7i=reports[SCRIPTS[1]];r312=reports[SCRIPTS[2]];rpsu=reports[SCRIPTS[3]]
 require({x['id']for x in r7['cases']}=={'R7_4_1417','R7_4_1420'} and {x['id']for x in r7i['cases']}=={'R7_4_1417','R7_4_1420'},'rank7 replay coverage')
 require(r312.get('id')=='R8_2_312' or any(x.get('id')=='R8_2_312'for x in r312.get('cases',[])),'R312 replay coverage')
 require({x['id']for x in rpsu['source_witnesses']}=={'R8_2_315','R8_2_317'},'pointed incompatibility coverage')
 require([x['bTy']for x in rpsu['branches']]==[-48,-12,-48] and all(x['minimum_yA']>=0 for x in rpsu['branches']),'exact pointed Farkas rays')
 extension=reports[SCRIPTS[4]]
 require(extension['scope']=='general_complex' and {x['id']for x in extension['source_witnesses']}=={'R8_2_53','R8_2_93'},'extension replay coverage')
 require([len(x)for x in extension['group_verification']['normal_abelian_subgroups']]==[1,9],'normal abelian square orders')
 extension2=reports[SCRIPTS[5]]
 require(extension2['scope']=='general_complex' and {x['id']for x in extension2['source_witnesses']}=={'R8_2_191','R8_2_299'},'A4 extension replay coverage')
 central=reports[SCRIPTS[7]]
 require(central.get('id')=='R7_2_160' and central.get('scope')=='general_complex','central boson replay coverage')
 four=reports[SCRIPTS[8]]
 require(four['scope']=='general_complex' and {x['id']for x in four['source_witnesses']}=={'R8_2_158','R8_2_186','R8_2_579','R8_2_682'},'S4 extension replay coverage')
 require(len(four['dimension12_classification']['valid_tables'])==6 and len(four['dimension12_classification']['eligible_tables'])==2,'complete intermediate ring classifier')
 require(four['S4_group_verification']['all_subgroups_enumerated']==30,'S4 group closure')
 # The parent checker pins its entire dependency manifest. Restore changed
 # dependencies and both ledgers, then remove c to prevent recursive dispatch.
 with tempfile.TemporaryDirectory(prefix='upper-c-parent-')as directory:
  H=Path(directory)/'repo'
  shutil.copytree(ROOT,H,ignore=shutil.ignore_patterns('__pycache__','.git','node_modules','*.pdf','*.zip','*.bin','*.o','*.log','*.aux','restore_selection.json','restore_pending.json','continuation'))
  for p in (E/'baseline_files').rglob('*'):
   if p.is_file():q=H/p.relative_to(E/'baseline_files');q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q)
  shutil.rmtree(H/'evidence/upper_residual_20261002c')
  spec=importlib.util.spec_from_file_location('published_parent_stage',H/'tools/verify_upper_residual_20261002b.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
  parent,anyon_ledgers=m.verify_update()
 require(parent['status']=='PASS' and parent['changed_records']==43,'parent replay')
 report={'status':'PASS','python_optimized':bool(sys.flags.optimize),'changed_records':len(D),'new_general_exclusions':len(D),'new_unitary_models':0,'previous_negative_records_unchanged':True,'unaffected_records_unchanged':True,'complete_historical_ledgers_restored':True,'pinned_source_files':len(sources),'source_manifest_sha256':MANIFEST_SHA256,'preservation_manifest_sha256':sha(E/'previous_records.json'),'parent_stage_replay':'PASS','parent_changed_records':43,'general_premise_replays':sorted(IDS),'status_totals':{str(r):dict(collections.Counter(x['status']for x in L))for r,L in ledgers.items()},'remaining_general_cases':{str(r):len(v)for r,v in remaining.items()},'scope':'General complex exclusions. Conditional and pivotal obstructions do not change the other decisions.'}
 return report,anyon_ledgers
def main():
 report,_=verify_update();print(json.dumps(report,indent=2));return report
if __name__=='__main__':main()
