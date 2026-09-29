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
 C=data['C'];one=tuple(C.one for _ in range(3));minus=tuple(C((-1)**k) for k in range(1,4));
 if rid.endswith('_91'):
  sigma_types={tuple(C.unit**(a*k%16) for k in range(1,4)) for a in [3,5,11,13]}
  def permitted(v,ti):return (not v[2] or data['phases'][ti] in sigma_types) and (not v[3] or data['phases'][ti]==minus)
 else:
  def permitted(v,ti):return not v[2] or data['phases'][ti] in (one,minus)
 keep=[j for j in range(len(A[0])) if j>=len(labels) or permitted(*labels[j])];A=[[row[j] for j in keep] for row in A]
 print('start',rid,lab,len(A),len(A[0]),flush=True);aa=np.array(A,dtype=float);bb=np.array(b,dtype=float);scale=np.maximum(1,np.maximum(abs(aa).max(axis=1),abs(bb)))
 sol=linprog(np.zeros(len(A[0])),A_eq=aa/scale[:,None],b_eq=bb/scale,bounds=(0,None),options={'time_limit':90},method='highs');print('LP',sol.status,sol.message,flush=True)
 rec=dict(id=rid,lab=lab,status=sol.status,rows=len(A),columns=len(A[0]))
 if sol.status==2:
  y=farkas(A,b)
  if y is not None:check_farkas(A,b,y);rec['ray']=y
 elif sol.status==0:
  from scipy.optimize import milp,Bounds,LinearConstraint
  integ=np.array([int(j<len(labels) or j>=base) for j in keep]);mi=milp(np.zeros(len(A[0])),integrality=integ,bounds=Bounds(0,np.inf),constraints=LinearConstraint(aa/scale[:,None],bb/scale,bb/scale),options={'time_limit':180});rec['integer_status']=int(mi.status);print('MILP',mi.status,mi.message,flush=True)
  if mi.status==0:
   vals=[str(Fraction(float(x)).limit_denominator(1000000)) for x in mi.x];values=list(map(Fraction,vals));rec['exact']=all(sum(x*y for x,y in zip(row,values))==rhs for row,rhs in zip(A,b));rec['variables']=vals;rec['keep']=keep;print('exact',rec['exact'],flush=True)
 out.append(rec);Path(__file__).with_name(rid+'_subcategory_support_probe.json').write_text(json.dumps(out,indent=2)+'\n')
