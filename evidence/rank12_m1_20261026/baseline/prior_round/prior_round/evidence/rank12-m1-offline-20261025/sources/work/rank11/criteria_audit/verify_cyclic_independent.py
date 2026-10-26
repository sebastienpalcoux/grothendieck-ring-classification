"""Independent replay of cyclic-stabilizer exclusions; no producer imports."""
from pathlib import Path
import gzip,hashlib,json,math,itertools
import sympy as s
HERE=Path(__file__).parent;ROOT=HERE.parents[2];t=s.Symbol('t')
def need(p,m):
 if not p:raise ValueError(m)
def verify(R,c):
 n=len(R);g=c['g'];h=0;order=None
 for k in range(1,n+1):
  product=R[h][g];need(sum(product)==1,'g not invertible');h=product.index(1)
  if h==0:order=k;break
 need(order==c['order'] and order>1,'order')
 x,y,z=(c[a] for a in ('X','Y','Z'));m=R[x][y][z]
 need(m>0 and m==c['multiplicity'],'coefficient')
 unit=lambda a:[int(i==a) for i in range(n)]
 need(R[g][x]==unit(x) and R[y][g]==unit(y) and R[g][z]==unit(z) and R[z][g]==unit(z),'fixedness')
 # Independent polynomial and exact largest-real-root isolation.
 char=s.det(t*s.eye(n)-s.Matrix(R[z]));f=s.Poly.from_list([s.Rational(a) for a in c['dimension_polynomial']],t)
 need(f.is_irreducible and s.rem(char,f.as_expr(),t)==0,'factor')
 real_roots=s.Poly(char,t).intervals(eps=s.Rational(1,10**20));top=real_roots[-1][0]
 need(top[0]>0,'positive Perron root')
 if top[0]==top[1]:need(f.eval(top[0])==0,'linear Perronroot')
 else:need(f.count_roots(*top)==1,'Perron factor')
 q=order//math.gcd(order,m);scaled=s.Poly(f.as_expr().subs(t,q*t)/q**f.degree(),t)
 need(list(map(str,scaled.all_coeffs()))==c['normalized_dimension_polynomial'],'scaled factor')
 need(any(a.q!=1 for a in scaled.all_coeffs()),'nonintegrality')
 return True

def main():
 p=ROOT/'repositories/fusion-ring-census/results/rank11/tables.txt.gz'
 Rs=[json.loads(l.replace('{','[').replace('}',']')) for l in gzip.open(p,'rt')]
 rows=json.load(open(HERE/'cyclic_results.json'))['records'];need(len(rows)==len(Rs)==182,'count');n=0
 for i,(R,row) in enumerate(zip(Rs,rows),1):
  need(row['id']==f'R11_1_{i}','ID');need(row['tensor_sha256']==hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest(),'tensor hash')
  if row['certificate']:verify(R,row['certificate']);n+=1
 out={'status':'PASS','inputs':182,'certificates':n,'optimized_python':not __debug__,'independent_implementation':True,'arithmetic':'exact determinant, irreducible factors, rational root isolation, scaled minimal polynomials'}
 (HERE/('cyclic_independent_optimized.json' if not __debug__ else 'cyclic_independent.json')).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
if __name__=='__main__':main()
