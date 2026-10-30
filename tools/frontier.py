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
FINDINGS={'R6_4_155': ('Every positive Morita dual has the same based ring. In the specified order-32 '
              'near-group construction route, the parent group must be C4 × C2³. Compatible '
              'pointed data exist, but the parent category and required algebra are unconstructed. '
              'General categorification remains unresolved.',
              'r155/CONTINUATION.md'),
 'R6_8_1660': ('A nonreal dimension-weighted third indicator excludes real forms and braided '
               'representatives in the positive Morita class. The center is prime, excluding '
               'smaller direct modular sources. The proposed algebra 1+X and its R941 Morita '
               'partner remain conditional.',
               'pair/REPORT.md'),
 'R8_3_928': ('Three of four necessary center patterns are excluded. For the positive spherical '
              'representative in the existence reduction, the surviving Drinfeld center must '
              'have rank 40 and split as Z(C) = Sem⁻ ⊠ B, with B of rank 20 (or the conjugate '
              'orientation). Sem⁻ is the rank-two opposite semion category. Anyon Atlas '
              'B20-02148, Galois orbit 20.167, supplies exact candidate modular data for B; '
              'uniqueness of the full data is unproved. Neither a category realizing B nor '
              'the required separable algebra is constructed. R928 remains unresolved.',
              'r928/REPORT.md'),
 'R8_3_941': ('The center of a positive representative is prime and obeys the direct '
              'modular-source obstruction. Its fermion centralizer is nonsplit and s-simple. The '
              'proposed R1660–R941 Morita equivalence still requires a category and a separable '
              'algebra 1+X.',
              'pair/REPORT.md'),
 'R8_3_1154': ('One branch of a hypothetical smallest algebra 1+X4 forces an explicit simple '
               'rank-seven Morita-dual fusion ring. The algebra and module associators are '
               'unconstructed, and the other based-module branch also survives. General '
               'categorification remains unresolved.',
               'r1154/CONDITIONAL_RANK7_ROUTE.md'),
 'R8_3_1768': ('General complex categorification is excluded. Pivotal conjugation preserves the '
               'symmetry sign of a self-duality; the required odd constituents contradict its '
               'pairing parity. The general-complex existence gate and complete center domains are '
               'explicit inherited premises; six exact rational separators replay successfully.',
               'r1768/PALINDROMIC_EXCLUSION.md'),
 'R9_2_137': ('Full-column Galois symmetry and nine exact integral Verlinde bounds exclude the '
              'positive Tambara–Yamagami sign in a positive spherical representative. The negative '
              'sign retains a checked rational necessary-condition witness, not a '
              'categorification. The ring remains unresolved.',
              'r137/NEW_RESULTS.md')}
def read(p):return json.loads(Path(p).read_text())
def write(p,v,compact=False):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text(json.dumps(v,ensure_ascii=False,indent=None if compact else 2,separators=(',',':')if compact else None)+'\n')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def active(repo=ROOT):return (Path(repo)/EVIDENCE/'accepted.json').is_file()
def proof(repo,path):
 p=Path(repo)/path
 return {'label':p.name,'path':path,'url':URL+path,'sha256':sha(p)}
def finding_path(rid):
 text,rel=FINDINGS[rid]
 return EVIDENCE+'/replay/'+('current/' if rid in REMAINING else 'new/')+rel
def restriction_metadata():
 item={
  'date':DATE,'new_general_exclusions':[],'new_models':0,'remaining_ids':list(REMAINING),
  'proof_directory':EVIDENCE+'/replay/current',
  'replay_receipt':EVIDENCE+'/current_run_receipt.json',
  'anyon_atlas_record':'https://anyonatlas.org/data/B20-02148',
  'atlas_galois_orbit':'20.167',
  'categorification_of_rank20_datum_established':False,
  'replay_receipt_sha256':sha(ROOT/EVIDENCE/'current_run_receipt.json'),
  'proof_manifest_sha256':sha(ROOT/EVIDENCE/'replay/current/manifest.json')}
 archive=ROOT/'site/dist/downloads/Fusion-Ring-Frontier-Proofs-and-Checks.zip'
 if archive.is_file():item['replay_archive']={'path':archive.relative_to(ROOT).as_posix(),'sha256':sha(archive),'bytes':archive.stat().st_size}
 return item
def current_scope(rid,scope,repo=ROOT):
 scope=deepcopy(scope)
 if rid not in FINDINGS:return scope
 text,rel=FINDINGS[rid];sources=[proof(repo,finding_path(rid))]
 scope['notes']=[text]
 scope['audit_sources']=sources
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
 for rid in REMAINING:
  if rid in sc['cases']:sc['cases'][rid]=current_scope(rid,sc['cases'][rid],repo)
 write(sp,sc)
 for name in ('unresolved_cases.json','resolved_cases.json','rank9_m2.json'):
  p=repo/'site/dist/data'/name
  if not p.is_file():continue
  v=read(p)
  for row in v['cases']:
   rid=row['id']
   if rid not in FINDINGS:continue
   text,rel=FINDINGS[rid];path=finding_path(rid);sources=[proof(repo,path)]
   row['summary']=text
   row['research']=[{'title':'Current proof and remaining gap','source':path,'url':URL+path,'source_sha256':sources[0]['sha256'],'data':{'status':'excluded'if rid=='R8_3_1768'else'unresolved','findings':text,'scope':'General complex exclusion'if rid=='R8_3_1768'else'Necessary conditions; no categorical model'}}]
   if rid=='R8_3_928':
    row['research'][0]['data']['modular_data']={
      'atlas_id':'B20-02148','atlas_url':'https://anyonatlas.org/data/B20-02148',
      'galois_orbit':'20.167','rank':20,'central_charge_mod8':1,'twist_order':96,
      'role':'Candidate modular data for the rank-20 factor B in the forced rank-40 decomposition Z(C) = Sem⁻ ⊠ B, in the chosen positive spherical orientation.',
      'center_rank':40,'pointed_factor':'Rank-two opposite semion category Sem⁻',
      'full_modular_data_uniqueness_established':False,
      'center_charge':'The opposite semion factor has charge -1; the Drinfeld center of a spherical fusion category has charge 0 modulo 8.',
      'exact_comparison':{'S_entries':400,'twists':20,'fusion_coefficients':8000},
      'categorification_established':False,'algebra_established':False}
    match=proof(repo,EVIDENCE+'/replay/current/r928/atlas/atlas_match_receipt.json')
    sources.append(match)
   if rid=='R9_2_137':
    row['research'][0]['data']['TY_branches']={
      'positive':'excluded','negative':'unresolved',
      'scope':'The positive spherical representative supplied by the inherited existence reduction.'}
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
 # The scope file was rewritten above; refresh its references in other profiles.
 def refresh_scope_binding(value):
  if isinstance(value,dict):
   if value.get('path')=='site/categorification_scope.json' and 'sha256' in value:
    value['sha256']=sha(sp)
   for child in value.values():refresh_scope_binding(child)
  elif isinstance(value,list):
   for child in value:refresh_scope_binding(child)
 for name in ('unresolved_cases.json','resolved_cases.json','rank9_m2.json','realized_rings.json'):
  path=repo/'site/dist/data'/name
  if path.is_file():
   payload=read(path);refresh_scope_binding(payload);write(path,payload,True)

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
 if name=='docs/CASE_INVENTORY.md':
  for rid in ('R6_4_155','R6_8_1660'):
   note=FINDINGS[rid][0]
   row=f'| `'+rid+'` | **Open.** '+note+' | [Current proof](../'+finding_path(rid)+') · [Manuscript](../manuscripts/rank6/papers/chapters/pairing_morita_20261027.tex) |'
   text=re.sub(r'^\| `'+re.escape(rid)+r'` \| \*\*Open\.\*\*.*$',lambda m:row,text,flags=re.M)
  text=text.replace('Current manuscript section','Current proof and manuscript')
 text=text.replace('The four remaining rings retain unresolved status for general complex categorification.','The three remaining rank-eight rings retain unresolved status for general complex categorification.')
 banner=('<!-- current-frontier -->\n**Current classification · 29 October 2026.** R8_3_1768 is excluded over the complex numbers by pivotal conjugation parity, using the established existence and center-domain reductions. **Six cases remain unresolved:** two at rank six, three at rank eight and one at rank nine. No additional model is claimed. [Current proofs and exact checks](https://github.com/sebastienpalcoux/grothendieck-ring-classification/blob/main/evidence/frontier/README.md).\n<!-- /current-frontier -->\n\n')
 if name=='README.md':banner=banner.replace('No additional model is claimed.','The latest restrictions exclude three R928 center patterns and the positive TY sign for R137. For R928, the surviving positive spherical center must have rank 40 and split as Sem⁻ ⊠ B, with B of rank 20 (or the conjugate orientation); [Anyon Atlas B20-02148](https://anyonatlas.org/data/B20-02148) supplies candidate modular data for B, whose full-data uniqueness is unproved. No additional model is claimed.')
 if name.startswith(('docs/','manuscripts/','site/'))or name=='README.md':
  at=text.find('\n\n');text=text[:at+2]+banner+text[at+2:]
 return text


def publication_matches(relative,expected,repo=ROOT):
 repo=Path(repo);p=repo/relative;receipt=repo/EVIDENCE/'publication_replacements.json'
 if not active(repo)or not p.is_file()or not receipt.is_file():return False
 v=read(receipt);entry=v['files'].get(relative)
 if not entry or expected not in entry['prior_sha256'] or sha(p)!=entry['after_sha256']:return False
 return all(sha(repo/name)==h for name,h in v['immutable_decisions'].items())
