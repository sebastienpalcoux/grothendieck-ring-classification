"""Current audit correction; frozen predecessor ledgers retain their identity.

The scalar R436 replay is still valid for its prescribed table. Its general
categorical completeness premise is withdrawn, while the unitary exclusion
is retained. This module never rewrites a historical certificate or receipt.
"""
from pathlib import Path
from collections import Counter
from copy import deepcopy
import hashlib,json,re
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
 text=text.replace('Every remaining categorification admits a spherical structure and has a pseudo-unitary Galois conjugate; none can have a braided Morita representative.','The generally open case $\\sha{R8_3_436}$ retains its unitary exclusion. The other four open cases admit sphericality and Galois pseudo-unitarity reductions and have no braided Morita representatives.')
 text=text.replace('For the four cases in the stated sphericality reduction these conclusions hold. The additional R436 case is unresolved in general, with its unitary exclusion retained.','The generally open case $\\sha{R8_3_436}$ retains its unitary exclusion. The other four open cases admit sphericality and Galois pseudo-unitarity reductions and have no braided Morita representatives.')
 if name=='rank8.tex':text=text.replace(r'\date{22 October 2026}',r'\date{24 October 2026}')
 from research_continuation_20261024 import active as latest_active, revise_generated_tex as latest_tex
 if latest_active(repo):return latest_tex(name,text,repo)
 return text

def revise_publication_document(name,text,repo=ROOT):
 """Apply current scope consistently after the preserved older renderers."""
 text=text.replace('a complete near-group TPE reduction','a conditional near-group TPE scalar-table reduction')
 text=text.replace('The current ledger is `supplements/rank8/output/exclusion_20261022/ledger.json`.','The current ledger is `supplements/rank8/output/audited_20261024/ledger.json`.')
 text=text.replace('Four rank-eight general categorification questions remain:',
                   'Apart from R8_3_436, four rank-eight general categorification questions remain:')
 text=text.replace('The remaining rings retain unresolved status for general complex categorification.',
                   'The remaining rings retain unresolved status for general complex categorification; R8_3_436 retains its unitary exclusion.')
 text=re.sub(r'Subsequent construction and research stages leave [45] current questions\.',
             'Subsequent construction and research stages, followed by the 24 October source-scope correction, leave five current rank-eight questions.',text)
 text=text.replace('The current ledger is `supplements/rank8/output/audited_20261024/ledger.json`.',
                   'The current ledger is `supplements/rank8/output/audited_20261024/ledger.json`. The preceding exclusion ledger is retained as historical evidence.')
 text=re.sub(r'\[Download all \d+ current open tensors\]\(\.\./data/remaining_cases\.py\)',
             '[Download all 26 current open tensors](../data/current_remaining_cases.py)',text)
 text=text.replace('Two rank-six and four rank-eight categorification questions remain open.',
                   'Two rank-six and five rank-eight categorification questions remain open.')
 text=text.replace('With the rank-two through rank-eight research-status report:',
                   'With the current research-status report:')
 stale=('For the current checkout, replay `python3 tools/verify_rank8_exclusion_20261022.py`; '
        'add `--historical` to replay earlier rank-eight stages in their preserved contexts. '
        'Earlier-stage commands below apply inside their corresponding immutable archives.')
 current=('For the current audited checkout, run `python3 tools/verify_audit_revision.py`. '
          'Full historical replay uses `python3 tools/verify_current_publication.py --historical`, '
          'which exports the pinned pre-audit Git snapshot. Earlier stage-specific commands '
          'below apply inside their corresponding immutable archives, with their original hypotheses.')
 text=text.replace(stale,current)
 notice='''<!-- current-audit-correction -->
**24 October audit correction.** R8_3_436 is unresolved for general complex
categorification; its unitary exclusion is retained. Rank eight through
multiplicity three now has 4,402 general exclusions, 93 models and five open
cases. With the rank-nine M2 continuation, the current project-wide total is
26 open cases. Earlier dated ledgers and replay receipts keep their historical
scope. [Correction and precise hypotheses](https://github.com/sebastienpalcoux/grothendieck-ring-classification/blob/main/evidence/audit_20261024/README.md).
<!-- /current-audit-correction -->'''
 if name.startswith('docs/') or name in ('manuscripts/README.md','site/README.md'):
  at=text.find('\n\n');text=text[:at]+'\n\n'+notice+text[at:]
 if name=='docs/PROJECT_GUIDE.md':
  text=text.replace('Potentially new tensor categories and open cases (PDF)','Earlier construction-candidates report (PDF)')
  text=re.sub(r'Seven provisional construction candidates, the known `Rep\(AGL\(1,7\)\)` model, and all \d+ current open cases\.',
              'Earlier report of seven provisional construction candidates, the known `Rep(AGL(1,7))` model, and the open cases at that checkpoint. [Current open tensors](../data/current_remaining_cases.py) cover all 26 present questions.',text)
 if name=='docs/VERIFY.md':
  section='''
## Current audit revision and structural filters

From the repository root:

```bash
python3 tools/verify_audit_revision.py
python3 tools/verify_current_publication.py --metadata-only
node site/tests/check_properties.mjs
```

The first command reconciles the single R436 correction, checks current
manuscript/download identities and all 26 open tensors, and recomputes exact
structural properties for every individual catalogue record. Metadata-only mode
checks identities and projections without repeating the exact property arithmetic.
Neither mode is a fresh replay of every categorical exclusion.

The automatic data workflow runs current publication checks and its separately
named mathematical controls. The predecessor's nested full-history run stopped
with disk exhaustion and supplies no new full-replay receipt. Historical replay
exports commit `111137a3e3ddf93be340b39c8a7c7b6ea94b844c` into a temporary
directory; it needs ample disk space and preserves the current checkout.
Inspect `python3 tools/replay_current_publication_ci.py --historical --plan`
before running it. A successful old scalar replay does not restore R436's
withdrawn general categorical premise.

The current rank-five complete replay remains the explicit command in its revised
guide. Its historical standalone verifier and bounded discovery driver have
the separately stated limitations.
'''
  at=text.index('<!-- /current-audit-correction -->')+len('<!-- /current-audit-correction -->')
  text=text[:at]+'\n'+section+text[at:]
 if name=='supplements/rank8/README.md':
  intro='''# Rank-eight current supplement

The [current audit correction](../../evidence/audit_20261024/accepted.json) binds
the ledger restored as `output/audited_20261024/ledger.json` by
`python3 tools/restore_data.py`. Through multiplicity three: **4,402 general
exclusions, 93 unitary models and five unresolved rings**. Exact multiplicity
three: **3,506 exclusions, 16 models and five unresolved rings**.
R8_3_436 remains excluded in the unitary setting.

[Correction and replay scope](../../evidence/audit_20261024/README.md) ·
[Current manuscript](../../manuscripts/rank8/paper/rank8.pdf) ·
[Open records](https://sebastienpalcoux.github.io/grothendieck-ring-classification/unresolved.html?rank=8)

<details><summary>Detailed method notes and historical replay receipts</summary>

'''
  text=intro+text.rstrip()+'\n\n</details>\n'
 if name=='oeis/update_2026-10-02.txt':
  text=text.replace('The certified exclusion of R8_3_3472 now leaves four rank-eight questions.',
                    'At the 22 October exclusion checkpoint, the exclusion of R8_3_3472 left four rank-eight questions.')
  text+='\nThe 24 October audit restores R8_3_436 to generally unresolved, retaining its unitary exclusion. The current rank-eight totals are 4,402 exclusions, 93 models and five open cases. Earlier checkpoint counts above are historical. See evidence/audit_20261024/README.md.\n'
 from research_continuation_20261024 import active as latest_active, revise_publication_document as latest_document
 if latest_active(repo):return latest_document(name,text,repo)
 return text

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--prepare',action='store_true');args=p.parse_args()
 if args.prepare:prepare()
 else:print(json.dumps(validate(),indent=2))
