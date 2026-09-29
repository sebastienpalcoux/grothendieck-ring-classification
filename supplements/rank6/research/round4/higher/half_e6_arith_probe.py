import sys,json,time
from pathlib import Path
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'software'));import round3_m4 as m
from exact import ec,vector
from fractions import Fraction
from scipy.optimize import milp,LinearConstraint,Bounds
import numpy as np
R=next(r['N']for r in json.load(open(P/'data/census.json'))if r['id']=='R6_6_1035');d=m.data_for(R,3,60);K=d['K'];dim=d['ds'][4];DE=K(2)+dim*dim;D=d['D'];targets=[dim,2*dim,dim,dim,dim+K(1),dim+K(1),dim+K(2)]
for ix in [1,3]:
 cols=d['lows'][ix];G,vs=m.high_vectors(d,cols);vs=[v for v in vs if v[3]];low=sum((K(c[4])*sum((K(c[i])*d['ds'][i]for i in range(6)),K.zero)for c in cols),K.zero)
 print(ix,'v',len(vs),'low',ec(low),'target1',ec(D/DE*(2*dim+K(3))),'diffpositive',d['embedding'].sign(D/DE*(2*dim+K(3))-low),flush=True)
 A=m.s.Matrix.hstack(*(vector(K(v[3])*sum((K(v[i])*d['ds'][i+1]for i in range(5)),K.zero),4)for v in vs));co=m.s.Matrix.hstack(A,*(vector(D/DE*t,4)for t in targets));den=m.s.ilcm(*(x.q for x in co));AA=np.array(A*den,dtype=float)
 for j,t in enumerate(targets):
  b=vector(D/DE*t,4);bb=np.array(b*den,dtype=float).ravel();sol=milp(np.zeros(len(vs)),integrality=np.ones(len(vs)),bounds=Bounds(0,np.inf),constraints=LinearConstraint(AA,bb,bb),options={'time_limit':5});print(j,sol.status,flush=True)
