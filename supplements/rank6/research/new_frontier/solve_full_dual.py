import json,itertools,sys
from pathlib import Path
import numpy as np
from scipy.optimize import milp,LinearConstraint,Bounds
here=Path(__file__).resolve().parent
for t in range(16):
 x=json.load(open(here/f'branch_{t}.json'));G=np.array(x['gram'],dtype=np.int64);r=6
 n=G.shape[0];rows=list(itertools.combinations_with_replacement(range(n),2))
 unique=x['unique'];cols=x['columns'];candidate=[c for cs in x['candidates'] for c in cs];classes=[j for j,cs in enumerate(x['candidates']) for c in cs]
 if len(candidate)==0:continue
 C=np.array(candidate,dtype=np.int64)
 A=np.vstack([C[:,i]*C[:,j] for i,j in rows]+[np.array([int(a==j) for a in classes]) for j in range(len(unique))])
 b=np.array([G[i,j] for i,j in rows]+[cols.count(v) for v in unique])
 lb=np.zeros(len(C));ub=np.array([cols.count(unique[j]) for j in classes])
 ident=np.eye(r,dtype=int).reshape(-1)
 matches=np.where(np.all(C==ident,axis=1))[0]
 if len(matches):lb[matches[0]]=1
 result=milp(np.zeros(len(C)),integrality=np.ones(len(C)),bounds=Bounds(lb,ub),constraints=LinearConstraint(A,b,b),options={'time_limit':15})
 print(t,result.message,flush=True)
 if result.x is not None:
  z=np.rint(result.x).astype(int)
  if not np.array_equal(A@z,b):raise Exception('bad exact')
  active=[(int(zj),c) for zj,c in zip(z,candidate) if zj]
  (here/f'full_gram_{t}.json').write_text(json.dumps(active))
  print('active',[(m,c[::6]) for m,c in active],flush=True)
