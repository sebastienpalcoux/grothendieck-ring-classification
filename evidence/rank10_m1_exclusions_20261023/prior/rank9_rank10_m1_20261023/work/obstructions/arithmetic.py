"""Exact rank-independent necessary categorification conditions.

Discovery and certificate checking use integer/rational arithmetic only.
"""
from pathlib import Path
import json,gzip,hashlib,collections,sys,itertools
import sympy as s
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(HERE))
from exact import cyclotomic_failure,check_cyclotomic,t

def sha(R):return hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest()
def read():
 out=[]
 for rank in [9,10]:
  p=ROOT/'inputs'/f'rank{rank}_M1_verified'/'FusionRingMultiplicationTables.txt.gz'
  for i,line in enumerate(gzip.open(p,'rt'),1):
   R=json.loads(line.replace('{','[').replace('}',']'))
   out.append(dict(id=f'R{rank}_1_{i}',rank=rank,tensor_sha256=sha(R),tensor=R))
 return out

def comm(R):return all(R[i][j]==R[j][i] for i in range(len(R)) for j in range(i))
def casimir(R):return sum((s.Matrix(A)*s.Matrix(A).T for A in R),s.zeros(len(R)))
def dnumber(R):
 p=casimir(R).charpoly(t).as_poly()
 for q,e in p.factor_list()[1]:
  co=list(map(int,q.all_coeffs()));d=q.degree();N=abs(co[-1])
  for j in range(1,d+1):
   rem=pow(co[j],d,N**j)
   if rem:
    return dict(kind='casimir_dnumber',factor=co,multiplicity=e,index=j,nonzero_remainder=rem,
     scope='general_complex_fusion_category',reference='Ostrik, On formal codegrees of fusion categories, Theorem 1.2 and Lemma 2.7; d-number property invariant under multiplication by rational integers')

def verify_dnumber(R,c):
 q=s.Poly.from_list(c['factor'],t);p=casimir(R).charpoly(t).as_poly();d=q.degree();co=list(map(int,q.all_coeffs()));j=c['index'];N=abs(co[-1]);rem=pow(co[j],d,N**j)
 assert q.is_irreducible and p.rem(q).is_zero and 1<=j<=d and rem and rem==c['nonzero_remainder']

def cyclotomic(R):
 if not comm(R):return None
 polys=[s.Matrix(A).charpoly(t).as_poly() for A in R]
 c=cyclotomic_failure(polys)
 if c:check_cyclotomic(polys,c)
 return c

def integral_dimensions(R):
 n=len(R);A=sum(map(s.Matrix,R),s.zeros(n));p=A.charpoly(t).as_poly()
 for q,e in p.factor_list()[1]:
  if q.degree()!=1:continue
  val=-q.TC();vs=(A-val*s.eye(n)).nullspace()
  if len(vs)!=1 or not vs[0][0]:continue
  d=[s.cancel(x/vs[0][0]) for x in vs[0]]
  if not all(v>0 and v.q==1 for v in d):continue
  d=list(map(int,d))
  assert all(sum(R[i][j][k]*d[k] for k in range(n))==d[i]*d[j] for i in range(n) for j in range(n))
  return d

def integral_drinfeld(R):
 if not comm(R):return None
 dims=integral_dimensions(R)
 if dims is None:return None
 D=sum(d*d for d in dims)
 for q,e in casimir(R).charpoly(t).as_poly().factor_list()[1]:
  if q.degree()>1 or D%int(-q.TC()):
   return dict(kind='integral_drinfeld',dims=dims,global_dimension=D,failed_factor=list(map(int,q.all_coeffs())),scope='general_complex_fusion_category')

def near_group(R):
 n=len(R);du=[next(j for j in range(n) if R[i][j][0]) for i in range(n)];G=[i for i in range(n) if sum(R[i][du[i]])==1]
 if len(G)!=n-1 or not comm(R):return None
 x=next(i for i in range(n) if i not in G);k=R[x][x][x]
 if 0<k<len(G)-1 and all(R[x][x][g]==1 and R[x][g][x]==R[g][x][x]==1 for g in G):
  return dict(kind='near_group_small_m',invertibles=G,object=x,kappa=k,scope='general_complex_fusion_category',reference='Schopieray, Categorification of integral group rings extended by one dimension, Proposition 3.2')

def main():
 rows=read();allout=[]
 for i,r in enumerate(rows):
  R=r['tensor'];out={k:v for k,v in r.items() if k!='tensor'};out['commutative']=comm(R);cs=[]
  for fn in [near_group,dnumber,cyclotomic,integral_drinfeld]:
   c=fn(R)
   if c:cs.append(c)
  out['certificates']=cs;allout.append(out)
  if cs:print(out['id'],[c['kind'] for c in cs],flush=True)
  if (i+1)%20==0:
   (HERE/'arithmetic.json').write_text(json.dumps(allout,indent=2)+'\n')
 (HERE/'arithmetic.json').write_text(json.dumps(allout,indent=2)+'\n')
 print('TOTAL',len(allout),'EXCLUDED',sum(bool(x['certificates']) for x in allout),dict(collections.Counter(c['kind'] for x in allout for c in x['certificates'])))
if __name__=='__main__':main()
