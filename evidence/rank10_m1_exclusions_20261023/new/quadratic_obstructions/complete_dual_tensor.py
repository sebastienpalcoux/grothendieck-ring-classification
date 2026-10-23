#!/usr/bin/env python3
from pathlib import Path
import json,numpy as np
P=Path(__file__).resolve().parent
for k in [21,114,115,152,153,179]:
 p=json.loads((P/f'R10_1_{k}_dual_products.json').read_text());sols=p['product_solutions'];U=p['unit'];N=np.full((16,16,16),-1,dtype=int)
 for ij,v in sols.items():
  if len(v)==1:i,j=map(int,ij.split(','));N[i,j]=v[0]
 module=json.loads((P/f'R10_1_{k}_module.json').read_text()); Gsource={0,7,8,9} if k==179 else {0,1,2,9}
 dims=[d for orbit in module['free_orbits'] for d in ([1,0] if orbit[0] in Gsource else [3,2],)*2]+[[1,1]]*8
 Zindices=[i for i,d in enumerate(dims) if d==[3,2]]
 expressions={}
 for i in range(8,16):
  for j in range(8,16):
   v=N[i,j]
   if v.min()>=0 and v.sum()==1 and np.argmax(v) in Zindices:expressions[int(np.argmax(v))]=(i,j)
 print(k,'Z expressions',expressions,flush=True)
 for z,(a,b) in expressions.items():
  for j in range(16):
   v=np.einsum('t,tk->k',N[b,j],N[a])
   if N[z,j].min()<0:
    if v.tolist() not in sols[f'{z},{j}']:raise RuntimeError('forced product not allowed')
    N[z,j]=v
   elif not np.array_equal(N[z,j],v):raise RuntimeError('association failed')
 if N.min()<0:raise RuntimeError('incomplete')
 if not np.array_equal(N[U],np.eye(16,dtype=int)):raise RuntimeError('unit')
 for i in range(16):
  for j in range(16):
   for t in range(16):
    if not np.array_equal(N[i,j]@N[:,t],N[j,t]@N[i]):raise RuntimeError('not associative')
 B=np.array([x['matrix'] for x in json.loads((P/f'R10_1_{k}_dual_action_candidates.json').read_text())['candidates']]);
 if not all(np.array_equal(B[i]@B[j],np.einsum('t,tjk->jk',N[i,j],B)) for i in range(16) for j in range(16)):raise RuntimeError('action mismatch')
 (P/f'R10_1_{k}_dual_tensor.json').write_text(json.dumps({'id':p['id'],'unit':U,'dual':p['dual'],'dimensions':dims,'fusion_tensor':N.tolist(),'Z_expressions':expressions,'status':'necessary_dual_ring'},indent=2)+'\n')
 print(k,'PASS forced dual tensor',flush=True)
