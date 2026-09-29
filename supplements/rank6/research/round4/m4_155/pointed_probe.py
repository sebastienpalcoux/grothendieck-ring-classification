import sys,json,time,signal
from pathlib import Path
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'software'))
import round4_155 as V,round3_m4 as M
from fractions import Fraction
import numpy as np
from scipy.optimize import linprog,milp,Bounds,LinearConstraint
from higher_traces import farkas,check_farkas
R=next(x['N'] for x in json.load(open(P/'data/census.json')) if x['id']=='R6_4_155');height=3;F=8;st=time.monotonic();out=Path(__file__).with_suffix('.json');rec={'id':'R6_4_155','height':height,'F':F,'scope':'pseudo_unitary_necessary','cases':[]}
def stop(*_):raise TimeoutError('840s budget')
signal.signal(signal.SIGALRM,stop);signal.alarm(840)
try:
 data=M.data_for(R,height,F);cols=data['lows'][6];lab=data['tab'].assignments(cols)[0];ep=(0,0,1,-1,-1)
 for Kp in ([0],[0,3],[0,4],[0,5],[0,3,4,5]):
  A,b,meta=V.central_invertible_system(R,data,cols,ep,lab,Kp);print('system',Kp,len(A),len(A[0]),flush=True)
  aa=np.array(A,dtype=float);bb=np.array(b,dtype=float);scale=np.maximum(1,np.maximum(abs(aa).max(axis=1),abs(bb)));sol=linprog(np.zeros(len(A[0])),A_eq=aa/scale[:,None],b_eq=bb/scale,bounds=(0,None),options={'time_limit':60},method='highs');print('lp',sol.status,flush=True)
  row={'K':Kp,'low':6,'labelling':lab,'indicators':ep,'rows':len(A),'variables':len(A[0]),'lp_status':sol.status}
  if sol.status==2:
   y=farkas(A,b)
   if y is not None:check_farkas(A,b,y)
   row.update({'outcome':'exact_farkas' if y else 'no_exact_ray','ray':y})
  elif sol.status==0:
   mi=milp(np.zeros(len(A[0])),integrality=np.ones(len(A[0])),bounds=Bounds(0,np.inf),constraints=LinearConstraint(aa/scale[:,None],bb/scale,bb/scale),options={'time_limit':60});print('milp',mi.status,flush=True);row['milp_status']=mi.status
   if mi.status==0:
    vals=[Fraction(float(x)).limit_denominator(1000000) for x in mi.x];ok=all(sum(x*y for x,y in zip(rr,vals))==rhs for rr,rhs in zip(A,b));row.update({'outcome':'exact_primal' if ok else 'numerical_primal','values':list(map(str,vals)),'center_rank':str(6+sum(vals[:len(meta['labels'])]))});print(row['outcome'],row['center_rank'],flush=True)
   else:row['outcome']='integer_budget' if mi.status==1 else 'no_integer_primal'
  else:row['outcome']='no_lp_decision'
  rec['cases'].append(row);out.write_text(json.dumps(rec,separators=(',',':'))+'\n')
except TimeoutError:rec['outcome']='budget_incomplete'
finally:signal.alarm(0)
rec['seconds']=time.monotonic()-st;out.write_text(json.dumps(rec,separators=(',',':'))+'\n');print('finished',rec['seconds'],flush=True)
