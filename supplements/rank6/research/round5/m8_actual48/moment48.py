"""Lift exact saturated-character modular moment identities to actual mu48."""
import sys,json,hashlib,time
from pathlib import Path
import actual48 as Q
sys.path.insert(0,str(Q.P/'research/round5/unification'))
import equality_modrep as E
from exact import require,evaluate
from modular_character_induction import rational_rows
import sympy as s
SOURCE=Q.P/'research/round5/unification/equality_modrep.json'

def append_rows(d,cols,labels,nv):
 C=d['C'];require(d['F']==48,'actual48 field required');V=sorted({tuple(v)for v,a in labels});ix={v:i for i,v in enumerate(V)};out=[];rhs=[];metadata=[]
 decode=lambda co:evaluate([s.Rational(x)for x in co],C.unit**2,C)
 records=[r for r in json.loads(SOURCE.read_text())if r['id']=='R6_8_1660']
 require(sorted(r['conductor']for r in records)==[12,24],'incomplete saturated character moments')
 for record in records:
  require(record['field_conductor']==24,'moment source field changed');certificate=dict(conductor=record['conductor'],lambda_value=decode(record['lambda_value']),relations=[[decode(co)for co in rel]for rel in record['relations']]);rr,bb,forbidden=E.phase_equations(d,V,cols,certificate)
  selected=[ix[tuple(v)]*48+a for v,a in labels];require(not(set(selected)&set(forbidden)),'actual labels violate moment support')
  for row,val in zip(rr,bb):
   for r,b in rational_rows([row[j]for j in selected]+[C.zero]*(nv-len(labels)),val,C):
    if any(r)or b:out.append({j:int(a)for j,a in enumerate(r)if a});rhs.append(int(b))
  metadata.append(dict(conductor=record['conductor'],identities=len(rr)))
 rr,bb,forbidden,md=E.mixed_phase_equations(d,V,cols);selected=[ix[tuple(v)]*48+a for v,a in labels];require(not(set(selected)&set(forbidden)),'actual labels violate mixed support')
 for row,val in zip(rr,bb):
  for r,b in rational_rows([row[j]for j in selected]+[C.zero]*(nv-len(labels)),val,C):
   if any(r)or b:out.append({j:int(a)for j,a in enumerate(r)if a});rhs.append(int(b))
 return out,rhs,dict(source_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),characters=metadata,mixed=md,rational_equations=len(out))

def verify_identity_source():
 R=next(r['N']for r in json.loads((Q.P/'data/census.json').read_text())if r['id']=='R6_8_1660');d=Q.M.data_for(R,3,24);pack=E.saturated_characters(d);records=[r for r in json.loads(SOURCE.read_text())if r['id']=='R6_8_1660'];computed=[dict(id='R6_8_1660',**E.encode(E.identities(d,ch)))for ch in pack['characters']];require(json.loads(json.dumps(computed))==records,'saturated moment identity source mismatch');return dict(passed=True,optimizer_used=False,identity_count=sum(len(x['relations'])for x in computed)+12,source_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest())
if __name__=='__main__':
 t=time.monotonic();r=verify_identity_source();r['seconds']=time.monotonic()-t;Path(__file__).with_name('moment_identity_replay_O.json').write_text(json.dumps(r,indent=2)+'\n');print(r,flush=True)
