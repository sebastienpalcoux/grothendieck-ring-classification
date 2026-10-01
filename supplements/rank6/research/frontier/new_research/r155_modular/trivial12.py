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
import runpy,contextlib,io,sys,json,itertools
import sympy as sp
P=_TASK_PACKAGE;sys.argv=[str(P/'research/frontier/R6_4_155/verify_forced_twists.py'),'--package',str(P)]
with contextlib.redirect_stdout(io.StringIO()):ns=runpy.run_path(sys.argv[0])
C,dd,W,tab,lab,dat,roots,eps=[ns[k]for k in ['C','d','W','tab','lab','dat','roots','eps']]
known={}
for a,j in enumerate([1,23,25,24,18,19]):
 dl=sum((C(t)*dim for t,dim in zip(dat['lows'][6][a],dat['dims'])),C.zero)
 known[j]=[dl*tab.values[lab[a],v]/(12*dd)for v in W]
for j,k in [(1,0),(23,22),(18,16),(19,17)]:known[k]=[C(e)*x for e,x in zip(eps,known[j])]
vectors=[{1:1,23:-1},{0:1,22:-1},{2:1,5:1},{3:1,6:1},{4:1,7:1},{20:1,21:1},{8:1},{9:1},{10:1},{11:1},{12:1,13:1},{14:1,15:1}]
norms=[sum(c*c for c in v.values())for v in vectors];exps=[(ns['exps'][next(iter(v))]+1)%24 for v in vectors]
H=sp.zeros(12)
for a in [0,1]:
 for b in range(12):
  z=sum((C(c*q)*known[i][j]for i,c in vectors[a].items()for j,q in vectors[b].items()),C.zero)
  if len(z.to_list())>1:raise ValueError('not rational')
  H[a,b]=H[b,a]=sp.Rational(z.to_list()[0])if z else 0
print('known H',H[:2,:],flush=True)
symbols=[]
for a in range(2,12):
 for b in range(a,12):
  q=sp.Symbol('h'+str(a)+'_'+str(b));H[a,b]=H[b,a]=q;symbols.append(q)
N=sp.diag(*norms);Ni=N.inv();equations=[]
for a in [0,1]:
 for b in range(12):
  terms=[(H[a,k]*H[k,b]/norms[k],roots[exps[k]])for k in range(12)]+[(-H[a,b],roots[(-exps[a]-exps[b])%24])]
  for p in range(8):
   eq=0
   for coeff,z in terms:
    raw=[sp.Rational(v)for v in z.to_list()];raw=[0]*(8-len(raw))+raw;eq+=coeff*raw[p]
   if eq!=0:equations.append(eq)
  equations.append(sum(H[a,k]*H[k,b]/norms[k]for k in range(12))-N[a,b])
sol=sp.linsolve(equations,symbols)
if len(sol)!=1:raise ValueError('linear system inconsistent')
H=H.subs(dict(zip(symbols,next(iter(sol)))));free=sorted(H.free_symbols,key=str);print('free',len(free),free,flush=True);print('H',H,flush=True)
json.dump(dict(vectors=vectors,norms=norms,t_exponents=exps,H=[[str(v)for v in row]for row in H.tolist()],free_symbols=[str(v)for v in free]),open(Path(__file__).with_suffix('.json'),'w'),indent=2)
# Full modular and square equations, expand into Q components.
polys=set()
for a in range(12):
 for b in range(a,12):
  eq=sp.expand(sum(H[a,k]*H[k,b]/norms[k]for k in range(12))-N[a,b])
  if eq:polys.add(eq)
  terms=[(H[a,k]*H[k,b]/norms[k],roots[exps[k]])for k in range(12)]+[(-H[a,b],roots[(-exps[a]-exps[b])%24])]
  for p in range(8):
   eq=0
   for coeff,z in terms:
    raw=[sp.Rational(v)for v in z.to_list()];raw=[0]*(8-len(raw))+raw;eq+=coeff*raw[p]
   eq=sp.expand(eq)
   if eq:polys.add(eq)
print('full equations',len(polys),flush=True)
# Extract any new linear constraints first.
linear=[p for p in polys if sp.Poly(p,*free).total_degree()<=1];print('additional linear',len(linear),flush=True)
if linear:
 sol2=sp.linsolve(linear,free);print('linear2',sol2,flush=True)
 if len(sol2)==1:
  sub=dict(zip(free,next(iter(sol2))));H=H.subs(sub);polys={sp.expand(p.subs(sub))for p in polys}-{sp.S.Zero};free=sorted(H.free_symbols,key=str);print('free2',len(free),free,flush=True)
  json.dump(dict(vectors=vectors,norms=norms,t_exponents=exps,H=[[str(v)for v in row]for row in H.tolist()],free_symbols=[str(v)for v in free],equations=[str(p)for p in sorted(polys,key=str)]),open(Path(__file__).with_suffix('.json'),'w'),indent=2)
# Eliminate the quadratic monomials by ordinary rational row reduction.
monomials=[a*b for i,a in enumerate(free)for b in free[i:]]+free+[sp.S.One]
polynomials=[sp.Poly(p,*free)for p in sorted(polys,key=str)]
coefficient_rows=[[p.coeff_monomial(m)for m in monomials]for p in polynomials]
rr,piv=sp.Matrix(coefficient_rows).rref()
linear_consequences=[]
for row in rr.tolist():
 if not any(row[:len(monomials)-len(free)-1]) and any(row[-len(free)-1:]):linear_consequences.append(sum(c*m for c,m in zip(row,monomials)))
print('row-reduced linear consequences',linear_consequences,flush=True)
lin=sp.linsolve(linear_consequences,free);print('linear completion',lin,flush=True)
if len(lin)!=1:raise ValueError('unique rational linear completion required')
solution=dict(zip(free,next(iter(lin))))
if any(v.free_symbols for v in solution.values()):raise ValueError('completion still has variables')
if any(sp.expand(p.subs(solution))!=0 for p in polys):raise ValueError('completed block fails a modular equation')
print('unique completion passes all equations',flush=True)
json.dump(dict(vectors=vectors,norms=norms,t_exponents=exps,H=[[str(v)for v in row]for row in H.tolist()],free_symbols=[str(v)for v in free],groebner=[str(p)for p in linear_consequences],groebner_used=False,linear_consequences=[str(p)for p in linear_consequences],equations=[str(p)for p in sorted(polys,key=str)],unique_solution={str(k):str(v)for k,v in solution.items()}),open(Path(__file__).with_suffix('.json'),'w'),indent=2)
