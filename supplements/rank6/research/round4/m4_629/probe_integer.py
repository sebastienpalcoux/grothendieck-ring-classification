import json,sys,time,itertools
from pathlib import Path
P=Path(__file__).resolve().parents[3];sys.path[:0]=[str(P/'software'),str(P/'research/round3/quartic')]
import round3_m4 as m
from exact import require
from spectral_induction import Spectrum
from modular_character_induction import rational_rows
from modular_moments import congruence_witness,check_congruence
from scipy.optimize import linprog,milp,Bounds,LinearConstraint
from fractions import Fraction
import numpy as np
import sympy as s
from verlinde_probe import verlinde
R=next(x['N'] for x in json.load(open(P/'data/unresolved_tensors.json')) if x['id']=='R6_4_629');st=time.monotonic();d=m.data_for(R,3,15);tab=d['tab'];C=d['C'];out=[]
for ix,cols in enumerate(d['lows']):
 why=m.low_failure(cols,d['ch'].C,d['ds'],d['D'],d['K'],d['embedding'],d['ch'].du)
 if why:print('lowfailure',ix,why,flush=True);continue
 G,vs=m.high_vectors(d,cols);sp=Spectrum(tab,cols,[(v,None) for v in vs]);vs=[v for v in vs if list(v) not in sp.forbidden];print('low',ix,'high',len(vs),'types',len(set(sp.types)-sp.bad),'missing',sp.missing_low,flush=True)
 if sp.missing_low:continue
 A=[[v[i]*v[j] for v in vs] for i in range(5) for j in range(i,5)];b=[int(G[i,j]) for i in range(5) for j in range(i,5)]
 rows,bs=sp.balance([(v,0) for v in vs],len(vs));A+=rows;b+=bs
 aa=np.array(A,dtype=float);bb=np.array(b,dtype=float)
 so=milp(np.ones(len(vs)),integrality=np.ones(len(vs)),bounds=Bounds(0,np.inf),constraints=LinearConstraint(aa,bb,bb),options={'time_limit':120})
 print('gramMILP',so.status,so.fun if so.status==0 else so.message,flush=True)
 rec={'low':ix,'high_types':vs,'gram_status':int(so.status)}
 if so.status==0:rec['gram_witness']=[int(round(x)) for x in so.x];require(all(sum(x*y for x,y in zip(row,rec['gram_witness']))==val for row,val in zip(A,b)),'inexact gram')
 for lab in tab.assignments(cols):
  AA=[row[:] for row in A];bb=b[:];AA,bb,labels,base=verlinde(R,d,tab,cols,lab,AA,bb,[(v,0) for v in vs]);print('strong',len(AA),len(AA[0]),flush=True)
  co=congruence_witness(AA,bb,[1]*len(AA[0]),primes=(2,3,5));print('congruence',co,flush=True)
  ma=np.array(AA,dtype=float);rb=np.array(bb,dtype=float);scale=np.maximum(1,np.maximum(abs(ma).max(axis=1),abs(rb)));lp=linprog(np.zeros(len(AA[0])),A_eq=ma/scale[:,None],b_eq=rb/scale,bounds=(0,None),options={'time_limit':120})
  print('LP',lp.status,flush=True)
  rr={'lab':lab,'rows':len(AA),'cols':len(AA[0]),'congruence':co,'LPstatus':int(lp.status)}
  if lp.status==0:
   mm=milp(np.zeros(len(AA[0])),integrality=np.ones(len(AA[0])),bounds=Bounds(0,np.inf),constraints=LinearConstraint(ma/scale[:,None],rb/scale,rb/scale),options={'time_limit':120});print('MILP',mm.status,flush=True);rr['MILPstatus']=int(mm.status)
   if mm.status==0:
    x=[int(round(v)) for v in mm.x];exact=all(sum(a*z for a,z in zip(row,x))==rhs for row,rhs in zip(AA,bb));rr['exact']=exact;print('exact',exact,flush=True)
    if exact:rr['x']=x
  rec.setdefault('branches',[]).append(rr)
  out.append(rec);Path(__file__).with_suffix('.json').write_text(json.dumps(out))
  break
print('seconds',time.monotonic()-st,flush=True)
