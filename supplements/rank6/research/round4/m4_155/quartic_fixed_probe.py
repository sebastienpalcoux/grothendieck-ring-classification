import sys,json,time,signal
from pathlib import Path
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'software'))
import round4_155 as V,round3_m4 as M
from fractions import Fraction
import numpy as np
from scipy.optimize import linprog,milp,Bounds,LinearConstraint
from higher_traces import farkas,check_farkas
R=next(x['N'] for x in json.load(open(P/'data/census.json')) if x['id']=='R6_4_155');height=3;F=8;st=time.monotonic();out=Path(__file__).with_suffix('.json');rec={'id':'R6_4_155','height':height,'F':F,'scope':'conditional_necessary_system','cases':[]}
def stop(*_):raise TimeoutError('840s budget')
signal.signal(signal.SIGALRM,stop);signal.alarm(840)
try:
 d=M.data_for(R,height,F);cols=d['lows'][6];lab=d['tab'].assignments(cols)[0];ep=(0,0,1,-1,-1);A,b,meta=V.system(R,d,cols,ep,lab,quartic=True,quartic_cutoff=8);print('system',len(A),len(A[0]),flush=True)
 tests=[json.load(open(Path(__file__).with_name('probe_h3.json')))]
 tests+=json.load(open(Path(__file__).with_name('pointed_probe.json')))['cases']
 aa=np.array(A,dtype=float);bb=np.array(b,dtype=float);sc=np.maximum(1,np.maximum(abs(aa).max(axis=1),abs(bb)))
 for c in tests:
  if 'values' not in c:continue
  vals=np.array(list(map(float,c['values'])));lower=np.zeros(len(A[0]));upper=np.full(len(A[0]),np.inf);nh=len(meta['labels']);lower[:nh]=vals[:nh];upper[:nh]=vals[:nh]
  sol=linprog(np.zeros(len(A[0])),A_eq=aa/sc[:,None],b_eq=bb/sc,bounds=list(zip(lower,upper)),options={'time_limit':45},method='highs');print(c.get('K'),c['center_rank'],'lp',sol.status,flush=True)
  row={'source_pointed_subgroup':c.get('K'),'source_rank':c['center_rank'],'lp_status':sol.status}
  if sol.status==0:
   mi=milp(np.zeros(len(A[0])),integrality=np.ones(len(A[0])),bounds=Bounds(lower,upper),constraints=LinearConstraint(aa/sc[:,None],bb/sc,bb/sc),options={'time_limit':90});print('milp',mi.status,flush=True);row['milp_status']=mi.status
   if mi.status==0:
    vv=[Fraction(float(x)).limit_denominator(1000000) for x in mi.x];ok=all(sum(x*y for x,y in zip(rr,vv))==rhs for rr,rhs in zip(A,b));row.update({'outcome':'exact_primal' if ok else 'numerical_primal','values':list(map(str,vv)),'center_rank':str(6+sum(vv[:nh])),'low':6,'labelling':lab,'indicators':ep,'rows':len(A),'variables':len(A[0])});print(row['outcome'],row['center_rank'],flush=True)
   else:row['outcome']='integer_budget'
  else:row['outcome']='conditional_numerical_infeasibility' if sol.status==2 else 'lp_budget'
  rec['cases'].append(row);out.write_text(json.dumps(rec,separators=(',',':'))+'\n')
except TimeoutError:rec['outcome']='budget_incomplete'
finally:signal.alarm(0)
rec['seconds']=time.monotonic()-st;out.write_text(json.dumps(rec,separators=(',',':'))+'\n');print('finished',rec['seconds'],flush=True)
