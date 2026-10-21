"""Exact quadratic relative traces with rational total dimension."""
import sys,math
from fractions import Fraction as Q
def install():
 import higher_traces as ht
 if getattr(ht.quadratic_data,'_supports_weak_quadratic',False):return
 original=ht.quadratic_data
 def data(R,gram_prune=False):
  ch=ht.Characters(R);f,K,ds,D,pD,emb=ch.fp()
  if f.degree()!=2 or pD.degree()!=1:return original(R,gram_prune)
  co=list(map(int,f.all_coeffs()));disc=co[1]**2-4*co[2]
  ht.require(disc>0,'weak integral FP field not real quadratic')
  fac=ht.s.factorint(disc);q=math.prod(int(p) for p,e in fac.items() if e%2)
  h=math.isqrt(disc//q);F=q if q%4==1 else 4*q
  def coords(x):
   z=[Q(str(c)) for c in ht.ec(x)];z=[Q(0)]*(2-len(z))+z
   return z[1]-Q(co[1],2)*z[0],Q(h,2)*z[0]
  d=list(map(coords,ds));dd=coords(D)
  ht.require(dd[1]==0 and dd[0].denominator==1 and dd[0]>0,'rational total FP dimension invalid')
  roots=ht.discover_roots(ht.codegree_poly(R),K)
  if roots is None:return None
  ht.check_roots(ht.codegree_poly(R),K,roots);rest=list(roots);rest.remove(D)
  cs=[ht.restriction_columns(ds,D/r,K,ch.C) for r in rest]
  lows=ht.low_matrices(cs,ch.C,gram_prune=gram_prune) if all(cs) else []
  primes=sorted(map(int,ht.s.factorint(dd[0].numerator)))
  ht.require(all(int(p) in primes for p in ht.s.factorint(F)),'quadratic conductor outside Cauchy prime support')
  return {'ch':ch,'factor':f,'K':K,'ds':ds,'D':D,'embedding':emb,'q':q,'conductor':F,'dimensions':d,'global_dimension':dd,'primes':primes,'columns':cs,'lows':lows}
 data._supports_weak_quadratic=True
 import balanced_traces,tensor_rotation,character_induction,spectral_induction,modular_character_induction
 for name in ['higher_traces','balanced_traces','tensor_rotation','character_induction','spectral_induction','modular_character_induction']:
  module=sys.modules[name]
  if hasattr(module,'quadratic_data'):module.quadratic_data=data
