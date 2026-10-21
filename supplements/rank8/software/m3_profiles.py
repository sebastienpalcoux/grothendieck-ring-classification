"""Exact structural metadata and explicitly labelled numerical FP profiles."""
import os
for _k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS'):os.environ[_k]='1'
import argparse,concurrent.futures,json
import numpy as np
import sympy as s
from m3_campaign import OUT,write
from analyze import dual,proper_closed_subrings,casimir_poly,commutes

def profile(row):
 R=row['tensor'];du=dual(R);A=np.asarray(R,dtype=float);P=A.sum(axis=0);vals,vecs=np.linalg.eig(P);j=max(range(8),key=lambda j:vals[j].real);v=vecs[:,j].real;v=v/v[0];D=float(v@v)
 inv=[i for i in range(8) if sum(R[i][du[i]])==1];sub=[{'basis':list(J),'rank':len(J),'multiplicity':max(x for M in S for r in M for x in r)} for J,S in proper_closed_subrings(R,max_rank=7)]
 out={'id':row['id'],'tensor_sha256':row['tensor_sha256'],'commutative':commutes(R),'dual':du,'invertibles':inv,'invertible_count':len(inv),'fp_dimensions_approx':[float(x) for x in v],'global_dimension_approx':D,'proper_subrings':sub,'casimir_factors':[{'coefficients':list(map(int,p.all_coeffs())),'multiplicity':int(e)} for p,e in casimir_poly(R).factor_list()[1]]}
 ds=[int(round(x)) for x in v]
 if all(x>0 for x in ds) and all(sum(R[i][j][k]*ds[k] for k in range(8))==ds[i]*ds[j] for i in range(8) for j in range(8)):
  out.update(fp_dimensions=ds,global_dimension=sum(x*x for x in ds),integral=True,fp_exact_scope='positive integral ring homomorphism, verified in all64 products')
 else:
  out['integral']=False
  if out['commutative']:
   from rings import Characters
   from exact import pc,ec
   a=Characters(R);f,K,ds,D,pD,e=a.fp();out.update(fp_field_polynomial=pc(f),fp_dimensions_exact=[ec(x) for x in ds],global_dimension_exact=ec(D),global_dimension_polynomial=pc(pD),fp_generator=a.k,fp_exact_scope='exact algebraic-field coordinates; designated positive real embedding')
 return out

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--jobs',type=int,default=6);args=ap.parse_args();rows=json.loads((OUT/'survivors_baseline.json').read_text())
 with concurrent.futures.ProcessPoolExecutor(max_workers=args.jobs) as pool:out=list(pool.map(profile,rows))
 write('survivor_profiles.json',out);print('PROFILED',len(out))
if __name__=='__main__':main()
