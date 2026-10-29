"""Pivotal selfduality-sign constraints on X Y X*. No positivity assumption.

This tool checks a supplied indicator assignment. The categorical existence
of a pivotal structure and the supplied signs are separate proof inputs.
"""
import hashlib,json,runpy
from pathlib import Path

def duals(N):
 r=len(N);out=[]
 for x in range(r):
  ds=[y for y in range(r) if N[x][y][0]]
  if len(ds)!=1 or N[x][ds[0]][0]!=1:raise ValueError('not a valid duality')
  out.append(ds[0])
 return out

def check(N,eps):
 r=len(N);dual=duals(N);bad=[]
 if len(eps)!=r or eps[0]!=1:raise ValueError('indicator input size/unit')
 for y in range(r):
  if (eps[y]==0)!=(dual[y]!=y):raise ValueError('sign/duality mismatch')
  if dual[y]!=y:continue
  for x in range(r):
   for z in range(r):
    if dual[z]!=z or eps[y]==eps[z]:continue
    m=sum(N[x][y][a]*N[a][dual[x]][z] for a in range(r))
    if m%2:bad.append({'conjugator':x,'object':y,'constituent':z,'multiplicity':m,'object_sign':eps[y],'constituent_sign':eps[z]})
 return bad

def components(N):
 r=len(N);dual=duals(N);p=list(range(r))
 def root(i):
  while p[i]!=i:i=p[i]
  return i
 for y in range(r):
  if dual[y]!=y:continue
  for x in range(r):
   for z in range(r):
    if dual[z]==z and sum(N[x][y][a]*N[a][dual[x]][z] for a in range(r))%2:p[root(y)]=root(z)
 return sorted([sorted(i for i in range(r) if dual[i]==i and root(i)==q) for q in set(root(i) for i in range(r) if dual[i]==i)])

if __name__=='__main__':
 P=Path(__file__).resolve().parents[2]
 T=runpy.run_path(str(P/'prior/data/current_remaining_cases.py'))['TENSORS']
 assignments={'R6_4_155':[[1,0,0,1,-1,-1]],'R6_8_1660':[[1,1,1,1,-1,1]],
  'R8_3_928':[[1,0,0,0,0,0,0,-1]],'R8_3_941':[[1,0,0,1,1,1,1,1]],
  'R8_3_1154':[[1,0,0,-1,1,1,1,1]],'R8_3_1768':[[1,-1,1,1,1,1,1,1]],
  'R9_2_137':[[1,1,1,1,1,1,1,1,e] for e in (1,-1)]}
 out=[]
 for rid,options in assignments.items():
  N=T[rid]
  out.append({'id':rid,'tensor_sha256':hashlib.sha256(json.dumps(N,separators=(',',':')).encode()).hexdigest(),
   'same_sign_components':components(N),'assignments':[{'indicators':e,'violations':check(N,e)} for e in options]})
 receipt={'scope':'conditional on the listed inherited second-indicator assignments; no new indicator derivations','cases':out}
 (Path(__file__).parent/'pivotal_conjugation_parity_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
 print(json.dumps([{'id':p['id'],'components':p['same_sign_components'],'violations':[len(a['violations']) for a in p['assignments']]} for p in out],indent=2))
