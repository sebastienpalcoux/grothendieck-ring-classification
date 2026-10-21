"""Reconcile only source-bound exact M3 results; preserve historical973 rows.

The default output is a preview. Publishing requires matching independently
replayed normal and optimized receipts, current source/proof hashes and logs.
"""
import argparse,collections,copy,hashlib,json
from pathlib import Path
from m3_campaign import REPO,P,OUT,OLD_SHA,require,sha,write
from analyze import fp
EVIDENCE=OUT.parent
GENERAL={'general_complex_fusion_category','general','complex','all_complex_fusion_categories','all_characteristics'}
POSITIVE={'unitarily_realized','pseudo_unitarily_realized'}

def load(path,default=None):
 path=Path(path)
 if not path.exists():
  if default is not None:return default
  raise FileNotFoundError(path)
 return json.loads(path.read_text())
def records(value):
 if isinstance(value,list):return value
 if isinstance(value,dict):
  for key in ('records','exclusions','accepted','entries','models','results','per_ring','per_ring_attempts','attempts'):
   if isinstance(value.get(key),list):return value[key]
  if 'id' in value:return [value]
 return []
def relative(path):return str(Path(path).resolve().relative_to(REPO))
def digest(obj):return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def read_models():return records(load(EVIDENCE/'models/consolidated_models.json',[]))
def proof_rows():
 manifest=EVIDENCE/'criteria/accepted_exclusions.json';out=[]
 if manifest.exists():
  for r in records(load(manifest)):out.append((manifest,r))
 # These two root-owned sources are independently replayed by the aggregate
 # runner; other general root criteria enter only via accepted.py.
 for name in ('scalar_results.json','results.json','weighted_results.json'):
  path=EVIDENCE/'noncommutative'/name
  if path.exists():
   for r in records(load(path)):
    if r.get('status',r.get('outcome'))=='excluded':out.append((path,r))
 return out

def reconcile():
 require(sha(P/'data/decisions.json')==OLD_SHA,'historical decision bytes changed')
 old=load(P/'data/decisions.json');census=load(OUT/'census_m3.json');baseline=load(OUT/'decisions_m3.json')
 require(len(old)==973 and len(census)==len(baseline)==3527,'reconciliation source counts')
 byid={r['id']:r for r in census};rows=copy.deepcopy(baseline);bydecision={r['id']:r for r in rows}
 for r in rows:require(r['tensor_sha256']==byid[r['id']]['tensor_sha256']==fp(byid[r['id']]['tensor']),'baseline source binding')
 proofs={}
 for path,item in proof_rows():
  rid=item['id'];require(rid in byid,'unknown accepted id')
  require(item.get('tensor_sha256',item.get('source_tensor_sha256'))==byid[rid]['tensor_sha256'],'accepted proof tensor binding '+rid)
  scope=item.get('scope',item.get('certificate',{}).get('scope'))
  require(scope in GENERAL,'non-general proof in accepted manifest '+rid+': '+str(scope))
  cert=item.get('certificate',item.get('witness'))
  require(cert is not None,'accepted proof missing complete certificate '+rid)
  source=item.get('source_certificate_path',item.get('source',item.get('source_file',item.get('source_certificate'))))
  source_hash=item.get('source_sha256',item.get('source_certificate_sha256'))
  if source and source_hash:
   target=REPO/source
   if not target.exists():target=EVIDENCE/source
   require(target.exists() and sha(target)==source_hash,'accepted source hash '+rid)
  proofs.setdefault(rid,(path,item,cert))
 for rid,(path,item,cert) in proofs.items():
  r=bydecision[rid]
  if r['status']=='excluded':continue
  require(r['status']=='unresolved','positive/negative collision '+rid)
  r.update(status='excluded',criterion=item.get('criterion',cert.get('kind','accepted_exact_exclusion')),certificate=cert,certificate_scope='general_complex_fusion_category',certificate_source=relative(path),certificate_source_sha256=sha(path))
 models=read_models();seen=set()
 for model in models:
  rid=model['id'];require(rid in byid and rid not in seen,'model identity');seen.add(rid)
  require(model['tensor_sha256']==byid[rid]['tensor_sha256']==fp(model['tensor']) and model['tensor']==byid[rid]['tensor'],'model full tensor binding '+rid)
  require(model['status'] in POSITIVE,'model existence scope '+rid);r=bydecision[rid]
  require(r['status']=='unresolved','negative/model collision '+rid)
  require(model.get('constructors'),'model constructors missing '+rid)
  r.update(status=model['status'],models=[c.get('model',model['model']) for c in model['constructors']],model_source=relative(EVIDENCE/'models/consolidated_models.json'))
 # Unitary-only obstructions annotate rather than exclude general existence.
 unitary_path=EVIDENCE/'noncommutative/unitary_primary3_results.json'
 for item in records(load(unitary_path,[])):
  if item.get('status',item.get('outcome')) not in ('unitary_excluded','excluded'):continue
  rid=item['id'];require(rid in byid and item.get('tensor_sha256')==byid[rid]['tensor_sha256'],'unitary diagnostic source identity');require(rid not in seen,'unitary model/obstruction collision '+rid)
  r=bydecision[rid]
  if r['status']=='unresolved':r.update(unitary_status='excluded',unitary_obstruction_source=relative(unitary_path))
 ledger=old+rows;require(ledger[:973]==old,'historical records altered')
 counts=dict(collections.Counter(r['status'] for r in rows));summary={'rank':8,'multiplicity':3,'rings':3527,'counts':counts,'excluded':counts.get('excluded',0),'realized':sum(counts.get(s,0) for s in POSITIVE),'unitarily_realized':counts.get('unitarily_realized',0),'pseudo_unitarily_realized':counts.get('pseudo_unitarily_realized',0),'unresolved':counts.get('unresolved',0),'remaining_ids':[r['id'] for r in rows if r['status']=='unresolved'],'realized_ids':[r['id'] for r in rows if r['status'] in POSITIVE],'cumulative_counts':dict(collections.Counter(r['status'] for r in ledger)),'old_records_preserved':973,'preview':True,'ledger_digest':digest(ledger)}
 summary['unresolved_ids']=summary['remaining_ids']
 return ledger,summary

def _outcome(row):
 value=row.get('outcome',row.get('status','unspecified'))
 return {'survives':'no_conclusion','budget_exhausted':'timeout','not_eligible':'ineligible','not_applicable':'inapplicable'}.get(value,value)
def attempts(pending):
 ids={r['id'] if isinstance(r,dict) else r for r in pending};census={r['id']:r for r in load(OUT/'census_m3.json')};byid={rid:[] for rid in ids}
 def add(path,rows,stage=None,kind='exclusion'):
  for r in rows:
   rid=r.get('id')
   if rid not in ids:continue
   z={k:copy.deepcopy(v) for k,v in r.items() if k not in ('tensor','certificate','witness','branches','proof')};z.update(stage=stage or r.get('stage',r.get('method',r.get('family',Path(path).stem))),outcome=_outcome(r),attempt_kind=kind,source=relative(path));byid[rid].append(z)
 baseline=OUT/'attempts.jsonl'
 if baseline.exists():
  rows=[json.loads(line) for line in baseline.read_text().splitlines() if line.strip()]
  for r in rows:
   if r['id'] not in ids:continue
   R=census[r['id']]['tensor'];stage=r['stage']
   if not census[r['id']]['commutative'] and stage in ('dnumber','integral_drinfeld','cyclotomic','involution_module','field_automorphisms','subring_dimension','primitive_codegree'):r=dict(r,status='scope_inapplicable',reason='Implementation requires commutativity.')
   if census[r['id']]['commutative'] and stage=='noncomm_dnumber':r=dict(r,status='scope_inapplicable',reason='Noncommutative Wedderburn branch only.')
   if stage=='near_group':
    from analyze import dual
    du=dual(R)
    if sum(sum(R[i][du[i]])==1 for i in range(8))!=7:r=dict(r,status='scope_inapplicable',reason='Not a rank-eight near-group ring.')
   add(baseline,[r])
 for path in sorted((EVIDENCE/'criteria').glob('advanced*/*/*.json')):add(path,records(load(path)))
 for path in sorted((EVIDENCE/'criteria').glob('advanced/*/*.json')):add(path,records(load(path)))
 for name in ('subring_transfer.json','quadratic_compression.json','native_eligibility.json'):
  path=EVIDENCE/'criteria'/name
  if path.exists():add(path,records(load(path)))
 for path in sorted((EVIDENCE/'noncommutative').glob('*.json')):
  if 'validation' in path.name or path.name=='general_global_polynomial_validation.json':continue
  add(path,records(load(path)))
 for path in sorted((EVIDENCE/'performance').glob('*.json')):
  if any(x in path.name for x in ('progress','validation')):continue
  add(path,records(load(path)))
 for name in ('one_spectrum_m3.json','frobenius_results.json','graded_extensions_attempt.json'):
  path=OUT/name
  if path.exists():add(path,records(load(path)),kind='construction' if name=='frobenius_results.json' else 'exclusion')
 modelpath=EVIDENCE/'models/model_search_attempts.json'
 if modelpath.exists():
  obj=load(modelpath)
  for row in records(obj):
   rid=row.get('id')
   for a in row.get('construction_attempts',row.get('attempts',[])):
    b=dict(a,id=rid)
    if 'outcome' not in b and 'status' not in b:
     if 'matching_test_numbers' in b:
      b['outcome']='abstract_ring_lead_without_model' if b['matching_test_numbers'] else 'no_match_in_tested_family';b['tested_tensors']=obj.get('explicit_tensor_test_count')
     elif 'rejected_by_elementary_filter' in b:b['outcome']='family_excluded' if b['rejected_by_elementary_filter'] else 'no_conclusion'
     elif 'rejected' in b:b['outcome']='family_excluded' if b['rejected'] else 'no_conclusion'
     elif 'center_has_no_nontrivial_invertible_if_categorified' in b.get('certificate',{}):
      b['outcome']='family_excluded' if b['certificate']['center_has_no_nontrivial_invertible_if_categorified'] else 'no_conclusion';b.setdefault('scope',b['certificate']['scope']);b['structural_filter']=b['certificate']
     elif 'heuristic' in b.get('scope','').lower():b['outcome']='heuristic_search_completed'
     elif rid in b.get('receipt',{}).get('excluded_model_family_for',[]):b['outcome']='family_excluded'
     else:b['outcome']='scoped_construction_attempt'
    b.setdefault('scope','This construction family only; no arbitrary categorification exclusion.')
    add(modelpath,[b],kind='construction')
 grouppath=EVIDENCE/'performance/group_scan/per_id_attempts.json'
 if grouppath.exists():
  for row in records(load(grouppath)):
   for a in row.get('construction_attempts',row.get('attempts',[row])):add(grouppath,[dict(a,id=row['id'])],kind='construction')
 out=[]
 for rid in sorted(ids,key=lambda s:int(s.rsplit('_',1)[1])):
  unique=[];seen=set()
  for a in byid[rid]:
   key=digest(a)
   if key not in seen:seen.add(key);unique.append(a)
  out.append({'id':rid,'tensor_sha256':census[rid]['tensor_sha256'],'attempts':unique})
 return out

def validate_receipts(ledger):
 normal=load(OUT/'continuation_replay.json');optimized=load(OUT/'continuation_replay_optimized_invocation.json')
 for report in (normal,optimized):
  require(report.get('result',report.get('status'))=='PASS','full replay has not passed')
  require(report.get('receipt_scope','publication')=='publication','isolated validation receipt cannot authorize publication')
  require(report.get('ledger_digest',report.get('ledger_sha256'))==digest(ledger),'replayed ledger differs')
  for key in ('source_manifests_sha256','proof_source_sha256'):
   for rel,h in report[key].items():require(sha(REPO/rel)==h,'changed replay source '+rel)
  for section in report['sections']:
   p=Path(section['log']);require(not p.is_absolute() and '..' not in p.parts,'noncanonical replay log path');require(sha(REPO/p)==section['log_sha256'],'changed replay log '+str(p))
 require(normal['source_manifests_sha256']==optimized['source_manifests_sha256'] and normal['proof_source_sha256']==optimized['proof_source_sha256'],'normal/optimized proof inputs differ')
 require(optimized.get('requested_optimization',optimized.get('invocation')) in ('-O','optimized','optimized_invocation'),'optimized replay marker absent')
 return normal,optimized

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--publish',action='store_true');args=ap.parse_args();ledger,summary=reconcile();pending=[r for r in ledger if r['multiplicity']==3 and r['status']=='unresolved'];attemptrows=attempts(pending)
 write('continuation_preview.json',ledger);write('continuation_summary.json',summary);write('residual_attempts.json',attemptrows)
 from m3_residual_audit import audit
 write('residual_audit.json',audit(pending,attemptrows))
 if args.publish:
  validate_receipts(ledger);path=P/'output/m3/ledger.json';path.parent.mkdir(parents=True,exist_ok=True);temp=path.with_suffix('.json.tmp');temp.write_text(json.dumps(ledger,separators=(',',':'))+'\n');temp.replace(path);summary['preview']=False;write('continuation_summary.json',summary)
 print(json.dumps(summary,sort_keys=True))
if __name__=='__main__':main()
