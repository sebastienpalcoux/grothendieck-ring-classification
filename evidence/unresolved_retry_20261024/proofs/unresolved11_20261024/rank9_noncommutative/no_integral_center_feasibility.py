from pathlib import Path
import sys,json,time,hashlib
P=Path(__file__).resolve().parent;ROOT=P.parents[1]/'rank9_m2_research'
sys.path.insert(0,str(ROOT/'phase3/noncomm1975'))
import symmetry as sy
start=time.monotonic();orig=sy.base;removed=[]
def base(R):
 d=orig(R);keep=[]
 for v,z in d['cols']:
  if z[1] or tuple(v)==(1,0,0,0,0,0,0,0,0):keep.append((v,z))
  else:removed.append({'v':v,'dimension':list(map(str,z))})
 d['cols']=keep
 return d
sy.base=base
A,b,meta=sy.build(sy.qc.inputs('R9_2_1975'),6)
print('system',len(A),len(A[0]),'removed',len(removed),flush=True)
import numpy as np
from scipy.optimize import linprog,milp,Bounds,LinearConstraint
from fractions import Fraction
M=np.array(A,dtype=float);rhs=np.array(b,dtype=float)
scale=np.maximum(1,np.maximum(np.max(abs(M),axis=1),abs(rhs)));matrix=M/scale[:,None];r=rhs/scale
sol=linprog(np.ones(len(A[0])),A_eq=matrix,b_eq=r,bounds=(0,None),method='highs')
print('primal LP',sol.status,sol.message,flush=True)
out={'rows':len(A),'columns':len(A[0]),'lp_status':sol.status,'scope':'Exact rational feasibility of a necessary relaxation only; no fusion-category existence claimed.'}
if sol.success:
 for bound in (10,100,1000,1000000):
  vals=[Fraction(float(x)).limit_denominator(bound)for x in sol.x]
  if all(sum(a*x for a,x in zip(row,vals))==z for row,z in zip(A,b)):
   out['rational_witness']=[[i,str(x)]for i,x in enumerate(vals)if x];print('exact rational witness',bound,'support',len(out['rational_witness']),flush=True);break
 ms=milp(c=np.zeros(len(A[0])),integrality=np.ones(len(A[0])),bounds=Bounds(0,np.inf),constraints=LinearConstraint(matrix,r,r),options={'time_limit':45})
 print('MILP',ms.status,ms.message,flush=True);out['milp_status']=ms.status
 if ms.x is not None:
  vals=[int(round(x))for x in ms.x]
  if all(sum(a*x for a,x in zip(row,vals))==z for row,z in zip(A,b)):
   out['integer_witness']=[[i,x]for i,x in enumerate(vals)if x];print('exact integer witness',len(out['integer_witness']),flush=True)
import gzip
out['system_hash']=hashlib.sha256(json.dumps([A,b],separators=(',',':')).encode()).hexdigest()
with gzip.open(P/'no_integral_center_system.json.gz','wt') as f:json.dump({'A':A,'b':b},f,separators=(',',':'))
(P/'no_integral_center_feasibility.json').write_text(json.dumps(out,indent=2)+'\n')
