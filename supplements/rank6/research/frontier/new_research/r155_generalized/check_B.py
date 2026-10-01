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

"""All rank-26 B targets in Z(B)=B x B^rev, generalized order two."""
from pathlib import Path
import sys,runpy,contextlib,io,json,time,hashlib
import sympy as sp
import numpy as np
HERE=Path(__file__).resolve().parent
P=_TASK_PACKAGE
sys.argv=[str(P/'research/frontier/R6_4_155/verify_forced_twists.py'),'--package',str(P)]
with contextlib.redirect_stdout(io.StringIO()):ns=runpy.run_path(sys.argv[0])
C,M,roots,tt=[ns[k]for k in ('C','M','roots','exps')]
src=HERE.parent/'r155_modular/reconstruction.json';rec=json.loads(src.read_text())
S=np.array([[M.evaluate([sp.Rational(x)for x in v],C.unit,C)for v in row]for row in rec['normalized_S']],dtype=object)
N=np.array(rec['fusion_rules'],dtype=np.int64)
dual=rec['duality']
z=sp.Symbol('z');K=sp.QQ.alg_field_from_poly(sp.Poly(sp.cyclotomic_poly(48,z),z),alias='z');zz=K.unit
def emb(v):return M.evaluate(v.to_list(),zz**2,K)
left=np.array([[S[i,j]*roots[(2*tt[j])%24]for j in range(26)]for i in range(26)],dtype=object)
right=np.array([[S[dual[i],j]*roots[(-2*tt[j])%24]for j in range(26)]for i in range(26)],dtype=object).T
left1=np.array([[S[i,j]*roots[tt[j]]for j in range(26)]for i in range(26)],dtype=object)
right1=np.array([[S[dual[i],j]*roots[(-tt[j])%24]for j in range(26)]for i in range(26)],dtype=object).T
failed=[];rows=[];start=time.monotonic()
for k in range(26):
 Nk=np.array([[C(int(N[a,b,k]))for b in range(26)]for a in range(26)],dtype=object)
 degree1=left1@Nk@right1
 for i in range(26):
  for j in range(26):
   if degree1[i,j]!=C(int(N[i,j,k]))*roots[(tt[j]-tt[i])%24]:
    raise ValueError(('degree-one normalization',k,i,j))
 traces=left@Nk@right
 for i in range(26):
  for j in range(26):
   dim=int(N[i,j,:]@N[k,k,:])
   trace=emb(traces[i,j])*zz**((tt[i]-tt[j])%48)
   mult=[(K(dim)+trace)/K(2),(K(dim)-trace)/K(2)]
   ok=all(len(a.to_list())<=1 and(not a or a.to_list()[0].denominator==1 and a.to_list()[0]>=0)for a in mult)
   row={'base':k,'target':[i,j],'dimension':dim,'multiplicities':[str(K.to_sympy(a))for a in mult],'passed':ok}
   rows.append(row)
   if not ok:
    failed.append(row)
    if len(failed)<=5:print('FAIL',row,flush=True)
 print('base',k,'failed',len(failed),'seconds',time.monotonic()-start,flush=True)
(HERE/'B_certificate.json').write_text(json.dumps({'blocks':len(rows),'degree_one_checks':26**3,'passed':not failed,'failed':failed,
 'scope':'26 B simples times all 676 targets in Z(B), order two only',
 'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'rows':rows},indent=2)+'\n')
