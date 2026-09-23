"""Short noncommuting-automorphism certificates for noncyclotomic fields."""
import itertools,json
from pathlib import Path
import sympy as s
from exact import require
x=s.Symbol('x')
def coeff(p):return [str(c) for c in p.all_coeffs()]
def parse(v):return s.Poly.from_list([s.Rational(c) for c in v],x,domain=s.QQ)
def compose(a,b,f):return a.compose(b).rem(f)
def certificate(R):
 n=len(R)
 if not all(R[i][j]==R[j][i] for i in range(n) for j in range(n)):return None
 for i in range(1,n):
  ff=s.Matrix(R[i]).charpoly(x).as_poly().factor_list()[1]
  for f,m in ff:
   if not 3<=f.degree()<=6:continue
   K=s.QQ.alg_field_from_poly(f);fac=s.Poly(f,x,domain=K).factor_list()[1];roots=[]
   for p,e in fac:
    if p.degree()==1:
     a=-p.rep.to_list()[-1]/p.rep.to_list()[0]
     roots.append(s.Poly.from_list([s.Rational(v.numerator,v.denominator) for v in a.to_list()],x,domain=s.QQ))
   for a,b in itertools.combinations(roots,2):
    if compose(a,b,f)!=compose(b,a,f):
     return {'kind':'noncommuting_field_automorphisms','object':i,'factor':coeff(f),'automorphisms':[coeff(a),coeff(b)],'commutator_difference':coeff(compose(a,b,f)-compose(b,a,f))}
 return None
def verify(R,c):
 n=len(R);require(c['kind']=='noncommuting_field_automorphisms','wrong field certificate');require(all(R[i][j]==R[j][i] for i in range(n) for j in range(n)),'commutativity required');i=c['object'];require(type(i) is int and 0<i<n,'bad object index');f=parse(c['factor']);p=s.Matrix(R[i]).charpoly(x).as_poly();require(f.is_irreducible and not p.rem(f),'not an irreducible character factor');a,b=map(parse,c['automorphisms']);require(not compose(f,a,f) and not compose(f,b,f),'map is not a field endomorphism');v=compose(a,b,f)-compose(b,a,f);require(v and coeff(v)==c['commutator_difference'],'automorphisms commute or bad witness')
if __name__=='__main__':
 import argparse
 P=Path(__file__).resolve().parents[1]
 ap=argparse.ArgumentParser(description=__doc__)
 ap.add_argument('--discover',action='store_true',help='search census tensors instead of verifying frozen certificates')
 ap.add_argument('--bound',type=int,default=3,help='maximum exact multiplicity for discovery')
 ap.add_argument('--out',type=Path,help='new output path for discovery; may not overwrite an existing file')
 args=ap.parse_args();rows=json.load(open(P/'data/census.json'));by={r['id']:r['N'] for r in rows}
 if not args.discover:
  records=json.load(open(P/'certificates/continuation_fields.json'))
  for rec in records:verify(by[rec['id']],rec['certificate'])
  print('EXACT FROZEN CERTIFICATES VERIFIED',len(records))
 else:
  if args.out is None:ap.error('--discover requires --out with a new file path')
  if args.out.exists():ap.error('refusing to overwrite an existing output')
  out=[]
  for r in rows:
   if r['m']>args.bound:continue
   c=certificate(r['N'])
   if c:
    verify(r['N'],c);out.append({'id':r['id'],'status':'excluded','certificate':c});print(r['id'],flush=True)
  args.out.parent.mkdir(parents=True,exist_ok=True)
  with args.out.open('x') as f:json.dump(out,f,indent=2);f.write('\n')
  print('NEW CERTIFICATES',len(out))
