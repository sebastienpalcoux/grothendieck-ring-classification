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
ray,why=sy.qc.exact_separator(A,b,timeout=45)
out={'scope':'Relaxation strengthened by Z(C)_int=Vec, not an independent categorical proof','rows':len(A),'columns':len(A[0]),'removed_integral_columns':removed,'system_hash':hashlib.sha256(json.dumps([A,b],separators=(',',':')).encode()).hexdigest(),'lp':why,'ray':ray,'seconds':time.monotonic()-start}
if ray:assert sy.qc.verify_ray(A,b,ray);out['result']='LP_infeasible_exact'
else:
 out['result']='LP_no_obstruction'
 import z3
 solver=z3.Solver();solver.set(timeout=45000);xs=[z3.Int('x'+str(i))for i in range(len(A[0]))]
 solver.add(*[x>=0 for x in xs]);solver.add(*[z3.Sum([v*x for v,x in zip(row,xs)if v])==rhs for row,rhs in zip(A,b)])
 ans=solver.check();out['integer_result']=str(ans)
 if ans==z3.sat:
  vv=[solver.model().eval(x).as_long()for x in xs]
  assert all(sum(a*x for a,x in zip(row,vv))==rhs for row,rhs in zip(A,b))
  out['integer_witness']=[[i,x]for i,x in enumerate(vv)if x]
 else:out['integer_reason']=solver.reason_unknown()
(P/'no_integral_center_probe.json').write_text(json.dumps(out,indent=2)+'\n')
print({k:v for k,v in out.items()if k not in('removed_integral_columns','ray','integer_witness')},flush=True)
