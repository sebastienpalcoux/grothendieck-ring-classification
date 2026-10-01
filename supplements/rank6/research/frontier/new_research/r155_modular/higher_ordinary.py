# Locate the enclosing frozen release or the explicitly supplied base.
import os as _task_os
from pathlib import Path as _TaskPath
def _find_release():
    if _task_os.environ.get("RANK6_PACKAGE"):
        return _TaskPath(_task_os.environ["RANK6_PACKAGE"]).resolve()
    for _p in _TaskPath(__file__).resolve().parents:
        for _c in (_p, _p / "Rank6_Categorification_M9"):
            if (_c / "software/round3_m4.py").is_file() and (_c / "data/census.json").is_file():
                return _c
    raise FileNotFoundError("Set RANK6_PACKAGE to the extracted multiplicity-nine package")
_TASK_PACKAGE = _find_release()

from pathlib import Path
import runpy,contextlib,io,sys,json,itertools,time,math
import sympy as sp
import numpy as np
P=_TASK_PACKAGE;HERE=Path(__file__).parent;sys.argv=[str(P/'research/frontier/R6_4_155/verify_forced_twists.py'),'--package',str(P)]
with contextlib.redirect_stdout(io.StringIO()):ns=runpy.run_path(sys.argv[0])
C,dims,DB,roots,exps=[ns[k]for k in ['C','dims','DB','roots','exps']];out=json.load(open(HERE/'reconstruction.json'));N=out['fusion_rules'];dual=out['duality'];ii=roots[6]
quaternionic=[N[dual[u]][u][24]for u in range(26)]
print('quaternionic',quaternionic,flush=True)
if any(v%2 for v in quaternionic):raise ValueError('quaternionic multiplicity odd')
weights=[[C.zero]*24 for _ in range(26)]
for i in range(26):
 for j in range(26):
  w=dims[i]*dims[j]/DB;e=(exps[i]-exps[j])%24
  for k in range(26):
   if N[i][j][k]:weights[k][e]+=C(N[i][j][k])*w
inds={q:[sum((v*roots[(q*e)%24]for e,v in enumerate(row)),C.zero)for row in weights]for q in [1,2,3,4,6,8,12,24]}
def sig(v,a):return ns['M'].evaluate(v.to_list(),roots[a%24],C)
results=[];fail=[]
for v in range(26):
 M=np.array(N[v],dtype=object);powers={0:np.eye(26,dtype=object)}
 for n in range(1,25):powers[n]=powers[n-1]@M
 for n in [2,3,4,6,8,12,24]:
  tr=[C(int(powers[n][1,1]))]
  for k in range(1,n):
   g=math.gcd(n,k);q=n//g;a=next(a for a in range(1,24)if math.gcd(a,24)==1 and (a-k//g)%q==0)
   val=sum((C(int(powers[g][1,j]))*inds[q][j]for j in range(26)if powers[g][1,j]),C.zero)
   tr.append(sig(val,a))
  mult=[sum((tr[k]*roots[(-j*k*(24//n))%24]for k in range(n)),C.zero)/C(n)for j in range(n)]
  valid=all(len(z.to_list())<=1 and (not z or z.to_list()[0].denominator==1 and z.to_list()[0]>=0)for z in mult)
  r=dict(simple=v,n=n,dimension=int(powers[n][1,1]),passed=valid)
  if not valid:r['multiplicities']=[str(C.to_sympy(z))for z in mult];fail.append(r);print('FAIL',r,flush=True)
  results.append(r)
print('higher blocks',len(results),'fail',len(fail),flush=True)
json.dump(dict(scope='ordinary B cyclic rotations at selected orders, not all generalized rotations',quaternionic_multiplicities=quaternionic,blocks=len(results),failed=fail,results=results),open(HERE/'higher_ordinary.json','w'),indent=2)
