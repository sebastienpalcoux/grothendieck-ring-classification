#!/usr/bin/env python3
import json,itertools,collections
from pathlib import Path
import numpy as np
P=Path(__file__).resolve().parent
for k in [21,114,115,152,153,179]:
 data=json.loads((P/f'R10_1_{k}_dual_action_candidates.json').read_text());B=np.array([x['matrix'] for x in data['candidates']],dtype=int);flat=B.reshape((16,64));idx={tuple(x):i for i,x in enumerate(flat)};solutions={};ct=collections.Counter()
 for i in range(16):
  for j in range(16):
   V=B[i]@B[j];total=V[:,0]; base=sum((int(total[m])*B[2*m+1] for m in range(8)),np.zeros((8,8),dtype=int));diff=np.array([B[2*m]-B[2*m+1] for m in range(8)])
   sols=[]
   for a in itertools.product(*(range(int(t)+1) for t in total)):
    if np.array_equal(base+np.einsum('m,mij->ij',np.array(a),diff),V):
     v=[x for m,t in enumerate(total) for x in (int(a[m]),int(t)-int(a[m]))];sols.append(v)
   solutions[f'{i},{j}']=sols;ct[len(sols)]+=1
 print(k,'counts',dict(ct),'dual',[idx.get(tuple(x.T.ravel())) for x in B],flush=True)
 (P/f'R10_1_{k}_dual_products.json').write_text(json.dumps({'id':data['id'],'unit':idx[tuple(np.eye(8,dtype=int).ravel())],'dual':[idx.get(tuple(x.T.ravel())) for x in B],'product_solutions':solutions},indent=2)+'\n')
