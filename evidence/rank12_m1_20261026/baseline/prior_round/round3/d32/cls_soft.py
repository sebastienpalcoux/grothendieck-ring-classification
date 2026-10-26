"""Exact CLS Table3/4 soft involution audit. Object labels: 0,1,2,3,N=4,D=5."""
from pathlib import Path
import itertools,json,sys,collections
import sympy as s
HERE=Path(__file__).resolve().parent
I=s.eye(2);X=s.Matrix([[0,1],[1,0]]);Y=s.Matrix([[0,-s.I],[s.I,0]]);Z=s.diag(1,-1);i=s.I;rt=s.sqrt(2)
N=[[[0]*6 for _ in range(6)]for _ in range(6)]
for a,b in itertools.product(range(4),repeat=2):N[a][b][a^b]=1
for a in range(4):N[a][4][4]=N[4][a][4]=N[a][5][5]=N[5][a][5]=1;N[4][4][a]=N[5][5][a]=1
N[4][5][5]=N[5][4][5]=N[5][5][4]=2
sg=[1,-1,-1,1]
L=s.Matrix([[1,1,1,1],[1,1,1,1],[1,-1,1,-1],[1,-1,1,-1]])
K=s.Matrix([[1,1,1,1],[1,-1,-1,1],[1,-1,-1,1],[1,1,1,1]])
P=[I,X,Z,-i*Y];Q=[I,-Z,-X,-i*Y]
W=[(X-Z)/2,(I-i*Y)/2,-(I+i*Y)/2,-(X+Z)/2]
chi=lambda a,b: (-1)**((a&1)*(b&1)+(a>>1)*(b>>1))
def left(a,b,c,d):return[(e,mu,nu)for e in range(6)for mu in range(N[a][b][e])for nu in range(N[e][c][d])]
def right(a,b,c,d):return[(f,mu,nu)for f in range(6)for mu in range(N[b][c][f])for nu in range(N[a][f][d])]
def ff(a,b,c,d,l,r,variant=1,kappa=1,eps=1):
 e,mu,nu=l;f,rho,sig=r
 if 0 in [a,b,c]:return s.Integer(int(mu+nu==rho+sig))
 if 5 not in [a,b,c,d]:
  if a<4 and b==4 and c<4:return s.Integer(chi(a,c))
  if a==4 and b<4 and c==4:return s.Integer(chi(b,d))
  if a==b==c==4:return s.Rational(chi(e,f),2)
  return s.Integer(1)
 if a<4 and b<4 and c==5:return L[a,b]
 if a==5 and b<4 and c<4:return L[b,c]
 if a<4 and b==4 and c==5:return P[a][nu,rho]
 if a==5 and b==4 and c<4:return P[c][mu,sig]
 if a==4 and b<4 and c==5:return Q[b][nu,sig]
 if a==5 and b<4 and c==4:return Q[b][nu,sig]
 if a==b==4 and c==5:return W[e][rho,sig]
 if a==5 and b==c==4:return W[f][mu,nu]
 if a==b==5 and c<4:
  return L[c,d]if d<4 else P[c][mu,sig]
 if a<4 and b==c==5:
  return L[d,a]if d<4 else [I,-Z,-X,i*Y][a][nu,rho]
 if a==b==5 and c==4:
  return [(-X+Z)/rt,(-I+i*Y)/rt,(I+i*Y)/rt,(X+Z)/rt][d][mu,rho]if d<4 else[-I/rt,Z/rt,X/rt,-i*Y/rt][e][rho,sig]
 if a==4 and b==c==5:
  return[I,X,Z,i*Y][d][mu,rho]if d<4 else W[f][mu,nu]
 if a<4 and b==5 and c<4:return K[a,c]
 if a==4 and b==5 and c<4:return[I,variant*Y,-variant*Y,-I][c][mu,sig]
 if a<4 and b==5 and c==4:return[I,-variant*Y,variant*Y,-I][a][nu,rho]
 if a==4 and b==5 and c==4:
  M=s.Matrix([[1+i,-1+i,-1+i,1+i],[-1+i,1+i,-1-i,1-i],[-1+i,-1-i,1+i,1-i],[1+i,1-i,1-i,1+i]])
  if variant==-1:M=s.conjugate(M)
  return kappa*M[2*mu+nu,2*rho+sig]/(2*rt)
 if a==5 and b<4 and c==5:
  return K[b,d]if d<4 else[I,variant*Y,-variant*Y,-I][b][nu,sig]
 if a==5 and b==4 and c==5:
  if d<4:return[(-X+Z)/rt,-variant*i*(X+Z)/rt,variant*i*(X+Z)/rt,(X-Z)/rt][d][mu,rho]
  M=s.Matrix([[1,-1,-1,-1],[i,i,i,-i],[-i,-i,-i,i],[1,-1,-1,-1]])/2
  if variant==-1:M=s.conjugate(M)
  return kappa*M[2*mu+nu,2*rho+sig]
 if a==b==c==5:
  if e<4 and f<4:return eps*s.Matrix([[1,1,1,-1],[1,-1,-1,-1],[1,-1,-1,-1],[-1,-1,-1,1]])[e,f]/(2*rt)
  if e<4:return eps*[-I/2,variant*Y/2,-variant*Y/2,-I/2][e][rho,sig]
  if f<4:return eps*[(X-Z)/(2*rt),-variant*i*(X+Z)/(2*rt),variant*i*(X+Z)/(2*rt),(X-Z)/(2*rt)][f][mu,nu]
  M=s.Matrix([[1,-1,-i,-i],[-1,-1,-i,i],[i,i,1,-1],[i,-i,-1,-1]])
  if variant==-1:M=s.conjugate(M)
  return eps*kappa*M[2*mu+nu,2*rho+sig]/(2*rt)
 raise ValueError((a,b,c,d,l,r))
def J(a,b,c):
 n=N[a][b][c]
 if a==4 and b==5:return Y
 if a==5 and b==4:return -Y
 if a==b==5 and c==4:return Y
 if a==5 and b==5 and c<4:return s.Matrix([[sg[c]]])
 if a<4 and b==5:return s.Matrix([[sg[a]]])
 if a==5 and b<4:return s.Matrix([[sg[b]]])
 return s.eye(n)
def check():
 count=0
 for v,kap,eps in itertools.product([1,-1],repeat=3):
  for a,b,c,d in itertools.product(range(6),repeat=4):
   Ls=left(a,b,c,d);Rs=right(a,b,c,d)
   if not Ls:continue
   F=s.Matrix([[ff(a,b,c,d,l,r,v,kap,eps)for r in Rs]for l in Ls])
   A=s.diag(*[s.kronecker_product(J(a,b,e),J(e,c,d))for e in range(6)if N[a][b][e]*N[e][c][d]])
   B=s.diag(*[s.kronecker_product(J(b,c,f),J(a,f,d))for f in range(6)if N[b][c][f]*N[a][f][d]])
   if any(s.simplify(x)!=0 for x in A*F-F*B):print('FAIL',v,kap,eps,a,b,c,d,A,F,B,flush=True);return False
   count+=len(Ls)*len(Rs)
 print('ALL SOFT COHERENCE PASS',count,flush=True);return True
if __name__=='__main__':check()
