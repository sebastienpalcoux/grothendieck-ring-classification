from fractions import Fraction as F
D=950;d=F(1,D)
phi=lambda x:x**3*(1-3*x)
assert phi(F(1,90))>d*d
v90=F(1,90)**2+(1-F(1,90))**2/3
assert (F(15,4)-4*v90)/5<F(49,100)
assert F(1,200)-d/2>d
assert phi(F(1,27))>d/27
S=F(3,40)
margin=F(21,5)-F(32,5)*S+F(88,15)*S*S-F(2,3)*d*(2*S+3)-F(15,4)
assert margin==F(3,3800)>0
psi=lambda x:x*(F(3,40)-x)**2*(F(17,20)+x)
psidd=lambda x:12*x*x+F(21,5)*x-F(39,160)
assert psidd(F(1,27))<0
assert psi(F(1,27))>psi(F(1,80))==F(69,1638400)>d/27
assert F(20480,1863)*d<F(1,85)
assert F(15,4)*F(85,84)**2<F(96,25)
assert (F(96,25)-F(5,3))/4==F(163,300)
assert -64+F(463,150)/F(571,2400)**2<0
assert 16+F(15,8)/(1-F(1,8)+F(1,128)-F(163,300))==F(70144,3259)<F(108,5)
L=F(163,15)
for r,A,W in [(F(27,2),F(21,125),F(81,2)),(F(81,4),F(43,375),F(1107,8)),(F(108,5),F(127,1500),F(3936,25))]:
 assert L>r/3
 gap=(L-r/3)**2-A*W
 assert gap>0
 print('Joint Cauchy squaring gap:',gap)
assert 1+F(85,84)*L==F(3023,252)<12
print('All exact rational certificates passed for the new D>=950 argument.')
