import json,sys,time,signal
from pathlib import Path
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'software'))
from round4_629_orbits import *
from higher_traces import farkas,check_farkas
from scipy.optimize import linprog,milp,Bounds,LinearConstraint
import numpy as np
rid=sys.argv[1] if len(sys.argv)>1 else 'R6_4_629';h=int(sys.argv[2]) if len(sys.argv)>2 else 3;strong=len(sys.argv)>3
R=next(x['N'] for x in json.load(open(P/'data/census.json')) if x['id']==rid);st=time.monotonic();out={'id':rid,'height':h,'with_verlinde':strong,'branches':[]};p=Path(__file__).with_name(rid+'_orbit_h'+str(h)+('_strong' if strong else '')+'_primal.json')
def stop(*a):raise TimeoutError('840 second budget')
signal.signal(signal.SIGALRM,stop);signal.alarm(840)
try:
 d=ambient.data_for(R,h,15)
 for ix,cols in enumerate(d['lows']):
  why=ambient.low_failure(cols,d['ch'].C,d['ds'],d['D'],d['K'],d['embedding'],d['ch'].du)
  if why:out['branches'].append({'low':ix,'ordinary':why});continue
  for lab in d['tab'].assignments(cols):
   for ep in ambient.indicator_choices(R):
    print('building',ix,lab,ep,flush=True);A,b,meta=refine(R,d,cols,lab,ep,strong)
    rec={'low':ix,'lab':lab,'ep':ep,'meta':meta};out['branches'].append(rec)
    if A is None:rec['outcome']='spectral_exclusion';continue
    print('system',len(A),len(A[0]),'removed',meta['removed_high_variables'],meta['orbit_sizes'],flush=True)
    from scipy.sparse import csr_matrix
    ma=csr_matrix(np.array(A,dtype=float));bb=np.array(b,dtype=float);scale=np.maximum(1,np.maximum(abs(ma).max(axis=1).toarray().ravel(),abs(bb)));ma=ma.multiply((1/scale)[:,None]).tocsr();bb=bb/scale
    lp=linprog(np.zeros(len(A[0])),A_eq=ma,b_eq=bb,bounds=(0,None),options={'time_limit':120});print('LP',lp.status,flush=True)
    y=farkas(A,b) if lp.status==2 else None
    if y is not None:check_farkas(A,b,y);rec.update(outcome='exact_obstruction',ray=y)
    else:
     sol=milp(np.zeros(len(A[0])),integrality=meta['integrality'],bounds=Bounds(0,np.inf),constraints=LinearConstraint(ma,bb,bb),options={'time_limit':180});rec['milp_status']=int(sol.status);print('MILP',sol.status,sol.message,flush=True)
     rec['outcome']='no_exact_obstruction'
     if sol.status==0:
      from fractions import Fraction
      x=[Fraction(float(v)).limit_denominator(1000000) for v in sol.x];ok=all(sum(a*z for a,z in zip(row,x))==rhs for row,rhs in zip(A,b));rec['exact_primal']=ok
      if ok:rec['primal']=[str(z) for z in x]
     p.write_text(json.dumps(out));raise ValueError('surviving branch')
    print('outcome',rec['outcome'],flush=True);p.write_text(json.dumps(out))
 out['outcome']='pseudo_unitary_excluded'
except (TimeoutError,ValueError,Ineligible) as e:out['outcome']=type(e).__name__;out['reason']=str(e)
finally:signal.alarm(0)
out['seconds']=time.monotonic()-st;p.write_text(json.dumps(out));print(out['outcome'],out['seconds'],flush=True)
