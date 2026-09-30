#!/usr/bin/env python3
"""Complete, optimizer-disabled exact exclusion of R6_5_1204.

First replay the general-to-pseudo-unitary reduction and complete 171-profile
frontier, checking its cached columns and counts against the reconstruction.
Then exclude 72 profiles structurally and 99 by integral rotation counts.
"""
from pathlib import Path
import json,sys,time,importlib.util
import scipy.optimize

def forbidden_optimizer(*args,**kwargs):
 raise RuntimeError("Numerical optimizer is forbidden during exact verification")
scipy.optimize.linprog=forbidden_optimizer
scipy.optimize.milp=forbidden_optimizer
PROOF=Path(__file__).resolve().parent
P=PROOF.parents[2]
sys.path.insert(0,str(P/'software'))
spec=importlib.util.spec_from_file_location('_r6_5_1204_trace_system',PROOF/'trace_system.py')
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
System=module.System

def require(condition,message):
 if not condition:raise ValueError(message)

def augment(A,b,cuts):
 n=len(A[0]);k=len(cuts)
 AA=[r+[0]*k for r in A];bb=b[:]
 for t,(j,op,v) in enumerate(cuts):
  require(type(j) is int and 0<=j<n and op in ('upper','lower') and type(v) is int,'Invalid bound')
  row=[0]*(n+k);row[j]=1 if op=='upper' else -1;row[n+t]=1
  AA.append(row);bb.append(v if op=='upper' else -v)
 return AA,bb

def check(A,b,ray):
 require(isinstance(ray,list) and ray,'Empty or malformed ray')
 ix=[i for i,v in ray];require(len(set(ix))==len(ix),'Duplicate ray index')
 require(all(type(i) is int and 0<=i<len(b) and type(v) is int and v!=0 for i,v in ray),'Invalid ray entry')
 require(sum(b[i]*v for i,v in ray)<0,'Ray does not contradict right side')
 require(all(sum(A[i][j]*v for i,v in ray)>=0 for j in range(len(A[0]))),'Ray has negative column pairing')

def verify(S,q):
 require(q['height']==S.height,'Height mismatch')
 A,b,labs=S.profile(q['profile']);cuts=[]
 require(all(type(v) is int for row in A for v in row) and all(type(v) is int for v in b),'System not exact integral')
 for c in q['cuts']:
  j,op,v=c['bound'];require(type(j) is int and 0<=j<len(labs),'Invalid original-variable index')
  require(tuple(c['label'])==labs[j],'Variable label mismatch')
  opposite=(j,'lower',v+1) if op=='upper' else (j,'upper',v-1)
  AA,bb=augment(A,b,cuts+[opposite]);check(AA,bb,c['ray']);cuts.append(c['bound'])
 AA,bb=augment(A,b,cuts);check(AA,bb,q['final_ray'])

def verify_forced_W(R):
 r=next(x for x in json.load(open(P/'data/census.json')) if x['id']=='R6_5_1204')
 require(R==r['N'],'Supplied tensor differs from canonical census input')
 p=json.load(open(P/'research/round5/m5_1204/remaining_profiles.json'))
 N=r['N'];lows=p['low_columns'];high=p['high_columns'];U=[0,1,1,0,0,0]
 require(r['dual']==list(range(6)),'Non-self-dual input')
 ui=high.index(U[1:]);wi=high.index([0,0,0,1,0])
 prod=[sum(U[i]*U[j]*N[i][j][k] for i in range(6) for j in range(6)) for k in range(6)]
 require(prod==[2,2,2,2,4,4],'Unexpected U square')
 prod[0]-=1
 admissible=[c for c in lows[1:] if all(x<=y for x,y in zip(c,prod))]
 require(admissible==[[1,1,1,1,2,2]]*3,'Unexpected nonunit low summand')
 residual=[a-b for a,b in zip(prod,admissible[0])]
 require(residual[4]-residual[3]==1,'Residual functional not positive')
 excluded=[];remaining=[]
 for q in p['profiles']:
  m=dict(q['multiplicities'])
  require(m.get(ui)==1,'U is not unique')
  require(all(high[i][3]<=high[i][2] for i in m if i!=wi),'Wrong high-column functional sign')
  (remaining if m.get(wi) else excluded).append(q['profile_index'])
 require(len(excluded)==72 and len(remaining)==99,'Wrong structural partition sizes')
 require(len(set(excluded+remaining))==171,'Repeated profile identifiers')
 old=json.loads(Path(__file__).with_name('forced_W.json').read_text())
 require(excluded==old['excluded_profiles'] and remaining==old['remaining_profiles'],'Stored structural partition mismatch')
 return set(excluded),set(remaining)

def verify_exclusion(R=None,progress=print):
 st=time.monotonic()
 if R is None:
  R=next(x['N'] for x in json.load(open(P/'data/census.json')) if x['id']=='R6_5_1204')
 import round5_1204
 inherited_path=P/'research/round5/m5_1204'
 frontier=json.load(open(inherited_path/'remaining_profiles.json'))
 inherited=round5_1204.verify(R,json.load(open(inherited_path/'profile_certificate.json')),
                            progress=progress,frontier=frontier)
 excluded,remaining=verify_forced_W(R)
 certificates=json.load(open(PROOF/'exact_trace_h6.json'))
 require(len(certificates)==99,'Wrong certificate count')
 S=System(6,R=R);covered=[];steps=0
 for q in certificates:
  require(bool(q.get('final_ray')),'Incomplete trace certificate')
  verify(S,q);covered.append(q['profile']);steps+=len(q['cuts'])
 require(set(covered)==remaining and len(covered)==len(remaining)==99,'Incomplete or duplicated profile coverage')
 require(len(excluded|set(covered))==171,'Incomplete inherited frontier coverage')
 require(all(c['label'][0]=='rotation' for q in certificates for c in q['cuts']),
         'Unexpected non-rotation integer bound')
 result=dict(passed=True,id='R6_5_1204',scope='general',outcome='not_categorifiable',
             optimizer_used=False,inherited_reduction=inherited,
             structural_profiles=len(excluded),trace_profiles=len(covered),
             integer_rotation_bounds=steps,exact_farkas_rays=steps+len(covered),
             seconds=time.monotonic()-st)
 progress('Exactly excluded 72 structural and 99 trace profiles')
 return result

if __name__=='__main__':
 print(json.dumps(verify_exclusion(),indent=2))
