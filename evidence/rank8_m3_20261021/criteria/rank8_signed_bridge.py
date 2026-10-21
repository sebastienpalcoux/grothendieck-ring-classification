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
 ac.verify=verify;oe.nc_certificate=nc;ac._complete_oriented_lift=complete;ac._rank8_signed_bridge_installed=True
