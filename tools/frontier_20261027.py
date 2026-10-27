"""Accepted three-case transition and seven-case theoretical continuation.

Historical categorical ledgers and receipts remain immutable. This module
selects the new ledger and adds explicitly scoped current case findings.
"""
from pathlib import Path
import hashlib, json, re

ROOT = Path(__file__).resolve().parents[1]
DATE = '2026-10-27'
EVIDENCE = 'evidence/frontier_20261027'
LEDGER = EVIDENCE + '/rank9_m2_ledger.json'
EXCLUDED = ('R9_2_1607', 'R9_2_1975', 'R9_2_1976')
REMAINING = ['R6_4_155', 'R6_8_1660', 'R8_3_928', 'R8_3_941',
             'R8_3_1154', 'R8_3_1768', 'R9_2_137']
COUNTS = {'excluded': 2046, 'unitarily_realized': 36, 'unresolved': 1}
URL = 'https://github.com/sebastienpalcoux/grothendieck-ring-classification/blob/main/'

FINDINGS = {
 'R6_4_155': ('A connected separable algebra with underlying object 1+kX+kX* has k at most two. The k=2 algebra is forced by the canonical central algebra, but its module category returns to the pointed-algebra Morita route. The k=1 algebra has not been constructed. General categorification remains unresolved.',
   ['evidence/unresolved7_20261027/audit_fs2/R155_ALGEBRA_REDUCTION.md']),
 'R6_8_1660': ('Pairing parity excludes two proposed Morita module realizations and a center subcase is removed; both overall spin alternatives remain. In a hypothetical pseudo-unitary categorification, any connected separable algebra 1+X, with FPdim(X)=3+2sqrt(2)+2sqrt(3)+sqrt(6), has bimodule category with ring R8_3_941. Neither the category nor this algebra is constructed.',
   [EVIDENCE+'/MORITA_R1660_R941.md', 'evidence/unresolved7_20261027/r6_1660/MORITA_PAIRING_FILTER.md', 'evidence/unresolved7_20261027/r6_1660/SPIN_CONSTRAINTS.md']),
 'R8_3_928': ('The nonpointed modular centralizer must be simple, of rank 17, 20 or 23, with exactly one nontrivial connected etale algebra. Every module category is regular, so the shared global FP dimension does not make it a rank-six Morita partner. These restrictions do not settle general categorification.',
   ['evidence/unresolved7_20261027/r8_928_941/REPORT.md', EVIDENCE+'/MORITA_R1660_R941.md']),
 'R8_3_941': ('Its rank-22 fermion centralizer must be nonsplit and have no proper nonpointed fusion subcategory. The conditional R6_8_1660 construction uses a connected separable algebra 1+X; the inverse algebra in that Morita context is also 1+one selfdual simple of the same dimension. Neither algebra is known to exist, and existence of a rank-six partner is not forced for every hypothetical R941 category.',
   [EVIDENCE+'/MORITA_R1660_R941.md', 'evidence/unresolved7_20261027/r8_928_941/REPORT.md']),
 'R8_3_1154': ('All six noninvertible third indicators equal two, so every corresponding trivalent rotation is identity. The integral center is Vec, excluding nontrivial finite-group extensions and equivariantizations throughout the Morita class. Three further specified central-condensation families are excluded. All three necessary center patterns remain; there is no categorical model or general exclusion.',
   ['evidence/unresolved7_20261027/r8_1154/ODD_ROTATION_THEOREM.md', 'evidence/unresolved7_20261027/r8_1154/INTEGRAL_CENTER_OBSTRUCTION.md', 'evidence/unresolved7_20261027/r8_1154/HAAGERUP_PRODUCT_ROUTES.md']),
 'R8_3_1768': ('No category with GH(C6,2) fusion rules can be Morita equivalent to a categorification of this ring, for any associator or algebra. Pairing parity and the complete module list exclude the entire proposed higher-Haagerup Morita route. The twisted precursor is not a model of this ring; general categorification remains unresolved.',
   ['evidence/unresolved7_20261027/r8_1768/MORITA_QUATERNIONIC_RIGIDITY.md', 'evidence/unresolved7_20261027/r8_1768/UNIVERSAL_GH6_ROUTE_OBSTRUCTION.md']),
 'R9_2_137': ('The forced nonpointed algebra in the remaining zero-shift Morita category returns to the central-involution module category. Both TY signs still have exact feasible witnesses after all positive second-indicator constraints are imposed. These witnesses are necessary data, not categorical constructions; general categorification remains unresolved.',
   ['evidence/unresolved7_20261027/audit_parity/R137_CONTINUATION.md']),
 'R9_2_1607': ('General complex categorification is excluded. The symmetric pairing on a multiplicity-one Galois summand forces four positive large second indicators in the zero-shift Morita dual. Morita invariance of the dimension-weighted second-indicator total contradicts the source duality. The spherical and Galois reductions cover arbitrary complex categorifications.',
   ['evidence/unresolved10_20261027/r9_commutative/GALOIS_FS2_EXCLUSION.md', 'evidence/unresolved7_20261027/audit_fs2/AUDIT.md']),
 'R9_2_1975': ('General complex categorification is excluded. After the complete signed and Morita reductions, projective stabilizer parity forces even restriction multiplicities, contradicting the odd multiplicity in the distinguished Galois-unit central object. The proof covers arbitrary complex cochains and does not impose a fourth-root normalization.',
   ['evidence/unresolved10_20261027/r9_noncommutative/GALOIS_PARITY_EXCLUSION.md', 'evidence/unresolved7_20261027/audit_parity/AUDIT_R1975.md']),
 'R9_2_1976': ('General complex categorification is excluded by the same Galois-pairing and Morita-invariant second-indicator argument as R9_2_1607. The required sum of four positive large indicators contradicts the source, which has no selfdual large simples. The proof retains the general-complex spherical and Galois reductions.',
   ['evidence/unresolved10_20261027/r9_commutative/GALOIS_FS2_EXCLUSION.md', 'evidence/unresolved7_20261027/audit_fs2/AUDIT.md']),
}

def active(repo=ROOT):
 return (Path(repo)/EVIDENCE/'accepted.json').is_file()

def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def read(path): return json.loads(Path(path).read_text())
def write(path,value,compact=False):
 path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
 path.write_text(json.dumps(value,ensure_ascii=False,indent=None if compact else 2,
                            separators=(',',':') if compact else None)+'\n')

def proof(repo,path):
 p=Path(repo)/path
 if not p.is_file(): raise ValueError('Missing frontier proof: '+path)
 return {'label':Path(path).name,'path':path,'url':URL+path,'sha256':sha(p)}

def publication_matches(relative,expected,repo=ROOT):
 repo=Path(repo);p=repo/relative;r=repo/EVIDENCE/'publication_replacements.json'
 if not active(repo) or not p.is_file() or not r.is_file():return False
 data=read(r);entry=data['files'].get(relative)
 if not entry or expected not in entry['prior_sha256'] or sha(p)!=entry['after_sha256']:return False
 return all(sha(repo/n)==h for n,h in data['immutable_decisions'].items())

def current_scope(rid, scope):
 """Apply the accepted research note while preserving audited status fields."""
 from copy import deepcopy
 scope=deepcopy(scope)
 if rid=='R8_3_1768':
  text=FINDINGS[rid][0]
  scope['notes']=[n for n in scope.get('notes',[])if n!=text and 'remaining categorical gap'not in n and 'lacks the required algebra'not in n]
  scope['notes'].append(text)
 return scope

def apply_profiles(repo=ROOT):
 repo=Path(repo)
 if not active(repo):return
 ledger={r['id']:r for r in read(repo/LEDGER)}
 for name in ('unresolved_cases.json','rank9_m2.json'):
  p=repo/'site/dist/data'/name
  if not p.is_file():continue
  value=read(p)
  for row in value['cases']:
   rid=row['id']
   if rid not in FINDINGS:continue
   text,paths=FINDINGS[rid];sources=[proof(repo,n)for n in paths]
   row['summary']=text
   row['research']=[r for r in row.get('research',[])if r.get('title')!='Audited continuation: 27 October 2026']
   row['research'].insert(0,{'title':'Audited continuation: 27 October 2026','source':paths[0],
       'url':sources[0]['url'],'source_sha256':sources[0]['sha256'],
       'data':{'status':'excluded'if rid in EXCLUDED else'unresolved','findings':text,
               'scope':'General categorification decision'if rid in EXCLUDED else'Necessary restrictions and construction-route exclusions only'}})
   row['evidence']=sources+[r for r in row.get('evidence',[])if r['path']not in paths]
   scope=current_scope(rid,row['categorification_scope'])
   row['categorification_scope']=scope
   if rid in EXCLUDED:
    current=proof(repo,LEDGER)
    row.update(status='excluded',existence='excluded',source_file=LEDGER,source_url=current['url'],investigation_deferred=False)
    row['research']=[r for r in row['research']if r.get('title')!='Current accepted case decision']
    row['research'].insert(0,{'title':'Current accepted case decision','source':LEDGER,
       'url':current['url'],'source_sha256':current['sha256'],'data':ledger[rid]})
    row['evidence']=[current]+[v for v in row['evidence']if v['path']!=LEDGER]
    scope.update(general_status='excluded',level_status={k:'excluded'for k in ('general','pivotal','spherical','pseudo_unitary','unitary')},
       strongest_excluded='general',same_category_implications=[],existence_implications=[],notes=[text],audit_sources=sources,
       braided={'status':'excluded','explanation':'General complex categorification is excluded.','sources':sources})
   row['evidence']=list({v['path']:v for v in row['evidence']}.values())
  if name=='rank9_m2.json':
   s=value['summary'];s.update(date=DATE,ledger_path=LEDGER,ledger_sha256=sha(repo/LEDGER),
      ledger_url=URL+LEDGER,totals=COUNTS,counts={'9':COUNTS},remaining_ids=['R9_2_137'],frontier_continuation=EVIDENCE)
  write(p,value,compact=True)

def revise_document(name,text,repo=ROOT):
 if not active(repo):return text
 if name=='oeis/update_2026-10-02.txt':return text
 # Replace superseded current notices; leave immutable dated proof archives alone.
 text=re.sub(r'<!-- current-theoretical-retry -->.*?<!-- /current-theoretical-retry -->\s*','',text,flags=re.S)
 text=re.sub(r'<!-- current-high-rank-publication -->.*?<!-- /current-high-rank-publication -->\s*','',text,flags=re.S)
 text=re.sub(r'<!-- frontier-20261027 -->.*?<!-- /frontier-20261027 -->\s*','',text,flags=re.S)
 for a,b in [('**10 open cases.**','**7 open cases.**'),('10 unresolved rings','7 unresolved rings'),
  ('ten unresolved cases','seven unresolved cases'),('Ten cases remain','Seven cases remain'),
  ('Ten open cases','Seven open cases'),('ten open cases','seven open cases'),
  ('ten earlier open cases are unchanged','seven remaining open cases are unchanged'),
  ('ten open cases at lower ranks are unchanged','seven open cases at lower ranks remain'),
  ('10 current open tensors','7 current open tensors'),('10 present questions','7 present questions'),
  ('all 10 open tensors','all 7 open tensors'),
  ('all ten open cases','all seven open cases'),('2,145 excluded, 76 realized','2,148 excluded, 76 realized'),
  ('[4 unresolved](https://sebastienpalcoux.github.io/grothendieck-ring-classification/unresolved.html?rank=9&m=2)',
   '[1 unresolved](https://sebastienpalcoux.github.io/grothendieck-ring-classification/unresolved.html?rank=9&m=2)'),
  ('2,043 general exclusions, 36 unitary models and 4 unresolved rings','2,046 general exclusions, 36 unitary models and 1 unresolved ring')]:text=text.replace(a,b)
 # Current dates on archival banners are preserved, but they no longer present a live lead.
 text=text.replace('the actual twisted precursor for R8_3_1768 do not claim further decisions.',
   'the subsequent GH(C6,2) Morita obstruction are recorded in the 27 October continuation.')
 depth=len(Path(name).parent.parts)
 prefix='../'*depth
 banner=('<!-- frontier-20261027 -->\n**27 October 2026 · audited continuation.** '
   'R9_2_1607, R9_2_1975 and R9_2_1976 are excluded over the complex numbers. '
   '**Seven cases remain unresolved:** two at rank six, four at rank eight and one at rank nine. '
   'The conditional R1660–R941 algebra construction is precise; every GH(C6,2) Morita route for R1768 is excluded. '
   f'[Proofs, individual findings and exact replay]({prefix}{EVIDENCE}/README.md). '
   'Independent human verification remains pending.\n<!-- /frontier-20261027 -->\n\n')
 at=text.find('\n\n');return text[:at+2]+banner+text[at+2:]
