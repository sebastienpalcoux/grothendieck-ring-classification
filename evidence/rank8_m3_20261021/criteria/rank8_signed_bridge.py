"""Exact rank-eight signed quotient adapter; complete enumeration is retained."""
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'noncommutative'))
from scalar_sieve import signed_component_certificate
def install():
 import weak_integral_quadratic,accelerated
 weak_integral_quadratic.install();accelerated.install()
 import advanced_criteria as ac,oriented_extension as oe,proofs
 if getattr(ac,'_rank8_signed_bridge_installed',False):return
 from oriented_signed import enumerate_all,from_values
 from rings import Characters
 from exact import pc,require
 original=oe.nc_certificate
 old_eligibility=ac.eligibility
 def eligibility(R,mode='dimension_order',height=6):
  info=old_eligibility(R,mode,height)
  if info.get('reason')!='current quadratic trace implementation requires irrational total dimension':return info
  # The additive weak-integral adapter supplies the previously missing exact
  # rational-total-dimension formulas; retain all remaining mode hypotheses.
  if mode=='tensor_rotation':return dict(info,eligible=True,reason='exact weak-integral quadratic relative traces')
  from itertools import combinations
  a=Characters(R);f,K,ds,D,pD,e=a.fp();factors={i:a.N[i].charpoly().as_poly().factor_list()[1] for i in range(1,len(R))}
  labels=[i for i,ff in factors.items() if all(g.degree()<=2 for g,m in ff)]
  seeds=[list(seed) for size in (1,2) for seed in combinations(labels,size) if ac.generated_basis(R,seed) is not None]
  if not seeds:return dict(info,reason='no one- or two-object quadratic-spectrum generating set')
  if mode=='modular':
   q=ac._squarefree_discriminant(f)
   for ff in factors.values():
    for g,m in ff:
     if g.degree()>2 or (g.degree()==2 and ac._squarefree_discriminant(g)!=q):return dict(info,reason='a character field lies outside the relative trace field')
  return dict(info,eligible=True,generating_sets=seeds,reason='exact weak-integral quadratic character traces')
 def nc(R,T):return signed_component_certificate(R,T) if len(R)==8 else original(R,T)
 def complete(R,sphere,timeout):
  a=Characters(R);f,K,ds,D,pD,e=a.fp()
  gate='weak_integrality' if pD.degree()==1 else 'two_FP_values' if len(set(ds))==2 else None
  if gate:return {'kind':'rank8_spherical_reduction','gate':gate,'sphere':sphere}
  vals,problem,stats=enumerate_all(R,timeout);branches=[]
  for values in vals:
   T=from_values(R,problem,values);branch={'values':list(values)}
   parity=proofs.signed_adjoint_parity(R,T);gauge=proofs.gauge_original(T,R)
   if parity is not None:branch['obstruction']=parity
   elif gauge is not None:branch['obstruction']={'kind':'gauge_original','signs':gauge}
   elif any(T[i][j]!=T[j][i] for i in range(len(T)) for j in range(len(T))):
    cert=nc(R,T)
    if cert is None:return None
    branch['noncommutative']=cert
   else:
    a=Characters(T);characters=[{'factor':pc(f),'obstruction':proofs.signed_component_certificate(R,T,a,f,sphere)} for f,m in a.components]
    if any(c['obstruction'] is None for c in characters):return None
    branch.update(characters=characters,generator=a.k)
   branches.append(branch)
  return {'kind':'oriented_signed','sphere':sphere,'branches':branches}
 oldverify=ac.verify
 def verify(R,c):
  if c['kind']!='rank8_spherical_reduction':return oldverify(R,c)
  a=Characters(R);f,K,ds,D,pD,e=a.fp()
  require((c['gate']=='weak_integrality' and pD.degree()==1) or (c['gate']=='two_FP_values' and len(set(ds))==2),'invalid Galois/pseudo-unitary reduction')
  oe.check_sphere(R,c['sphere'],oe.pseudo_check)
 ac.verify=verify;ac.eligibility=eligibility;oe.nc_certificate=nc;ac._complete_oriented_lift=complete;ac._rank8_signed_bridge_installed=True
