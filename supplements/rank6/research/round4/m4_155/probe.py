import sys,json,time,signal
from pathlib import Path
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'software'))
import round4_155 as V
import round3_m4 as M
from higher_traces import farkas,check_farkas
from modular_moments import congruence_witness,check_congruence
import numpy as np
from scipy.optimize import linprog,milp,Bounds,LinearConstraint
from fractions import Fraction
R=next(x['N'] for x in json.load(open(P/'data/census.json')) if x['id']=='R6_4_155')
height=int(sys.argv[1]) if len(sys.argv)>1 else 3
F=int(sys.argv[2]) if len(sys.argv)>2 else 8
quartic=len(sys.argv)>3 and sys.argv[3]=='quartic'
out=Path(__file__).with_name(('quartic_' if quartic else '')+'probe_F'+str(F)+'_h'+str(height)+'.json');st=time.monotonic();rec={'id':'R6_4_155','height':height,'scope':'pseudo_unitary_necessary'}
def stop(*_):raise TimeoutError('budget')
signal.signal(signal.SIGALRM,stop);signal.alarm(840)
try:
 data=M.data_for(R,height,F);cols=data['lows'][6];lab=data['tab'].assignments(cols)[0];ep=(0,0,1,-1,-1)
 A,b,meta=V.system(R,data,cols,ep,lab,quartic=quartic);print('system',len(A),len(A[0]),flush=True)
 rec.update({'low':6,'labelling':lab,'indicators':ep,'rows':len(A),'variables':len(A[0])})
 aa=np.array(A,dtype=float);bb=np.array(b,dtype=float);scale=np.maximum(1,np.maximum(abs(aa).max(axis=1),abs(bb)));sol=linprog(np.zeros(len(A[0])),A_eq=aa/scale[:,None],b_eq=bb/scale,bounds=(0,None),options={'time_limit':120},method='highs');print('lp',sol.status,sol.message,flush=True);rec['lp_status']=sol.status
 if sol.status==2:
  y=farkas(A,b)
  if y is not None:check_farkas(A,b,y)
  rec.update({'outcome':'exact_farkas' if y else 'no_exact_ray','ray':y})
 elif sol.status==0:
  mi=milp(np.zeros(len(A[0])),integrality=np.ones(len(A[0])),bounds=Bounds(0,np.inf),constraints=LinearConstraint(aa/scale[:,None],bb/scale,bb/scale),options={'time_limit':120});print('milp',mi.status,mi.message,flush=True);rec['milp_status']=mi.status
  if mi.status==0:
   vals=[Fraction(float(x)).limit_denominator(1000000) for x in mi.x]
   ok=all(sum(x*y for x,y in zip(row,vals))==rhs for row,rhs in zip(A,b));rec.update({'outcome':'exact_primal' if ok else 'numerical_primal','values':list(map(str,vals)),'center_rank':str(6+sum(vals[:len(meta['labels'])]))});print('exact',ok,'rank',rec['center_rank'],flush=True)
  else:rec['outcome']='integer_budget' if mi.status==1 else 'no_integer_primal'
 else:rec['outcome']='no_lp_decision'
except TimeoutError:rec['outcome']='budget_incomplete'
finally:signal.alarm(0)
rec['seconds']=time.monotonic()-st;out.write_text(json.dumps(rec,separators=(',',':'))+'\n');print(rec['outcome'],rec['seconds'],flush=True)
