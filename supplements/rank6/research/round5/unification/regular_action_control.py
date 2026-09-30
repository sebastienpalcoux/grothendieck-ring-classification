"""Nonselfdual regular-action positive control from Z(Vec_C3)."""
import hashlib,itertools,json,sys
from pathlib import Path
import sympy as s
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'software'))
from exact import require
from round5_low_actions import low_action_system,general_action_system,enumerate_actions

n=3;objects=list(itertools.product(range(n),repeat=2));r=len(objects)
add=lambda x,y:tuple((a+b)%n for a,b in zip(x,y))
star=[objects.index(tuple(-a%n for a in x)) for x in objects]
R=[[[int(k==(i+j)%n) for k in range(n)] for j in range(n)] for i in range(n)]
W=[[int(i==g) for i in range(n)] for g,k in objects]
N=[[[int(z==add(x,y)) for z in objects] for y in objects] for x in objects]
words=[w for degree in (2,3) for w in itertools.combinations_with_replacement(range(1,n),degree)]
U=[[int(x==(0,sum(w)%n)) for x in objects] for w in words]
poly=list(map(int,s.Poly((s.Symbol('t')**3-1)**3,s.Symbol('t')).all_coeffs()))
checks=[]
for a in (1,2):
 system=low_action_system(R,W,star,words,U,a,known_actions=[N[star[a]]],trace=0)
 result=enumerate_actions(system,expected_charpoly=poly)
 require(N[a] in result['matrices'],'actual nonselfdual low action excluded')
 checks.append(dict(a=a,stage='low',affine_solutions=result['affine_solutions'],spectral_survivors=len(result['matrices'])))
for a in range(3,r):
 known={b:N[b] for b in range(1,r) if b!=a}
 system=general_action_system(R,W,star,a,known);result=enumerate_actions(system)
 require(result['matrices']==[N[a]],'fully constrained categorical action not recovered')
 checks.append(dict(a=a,stage='general',affine_solutions=result['affine_solutions']))
out=dict(passed=True,optimizer_used=False,python_optimized=not __debug__,category='Vec(C3)',center='Vec(C3 x C3) with double braiding',duality=star,checks=checks,source_sha256={})
for name in ['software/round5_low_actions.py','research/round5/unification/regular_action_control.py']:
 out['source_sha256'][name]=hashlib.sha256((P/name).read_bytes()).hexdigest()
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
