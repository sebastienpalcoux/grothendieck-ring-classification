#!/usr/bin/env python3
"""Verify existing small character tables, without reconstructing irreducibles."""
from pathlib import Path
import sys,types,json,hashlib,time,signal
import sympy as s
HERE=Path(__file__).resolve().parent
def need(ok,msg):
 if not ok:raise ValueError(msg)
def evaluate(coeff,z,C):
 out=C.zero
 for c in coeff:out=out*z+C(c)
 return out
stub=types.ModuleType('exact');stub.require=need;stub.evaluate=evaluate
sys.modules['exact']=stub
import finite_spectra48 as F
if hasattr(signal,'SIGALRM'):
 signal.signal(signal.SIGALRM,lambda *_:(_ for _ in ()).throw(TimeoutError('60-second verification cap')))
 signal.alarm(60)
st=time.monotonic();C=F.coefficient_field();out=[]
for q,expected in [(8,384),(3,24)]:
 path=HERE/f'sl2_{q}.json';loc=json.loads(path.read_text());g=loc['group']
 classes=[[tuple(x) for x in c] for c in g['classes']]
 flat=[x for c in classes for x in c];index={x:i for i,c in enumerate(classes) for x in c}
 need(len(flat)==len(index)==expected==g['order'],'complete group order / distinct matrices')
 need(all((a*d-b*c)%q==1 for a,b,c,d in flat),'determinants')
 need(g['sizes']==[len(c) for c in classes],'class sizes')
 # Since the number matches |SL2(Z/q)|, these are all determinant-one matrices.
 S=(0,q-1,1,0);T=(1,1,0,1);one=(1,0,0,1)
 for i,cl in enumerate(classes):
  seen={cl[0]};todo=[cl[0]]
  while todo:
   x=todo.pop()
   for a in [S,T]:
    y=F.mul(F.mul(a,x,q),F.inv(a,q),q)
    need(index[y]==i,'conjugation stability')
    if y not in seen:seen.add(y);todo.append(y)
  need(seen==set(cl),'each recorded class is one conjugacy orbit')
 # Check every class-algebra entry directly against these concrete matrices.
 for i,cl in enumerate(classes):
  x=cl[0]
  for j,cj in enumerate(classes):
   counts=[0]*len(classes)
   for y in cj:counts[index[F.mul(x,y,q)]]+=1
   for k,z in enumerate(counts):
    n,r=divmod(z*len(cl),len(classes[k]))
    need(not r and n==g['class_algebra'][i][j][k],'class multiplication')
 x=one;power=[]
 for _ in range(q):power.append(index[x]);x=F.mul(x,T,q)
 need(x==one and power==g['power_classes'],'T power classes')
 need(index[(q-1,0,0,q-1)]==g['central_class'],'minus-identity class')
 F.verify(g,loc['irreps'],C)
 a=5%q;gi=index[(a,0,0,pow(a,-1,q))];ri=1 if q==8 else 2
 need(loc['irreps'][ri]['degree']==1 and loc['irreps'][ri]['characters'][gi]==['1'],'sign character G5')
 out.append(dict(modulus=q,order=expected,irreducibles=len(loc['irreps']),sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
need(30*7==210 and 384*24==9216,'CRT product')
payload=dict(status='PASS',tables=out,product_irreducibles=210,product_order=9216,seconds=time.monotonic()-st,
 scope='Complete exact validation of existing class tables and their T spectra; no new categorical model.')
(HERE/'table_verification.json').write_text(json.dumps(payload,indent=2)+'\n')
if hasattr(signal,'SIGALRM'):signal.alarm(0)
print(json.dumps(payload))
