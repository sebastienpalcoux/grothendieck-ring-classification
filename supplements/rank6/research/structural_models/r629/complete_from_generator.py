import json,itertools,sympy as s
from pathlib import Path
P=Path(__file__).parent
def require(value,message):
 if not value:raise ValueError(message)
target=next(r['N'] for r in json.load(open(P.parent/'data/model_input_tensors.json')) if r['id']=='R6_4_629')
graph=json.load(open(P/'graph_extraction.json'))['matrices']['brown']
order=[1,3,7,8,4,6]
M=s.Matrix([[graph[i-1][j-1] for j in order] for i in order])
N0=[s.eye(6).tolist(),M.tolist()]
require(M.tolist()==target[1],'Extracted source generator differs from target')
automorphisms=[]
for tail in itertools.permutations(range(2,6)):
 p=[0,1]+list(tail)
 if all(M[p[i],p[j]]==M[i,j] for i in range(6) for j in range(6)):automorphisms.append(p)
require(automorphisms==[list(range(6)),[0,1,3,2,4,5]],'Unexpected duality automorphisms')
print('Generator characteristic polynomial:',s.factor(M.charpoly().as_expr()))
# Identify commutative fusion tensor coefficients by Frobenius reciprocity.
records=[]
for star in [list(range(6)),[0,1,3,2,4,5]]:
 parent={t:t for t in itertools.product(range(6),repeat=3)}
 def root(t):
  while parent[t]!=t:t=parent[t]
  return t
 def join(a,b):parent[root(a)]=root(b)
 for i,j,k in parent:
  join((i,j,k),(j,i,k));join((i,j,k),(star[i],k,j));join((i,j,k),(star[j],star[i],star[k]))
 orbits={root(t) for t in parent}
 vals={};conflict=False
 for i in [0,1]:
  for j in range(6):
   for k in range(6):
    r=root((i,j,k));v=N0[i][j][k]
    if r in vals and vals[r]!=v:conflict=True
    vals[r]=v
 syms=s.symbols('a:'+str(len(orbits-vals.keys())))
 vals.update(zip(sorted(orbits-vals.keys()),syms))
 N=[s.Matrix(6,6,lambda j,k:vals[root((i,j,k))]) for i in range(6)]
 eq=[]
 for i in range(6):
  m=N[i]*N[1]-sum((N[1][i,k]*N[k] for k in range(6)),s.zeros(6))
  eq+=list(m)
 sol=list(s.linsolve(eq,syms))[0];subs=dict(zip(syms,sol));N=[m.subs(subs) for m in N]
 free=set().union(*(m.free_symbols for m in N))
 print('star',star,'free',free)
 print('N2',N[2])
 eq=set()
 for i in range(6):
  for j in range(6):
   m=N[i]*N[j]-sum((N[i][j,k]*N[k] for k in range(6)),s.zeros(6))
   eq.update(s.factor(x) for x in m if x!=0)
 eq.discard(s.Integer(0))
 print('associativity equations',eq)
 require(not conflict,'Unit and generator contradict Frobenius reciprocity')
 require(not eq,'Some full associativity identities failed')
 rec=dict(star=star,free=[str(x) for x in free],matrices=[[[str(x) for x in row] for row in m.tolist()] for m in N],associativity_equations=list(map(str,eq)))
 if star==list(range(6)):
  require(len(free)==1,'Expected one completion parameter')
  a=next(iter(free));completions=[]
  for t in [1,2,3]:
   mats=[m.subs(a,t) for m in N]
   require(all(v.is_Integer and v>=0 for m in mats for v in m),'Invalid nonnegative integral completion')
   casimir=sum((m*m for m in mats),s.zeros(6))
   polynomial=s.factor(casimir.charpoly().as_expr())
   match=[m.tolist() for m in mats]==target
   require(match==(t==2),'Unexpected full tensor equality result')
   completions.append(dict(parameter=t,all_216_target_entries_equal=match,formal_codegree_polynomial=str(polynomial)))
  rec['completions']=completions
  print('Complete tensor equality and codegrees:',completions)
 else:
  require(not free,'Unexpected parameter for swapped duality')
  fractions=sorted(set(v for m in N for v in m if not v.is_Integer))
  require(bool(fractions),'Expected nonintegral obstruction')
  rec['nonintegral_obstruction']=list(map(str,fractions))
 records.append(rec)
json.dump(records,open(P/'fusion_completion.json','w'),indent=2)
