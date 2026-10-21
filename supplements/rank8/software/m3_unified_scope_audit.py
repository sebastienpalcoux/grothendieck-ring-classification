"""Complete scoped attempt inventory for the two cheap unified criteria.

This records completed no-conclusion outcomes and explicit inapplicability;
it does not infer success from the absence of an exclusion certificate.
"""
import os
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS'):os.environ[k]='1'
import argparse,concurrent.futures,json,sys
from m3_campaign import OUT,REPO,write,require
sys.path.insert(0,str(OUT.parent/'criteria'))

def run(row):
 import negative_subring,quadratic_compression
 from analyze import proper_closed_subrings,casimir_poly
 R=row['tensor'];base={'id':row['id'],'tensor_sha256':row['tensor_sha256'],'scope':'general_complex_fusion_category'};out=[]
 eligible=[list(J) for J,S in proper_closed_subrings(R,max_rank=7) if len(J) in (6,7)]
 if eligible:
  c=negative_subring.discover(R)
  out.append(dict(base,stage='expanded_exact_negative_subring_transfer',outcome='excluded' if c else 'no_conclusion',eligible_subsets=eligible,**({'certificate':c} if c else {})))
 else:out.append(dict(base,stage='expanded_exact_negative_subring_transfer',outcome='scope_inapplicable',reason='No closed based subring of rank6or7 exists.'))
 quadratics=[list(map(int,p.all_coeffs())) for p,m in casimir_poly(R).factor_list()[1] if p.degree()==2]
 if quadratics:
  c=quadratic_compression.discover(R)
  out.append(dict(base,stage='multiquadratic_casimir_compression',outcome='excluded' if c else 'no_conclusion',quadratic_factors=quadratics,**({'certificate':c} if c else {})))
 else:out.append(dict(base,stage='multiquadratic_casimir_compression',outcome='scope_inapplicable',reason='Regular Casimir polynomial has no irreducible quadratic factor.'))
 return out

def main():
 p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');p.add_argument('--jobs',type=int,default=4);args=p.parse_args();rows=json.loads((OUT/'survivors_m3.json').read_text())
 with concurrent.futures.ProcessPoolExecutor(max_workers=args.jobs) as pool:result=[a for pair in pool.map(run,rows) for a in pair]
 dest=OUT/'unified_scope_attempts.json'
 if args.write:write(dest.name,result)
 else:require(json.loads(dest.read_text())==result,'unified scoped attempt replay differs')
 print('PASS unified scoped attempts',len(rows),'tensors',len(result),'records')
if __name__=='__main__':main()
