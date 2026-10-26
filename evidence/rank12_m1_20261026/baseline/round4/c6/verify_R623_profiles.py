#!/usr/bin/env python3
"""Exact finite central-semion Gram reduction; no optimization or repo imports."""
import json,itertools,math
from pathlib import Path
from fractions import Fraction as Q
P=Path(__file__).resolve().parent
J=json.loads((P/'audit/frozen_inputs.json').read_text());R=J['tensors']['R12_1_623']
def need(x,m):
 if not x:raise ValueError(m)
L=[r for r in J['controls']['R623']['low']['branches']if r['psd']][1]['columns']
du=[next(j for j in range(12)if R[i][j][0])for i in range(12)]
z=[R[11][i].index(1)for i in range(12)]
B=[[sum(R[a][i][k]*R[k][du[a]][j]for a in range(12)for k in range(12))for j in range(12)]for i in range(12)]
H=L+[[v[z[i]]for i in range(12)]for v in L]
res=[[B[i][j]-sum(v[i]*v[j]for v in H)for j in range(12)]for i in range(12)]
classes=[[1,2],[9,10],[3,5,7],[4,6,8]]
M=[[res[a[0]][b[0]]for b in classes]for a in classes]
need(M==[[6,0,6,6],[0,6,6,6],[6,6,32,30],[6,6,30,32]],'residual Gram')
def good(p,a,b):
 u=Q(2*p+9*(a+b));v=Q(3*(a+b));n=u*u-10*v*v
 if n==0:return False
 r=(120*u-360*v)/n;s=(36*u-120*v)/n
 return (2*r).denominator==1 and(r*r-10*s*s).denominator==1 and(not v or((2*u)**2/n).denominator==1)
off=[(p,m)for p in range(2)for m in range(3)if good(p,m+1,m)]
need(off==[(0,0)],'off-diagonal orbit not forced')
types=[(p,t)for p in range(3)for t in range(4)if(p or t)and good(p,t,t)]
need(types==[(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,2)],'symmetric pair domain')
profiles=[]
def search(i,a,b,c,cs):
 if min(a,b,c)<0:return
 if i==len(types):
  if a==b==c==0:profiles.append(cs)
  return
 p,t=types[i];bounds=[16]
 if p:bounds.append(a//(p*p))
 if t:bounds.append(c//(t*t))
 if p*t:bounds.append(b//(p*t))
 for k in range(min(bounds)+1):search(i+1,a-k*p*p,b-k*p*t,c-k*t*t,cs+[k])
search(0,6,6,15,[]);need(len(profiles)==13,'profile count')
for cs in profiles:
 gram=[[0]*4 for _ in range(4)]
 columns=[[0,0,1,0]]*2+[[0,0,0,1]]*2
 for(p,t),n in zip(types,cs):columns +=[[p,0,t,t],[0,p,t,t]]*n
 for v in columns:
  for i,j in itertools.product(range(4),repeat=2):gram[i][j]+=v[i]*v[j]
 need(gram==M,'full profile Gram')
report={'status':'PASS','ring':'R12_1_623','restriction_only':True,'new_exclusion':False,'residual_Gram':M,'off_diagonal_orbit':{'pointed_coefficient':0,'noninvertible_coefficients':[1,0],'objects':4,'dimension':'3d'},'symmetric_pair_types':types,'profiles':profiles,'optimizer_used':False,'parent_repository_imports':False}
(P/'R623_profiles_verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k!='profiles'}))
