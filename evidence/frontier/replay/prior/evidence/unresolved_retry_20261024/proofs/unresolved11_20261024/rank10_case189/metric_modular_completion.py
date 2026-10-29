"""Exact conditional metric-C5 modular completion test in Q(zeta5).
No candidate below is treated as a fusion category.
"""
from fractions import Fraction as Q
from pathlib import Path
import json
HERE=Path(__file__).resolve().parent

def cv(a):return (Q(a),Q(0),Q(0),Q(0)) if isinstance(a,(int,Q)) else tuple(map(Q,a))
def add(a,b):return tuple(x+y for x,y in zip(cv(a),cv(b)))
def neg(a):return tuple(-x for x in cv(a))
def sub(a,b):return add(a,neg(b))
def mul(a,b):
 a,b=cv(a),cv(b);r=[Q(0)]*7
 for i,x in enumerate(a):
  if x:
   for j,y in enumerate(b):
    if y:r[i+j]+=x*y
 for i in range(6,3,-1):
  for j in range(i-4,i):r[j]-=r[i]
 return tuple(r[:4])
def total(v):
 out=cv(0)
 for x in v:out=add(out,x)
 return out
z=cv((0,1,0,0));zp=[cv(1)]
for k in range(4):zp.append(mul(zp[-1],z))
sq5=add(1,mul(2,add(zp[1],zp[4])));d=add(2,sq5);dp=sub(2,sq5)
B=add(1,d);C=add(1,mul(3,d));U=mul(d,d)
uplus=mul(Q(1,2),sub(d,3));uminus=mul(Q(-1,2),sub(d,1))
rootinv=mul(Q(-1,10),dp) # 1/(10d)
zero=cv(0)

def conj(a):return total(mul(a[k],zp[-k%5]) for k in range(4))
def matmul(A,B):return [[total(mul(A[i][k],B[k][j]) for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
def enc(a):return [str(x) for x in a]

def build(q,c,sgn):
 # 0=unit,1=U,2..5=B_l,6..9=C_l,10=Y,11=P1,12=P2,13=X.
 params=[(0,d),(0,dp)]+[(l,uminus) for l in range(1,5)]+[(l,uplus) for l in range(1,5)]
 dims=[cv(1),U]+[B]*4+[C]*4+[d,mul(2,d),mul(2,d),mul(5,d)]
 vcols=[(0,0,0,0,0),(0,1,1,1,1)]
 for l in range(1,5):vcols.append(tuple(int(i==c*l%5) for i in range(5)))
 for l in range(1,5):vcols.append(tuple(int(i not in (0,c*l%5)) for i in range(5)))
 pure=[(1,0,0,0,0),(0,1,0,0,1),(0,0,1,1,0),(1,1,1,1,1)]
 S=[[zero for _ in range(14)] for _ in range(14)]
 for i,(l,w) in enumerate(params):
  for j,v in enumerate(vcols):
   val=add(1,mul(w,total(mul(v[k],zp[l*k%5]) for k in range(5))))
   S[i][j]=mul(mul(mul(dims[i],val),rootinv),zp[-l*params[j][0]*pow(2*q,-1,5)%5])
  for j,v in enumerate(pure,10):
   val=mul(w,total(mul(v[k],zp[l*k%5]) for k in range(5)))
   S[i][j]=S[j][i]=mul(mul(dims[i],val),rootinv)
 a=mul(Q(1,10),add(3,mul(sgn,sq5)));b=mul(Q(1,10),sub(3,mul(sgn,sq5)))
 block=[[cv(Q(-3,10)),cv(Q(2,5)),cv(Q(2,5)),cv(Q(-1,2))],[cv(Q(2,5)),a,b,zero],[cv(Q(2,5)),b,a,zero],[cv(Q(-1,2)),zero,zero,cv(Q(1,2))]]
 for i in range(4):
  for j in range(4):S[10+i][10+j]=block[i][j]
 twists=[zp[-l*l*pow(4*q,-1,5)%5] for l,w in params]+[cv(1),zp[3*q%5],zp[-3*q%5],cv(-1)]
 dual=[0,1,5,4,3,2,9,8,7,6,10,11,12,13]
 return S,twists,dual,dims

results=[]
for q,c in [(1,2),(1,4),(4,1),(4,3)]:
 for sign in [-1,1]:
  S,T,dual,dims=build(q,c,sign)
  receipt={'q':q,'c':c,'sign':sign}
  receipt['symmetric']=all(S[i][j]==S[j][i] for i in range(14) for j in range(14))
  S2=matmul(S,S)
  receipt['S2_charge_conjugation']=all(S2[i][j]==cv(int(j==dual[i])) for i in range(14) for j in range(14))
  STS=matmul([[mul(S[i][j],T[j]) for j in range(14)] for i in range(14)],S)
  target=[[mul(mul(conj(T[i]),conj(S[i][j])),conj(T[j])) for j in range(14)] for i in range(14)]
  failures=[(i,j,enc(sub(STS[i][j],target[i][j]))) for i in range(14) for j in range(14) if STS[i][j]!=target[i][j]]
  receipt['STS_identity']=not failures
  if failures:receipt['first_STS_failure']=failures[0]
  if receipt['S2_charge_conjugation']:
   invdims=[cv(1),mul(dp,dp)]+[mul(Q(1,4),add(1,dp))]*4+[mul(Q(1,4),add(1,mul(3,dp)))]*4+[neg(dp),mul(Q(-1,2),dp),mul(Q(-1,2),dp),mul(Q(-1,5),dp)]
   invS0=[mul(mul(10,d),v) for v in invdims]
   bad=[]
   N=[[[0]*14 for j in range(14)] for i in range(14)]
   for i,j,k in [(i,j,k) for i in range(14) for j in range(i,14) for k in range(14)]:
    val=total(mul(mul(mul(S[i][l],S[j][l]),conj(S[k][l])),invS0[l]) for l in range(14))
    if any(val[l] for l in range(1,4)) or val[0].denominator!=1 or val[0]<0:
     bad.append((i,j,k,enc(val)));break
    N[i][j][k]=N[j][i][k]=int(val[0])
   receipt['Verlinde_nonnegative_integer']=not bad
   if bad:receipt['first_Verlinde_failure']=bad[0]
   else:
    closures=[]
    for generator in range(1,14):
     closure={0,generator,dual[generator]}
     while True:
      bigger=closure|{dual[i] for i in closure}|{k for i in closure for j in closure for k,n in enumerate(N[i][j]) if n}
      if bigger==closure:break
      closure=bigger
     closures.append(sorted(closure))
    receipt['single_object_closures']=closures
    candidate={'warning':'Necessary modular-data candidate only; no fusion category or original-ring model has been constructed.','q':q,'c':c,'pure_block_sign':sign,'basis':['1','U']+['B'+str(i) for i in range(1,5)]+['C'+str(i) for i in range(1,5)]+['Y','P1','P2','X'],'cyclotomic_field':'Q(zeta5), coefficients in basis1,zeta5,zeta5^2,zeta5^3','S':[[enc(x) for x in row] for row in S],'theta':[enc(x) for x in T],'dimensions':[enc(x) for x in dims],'dual':dual,'fusion_tensor':N,'checks':receipt}
    (HERE/('metric_candidate_q'+str(q)+'_c'+str(c)+'.json')).write_text(json.dumps(candidate,indent=2)+'\n')
  print(receipt,flush=True)
  results.append(receipt)
(HERE/'metric_modular_completion_results.json').write_text(json.dumps({'warning':'Conditional necessary modular data only.','results':results},indent=2)+'\n')
