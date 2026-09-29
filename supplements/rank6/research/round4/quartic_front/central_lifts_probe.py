import sys,json,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];sys.path[:0]=[str(ROOT/'software'),str(ROOT/'research/round3/quartic')]
from verlinde_probe import *
from fractions import Fraction
from scipy.optimize import linprog
import numpy as np
rid=sys.argv[1] if len(sys.argv)>1 else 'R6_4_91'
R=next(r['N'] for r in json.load(open(ROOT/'data/census.json')) if r['id']==rid);m.R=R;data=data_for(R,3);tab=table_for(R,data);cols=data['lows'][1];ep=(0,0,-1,1,1) if rid.endswith('_91') else (0,0,1,1,1);mod=forced_module_data(R);out=[]
for lab in tab.assignments(cols):
 A,b,meta,labels=system(R,data,cols,ep,mod['objects'],True);A,b,meta=stronger_system(data,tab,cols,lab,A,b,labels);A,b,n=coupled(data,tab,cols,A,b,labels);A,b,labels,base=verlinde(R,data,tab,cols,lab,A,b,labels)
 keep=list(range(len(A[0])))
 if rid.endswith('_91'):
  C=data['C'];allowed={j for j,t in enumerate(data['phases']) if t in {tuple(C.unit**(a*k%16) for k in range(1,4)) for a in range(1,16,2)}};keep=[j for j in range(len(A[0])) if j>=len(labels) or not labels[j][0][2] or labels[j][1] in allowed];A=[[row[j] for j in keep] for row in A]
 print('start',rid,lab,len(A),len(A[0]),flush=True);aa=np.array(A,dtype=float);bb=np.array(b,dtype=float);scale=np.maximum(1,np.maximum(abs(aa).max(axis=1),abs(bb)))
 for obj in [3,4]:
  target=tuple(int(j==obj) for j in range(1,6));objco=np.array([int(j<len(labels) and tuple(labels[j][0])==target) for j in keep]);sol=linprog(objco,A_eq=aa/scale[:,None],b_eq=bb/scale,bounds=(0,None),options={'time_limit':60},method='highs');print('minimum',obj,sol.status,sol.fun,flush=True)
  rec=dict(id=rid,lab=lab,obj=obj,status=sol.status,minimum_float=sol.fun)
  if sol.status==0 and sol.fun<0.001:
   from scipy.optimize import milp,Bounds,LinearConstraint
   integ=np.array([int(j<len(labels) or j>=base) for j in keep]); mi=milp(objco,integrality=integ,bounds=Bounds(0,np.inf),constraints=LinearConstraint(aa/scale[:,None],bb/scale,bb/scale),options={'time_limit':120})
   rec['integer_status']=int(mi.status);rec['integer_min']=mi.fun;print('integer minimum',obj,mi.status,mi.fun,flush=True)
  if sol.status==0 and sol.fun>0.999:
   A2=A+[list(map(int,objco))];b2=b+[0];y=farkas(A2,b2)
   if y is not None:check_farkas(A2,b2,y);rec['zero_column_ray']=y
  out.append(rec);Path(__file__).with_name(rid+'_central_lifts_probe.json').write_text(json.dumps(out,indent=2)+'\n')
