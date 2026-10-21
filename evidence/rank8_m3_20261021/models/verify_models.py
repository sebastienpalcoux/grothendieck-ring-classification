#!/usr/bin/env python3
"""Reconstruct the positive models and verify every source tensor coefficient.

This recovery verifier rebuilds evidence from independent constructors; it
does not reuse memorized PASS receipts. All validation uses explicit guards.
"""
from pathlib import Path
import argparse,hashlib,itertools,json,sys
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path.insert(0,str(HERE));sys.path.insert(0,str(ROOT/'supplements/rank8/software'))
from model_constructors import all_models,require
from prepare import key

def fp(R):return hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest()
def axioms(R):
 n=len(R);require(n==8,'rank8');require(all(isinstance(v,int)and v>=0 for M in R for row in M for v in row),'nonnegative integral tensor')
 require(all(R[0][i]==R[i][0]==[int(i==j)for j in range(n)]for i in range(n)),'unit')
 du=[next(j for j in range(n)if R[i][j][0])for i in range(n)]
 require(all(R[i][j][0]==int(j==du[i])for i,j in itertools.product(range(n),repeat=2)),'duality')
 require(all(R[i][j][k]==R[du[j]][du[i]][du[k]]==R[du[i]][k][j]for i,j,k in itertools.product(range(n),repeat=3)),'reciprocity')
 require(all(sum(R[i][j][a]*R[a][k][b]for a in range(n))==sum(R[j][k][a]*R[i][a][b]for a in range(n))for i,j,k,b in itertools.product(range(n),repeat=4)),'associativity')
 require(max(v for M in R for row in M for v in row)==3,'exact multiplicity3')

def verify(include_external=True):
 source={r['id']:r for r in json.loads((HERE.parent/'pipeline/census_m3.json').read_text())};out=[]
 def add(ident,name,R,ref,construction,certificate):
  ident='R8_3_'+str(ident)if isinstance(ident,int)else ident;src=source[ident];axioms(R)
  require(fp(src['tensor'])==src['tensor_sha256'],'source SHA')
  a,ps=key(src['tensor'],True);b,pm=key(R,True);require(a==b,'based tensor mismatch '+ident)
  p=[None]*8
  for i,j in zip(ps,pm):p[i]=j
  require(p[0]==0 and sorted(p)==list(range(8)),'basis map')
  require(all(src['tensor'][i][j][k]==R[p[i]][p[j]][p[k]]for i,j,k in itertools.product(range(8),repeat=3)),'all512 coefficients')
  out.append(dict(id=ident,multiplicity=3,status='unitarily_realized',model=name,tensor_sha256=src['tensor_sha256'],tensor=src['tensor'],source_certificate=certificate,model_scope='unitary',unitary='yes',pseudo_unitary='yes',constructors=[dict(model=name,reference=ref,tensor=R,basis_map_source_to_model=p,construction=construction)]))
 for ident,name,R,ref,extra in all_models():add(ident,name,R,ref,extra,'evidence/rank8_m3_20261021/models/model_constructors.py')
 if include_external:
  sys.path.insert(0,str(HERE/'psl2_11/r360'))
  from verify_a6_twist import local_relative_cocycle,stable_elements,model_tensor
  omega,local=local_relative_cocycle();stability=stable_elements(omega);R,model=model_tensor()
  cert=json.loads((HERE/'psl2_11/r360/certificate.json').read_text())
  require(json.loads(json.dumps(local))==cert['local_relative_cocycle'],'A6 local cocycle')
  require(json.loads(json.dumps(stability))==cert['global_stable_element_verification'],'A6 all360 stability witnesses')
  require(model==cert['constructed_fusion_tensor'],'A6 tensor')
  add(3342,'Twisted group-theoretical C(A6,omega,A5,psi) from a stable relative mu2 class',R,'Cartan–Eilenberg stable-elements theorem; Gelaki–Naidu arXiv:0709.4326 §5.1; exact local cocycle and tensor derivation.',dict(kind='twisted finite-group bimodules',proof='evidence/rank8_m3_20261021/models/psl2_11/r360/proof.md',cocycle='Explicit SylowD8 cocycle and360 stable-element witnesses; global class existence, not global cochain table',human_review='New derivation independently reviewed during this investigation; further specialist review appropriate.'),'evidence/rank8_m3_20261021/models/psl2_11/r360/certificate.json')
  # The finite-group constructor is recovered independently by its owner.
  sys.path.insert(0,str(HERE/'psl2_11'))
  from verify_psl2_11 import reconstructed_model
  c=reconstructed_model()
  add(724,c['model'],c['tensor'],c['reference'],c.get('construction',{}),'evidence/rank8_m3_20261021/models/psl2_11/certificate.json')
 out.sort(key=lambda r:int(r['id'].split('_')[-1]));require(len(out)==(14 if include_external else 12),'model count')
 return json.loads(json.dumps(out))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');p.add_argument('--core-only',action='store_true');a=p.parse_args();out=verify(not a.core_only)
 if a.core_only:require(not a.write,'core-only mode cannot publish an incomplete manifest')
 elif a.write:(HERE/'consolidated_models.json').write_text(json.dumps(out,indent=2)+'\n')
 else:require(out==json.loads((HERE/'consolidated_models.json').read_text()),'manifest differs')
 print('PASS:',len(out),'independent unitary models;',512*len(out),'source coefficients freshly verified.')
