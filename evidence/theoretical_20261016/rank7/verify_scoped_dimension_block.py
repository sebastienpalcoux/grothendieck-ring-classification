#!/usr/bin/env python3
"""Exact source checks for THREE PIVOTAL-ONLY exclusions. No general decisions."""
import argparse,collections,gzip,hashlib,json
from pathlib import Path
import sympy as s
HERE=Path(__file__).resolve().parent
ROOT=next((p for p in HERE.parents if (p/'supplements/rank7/data/rank7_tables.txt.gz').exists()),Path('.'))

def require(x,msg):
 if not x:raise RuntimeError(msg)

def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,default=ROOT);p.add_argument('--output',type=Path);a=p.parse_args();x=s.Symbol('x')
 specs={'R7_3_695':(840,4900,140,[5,7],None),'R7_3_783':(240,900,60,[6,15],4),'R7_3_1015':(240,900,60,[6,15],5)};ct=collections.Counter();out=[]
 for line in gzip.open(a.repo/'supplements/rank7/data/rank7_tables.txt.gz','rt'):
  N=json.loads(line.replace('{','[').replace('}',']'));m=max(v for r in N for row in r for v in row);ct[m]+=1;rid=f'R7_{m}_{ct[m]}'
  if rid not in specs:continue
  tr,norm,disc,ints,fixed=specs[rid];mats=list(map(s.Matrix,N));C=sum((m*m.T for m in mats),s.zeros(7));pol=C.charpoly(x).as_expr();f=x*x-tr*x+norm
  factors=s.factor_list(pol)[1]
  require(set(str(z) for z,e in factors)==set([str(x-k) for k in ints]+[str(f)]),'Unexpected Casimir factorization')
  dual=[next(j for j in range(7) if N[i][j][0]) for i in range(7)]
  if fixed is None:require(dual==list(range(7)),'Expected all self-dual')
  else:
   for g in [1,2]:require(all(N[g][fixed][j]==int(j==fixed) for j in range(7)),'gE=E fails')
   orbit=set(range(7))-{0,1,2,fixed}
   require(all(sum(N[g][i][j] for j in orbit)==1 for g in [1,2] for i in orbit),'Orbit not preserved')
   require({next(j for j in range(7) if N[g][min(orbit)][j]) for g in [0,1,2]}==orbit,'Orbit not transitive')
   require(dual[fixed]==fixed and all(dual[i] in orbit for i in orbit),'Unexpected duality')
  require(all(s.Rational(k*k,norm).q!=1 for k in ints),'Rational categorical dimension branch not excluded')
  lhs=s.Rational(tr*tr-4*norm,norm*norm);rhs=s.Rational(1,disc)
  require(lhs>rhs,'No strict dimension-block violation')
  out.append({'id':rid,'scope':'pivotal_only','general_conclusion_from_this_test':'none','Casimir_polynomial':str(s.factor(pol)),'FP_dimension_polynomial':str(f),'quadratic_field_discriminant':disc,'dimension_block_left':str(lhs),'dimension_block_bound':str(rhs),'rational_dimension_norm_obstructions':{str(k):str(s.Rational(k*k,norm)) for k in ints},'tensor_sha256':hashlib.sha256(json.dumps(N,separators=(',',':')).encode()).hexdigest()})
 require(len(out)==3,'Missing source cases');res={'status':'PASS','new_general_exclusions':0,'pivotal_only_exclusions':3,'source':'Schopieray arXiv:2609.35287v1, Theorem5.1','cases':out}
 if a.output:a.output.write_text(json.dumps(res,indent=2)+'\n')
 print(json.dumps(res,indent=2))
if __name__=='__main__':main()
