"""Exact algebraic certificates for outside_ratio_950.tex; no numerical roots."""
import sympy as s
R=s.Rational
t=s.symbols('t')
cases=[
 (R(201,250),R(51,4),R(2000,3),R(1,32),
 1029375*t**4-1869750*t**3+910431*t**2-51704*t+784,
 1029375*t**2-R(28886625,16)*t+R(815705469,1024),
 -R(1263121,8192),R(1325631,1048576),300000,155,R(1),R(3,100)),
 (R(8063,10000),R(68,5),R(5000,3),R(29,1000),
 2909400*t**4-5320800*t**3+2594833*t**2-137622*t+1937,
 2909400*t**2-R(25760274,5)*t+R(11467835081,5000),
 -R(327793717,1250000),R(2526625707,5000000000),800000,263,R(1,2),R(1,36))]
for B,ratio,scale,r,f,H,L,C,m,ell,c,lo in cases:
 N=-3*ratio*t*t+(3*ratio-3)*t-1
 F=N*N+(1-3*t)**4-(6*B-4)*(1-3*t)**2
 assert s.expand(f-scale*F)==0
 assert s.expand(f-H*(t-r)**2-L*(t-r)-C)==0
 assert s.diff(H,t,2)>0 and s.diff(H,t).subs(t,R(1,3))<0
 assert H.subs(t,R(1,3))>m and abs(L)<ell and C>c
 assert ell**2<4*m*c
 assert 6*B-4<(1-3*lo)**2
 assert N.subs(t,lo)>0 and s.diff(N,t).subs(t,R(1,3))>0
 print('Verified ratio',B,ratio)
d,q=s.symbols('d q')
C=R(4,5)-d*d-(1-d)**2/3
B=R(1,3)+(C-q*q)/(1-q)**2
assert s.simplify(s.diff(B,d)-(2-8*d)/(3*(1-q)**2))==0
assert s.simplify(s.diff(B,q)-2*(C-q)/(1-q)**3)==0
assert B.subs({d:R(1,950),q:R(1,300)})<R(201,250)
assert B.subs({d:R(1,950),q:R(1,168)})<R(8063,10000)
assert 14-(1+R(300,299)*R(51,4))==R(62,299)
assert 14-(R(300,950)+R(168,167)*R(68,5))==R(44,15865)
print('Verified normalization and trace margins')
