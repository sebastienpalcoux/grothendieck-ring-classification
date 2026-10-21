exec(open(__file__.replace('power_indicator_probe.py','twist_sums_probe.py')).read().split('for case in cases:')[0])
s=c.s
v0,v3,v4,v5=[allcols[t+5]for t in(0,3,4,5)];ds=[md.value(chs[0],v,K)for v in cols];d0,d3,d4,d5=[md.value(chs[0],v,K)for v in(v0,v3,v4,v5)];gauss=K.from_sympy(s.Rational(8,5))-K.unit/s.Integer(10)
for power in range(1,18):
 for z4 in([1,-1]if power%4==0 else[None]):
  sc=4*K(z4)**(power//4)if power%4==0 else K.zero
  sd=K(8)if power%17==0 else(gauss if pow(power%17,8,17)==1 else -K.one-gauss)
  nus=[(sum((d*K(v[j])for d,v in zip(ds,cols)),K.zero)+K(4*(-1)**power)*d0*K(v0[j])+d3*K(v3[j])+d4*K(v4[j])*sc+d5*K(v5[j])*sd)/a['D']for j in range(8)]
  print(power,z4,[c.ec(x)for x in nus])
