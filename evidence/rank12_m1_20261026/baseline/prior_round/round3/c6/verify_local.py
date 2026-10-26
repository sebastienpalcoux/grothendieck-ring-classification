#!/usr/bin/env python3
"""Small exact checks for five unresolved quadratic rank-12 rings.

This creates no categorification or exclusion certificate for any rank-12 ring.
It records tensor bindings, conditional quotient tensors, and a surviving
central-induction necessary-condition search for R350. No online mutations.
"""
import hashlib,itertools,json,sys
from pathlib import Path
import sympy as s
import numpy as np
ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
IDS=['R12_1_332','R12_1_350','R12_1_561','R12_1_623','R12_1_628']
T=json.loads((ROOT/'rank12-m1-offline-20261025/tensors.json').read_text())
def digest(x):return hashlib.sha256(json.dumps(x,separators=(',',':')).encode()).hexdigest()
def validate(R):
 N=np.asarray(R,dtype=np.int64); n=len(R)
 assert np.array_equal(N[0],np.eye(n,dtype=int)) and np.array_equal(N[:,0],np.eye(n,dtype=int))
 assert np.all(N>=0) and int(N.max())==1
 du=N[:,:,0].argmax(axis=1).tolist()
 assert np.all(N[:,:,0].sum(axis=1)==1) and all(du[du[i]]==i for i in range(n))
 assert np.array_equal(np.einsum('ija,akl->ijkl',N,N),np.einsum('jka,ial->ijkl',N,N))
 for i,j,k in itertools.product(range(n),repeat=3):
  assert R[i][j][k]==R[du[j]][du[i]][du[k]]==R[du[i]][k][j]==R[k][du[j]][i]
 G=[i for i in range(n) if sum(R[i][du[i]])==1]
 O=[i for i in range(n) if i not in G]
 return du,G,O
bindings={}
for rid in IDS:
 R=T[rid];du,G,O=validate(R)
 mul=lambda a,b:next(i for i,x in enumerate(R[a][b]) if x)
 abelian=all(mul(a,b)==mul(b,a) for a,b in itertools.product(G,repeat=2))
 assert len(G)==len(O)==6
 assert all(len({mul(g,x) for g in G})==6 for x in O)
 b={'tensor_sha256':digest(R),'dual':du,'invertibles':G,'noninvertibles':O,'pointed_group':'C6' if abelian else 'S3','selfdual_noninvertibles':[i for i in O if du[i]==i],'all_left_stabilizers_trivial':True,'all_right_stabilizers_trivial':all(mul(x,g)!=x for x in O for g in G if g)}
 if rid!='R12_1_332':
  assert all(sum(R[x][y][k] for k in G)==1 and all(R[x][y][k]==1 for k in O) for x in O for y in O)
  b['dimension_relation']={'d^2':{'1':1,'d':6},'positive_root':'3+sqrt(10)'}
  if abelian:
   gens=[]
   for g in G:
    p=[0]
    for i in range(5):p.append(mul(p[-1],g))
    if len(set(p))==6:gens.append(p)
   pp=gens[0]; z=pp[3]
   target_z=0 if rid=='R12_1_561' else z
   rho=next(x for x in O if R[x][x][target_z])
   tau=1 if all(mul(rho,g)==mul(g,rho) for g in G) else -1
   mapping=pp+[mul(g,rho) for g in pp]
   for a,b0 in itertools.product(range(6),repeat=2):
    assert mul(mapping[6+a],mapping[b0])==mapping[6+(a+tau*b0)%6]
    unit=(a+tau*b0+(0 if target_z==0 else 3))%6
    assert R[mapping[6+a]][mapping[6+b0]][mapping[unit]]==1
   b['quadratic_coordinates']={'generator':pp[1],'rho':rho,'coordinate_to_input':mapping,'right_action_tau':tau,'rho_square_pointed_exponent':0 if target_z==0 else 3}
 else:
  b['dimension_relation']={'d^2':{'1':1,'d':3},'positive_root':'(3+sqrt(13))/2'}
 bindings[rid]=b

# Conditional C3 orbit quotients for the commutative rings. A tensor quotient
# is not a tensor functor: a central Tannakian lift is an additional hypothesis.
quotients={}
for rid in ['R12_1_561','R12_1_628']:
 R=T[rid];p=bindings[rid]['quadratic_coordinates']['coordinate_to_input'];
 q=[None]*12
 for i,x in enumerate(p):q[x]=(i%6)%2 + (2 if i>=6 else 0)
 reps=[q.index(i) for i in range(4)]
 Q=[[[sum(R[reps[i]][reps[j]][x] for x in range(12) if q[x]==k) for k in range(4)] for j in range(4)] for i in range(4)]
 for i,j,k in itertools.product(range(12),range(12),range(4)):
  assert sum(R[i][j][x] for x in range(12) if q[x]==k)==Q[q[i]][q[j]][k]
 quotients[rid]={'quotient_tensor':Q,'orbit_map':q,'additional_hypothesis':'A fully faithful central Tannakian Rep(C3) lift of the order-three pointed subgroup, with faithful forgetful image. Not established.'}

# Replay the existing rank-four theorems without importing any online status.
sys.path.insert(0,str(ROOT/'grothendieck-revision/supplements/rank4/software'))
from applications import diagonal_recognizer,check_diagonal
from induction import pseudo_certificate,check_pseudo
from rings import validate as validate4
for rid,rec in quotients.items():
 Q=rec['quotient_tensor'];validate4(Q)
 if rid=='R12_1_561':
  c=diagonal_recognizer(Q);assert c;check_diagonal(Q,c)
 else:
  c=pseudo_certificate(Q);assert c;check_pseudo(Q,c)
 rec['exact_rank4_exclusion_certificate']=c
 rec['rank12_status']='unresolved; central lift not forced'

# Exact reduced low-induction screen for R350.
R=T['R12_1_350'];N=list(map(s.Matrix,R));du=bindings['R12_1_350']['dual'];B=s.Matrix(12,12,lambda j,i:sum(R[a][j][k]*R[k][du[a]][i] for a in range(12) for k in range(12)));assert B==B.T;classes=[[3,4],[6,7,9],[11]]
cs=lambda m:[v for v in itertools.product(range(m+1),repeat=3) if 2*v[0]+3*v[1]+v[2]==m]
def vec(a,u):
 v=[0]*12;v[0]=u
 for cl,t in zip(classes,a):
  for j in cl:v[j]=t
 return s.Matrix(v)
def psd_witness(Q):
 M=Q.copy();V=s.eye(len(Q.row(0)));pivots=[]
 while M.rows:
  for i in range(M.rows):
   if M[i,i]<0:return {'psd':False,'vector':[str(x) for x in V[:,i]],'value':str(M[i,i])}
  p=next((i for i in range(M.rows) if M[i,i]>0),None)
  if p is None:
   pair=next(((i,j) for i in range(M.rows) for j in range(i) if M[i,j]),None)
   if pair:
    i,j=pair;v=V[:,i]-s.sign(M[i,j])*V[:,j]
    return {'psd':False,'vector':[str(x) for x in v],'value':str((v.T*Q*v)[0])}
   return {'psd':True,'positive_pivots':[str(x) for x in pivots],'nullity':M.rows}
  # A zero diagonal row with nonzero entry is already a 2x2 obstruction.
  for i in range(M.rows):
   if M[i,i]==0:
    j=next((j for j in range(M.rows) if M[i,j]),None)
    if j is not None:
     a=-M[i,j]/(M[j,j]+1);v=V[:,i]+a*V[:,j]
     return {'psd':False,'vector':[str(x) for x in v],'value':str((v.T*Q*v)[0])}
  rest=[j for j in range(M.rows) if j!=p];pivot=M[p,p];pivots.append(pivot)
  V=s.Matrix.hstack(*(V[:,j]-M[p,j]/pivot*V[:,p] for j in rest)) if rest else s.zeros(12,0)
  M=M.extract(rest,rest)-M.extract(rest,[p])*M.extract([p],rest)/pivot
 return {'psd':True,'positive_pivots':[str(x) for x in pivots],'nullity':0}
branches=[]
for a,b,c,e,f in itertools.product(cs(6),cs(3),cs(3),cs(6),cs(6)):
 if any(a[i]+b[i]+c[i]+2*e[i]+2*f[i]!=6 for i in range(3)):continue
 L=s.Matrix.hstack(s.eye(12)[:,0],vec(a,1),vec(b,1),vec(c,1),vec(e,2),vec(f,2));Q=B-L*L.T;w=psd_witness(Q)
 if not w['psd']:
  v=s.Matrix([s.Rational(x) for x in w['vector']]);assert (v.T*Q*v)[0]<0
 branches.append({'column_class_coefficients':[a,b,c,e,f],**w})
assert len(branches)==30
survivors=sum(x['psd'] for x in branches)
(OUT/'tensor_bindings.json').write_text(json.dumps(bindings,indent=2)+'\n')
(OUT/'conditional_quotients.json').write_text(json.dumps(quotients,indent=2)+'\n')
(OUT/'R350_induction_low_exact.json').write_text(json.dumps({'conjugation_classes':classes,'formal_rep_dimensions':[1,1,1,1,2,2],'central_dimensions':['1','d^2','1+3d','1+3d','2+6d','2+6d'],'branches':branches,'surviving_branches':survivors,'rank12_status':'not_decided_by_low_gram_test'},indent=2)+'\n')
print(json.dumps({'tensor_bindings':len(bindings),'conditional_rank4_certificates_replayed':len(quotients),'R350_low_branches':len(branches),'R350_remaining_low_branches':survivors,'standalone_structural_checks_only':True}))
