#!/usr/bin/env python3
"""Exact ring inputs for the integral-center obstruction; no search."""
from pathlib import Path
import hashlib,json
HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[2]
def need(p,msg):
    if not p:raise ValueError(msg)
source=ROOT/'evidence/unresolved_retry_20261024/proofs/unresolved11_20261024/inputs/R8_3_1154.json'
N=json.loads(source.read_text())['fusion_tensor']
sha=hashlib.sha256(json.dumps(N,separators=(',',':')).encode()).hexdigest()
need(sha=='c399505be76a64c8aba65feaf2cd55125dc7132f5894b74e58b64473d1387e25','Source binding')
d=[(1,0),(7,3),(7,3),(1,0),(6,3),(6,3),(7,3),(7,3)]
mul=lambda z,w:(z[0]*w[0]+5*z[1]*w[1],z[0]*w[1]+z[1]*w[0])
for i in range(8):
 for j in range(8):
  need(mul(d[i],d[j])==tuple(sum(N[i][j][k]*d[k][a]for k in range(8))for a in range(2)),'Dimension identity')
need([i for i,v in enumerate(d) if v[1]==0]==[0,3],'Integral source support')
need(all(v[1]>0 for i,v in enumerate(d) if i not in (0,3)),'Positive irrational coefficients')
need(N[3][1]==[int(k==7)for k in range(8)] and N[1][3]==[int(k==6)for k in range(8)],'g is noncentral')
du=[next(j for j in range(8) if N[i][j][0]) for i in range(8)]
adj={0}
for i in range(8):adj.update(k for k,v in enumerate(N[i][du[i]]) if v)
while True:
 old=set(adj)
 for i in old:
  for j in old:adj.update(k for k,v in enumerate(N[i][j]) if v)
 if adj==old:break
need(adj==set(range(8)),'Full adjoint closure')
out={'status':'PASS','tensor_sha256':sha,'integral_support':[0,3],'noncentral_g_products':[7,6],'adjoint_closure':sorted(adj),'scope':'Exact ring inputs for general-complex proof Z(C)_int=Vec; no categorification or exclusion asserted.'}
(HERE/'integral_center_receipt.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS: integral central restriction is supported on the unit; full adjoint closure.')
