import json,sys,time,itertools,math,signal
from pathlib import Path
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'software'))
import round3_m4 as m
from spectral_induction import Spectrum
from modular_character_induction import rational_rows
from higher_traces import farkas,check_farkas
from modular_moments import congruence_witness
from scipy.optimize import linprog,milp,Bounds,LinearConstraint
from exact import require
from fractions import Fraction
import numpy as np
R=next(x['N'] for x in json.load(open(P/'data/unresolved_tensors.json')) if x['id']=='R6_4_629');st=time.monotonic();d=m.data_for(R,3,15);cols=d['lows'][3];tab=d['tab'];C=d['C'];G,vs=m.high_vectors(d,cols);sp=Spectrum(tab,cols,[(v,None) for v in vs]);vs=[v for v in vs if list(v) not in sp.forbidden];A=[[v[i]*v[j] for v in vs] for i in range(5) for j in range(i,5)];b=[int(G[i,j]) for i in range(5) for j in range(i,5)];rows,bs=sp.balance([(v,0) for v in vs],len(vs));A+=rows;b+=bs
lab=tab.assignments(cols)[0];types=dict(zip(sp.vectors,sp.types));vecs=list(map(tuple,cols))+[(0,)+v for v in vs];n=len(vs);weights={():[tab.dims[v]**2/tab.D**2 for v in vecs]};out={'id':'R6_4_629','scope':'pseudo_unitary_necessary','branches':[]};depth=int(sys.argv[1]) if len(sys.argv)>1 else 5
for k in range(1,depth+1):
 for word in itertools.combinations_with_replacement(range(1,6),k):
  w=[z*types[v][lab[word[-1]]] for v,z in zip(vecs,weights[word[:-1]])];weights[word]=w
  if k<3:continue
  rhs=-sum(w[:6],C.zero);co=w[6:]+[C.zero]*(len(A[0])-n)+[-C.one]
  for row in A:row.append(0)
  for row,val in rational_rows(co,rhs,C):
   if any(row) or val:A.append(row);b.append(val)
 print('depth',k,'shape',len(A),len(A[0]),flush=True)
 if k<3:continue
 ma=np.array(A,dtype=float);bb=np.array(b,dtype=float);scale=np.maximum(1,np.maximum(abs(ma).max(axis=1),abs(bb)));lp=linprog(np.zeros(len(A[0])),A_eq=ma/scale[:,None],b_eq=bb/scale,bounds=(0,None),options={'time_limit':60});rec={'depth':k,'rows':len(A),'variables':len(A[0]),'LPstatus':int(lp.status)}
 print('LP',lp.status,flush=True)
 if lp.status==2:
  y=farkas(A,b);rec['ray']=y
  if y is not None:check_farkas(A,b,y);out['outcome']='exact_obstruction'
 elif lp.status==0:
  mm=milp(np.zeros(len(A[0])),integrality=np.ones(len(A[0])),bounds=Bounds(0,np.inf),constraints=LinearConstraint(ma/scale[:,None],bb/scale,bb/scale),options={'time_limit':90});rec['MILPstatus']=int(mm.status);print('MILP',mm.status,flush=True)
  if mm.status==0:
   xx=[int(round(z)) for z in mm.x];ok=all(sum(a*z for a,z in zip(row,xx))==v for row,v in zip(A,b));rec['exact_primal']=ok;print('exact',ok,flush=True)
   if ok:rec['primal']=xx
 out['branches'].append(rec);out['seconds']=time.monotonic()-st;Path(__file__).with_suffix('.json').write_text(json.dumps(out))
 if out.get('outcome')=='exact_obstruction':break
print('total',time.monotonic()-st,flush=True)
