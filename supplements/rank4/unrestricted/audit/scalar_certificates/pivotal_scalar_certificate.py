from fractions import Fraction as F
# exact lower comparison in variable t=sqrt(D), t>=158/5
b=F(301,100);t=F(158,5);rtlo=F(28,5);rthi=F(45,8)
rows=[(F(18,5),F(0),F(0),F(2683,1000),F(671,250),F(6831,1000)),(F(10,3),F(1,1000),F(4,25),F(2581,1000),F(1291,500),F(3043,500)),(F(5,2),F(1,250),F(8,25),F(559,250),F(2237,1000),F(3953,1000))]
for e,v,k,rlo,rhi,e3hi in rows:
 assert rlo*rlo<2*e<rhi*rhi
 assert e3hi*e3hi>e**3
 A=2*e-4
 B=(F(471,100)+k)*rhi
 C0=11-F(91,3)-b+2*e-F(3,2)*e*e+32*v
 C1=8*rlo-(F(71213,100000)+F(1003,1000)*k)*e3hi
 C2=64+(2*b-3)*e-(e if not v else 0)
 C3=F(40,3)+F(1,2)+F(3,2)*b*e*e
 C4=-64+b*e
 C5=F(128,3)-b/2
 assert C1>0 and C2>0 and C3>0 and C4<0 and C5>0
 # L(t)=18v t²+(A−48v)t−B sqrt(t)+C0+C1/sqrt(t)+C2/t−C3/t²+C4/t³+C5/t⁴
 val=18*v*t*t+(A-48*v)*t-B*rthi+C0+C1/rthi+C2/t-C3/t**2+C4/t**3+C5/t**4
 der=36*v*t+A-48*v-B/(2*rtlo)-C1/(2*t*rtlo)-C2/t**2-4*C5/t**5
 print('row',e,'value',float(val),val,'derivative',float(der),der)
 assert val>0 and der>0
