"""Bounded applicability and exact survival control scan; never an exclusion."""
import sys,json,time,signal,os
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor,as_completed
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'software'))
import round4_155 as V,round3_m4 as M
from fractions import Fraction
from exact import VerificationError
from character_induction import Ineligible
import numpy as np
from scipy.optimize import linprog,milp,Bounds,LinearConstraint

def one(args):
 rid,R,status=args;st=time.monotonic();out={'id':rid,'status':status,'criterion':'complex_low_verlinde_restriction','budget_seconds':24}
 def stop(*_):raise TimeoutError('explicit per-input 24-second budget')
 signal.signal(signal.SIGALRM,stop);signal.alarm(24)
 try:
  data=M.data_for(R,3);out['field']=M.metadata(data);out['eligible']=True
  for ix,cols in enumerate(data['lows']):
   why=M.low_failure(cols,data['ch'].C,data['ds'],data['D'],data['K'],data['embedding'],data['ch'].du)
   if why:continue
   for lab in data['tab'].assignments(cols):
    for ep in M.indicator_choices(R):
     A,b,meta=V.system(R,data,cols,ep,lab)
     if A is None:continue
     out['attempted_system']={'low':ix,'labelling':list(lab),'indicators':list(ep),'rows':len(A),'variables':len(A[0])}
     aa=np.array(A,dtype=float);bb=np.array(b,dtype=float);sc=np.maximum(1,np.maximum(abs(aa).max(axis=1),abs(bb)));sol=linprog(np.zeros(len(A[0])),A_eq=aa/sc[:,None],b_eq=bb/sc,bounds=(0,None),options={'time_limit':5},method='highs')
     if sol.status==0:
      vals=[Fraction(float(x)).limit_denominator(100000) for x in sol.x];ok=all(sum(x*y for x,y in zip(row,vals) if x and y)==rhs for row,rhs in zip(A,b));out['outcome']='exact_rational_survival' if ok else 'numerical_survival';out['minimum_variable']=str(min(vals));out['all_equations_verified']=ok;return out
  out['outcome']='no_surviving_branch_found_without_exact_exclusion'
 except Ineligible as e:out.update({'eligible':False,'outcome':'ineligible','reason':str(e)})
 except TimeoutError as e:out['outcome']='budget_incomplete';out['reason']=str(e)
 except VerificationError as e:out['outcome']='unsupported_branch';out['reason']=str(e)
 except Exception as e:out['outcome']='error';out['reason']=repr(e)
 finally:signal.alarm(0);out['seconds']=time.monotonic()-st
 return out

if __name__=='__main__':
 tasks=V.frozen_control_tasks(P);out=[]
 with ProcessPoolExecutor(max_workers=2) as pool:
  for f in as_completed([pool.submit(one,a) for a in tasks]):
   z=f.result();out.append(z);print(z['id'],z['outcome'],flush=True);Path(__file__).with_suffix('.json').write_text(json.dumps({'input_count':len(tasks),'complete':len(out)==len(tasks),'records':sorted(out,key=lambda x:x['id'])},indent=2)+'\n')
