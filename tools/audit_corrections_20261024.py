"""Current audit correction; frozen predecessor ledgers retain their identity.

The scalar R436 replay is still valid for its prescribed table. Its general
categorical completeness premise is withdrawn, while the unitary exclusion
is retained. This module never rewrites a historical certificate or receipt.
"""
from pathlib import Path
from collections import Counter
from copy import deepcopy
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]
EVIDENCE='evidence/audit_20261024'
LEDGER='supplements/rank8/output/audited_20261024/ledger.json'
AUDIT=EVIDENCE+'/per_ring_research_audit.json'
BASELINE='supplements/rank8/output/exclusion_20261022/ledger.json'
RING_ID='R8_3_436'
REMAINING_IDS=['R8_3_436','R8_3_928','R8_3_941','R8_3_1154','R8_3_1768']
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def active(repo):return (Path(repo)/LEDGER).is_file()
def read(repo,name):return json.loads((Path(repo)/name).read_text())
def write(repo,name,value):
 p=Path(repo)/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
def corrected_rows(repo):
 acceptance=read(repo,EVIDENCE+'/accepted.json')
 if sha(Path(repo)/BASELINE)!=acceptance['baseline_sha256']:raise ValueError('Audit predecessor ledger changed')
 before=read(repo,BASELINE);rows=list(before)
 index=next(i for i,r in enumerate(rows)if r['id']==RING_ID)
 rows[index]=deepcopy(rows[index]);row=rows[index]
 if row['status']!='excluded' or row['criterion']!='near_group_C3_TPE_Galois_unitarity':raise ValueError('Unexpected R436 predecessor')
 row['withdrawn_general_certificate']=row.pop('certificate');row.pop('criterion')
 row.update(status='unresolved',general_status='unresolved',unitary_status='excluded',
            correction_source=EVIDENCE+'/README.md',
            correction_reason='The cited scalar-table completeness theorem is unitary in scope; completeness for an arbitrary spherical input category has not been established.')
 return rows

def validate(repo=ROOT):
 rows=corrected_rows(repo);published=read(repo,LEDGER)
 if rows!=published:raise ValueError('Published audit correction differs from the one-record reconciliation')
 exact=Counter(r['status']for r in rows if r['multiplicity']==3);total=Counter(r['status']for r in rows)
 if exact!=Counter(excluded=3506,unitarily_realized=16,unresolved=5):raise ValueError('Exact rank-eight counts')
 if total!=Counter(excluded=4402,unitarily_realized=93,unresolved=5):raise ValueError('Cumulative rank-eight counts')
 if [r['id']for r in rows if r['status']=='unresolved']!=REMAINING_IDS:raise ValueError('Audited remaining identifiers')
 a=read(repo,EVIDENCE+'/accepted.json')
 for name,h in a['source_sha256'].items():
  if sha(Path(repo)/name)!=h:raise ValueError('Audit source changed: '+name)
 return {'date':'2026-10-24','ledger':LEDGER,'ledger_sha256':sha(Path(repo)/LEDGER),'counts':dict(exact),'cumulative_counts':dict(total),'remaining_ids':REMAINING_IDS,'withdrawn_general_ids':[RING_ID],'preserved_other_records':4499,'unitary_exclusion_retained':True,'attempts_source':AUDIT,'evidence':EVIDENCE,'scope':'One proof-scope correction; no counterexample or new categorification is asserted.'}

def prepare(repo=ROOT):
 proof=EVIDENCE+'/README.md'
 write(repo,EVIDENCE+'/accepted.json',{'schema':'mathematical-audit-correction/v1','date':'2026-10-24','baseline':BASELINE,'baseline_sha256':sha(Path(repo)/BASELINE),'source_sha256':{name:sha(Path(repo)/name)for name in (proof,EVIDENCE+'/predecessor_publication.json','supplements/rank8/output/creative_20261022/model_catalog.json','supplements/rank8/data/rank8_m3_tables.txt.gz')},'corrections':['F1','F2','F3','F4','F5','F6','F7','F8']})
 rows=corrected_rows(repo);write(repo,LEDGER,rows)
 old=read(repo,'evidence/r3472_exclusion_20261022/per_ring_research_audit.json');a=deepcopy(old)
 a.update(schema='audited-rank8-per-ring/v1',remaining_unresolved=5,research_status='Five rank-eight general categorification questions remain open; the R436 unitary exclusion is retained.')
 r=next(r for r in a['rows']if r['id']==RING_ID)
 r['withdrawn_general_certificate']=r.pop('accepted_certificate',None)
 r['prior_stage_completed']=r.get('latest_completed',[])
 r.update(general_status='unresolved',screening_stage='unresolved',noncategorification_proved=False,categorification_or_novelty_proved=False,
          latest_completed=[{'domain':'scalar_table_scope_audit','outcome':'Prescribed scalar equations pass. General categorical completeness is unsupported by the pinned source.','scope':'Unitary exclusion retained; general existence unresolved.','limitation':'No counterexample and no categorification constructed.','proof':proof}],
          limitations=['General exclusion requires an additional theorem placing every spherical input category in the prescribed scalar normal form.'])
 write(repo,AUDIT,a);print(json.dumps(validate(repo),indent=2))
def publication_extension(repo=ROOT):
 """Current correction over a bound historical metadata checkpoint.

 This checks the exact current ledger, tensor source and model inventory. It
 does not decompress old proof archives or claim a fresh historical replay.
 """
 repo=Path(repo);report=validate(repo)
 item=deepcopy(read(repo,EVIDENCE+'/predecessor_publication.json'))
 item.pop('metadata_path',None);item.pop('metadata_sha256',None);item.pop('attempts',None)
 item.update(date='2026-10-24',excluded=3506,unresolved=5,remaining_ids=REMAINING_IDS,
             unitary_excluded_ids=[RING_ID],ledger=LEDGER,ledger_sha256=report['ledger_sha256'],
             evidence=EVIDENCE,attempts_source=AUDIT,audit_correction=report,
             historical_metadata_checkpoint=EVIDENCE+'/predecessor_publication.json',
             historical_metadata_scope='Retained source-bound checkpoint; no new historical categorical replay.')
 return item

def refresh_scope_sources(repo=ROOT):
 """Refresh current source bindings, retaining each prior hash as provenance."""
 repo=Path(repo);path=repo/'site/categorification_scope.json';payload=json.loads(path.read_text())
 def refresh(value):
  if isinstance(value,dict):
   relative=value.get('path')
   if relative and isinstance(relative,str)and value.get('sha256')and (repo/relative).is_file():
    current=sha(repo/relative)
    if current!=value['sha256']:
     value.setdefault('prior_sha256',value['sha256']);value['sha256']=current
   source=value.get('source')
   if isinstance(source,str)and isinstance(value.get('source_sha256'),str)and (repo/source).is_file():
    current=sha(repo/source)
    if current!=value['source_sha256']:
     value.setdefault('prior_source_sha256',value['source_sha256']);value['source_sha256']=current
   for child in value.values():refresh(child)
  elif isinstance(value,list):
   for child in value:refresh(child)
 refresh(payload);path.write_text(json.dumps(payload,indent=2,ensure_ascii=False)+'\n')
 for name in ('unresolved_cases.json','resolved_cases.json'):
  path=repo/'site/dist/data'/name
  if not path.exists():continue
  data=json.loads(path.read_text())
  for row in data['cases']:
   key='cases'if row['status']=='unresolved'else 'realized_cases'if row['status']=='unitarily_realized'else 'closed_cases'
   if row['id']in payload.get(key,{}):row['categorification_scope']=payload[key][row['id']]
   refresh(row.get('evidence',[]));refresh(row.get('research',[]))
  path.write_text(json.dumps(data,ensure_ascii=False,separators=(',',':'))+'\n')

def revise_generated_tex(name,text,repo=ROOT):
 if name=='m3_frontier.tex':
  start=text.find('\\subsection{A general inversion obstruction')
  if start>=0:
   end=text.index('\\subsection',start+12)
   text=text[:start]+(Path(repo)/EVIDENCE/'r436_conditional.tex').read_text()+text[end:]
  text=text.replace('These exact dimension, rank and invertible-group tests, supplemented by\nthe independent general exclusion of $\\sha{R8_3_436}$, exclude all five\nsingle-operation routes for the original $34$ frontier tensors, for every\npositive $n$.','These arithmetic tests exclude the listed routes except the general R436 branch. That branch requires the additional scalar-table completeness hypothesis; the unitary obstruction is retained. The uniform general exclusion of all five routes for all 34 tensors is not established.')
 if name=='m3_center_followup.tex':
  text=text.replace('as columns.  Then their unknown pair multiplicities form a matrix','as columns. Let $n_{\\mathrm{high}}$ be the number of remaining central simples. Their pair multiplicities form a matrix')
  text=text.replace('^{r\\times\\binom{s+1}{2}}','^{n_{\\mathrm{high}}\\times\\binom{s+1}{2}}')
 text=text.replace('Every remaining categorification admits a spherical structure and has a pseudo-unitary Galois conjugate; none can have a braided Morita representative.','For the four cases in the stated sphericality reduction these conclusions hold. The additional R436 case is unresolved in general, with its unitary exclusion retained.')
 return text

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--prepare',action='store_true');args=p.parse_args()
 if args.prepare:prepare()
 else:print(json.dumps(validate(),indent=2))
