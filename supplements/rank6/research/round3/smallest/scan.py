"""Replay full-census family applicability and the frozen 22/54 input domains."""
import json,sys,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];BASE=Path(__file__).parent;sys.path.insert(0,str(ROOT/'software'))
import round3_smallest as C
rows=json.load(open(ROOT/'data/census.json'));frozen=json.load(open(BASE/'campaign_inputs.json'))
C.require(hashlib.sha256((ROOT/'data/census.json').read_bytes()).hexdigest()==frozen['census_sha256'],'source census changed')
known={x['id'] for x in rows};C.require(set(frozen['residual_ids'])<=known and set(frozen['positive_ids'])<=known,'unknown input id')
hits=[]
for r in rows:
 f=C.family(r['N'])
 if f is None:continue
 rec=dict(id=r['id'],family=f)
 if f['multiplicity']%2:
  c=C.certificate(r['N']);C.verify(r['N'],c);rec.update(outcome='general_excluded',certificate=c)
 else:
  path=BASE/(r['id']+('_control.json' if r['id'] in frozen['positive_ids'] else '_certificate.json'))
  if path.exists():rec['outcome']=json.load(open(path))['outcome'];rec['record']=str(path.relative_to(ROOT))
  else:rec['outcome']='pending_exact_record'
 hits.append(rec)
report={'census_rows_checked':len(rows),'census_sha256':frozen['census_sha256'],'family_applicable':len(hits),'records':hits,
'residual_rows_checked':len(frozen['residual_ids']),'residual_applicable':[x['id'] for x in hits if x['id'] in frozen['residual_ids']],
'positive_rows_checked':len(frozen['positive_ids']),'positive_family_applicable':[x['id'] for x in hits if x['id'] in frozen['positive_ids']],
'positive_control_scope':'All 54 known realizations screened for family eligibility. Two fit the theorem: R6_2_4 survives the central relaxation; R6_1_3 has rational global dimension and is ineligible for this quadratic central implementation. Neither is excluded.',
'new_general_exclusions':[x['id'] for x in hits if x['id'] in frozen['residual_ids'] and x['outcome']=='general_excluded']}
C.require(not any(x['outcome']=='general_excluded' for x in hits if x['id'] in frozen['positive_ids']),'positive control excluded')
(BASE/'coverage.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='records'}))
