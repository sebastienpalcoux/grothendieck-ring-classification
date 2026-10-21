"""Exact Frobenius-type diagnostic, restricted to weakly group-theoretical models.

ENO, Weakly group-theoretical and solvable fusion categories, Theorem1.5:
weakly group-theoretical categories have the strong Frobenius property.
Failure here is NOT a general complex categorification exclusion.
"""
import argparse,json
import sympy as s
from m3_campaign import OUT,write,require
from rings import Characters
from exact import t,vector

def check(row,profile):
 out={'id':row['id'],'tensor_sha256':row['tensor_sha256'],'stage':'strong_frobenius_weak_group_theoretical','scope':'weakly_group_theoretical_models_only','outcome':'no_conclusion'}
 if profile.get('integral'):
  D=profile['global_dimension'];ds=profile['fp_dimensions'];bad=[{'object':i,'quotient':str(s.Rational(D,d))} for i,d in enumerate(ds) if D%d]
  out.update(exact_fp_dimensions=ds,exact_global_dimension=D,failed_objects=bad)
 elif row['commutative']:
  a=Characters(row['tensor']);f,K,ds,D,pD,e=a.fp();u=K(s.Poly(t,t).rem(f).all_coeffs());bad=[]
  for i,d in enumerate(ds):
   q=D/d;M=s.Matrix.hstack(*(vector(q*u**j,f.degree()) for j in range(f.degree())));p=M.charpoly(t).as_poly()
   if any(x.q!=1 for x in p.all_coeffs()):bad.append({'object':i,'quotient_characteristic_polynomial':[str(x) for x in p.all_coeffs()]})
  out['failed_objects']=bad
 else:
  out.update(outcome='implementation_ineligible',reason='Nonintegral noncommutative FP-field quotient not implemented in this diagnostic.');return out
 if bad:out['outcome']='family_excluded'
 return out

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');ap.add_argument('--verify',action='store_true',help='Read-only exact replay (the default).');args=ap.parse_args();rows=json.loads((OUT/'survivors_m3.json').read_text());profiles={x['id']:x for x in json.loads((OUT/'survivor_profiles.json').read_text())};records=[check(r,profiles[r['id']]) for r in rows];path=OUT/'frobenius_results.json'
 if args.write:write(path.name,records)
 else:require(json.loads(path.read_text())==records,'Frobenius diagnostic differs')
 print('PASS Frobenius scoped diagnostic',len(records),'records;',sum(x['outcome']=='family_excluded' for x in records),'weak-GT family negatives')
if __name__=='__main__':main()
