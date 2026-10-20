"""Independent exact conductor-five saturation/sign calculation."""
import json,sympy as s
from pathlib import Path
def require(value, message):
 if not value:raise RuntimeError(message)
def chi(x):return 0 if x%5==0 else 1 if x%5 in [1,4] else -1
reps=[(x,1) for x in range(5)]+[(1,0)]
def action(mat):
 A=s.zeros(6)
 for i,(p,q) in enumerate(reps):
  pp=(mat[0][0]*p+mat[0][1]*q)%5;qq=(mat[1][0]*p+mat[1][1]*q)%5
  if qq:j=(pp*pow(qq,-1,5))%5;scale=qq
  else:j=5;scale=pp
  A[i,j]=chi(scale)
 return A
S=action([[0,1],[-1,0]]);T=action([[1,-1],[0,1]]);I=s.eye(6)
require(S*S==I and T**5==I and (S*T)**3==I, 'The level-five group relations failed.')
require(S.T*S==T.T*T==I, 'The finite representation is not orthogonal.')
F=s.Matrix([1]*5+[0]);G=s.Matrix([0]*5+[1]);P=sum((T**i for i in range(5)),s.zeros(6))/5
require(P*S*F==G and P*S*G==F/5, 'The exact compressed action failed.')
out=[]
for delta in [-1,1]:
 w=F+delta*s.sqrt(5)*G;v=S*w;lam=delta/s.sqrt(5);a=(-1+delta*s.sqrt(5))/2
 require((P*v-lam*w).applyfunc(s.simplify)==s.zeros(6,1), 'The extremal eigenvalue failed.')
 require(((T-I)*(T*T-a*T+I)*v).applyfunc(s.simplify)==s.zeros(6,1), 'The primitive-residue polynomial failed.')
 require(s.simplify((P*v).dot(P*v)/w.dot(w))==s.Rational(1,5), 'The compressed norm ratio failed.')
 out.append({'delta':delta,'primitive_polynomial':['1',str(-a),'1'],'compressed_norm_ratio':'1/5'})
report={'status':'PASS','level':5,'S':S.tolist(),'T':T.tolist(),'F':list(F),'G':list(G),'cases':out}
Path(__file__).with_name('q5_saturation_finite_check.json').write_text(json.dumps(report,default=int,indent=2)+'\n')
print('PASS: exact six-dimensional level-five representation, compressed eigenvalues and primitive-residue polynomials.')
