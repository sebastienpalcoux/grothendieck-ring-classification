"""Integer-core/full-phase proposal with exact rational joint witness replay."""
from pathlib import Path
import json,math,sys,time
from fractions import Fraction
import numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint
from scipy.sparse import coo_matrix
from joint_phase import Joint,p
HERE=Path(__file__).resolve().parent

def main():
 start=time.monotonic();s=json.loads((HERE/'joint_phase_system.json').read_text());d=json.loads((HERE/'central_dual_frame2_system.json').read_text());dom=json.loads((HERE/'central_dual_frame2_result.json').read_text())['propagation']['domains']
 cols=[{int(i):int(a)for i,a in c.items()}for c in s['columns']];rhs=s['rhs'];n=len(cols);m=len(rhs);nc=s['core_variables'];pars=d['central_action_parities']
 lower=[0]*n;upper=[np.inf]*n;integral=[1]*nc+[0]*(n-nc)
 for k,(j,residue,_)in enumerate(pars):
  row=len(rhs);r=(residue-s['original_bounds'][j][0])%2;rhs.append(r);cols[j][row]=1;cols.append({row:-2});lower.append(0);upper.append((max(dom[j])-s['original_bounds'][j][0]-r)//2);integral.append(1)
 scales=[max(1,abs(b))for b in rhs]
 for col in cols:
  for i,a in col.items():scales[i]=max(scales[i],abs(a))
 rr=[];cc=[];vv=[]
 for j,col in enumerate(cols):
  for i,a in col.items():rr.append(i);cc.append(j);vv.append(a/scales[i])
 A=coo_matrix((vv,(rr,cc)),shape=(len(rhs),len(cols))).tocsc();b=np.array([a/v for a,v in zip(rhs,scales)])
 ans=milp(np.zeros(len(cols)),integrality=np.array(integral),bounds=Bounds(lower,upper),constraints=LinearConstraint(A,b,b),options={'time_limit':300,'mip_rel_gap':0})
 out={'scope':'integer_core_with_full_continuous_phase_necessary_system','numerical_status':int(ans.status),'numerical_message':str(ans.message),'status':'no_exact_joint_integer_conclusion','seconds':time.monotonic()-start}
 if ans.x is not None:
  shifted=[int(round(v))for v in ans.x[:nc]];actual=[v+s['original_bounds'][j][0]for j,v in enumerate(shifted)]
  if all(actual[j]in dom[j]for j in range(nc)) and all(actual[j]%2==r for j,r,_ in pars):
   # Fix only the actual integer variables, then reconstruct phase weights
   # exactly. Numerical phase weights are never accepted as a certificate.
   b=list(s['rhs'])
   # s['rhs'] was aliased before appended parity rows; discard them here.
   b=b[:m]
   sourcecols=[{int(i):int(a)for i,a in c.items()}for c in s['columns']]
   for j,value in enumerate(shifted):
    for i,a in sourcecols[j].items():b[i]-=a*value
   J=Joint(sourcecols[nc:],b);rows=p.old.cg.active_rows(J,range(J.nvars));res,diag=p.old.cg.phase_one(rows,b,J.nvars,120)
   out['conditional_phase_numerical']=diag
   if res.success and res.fun<1e-7:
    primal=p.old.cg.exact_feasible(J,list(range(J.nvars)),b,res.x[:J.nvars])
    if primal is not None:
     total=[Fraction(0)]*m
     for j,w in zip(primal['indices'],map(Fraction,primal['weights'])):
      if w<0:raise AssertionError('negative phase witness')
      for i,a in J.column(j).items():total[i]+=w*a
     if total!=b:raise AssertionError('joint integer phase witness fails')
     out.update(status='exact_integer_core_and_rational_full_phase_survivor',integer_core_values=actual,shifted_integer_core_values=shifted,phase_certificate=primal)
 (HERE/'joint_integer_result.json').write_text(json.dumps(out,separators=(',',':'))+'\n');print(out['status'],out['numerical_status'],out['numerical_message'],'seconds',time.monotonic()-start,flush=True)
if __name__=='__main__':main()
