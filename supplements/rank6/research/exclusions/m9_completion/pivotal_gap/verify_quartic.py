"""General obstruction for R6_9_8099/8101: exact cyclic-quartic signed spectrum.
No associator search, optimization, floats, pivotality, or pseudo-unitarity.
All proof conditions use explicit checks, hence run identically under python -O.
"""
import hashlib,itertools,json,math,time
from fractions import Fraction as F
from pathlib import Path
import sympy as s
from sympy.matrices.normalforms import hermite_normal_form
from sympy.polys.numberfields import round_two

from common import tensors as input_tensors
x=s.symbols('x');h=s.Poly(x**4-x**3-4*x*x+4*x+1,x)

def need(test,msg):
 if not test:raise ValueError(msg)
def flat(M):return [v for row in M.tolist() for v in row]
def integers(M):return all(v.q==1 for v in M)
def matrix_rows(M):return [[str(v) for v in row] for row in M.tolist()]
def integral_lattice(rows):
 A=s.Matrix.vstack(s.eye(4),*rows);q=s.ilcm(*[s.denom(z) for z in A]);B=hermite_normal_form((q*A.T).applyfunc(int));return q*B.inv().T

def run(source_root=None):
 started=time.monotonic()
 need(h.is_irreducible,'field polynomial reducible')
 O,disc=round_two(h)
 need(O.matrix.to_Matrix()/O.denom==s.eye(4) and disc==1125,'incorrect maximal order')
 C=s.zeros(4)
 for j in range(4):
  p=s.rem(x**(j+1),h.as_expr(),x)
  for i in range(4):C[i,j]=p.coeff(x,i)
 P=[C**i for i in range(4)]
 def mul(v):return sum((a*p for a,p in zip(v,P)),s.zeros(4))
 # sigma(r) has order4; sqrt5 is its quadratic subfield generator.
 sigma=-x**3-x*x+3*x+2
 need(s.rem(h.as_expr().subs(x,sigma),h.as_expr(),x)==0,'not automorphism')
 orbit=[x]
 for i in range(4):orbit.append(s.rem(orbit[-1].subs(x,sigma),h.as_expr(),x))
 need(orbit[-1]==x and len(set(orbit[:-1]))==4,'Galois group not proved C4')
 q5=1-6*x+2*x**3
 need(s.rem(q5*q5-5,h.as_expr(),x)==0,'quadratic subfield incorrect')
 fp=s.Poly(x*x-4225*x+21125,x)
 gs={8099:s.Poly(x**4-300*x**3+5250*x*x-22500*x+28125,x),8101:s.Poly(x**4-300*x**3+26250*x*x-562500*x+703125,x)}
 # Ascending coefficients of all roots in the maximal-order basis1,r,r²,r³.
 Ds=[[3055,-5655,0,1885],[1170,5655,0,-1885]]
 qs={8099:[[95,390,-40,-110],[-35,-170,60,70],[245,-190,-60,50],[-5,-30,40,-10]],8101:[[145,110,-40,-30],[15,70,20,-10],[135,-70,-20,10],[5,-110,40,30]]}
 for v in Ds:need(mul(v).charpoly(x).as_poly()==fp**2,'wrong quadratic embedding')
 Ls={}
 for idx in gs:
  need(gs[idx].is_irreducible,'quartic codegree not irreducible')
  for v in qs[idx]:need(mul(v).charpoly(x).as_poly()==gs[idx],'wrong quartic embedding')
  need(len(set(map(tuple,qs[idx])))==4,'missing quartic conjugate')
  Ls[idx]=integral_lattice([mul(v).inv() for v in Ds+qs[idx]])
  need(integers(Ls[idx]),'nonintegral ideal basis')
 L=65*s.Matrix([[1,0,0,0],[0,1,0,0],[-8,-13,15,0],[-7,-4,0,15]])
 need(Ls[8099]==L,'common ideal incorrect')
 need(integers(L.inv()*Ls[8101]),'8101 ideal not contained in common ideal')
 traces=s.Matrix([[s.trace(p) for p in P]])
 need(s.gcd_list(list(traces*L))==975,'trace ideal incorrect')
 # Bind the argument to both complete input tensors.
 tensors=[]
 for row in input_tensors(source_root):
  if row['id'] not in ['R6_9_8099','R6_9_8101']:continue
  R=row['N'];N=list(map(s.Matrix,R));need(len(R)==6,'rank')
  for i,j,k in itertools.product(range(6),repeat=3):
   need(type(R[i][j][k]) is int and R[i][j][k]>=0,'coefficient')
   need(R[0][i][j]==int(i==j) and R[i][j][0]==int(i==j),'unit/selfduality')
   need(R[i][j][k]==R[j][i][k]==R[i][k][j],'symmetry')
  for i,j in itertools.product(range(6),repeat=2):need(N[i]*N[j]==sum((R[i][j][k]*N[k] for k in range(6)),s.zeros(6)),'associativity')
  cas=sum((M*M for M in N),s.zeros(6));need(cas.charpoly(x).as_poly()==fp*gs[row['index']],'codegree profile')
  need(s.trace(cas)==4525,'trace cap')
  tensors.append({'id':row['id'],'tensor_sha256':hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest(),'casimir_trace':4525})
 need(len(tensors)==2,'input tensors missing')
 # Rational isolation intervals for all four real embeddings.
 denominator=10**8;lower=[-195629521,-20905693,133826121,182709091]
 for q in lower:need(h.count_roots(s.Rational(q,denominator),s.Rational(q+1,denominator))==1,'root interval')
 # If theta is totally positive of trace t, each coordinate equals
 # Tr(theta*b_i^vee), so |coordinate|<2t. Verify the dual bound exactly.
 H=s.Matrix(4,4,lambda i,j:s.trace(P[i]*P[j]));Hi=H.inv();dual_polys=[]
 for i in range(4):
  B=sum((Hi[i,j]*P[j] for j in range(4)),s.zeros(4));poly=B.charpoly(x).as_poly()
  need(poly.count_roots(-2,2)==4,'trace-dual coefficient bound')
  dual_polys.append(list(map(str,poly.all_coeffs())))
 a,b,c,d=s.symbols('a b c d');coeff=s.lambdify((a,b,c,d),mul([a,b,c,d]).charpoly(x).all_coeffs(),'math',cse=True)
 def positive(v,t):
  a,b,c,d=v;error=34*t*denominator**2
  for q in lower:
   value=((d*q+c*denominator)*q+b*denominator**2)*q+a*denominator**3
   if value<-error:return False
   need(value>error,'undecided rational sign interval')
  return True
 def pairs(cs,t):
  remainder=1+F(cs[3],65*cs[4])
  if remainder<=0:return []
  A,B=remainder.numerator,remainder.denominator;out=[]
  for k in range(1,(4525-65*t)//A+1):
   S,N=A*k,B*k;disc=S*S-4*N
   if disc<0 or S<=2 or N<=S-1:continue
   r=math.isqrt(disc)
   if r*r==disc:
    if (S-r)%2 or (S-r)//2<=1:continue
   else:
    if S*S%N or disc%5 or math.isqrt(disc//5)**2*5!=disc:continue
   out.append([S,N])
  return out
 stats=[];candidates=[]
 for t in [15,30,45,60]:
  counts={'theta_trace':t,'positive':0,'dnumber':0,'complementary_pairs':0}
  for a,b in itertools.product(range(-2*t+1,2*t),repeat=2):
   residue=(-8*a-13*b)%15;lo=-2*t+1;lo+=(residue-lo)%15
   for c in range(lo,2*t,15):
    d=t-4*a-b-9*c
    if abs(d)>=2*t:continue
    v=[a,b,c,d]
    need((d+7*a+4*b)%15==0,'second ideal congruence')
    if not positive(v,t):continue
    counts['positive']+=1;cs=list(map(int,coeff(*v)));need(cs[1]==-t and cs[-1]>0,'positive charpoly')
    norm=cs[-1]
    if any(cs[j]**4%norm**j for j in range(1,5)):continue
    counts['dnumber']+=1;ps=pairs(cs,t);counts['complementary_pairs']+=len(ps)
    candidates.append({'theta':v,'theta_polynomial':cs,'remaining_pairs':ps})
  stats.append(counts)
 need([(r['positive'],r['dnumber'],r['complementary_pairs']) for r in stats]==[(0,0,0),(6,6,0),(28,12,0),(69,21,0)],'spectrum enumeration differs')
 return {'kind':'cyclic_quartic_signed_spectrum_exclusion','scope':'general_complex_fusion_categories','tensors':tensors,'field_polynomial':list(map(int,h.all_coeffs())),'field_discriminant':int(disc),'maximal_order_basis':'1,r,r²,r³','codegree_ideal_bases':{str(i):matrix_rows(v) for i,v in Ls.items()},'common_trace_ideal':975,'trace_parameters':[15,30,45,60],'exact_root_interval_denominator':denominator,'exact_root_interval_lower_numerators':lower,'trace_dual_polynomials':dual_polys,'counts':stats,'dnumber_candidates':candidates,'complete':True,'seconds':time.monotonic()-started}

