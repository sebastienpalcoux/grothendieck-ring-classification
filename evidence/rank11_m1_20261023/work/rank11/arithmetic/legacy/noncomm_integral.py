from arithmetic import *

def test(R):
 ds=integral_dimensions(R)
 if ds is None:return None
 D=sum(d*d for d in ds);bad=[];factors=[]
 for q,m in casimir(R).charpoly(t).as_poly().factor_list()[1]:
  co=list(map(int,q.all_coeffs()));factors.append([co,m])
  if q.degree()!=1:
   return dict(kind='noncomm_integral_drinfeld',dims=ds,global_dimension=D,failed_factor=co,multiplicity=m,reason='nonlinear_Casimir_factor')
  lam=-co[-1];allowed=[e for e in range(1,s.integer_nthroot(m,2)[0]+1) if lam%e==0 and D%(lam//e)==0]
  reachable={0}
  for j in range(1,m+1):
   if any(j-e*e in reachable for e in allowed):reachable.add(j)
  if m not in reachable:
   return dict(kind='noncomm_integral_drinfeld',dims=ds,global_dimension=D,failed_factor=co,multiplicity=m,allowed_irrep_degrees=allowed,reachable_multiplicities=sorted(reachable),reason='no_square_partition')
 return None

def main():
 out=[]
 for r in read():
  R=r['tensor']
  if comm(R):continue
  c=test(R)
  out.append(dict(id=r['id'],rank=r['rank'],tensor_sha256=r['tensor_sha256'],certificate=c))
  if c:print(r['id'],c,flush=True)
 (HERE/'noncomm_integral.json').write_text(json.dumps(out,indent=2)+'\n')
 print('TOTAL',len(out),'EXCLUSIONS',sum(x['certificate'] is not None for x in out))
if __name__=='__main__':main()
