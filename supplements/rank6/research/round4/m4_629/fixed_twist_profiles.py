import sys,json,math,itertools,time,signal
from pathlib import Path
import numpy as np
from scipy.sparse import csr_matrix
from scipy.optimize import linprog,milp,Bounds,LinearConstraint
from fractions import Fraction
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'software'))
from round4_629_orbits import *
from higher_traces import farkas,check_farkas
R=next(x['N'] for x in json.load(open(P/'data/unresolved_tensors.json')) if x['id']=='R6_4_629');here=Path(__file__).parent;source=json.load(open(here/'filtered_profiles.json'));h=int(sys.argv[1]) if len(sys.argv)>1 else 6;st=time.monotonic();data=ambient.data_for(R,h,15);cols=data['lows'][3];tab=data['tab'];lab_index=int(sys.argv[2]) if len(sys.argv)>2 else 0;lab=tab.assignments(cols)[lab_index];ep=(1,1,1,1,1);A,b,meta=ambient.system(R,data,cols,ep,lab);G,vs=ambient.high_vectors(data,cols);sp=Spectrum(tab,cols,[(v,None) for v in vs]);vs=[v for v in vs if list(v) not in sp.forbidden];require(list(map(list,vs))==source['vectors'],'profile vector mismatch');labels=[(v,ti) for v in vs for ti in range(len(data['phases']))];nh=len(labels);rec={'id':'R6_4_629','height':h,'scope':'pseudo_unitary_necessary','low':3,'lab':lab,'ep':ep,'source_profiles':source['surviving_indices'],'branches':[]};out=here/('fixed_twist_h'+str(h)+('_lab'+str(lab_index) if lab_index else '')+'.json')
for pi,c in zip(source['surviving_indices'],source['counts']):
 weights={v:cc for v,cc in zip(vs,c)};domains={B:orbit_domain(data,B) for B in set(c) if B};keep=[]
 for j in range(len(A[0])):
  if j>=nh:keep.append((j,1));continue
  v,ti=labels[j]
  if weights[v]:keep.extend((j,e) for e in domains[weights[v]].get(ti,[]))
 AA=[[row[j]*e for j,e in keep] for row in A];bb=b[:]
 for v,cc in zip(vs,c):
  if not cc:continue
  AA.append([int(j<nh and labels[j][0]==v)*e for j,e in keep]);bb.append(cc)
 ma=csr_matrix(np.array(AA,dtype=float));rb=np.array(bb,dtype=float);sc=np.maximum(1,np.maximum(abs(ma).max(axis=1).toarray().ravel(),abs(rb)));ma=ma.multiply((1/sc)[:,None]).tocsr();rb=rb/sc
 rr={'profile':pi,'rank':6+sum(c),'variables':len(keep),'rows':len(AA),'columns':keep};print('profile',pi,'rank',rr['rank'],'shape',len(AA),len(keep),flush=True)
 lp=linprog(np.zeros(len(keep)),A_eq=ma,b_eq=rb,bounds=(0,None),options={'time_limit':60});rr['LPstatus']=int(lp.status);print('LP',lp.status,flush=True)
 if lp.status==2:
  ray=farkas(AA,bb);rr['ray']=ray
  if ray is not None:check_farkas(AA,bb,ray);rr['outcome']='exact_linear_obstruction'
  else:rr['outcome']='numerical_infeasibility_only'
 elif lp.status==0:
  mm=milp(np.zeros(len(keep)),integrality=np.ones(len(keep)),bounds=Bounds(0,np.inf),constraints=LinearConstraint(ma,rb,rb),options={'time_limit':90});rr['MILPstatus']=int(mm.status);print('MILP',mm.status,flush=True)
  if mm.status==0:
   x=[int(round(z)) for z in mm.x];ok=all(sum(a*z for a,z in zip(row,x))==rhs for row,rhs in zip(AA,bb));rr['exact_primal']=ok
   if ok:rr['primal']=x;rr['outcome']='exact_necessary_witness';print('EXACT',True,flush=True)
   else:rr['outcome']='inexact_solver_output'
  else:rr['outcome']='no_exact_conclusion'
 else:rr['outcome']='no_exact_conclusion'
 rec['branches'].append(rr);rec['seconds']=time.monotonic()-st;out.write_text(json.dumps(rec))
 print(rr['outcome'],flush=True)
print('seconds',time.monotonic()-st,flush=True)
