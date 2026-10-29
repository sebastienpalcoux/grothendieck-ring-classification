"""Rank-independent adapter of the existing scalar-character/weighted-codegree method.
Only semisimple signed based *-algebras of dimension nine are used here.
"""
from common import *
import sympy as s
from rings import Characters,matrices,dual,casimir
from exact import *
class ScalarCharacters:
 def __init__(self,R):
  self.R=R;self.N=N=matrices(R);self.n=n=len(R);self.du=dual(R);self.C=casimir(R)
  W=s.Matrix.vstack(*(N[i]*N[j]-N[j]*N[i] for i in range(n) for j in range(i))).nullspace()
  self.scalar_rank=m=len(W)
  require(n==9 and m in [0,1,5,9],'rank-nine Wedderburn shape')
  if not m:self.components=[];self.cf=[];return
  W=s.Matrix.hstack(*W);piv=list(W.T.rref()[1]);J=W.extract(piv,range(m)).inv()
  A=[J*(a*W).extract(piv,range(m)) for a in N]
  self.A=A
  require(all(a*W==W*b for a,b in zip(N,A)),'invariant scalar space')
  for k in range(1,n*(n-1)*(n-2)//2+2):
   H=A[0]+sum((k**(i-1)*A[i] for i in range(1,n)),s.zeros(m));p=H.charpoly(t).as_poly()
   if s.gcd(p,p.diff()).degree()==0:break
  require(s.gcd(p,p.diff()).degree()==0,'scalar separation')
  self.k=k;self.p=p;self.components=p.factor_list()[1]
  V=s.Matrix.hstack(*(s.Matrix(list(H**i)) for i in range(m)))
  piv=list(V.T.rref()[1]);Vi=V.extract(piv,range(m)).inv()
  self.coeff=[]
  for a in A:
   b=Vi*s.Matrix(list(a)).extract(piv,[0]);self.coeff.append(list(b))
   require(sum((b[j]*H**j for j in range(m)),s.zeros(m))==a,'scalar coordinates')
  scalar_C=sum((A[i]*A[self.du[i]] for i in range(n)),s.zeros(m));sp=scalar_C.charpoly(t).as_poly()
  self.scalar_codegree_polynomial=sp
  full=self.C.charpoly(t).as_poly();q,rem=full.div(sp);require(rem.is_zero,'scalar Casimir factor')
  self.cf=list(sp.factor_list()[1])
  for f,e in q.factor_list()[1]:
   require(e%4==0,'matrix-block multiplicity')
   g=s.Poly(f.as_expr().subs(t,2*t)/2**f.degree(),t,domain=s.QQ)
   self.cf.append((g,e//4))
 def component(self,f):
  K=field(f);ds=[K(s.Poly.from_list(list(reversed(c)),t,domain=s.QQ).rem(f).all_coeffs()) for c in self.coeff]
  D=sum((ds[i]*ds[self.du[i]] for i in range(self.n)),K.zero)
  ps=[p for p,m in self.cf if not evaluate(p.all_coeffs(),D,K)]
  require(ps,'scalar codegree not found');return K,ds,D,ps[0]
 def fp(self):
  candidates=[]
  for f,m in self.components:
   K,ds,D,pD=self.component(f)
   for emb in embeddings(f):
    if all(emb.sign(d)>0 for d in ds):candidates.append((f,K,ds,D,pD,emb))
  require(len(candidates)==1,'unique positive scalar character');return candidates[0]
def chars(R):
 return Characters(R) if all(R[i][j]==R[j][i] for i in range(len(R)) for j in range(len(R))) else ScalarCharacters(R)
