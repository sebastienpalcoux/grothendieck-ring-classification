from fractions import Fraction as F
from itertools import combinations_with_replacement as comb
from math import gcd,isqrt
import sympy as s
q=149; scale=9;T=6741
for y in range(1,6):
 for x in range(-isqrt(q*y*y-1),isqrt(q*y*y-1)+1):
  if (x-y)%2:continue
  n=q*y*y-x*x
  if (4*q*y*y)%n: continue
  # delta=scale*(q*y+x*sqrtq)/2 in basis1, (1+sqrtq)/2
  content=gcd(scale*(q*y-x)//2,scale*x)
  ds=[int(d) for d in s.divisors(abs(content)) if d>1]
  inv=F(4*y,scale*n)
  if inv>=1:continue
  for fs in comb(ds,4):
   if sum(fs)+scale*q*y>T:continue
   if sum((F(1,f) for f in fs),F(0))!=1-inv:continue
   print(y,x,'delta', [scale*q*y,scale*x],'norm',scale*scale*q*n//4,'fs',fs,'T',sum(fs)+scale*q*y)
