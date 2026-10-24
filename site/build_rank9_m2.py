#!/usr/bin/env python3
"""Publish the audited exact-M2 rank-nine band in the shared Atlas schema.

The accepted mathematical ledger is immutable input. This builder validates
identities and model transports; it does not infer categorifiability.
"""
from collections import Counter
import ast,hashlib,json,re,shutil,sys
from pathlib import Path
import numpy as np
import sympy as s
from build_realized import tensor_checks
ROOT=Path(__file__).resolve().parents[1];DIST=ROOT/'site/dist';REL='evidence/rank9_m2_20261024';E=ROOT/REL
URL='https://github.com/sebastienpalcoux/grothendieck-ring-classification'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def write(p,x,compact=False):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=None if compact else 2,separators=(',',':')if compact else None)+'\n')
def safe(x):
 if type(x)is int and abs(x)>2**53-1:return str(x)
 if isinstance(x,dict):return{k:safe(v)for k,v in x.items()}
 if isinstance(x,list):return list(map(safe,x))
 return x

def build():
 ledger=read(E/'ledger.json');tensors=read(E/'tensors.json');meta={r['id']:r for r in read(E/'input_metadata.json')};models={r['id']:r for r in read(E/'models.json')};unresolved={r['id']:r for r in read(E/'unresolved.json')}
 assert len(ledger)==len(tensors)==len(meta)==2083
 counts=dict(Counter(r['status']for r in ledger));assert counts=={'excluded':2043,'unitarily_realized':36,'unresolved':4}
 frozen=['rank9_rank10_m1.json','rank11_m1.json','atlas.json','classification_status.json','realized_rings.json','unresolved_cases.json','resolved_cases.json']
 before={n:digest(DIST/'data'/n)for n in frozen}
 def evidence(name,label=None):
  p=E/name;assert p.is_file(),name
  return{'label':label or name,'path':REL+'/'+name,'url':URL+'/blob/main/'+REL+'/'+name,'sha256':digest(p)}
 ledger_src=evidence('ledger.json','Current accepted decisions');archive=evidence('replay.zip','Complete exact proofs and replay archive');audit=evidence('proofs/phase5/REPORT.md','Current audited theoretical classification report')
 def proof(name):
  p='proofs/'+name
  return evidence(p)if(E/p).is_file()else archive
 out=[];z=s.Symbol('t');folder=DIST/'downloads/fusion-tensors';folder.mkdir(parents=True,exist_ok=True)
 for row in ledger:
  rid=row['id'];T=tensors[rid];m=meta[rid];a,dual=tensor_checks(T)
  h=hashlib.sha256(json.dumps(T,separators=(',',':')).encode()).hexdigest()
  assert h==row['tensor_sha256']==m['tensor_sha256'] and len(T)==9 and int(a.max())==2 and dual==m['dual']
  model=models.get(rid);assert bool(model)==(row['status']=='unitarily_realized')
  if model:
   p=model['basis_map_source_to_model'];N=model['tensor'];assert sorted(p)==list(range(9))and p[0]==0
   assert all(T[i][j][k]==N[p[i]][p[j]][p[k]]for i in range(9)for j in range(9)for k in range(9))
  txt=json.dumps(T,indent=2)+'\n';assert ast.literal_eval(txt)==T;(folder/(rid+'.txt')).write_text(txt)
  C=sum((a[i]@a[dual[i]]for i in range(9)),np.zeros((9,9),dtype=np.int64));poly=str(s.factor(s.Matrix(C.tolist()).charpoly(z).as_expr()))
  inv={'dual_indices':dual,'invertible_indices':m['invertibles'],'commutative':m['commutative'],'frobenius_perron_dimensions_approx':m['dimensions_approx'],'global_fp_dimension_approx':m['global_dimension_approx'],'central_casimir_polynomial':poly,'dimensions_method':'FP dimensions are approximate; exact algebraic invariants and character certificates are in the proof archive.','character_method':'Exact characters and formal codegrees: hash-bound replay archive.','proper_fusion_subrings':m['subrings'],'original_physical_line':m['physical_line']}
  if row['commutative']:inv['formal_codegree_polynomial']=poly
  sources=[ledger_src,audit,archive];notes=[]
  if model:
   summary='A unitary model is recorded: '+model['model']+'. All 729 source coefficients match under the recorded basis permutation.'
   for k in ('proof','independent_audit'):
    if isinstance(model.get(k),str):sources.append(proof(model[k]))
   research=[{'title':'Categorical model and exact basis transport','data':{'model':model['model'],'basis_map_source_to_model':model['basis_map_source_to_model'],'tensor_sha256':h}}]
  elif row['status']=='excluded':
   summary='General complex fusion categorification is excluded by the recorded theoretical argument and exact certificate.'
   research=[{'title':'Accepted exclusion receipts','data':row['exclusion_certificates']}]
   for c in row['exclusion_certificates']:
    for k in ('proof','independent_audit','alternative_theoretical_proof','alternative_independent_audit'):
     if isinstance(c.get(k),str):sources.append(proof(c[k]))
   if row.get('withdrawn_claims'):
    notes.append('An unsupported half-E6 subring claim was withdrawn. The current exclusion uses a different valid proof.')
  else:
   p=unresolved[rid];summary='General categorification remains unresolved. Completed restrictions and bounded searches supply no accepted model or nonexistence proof.'
   research=[{'title':'Exact invariants, restrictions and remaining scope','data':p}]
   for path in p.get('phase3_attempt_records',[])+[p.get('phase4_research_report',''),p.get('phase5_research_report','')]:
    if path.endswith('.md'):sources.append(proof(path))
   notes.append('Passing necessary conditions or reaching a search time limit is not a categorification decision.')
  sources=list({x['path']:x for x in sources}.values())
  level='realized'if model else row['status'];scope={'general_status':level,'level_status':{k:level for k in ('general','pivotal','spherical','pseudo_unitary','unitary')},'strongest_excluded':'general'if level=='excluded'else None,'same_category_implications':[],'existence_implications':[],'notes':notes,'audit_sources':sources}
  if row['status']=='unresolved':
   gate=unresolved[rid]['general_to_PU_gate']
   if gate=='weak_integrality':
    scope['same_category_implications']=[{'from':'general','to':'pseudo_unitary','label':'Every hypothetical categorification is pseudo-unitary','explanation':'Its integral global Frobenius-Perron dimension gives weak integrality. The canonical positive spherical structure exists on the same category.','sources':[ledger_src,audit]}]
   else:
    scope['existence_implications']=[{'from':'general','to':'pseudo_unitary','label':'General existence implies pseudo-unitary existence','mechanism':'Audited signed-sphericalization and Galois dimension reduction','explanation':'A hypothetical categorification gives a pseudo-unitary Galois conjugate of the same based ring. This does not assert that the original category is pseudo-unitary.','sources':[ledger_src,audit,archive]}]
  if row['status']=='excluded':
   scope['braided']={'status':'excluded','explanation':'The general complex nonexistence theorem also excludes braided categorification.','sources':[ledger_src,audit]}
  elif not row['commutative']:
   i,j,k=next((i,j,k)for i in range(9)for j in range(9)for k in range(9)if T[i][j][k]!=T[j][i][k])
   scope['braided']={'status':'excluded','explanation':'A braiding would make the Grothendieck ring commutative; the recorded source products do not commute.','obstruction':'noncommutative','noncommutativity_witness':{'i':i,'j':j,'k':k,'N_ij_k':T[i][j][k],'N_ji_k':T[j][i][k]},'sources':[ledger_src]}
  elif row['status']=='unresolved':
   braided_proof=proof('phase4/quadratic_comm/BRAIDED_OBSTRUCTION.md')
   if not any(x['path']==braided_proof['path']for x in sources):sources.append(braided_proof)
   scope['braided']={'status':'excluded','explanation':'The audited TY/pointed-subcategory argument excludes braided categorification. General unbraided existence remains unresolved.','sources':[ledger_src,braided_proof]}
  if row['status']=='unresolved':
   scope['notes'].append('The three commutative sources reduce to two common necessary D8 Morita types. A based-ring completion is not a categorical model; see the current proof reports.')
  record={'id':rid,'rank':9,'multiplicity':2,'status':row['status'],'name':model['model']if model else rid,'summary':summary,'existence':'unitary'if model else row['status'],'model_reference':model.get('proof','Exact audited categorical construction in the replay archive')if model else'','model_reference_url':ledger_src['url'],'source_file':ledger_src['path'],'source_url':ledger_src['url'],'source_location':rid,'report_url':'./papers/rank9-m2.pdf','report_label':'Rank-nine multiplicity-two manuscript','case_url':'./case.html?id='+rid,'fusion_tensor':T,'tensor_sha256':h,'basis':['X'+str(i)for i in range(9)],'unit_index':0,'tensor_convention':'Source basis; zero-based indices; X_0=1. N[i][j][k] is the coefficient of X_k in X_i*X_j.','hash_convention':'SHA-256 of compact UTF-8 JSON; no trailing newline.','invariants':inv,'research':[{'title':'Current accepted case decision','source':ledger_src['path'],'url':ledger_src['url'],'source_sha256':ledger_src['sha256'],'data':row}]+research,'evidence':sources,'categorification_scope':scope,'download_url':'./downloads/fusion-tensors/'+rid+'.txt','investigation_deferred':False}
  out.append(safe(record))
 summary={'date':'2026-10-24','rank':9,'multiplicity':2,'release':REL,'input_count':2083,'counts':{'9':counts},'totals':counts,'ledger_sha256':digest(E/'ledger.json'),'ledger_url':ledger_src['url'],'source_url':URL+'/tree/main/'+REL,'report_url':'./papers/rank9-m2.pdf','report_title':'Rank-nine fusion rings of multiplicity two','report_source':'publications/rank9-m2/paper/rank9-m2.tex','remaining_ids':[r['id']for r in ledger if r['status']=='unresolved'],'archive':{'url':archive['url'].replace('/blob/','/raw/'),'sha256':archive['sha256'],'bytes':(E/'replay.zip').stat().st_size},'enumeration_qualification':'Producer-reported complete enumeration; independent exact tensor and uniqueness checks; full enumeration not independently rerun.'}
 write(DIST/'data/rank9_m2.json',{'schema':'ring-atlas/rank9-m2/v1','summary':summary,'cases':out},True)
 write(DIST/'data/rank9_m2_build.json',{'records':2083,'counts':counts,'ledger_sha256':summary['ledger_sha256'],'tensor_downloads':2083,'legacy_sha256':before})
 for n,h in before.items():assert digest(DIST/'data'/n)==h,n
 shutil.copy2(ROOT/'publications/rank9-m2/paper/rank9-m2.pdf',DIST/'papers/rank9-m2.pdf')
 print('Built 2083 shared case profiles; 2043 exclusions,36 unitary models,4 unresolved; all earlier datasets unchanged.')
if __name__=='__main__':build()
