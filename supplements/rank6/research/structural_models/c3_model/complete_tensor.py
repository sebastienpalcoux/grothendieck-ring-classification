"""Exact, exhaustive rank-six tensor completion from source induction.
Run after exact_certificate.py. Uses integer arithmetic for the finite search.
"""
from pathlib import Path
import itertools,json,sympy as s
P=Path(__file__).parent;c=json.load(open(P/'exact_certificate.json'));q=json.load(open(P/'probe_data.json'));W=list(map(tuple,q['weights']));E=[W.index(tuple(w)) for w in c['even_weights']];B=c['free_induction_matrix'];source=q['N'];
if s.Matrix(B).rank()!=5:raise ValueError('central image rank')
target=json.load(open(P/'target_R91.json'));records=[]
for star in [[0,2,1,3,4,5],list(range(6))]:
 parent={t:t for t in itertools.product(range(6),repeat=3)}
 def root(t):
  while parent[t]!=t:t=parent[t]
  return t
 def join(a,b):parent[root(a)]=root(b)
 for i,j,k in parent:
  join((i,j,k),(j,i,k));join((i,j,k),(star[i],k,j));join((i,j,k),(star[j],star[i],star[k]))
 fixed={}
 def fix(t,v):
  a=root(t)
  if a in fixed and fixed[a]!=v:raise ValueError(('fixed conflict',t,v))
  fixed[a]=v
 for j in range(6):
  for k in range(6):fix((0,j,k),int(j==k))
 # Local Ising multiplication follows from the conformal embedding.
 for i,j,terms in [(4,4,{0:1}),(4,3,{3:1}),(3,3,{0:1,4:1})]:
  for k in range(6):fix((i,j,k),terms.get(k,0))
 keys=sorted({root(t) for t in parent}-fixed.keys());syms=s.symbols('a:'+str(len(keys)));values=fixed|dict(zip(keys,syms));T=[[[values[root((i,j,k))] for k in range(6)] for j in range(6)] for i in range(6)]
 equations=[]
 for i,a in enumerate(E):
  for j,b in enumerate(E):
   for k in range(6):
    equations.append(sum(B[i][u]*B[j][v]*T[u][v][k] for u in range(6) for v in range(6))-sum(source[a][b][w]*B[l][k] for l,w in enumerate(E)))
 sol=list(s.linsolve(equations,syms))
 if len(sol)!=1:raise ValueError('not unique affine solution')
 subst=dict(zip(syms,sol[0]));result=[[[s.sympify(v).subs(subst) for v in row] for row in m] for m in T]
 free=sorted(set().union(*(v.free_symbols for m in result for row in m for v in row)),key=str)
 # Prove the cube bound from coordinatewise nonnegativity: for each free
 # variable there is a coefficient -c*v+b (c>0, 0<=b/c<=4).
 for v in free:
  if not any(t.coeff(v)<0 and all(t.coeff(w)<=0 for w in free) and 0<=t.subs(dict.fromkeys(free,0))/(-t.coeff(v))<=4 for m in result for row in m for t in row):raise ValueError(('missing upper bound',v))
 denom=int(s.ilcm(*(s.denom(t) for m in result for row in m for v in row for t in s.Poly(v,*free).coeffs())))
 flat=[s.Poly(v*denom,*free) for m in result for row in m for v in row]
 coeffs=[([int(p.coeff_monomial(v)) for v in free],int(p.coeff_monomial(1))) for p in flat]
 solutions=[]
 for tup in itertools.product(range(5),repeat=len(free)):
  nums=[b+sum(a*t for a,t in zip(aa,tup)) for aa,b in coeffs]
  if any(n<0 or n%denom for n in nums):continue
  vals=[n//denom for n in nums];rr=[[[vals[36*i+6*j+k] for k in range(6)] for j in range(6)] for i in range(6)]
  if any(sum(rr[i][j][a]*rr[a][k][l] for a in range(6))!=sum(rr[j][k][a]*rr[i][a][l] for a in range(6)) for i,j,k,l in itertools.product(range(6),repeat=4)):continue
  M=sum((s.Matrix(rr[i])*s.Matrix(rr[star[i]]) for i in range(6)),s.zeros(6));cp=str(s.factor(M.charpoly().as_expr()))
  solutions.append({'fusion_tensor':rr,'x_squared':rr[1][1],'equals_R91':rr==target,'casimir_characteristic_polynomial':cp})
 expected=1 if star[1]==2 else 3
 if len(solutions)!=expected:raise ValueError(('candidate count',len(solutions)))
 if star[1]==2 and not solutions[0]['equals_R91']:raise ValueError('R91 tensor mismatch')
 records.append({'star':star,'free_parameters':list(map(str,free)),'affine_solution':list(map(str,sol[0])),'search_bound':[0,4],'search_size':5**len(free),'exact_associativity_checks_per_candidate':6**4,'solutions':solutions})
json.dump(records,open(P/'completion_certificate.json','w'),indent=2)
print('Exact completion:',[(r['star'],len(r['solutions'])) for r in records])
