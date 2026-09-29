"""Independent brute-force Gram and minimal-polynomial pruning audit."""
import itertools,json,math,sys
from fractions import Fraction as Q
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'software'))
import sympy as s
from exact import require,vector
import cyclotomic_stabilizer_trace as C

def psd(A):
 A=[[Q(x) for x in row] for row in A];n=len(A)
 for j in range(n):
  if A[j][j]<0:return False
  if not A[j][j]:
   if any(A[j][k] for k in range(j+1,n)):return False
   continue
  for k in range(j+1,n):
   for l in range(k,n):
    A[k][l]-=A[k][j]*A[j][l]/A[j][j];A[l][k]=A[k][l]
 return True

def minimal_coefficients(x,K):
 m=K.mod.degree();M=s.Matrix.hstack(*(vector(x*K.unit**j,m) for j in range(m)))
 p=M.charpoly().as_poly().sqf_part().monic()
 return p.all_coeffs()

def integral(coeff):return all(a.q==1 for a in coeff)
def dnumber(coeff):
 if not integral(coeff):return False
 k=len(coeff)-1;norm=abs(int(coeff[-1]));require(norm>0,'zero dimension in pruning audit')
 return all(int(coeff[j])**k%norm**j==0 for j in range(1,k+1))
reports=[]
for rid in ('R6_4_258','R6_4_325'):
 R=next(r['N'] for r in json.loads((ROOT/'data/census.json').read_text()) if r['id']==rid);data=C.data_for(R,3);frames=[]
 for ix,cols in enumerate(data['lows']):
  L=s.Matrix.hstack(*map(s.Matrix,cols));G=(data['ch'].C-L*L.T).extract(range(1,len(R)),range(1,len(R)));n=G.rows
  bounds=[math.isqrt(int(G[i,i])) for i in range(n)];brute=[]
  for v in itertools.product(*(range(b+1) for b in bounds)):
   if not any(v):continue
   H=[[int(G[i,j])-v[i]*v[j] for j in range(n)] for i in range(n)]
   if any(x<0 for row in H for x in row):continue
   if psd(H):brute.append(v)
  native=list(C.native(G));require(sorted(brute)==native,'native Gram vectors differ from full-box PSD enumeration')
  kept=0;division_reject=0;dimension_reject=0
  for v in native:
   z=sum((data['K'](v[i])*data['ds'][i+1] for i in range(n)),data['K'].zero)
   source_div=C.integral_charpoly(data['D']/z,data['K']) is not None
   independent_div=integral(minimal_coefficients(data['D']/z,data['K']))
   require(source_div==independent_div,'ambient characteristic/minimal integrality differ')
   co=C.integral_charpoly(z,data['K']);require(co is not None,'nonintegral dimension')
   source_dim=dnumber(list(map(s.Rational,co)));independent_dim=dnumber(minimal_coefficients(z,data['K']))
   require(source_dim==independent_dim,'ambient characteristic/minimal d-number tests differ')
   if not source_div:division_reject+=1
   elif not source_dim:dimension_reject+=1
   else:kept+=1
  frames.append({'low_frame':ix,'full_box_size':math.prod(b+1 for b in bounds),'gram_diagonal':list(map(int,G.diagonal())),'max_coordinate':max(bounds),'native_vectors':len(native),'independent_gram_match':True,'division_integrality_rejections':division_reject,'dnumber_rejections':dimension_reject,'kept_vectors':kept,'minimal_polynomial_pruning_match':True})
 reports.append({'id':rid,'frames':frames})
print(json.dumps({'complete':True,'reports':reports},indent=2))
