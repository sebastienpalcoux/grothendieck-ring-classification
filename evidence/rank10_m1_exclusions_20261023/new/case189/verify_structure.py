#!/usr/bin/env python3
"""Exact standard-library checks of structural facts; no classification claim."""
from fractions import Fraction as Q
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[2]
c=next(c for c in json.loads((ROOT/'catalogue.json').read_text())['cases'] if c['id']=='R10_1_189')
N=c['fusion_tensor'];perm=[0,1,8,7,2,9,4,6,5,3]
M=[[[N[perm[i]][perm[j]][perm[k]] for k in range(10)] for j in range(10)] for i in range(10)]
for i in range(10):
 for j in range(10):
  want=[0]*10;a,b=i%5,j%5
  if i<5 and j<5:want[(a+b)%5]=1
  elif i<5 or j<5:want[5+(a+b)%5]=1
  else:
   want[(a+b)%5]=1
   for k in range(1,5):want[5+(a+b+k)%5]=1
  assert M[i][j]==want,(i,j)
dual=[next(j for j in range(10) if M[i][j][0]) for i in range(10)]
B=[[sum(M[a][j][k]*M[k][dual[a]][i] for a in range(10) for k in range(10)) for j in range(10)] for i in range(10)]
for i in range(10):
 for j in range(10):
  w=10*int(i==j) if i<5 and j<5 else (15+15*int(i==j) if i>=5 and j>=5 else 5*int(i%5!=j%5))
  assert B[i][j]==w,(i,j,B[i][j],w)
# Q(zeta5), with zeta5^4=-1-zeta5-zeta5^2-zeta5^3.
def cv(v):
 if isinstance(v,int) or isinstance(v,Q):return (Q(v),Q(0),Q(0),Q(0))
 return tuple(Q(x) for x in v)
def add(a,b):return tuple(x+y for x,y in zip(cv(a),cv(b)))
def neg(a):return tuple(-x for x in cv(a))
def sub(a,b):return add(a,neg(b))
def mul(a,b):
 a,b=cv(a),cv(b);r=[Q(0)]*7
 for i,x in enumerate(a):
  for j,y in enumerate(b):r[i+j]+=x*y
 for i in range(6,3,-1):
  for j in range(i-4,i):r[j]-=r[i]
 return tuple(r[:4])
def pw(a,n):
 r=cv(1)
 for _ in range(n):r=mul(r,a)
 return r
z=(Q(0),Q(1),Q(0),Q(0));zpow=[pw(z,i) for i in range(5)]
sq5=add(1,mul(2,add(zpow[1],zpow[4])))
d=add(2,sq5);db=sub(2,sq5)
u=mul(Q(1,2),sub(sq5,1));ub=mul(Q(-1,2),add(sq5,1))
# f inverse: for a root w of w²=r*w+1, 1/[5(1+w²)]=(2+r²-r*w)/[5(4+r²)].
def hinv(w,r):return mul(Q(1,5*(4+r*r)),sub(2+r*r,mul(r,w)))
params=[(0,d,4),(0,db,4)]+[(k,w,-1) for k in range(1,5) for w in [u,ub]]
D=add(10,mul(20,d))
i1_b=[]
for k,w,r in params:
 dim=mul(D,hinv(w,r))
 b=next(b for b in range(5) if dim==add(1,mul(b,d)))
 i1_b.append(b)
assert sorted(i1_b)==[0,1,1,1,1,3,3,3,3,4]
H=[]
for k,w,r in params:
 row=[mul(zpow[k*i%5],hinv(w,r)) for i in range(5)]
 H.append(row+[mul(v,w) for v in row])
def sigma(a):
 out=cv(0)
 for i,x in enumerate(a):out=add(out,mul(x,zpow[2*i%5]))
 return out
T=[[0]*10 for _ in range(10)]
for i in range(5):
 T[i][3*i%5]=1
 for j in range(5):T[5+i][j]=int(j!=3*i%5)
 T[5+i][5+3*i%5]=-1
for row in H:
 for j in range(10):
  got=cv(0)
  for k in range(10):got=add(got,mul(row[k],T[k][j]))
  assert got==sigma(row[j]),(j,got,sigma(row[j]))
third=[sum(M[i][i][j]*M[j][i][0] for j in range(10)) for i in range(5,10)]
assert third==[0,1,1,1,1]
receipt={'id':c['id'],'status':'structural_constraints_only','source_tensor_sha256':hashlib.sha256(json.dumps(N,separators=(',',':')).encode()).hexdigest(),'normal_to_source_basis':perm,'all_1000_coefficients_match_normal_form':True,'induction_gram':B,'galois_transform':T,'H_T_equals_sigma_H_exact_Q_zeta5':True,'I1_b_coefficients_from_D_over_formal_codegrees':i1_b,'third_power_unit_multiplicities':third,'pure_b_formal_codegree_integrality':[b for b in range(1,23) if 500%(b*b)==0]}
p=Path(__file__).with_name('structure_receipt.json');p.write_text(json.dumps(receipt,indent=2)+'\n');print('PASS: tensor normal form, induction Gram, exact Galois transform, third-power multiplicities. No classification decision.')
