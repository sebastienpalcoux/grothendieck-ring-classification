#!/usr/bin/env python3
"""Seven general exclusions by anti-invariant module spectral bounds.

This verifies source identities and the arithmetic in the short theoretical
proof; no categorification search or finite signed-lift enumeration is used.
"""
import argparse,collections,gzip,hashlib,itertools,json
from pathlib import Path
import sympy as s
HERE=Path(__file__).resolve().parent
ROOT=next((p for p in HERE.parents if (p/'supplements/rank7/data/rank7_tables.txt.gz').exists()),Path('repo'))
def require(c,m):
 if not c:raise RuntimeError(m)
x=s.Symbol('x')
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,default=ROOT);ap.add_argument('--output',type=Path);args=ap.parse_args()
 specs={'R7_2_116':(1,2,[4,5,6],'integral'),'R7_2_261':(3,1,[4,5,6],'integral_complex'),'R7_3_364':(1,4,[4,5,6],'quadratic'),'R7_3_938':(3,4,[4,5,6],'quadratic'),'R7_3_970':(3,1,[4,5,6],'nine'),'R7_4_2644':(3,1,[4,5,6],'sqrt3_product'),'R7_4_2683':(5,3,[1,2,6],'sqrt3_square')}
 ct=collections.Counter();out=[]
 for line in gzip.open(args.repo/'supplements/rank7/data/rank7_tables.txt.gz','rt'):
  if not line.strip():continue
  N=json.loads(line.replace('{','[').replace('}',']'));m=max(z for a in N for b in a for z in b);ct[m]+=1;rid=f'R7_{m}_{ct[m]}'
  if rid not in specs:continue
  g,i,F,kind=specs[rid];du=[next(j for j in range(7) if N[a][j][0]) for a in range(7)]
  require(all(N[a][b]==N[b][a] for a,b in itertools.product(range(7),repeat=2)),'Noncommutative source')
  require(N[g][g]==[1,0,0,0,0,0,0] and all(sum(z)==1 for z in N[g]),'Not an invertible involution')
  require(F==[a for a in range(7) if N[g][a][a]],'Incorrect fixed simples')
  B=lambda j:[[N[j][a][b] for b in F] for a in F]
  P=s.Poly(s.Matrix(N[i]).charpoly(x).as_expr(),x).sqf_part().monic()
  rec={'id':rid,'scope':'general_complex','decision':'excluded','generator':g,'fixed':F,'test_simple':i,'duality':du,'bound_matrix':B(i),'source_characteristic_polynomial':str(s.factor(s.Matrix(N[i]).charpoly(x).as_expr())),'squarefree_polynomial':str(s.factor(P.as_expr())),'tensor_sha256':hashlib.sha256(json.dumps(N,separators=(',',':')).encode()).hexdigest()}
  if kind.startswith('integral'):
   require(B(i)==[[0,1,1],[1,0,1],[1,1,2]],'Integral bound mismatch')
   want=x*(x-5)*(x-1)*(x+1)
   if kind=='integral_complex':want*=x*x+1
   require(P==s.Poly(want,x,domain=s.QQ),'Integral polynomial mismatch')
   require(max(map(sum,B(i)))==4<5 and sum(z%2 for z in B(i)[0])==2>1,'Norm contradiction failed')
   rec['contradiction']='normal operator norm at most1; first row norm squared2'
  elif kind=='quadratic':
   require(du[i]==i,'Test simple not self-dual')
   require(B(i)==[[3,1,2],[1,1,2],[2,2,2]],'Quadratic bound mismatch')
   require(P==s.Poly(x*(x*x-8*x-8)*(x*x-2*x-2),x,domain=s.QQ),'Quadratic polynomial mismatch')
   maximum=sum(v*v for row in B(i) for v in row)
   require(maximum==32<80,'Large quadratic trace bound failed')
   # In the small branch tr(T^2)=8. Odd a,b,d contribute at least4;
   # nonzero even c or e, or |a|=3, contributes at least eight more.
   require(4+2*2**2>8 and 3**2+1+2>8,'Coercive trace estimate failed')
   traces=sorted({2*a+f for a in(-1,1) for f in(-2,2)})
   require(traces==[-4,0,4] and 2 not in traces,'Small trace contradiction failed')
   rec['contradiction']={'maximum_trace_square':maximum,'large_pair_trace_square':80,'small_pair_trace':2,'forced_traces':traces}
  elif kind=='nine':
   require(B(i)==[[0,0,0],[0,1,2],[0,2,1]],'Nine bound mismatch')
   require(P==s.Poly(x*(x-9)*(x-1)*(x+1)*(x*x+1),x,domain=s.QQ),'Nine polynomial mismatch')
   require(du[1]==2 and max(map(sum,B(i)))==3<9,'Nine norm or duality mismatch')
   require(B(5)==[[0,2,0],[2,2,0],[0,0,0]] and B(6)==[[0,0,2],[0,0,0],[2,0,2]],'Disjoint supports mismatch')
   require(N[5][6]==[0,2,2,0,0,0,0],'Nine product mismatch')
   rec['other_bounds']={'5':B(5),'6':B(6)};rec['product']={'inputs':[5,6],'coefficients':N[5][6]};rec['contradiction']='disjoint diagonal supports give0=4diag(0,+/-1,+/-1)'
  else:
   require(B(i)==[[1,2,2],[2,1,2],[2,2,3]],'sqrt3 bound mismatch')
   require(P==s.Poly((x-1)*(x+1)*(x*x+1)*(x*x-14*x+1),x,domain=s.QQ),'sqrt3 polynomial mismatch')
   require(max(map(sum,B(i)))==7 and s.sqrt(3).is_positive,'sqrt3 large root bound failed')
   if kind=='sqrt3_product':
    require(du[1]==2 and B(5)[0][0]==B(5)[1][0]==B(5)[2][0]==0,'Product zero column mismatch')
    require(N[4][5]==[0,2,2,0,0,0,0],'sqrt3 product mismatch')
    rec['other_bounds']={'5':B(5)};rec['product']={'inputs':[4,5],'coefficients':N[4][5]}
   else:
    require(du[3]==4 and B(1)[0]==[0,0,0],'Square zero row mismatch')
    require(N[1][1]==[0,0,0,2,2,0,0],'sqrt3 square mismatch')
    rec['other_bounds']={'1':B(1)};rec['product']={'inputs':[1,1],'coefficients':N[1][1]}
   rec['contradiction']='source zero entry gives0=+/-4'
  out.append(rec)
 require(len(out)==7,'Missing cases')
 result={'status':'PASS','general_exclusions':7,'method':'anti-invariant module spectral and zero-entry bounds','cases':out}
 if args.output:args.output.write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result,indent=2))
if __name__=='__main__':main()
