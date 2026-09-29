import sys,json,time,signal,traceback
from pathlib import Path
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'software'));import round4_higher_real as m
from scipy.optimize import milp,LinearConstraint,Bounds
import numpy as np
from fractions import Fraction
rid='R6_6_1035';R=next(r['N']for r in json.load(open(P/'data/census.json'))if r['id']==rid);st=time.monotonic();out={'id':rid,'branches':[]};p=Path(__file__).with_suffix('.json')
def stop(*a):raise TimeoutError('840-second budget')
signal.signal(signal.SIGALRM,stop);signal.alarm(840)
try:
 d=m.data_for(R);tab=d['tab'];print('data',time.monotonic()-st,flush=True)
 for ix in[1,3]:
  cols=d['lows'][ix]
  for lab in tab.assignments(cols):
   for ep in m.ambient.indicator_choices(R):
    if ep[0]!=1 or ep[3]!=1:continue
    A,b,meta=m.system(R,d,cols,ep,lab);base=len(A[0]);A,b=m.add_verlinde(R,d,cols,lab,A,b,meta['labels']);print('system',ix,ep,len(A),len(A[0]),time.monotonic()-st,flush=True);y=m.farkas(A,b);print('ray',y is not None,time.monotonic()-st,flush=True);rec={'low':ix,'labelling':list(lab),'indicators':list(ep),'system':meta,'rows':len(A),'variables':len(A[0]),'ray':y};out['branches'].append(rec);p.write_text(json.dumps(out,separators=(',',':'))+'\n')
    if y is None:
     aa=np.array(A,float);bb=np.array(b,float);scale=np.maximum(1,np.maximum(abs(aa).max(axis=1),abs(bb)));integ=[int(j<len(meta['labels'])or j>=base)for j in range(len(A[0]))];sol=milp(np.zeros(len(A[0])),integrality=integ,bounds=Bounds(0,np.inf),constraints=LinearConstraint(aa/scale[:,None],bb/scale,bb/scale),options={'time_limit':120});rec['milp_status']=int(sol.status);print('MILP',sol.status,sol.message,time.monotonic()-st,flush=True)
     if sol.status==0:
      vv=[Fraction(float(z)).limit_denominator(10**6)for z in sol.x];rec['exact_primal']=all(sum(a*z for a,z in zip(row,vv))==rhs for row,rhs in zip(A,b));rec['primal']=[str(z)for z in vv];print('exactprimal',rec['exact_primal'],flush=True)
 out['outcome']='pseudo_unitary_excluded'if all(r['ray']is not None for r in out['branches'])else'no_exact_obstruction'
except Exception as e:out.update(outcome='budget_incomplete'if isinstance(e,TimeoutError)else'error',reason=str(e));traceback.print_exc()
finally:signal.alarm(0);out['seconds']=time.monotonic()-st;p.write_text(json.dumps(out,separators=(',',':'))+'\n')
