"""Exact congruence discovery after eliminating continuous columns."""
from fractions import Fraction as Q
import math
from modular_moments import congruence_witness
from exact import require

def discover(A,b,integ):
 nv=len(A[0]);rr=[{j:Q(v) for j,v in enumerate(row+[rhs]) if v} for row,rhs in zip(A,b)];comb=[{i:Q(1)} for i in range(len(A))];active=set(range(len(A)));cont=[j for j,v in enumerate(integ) if not v]
 for j in cont:
  choices=[i for i in active if rr[i].get(j)];
  if not choices:continue
  p=min(choices,key=lambda i:len(rr[i]));a=rr[p][j];rr[p]={k:v/a for k,v in rr[p].items()};comb[p]={k:v/a for k,v in comb[p].items()};active.remove(p)
  for i in list(active):
   a=rr[i].get(j)
   if not a:continue
   for k,v in rr[p].items():
    rr[i][k]=rr[i].get(k,Q(0))-a*v
    if not rr[i][k]:del rr[i][k]
   for k,v in comb[p].items():
    comb[i][k]=comb[i].get(k,Q(0))-a*v
    if not comb[i][k]:del comb[i][k]
 ids=sorted(active);ii=[j for j,v in enumerate(integ) if v];AA=[];bb=[];cc=[]
 for i in ids:
  require(not any(rr[i].get(j) for j in cont),'continuous elimination failed');den=math.lcm(*(v.denominator for v in rr[i].values()))
  AA.append([int(rr[i].get(j,Q(0))*den) for j in ii]);bb.append(int(rr[i].get(nv,Q(0))*den));cc.append({k:v*den for k,v in comb[i].items()})
 w=congruence_witness(AA,bb,[1]*len(ii),primes=(2,3,5,7,11,13))
 if w is None:return None
 y={}
 for i,m in w['rows']:
  for k,v in cc[i].items():y[k]=y.get(k,Q(0))+m*v
 y={k:v for k,v in y.items() if v};return {'prime':w['prime'],'rows':[[i,str(v)] for i,v in sorted(y.items())]}

def verify(A,b,integ,c):
 p=c['prime'];rows=[(i,Q(v)) for i,v in c['rows']];require(__import__('sympy').isprime(p),'modulus not prime');vals=[sum(y*A[i][j] for i,y in rows) for j in range(len(A[0]))];rhs=sum(y*b[i] for i,y in rows)
 require(all((v.denominator==1 and v.numerator%p==0) if integ[j] else v==0 for j,v in enumerate(vals)),'invalid integer congruence combination');require(rhs.denominator==1 and rhs.numerator%p!=0,'congruence rhs vanishes');return True
