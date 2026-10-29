#!/usr/bin/env python3
"""Exact necessary R928 fusion matrices. No associators, no exclusion claimed."""
from pathlib import Path
from fractions import Fraction as Q
from collections import Counter
import json, hashlib, importlib.util
HERE=Path(__file__).resolve().parent
PRIOR=HERE.parents[1]/'prior'
helper=PRIOR/'evidence/unresolved7_20261027/r8_928_941/verify.py'
spec=importlib.util.spec_from_file_location('quartic',helper);v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
src=PRIOR/'evidence/rank8_frontier_20261021/quartic_integer_center/source.json'
pat=src.with_name('gram_cubic.json')
r=next(x for x in json.loads(src.read_text())['records'] if x['id']=='R8_3_928')
pats=json.loads(pat.read_text())['patterns']
ds=[tuple(map(Q,x)) for x in r['full_characters'][0]]
cols=r['low_columns']+[[0]+z for z in r['canonical_high_vectors']]
dims=[v.dot(z,ds) for z in cols]
sig=[(1,1),(-1,1),(-1,-1),(1,-1)]
low=[v.mul(v.D,v.inv(v.sigma(v.D,*s))) for s in sig]
w=v.scale(Q(1,4),v.D);glob=v.scale(Q(1,2),v.mul(v.D,v.D));ig=v.inv(glob)
known=[[0,0,0,1],[0,3,5,7],[0,5,6,10],[1,7,10,17]]
E=[v.mul(low[3],v.mul(v.sigma(d,*sig[3]),v.inv(d))) for d in low]
out={'status':'PASS','date':'2026-10-29','scope':'necessary fusion matrices only; R928 remains unresolved',
'dependencies':{str(p.relative_to(PRIOR)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [helper,src,pat]},'patterns':[]}
def rational(z):
 assert z[1:]==v.ZERO[1:]
 return z[0]
def mm(A,B):return [[sum(A[i][k]*B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
def enc(A):return [[str(x) for x in row] for row in A]
for ix in [40,49,186,191]:
 hist=Counter()
 for d,n in zip(dims,[1]*5+pats[ix]):hist[d]+=n
 assert all(n%2==0 for n in hist.values())
 objs=[d for d,n in hist.items() for _ in range(n//2)];n=len(objs)
 assert objs[:5]==low+[w]
 L=[[v.mul(low[k],v.mul(v.sigma(d,*sig[k]),v.inv(d))) for k in range(4)] for d in objs]
 LW=[v.mul(w,v.inv(d)) if d in low else v.scale(-2,v.ONE) if d==w else v.ZERO for d in objs]
 NW=[];M=[];Square=[]
 for i,di in enumerate(objs):
  roww=[];rowm=[];row2=[]
  for j,dj in enumerate(objs):
   fac=v.mul(v.mul(di,dj),ig);zw=zm=z2=v.ZERO
   for k in range(4):
    u=v.mul(L[i][k],L[j][k])
    zw=v.add(zw,v.mul(v.mul(w,v.inv(low[k])),u))
    zm=v.add(zm,v.mul(v.add(E[k],v.ONE),u))
    z2=v.add(z2,v.mul(v.add(v.mul(E[k],E[k]),v.scale(-1,v.ONE)),u))
   zw=v.add(zw,v.scale(-2,v.mul(LW[i],LW[j])))
   roww.append(rational(v.mul(zw,fac)))
   rowm.append(rational(v.mul(zm,fac))-int(i==j))
   row2.append(rational(v.mul(z2,fac))+int(i==j))
  NW.append(roww);M.append(rowm);Square.append(row2)
 assert all(x>=0 and x.denominator==1 for row in NW for x in row)
 assert NW[0]==[Q(int(j==4)) for j in range(n)]
 assert sum(NW[i][i] for i in range(n))==142
 for i in range(n):assert v.dot(NW[i],objs)==v.mul(w,objs[i])
 # Galois-unit cubic coefficients, independently via all column dimensions.
 triple=[]
 for i in range(4):
  row=[]
  for j in range(4):
   z=v.ZERO
   for k,d in enumerate(objs):z=v.add(z,v.mul(v.mul(d,d),v.mul(L[k][3],v.mul(L[k][i],L[k][j]))))
   row.append(rational(v.mul(z,ig)))
  triple.append(row)
 assert triple==known
 Q0=[[Q(0) for j in range(n)] for i in range(n)]
 for i in range(4):
  for j in range(4):Q0[i][j]=Q(known[i][j])-M[i][j]
 for i in range(5):Q0[i][4]=Q0[4][i]=NW[i][3]-M[i][4]
 assert Q0[4][4]==1 and all(Q0[i][4]==-Q(1,2) for i in range(4))
 assert mm(Q0,Q0)==[[2*x for x in row] for row in Q0]
 assert sum(Q0[i][i] for i in range(n))==4
 plus=sum(1 for k in range(4,n) if L[k][3]==v.ONE)
 assert plus==(2 if ix in [49,191] else 5)
 case={'pattern':ix,'rank':n,'dimensions':list(map(v.enc,objs)),'N_W':[[int(x) for x in row] for row in NW],
      'N_c_squared':[[int(x) for x in row] for row in Square], 'baseline_M':enc(M),'fixed_Q0':enc(Q0),
      'remaining_positive_projector_rank':plus-2}
 if plus==2:
  NC=[[M[i][j]+Q0[i][j] for j in range(n)] for i in range(n)]
  assert all(x>=0 and x.denominator==1 for row in NC for x in row)
  assert mm(NC,NC)==Square and mm(NC,NW)==mm(NW,NC)
  assert NC[0]==[Q(int(j==3)) for j in range(n)]
  for i in range(n):assert v.dot(NC[i],objs)==v.mul(low[3],objs[i])
  case['unique_N_c']=[[int(x) for x in row] for row in NC]
 out['patterns'].append(case)
(HERE/'spectral_reduction.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS: N_W forced in four patterns; N_c forced in patterns49 and191; no status change.')
