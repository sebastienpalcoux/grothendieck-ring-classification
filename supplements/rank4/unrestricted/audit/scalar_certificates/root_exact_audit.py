"""Independent exact checks of the new analytic certificates; no ring census."""
import sympy as s
R=s.Rational
t=s.symbols('t',real=True)
d=R(1,950); q=R(1,168); a=R(7,250)
c=R(4,5)-d*d-(1-d)**2/3
assert a*a+(1-q-a)**2/2-(c-q*q)==R(2706003,35378000000)
assert q*a*(1-q-a)**2/4-d*(1-d)**3/27==R(30295201169,1379317464000000000)
assert c>R(1,3)
assert c-q*q<(1-q)**2/2
assert R(33,40)-2*d/3-4*q/3>R(4,5)
for B,r,tmin,tcenter,H,L,C,Hlower,Lupper,Clower in [
 (R(201,250),R(51,4),R(3,100),R(1,32),
  1029375*t*t-R(28886625,16)*t+R(815705469,1024),
  -R(1263121,8192),R(1325631,1048576),300000,155,1),
 (R(8063,10000),R(68,5),R(1,36),R(29,1000),
  2909400*t*t-R(25760274,5)*t+R(11467835081,5000),
  -R(327793717,1250000),R(2526625707,5000000000),800000,263,R(1,2))]:
    N=-3*r*t*t+(3*r-3)*t-1
    F=N*N+(1-3*t)**4-(6*B-4)*(1-3*t)**2
    f=s.Poly(F,t).clear_denoms()[1].primitive()[1].as_expr()
    assert s.expand(f-H*(t-tcenter)**2-L*(t-tcenter)-C)==0
    assert s.diff(H,t).subs(t,R(1,3))<0
    assert H.subs(t,R(1,3))>Hlower
    assert abs(L)<Lupper and C>Clower
    assert Lupper**2<4*Hlower*Clower
    assert 6*B-4<(1-3*tmin)**2
    assert N.subs(t,tmin)>0
    assert s.diff(N,t).subs(t,R(1,3))>0
assert 14-(1+R(300,299)*R(51,4))==R(62,299)
assert 14-(R(300,950)+R(168,167)*R(68,5))==R(44,15865)
print('All outside-field rational product, ratio and scalar certificates passed.')
