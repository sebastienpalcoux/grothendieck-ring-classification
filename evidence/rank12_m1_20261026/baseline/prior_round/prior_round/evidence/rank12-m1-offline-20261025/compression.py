from fractions import Fraction
import math, sympy as s
from common import dual,require
def rank(values):
 primes=sorted({p for q in values for p in s.factorint(q)});piv={}
 for q in values:
  v=sum(1<<i for i,p in enumerate(primes) if s.factorint(q).get(p,0)%2)
  while v:
   i=v.bit_length()-1
   if i in piv:v^=piv[i]
   else:piv[i]=v;break
 return len(piv)

def gates(R):
 n=len(R);du=dual(R);G=[i for i in range(n) if sum(R[i][du[i]])==1];X=set(range(n))-set(G)
 # A transitive invertible action forces precisely two FP dimensions.
 if X:
  x=min(X);orb={next(k for k in range(n) if R[g][x][k]) for g in G}
  if orb==X:return 'two_FP_values_transitive',{'invertibles':G,'noninvertibles':sorted(X),'object':x}
 # The maximal Casimir eigenvalue is the positive global FP dimension.
 B=sum((s.Matrix(A)*s.Matrix(A).T for A in R),s.zeros(n));candidates=[]
 for f,m in B.charpoly().as_poly().factor_list()[1]:
  iv=f.intervals(eps=s.Rational(1,10**10))
  if iv:candidates.append((f,iv[-1][0]))
 f,(lo,hi)=max(candidates,key=lambda a:a[1][0])
 require(all(a==f or bounds[1]<lo for a,bounds in candidates),'Perron factor separation')
 if f.degree()==1:return 'weak_integrality',{'global_dimension':int(-f.TC())}
 return None,None

def discover(R):
 n=len(R);B=sum((s.Matrix(A)*s.Matrix(A).T for A in R),s.zeros(n));fields={};frows=[]
 for f,m in B.charpoly().as_poly().factor_list()[1]:
  co=list(map(int,f.all_coeffs()));frows.append({'coefficients':co,'multiplicity':m})
  if f.degree()!=2:continue
  a,b,c=co;disc=b*b-4*c;require(a==1 and disc>0,'quadratic Casimir factor')
  q=math.prod(int(p) for p,e in s.factorint(disc).items() if e%2);cond=q if q%4==1 else 4*q
  fields.setdefault(q,{'conductor':cond,'ratio':Fraction(0),'factors':[]})
  fields[q]['ratio']+=Fraction(cond*m*disc,c*c);fields[q]['factors'].append({'coefficients':co,'multiplicity':m})
 r=rank(fields)
 report={'factors':frows,'squareclass_rank':r,'quadratic_fields':[{'radicand':q,'conductor':z['conductor'],'ratio':str(z['ratio']),'factors':z['factors']} for q,z in sorted(fields.items())]}
 if not r:return report,None
 for q,z in sorted(fields.items()):
  if 2**(r-1)*z['ratio']>4:return report,dict(report,kind='quadratic_casimir_compression',gate='sphericalization',radicand=q,extension_degree_lower_bound=2**(r-1),upper_bound=4)
 gate,witness=gates(R);report['strong_gate']=gate;report['gate_certificate']=witness
 if gate:
  for q,z in sorted(fields.items()):
   if 2**(r-1)*z['ratio']>1:return report,dict(report,kind='quadratic_casimir_compression',gate=gate,radicand=q,extension_degree_lower_bound=2**(r-1),upper_bound=1)
 return report,None
