#!/usr/bin/env python3
"""All twenty simples, indicator orders4 through12, exact finite checks."""
from pathlib import Path
from fractions import Fraction as Q
import sys,json,math,time
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE));from cyclotomic288 import RT,ONE,add,scale,mul,sqrt2,sqrt3,sqrt6,need
sys.path.insert(0,str(HERE/'prior'));import quartic as quart
start=time.monotonic();n=20
N=json.load(open(HERE/'rank20_fusion_tensor.json'))['tensor']
md=json.load(open(HERE/'rank20_modular_data.json'));ph=md['twist_exponents_mod288']
p=next(p for p in json.load(open(HERE/'prior/spectral_reduction.json'))['patterns'] if p['pattern']==186)
def encq(d):return add(*(scale(a,b) for a,b in zip(d,(ONE,sqrt2,sqrt3,sqrt6))))
dims=[encq(tuple(map(Q,d))) for d in p['dimensions']]
invG=encq(quart.scale(2,quart.inv(quart.mul(quart.D,quart.D))))
DD=[[mul(d,e) for e in dims] for d in dims]
results={}
for m in range(4,13):
 weights=[[mul(mul(DD[i][j],RT[(m*(ph[i]-ph[j]))%288]),invG) for j in range(n)] for i in range(n)]
 out=[]
 for k in range(n):
  val=add(*(scale(N[k][i][j],weights[i][j]) for i in range(n) for j in range(n) if N[k][i][j]))
  if m in (8,12):
   radical=sqrt2 if m==8 else sqrt3
   rd=dict(radical);vd=dict(val);r=next(i for i in rd if i)
   b=Q(vd.get(r,0))/rd[r];a=Q(vd.get(0,0))-b*rd.get(0,0)
   need(val==add(scale(a,ONE),scale(b,radical)) and a.denominator==b.denominator==1,'quadratic cyclotomic integer indicator')
   out.append([int(a),int(b)])
  else:
   need(not val or len(val)==1 and val[0][0]==0 and Q(val[0][1]).denominator==1,'rational integral indicator')
   a=int(val[0][1]) if val else 0;out.append(a)
   if m in (5,7,11):
    row=[1]+[0]*(n-1)
    for _ in range(m):row=[sum(row[i]*N[k][i][j] for i in range(n)) for j in range(n)]
    mass=row[0];q,r=divmod(mass-a,m)
    need(r==0 and q>=0 and q+a>=0,'prime rotation eigenspace multiplicities')
 results[str(m)]=out
payload={'status':'PASS','scope':'All-simple necessary indicators; not categorical existence',
 'orders':list(range(4,13)),'count':180,'values':results,
 'coordinate_conventions':{'8':'a+b sqrt2','12':'a+b sqrt3','other':'integer'},
 'prime_rotation_eigenspace_checks':[5,7,11],'seconds':time.monotonic()-start}
(HERE/'higher_indicators_verification.json').write_text(json.dumps(payload,indent=2)+'\n')
print('PASS: all180 indicators of orders4..12 and prime rotation multiplicities.',time.monotonic()-start)
