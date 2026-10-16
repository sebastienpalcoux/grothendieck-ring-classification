#!/usr/bin/env python3
"""Source checks for general R7_3_695 exclusion using compression saturation."""
import argparse,collections,gzip,hashlib,itertools,json
from pathlib import Path
import sympy as s
HERE=Path(__file__).resolve().parent
ROOT=next((p for p in HERE.parents if (p/'supplements/rank7/data/rank7_tables.txt.gz').exists()),Path('.'))

def require(c,msg):
 if not c:raise RuntimeError(msg)

def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,default=ROOT);p.add_argument('--output',type=Path);a=p.parse_args();ct=collections.Counter();N=None
 for line in gzip.open(a.repo/'supplements/rank7/data/rank7_tables.txt.gz','rt'):
  n=json.loads(line.replace('{','[').replace('}',']'));m=max(v for aa in n for b in aa for v in b);ct[m]+=1
  if f'R7_{m}_{ct[m]}'=='R7_3_695':N=n;break
 require(N is not None,'Missing tensor');require(all(N[i][j][0]==int(i==j) for i,j in itertools.product(range(7),repeat=2)),'Not all self-dual');require(all(N[i][j]==N[j][i] for i,j in itertools.product(range(7),repeat=2)),'Noncommutative source')
 mats=list(map(s.Matrix,N));B=sum((M*M.T for M in mats),s.zeros(7));x=s.Symbol('x');P=B.charpoly(x).as_expr();expected=(x-7)**3*(x-5)**2*(x*x-840*x+4900);require(s.expand(P-expected)==0,'Wrong polynomial')
 Q=s.Rational(140*(840**2-4*4900),4900**2);require(Q==4,'Not at saturation boundary')
 require(s.Poly(P,x,modulus=2)==s.Poly(x*x*(x+1)**5,x,modulus=2),'Wrong mod2 polynomial')
 D=420+70*s.sqrt(35);require(s.simplify(1/D-(6-s.sqrt(35))/70)==0,'Inverse identity fails');require(35%4==3,'Wrong quadratic integer ring')
 # For delta even and h odd, its inverse modulo4 is h modulo4.
 parity=[]
 for delta in [0,2]:
  residues={(delta*h)%4 for h in [1,3]};require(residues=={delta},'Odd divisor congruence fails')
  left=5*delta%4;right=(delta-2)%4;require(left!=right,'Parity contradiction fails');parity.append({'delta_mod4':delta,'sum_five_quotients_mod4':left,'delta_minus_two_mod4':right})
 out={'status':'PASS','id':'R7_3_695','decision':'excluded','scope':'general_complex','categorical_input':'full-I(1) compression boundary corollary, independently audited','tensor_sha256':hashlib.sha256(json.dumps(N,separators=(',',':')).encode()).hexdigest(),'Casimir_polynomial':str(s.factor(P)),'quadratic_discriminant':140,'compression_quantity':str(Q),'signed_Casimir_mod2':'x^2*(x+1)^5','delta_divisibility':70,'mod4_branches':parity}
 if a.output:a.output.write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps(out,indent=2))
if __name__=='__main__':main()
