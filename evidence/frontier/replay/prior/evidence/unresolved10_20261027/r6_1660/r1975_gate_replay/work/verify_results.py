"""Exact replay of the selected first-pass classification certificates."""
from common import *
from exact import *
from arithmetic import casimir,near_group,verify_dnumber,comm,integral_dimensions
from scalar_characters import chars
from spectrum_verify import verify as verify_spectrum
import sympy as s,itertools,collections,os,time,math
from concurrent.futures import ProcessPoolExecutor,as_completed
import multiprocessing as mp
CORPUS=None
def initialize():
 global CORPUS
 CORPUS=load('verification_corpus.json')
def check_integral(R,c):
 ds=c['dims'];n=len(R);D=sum(x*x for x in ds);assert ds[0]==1 and all(type(x)is int and x>0 for x in ds)
 assert all(sum(R[i][j][k]*ds[k]for k in range(n))==ds[i]*ds[j]for i,j in itertools.product(range(n),repeat=2));assert D==c['global_dimension']
 B=casimir(R);f=poly(c.get('failed_factor'));assert B.charpoly(t).as_poly().rem(f).is_zero
 if c['kind']=='integral_drinfeld':assert comm(R)and(f.degree()>1 or D%int(-f.TC()))
 else:
  if f.degree()>1:return
  m=c['multiplicity'];lam=int(-f.TC());allowed=[e for e in range(1,math.isqrt(m)+1)if lam%e==0 and D%(lam//e)==0];reachable={0}
  for j in range(1,m+1):
   if any(j-e*e in reachable for e in allowed):reachable.add(j)
  assert m not in reachable
def check_index_or_cyclic(R,c):
 a=chars(R);f,K,ds,D,pD,emb=a.fp();u=K(s.Poly(t,t).rem(f).all_coeffs());n=len(R)
 if c['kind']=='subring_index':
  J=c['subset'];assert all(a.du[i]in J for i in J);assert all(not R[i][j][k]for i in J for j in J for k in range(n)if k not in J)
  q=D/sum((ds[i]*ds[a.du[i]]for i in J),K.zero)
 else:
  g=c['g'];order=c['order'];x,y,z=c['triple'];v=g;k=1
  while v:v=R[v][g].index(1);k+=1
  assert order==k and R[g][x][x]and R[y][g][y]and R[g][z][z]and R[z][g][z]
  m=R[x][y][z];assert m==c['multiplicity']and m>0
  q=K(s.Rational(math.gcd(order,m),order))*ds[z]
 p=s.Matrix.hstack(*(vector(q*u**i,f.degree())for i in range(f.degree()))).charpoly(t).as_poly();assert pc(p)==c['polynomial']and any(v.q!=1 for v in p.all_coeffs())
def check_spherical_report(R,report):
 from sphere import analyse
 actual=analyse(R,low=False);assert actual['spherical_excluded']and report['spherical_excluded'];assert actual['branches']==report['branches']
def check_signed(R,report):
 from signed_pb import FiniteProblem
 from signed_sieve import tensor,original_gauge
 from sphere import char_obstruction
 P=FiniteProblem(R,timeout=60000);src=chars(R);spherical_checked=False
 for b in report['branches']:
  values=b['values'];T=tensor(R,P.mapping,values);c=b['obstruction'];kind=c['kind']
  if kind=='original_gauge':
   assert original_gauge(R,T)is not None
   if not spherical_checked:check_spherical_report(R,c['spherical_report']);spherical_checked=True
  elif kind=='casimir_dnumber':verify_dnumber(T,c)
  elif kind=='all_signed_scalar_characters_excluded':
   a=chars(T);assert len(a.components)==len(c['characters'])
   for(f,e),branch in zip(a.components,c['characters']):assert pc(f)==branch['factor']and char_obstruction(a,f,list(src.cf)+list(a.cf))is not None
  else:raise ValueError('unknown signed obstruction '+kind)
  if 'gauge_orbit_size'in b:P.block_gauge_orbit(values)
  else:P.block(values)
 assert str(P.check())=='unsat','independent signed completeness replay did not return UNSAT'
def check(rid):
 row=CORPUS['ledger'][rid];R=CORPUS['tensors'][rid];assert digest(R)==row['tensor_sha256'];status=row['status']
 if status=='unresolved':return {'id':rid,'status':'PASS','scope':'no exclusion or model claimed'}
 if status=='unitarily_realized':
  for m in CORPUS['models'][rid]:
   T=m['tensor'];p=m['basis_map_source_to_model'];n=len(R);assert p[0]==0 and sorted(p)==list(range(n));assert all(R[i][j][k]==T[p[i]][p[j]][p[k]]for i,j,k in itertools.product(range(n),repeat=3))
  return {'id':rid,'status':'PASS','scope':'exact known-model tensor and unitary existence reference'}
 pr=CORPUS['proofs'][rid];path=row['exclusion_certificates'][0]['record_file'];stem=Path(path).stem
 if stem in ['baseline','structural']:
  c=pr['certificates'][0];kind=c['kind']
 elif stem in ['zero_spectrum','one_spectrum','established_scan','remaining_arithmetic']:c=pr['certificate'];kind=c['kind']
 elif stem in ['signed_sieve','pb_scan']:check_signed(R,pr['report']);return {'id':rid,'status':'PASS','scope':'all oriented signed branches, with independent exact Boolean completeness replay'}
 elif stem=='module_scan':
  from module_smt import discover
  c=next(c for c in pr['reports']if c['outcome']=='excluded');assert discover(R,c['involution'],timeout=60000)['outcome']=='excluded';return {'id':rid,'status':'PASS','scope':'complete parity-bounded involution-module system'}
 elif stem=='induction_smt_scan':
  from induction_smt import discover
  assert pr['general_gate']in ['weak_integrality','two_FP_values'];a=chars(R);f,K,ds,D,pD,e=a.fp();assert pD.degree()==1 or len(set(ds))==2
  assert discover(R,timeout_ms=60000)['outcome']=='excluded';return {'id':rid,'status':'PASS','scope':'exact low-induction necessary conditions after verified general reduction'}
 elif stem=='weighted_scan':
  from weighted_smt import discover
  actual=discover(R,timeout=60000);assert actual['outcome']=='excluded';assert actual['gate']in ['weak_integrality','two_FP_values'];return {'id':rid,'status':'PASS','scope':'exact multiplicity-weighted induction with categorical dimensions D/f_E'}
 elif stem in ['advanced_scan','advanced_native_retry']:
  import importlib
  mode=pr['mode'];mod=importlib.import_module({'morita':'full_morita_gram','spectral_module':'new_module_spectral','rotation':'tensor_rotation','character':'character_induction','modular':'modular_character_induction','integer_gram':'integer_gram'}[mode]);mod.verify(R,pr['certificate'])
  if mode not in ['morita','spectral_module']:
   a=chars(R);f,K,ds,D,pD,e=a.fp();assert pD.degree()==1 or len(set(ds))==2
  return {'id':rid,'status':'PASS','scope':'established advanced criterion with exact certificate replay'}
 else:raise ValueError('unrecognized proof file '+stem)
 if kind=='casimir_dnumber':verify_dnumber(R,c)
 elif kind=='cyclotomic':check_cyclotomic([s.Matrix(A).charpoly(t).as_poly()for A in R],c)
 elif kind=='near_group_small_m':assert near_group(R)==c
 elif kind in ['integral_drinfeld','noncomm_integral_drinfeld']:check_integral(R,c)
 elif kind=='excluded_lower_subring':
  J=c['subset'];n=len(R);S=[[[R[i][j][k]for k in J]for j in J]for i in J];assert digest(S)==c['subtensor_sha256']and len(J)==c['subrank'];du=[next(j for j in range(n)if R[i][j][0])for i in range(n)]
  assert all(du[i]in J for i in J)and all(not R[i][j][k]for i in J for j in J for k in range(n)if k not in J)
  assert not any(based_iso(S,m['tensor'])is not None for m in CORPUS['lower_models']if len(m['tensor'])==len(J)and coarse(S)==coarse(m['tensor']))
 elif kind in ['zero_spectrum','one_spectrum']:verify_spectrum(R,c)
 elif kind in ['subring_index','cyclic_isotypic_integrality']:check_index_or_cyclic(R,c)
 elif kind=='involution_module':
  import involution_module
  involution_module.verify(R,c)
 else:raise ValueError('unimplemented certificate replay '+kind)
 return {'id':rid,'status':'PASS','scope':'exact '+kind}
def main():
 global math
 import math
 ledger=load('ledger.json');raw={r['id']:r['tensor']for r in read()if r['multiplicity']==2};proofs={};models=collections.defaultdict(list);cache={}
 for r in ledger:
  if r['status']=='excluded':
   f=r['exclusion_certificates'][0]['record_file'].replace('work/','')
   if f not in cache:cache[f]={x['id']:x for x in load(f)}
   proofs[r['id']]=cache[f][r['id']]
  if r['status']=='unitarily_realized':
   for m in r['models']:models[r['id']].append(load(m['record_file'].replace('work/',''))[m['record_index']])
 corpus={'ledger':{r['id']:r for r in ledger},'tensors':raw,'proofs':proofs,'models':dict(models),'lower_models':load('lower_positive_registry.json')}
 fresh='--fresh'in sys.argv
 out=[];todo=[];previous=load('verification_corpus.json')if not fresh and(BASE/'work/verification_corpus.json').exists()else{};previous_results={r['id']:r for r in load('verification_results.json')}if not fresh and(BASE/'work/verification_results.json').exists()else{}
 for r in ledger:
  rid=r['id'];old=previous.get('ledger',{}).get(rid);result=previous_results.get(rid)
  same=old is not None and result is not None and result['status']=='PASS'and old['status']==r['status']and old['tensor_sha256']==r['tensor_sha256']
  if same and r['status']=='excluded':same=old['exclusion_certificates'][0]==r['exclusion_certificates'][0]and previous.get('proofs',{}).get(rid)==proofs[rid]
  if same and r['status']=='unitarily_realized':same=previous.get('models',{}).get(rid)==models[rid]
  if same:out.append(dict(result,classification_status=r['status'],reused_exact_certificate_replay=True))
  else:todo.append(r)
 save('verification_corpus.json',corpus);start=time.time();print('REUSE',len(out),'FRESH',len(todo),flush=True)
 with ProcessPoolExecutor(max_workers=3,mp_context=mp.get_context('spawn'),initializer=initialize)as pool:
  futures={pool.submit(check,r['id']):r['id']for r in todo}
  for fut in as_completed(futures):
   try:r=fut.result()
   except Exception as e:r={'id':futures[fut],'status':'FAIL','error':repr(e)}
   r['classification_status']=corpus['ledger'][r['id']]['status'];out.append(r)
   if r['status']!='PASS':print('FAIL',r,flush=True)
   if len(out)%100==0:save('verification_results.json',out);print('CHECKED',len(out),'failed',sum(x['status']!='PASS'for x in out),'seconds',round(time.time()-start,2),flush=True)
 save('verification_results.json',out);print('FINAL',len(out),'failed',sum(x['status']!='PASS'for x in out),'seconds',time.time()-start,flush=True)
if __name__=='__main__':main()
