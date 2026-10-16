"""Independent exact scalar audit of rank-four section 8 closing bounds.
This checks no categorical hypothesis and proves no formalization claim.
"""
def _require(condition, message):
    if not condition:
        raise RuntimeError(message)

import sympy as s,json
R=s.Rational
x,p,c,E=s.symbols('x p c E',real=True)
F=lambda z:z*z+(1-z)**2
C=lambda z:(1-2*z)/(3+4*z*z)
g=lambda z:(1-z)**2/(2*(1+z*z))
checks=[]
def pos(expr,label):
    expr=s.simplify(expr)
    sign=s.sign(expr)
    if sign!=1:raise ValueError((label,expr,sign))
    checks.append(label)
def eq(expr,label):
    _require(s.simplify(expr)==0, (label,s.simplify(expr)))
    checks.append(label)
def interval_nonnegative(poly,lo,hi,label):
    poly=s.Poly(poly,x)
    vals=[poly.eval(lo),poly.eval(hi)]
    for root in s.polys.polytools.intervals(poly.diff(),eps=R(1,10**10)):
        a,b=root[0]
        if lo<a<hi or lo<b<hi:
            # For the few degree<=2 derivative instances, exact roots are simple.
            for rr in s.solve(poly.diff().as_expr(),x):
                if rr.is_real and bool(rr>lo) and bool(rr<hi): vals.append(poly.eval(rr))
            break
    _require(all(s.sign(s.simplify(v)) in [0,1] for v in vals), (label,vals))
    checks.append(label)
eq(F(p)+F(c*p)-1-2*(1+c*c)*(p-(1+c)/(2*(1+c*c)))**2-(1-c)**2/(2*(1+c*c)),'first completed square')
eq(p*p+(1-p)**2/2+F(c*p)-1-(3+4*c*c)*(p-(1+2*c)/(3+4*c*c))**2/2-(1-2*c)/(3+4*c*c),'mixed completed square')
# Codegree-two and short-orbit numerical exclusions.
for expr,label in [(R(163,200)-R(1,600)-R(61,75),'Pell U2'),(R(1,4)+R(1,9)+R(1,36)-R(2,3600)-R(233,600),'Pell V2'),(R(61,75)+R(233,600)-1-R(121,600),'Pell combined')]:eq(expr,label)
for expr,label in [(R(121,600)-R(31,300),'Pell contradiction'),((3+s.sqrt(5))/2-R(44,17),'h >=11 unit contradiction'),(R(13,4)-(35-s.sqrt(833))/2,'h7 smaller root'),((3+s.sqrt(5))/2-(9-3*s.sqrt(5)),'(3,h) smaller root'),(R(79,360)-R(4,1125)-R(1,5),'norm45 lower'),(R(1,5)-R(1,300)-s.sqrt(R(3,300)),'norm45 upper'),(R(29,96)-R(6,576)-R(7,24),'norm64 lower exact zero')]:
    if s.simplify(expr)==0:eq(expr,label)
    else:pos(expr,label)
pos(R(37,200)-R(1,100)-s.sqrt(R(3,100)),'norm64 upper')
pos(R(43,96)-R(4,864)-R(2,5),'norm96 lower')
pos(R(2,5)-R(1,200)-s.sqrt(R(3,200)),'norm96 upper')
# h>=2.
pos(R(11,27)+F(R(7,150))-1-R(23,1000)-R(29,100),'h>=2 E<60 lower')
pos(R(29,100)-R(1,44)-s.sqrt(R(3,44)),'h>=2 E<60 upper')
for lower,split,endpoint,label in [(R(90,301)-R(23,1000),R(11,40),60,'60--100'),(R(5,19)-R(23,1000),R(21,100),100,'100--200'),(R(15,79)-R(23,1000),R(7,50),200,'200--400'),(R(5,42)-R(23,1000),R(19,200),400,'>=400')]:
    pos(lower-split,'h>=2 lower '+label);pos(split-R(3,endpoint)-s.sqrt(R(3,endpoint)),'h>=2 upper '+label)
# Large product.
pos(R(361,802)-R(44,1000)-R(2,5),'large product small t coefficient')
pos((4*E*E-135*E+300).subs(E,R(63,2)),'large product small t endpoint')
B=1000*x*(g(x)-R(1,25))-4*x+2*x*x-3
eq(s.diff(B,x,2)-(2000*(3*x*x-1)/(1+x*x)**3+4),'large product curvature')
pos(B.subs(x,R(1,20))-R(33,2),'large product first chord endpoint')
pos(B.subs(x,R(2,5))-41,'large product last chord endpoint')
eq((13+70*x)**2-3*(1000*x-1)-(70*x-R(59,7))**2-R(4947,49),'large product chord square')
# Exceptional rational complement: A and endpoint bounds.
t=(3-s.sqrt(5))/2
pairs=[(3,15),(3,27),(4,20),(6,6),(7,7)]
for aa,bb in pairs:
    pp=1-R(1,aa)-R(1,bb)
    A=pp*pp+R(1,aa*aa)+R(1,bb*bb)+F(t*pp)-1-R(1,50)
    pos(A-R(1,10),'exceptional rational A '+str((aa,bb)))
eq((102*t-5)**2-(3000*t-3)-(30412-13596*s.sqrt(5)),'exceptional rational squared difference')
pos(30412-13596*R(161,72),'exceptional rational endpoint')
# Ordinary short quadratic orbits: polynomial lower envelopes.
f=R(167,400)-x+x*x/2
for pp,U in [(R(1,4),R(19,32)),(R(1,3),R(1,2)),(R(2,5),R(11,25)),(R(1,2),R(7,16)),(R(2,3),R(23,45)),(R(3,4),R(19,32))]:
    interval_nonnegative(U+F(x*pp)-1-R(1,50)-f,0,R(2,5),'short quadratic envelope '+str(pp))
pos(f.subs(x,R(1,25))-R(3,8),'short quadratic small t coefficient')
pos((R(3,8)*36-R(16,5))**2-3*(36-1),'short quadratic small t endpoint')
B=R(827,2)*x-998*x*x+500*x**3
# Original B includes -3.
B-=3
for xx,yy in [(R(1,25),R(119,10)),(R(3,25),R(331,10))]:pos(B.subs(x,xx)-yy,'short quadratic chord endpoint '+str(xx))
eq(B.subs(x,R(2,5))-R(868,25),'short quadratic final endpoint')
for aff,lo,hi in [(R(13,10)+265*x,R(1,25),R(3,25)),(R(162,5)+R(29,5)*x,R(3,25),R(2,5))]:interval_nonnegative(aff*aff-3000*x+3,lo,hi,'short quadratic chord square '+str(lo))
f5=R(21,50)-R(6,5)*x+R(18,25)*x*x
pos(f5.subs(x,R(1,25))-R(37,100),'constant5 small t coefficient')
pos((R(37,100)*40-R(16,5))**2-3*(40-1),'constant5 small t endpoint')
B5=416*x-1198*x*x+720*x**3-3
for xx in [R(1,25),R(3,25)]:pos(B5.subs(x,xx)-(R(11,5)+238*xx),'constant5 chord '+str(xx))
interval_nonnegative((R(11,5)+238*x)**2-3000*x+3,R(1,25),R(3,25),'constant5 chord square')
for xx in [R(3,25),R(3,10)]:pos(B5.subs(x,xx)-30,'constant5 high chord '+str(xx))
eq(f5.subs(x,t)-(R(24,25)*t-R(3,10)),'constant5 exceptional expression')
pos(f5.subs(x,t)-R(1,15),'constant5 exceptional lower')
eq((202*t-5)**2-(9000*t-3)-(111392*t-40776),'constant5 exceptional square')
pos(111392*R(3,8)-40776-996,'constant5 coarse strict endpoint zero') if 111392*R(3,8)-40776-996 else eq(111392*R(3,8)-40776-996,'constant5 coarse endpoint')
# Moderate t.
A=-x**R(3,2)*s.diff(C(x),x)
eq(s.diff(A,x)-s.sqrt(x)*(16*x**4-48*x**3-144*x*x+60*x+27)/(4*x*x+3)**3,'moderate derivative')
pos(27-144*R(2,5)**2-48*R(2,5)**3,'moderate derivative numerator positive')
pos(C(R(8,125))-R(3,125)-R(53,200),'moderate first endpoint lower')
pos(R(53,200)-R(3,64)-s.sqrt(R(3,64)),'moderate first endpoint upper')
pos(C(R(67,250))-R(1411,10000),'moderate second endpoint lower')
pos(R(1171,10000)-R(30,2679)-s.sqrt(R(30,2679)),'moderate second endpoint upper')
pos(R(59,128)+F(R(21,250))-1-R(3,125)-R(7,25),'irrational moderate lower')
pos(R(27,100)-R(1,50)-s.sqrt(R(3,50)),'irrational moderate upper')
# Rational selected E.
lo=lambda A,E:A-R(4,E)+R(4,E*E)-R(1,50)
hi=lambda E:(1+s.sqrt(3*(E-1)))/E
for aa,ee,bb in [(R(19,32),30,R(2,5)),(R(59,128),36,R(33,100)),(R(41,96),40,R(3,10)),(R(505,1152),38,R(31,100)),(R(179,441),42,R(29,100))]:pos(lo(aa,ee)-bb,'rational E lower '+str(ee))
for ee,bb in [(30,R(7,20)),(36,R(8,25)),(40,R(3,10)),(38,R(31,100)),(42,R(29,100))]:pos(bb-hi(ee),'rational E upper '+str(ee))
print(json.dumps({'status':'PASS','exact_scalar_checks':len(checks),'checks':checks},indent=2))
