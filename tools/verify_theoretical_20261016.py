#!/usr/bin/env python3
"""Replay the theoretical update, preserve all earlier decisions, optionally replay history."""
from pathlib import Path
import argparse,collections,copy,hashlib,json,shutil,subprocess,sys,tempfile
ROOT=Path(__file__).resolve().parents[1]
STAGE='evidence/theoretical_20261016'
# Bound after the final proof/source inventory is frozen.
MANIFEST_SHA256='a34df291f7ca848d0f877cd994b923e41ba0d0fc496c79a65612d1542941335b'
def need(ok,message):
 if not ok:raise ValueError(message)
def cd(value):return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def read(path):return json.loads(path.read_text())
def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--repo',type=Path,default=ROOT);parser.add_argument('--historical',action='store_true');parser.add_argument('--spectral',action='store_true');args=parser.parse_args();root=args.repo.resolve();e=root/STAGE
 need(sha(e/'source_files.json')==MANIFEST_SHA256,'Proof manifest identity')
 for relative,digest in read(e/'source_files.json').items():
  p=root/relative;need(p.is_file() and sha(p)==digest,'Source changed: '+relative)
 decisions=read(e/'decisions.json');prior=read(e/'previous_records.json');remaining=read(e/'remaining_ids.json');expected=read(e/'expected_totals.json')
 need(len(decisions)==len({x['id'] for x in decisions}), 'Duplicate decisions')
 need(all(x['scope']=='general_complex' and x['status']=='excluded' for x in decisions),'General scope')
 restored={};totals={}
 for rank,meta in prior['ranks'].items():
  rows=read(root/meta['ledger']);by={x['id']:x for x in rows};changes={x['id']:x for x in decisions if str(x['rank'])==rank};old={x['id']:x for x in meta['previous_records']}
  need(len(rows)==len(by)==meta['records'],'Census coverage')
  need(set(old)==set(changes)==set(meta['transitions']),'Decision coverage')
  for rid,d in changes.items():
   row=by[rid];need(old[rid]['status']=='unresolved' and row['status']=='excluded','Transition '+rid)
   need(cd(row)==meta['transitions'][rid]['new_record_sha256'],'Updated record '+rid)
   stable=('id','rank','multiplicity','source_line','commutative','tensor') if rank=='7' else ('id','multiplicity','index','tensor_sha256','commutative')
   need(all(row[k]==old[rid][k] for k in stable),'Tensor identity '+rid)
   need(row['certificate']['scope']=='general_complex' and row['certificate']['proof']==STAGE+'/'+d['proof'],'Proof binding '+rid)
  need(cd([x for x in rows if x['id'] not in changes])==meta['unchanged_records_sha256'],'Unchanged records')
  historical=[copy.deepcopy(old.get(x['id'],x)) for x in rows]
  need(cd(historical)==meta['baseline_canonical_sha256'],'Complete baseline ledger')
  need(cd([x for x in historical if x['status']=='excluded'])==meta['previous_negative_records_sha256'],'Previous negatives')
  need([x['id'] for x in rows if x['status']=='unresolved']==remaining[rank],'Remaining frontier')
  totals[rank]=dict(collections.Counter(x['status'] for x in rows));need(totals[rank]==expected[rank],'Current totals')
  restored[meta['ledger']]=historical
 scripts=sorted({d['verifier'] for d in decisions})+['compression/verify_full_I1_scan.py','compression/verify_higher_field_compression.py','rank7/verify_scoped_dimension_block.py','compression/verify_rank8_full_I1.py','rank6/verify_twist_one_arithmetic.py','rank6/r155_reflection/replay.py','rank6/r155_center_module/verify_anti_module.py','rank6/r1660_modular_witness/replay.py','rank8_m1/verify.py','rank8/verify_frontier_modules.py']
 reports={}
 for script in scripts:
  cmd=[sys.executable]+(['-O'] if sys.flags.optimize else [])+[str(e/script)]
  if script.startswith(('rank7/','rank8/')):cmd+=['--repo',str(root)]
  result=subprocess.run(cmd,cwd=root,text=True,capture_output=True)
  need(result.returncode==0,script+' failed:\n'+result.stdout+result.stderr)
  try:report=json.loads(result.stdout)
  except json.JSONDecodeError:raise ValueError(script+' must print its exact JSON receipt')
  need(report.get('status')=='PASS',script+' not PASS');reports[script]=report
 if args.spectral:
  with tempfile.TemporaryDirectory() as directory:
   cmd=[sys.executable]+(['-O'] if sys.flags.optimize else [])+[str(e/'rank7/verify_signed_pair.py'),'--repo',str(root),'--output',str(Path(directory)/'receipt.json')]
   result=subprocess.run(cmd,cwd=root,text=True,capture_output=True);need(result.returncode==0,'Independent spectral backup failed: '+result.stderr)
 historical_status='not requested; parent evidence preserved'
 if args.historical:
  with tempfile.TemporaryDirectory(prefix='theoretical-parent-') as directory:
   target=Path(directory)/'repo'
   shutil.copytree(root,target,ignore=shutil.ignore_patterns('.git','work','node_modules','__pycache__','*.pdf','*.zip','*.bin','*.log','*.aux','*.out','*.toc','*.fls','*.fdb_latexmk'))
   for relative,rows in restored.items():(target/relative).write_text(json.dumps(rows,indent=2)+'\n')
   # Later publication counts are not inputs to the frozen stage; its verifiers
   # restore every earlier changed dependency from their own baseline_files.
   cmd=[sys.executable]+(['-O'] if sys.flags.optimize else [])+[str(target/'tools/verify_upper_residual_20261002c.py')]
   result=subprocess.run(cmd,cwd=target,text=True,capture_output=True)
   need(result.returncode==0,'Historical replay failed:\n'+result.stdout+result.stderr)
   parent=json.loads(result.stdout);need(parent['status']=='PASS','Historical stage not PASS');historical_status='PASS'
 print(json.dumps({'status':'PASS','python_optimized':bool(sys.flags.optimize),'changed_records':len(decisions),'new_general_exclusions':len(decisions),'new_unitary_models':0,'status_totals':totals,'previous_negative_records_unchanged':True,'unaffected_records_unchanged':True,'complete_baseline_ledgers_reconstructed':True,'source_manifest_sha256':MANIFEST_SHA256,'exact_replays':{p:r.get('status') for p,r in reports.items()},'historical_replay':historical_status,'spectral_backup_replayed':args.spectral,'scope':'General exclusions only. Scoped results do not change other categorification decisions.'},indent=2))
if __name__=='__main__':main()
