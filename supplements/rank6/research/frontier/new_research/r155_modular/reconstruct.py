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
C,dd,W,tab,lab,dat,roots,eps=[ns[k]for k in ['C','d','W','tab','lab','dat','roots','eps']];ii=roots[6]
known={}
for a,j in enumerate([1,23,25,24,18,19]):
 dl=sum((C(t)*dim for t,dim in zip(dat['lows'][6][a],dat['dims'])),C.zero)
 known[j]=[dl*tab.values[lab[a],v]/(12*dd)for v in W]
for j,k in [(1,0),(23,22),(18,16),(19,17)]:known[k]=[C(e)*x for e,x in zip(eps,known[j])]
D=json.load(open(HERE/'trivial12.json'));variables={v:sp.Symbol(v)for v in D['free_symbols']};grob=[sp.sympify(p,locals=variables)for p in D['groebner']];solutions=sp.solve(grob,list(variables.values()));H=[[C(sp.sympify(x,locals=variables).subs(solutions))for x in row]for row in D['H']];vectors=[{int(k):v for k,v in r.items()}for r in D['vectors']];blocks=[(vectors,H)]
vectors2=[{1:1,23:1},{0:1,22:1},{16:1,17:1},{18:1,19:1},{24:1},{25:1}]
H2=[[sum((C(c*q)*known[i][j]for i,c in v.items()for j,q in w.items()),C.zero)for w in vectors2]for v in vectors2];blocks.append((vectors2,H2))
D6=json.load(open(HERE/'chi_i_completion.json'));v6=[{a:1,b:-1}for a,b in D6['six_block_pairs']];H6=[[2*ii*C(sp.Rational(q))for q in row]for row in D6['Q']];blocks.append((v6,H6));blocks.append(([{12:1,13:-1},{14:1,15:-1}],[[2*ii,C.zero],[C.zero,2*ii]]))
S=[[C.zero]*26 for _ in range(26)]
for vv,hh in blocks:
 nn=[sum(c*c for c in v.values())for v in vv]
 for i,v in enumerate(vv):
  for j,w in enumerate(vv):
   for a,c in v.items():
    for b,q in w.items():S[a][b]+=hh[i][j]*C(c*q)/C(nn[i]*nn[j])
for j,row in known.items():
 if S[j]!=row:raise ValueError('known rows mismatch')
if any(S[i][j]!=S[j][i]for i in range(26)for j in range(26)):raise ValueError('not symmetric')
dual=list(range(26))
for a,b in [(2,5),(3,6),(4,7),(12,13),(14,15),(16,17),(18,19),(20,21)]:dual[a]=b;dual[b]=a
texps=[(e+1)%24 for e in ns['exps']]
for i in range(26):
 for j in range(26):
  if sum((S[i][k]*S[k][j]for k in range(26)),C.zero)!=C(int(dual[i]==j)):raise ValueError('square')
  if sum((S[i][k]*roots[texps[k]]*S[k][j]for k in range(26)),C.zero)!=roots[(-texps[i]-texps[j])%24]*S[i][j]:raise ValueError('modular')
print('full modular identities pass',flush=True)
z=np.exp(2j*np.pi/24)
def complex_(x):
 rr=x.to_list();return sum(complex(v)*z**(len(rr)-1-i)for i,v in enumerate(rr))
SS=np.array([[complex_(x)for x in row]for row in S]);N=np.einsum('il,jl,kl,l->ijk',SS,SS,SS[dual,:],1/SS[1,:]);error=np.abs(N.imag)+np.abs(N.real-np.rint(N.real))+np.maximum(0,-N.real);ind=np.unravel_index(np.argmax(error),error.shape);print('max error',ind,N[ind],error[ind],flush=True)
out=dict(scope='unique modular S candidate forced by necessary constraints',normalized_S=[[[str(q)for q in x.to_list()]for x in row]for row in S],duality=dual,unit=1,full_modular_equations=True)
if error[ind]>1e-6:
 i,j,k=map(int,ind);v=sum((S[i][l]*S[j][l]*S[dual[k]][l]/S[1][l]for l in range(26)),C.zero);out['failed_verlinde']={'indices':[i,j,k],'value':str(C.to_sympy(v)),'coeffs':[str(q)for q in v.to_list()]};print('exact failed',out['failed_verlinde'],flush=True)
else:
 NN=np.rint(N.real).astype(int);print('numeric integral candidate',flush=True)
 # Exact verification by every N_i S = S diag(S_i/S_0), cheaper sparse integer multiplication.
 for i in range(26):
  for j in range(26):
   for l in range(26):
    if sum((C(int(NN[i,j,k]))*S[k][l]for k in range(26)if NN[i,j,k]),C.zero)!=S[i][l]*S[j][l]/S[1][l]:raise ValueError('exact fusion diagonalization')
 print('all fusion exactly integral nonnegative',flush=True);out['fusion_rules']=NN.tolist();out['exact_integral_nonnegative_verlinde']=True
json.dump(out,open(HERE/'reconstruction.json','w'),indent=2)
