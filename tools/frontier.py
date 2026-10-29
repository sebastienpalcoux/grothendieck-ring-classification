"""Current fusion-ring decisions and unified research frontier.

Frozen ledgers and categorical certificates are inputs. Only the explicitly
accepted R1768 record changes; current display metadata is derived here.
"""
from pathlib import Path
from collections import Counter
from copy import deepcopy
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]
DATE='2026-10-29'
EVIDENCE='evidence/frontier'
LEDGER=EVIDENCE+'/rank8_ledger.json'
EXACT_LEDGER=EVIDENCE+'/rank8_m3_ledger.json'
BASELINE='supplements/rank8/output/research_20261024/ledger.json'
REMAINING=['R6_4_155','R6_8_1660','R8_3_928','R8_3_941','R8_3_1154','R9_2_137']
R8_REMAINING=['R8_3_928','R8_3_941','R8_3_1154']
URL='https://github.com/sebastienpalcoux/grothendieck-ring-classification/blob/main/'
FINDINGS={
 'R6_4_155':('Every Morita dual of a pseudo-unitary categorification has the same based ring R6_4_155. The complete connected-algebra reduction leaves a possible algebra 1+X+X*, whose existence is not proved. General categorification remains unresolved.','r155/MORITA_RING_RIGIDITY.md'),
 'R6_8_1660':('The fermion centralizer is nonsplit and s-simple. The candidate algebra 1+X has two cyclic multiplication directions; associativity and separability remain unproved. Such an algebra would give the R8_3_941 Morita partner. Neither categorification nor the algebra is constructed.','r1660_941/REPORT.md'),
 'R8_3_928':('One complete necessary fusion matrix is forced in all four modular patterns, and a second in two patterns. They pass exact integrality and positivity checks. No full modular completion or categorical model is established; general categorification remains unresolved.','r928/SPECTRAL_FUSION_REDUCTION.md'),
 'R8_3_941':('The fermion centralizer is nonsplit and s-simple. Whole-column Galois symmetry restricts ninth-root twist sectors; all fourteen retained allocations survive. A Morita construction from R6_8_1660 remains conditional on the existence of that category and a separable algebra 1+X.','r1660_941/REPORT.md'),
 'R8_3_1154':('Every complex categorification has simple Drinfeld center, using the established integral-center restriction. The auxiliary rank-ten candidate passes conjugation parity. These are necessary restrictions, not a categorification or a general exclusion.','r1154/SIMPLE_CENTER.md'),
 'R8_3_1768':('General complex categorification is excluded. Pivotal conjugation preserves the symmetry sign of a self-duality; the required odd constituents contradict its pairing parity. The general-complex existence gate and complete center domains are explicit inherited premises; six exact rational separators replay successfully.','r1768/PALINDROMIC_EXCLUSION.md'),
 'R9_2_137':('Whole restriction-column Galois symmetry and the fourth-rotation Clifford bound strengthen the necessary center system. Both TY signs still admit exact rational witnesses after 7,222 variable removals. The witnesses are necessary data, not categorical models; general categorification remains unresolved.','r137/REPORT.md'),
}
def read(p):return json.loads(Path(p).read_text())
def write(p,v,compact=False):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text(json.dumps(v,ensure_ascii=False,indent=None if compact else 2,separators=(',',':')if compact else None)+'\n')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def active(repo=ROOT):return (Path(repo)/EVIDENCE/'accepted.json').is_file()
def proof(repo,path):
 p=Path(repo)/path
 return {'label':p.name,'path':path,'url':URL+path,'sha256':sha(p)}
def current_scope(rid,scope,repo=ROOT):
 scope=deepcopy(scope)
 if rid not in FINDINGS:return scope
 text,rel=FINDINGS[rid];sources=[proof(repo,EVIDENCE+'/replay/new/'+rel)]
 scope['notes']=[text]
 if rid=='R8_3_1768':
  scope.update(general_status='excluded',level_status={k:'excluded'for k in ('general','pivotal','spherical','pseudo_unitary','unitary')},strongest_excluded='general',same_category_implications=[],existence_implications=[],audit_sources=sources,
   braided={'status':'excluded','explanation':'General complex categorification is excluded.','sources':sources})
 return scope
def validate_ledger(repo=ROOT):
 repo=Path(repo);old=read(repo/BASELINE);new=read(repo/LEDGER)
 fields=('id','rank','multiplicity','index','status','tensor_sha256','criterion','proof','certificate')
 def project(r):return {k:r[k]for k in fields if k in r and isinstance(r[k],(str,int,bool))}
 if len(old)!=4500 or len(new)!=4500:raise ValueError('Rank-eight complete ledger coverage')
 changed=[]
 for source,current in zip(old,new):
  before=project(source)
  if before['id']!=current['id']or before['tensor_sha256']!=current['tensor_sha256']:raise ValueError('Ledger tensor identity')
  if before!=current:
   changed.append(current['id'])
   if current['id']!='R8_3_1768'or before['status']!='unresolved'or current['status']!='excluded':raise ValueError('Unexpected status change')
   if current.get('criterion')!='pivotal_conjugation_pairing':raise ValueError('Exact accepted criterion')
   if {k:v for k,v in current.items()if k in before and k!='status'}!={k:v for k,v in before.items()if k!='status'}:raise ValueError('Unrelated case fields changed')
 if changed!=['R8_3_1768']:raise ValueError('Exactly one new exclusion required')
 if Counter(r['status']for r in new)!=Counter(excluded=4404,unitarily_realized=93,unresolved=3):raise ValueError('Rank-eight cumulative partition')
 exact=[r for r in new if r['multiplicity']==3]
 if exact!=read(repo/EXACT_LEDGER):raise ValueError('Exact-multiplicity ledger projection')
 return {'status':'PASS','excluded':3508,'unitarily_realized':16,'unresolved':3,'remaining_ids':R8_REMAINING,'cumulative':{'excluded':4404,'unitarily_realized':93,'unresolved':3},'proof_payloads':'Unchanged in the SHA-bound frozen baseline ledger; current index preserves identity, status and criterion references.'}
def publication_extension(repo=ROOT):
 from research_continuation_20261024 import publication_extension as prior
 repo=Path(repo);validate_ledger(repo);item=deepcopy(prior(repo))
 item.update(date=DATE,excluded=3508,unresolved=3,remaining_ids=R8_REMAINING,ledger=LEDGER,ledger_sha256=sha(repo/LEDGER),evidence=EVIDENCE,attempts_source=EVIDENCE+'/rank8_research_audit.json',current_frontier=EVIDENCE+'/accepted.json')
 return item
def apply_profiles(repo=ROOT):
 repo=Path(repo)
 if not active(repo):return
 decision=next(r for r in read(repo/LEDGER)if r['id']=='R8_3_1768')
 r9_path='evidence/frontier_20261027/rank9_m2_ledger.json'
 r9={r['id']:r for r in read(repo/r9_path)}
 up=repo/'site/dist/data/unresolved_cases.json';rp=repo/'site/dist/data/resolved_cases.json'
 un=read(up);closed=read(rp);moved=[r for r in un['cases']if r['id']=='R8_3_1768']
 if moved:
  un['cases']=[r for r in un['cases']if r['id']!='R8_3_1768'];closed['cases']=[r for r in closed['cases']if r['id']!='R8_3_1768']+moved
  write(up,un,True);write(rp,closed,True)
 sp=repo/'site/categorification_scope.json';sc=read(sp)
 previous=sc['cases'].pop('R8_3_1768',sc['closed_cases'].get('R8_3_1768'))
 if previous is not None:sc['closed_cases']['R8_3_1768']=current_scope('R8_3_1768',previous,repo)
 write(sp,sc)
 for name in ('unresolved_cases.json','resolved_cases.json','rank9_m2.json'):
  p=repo/'site/dist/data'/name
  if not p.is_file():continue
  v=read(p)
  for row in v['cases']:
   rid=row['id']
   if rid not in FINDINGS:continue
   text,rel=FINDINGS[rid];path=EVIDENCE+'/replay/new/'+rel;sources=[proof(repo,path)]
   row['summary']=text
   row['research']=[{'title':'Current proof and remaining gap','source':path,'url':URL+path,'source_sha256':sources[0]['sha256'],'data':{'status':'excluded'if rid=='R8_3_1768'else'unresolved','findings':text,'scope':'General complex exclusion'if rid=='R8_3_1768'else'Necessary conditions; no categorical model'}}]
   row['evidence']=sources
   row['categorification_scope']=current_scope(rid,row['categorification_scope'],repo)
   def scope_sources(v):
    if isinstance(v,dict):
     if all(k in v for k in ('path','url','sha256')):yield v
     for z in v.values():yield from scope_sources(z)
    elif isinstance(v,list):
     for z in v:yield from scope_sources(z)
   row['evidence']=list({x['path']:x for x in row['evidence']+list(scope_sources(row['categorification_scope']))}.values())
   if rid in r9:
    src=proof(repo,r9_path)
    row['research'].insert(0,{'title':'Current accepted case decision','source':r9_path,'url':src['url'],'source_sha256':src['sha256'],'data':r9[rid]})
    row['evidence'].insert(0,src)
   if rid=='R8_3_1768':
    s=proof(repo,LEDGER)
    row.update(status='excluded',existence='excluded',source_file=LEDGER,source_url=s['url'],investigation_deferred=False)
    row['research'].insert(0,{'title':'Current accepted case decision','source':LEDGER,'url':s['url'],'source_sha256':s['sha256'],'data':decision})
    row['evidence'].insert(0,s)
   row['evidence']=list({x['path']:x for x in row['evidence']}.values())
  v['scope']='Current case profiles; excluded and unresolved status is explicit for each record.'
  write(p,v,True)
def revise_document(name,text,repo=ROOT):
 """Final readable account after historical source renderers have run."""
 if not active(repo):return text
 from frontier_docs import render
 current=render(name,repo)
 if current is not None:return current
 import re
 text=re.sub(r'<!-- (?:frontier-20261027|correctness-20261025|current-research-continuation|current-theoretical-retry|current-high-rank-publication|current-audit-correction|current-frontier) -->.*?<!-- /(?:frontier-20261027|correctness-20261025|current-research-continuation|current-theoretical-retry|current-high-rank-publication|current-audit-correction|current-frontier) -->\s*','',text,flags=re.S)
 text=re.sub(r'<details>\s*<summary>(?:Earlier lower-rank reading notes and research history|Earlier research and classification notes).*?</details>\s*','',text,flags=re.S)
 replacements={
  '**7 open cases.**':'**6 open cases.**','7 unresolved rings':'6 unresolved rings','all seven open cases':'all six open cases','all 7 open tensors':'all 6 open tensors',
  'Seven cases remain unresolved':'Six cases remain unresolved','seven cases remain unresolved':'six cases remain unresolved','seven open cases':'six open cases','seven remaining open cases':'six remaining open cases',
  'two at rank six, four at rank eight and one at rank nine':'two at rank six, three at rank eight and one at rank nine',
  'two rank-six and four rank-eight':'two rank-six and three rank-eight','Two rank-six and four rank-eight':'Two rank-six and three rank-eight',
  '4,403 excluded, 93 realized, 4 unresolved':'4,404 excluded, 93 realized, 3 unresolved',
  '4,403 general exclusions, 93 unitary models and four unresolved':'4,404 general exclusions, 93 unitary models and three unresolved',
  '3,507 general exclusions, 16 models and 4 unresolved':'3,508 general exclusions, 16 models and 3 unresolved',
  'four current rank-eight questions':'three current rank-eight questions',
  '[Earlier construction-candidates report · PDF](docs/New_category_candidates_and_open_cases.pdf)':'[Current frontier report · PDF](manuscripts/frontier/Fusion_Ring_Frontier.pdf)',
  '4,403 exclusions, 93 unitary models and 4 unresolved':'4,404 exclusions, 93 unitary models and 3 unresolved',
 }
 for a,b in replacements.items():text=text.replace(a,b)
 banner=('<!-- current-frontier -->\n**Current classification · 29 October 2026.** R8_3_1768 is excluded over the complex numbers by pivotal conjugation parity, using the established existence and center-domain reductions. **Six cases remain unresolved:** two at rank six, three at rank eight and one at rank nine. No additional model is claimed. [Current proofs and exact checks](https://github.com/sebastienpalcoux/grothendieck-ring-classification/blob/main/evidence/frontier/README.md).\n<!-- /current-frontier -->\n\n')
 if name.startswith(('docs/','manuscripts/','site/'))or name=='README.md':
  at=text.find('\n\n');text=text[:at+2]+banner+text[at+2:]
 return text


def publication_matches(relative,expected,repo=ROOT):
 repo=Path(repo);p=repo/relative;receipt=repo/EVIDENCE/'publication_replacements.json'
 if not active(repo)or not p.is_file()or not receipt.is_file():return False
 v=read(receipt);entry=v['files'].get(relative)
 if not entry or expected not in entry['prior_sha256'] or sha(p)!=entry['after_sha256']:return False
 return all(sha(repo/name)==h for name,h in v['immutable_decisions'].items())
