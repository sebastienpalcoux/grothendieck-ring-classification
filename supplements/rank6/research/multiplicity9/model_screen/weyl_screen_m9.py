"""Bounded numerical WZW model screen; a missing match is not an exclusion."""
from itertools import combinations, product
from fractions import Fraction
from pathlib import Path
import mpmath as m,json
m.mp.dps=65

def inv_vac(typ,n,k):
 if typ=='A':
  kap=k+n+1; hs=[j for j in range(1,n+1) for _ in range(n+1-j)]; index=n+1
 elif typ=='B':
  kap=k+2*n-1;rho=[m.mpf(n-i)-m.mpf('.5') for i in range(n)];hs=rho+[rho[i]+sg*rho[j] for i,j in combinations(range(n),2) for sg in [-1,1]];index=4
 elif typ=='C':
  kap=k+n+1;rho=[m.mpf(n-i) for i in range(n)];hs=rho+[(rho[i]+sg*rho[j])/2 for i,j in combinations(range(n),2) for sg in [-1,1]];index=2**n
 elif typ=='D':
  kap=k+2*n-2;rho=[m.mpf(n-1-i) for i in range(n)];hs=[rho[i]+sg*rho[j] for i,j in combinations(range(n),2) for sg in [-1,1]];index=4
 elif typ=='E':
  hs=[j for e in {6:[1,4,5,7,8,11],7:[1,5,7,9,11,13,17],8:[1,7,11,13,17,19,23,29]}[n] for j in range(1,e+1)];kap=k+{6:12,7:18,8:30}[n];index={6:3,7:2,8:1}[n]
 elif typ=='F':
  rho=[m.mpf(x)/2 for x in [11,5,3,1]];hs=rho+[rho[i]+sg*rho[j]for i,j in combinations(range(4),2)for sg in [-1,1]]
  hs += [sum(a*r for a,r in zip(v,rho))/2 for v in product([-1,1],repeat=4) if sum(a*r for a,r in zip(v,rho))>0];kap=k+9;index=4
 elif typ=='G':
  hs=[m.mpf(a)/3+b for a,b in [(1,0),(0,1),(1,1),(2,1),(3,1),(3,2)]];kap=k+4;index=3
 return m.sqrt(index)*m.mpf(kap)**(m.mpf(n)/2)/m.fprod(2*m.sin(m.pi*x/kap)for x in hs)
a=2*m.cos(m.pi/7); b=a*a-1; h=2+2*a+b; x=(h+m.sqrt(h*h+4))/2
D=(1+a*a+b*b)*(1+x*x)
p=[1,-637,22295,-298116,1854944,-5274997,5274997]
assert abs(m.polyval(p,D))<m.mpf('1e-43')
Ds={'R6_9_3748':D}
res=[]
for typ,ns in [('A',range(1,13)),('B',range(2,13)),('C',range(2,13)),('D',range(4,13)),('E',[6,7,8]),('F',[4]),('G',[2])]:
 for n in ns:
  for k in range(1,49):
   inv=inv_vac(typ,n,k)
   for target,D in Ds.items():
    for power,ratio in [('square_global_ratio',inv**2/D**2),('global_ratio',inv**2/D)]:
     if ratio<m.mpf(1)/100 or ratio>100:continue
     r=Fraction(float(ratio)).limit_denominator(100)
     if abs(ratio-m.mpf(r.numerator)/r.denominator)<m.mpf('1e-50'):
      res.append(dict(type=typ,rank=n,level=k,target=target,screen=power,rational_ratio=str(r),global_dimension=m.nstr(inv**2,60)))
report=dict(target_fp_global_dimension=m.nstr(D,60),global_dimension_polynomial=p,coefficient_maximum=9,precision_decimal_digits=65,tolerance='1e-50',status='discovery_only_no_categorification',domain='A1..A12, B2..B12,C2..C12,D4..D12,E6,E7,E8,F4,G2; levels1..48; rational ratios numerator/denominator max denominator100, value[1/100,100]',matches=res)
Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
