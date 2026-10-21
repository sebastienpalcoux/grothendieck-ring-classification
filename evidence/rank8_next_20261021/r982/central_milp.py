"""Numerical proposal only; exact candidate verification is mandatory."""
from pathlib import Path
import json,math,sys,time
import numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint
from scipy.sparse import csc_matrix
from domain_probe import rows_for
HERE=Path(__file__).resolve().parent
prefix='central_dual' if '--dual'in sys.argv else'central'
fi=2;bi=4;d,rows,rank=rows_for(prefix+'_frame2');rr=rows[len(d['rhs']):len(d['rhs'])+rank]
report=json.loads((HERE/(prefix+'_frame2_result.json')).read_text());domains=report['propagation']['domains'];phase=json.loads((HERE/'phasecut_frame2.json').read_text());branch=phase['branches'][bi];keep=d['metadata']['source_metadata']['retained_indices'];lower=d['source_lower']
ineq=[[c[j]for j in keep]+[b-sum(x*y for x,y in zip(c,lower))]for c,b in zip(phase['rounded_coefficients'],branch['rounded_rhs'])]
n=len(domains);pars=d['central_action_parities'];p=len(pars);a=[row[:-1]+[0]*p for row in rr];rhs=[row[-1]for row in rr]
lo=[min(v)for v in domains];hi=[max(v)for v in domains]
for k,(j,r,_)in enumerate(pars):
 row=[0]*(n+p);row[j]=1;row[n+k]=-2;a.append(row);rhs.append(r);lo.append((min(domains[j])-r)//2);hi.append((max(domains[j])-r)//2)
sc=[max(1,abs(b),max(map(abs,row)))for row,b in zip(a,rhs)];A=np.array([[x/s for x in row]for row,s in zip(a,sc)]);B=np.array([b/s for b,s in zip(rhs,sc)])
c=[row[:-1]+[0]*p for row in ineq];cs=[max(1,abs(row[-1]),max(map(abs,row[:-1])))for row in ineq];C=np.array([[x/s for x in row]for row,s in zip(c,cs)]);D=np.array([row[-1]/s for row,s in zip(ineq,cs)])
r=milp(np.zeros(n+p),integrality=np.ones(n+p),bounds=Bounds(lo,hi),constraints=[LinearConstraint(csc_matrix(A),B,B),LinearConstraint(csc_matrix(C),-np.inf,D)],options={'time_limit':60})
out={'numerical_status':int(r.status),'numerical_message':str(r.message),'conclusion':'no_exact_conclusion'}
if r.x is not None:
 x=[int(round(v))for v in r.x[:n]]
 if all(x[j]in domains[j]for j in range(n))and all(sum(a*v for a,v in zip(row[:-1],x))==row[-1]for row in rr)and all(sum(a*v for a,v in zip(row[:-1],x))<=row[-1]for row in ineq):out.update(conclusion='exact_integer_necessary_system_survivor',values=x)
(HERE/(prefix+'_milp24.json')).write_text(json.dumps(out,separators=(',',':'))+'\n');print(out['conclusion'],out['numerical_status'],out['numerical_message'],flush=True)
