#!/usr/bin/env python3
"""Five general exclusions by cyclic-stabilizer divisibility; exact source replay."""
import argparse,collections,gzip,hashlib,itertools,json
from pathlib import Path
import sympy as s
HERE=Path(__file__).resolve().parent
ROOT=next((p for p in HERE.parents if (p/'supplements/rank7/data/rank7_tables.txt.gz').exists()),Path('.'))
def require(c,m):
 if not c:raise RuntimeError(m)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,default=ROOT);ap.add_argument('--output',type=Path);args=ap.parse_args()
 rt=s.sqrt(5);base=[1,1,6+3*rt,8+3*rt,5+3*rt,7+3*rt,7+3*rt]
 specs={'R7_4_1212':(2,(2,2,3),base),'R7_4_1213':(2,(2,2,3),base),'R7_4_1438':(2,(2,2,2),base),'R7_4_1440':(2,(2,2,2),base),'R7_4_2731':(3,(3,3,3),[1,1,1,5+s.sqrt(13),5+s.sqrt(13),3,4+2*s.sqrt(13)])}
 ct=collections.Counter();out=[];x=s.Symbol('x')
 for line in gzip.open(args.repo/'supplements/rank7/data/rank7_tables.txt.gz','rt'):
  if not line.strip():continue
  n=json.loads(line.replace('{','[').replace('}',']'));m=max(z for a in n for b in a for z in b);ct[m]+=1;rid=f'R7_{m}_{ct[m]}'
  if rid not in specs:continue
  p,(i,j,k),ds=specs[rid];ds=list(map(s.sympify,ds));g=1
  require(all(d.is_positive for d in ds),'Nonpositive dimension')
  require(all(s.expand(ds[a]*ds[b]-sum(n[a][b][c]*ds[c] for c in range(7)))==0 for a,b in itertools.product(range(7),repeat=2)),'Not a dimension character')
  require(ds[0]==ds[g]==1 and s.Matrix(n[g])**p==s.eye(7) and s.Matrix(n[g])!=s.eye(7),'Invalid prime order subgroup')
  for a in (i,j,k):
   require(n[g][a]==[int(c==a) for c in range(7)] and n[a][g]==[int(c==a) for c in range(7)],'Target/witness not fixed on both sides')
  mp=s.Poly(s.minpoly(ds[k]/p,x),x).monic()
  require(any(c.q!=1 for c in mp.all_coeffs()),'Quotient is integral')
  require(n[i][j][k]%p!=0,'Multiplicity divisible by p')
  out.append({'id':rid,'scope':'general_complex','decision':'excluded','prime':p,'generator':g,'witness':[i,j,k],'coefficient':n[i][j][k],'FP_dimensions':list(map(str,ds)),'quotient_minimal_polynomial':str(mp.as_expr()),'tensor_sha256':hashlib.sha256(json.dumps(n,separators=(',',':')).encode()).hexdigest()})
 require(len(out)==len(specs),'Missing cases');result={'status':'PASS','general_exclusions':5,'method':'cyclic-stabilizer bimodule divisibility','cases':out}
 if args.output:args.output.write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result,indent=2))
if __name__=='__main__':main()
