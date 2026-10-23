"""General two-orbit obstruction from dimensions of summands of I(1).

Schopieray Lem3.1 supplies a Galois-pseudo-unitary categorification whenever
one exists. In a commutative ring every simple summand of I(1) occurs once,
with dimension D/f for an ordinary formal codegree f. Its restriction has
FP dimension a+b*d with integers a>=1,b>=0.
"""
from arithmetic import *
from fractions import Fraction
import math

def rational_square(q):
 q=s.Rational(q)
 if q<0:return None
 a,b=math.isqrt(int(q.p)),math.isqrt(int(q.q))
 return s.Rational(a,b) if a*a==q.p and b*b==q.q else None

def data(R):
 if not comm(R):return None
 n=len(R);du=[next(j for j in range(n)if R[i][j][0])for i in range(n)];G=[i for i in range(n)if sum(R[i][du[i]])==1];X=[i for i in range(n)if i not in G]
 if not X:return None
 x=X[0]
 if {next(k for k in range(n)if R[g][x][k])for g in G}!=set(X):return None
 H=[g for g in G if R[g][x][x]];r=sum(R[x][du[x]][i]for i in X);ss=len(H);disc=r*r+4*ss
 if math.isqrt(disc)**2==disc:return None
 return dict(invertibles=G,noninvertibles=X,object=x,stabilizer=H,r=r,s=ss,discriminant=disc,D=[len(G)+len(X)*ss,len(X)*r])

def certificate(R):
 z=data(R)
 if not z:return None
 r,ss=z['r'],z['s'];disc=z['discriminant'];DA,DB=map(s.Rational,z['D'])
 for q,m in casimir(R).charpoly(t).as_poly().factor_list()[1]:
  co=list(map(int,q.all_coeffs()));roots=[]
  if q.degree()==1:roots=[(-s.Rational(co[1]),s.S.Zero)]
  elif q.degree()==2:
   dc=co[1]**2-4*co[2];h=rational_square(s.Rational(dc,disc))
   if h is None:
    return dict(kind='two_dimension_induction',**z,failed_factor=co,reason='codegree_field_not_contained',codegree_discriminant=dc,scope='general_complex_fusion_category')
   roots=[((-co[1]-eps*h*r)/2,eps*h)for eps in [-1,1]]
  else:
   return dict(kind='two_dimension_induction',**z,failed_factor=co,reason='codegree_field_degree',scope='general_complex_fusion_category')
  for a,b in roots:
   norm=a*a+a*b*r-b*b*ss
   ca=(DA*(a+b*r)-DB*b*ss)/norm;cb=(DB*a-DA*b)/norm
   if ca.q!=1 or cb.q!=1 or ca<1 or cb<0:
    return dict(kind='two_dimension_induction',**z,failed_factor=co,codegree_coordinates=list(map(str,[a,b])),restriction_dimension_coordinates=list(map(str,[ca,cb])),reason='not_nonnegative_integral_dimension_sum',scope='general_complex_fusion_category')
 return None

def verify(R,c):
 if certificate(R)!=c:raise ValueError('two-dimension induction certificate mismatch')
 return True

def main():
 out=[]
 for r in read():
  c=certificate(r['tensor'])
  if c:verify(r['tensor'],c);print(r['id'],c['restriction_dimension_coordinates']if'restriction_dimension_coordinates'in c else c['reason'],flush=True)
  out.append(dict(id=r['id'],rank=r['rank'],tensor_sha256=r['tensor_sha256'],certificate=c))
 (HERE/'two_dimension_induction.json').write_text(json.dumps(out,indent=2)+'\n')
 print('TOTAL',sum(r['certificate']is not None for r in out))
if __name__=='__main__':main()
