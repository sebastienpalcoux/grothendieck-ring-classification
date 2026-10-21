exec(open(__file__.replace('rotation_integer_probe.py','twist_sums_probe.py')).read().split('for case in cases:')[0])
s=c.s
v0,v3,v4,v5=[allcols[t+5]for t in(0,3,4,5)];ds=[md.value(chs[0],v,K)for v in cols];d0,d3,d4,d5=[md.value(chs[0],v,K)for v in(v0,v3,v4,v5)];gauss=K.from_sympy(s.Rational(8,5))-K.unit/s.Integer(10)

import math

def nus(power,z4):
 sc=4*K(z4)**(power//4)if power%4==0 else K.zero
 sd=K(8)if power%17==0 else(gauss if pow(power%17,8,17)==1 else -K.one-gauss)
 return [(sum((d*K(v[j])for d,v in zip(ds,cols)),K.zero)+K(4*(-1)**power)*d0*K(v0[j])+d3*K(v3[j])+d4*K(v4[j])*sc+d5*K(v5[j])*sd)/a['D']for j in range(8)]
for z4 in [1,-1]:
 bad=[];checked=0
 for obj in range(1,8):
  powers=[[1]+[0]*7]
  for n in range(1,137):powers.append([sum(powers[-1][i]*R[i][obj][j]for i in range(8))for j in range(8)])
  for n in range(2,137):
   if n%17==0:continue
   divs=list(map(int,s.divisors(n))); traces={}
   for d in divs:
    nu=nus(d,z4);t=sum((K(co)*v for co,v in zip(powers[n//d],nu)),K.zero);raw=t.to_list();need=(len(raw)<2 and(not raw or raw[0].denominator==1))
    assert need,(n,d,obj,t)
    traces[d]=int(raw[0])if raw else 0
   for k in divs:
    mult=sum(traces[d]*int(s.mobius(d//math.gcd(d,k))*s.totient(d)/s.totient(d//math.gcd(d,k)))for d in divs)
    checked+=1
    if mult<0 or mult%n:bad.append((obj,n,k,mult,n))
 print('z4',z4,'checked',checked,'bad',bad[:20],'numberbad',len(bad))
