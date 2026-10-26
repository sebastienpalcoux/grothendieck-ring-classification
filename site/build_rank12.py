#!/usr/bin/env python3
"""Integrate the complete rank-twelve ledger into the shared Atlas catalogue."""
from pathlib import Path
import collections,hashlib,json,re
import numpy as np
import sympy as sp
from build_realized import tensor_checks
from build_rank9_10 import CONVENTION,REPO_URL,sha,write_json

ROOT=Path(__file__).resolve().parents[1];DIST=ROOT/'site/dist'
RELEASE='evidence/rank12_m1_20261026';E=ROOT/RELEASE
FIRST=E/'baseline/prior_round/prior_round/evidence/rank12-m1-offline-20261025'

def safe(value):
 if type(value)is int and abs(value)>2**53-1:return str(value)
 if isinstance(value,dict):return {k:safe(v)for k,v in value.items()}
 if isinstance(value,list):return [safe(v)for v in value]
 return value

def build():
 ledger=json.loads((E/'ledger.json').read_text())
 tensors=json.loads((FIRST/'tensors.json').read_text())
 stages=[E,E/'baseline',E/'baseline/prior_round',E/'baseline/prior_round/prior_round']
 decisions=[json.loads((p/'new_decisions.json').read_text())for p in stages]
 profiles=[];index={}
 feudal=json.loads((FIRST/'feudal.json').read_text())['records']
 def ev(path,label=None):
  path=path.resolve()
  if not path.is_relative_to(E.resolve())or not path.is_file():raise ValueError('Evidence path: '+str(path))
  rel=path.relative_to(ROOT).as_posix()
  if rel not in index:index[rel]=dict(label=label or path.name,path=rel,url=f'{REPO_URL}/blob/main/{rel}',sha256=sha(path))
  return index[rel]
 models_first={}
 for file in FIRST.glob('*models*.json'):
  content=json.loads(file.read_text())
  if isinstance(content,list):
   for entry in content:
    if isinstance(entry,dict) and 'id' in entry:models_first.setdefault(entry['id'],entry)
 for entry in feudal:
  if entry.get('model'):models_first.setdefault(entry['id'],dict(id=entry['id'],model=entry['model'],source='feudal.json'))
 for row in ledger['records']:
  rid=row['id'];T=tensors[rid];a,dual=tensor_checks(T)
  h=hashlib.sha256(json.dumps(T,separators=(',',':')).encode()).hexdigest()
  if h!=row['tensor_sha256']or len(T)!=12 or int(a.max())!=1:raise ValueError('Input binding: '+rid)
  negative=row['status']=='excluded';unitary=row['status']=='unitarily_realized'
  accepted=None;stage=None;paths=[]
  for p,d in zip(stages,decisions):
   family='exclusions' if negative else 'models'
   if rid in d[family]:accepted=d[family][rid];stage=p;break
  if accepted is None:
   accepted=row['exclusion_evidence'] if negative else models_first[rid]
   stage=FIRST
  def links(obj):
   if isinstance(obj,dict):
    for key,value in obj.items():
     if key in ('proof','replay','independent_audit','independent_replay','central_lift_proof','evidence_source','source')and isinstance(value,str):
      value=value.split(':',1)[0]
      trials=[stage/value,stage/'evidence/rank12-m1-round2-20261025'/value]
      for p in trials:
       if p.is_file():paths.append(p);break
     elif key not in ('model_tensor','fusion_tensor','parameters','certificate'):links(value)
   elif isinstance(obj,list):
    for value in obj:links(value)
  links(accepted)
  proof_paths=[stage/'new_decisions.json'] if (stage/'new_decisions.json').exists() else []
  if stage==FIRST:proof_paths.append(FIRST/'report.pdf')
  elif (stage/'report.pdf').is_file():proof_paths.append(stage/'report.pdf')
  paths=proof_paths+paths
  source=ev(E/'ledger.json','Accepted classification ledger')
  evidence=[source,ev(E/'README.md','Proof archive and replay guide')]
  evidence += [ev(p)for p in dict.fromkeys(paths) if p.resolve()!=(E/'ledger.json').resolve()]
  # A sparse positive Perron vector of the sum of fusion matrices suffices to
  # display approximate dimensions. Exact structural flags are built separately.
  vals,vecs=np.linalg.eig(a.sum(axis=0).astype(float))
  j=int(np.argmax(vals.real));v=np.abs(vecs[:,j].real);v=v/v[0]
  dims=[float((a[i]@v)[0]/v[0]) for i in range(12)]
  inv=[i for i in range(12)if sum(T[i][dual[i]])==1]
  name=row['model_name']or rid
  name=name.replace('$','').replace('\\times','×').replace('\\rtimes','⋊').replace('\\Rep','Rep').replace('\\','').replace('{','').replace('}','')
  if negative:
   description='Excluded from fusion categorification over ℂ by '+row['exclusion_route'].replace('_',' ')+'. The argument applies to general complex fusion categories.'
  elif unitary:
   description='A unitary realization exists: '+name+'. The categorical construction and complete tensor identification are recorded in the accepted proof archive.'
  else:
   description='A complex and pseudo-unitary realization exists by central C6 condensation of the algebraic C36+36 near-group category. Unitarity is not established.'
  levels={k:('excluded'if negative else'realized')for k in ('general','pivotal','spherical','pseudo_unitary','unitary')}
  if not negative and not unitary:levels['unitary']='unresolved'
  scope=dict(general_status='excluded'if negative else'realized',level_status=levels,
   strongest_excluded='general'if negative else None,same_category_implications=[],existence_implications=[],notes=[description],audit_sources=[source])
  if negative or not row['commutative']:
   scope['braided']=dict(status='excluded',explanation='General nonexistence excludes braided categorification.'if negative else'Noncommutative fusion rules exclude braided categorification.',sources=[source])
  elif row['model_constructor'] in ('su2','dihedral_rep','rep_cyclic_semidirect_inversion','odd_metaplectic','half_even_metaplectic') or len(inv)==12:
   scope['braided']=dict(status='realized',explanation='The recorded classical quantum-group, representation, or abelian pointed construction provides a braided realization. This is an existence statement, not a statement about every associator.',sources=[source])
  profile=dict(id=rid,rank=12,multiplicity=1,status=row['status'],summary=description,name=name,
   existence='excluded'if negative else'unitary'if unitary else'pseudo-unitary',
   model_reference=description,model_reference_url=source['url'],source_file=source['path'],source_url=source['url'],source_location=rid,
   report_url='./papers/rank12.pdf',report_label='Rank-twelve classification manuscript',case_url='./case.html?id='+rid,
   fusion_tensor=T,tensor_sha256=h,basis=['X'+str(i)for i in range(12)],unit_index=0,tensor_convention=CONVENTION,
   hash_convention='SHA-256 of UTF-8 compact JSON without a trailing newline.',
   invariants=dict(dual_indices=dual,invertible_indices=inv,commutative=row['commutative'],
    frobenius_perron_dimensions_approx=dims,global_fp_dimension_approx=float(sum(d*d for d in dims)),
    dimensions_method='Approximate Perron eigenvalues for display; exact integrality and structural flags are independently certified.',
    character_method='Exact character and formal-codegree certificates are retained in the source-bound proof archive.'),
   research=[dict(title='Current accepted case decision',source=source['path'],url=source['url'],source_sha256=source['sha256'],data=row),
             dict(title='Categorical construction and exact certificate'if not negative else'General complex exclusion certificate',
                  source=stage.relative_to(ROOT).as_posix(),url=REPO_URL+'/tree/main/'+stage.relative_to(ROOT).as_posix(),data=accepted)],
   evidence=evidence,categorification_scope=scope,download_url='./downloads/fusion-tensors/'+rid+'.txt',investigation_deferred=False)
  omega=sum((sp.Matrix((a[i]@a[dual[i]]).tolist())for i in range(12)),sp.zeros(12))
  poly=str(sp.factor(omega.charpoly(sp.Symbol('t')).as_expr()))
  profile['invariants']['central_casimir_polynomial']=poly
  if row['commutative']:profile['invariants']['formal_codegree_polynomial']=poly
  profiles.append(safe(profile))
  (DIST/'downloads/fusion-tensors'/(rid+'.txt')).write_text(json.dumps(T,indent=2)+'\n')
 counts=dict(collections.Counter(r['status']for r in profiles))
 if counts!={'unitarily_realized':151,'excluded':480,'pseudo_unitarily_realized':1}:raise ValueError('Final partition')
 summary=dict(date='2026-10-26',multiplicity=1,release=RELEASE,input_count=632,counts={'12':counts},totals=counts,
  ledger_sha256=sha(E/'ledger.json'),ledger_url=f'{REPO_URL}/blob/main/{RELEASE}/ledger.json',source_url=f'{REPO_URL}/tree/main/{RELEASE}',
  report_url='./papers/rank12.pdf',report_title='Rank twelve, multiplicity one: complex categorification',report_source='publications/rank12/paper/rank12.tex',remaining_ids=[],
  census_url='https://github.com/sebastienpalcoux/fusion-ring-census/tree/main/verification/rank12',
  enumeration_qualification='Producer-reported complete enumeration; exact tensor and based-isomorphism checks; full search not independently repeated.',
  current_documents=dict(path='data/current_publication_revision.json',sha256=sha(ROOT/'data/current_publication_revision.json'),date='2026-10-26'))
 archive=DIST/'downloads/Rank12_M1_Completion_Evidence.zip'
 summary['archive']=dict(url='./downloads/'+archive.name,sha256=sha(archive),bytes=archive.stat().st_size)
 write_json(DIST/'data/rank12_m1.json',dict(schema='ring-atlas/rank12-m1/v1',summary=summary,cases=profiles))
 write_json(DIST/'data/rank12_m1_build.json',dict(records=632,counts=counts,ledger_sha256=sha(E/'ledger.json'),tensor_downloads=632,
  model_scope='151 unitary; one additional complex/pseudo-unitary realization with unitarity unproved; 480 general exclusions.'))
 print('Rank twelve: 632 shared-catalogue records, 480 general exclusions, 151 unitary models and one pseudo-unitary model.')

if __name__=='__main__':build()
