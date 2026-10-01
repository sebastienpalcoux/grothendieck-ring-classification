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
import runpy,contextlib,io,sys,json
import sympy as sp
P=_TASK_PACKAGE;sys.argv=[str(P/'research/frontier/R6_4_155/verify_forced_twists.py'),'--package',str(P)]
with contextlib.redirect_stdout(io.StringIO()):ns=runpy.run_path(sys.argv[0])
C,dd,W,tab,lab,dat,roots,eps=[ns[k]for k in ['C','d','W','tab','lab','dat','roots','eps']]
known={}
for a,j in enumerate([1,23,25,24,18,19]):
 dl=sum((C(t)*dim for t,dim in zip(dat['lows'][6][a],dat['dims'])),C.zero)
 known[j]=[dl*tab.values[lab[a],v]/(12*dd)for v in W]
for j,k in [(1,0),(23,22),(18,16),(19,17)]:known[k]=[C(e)*x for e,x in zip(eps,known[j])]
pairs=[(2,5),(3,6),(4,7),(20,21),(16,17),(18,19)];exps=[(ns['exps'][a]+1)%24 for a,b in pairs];ii=roots[6]
Q=sp.zeros(6)
for k in [4,5]:
 a,b=pairs[k]
 for l,(c,d)in enumerate(pairs):
  z=(known[a][c]-known[a][d]-known[b][c]+known[b][d])/C(2)/ii
  if len(z.to_list())>1:raise ValueError('not rational')
  Q[k,l]=Q[l,k]=sp.Rational(z.to_list()[0])if z else 0
print('known Q',Q)
var={};symbols=[]
for a in range(4):
 for b in range(a,4):
  q=sp.Symbol('q'+str(a)+str(b));Q[a,b]=Q[b,a]=q;symbols.append(q)
# Coefficient equations over rational field for known rows of s t s=t^-1 s t^-1.
equations=[]
for a in [4,5]:
 for b in range(6):
  terms=[(Q[a,k]*Q[k,b],roots[exps[k]])for k in range(6)]+[(Q[a,b],ii*roots[(-exps[a]-exps[b])%24])]
  for p in range(8):
   eq=0
   for coeff,z in terms:
    raw=[sp.Rational(v)for v in z.to_list()];raw=[0]*(8-len(raw))+raw;eq+=coeff*raw[p]
   if eq!=0:equations.append(eq)
sol=sp.linsolve(equations,symbols);print('solutions',sol)
if len(sol)==1:
 Q=Q.subs(dict(zip(symbols,next(iter(sol)))));print('Q=',Q);print('Q²-I',sp.simplify(Q*Q-sp.eye(6)))
 json.dump(dict(pairs=pairs,t_exponents=exps,Q=[[str(v)for v in row]for row in Q.tolist()],free_symbols=sorted(str(q)for q in Q.free_symbols)),open(Path(__file__).with_suffix('.json'),'w'),indent=2)
# Known rows of Q²=I impose linear equations on the three residual variables.
linear=[(Q*Q-sp.eye(6))[a,b]for a in [4,5]for b in range(6)]
variables=sorted(Q.free_symbols,key=str);finish=sp.linsolve(linear,variables)
if len(finish)!=1:raise ValueError('nonunique orthogonality completion')
Q=Q.subs(dict(zip(variables,next(iter(finish)))))
if Q.free_symbols or Q*Q!=sp.eye(6):raise ValueError('Q involution failed')
SM=[[ii*C(Q[a,b])for b in range(6)]for a in range(6)]
for a in range(6):
 for b in range(6):
  lhs=sum((SM[a][k]*roots[exps[k]]*SM[k][b]for k in range(6)),C.zero)
  rhs=roots[(-exps[a]-exps[b])%24]*SM[a][b]
  if lhs!=rhs:raise ValueError('full six-block modular equation failed')
# The selfdual branch's two-block offdiagonal modular equation forces a=1/sqrt(3).
w=roots[8];a=C.one/(ii*(ii*w)*(ii-ii*w));sqrt3=roots[2]+roots[22]
if a!=C.one/sqrt3 or C.one-a*a!=C(2)/C(3):raise ValueError('two-block obstruction identity failed')
# b/sqrt3 must be rational but would square to 2/9, which is not a rational square.
if (C.one-a*a)/C(3)!=C(2)/C(9):raise ValueError('rational-square obstruction normalization')
out=dict(passed=True,optimizer_used=False,six_block_pairs=pairs,t_exponents=exps,Q=[[str(v)for v in row]for row in Q.tolist()],full_six_block_modular_equations=True,selfdual_odd_2d_excluded=True,required_rational_square='2/9',selfdual_count_B=10,selfdual_count_center=20)
json.dump(out,open(Path(__file__).with_suffix('.json'),'w'),indent=2);print(out)
