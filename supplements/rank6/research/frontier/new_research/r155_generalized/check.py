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
import sys,runpy,contextlib,io,json,math,time
from functools import lru_cache
import sympy as sp

HERE=Path(__file__).resolve().parent
P=_TASK_PACKAGE
sys.argv=[str(P/'research/frontier/R6_4_155/verify_forced_twists.py'),'--package',str(P)]
with contextlib.redirect_stdout(io.StringIO()):ns=runpy.run_path(sys.argv[0])
C,M,R,W,roots,exps,dat=[ns[k]for k in ('C','M','R','W','roots','exps','dat')]
rec=json.loads((HERE.parent/'r155_modular/reconstruction.json').read_text())
S=[[M.evaluate([sp.Rational(x) for x in v],C.unit,C) for v in row]for row in rec['normalized_S']]
sqrt2=(ns['d']-C(4))/C(3)
# Identify the semion underlying invertible by its leaf permutation X<->gX.
g=next(i for i in range(1,6)if R[i][i][0] and R[i][1][2])
gp=[next(k for k,v in enumerate(R[g][j])if v)for j in range(6)]
WW=W+[tuple(v[gp[j]]for j in range(6))for v in W]
tt=exps+[(x+6)%24 for x in exps]
SS=[[S[i%26][j%26]*(C(-1)if i>=26 and j>=26 else C.one)/sqrt2
     for j in range(52)]for i in range(52)]

def mul(a,b):
 return tuple(sum(a[i]*b[j]*R[i][j][k]for i in range(6)for j in range(6))for k in range(6))
@lru_cache(None)
def power(x,n):
 if n==0:return (1,0,0,0,0,0)
 return mul(power(x,n-1),tuple(int(i==x)for i in range(6)))
@lru_cache(None)
def ind(x,r,n,z):
 vp=power(x,r)
 return sum((SS[z][j]*roots[(n*tt[j])%24]*sum(WW[j][k]*vp[k]for k in range(6))
             for j in range(52)),C.zero)

@lru_cache(None)
def ext(L):
 z=sp.Symbol('z');return sp.QQ.alg_field_from_poly(sp.Poly(sp.cyclotomic_poly(L,z),z),alias='z')
@lru_cache(None)
def embed(v,L):
 K=ext(L);return M.evaluate(v.to_list(),K.unit**(L//24),K)
def autom(v,L,ell):
 K=ext(L);return M.evaluate(v.to_list(),K.unit**ell,K)
def unit_lift(k,q,L):return next(j for j in range(1,L)if math.gcd(j,L)==1 and (j-k)%q==0)

# Degree-one target-twist convention checks every central object and base simple.
for x in range(6):
 for z in range(52):
  vv=ind(x,1,1,z)
  expected=C(WW[z][x])*roots[(-tt[z])%24]
  if vv!=expected:raise ValueError(('degree one fails',x,z,C.to_sympy(vv),C.to_sympy(expected)))
print('All 312 degree-one normalizations pass',flush=True)
rows=[];failed=[];start=time.monotonic()
for n in range(2,25):
 L=24*n;K=ext(L);zz=K.unit
 for x in range(6):
  for z in range(52):
   dim=sum(WW[z][j]*power(x,n)[j]for j in range(6))
   tr=[K(dim)]
   for k in range(1,n):
    r=math.gcd(n,k);q=n//r;kk=k//r
    v=embed(ind(x,r,q,z),L)*zz**((tt[z]*L//(24*q))%L)
    tr.append(autom(v,L,unit_lift(kk,q,L)))
   mult=[sum((tr[k]*zz**((-j*k*(L//n))%L)for k in range(n)),K.zero)/K(n)for j in range(n)]
   ok=all(len(a.to_list())<=1 and(not a or a.to_list()[0].denominator==1 and a.to_list()[0]>=0)for a in mult)
   row={'n':n,'base_simple':x,'central_simple':z,'dimension':dim,'passed':ok,
        'multiplicities':[str(K.to_sympy(a))for a in mult]}
   rows.append(row)
   if not ok:
    failed.append(row);print('FAIL',row,flush=True)
 print('order',n,'blocks',len(rows),'failed',len(failed),'seconds',time.monotonic()-start,flush=True)
out={'degree_one_checks':312,'rotation_blocks':len(rows),'failed':failed,'all_passed':not failed,
     'source':'r155_modular/reconstruction.json','scope':'all 52 central targets and six original base simples at orders 2 through 24',
     'rows':rows}
(HERE/'certificate.json').write_text(json.dumps(out,indent=2)+'\n')
