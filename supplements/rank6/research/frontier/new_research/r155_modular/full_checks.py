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
import runpy,contextlib,io,sys,json,itertools,time
import sympy as sp
import numpy as np
P=_TASK_PACKAGE;HERE=Path(__file__).parent;sys.argv=[str(P/'research/frontier/R6_4_155/verify_forced_twists.py'),'--package',str(P)]
with contextlib.redirect_stdout(io.StringIO()):ns=runpy.run_path(sys.argv[0])
C,dims,DB,roots,exps=[ns[k]for k in ['C','dims','DB','roots','exps']];out=json.load(open(HERE/'reconstruction.json'));N=out['fusion_rules'];dual=out['duality'];ii=roots[6]
nu=[]
for k in range(26):
 v=sum((C(N[i][j][k])*dims[i]*dims[j]*roots[(2*(exps[i]-exps[j]))%24]for i in range(26)for j in range(26)if N[i][j][k]),C.zero)/DB
 nu.append(v)
 print('nu2',k,C.to_sympy(v),'selfdual',dual[k]==k,flush=True)
 if v not in ((C.one,-C.one)if dual[k]==k else (C.zero,)):raise ValueError('FS2 fails '+str(k))
NN=np.array(N,dtype=np.int64);tt=np.array(exps,dtype=np.int64)
# General Vafa formula with correct dual conventions: N_ab^j N_cd^(j*) etc.
fail=[];counter=0
for a,b,c,e in itertools.product(range(26),repeat=4):
 ab,ce,ac,be,ae,bc=[NN[x,y,:]for x,y in [(a,b),(c,e),(a,c),(b,e),(a,e),(b,c)]]
 H=int(ab@ce[dual]);lhs=(exps[a]+exps[b]+exps[c]+exps[e])*H
 rhs=int(tt@(ab*ce[dual]+ac*be[dual]+ae*bc[dual]))
 if (lhs-rhs)%24:fail.append([a,b,c,e,(lhs-rhs)%24]);break
 counter+=1
print('vafa checked',counter,'fail',fail,flush=True)
json.dump(dict(FS2=[str(C.to_sympy(v))for v in nu],Vafa_checked=counter,Vafa_fail=fail),open(HERE/'full_checks.json','w'),indent=2)
