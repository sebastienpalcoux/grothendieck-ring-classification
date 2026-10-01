"""Exclude the quadratic signed-dimension-field sector of R6_9_7018.
General category hypotheses; conclusion conditional on [K:Q]=2 only.
"""
import itertools,json,hashlib,math,time
from fractions import Fraction as F
from pathlib import Path
import sympy as s
from common import tensors as input_tensors

def need(v,msg):
 if not v:raise ValueError(msg)
def rank2(A):
 A=[row[:] for row in A];r=0
 for col in range(len(A[0])):
  k=next((k for k in range(r,len(A)) if A[k][col]%2),None)
  if k is None:continue
  A[r],A[k]=A[k],A[r]
  for j in range(len(A)):
   if j!=r and A[j][col]%2:A[j]=[(x+y)%2 for x,y in zip(A[j],A[r])]
  r+=1
 return r

def integer(a,b):return (2*a).denominator==1 and (2*b).denominator==1 and (a-b).denominator==1

def divintegral(A,B,S,b,N):return integer(F(A*S-5*B*b,4*N),F(B*S-A*b,4*N))

def run(source_root=None):
 start=time.monotonic();row=next(r for r in input_tensors(source_root) if r['id']=='R6_9_7018');R=row['N'];z=s.symbols('z');N=list(map(s.Matrix,R));C=sum((M*M for M in N),s.zeros(6))
 for i,j,k in itertools.product(range(6),repeat=3):
  need(type(R[i][j][k]) is int and R[i][j][k]>=0,'coefficient')
  need(R[0][i][j]==int(i==j) and R[i][j][0]==int(i==j),'unit/selfdual')
  need(R[i][j][k]==R[j][i][k]==R[i][k][j],'symmetry')
 for i,j in itertools.product(range(6),repeat=2):need(N[i]*N[j]==sum((R[i][j][k]*N[k] for k in range(6)),s.zeros(6)),'associativity')
 original=(z*z-4225*z+21125)*(z*z-150*z+1125)*(z*z-30*z+45)
 need(C.charpoly(z).as_poly()==s.Poly(original,z) and s.trace(C)==4405,'codegrees or trace')
 # Since Frobenius²=identity, algebra mod2 is etale with factorsF2/F4.
 # Fixed-space dimension3 and totaldimension6 forceexactlyF4³.
 Frobenius=s.Matrix(6,6,lambda i,j:R[j][j][i]%2)
 need(all(int(v)%2==0 for v in Frobenius**2-s.eye(6)),'Frobenius²')
 need(rank2([[int(v)%2 for v in rr] for rr in (Frobenius-s.eye(6)).tolist()])==3,'F4³')
 # All originalcodegree ideals are c sqrt5 O_E, c=65,15,3.
 # The displayed ratios are integralunits ofnorm-1.
 need(F(29*29-5*13*13,4)==-1 and 2*2-5==-1,'units')
 need(math.lcm(65,15,3)==195,'idealintersection')
 expected=[int(v)%2 for v in s.Poly(original,z).all_coeffs()];out=[]
 for y in range(1,5):
  for x in range(-math.isqrt(5*y*y-1),math.isqrt(5*y*y-1)+1):
   if (x-y)%2:continue
   n=5*y*y-x*x
   if 20*y*y%n:continue
   A=975*y;B=195*x;norm=(A*A-5*B*B)//4;rem=1-F(A,norm);cap=4405-A
   if rem<=0:continue
   ps=[]
   for normf in map(int,s.divisors(norm)):
    for S in range(3,cap-3+1):
     disc=S*S-4*normf
     if disc<0 or normf<=S-1:continue
     if disc==0:
      if S%2:continue
      b=0
     else:
      if disc%5 or math.isqrt(disc//5)**2*5!=disc or S*S%normf:continue
      b=math.isqrt(disc//5)
      if (S-b)%2:continue
     if not(divintegral(A,B,S,b,normf) and divintegral(A,B,S,-b,normf)):continue
     ps.append((S,normf,b))
   matches=[]
   for i,p in enumerate(ps):
    for q in ps[i:]:
     if p[0]+q[0]>cap or F(p[0],p[1])+F(q[0],q[1])!=rem:continue
     polynomial=(z*z-A*z+norm)*(z*z-p[0]*z+p[1])*(z*z-q[0]*z+q[1]);parity=[int(v)%2 for v in s.Poly(polynomial,z).all_coeffs()]
     need(parity!=expected,'admissible spectrum remains')
     matches.append({'pairs':[p,q],'casimir_mod2':parity,'rejected':'Casimir polynomial mod2'})
   out.append({'y':y,'x':x,'Delta_trace':A,'Delta_norm':norm,'pair_candidates':len(ps),'pre_parity_matches':matches})
 need(len(out)==16 and sum(len(r['pre_parity_matches']) for r in out)==2,'inventory')
 return {'id':'R6_9_7018','tensor_sha256':hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest(),'kind':'quadratic_signed_spectrum_exclusion','scope':'general_complex_fusion_categories_conditional_on_signed_dimension_field_degree2','quadratic_radicand':5,'signed_mod2_algebra':'F4 × F4 × F4','original_Casimir_mod2':expected,'ideal_scale':195,'trace_bound':4405,'trace_parameter_upper_bound':4,'spectra':out,'complete':True,'seconds':time.monotonic()-start}
