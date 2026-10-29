"""Exact Q(zeta_1728) helper and complete square-Galois orbits."""
import math,json
from collections import Counter
from itertools import combinations_with_replacement
import sympy as s
N=1728;deg=576
# Phi1728=x576-x288+1. sparse roots represented dict reduced to degree<576

def root(k):
 k%=N
 if k<576:return ((k,1),)
 # reduce x^k by x^576=x^288-1, only three steps
 d={k:1}
 for i in range(k,575,-1):
  a=d.pop(i,0)
  if a:
   d[i-288]=d.get(i-288,0)+a;d[i-576]=d.get(i-576,0)-a
 return tuple(sorted((i,a) for i,a in d.items() if a))
def add(*vs):
 d=Counter()
 for v in vs:
  for i,a in v:d[i]+=a
 return tuple(sorted((i,a) for i,a in d.items() if a))
def scale(k,v):return tuple((i,a*k) for i,a in v if a*k)
def mul(a,b):return add(*(scale(x*y,root(i+j)) for i,x in a for j,y in b))
units=[a for a in range(N) if math.gcd(a,N)==1];sq=sorted(set(a*a%N for a in units));orbits=[];left=set(range(N))
while left:
 k=min(left);orb=sorted(set(k*a%N for a in sq));left.difference_update(orb);orbits.append(orb)
rt=[root(i) for i in range(N)];small=[o for o in orbits if len(o)<=9]

# coarse sparse target equation, recursion over orbits with total multiplicity 5 or9
sqrt3=add(rt[N//12],rt[-N//12]);sqrt6=mul(sqrt3,add(rt[N//8],rt[-N//8]));xi=rt[N//8]
base=[(t,add(scale(-1,rt[0]),scale(-2,rt[t*N//144]),scale(-2,mul(sqrt3,xi)))) for t in (60,84,96)]
