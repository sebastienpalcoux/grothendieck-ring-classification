"""Independent exact identities supporting the quartic bound.
Uses explicit rational functional calculus and Sturm counts for scalar rows,
and symbolic minimization for the fixed-field bootstrap.
"""
import json
from pathlib import Path
import sympy as s
from paths import repository_root
ROOT=repository_root()
R=s.Rational;x=s.Symbol('x'); rows=json.loads((ROOT/'supplements/rank4/unrestricted/audit/quartic_trace13_exact_resolvent_chart.json').read_text())
def require(value,message):
 if not value: raise RuntimeError(message)
scalar=[]
for row in rows:
 _,mt,c,mr,h=row['polynomial']; t=-mt;r=-mr
 C=s.Matrix([[0,0,0,-h],[1,0,0,r],[0,1,0,-c],[0,0,1,t]])
 I=s.eye(4); trace=s.trace((C+2*I)**2*(C*C+I).inv())
 A0=1-c+h;B0=t-r;C0=3*t-r;F0=2*c-4
 formula=4-R((4*C0+3*F0)*A0+(4*F0-3*C0)*B0,A0*A0+B0*B0)
 require(trace==formula,'rational-functional-calculus trace')
 f=s.Poly(row['polynomial'],x)
 if trace>R(583,40):
  a=R(1,10) if t in (7,11) else R(1,4)
  require(f.count_roots(0,a)==0 and f.count_roots(a,R(3,10))>=1,'least-root certified bracket')
  ga=(a+2)**2/(a*a+1)
  require(trace-ga<R(423,40),'exception scalar margin')
 else:
  require(f.count_roots(0,1)>=1,'least root below 1')
 scalar.append({'polynomial':row['polynomial'],'trace_g':str(trace)})
# Derive rather than assume the fixed-field square-sum bootstrap.
d,S,q,x=s.symbols('d S q x',real=True); A=1-d;B=1-S
expr=5*(d*d+x*x+(A-x)**2/2)+4*(q*q+(S-q)**2+B*B-(A-x)*B/2)
xmin=s.solve(s.diff(expr,x),x)[0]
minimum=s.expand(expr.subs(x,xmin))
claimed=R(21,5)-R(32,5)*S+R(118,15)*S*S+R(2,3)*d*(-2*S+10*d-3)-8*q*(S-q)
require(s.expand(minimum-claimed)==0,'fixed-field exact minimized quadratic')
require(s.diff(expr,x,2)==15,'positive Hessian')
a=s.Symbol('a',positive=True);m=a/(1+a)
u=d*d+(m-d)**2+(1-m)**2/2
v=(d/a)**2+((m-d)/a)**2+(1-m/a)**2/2
base=(7*a*a+R(13,2))/(1+a)**2-(10*a+8/a)*d/(1+a)
require(s.factor(5*u+4*v-base)==2*d*d*(5*a*a+4)/a**2,'golden-ratio pair-square minimum')
# Quadratic character restrictions in Q(sqrt2,sqrt5): all possible traces/norms.
quadratic=[]
for norm in (1,2):
 for trace in range(1,6):
  disc=trace*trace-4*norm
  if disc<=0 or s.integer_nthroot(disc,2)[1]:continue
  if trace*trace%norm:continue
  squarefree=s.prod(p for p,e in s.factorint(disc).items() if e%2)
  if squarefree in (2,5,10):quadratic.append((trace,norm))
require(quadratic==[(3,1),(4,2)],'fixed-field quadratic list')
out={'status':'PASS','scalar_rows':scalar,'bootstrap':'exact quadratic minimization PASS','quadratic_cases':quadratic}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':'PASS','scalar_rows':len(scalar),'bootstrap':'PASS','quadratic_cases':quadratic}))
