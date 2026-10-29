"""Height4 necessary center relaxation with full TY eighth-root restriction."""
from pathlib import Path
from fractions import Fraction as Q
import inspect,sys,json,time,math,hashlib,gzip
P=Path(__file__).resolve().parent;ROOT=P.parents[1]/'rank9_m2_research'
sys.path.insert(0,str(ROOT/'phase3/noncomm1975'))
import symmetry as sy
qc=sy.qc;R=qc.inputs('R9_2_1975');data=sy.base(R);original_cols=data['cols']
data['cols']=[(v,z)for v,z in original_cols if z[1] or tuple(v)==(1,0,0,0,0,0,0,0,0)]
source=inspect.getsource(sy.build).replace('return AA,bb,meta','return AA,bb,meta,keys')
ns=dict(vars(sy));ns['base']=lambda _:data;exec(source,ns)
height=int(sys.argv[1]) if len(sys.argv)>1 else 4
A0,b0,meta,keys0=ns['build'](R,height,False)
types,bound=qc.trace_types(2,[2,3],height);col_dims={v:z for v,z in data['cols']};Y=8
assert all(not v[Y] for kind,v,t in keys0 if kind in ('label','anon'))
for tau in [-1,1]:
 start=time.monotonic()
 costs=[(Q(1),Q(0)),(Q(0),Q(1,2)),(Q(0),Q(0)),(Q(0),Q(-1,2)),(Q(-1),Q(0)),(Q(0),Q(-1,2)),(Q(0),Q(0)),(Q(0),Q(1,2))]
 eighths=[tuple(costs[(j*k)%8]for k in range(1,height+1))for j in [1,3]]
 allowed=eighths+([tuple((Q(a**k),Q(0))for k in range(1,height+1))for a in [1,-1]]if tau==1 else [tuple((Q(0)if k%2 else Q((-1)**(k//2)),Q(0))for k in range(1,height+1))])
 keep=[j for j,(kind,v,t) in enumerate(keys0)if kind!='high' or not v[Y] or tuple(types[t])in allowed]
 A=[[row[j]for j in keep]for row in A0];b=list(b0);keys=[keys0[j]for j in keep]
 for k,value in [(k,v)for k,v in [(2,tau),(4,0),(6,tau)]if k<=height]:
  vals=[qc.scale(qc.mul(col_dims[v],types[t][k-1],2),v[Y])if kind=='high' and v[Y]else(Q(0),Q(0))for kind,v,t in keys]
  rhs=qc.scale(data['D'],value)
  for c in range(2):
   row=[z[c]for z in vals];den=math.lcm(*(Q(z).denominator for z in row+[rhs[c]]));A.append([int(z*den)for z in row]);b.append(int(rhs[c]*den))
 print('tau',tau,'system',len(A),len(A[0]),flush=True)
 ray,why=qc.exact_separator(A,b,timeout=60)
 out={'source':'R9_2_1975','tau_sign':tau,'height':height,'rows':len(A),'variables':len(A[0]),'system_sha256':hashlib.sha256(json.dumps([A,b],separators=(',',':')).encode()).hexdigest(),'ray':ray,'solver_report':why,'scope':'Requires audited general-to-PU reduction, integral-center theorem, TY indicator spectrum, and prior full column-domain derivation','result':'exact_separator'if ray else'no_separator','seconds':time.monotonic()-start}
 if ray:
  assert qc.verify_ray(A,b,ray);out['bTy']=sum(a*v for a,v in zip(b,ray));out['min_ATy']=min(sum(A[i][j]*ray[i]for i in range(len(A)))for j in range(len(A[0])))
 if ray is None:
  import numpy as np
  from scipy.optimize import linprog,milp,Bounds,LinearConstraint
  M=np.array(A,dtype=float);rhs=np.array(b,dtype=float);scale=np.maximum(1,np.maximum(np.max(abs(M),axis=1),abs(rhs)))
  matrix=M/scale[:,None];rs=rhs/scale
  sol=linprog(np.ones(len(A[0])),A_eq=matrix,b_eq=rs,bounds=(0,None),method='highs')
  out['primal_lp_status']=sol.status
  if sol.success:
   for denbound in (10,100,1000,1000000):
    vals=[Q(float(x)).limit_denominator(denbound)for x in sol.x]
    if all(sum(a*x for a,x in zip(row,vals))==z for row,z in zip(A,b)):
     out['rational_witness']=[[i,str(x)]for i,x in enumerate(vals)if x];break
   ms=milp(c=np.zeros(len(A[0])),integrality=np.ones(len(A[0])),bounds=Bounds(0,np.inf),constraints=LinearConstraint(matrix,rs,rs),options={'time_limit':30})
   out['milp_status']=ms.status
   if ms.x is not None:
    vals=[int(round(x))for x in ms.x]
    if all(sum(a*x for a,x in zip(row,vals))==z for row,z in zip(A,b)):
     out['integer_witness']=[[i,x]for i,x in enumerate(vals)if x]
 with gzip.open(P/f'ty_spectrum_h{height}_tau{tau}_system.json.gz','wt')as f:json.dump({'A':A,'b':b},f,separators=(',',':'))
 (P/f'ty_spectrum_h{height}_tau{tau}.json').write_text(json.dumps(out,indent=2)+'\n')
 print({k:v for k,v in out.items()if k not in ('ray','rational_witness','integer_witness')},flush=True)
