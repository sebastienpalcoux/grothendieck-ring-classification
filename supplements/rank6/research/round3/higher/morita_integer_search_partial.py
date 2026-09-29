import json,sys,time,signal
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'software'));import stabilizer_rotation_higher as H
import scipy.optimize as O;import numpy as np
D=Path(__file__).parent;R=next(r['N']for r in json.load(open(ROOT/'data/census.json'))if r['id']=='R6_5_638');fixed,seed,nodes,reps=H.anti_representations(R,1);out=[]
def end(*a):raise TimeoutError('90-second total probe budget')
signal.signal(signal.SIGALRM,end);signal.alarm(90)
for ix in (5,7,8,9):
 t=time.monotonic();ab,meta=H.C.morita_system(R,1,fixed,reps[ix]);A,b=ab
 ans=O.milp(np.zeros(len(A[0])),integrality=np.ones(len(A[0])),bounds=O.Bounds(0,2),constraints=O.LinearConstraint(np.array(A,dtype=float),b,b),options={'time_limit':10})
 row={'branch':ix,'meta':meta,'milp_status':int(ans.status),'seconds':time.monotonic()-t}
 if ans.x is not None:
  x=[round(z)for z in ans.x];row['exact_feasible']=all(sum(v*w for v,w in zip(a,x))==bb for a,bb in zip(A,b));row['multiplicities']=x
 out.append(row);(D/'morita_integer_search_partial.json').write_text(json.dumps(out)+'\n');print(row,flush=True)
