import sys,json,time,signal
from pathlib import Path
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'software'));import round3_m4 as m
from round4_higher_fast import half_e6_subrings, SmallFieldSpectrum
import modular_moments as M
from scipy.optimize import milp,LinearConstraint,Bounds
import numpy as np
rid='R6_6_1035';R=next(r['N']for r in json.load(open(P/'data/census.json'))if r['id']==rid);st=time.monotonic();d=m.data_for(R,3,60);K=d['K'];g,x=half_e6_subrings(R)[0];D=d['D'];dx=d['ds'][x];DE=K(2)+dx*dx;targets=[dx,2*dx,dx,dx,dx+K.one];out=[]
for ix in[3,1]:
 cols=d['lows'][ix];G,vs=m.high_vectors(d,cols);sp=SmallFieldSpectrum(d['tab'],cols,[(v,None)for v in vs],d);bad=set(map(tuple,sp.forbidden));vs=[v for v in vs if v not in bad]
 # phases 0..3 are Xi, phase4=-1, phase5=all subcategory-zero twists
 labels=[(v,t)for v in vs for t in range(6)if (not v[g-1]and not v[x-1]and t==5)or(not v[g-1]and v[x-1]and t<4)or(v[g-1]>=v[x-1]and v[g-1]and t==4)]
 z={v:sum((K(v[i])*d['ds'][i+1]for i in range(5)),K.zero)for v in vs};A=[];b=[]
 for i in range(5):
  for j in range(i,5):A.append([v[i]*v[j]for v,t in labels]);b.append(int(G[i,j]))
 for t0,target in enumerate(targets):
  aa=m.s.Matrix.hstack(*(m.vector(K(v[x-1])*z[v]if t==t0 else K.zero,4)for v,t in labels));bb=m.vector(D/DE*target,4)
  for i in range(4):
   den=m.s.ilcm(*(a.q for a in list(aa[i,:])+[bb[i]]));A.append([int(a*den)for a in aa[i,:]]);b.append(int(bb[i]*den))
 print('system',ix,len(A),len(A[0]),time.monotonic()-st,flush=True)
 y=m.cached_farkas(A,b);cong=M.congruence_witness(A,b,[1]*len(labels));print('ray?',y is not None,'cong',cong,flush=True)
 aa=np.array(A,float);bb=np.array(b,float);scale=np.maximum(1,np.maximum(abs(aa).max(axis=1),abs(bb)));sol=milp(np.zeros(len(labels)),integrality=np.ones(len(labels)),bounds=Bounds(0,np.inf),constraints=LinearConstraint(aa/scale[:,None],bb/scale,bb/scale),options={'time_limit':60});print('milp',sol.status,sol.message,flush=True)
 out.append(dict(low=ix,variables=len(labels),rows=len(A),farkas=y,congruence=cong,milp_status=int(sol.status)))
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
