#!/usr/bin/env python3
"""Two general exclusions: source-bound theoretical signed C3 argument."""
import argparse,collections,gzip,hashlib,json,itertools
from pathlib import Path
import sympy as s
HERE=Path(__file__).resolve().parent
ROOT=next((p for p in HERE.parents if (p/'supplements/rank7/data/rank7_tables.txt.gz').exists()),Path('.'))

def require(c,msg):
 if not c:raise RuntimeError(msg)

def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,default=ROOT);p.add_argument('--output',type=Path);args=p.parse_args();specs={'R7_3_783':(4,-1),'R7_3_1015':(5,1)};ct=collections.Counter();out=[];x=s.Symbol('x')
 for line in gzip.open(args.repo/'supplements/rank7/data/rank7_tables.txt.gz','rt'):
  N=json.loads(line.replace('{','[').replace('}',']'));m=max(t for a in N for b in a for t in b);ct[m]+=1;rid=f'R7_{m}_{ct[m]}'
  if rid not in specs:continue
  E,r=specs[rid];g=1;rho=6
  gp=[0,g,next(j for j in range(7) if N[g][g][j])];orb=[next(j for j in range(7) if N[a][rho][j]) for a in gp]
  require(len(set(gp+[E]+orb))==7,'Not a full basis')
  vec=lambda pairs:[sum(c for k,c in pairs if k==j) for j in range(7)]
  pred=[[[0]*7 for _ in range(7)] for _ in range(7)]
  for a,b in itertools.product(range(3),repeat=2):pred[gp[a]][gp[b]]=vec([(gp[(a+b)%3],1)])
  for a in range(3):
   pred[gp[a]][E]=pred[E][gp[a]]=vec([(E,1)])
   for b in range(3):
    pred[gp[a]][orb[b]]=vec([(orb[(a+b)%3],1)])
    pred[orb[b]][gp[a]]=vec([(orb[(b+r*a)%3],1)])
  pred[E][E]=vec([(k,1) for k in gp]+[(E,3)]+[(k,1) for k in orb])
  for a in range(3):
   pred[E][orb[a]]=pred[orb[a]][E]=vec([(E,1)]+[(k,2) for k in orb])
   for b in range(3):pred[orb[a]][orb[b]]=vec([(gp[(a+r*b)%3],1),(E,2)]+[(k,2) for k in orb])
  require(pred==N,'Model rules do not match all343 coefficients')
  require(N[rho][rho][0]==1 and N[E][E][0]==1,'Positive-FS objects not self-dual')
  branches=[{'a':a,'b':b,'required_sum_c':3*a*a-b*a,'possible':3*a*a-b*a<=6} for a,b in itertools.product([-2,2],[-1,3])]
  require([(z['a'],z['b'],z['required_sum_c']) for z in branches if z['possible']]==[(2,3,6)],'Unexpected signed branch')
  mats=list(map(s.Matrix,N));C=sum((A*A.T for A in mats),s.zeros(7));poly=C.charpoly(x).as_expr();expected=(x-15)*(x-6)**4*(x*x-240*x+900)
  require(s.expand(poly-expected)==0,'Wrong Casimir polynomial')
  lhs=s.Rational(240**2-4*900,900**2);require(lhs==s.Rational(1,15)>s.Rational(1,60),'Dimension-block inequality check')
  require(all(s.Rational(d*d,900).q!=1 for d in [6,15]),'Norm obstruction failed')
  out.append({'id':rid,'scope':'general_complex','decision':'excluded','g':g,'E':E,'rho':rho,'orbit':orb,'commutation_exponent':r,'source_coefficients_checked':343,'signed_branches':branches,'Casimir_polynomial':str(s.factor(poly)),'dimension_block_left':str(lhs),'dimension_block_bound':'1/60','tensor_sha256':hashlib.sha256(json.dumps(N,separators=(',',':')).encode()).hexdigest()})
 require(len(out)==2,'Missing source');res={'status':'PASS','general_exclusions':2,'cases':out}
 if args.output:args.output.write_text(json.dumps(res,indent=2)+'\n')
 print(json.dumps(res,indent=2))
if __name__=='__main__':main()
