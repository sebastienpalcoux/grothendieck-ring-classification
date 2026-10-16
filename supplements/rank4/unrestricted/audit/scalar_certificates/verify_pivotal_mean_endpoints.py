from fractions import Fraction as F

def check(flag,label):
    if not flag:raise AssertionError(label)
    print(label)

m=F(333,1000)
check(F(577,1000)**2<m,'sqrt(m)>577/1000')
for name,V,Elower,Eupper,l0,mub,errb,c0,pcap,p0,fac0,err_product in [
 ('first',F(1,1000),F(113),F(2277,20),F(307,1000),F(89,1000),F(29,1000),F(41,200),F(1,6),F(147,4000),F(327,250),F(1,200000)),
 ('second',F(1,250),F(105),F(211,2),F(281,1000),F(93,1000),F(60,1000),F(27,100),F(7,40),F(181,5000),F(53,50),F(35,10**6)),
]:
 check((m-l0)**2>2*V/3,name+': l lower bound')
 check((1000-Elower)/(1000*Elower)<mub*mub,name+': mean term')
 check(V/(4*l0)<errb*errb,name+': variance term')
 check((mub+errb)/F(577,1000)<c0,name+': c upper bound')
 check((1000-Eupper)*Eupper**3/10**9<fac0,name+': prefactor')
 check(V**3/54<err_product**2,name+': product radical')
 check(m**3-m*V/2-err_product>p0,name+': product lower bound')
 R=54*pcap-c0*(9-5*c0*c0)
 check(R>0 and R*R>2*(3-c0*c0)**3,name+': P upper bound')
 check(fac0*pcap**2/p0<1,name+': determinant <1')
V=F(7,500)
check(V**3/54<F(23,100000)**2,'third: product radical')
check(m**3-m*V/2-F(23,100000)>F(17,500),'third: product lower bound')
check((1000-80)*80**3/10**9<F(12,25),'third: prefactor')
check(F(12,25)/(27*F(17,500))<1,'third: determinant <1')
