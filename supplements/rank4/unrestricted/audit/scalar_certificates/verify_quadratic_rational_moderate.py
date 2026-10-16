from fractions import Fraction as F
C=lambda t:(1-2*t)/(3+4*t*t)
V=lambda t:t*t+(1-t)**2
# Compare a+b sqrt(c)<r with positive rational residue.
def sqrt_lt(c,r): assert r>0 and c<r*r
assert 27-48*F(2,5)**3-144*F(2,5)**2==F(111,125)>0
assert C(F(8,125))-F(3,125)>F(53,200)
sqrt_lt(F(3,64),F(53,200)-F(3,64))
assert C(F(67,250))>F(1411,10000)
sqrt_lt(F(30,2679),F(1171,10000)-F(30,2679))
# Bounds on 2-sqrt3.
assert (2-F(2679,10000))**2>3
assert (2-F(67,250))**2<3
assert F(325,512)>F(5,8)
assert F(59,128)+V(F(21,250))-1-F(3,125)>F(7,25)
sqrt_lt(F(3,50),F(27,100)-F(1,50))
B=lambda A,E:A-F(4,E)+F(4,E*E)-F(1,50)
for A,E,lower,upper in [(F(19,32),30,F(2,5),F(7,20)),(F(59,128),36,F(33,100),F(8,25)),(F(41,96),40,F(3,10),F(3,10)),(F(505,1152),38,F(31,100),F(31,100)),(F(179,441),42,F(29,100),F(29,100))]:
 assert B(A,E)>lower
 sqrt_lt(F(3*(E-1)),E*upper-1)
 print('E endpoint',E,'lower margin',B(A,E)-lower)
assert B(F(41,96),40)==F(743,2400)
assert B(F(179,441),42)==F(46,147)-F(1,50)
assert F(1000,36*36)>F(3,4)
assert F(1000,42*42)>F(9,16)
print('All exact scalar certificates passed.')
